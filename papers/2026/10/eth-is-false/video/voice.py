"""Narration voice: a Piper (VITS) ONNX voice that reads each caption's spoken
text. Used by eth_video.py (clip durations set the pacing) and by
make_voiceover.py (the clips become the soundtrack).

The voiceover was made with BookVoice's American male narrator ("US-M1", key
eam), a designed voice (no real person cloned) trained on English-aware
phonemes. phoneme_ids() reproduces how the app phonemizes English text:
espeak-ng "en-us" clause by clause as in piper1-gpl, language flags removed,
punctuation kept, NFD codepoints, and English /aI/ written as Vietnamese "ai"
(a long a + j), the spelling that voice was trained on. Any standard English
Piper voice works too, e.g. en_US-ryan-high from
https://huggingface.co/rhasspy/piper-voices: a model whose config names an
English espeak voice is read with that voice and plain espeak phonemes.

    pip install piper-tts onnxruntime numpy
    python voice.py MODEL.onnx "Text to read." out.wav
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unicodedata
import wave
from pathlib import Path

EN_AI, VI_AI = "aɪ", "aːj"      # "aɪ" -> "aːj" (BookVoice's English-aware phonemes)


class Voice:
    def __init__(self, model: str | Path, cache_dir: str | Path, *, length_scale: float = 1.0,
                 noise_scale: float = 0.667, noise_w: float = 0.8):
        self.model = Path(model)
        self.config = json.loads(Path(f"{self.model}.json").read_text(encoding="utf-8"))
        self.sample_rate = self.config["audio"]["sample_rate"]
        self.id_map = self.config["phoneme_id_map"]
        self.scales = (noise_scale, length_scale, noise_w)
        # BookVoice's voices are configured with espeak "vi" and read English through "en-us"
        espeak_voice = self.config.get("espeak", {}).get("voice", "")
        self.plain_phonemes = espeak_voice.startswith("en")
        self.espeak_voice = espeak_voice if self.plain_phonemes else "en-us"
        self.cache_dir = Path(cache_dir)
        self._session = None
        self._espeak = None
        digest = hashlib.sha256()
        with open(self.model, "rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                digest.update(block)
        self.model_hash = digest.hexdigest()[:16]

    # text -> phoneme ids ------------------------------------------------------
    def phonemes(self, text: str) -> list[list[str]]:
        """Sentences of phoneme codepoints."""
        if self._espeak is None:
            from piper import espeakbridge
            from piper.phonemize_espeak import ESPEAK_DATA_DIR
            espeakbridge.initialize(str(ESPEAK_DATA_DIR))
            self._espeak = espeakbridge
        self._espeak.set_voice(self.espeak_voice)
        sentences, current = [], []
        for phonemes, terminator, end_of_sentence in self._espeak.get_phonemes(text):
            phonemes = re.sub(r"\([^)]+\)", "", phonemes) + terminator
            if not self.plain_phonemes:
                phonemes = phonemes.replace(EN_AI, VI_AI)
            if terminator in (",", ":", ";"):
                phonemes += " "
            current.extend(unicodedata.normalize("NFD", phonemes))
            if end_of_sentence:
                sentences.append(current)
                current = []
        if current:
            sentences.append(current)
        return sentences

    def phoneme_ids(self, text: str) -> list[int]:
        """[^ _ p1 _ p2 _ ... $] per sentence, concatenated (piper's phoneme_ids)."""
        ids, m = [], self.id_map
        for sentence in self.phonemes(text):
            ids += m["^"] + m["_"]
            for p in sentence:
                if p in m:
                    ids += m[p] + m["_"]
            ids += m["$"]
        return ids

    # phoneme ids -> audio, cached ----------------------------------------------
    def clip(self, text: str) -> Path:
        """WAV of `text` (mono, 16-bit, the model's rate). VITS samples a new take on
        every run, so the first take is cached and reused: the render and the
        soundtrack then hear the same clip."""
        ids = self.phoneme_ids(text)
        key = hashlib.sha1(json.dumps([self.model_hash, self.scales, ids]).encode()).hexdigest()[:20]
        path = self.cache_dir / f"{key}.wav"
        if path.exists():
            return path
        import numpy as np
        if self._session is None:
            import onnxruntime as ort
            self._session = ort.InferenceSession(str(self.model), providers=["CPUExecutionProvider"])
        x = np.array([ids], dtype=np.int64)
        feed = {"input": x, "input_lengths": np.array([x.shape[1]], dtype=np.int64),
                "scales": np.array(self.scales, dtype=np.float32)}
        names = {i.name for i in self._session.get_inputs()}
        if "sid" in names:
            feed["sid"] = np.array([0], dtype=np.int64)
        if "ru_slow" in names:          # BookVoice's paced packs: neutral pacing
            feed["ru_slow"] = np.ones((1, x.shape[1]), dtype=np.float32)
            feed["ru_syllables"] = np.array([len(text.split())], dtype=np.float32)
        audio = self._session.run(None, feed)[0].reshape(-1)
        pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(self.sample_rate)
            w.writeframes(pcm.tobytes())
        tmp.replace(path)               # atomic: scenes may render in parallel
        return path

    def duration(self, text: str) -> float:
        with wave.open(str(self.clip(text)), "rb") as w:
            return w.getnframes() / w.getframerate()


def voices_from_env(cache_root: str | Path) -> dict[str, Voice]:
    """NARRATION_VOICES="us-male=/path/a.onnx,us-female=/path/b.onnx", in that order;
    clips are cached in cache_root/<key>/. Empty when the variable is unset."""
    spec = os.environ.get("NARRATION_VOICES", "").strip()
    pairs = (item.split("=", 1) for item in spec.split(",") if item.strip())
    return {key.strip(): Voice(path.strip(), Path(cache_root) / key.strip()) for key, path in pairs}


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    model, text, out = sys.argv[1:]
    voice = Voice(model, Path(out).parent / ".voice-cache")
    print(" | ".join("".join(s) for s in voice.phonemes(text)))
    Path(out).write_bytes(voice.clip(text).read_bytes())
    print(f"{out}: {voice.duration(text):.2f} s")

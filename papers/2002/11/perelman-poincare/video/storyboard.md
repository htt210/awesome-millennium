# Video script: "Perelman's proof of the Poincaré conjecture"

*Written 3 November 2026 from the plain-language explainer ([`../README.md`](../README.md)).* This script is the source of the video's narration: each scene in [`poincare_video.py`](poincare_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `poincare_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end. The only formula on screen is Hamilton's equation (chapter 3); numbers are spoken in words.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A ball, drawn with shading. A loop of string lies on it and slides off, shrinking to a point. | Lay a loop of string on a ball and pull it tight. It slides off and shrinks to a point. |
| 0.2 | A doughnut. A loop through its hole tightens, but stays stuck around the hole. | On a doughnut, a loop through the hole gets stuck. No amount of sliding will free it. |
| 0.3 | Title card: *Perelman's proof of the Poincaré conjecture*, with "Ricci flow, 2002–2003" underneath. | In 1904, Henri Poincaré asked whether this simple test can recognise the simplest shape one dimension up. It took a century, and a mathematician named Grigori Perelman, to answer yes. |
| 0.4 | The road map appears: **Shapes · The question · Ricci flow · Perelman · Checked** | |

## Chapter 1 — Shapes

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. A wiggly closed curve smoothly morphs into a circle. | Topology is the study of shapes that you may stretch and bend as much as you like, but never tear or glue. |
| 1.2 | A mug outline (a cup with a handle) beside a doughnut; under each, "one hole". | To a topologist, a coffee mug and a doughnut are the same shape. Each has exactly one hole, and one can be squished into the other. |
| 1.3 | A ball beside a doughnut, with a "≠" between them. | But a ball and a doughnut are different. No squishing can make the hole go away. |
| 1.4 | A tiny figure stands on the surface of a large ball, seeing only the ground around it. | How can you tell shapes apart if you live inside one and cannot look at it from outside? Poincaré's answer was a test with a loop of string. |
| 1.5 | On the ball, a loop is drawn and slides off to a point. | Lay a loop anywhere on the shape and pull it tight, keeping it on the surface. On a ball's surface, every loop shrinks to a point. |
| 1.6 | On the doughnut, a loop around the hole tightens and stops; the word "stuck". | On a doughnut, a loop around the hole cannot shrink, however you slide it. |
| 1.7 | The label **simply connected** appears under the ball. | A shape in which every loop can shrink is called simply connected. |
| 1.8 | A row: sphere (tick), doughnut (cross), two-holed doughnut (cross). | For surfaces, this one test is enough. Every closed surface, finite and with no edge, in which every loop shrinks, is a sphere. That was known by the end of the eighteen hundreds. |
| 1.9 | **Recap card:** "Shapes up to stretching. The lasso test: can every loop shrink?" | So: shapes up to stretching, and one test. Can every loop shrink to a point? |

## Chapter 2 — The question

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A square "screen" with a dot moving right; it leaves through the right edge and comes back through the left. | Now go up one dimension. A closed three-dimensional space looks like ordinary space near every point, but it is finite and has no edge, |
| 2.2 | The dot keeps travelling and wraps around again; a faint trail. | like a video game screen where leaving on one side brings you back on the other. You could live inside one, and if you travelled far enough in a straight line, you might come back to where you started. |
| 2.3 | Two line segments bend toward each other and join at their ends: a circle. Label "a circle". | The simplest such space is built by gluing. Glue two line segments at their ends, and you get a circle. |
| 2.4 | Two discs become the two halves of a balloon and close up: a sphere. Label "a sphere". | Glue two discs along their edges, like the two halves of a balloon, and you get a sphere. |
| 2.5 | Two shaded balls side by side. A dot travels to the edge of the left ball and reappears just inside the right one. Label "the three-sphere". | Glue two solid balls along their surfaces, and you get the three-sphere. Leave one ball through its surface, and you find yourself inside the other. |
| 2.6 | The two balls, with a loop drawn across both that shrinks to a point. | It naturally lives in four dimensions, so we cannot draw it, but you could live inside it, and every loop in it can be shrunk. |
| 2.7 | Statement card: "**The Poincaré conjecture.** Every closed three-dimensional space in which every loop can shrink is a three-sphere." | Poincaré asked: does the lasso test still recognise the sphere, one dimension up? If every loop in a closed three-dimensional space can shrink, must the space be a three-sphere in disguise? |
| 2.8 | A timeline builds: 1904 Poincaré; 1961 Smale, dimensions five and up; 1982 Freedman, dimension four. | Strangely, higher dimensions turned out to be easier, because there is more room to move things around. Stephen Smale settled dimensions five and up in 1961, and Michael Freedman dimension four in 1982. |
| 2.9 | "dimension three" in yellow under 1904; then "2000: Millennium Prize" is added. | Dimension three, the one Poincaré asked about, resisted every attack. In 2000 it became one of the seven Millennium Prize Problems. |
| 2.10 | **Recap card:** "Does every loop shrinking force a three-sphere?" | So the question is: in three dimensions, does every loop shrinking force the shape to be a sphere? |

## Chapter 3 — Ricci flow

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, third box lit. A lumpy closed shape, outlined. | In 1982, Richard Hamilton suggested a new approach. Don't stare at the shape. Let it change. |
| 3.2 | A temperature profile with hot spikes flattens out into an even level. | Give the shape a geometry, with bumps, dents and curvature, and let it smooth itself out over time, the way heat flows from hot spots to cold ones until the temperature is even. |
| 3.3 | Hamilton's equation, with "the shape" and "its curvature" labelled under the two sides. | His rule is called Ricci flow. Where the space curves like a sphere, it shrinks; where it curves like a saddle, it expands. It is a heat equation for geometry. |
| 3.4 | The wiggly curve from the explainer's figure, moving: every point moves toward the inside of its bend, the wiggles melting away. | A simpler cousin works on curves in a flat plane. Every point moves toward the inside of its bend, faster where the curve bends more sharply. |
| 3.5 | The curve keeps shrinking. A rescaled copy beside it becomes a perfect circle; it shrinks to a point. | Any such curve loses its wiggles, becomes round, and shrinks to a point. Gage, Hamilton and Grayson proved this in the nineteen eighties. |
| 3.6 | A gently lumpy blob, labelled "curved positively everywhere", rounds out and shrinks to a point. | Hamilton proved the same for three-dimensional shapes that already curve positively in every direction. They become rounder and rounder, and vanish as a round point. So they were spheres all along. |
| 3.7 | **Recap card:** "Ricci flow: let the shape smooth itself by its own curvature." | So: let the shape smooth itself by its own curvature, and see what it becomes. |

## Chapter 4 — Necks that pinch

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box still lit. A dumbbell: two round balls joined by a thin neck. | For a general shape, the flow can go wrong. Picture a dumbbell: two balls joined by a thin neck. |
| 4.2 | The neck thins and pinches to a point; the balls are still large. | The neck is curved tightly around its waist, so the flow squeezes it hardest. It pinches off in finite time, while the balls are still large. |
| 4.3 | A red flash at the pinch point; the word "singularity". | At that moment the curvature becomes infinite, and the flow cannot go on. This is called a singularity. |
| 4.4 | Rewind to just before the pinch. Scissors cut the neck; each end gets a round cap; the two pieces keep flowing. | Hamilton's plan was surgery. Just before a neck pinches, cut it, cap each end with a round cap, and keep flowing. |
| 4.5 | A three-item checklist builds: "only cuttable singularities", "cuts stay under control", "a clear ending". | To make the plan work, three things had to be shown. Every singularity must be one you can cut. The cuts must not pile up out of control. And the flow must end in a way you can read. |
| 4.6 | A long, thin cigar shape with a rounded tip; a question mark. | Necks are fine. But a long, thin, cigar-shaped tip that never pinches would be a disaster, with no good place to cut. Hamilton could not rule it out. |
| 4.7 | **Recap card:** "Necks pinch; surgery cuts them. Three things were missing." | Necks pinch, and surgery cuts them. After twenty years, three things were still missing. |

## Chapter 5 — What Perelman added

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. Three paper cards appear one by one: November 2002, March 2003, July 2003. | In November 2002, Grigori Perelman, a mathematician in Saint Petersburg, posted the first of three papers online. Together, they finished Hamilton's program. |
| 5.2 | A curve that only rises, labelled "entropy". | His first idea was a quantity, built from the geometry, that only goes up while the flow runs, a bit like entropy in physics. Something that can only move one way is a powerful tool. |
| 5.3 | Two small balls: a round one with a tick, and a squashed flat one with a cross. Label "no local collapsing". | From it he proved that wherever the curvature is under control, the shape cannot be squashed thin. A small ball always holds a fair share of the volume an ordinary ball would hold. |
| 5.4 | The cigar from chapter 4. A zoom box on its tip shows a squashed tube; a red cross over the cigar. | That kills the cigar. Zoom in on its tip, and you see a squashed, collapsed tube, which the flow can never produce. |
| 5.5 | Three small pictures appear: a thin neck, a neck closed off by a cap, and a small round piece. | Second, he showed that wherever the curvature is very large, the shape looks almost exactly like one of a short list of models: a thin round neck, a neck closed off by a cap, or a small, nearly round piece. |
| 5.6 | Each model gets a small pair of scissors. | Every one of them is something you know how to cut. |
| 5.7 | A time axis; tick marks for surgeries, a finite number before each moment. | Third, he said exactly where to cut, deep inside very thin necks, and proved that the cuts never pile up: only finitely many happen in any stretch of time. |
| 5.8 | The volume graph from the explainer: total volume falls, drops at each surgery, and reaches zero, marked "extinct". | Finally, for a shape in which every loop shrinks, he proved that the flow with surgery burns the shape away completely, in finite time. |
| 5.9 | A "width" curve under a straight falling line that hits zero. | He measured how wide the shape is, using the smallest disc that a loop can be filled with, and showed that this width shrinks at a steady rate. Something positive that shrinks at a steady rate must reach zero. |
| 5.10 | **Recap card:** "An entropy that only rises; no collapsing; a short list of models; controlled surgery; extinction." | So: a quantity that only rises, no collapsing, a short list of shapes, surgery under control, and extinction. |

## Chapter 6 — Putting it together

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fourth box still lit. A shape with two necks flows; the necks are cut; the pieces shrink away. | Start with any closed three-dimensional space in which every loop shrinks. Run the flow, cut each neck before it pinches, and wait. After finitely many cuts, nothing is left. |
| 6.2 | The film runs backwards: the pieces reappear, each labelled "a round sphere". | Now run the film backwards. Every piece that vanished was a known shape: a round three-sphere, or one of a few close relatives. |
| 6.3 | The relatives are shown with a stuck loop each; they fade, crossed out. | Each of those relatives contains a loop that gets stuck, and our shape has none. So every piece was a three-sphere. |
| 6.4 | The spheres are glued back along their necks and merge into one sphere. | Gluing three-spheres together along necks gives back a three-sphere. So the shape we started with was a three-sphere all along. |
| 6.5 | **Recap card:** "Flow, cut, burn away, and read the answer backwards." | Flow, cut, burn away, and read the answer backwards. |

## Chapter 7 — Checked

| # | On screen | Narration |
|---|---|---|
| 7.1 | Road map, fifth box lit. The three paper cards, with "never sent to a journal". | Perelman never sent his papers to a journal. They were extremely compressed, with many steps left to the expert reader, so others set out to write every step in full. |
| 7.2 | Three cards: "Kleiner and Lott: detailed notes", "Morgan and Tian: a book-length proof", "Cao and Zhu: a complete account". A tick on each. | Bruce Kleiner and John Lott wrote detailed notes. John Morgan and Gang Tian wrote a book-length proof. Huai-Dong Cao and Xi-Ping Zhu published another account. By 2006, they agreed: the proof was right. |
| 7.3 | A medal: "Fields Medal, 2006: declined". | In 2006, Perelman was awarded the Fields Medal, one of the highest honours in mathematics. He became the first person to decline it. |
| 7.4 | A second card: "Millennium Prize, 2010: declined". | In 2010, the Clay Institute awarded him the first Millennium Prize, a million dollars. He declined that too, saying that Hamilton's contribution was no less than his own. |
| 7.5 | **Recap card:** "Checked by several teams. Two prizes, both declined." | Checked by several teams, and two prizes, both declined. |

## Chapter 8 — What it means

| # | On screen | Narration |
|---|---|---|
| 8.1 | A tick: "The Poincaré conjecture is true". | So the Poincaré conjecture is true. The lasso test recognises the three-sphere. |
| 8.2 | A tick: "Geometrization: every closed 3D space is built from eight kinds of pieces". | The same tools prove Thurston's geometrization conjecture: every closed three-dimensional space is built from eight kinds of uniform pieces, a classification as complete as the one for surfaces. |
| 8.3 | A cross: "The smooth four-dimensional version is still open". | It does not settle a subtler version in four dimensions, about shapes you can do calculus on, which is still open. |
| 8.4 | A cross: "No complete computer-checked proof yet". | And every complete account runs to hundreds of pages. As far as we know, no computer has checked the whole proof yet. |
| 8.5 | **Recap card:** "The only Millennium problem the Clay Institute has declared solved." | It is still the only Millennium problem the Clay Institute has declared solved. |

## Chapter 9 — Closing

| # | On screen | Narration |
|---|---|---|
| 9.1 | The full road map lit; the loop on the ball slides off once more; the wiggly curve rounds out. | Let's recap. A test with a loop of string, from 1904. A shape that smooths itself by its own curvature. Necks cut just before they pinch. And a shape in which every loop shrinks, burning away to nothing: a three-sphere all along. |
| 9.2 | Final title card and link: github.com/htt210/awesome-millennium. | A question about pure shape, answered with the mathematics of heat. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration. Animations play while the narrator describes them.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** the narrator says "Pwan-ka-ray", "Pair-el-man", "Ree-chee", "Tyen", "Tsao", "Joo"; the captions keep the usual spellings.
- **Three dimensions on a flat screen:** every three-dimensional shape is drawn as its two-dimensional cousin (a ball's surface, a doughnut, a dumbbell's outline). The narration says so where it matters (2.6).

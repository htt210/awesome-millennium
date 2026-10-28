# Video script: "The Exponential Time Hypothesis is False"

*Reviewed on 28 October 2026, before anything was animated.* This script follows the plain-language explainer ([`../README.md`](../README.md)) and is the source of the video's narration: each scene in [`eth_video.py`](eth_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `eth_video.py`).

**How this script differs from the first video.** The first video covered the whole technical argument in 8½ minutes and named things before showing them. This one follows four rules:

1. **One idea per beat.** A beat ends with a pause, about 1.5 seconds, before the next idea starts.
2. **Example first, name second.** Every new word is introduced by showing a concrete case, and only then named. The "New words" column at the end lists where each word first appears.
3. **Signposts.** Each chapter opens with a title card and a small road map showing where we are, and ends with a one-sentence recap.
4. **No formulas on screen** except one, shown once (chapter 5) and read aloud in words. Everything else is numbers, pictures and graphs.

Length: the finished video runs 22 minutes 42 seconds (about 2,700 words of narration, plus pauses, recap cards and animations), more than twice the first video: the cost of introducing every idea properly.

---

## Chapter 0 — Cold open (≈ 0:55)

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A single switch fades in and clicks on, then off. | Here is a switch. It can be on, or off. |
| 0.2 | More switches appear in a row, ten of them, flickering through random settings faster and faster. | With a few dozen switches, and a list of rules about them, you get one of the most famous puzzles in computer science. For fifty years, every method for solving it has hit the same wall. |
| 0.3 | The wall: a steep curve shooting off the top of the screen. | The work explodes as the puzzle grows. |
| 0.4 | Title card: *The Exponential Time Hypothesis is False*. Below it, small: "OpenAI preprint, October 2026". | In October 2026, a paper from OpenAI, written by one of its AI models, claimed a way around that wall. Not a practical one. But if it is right, it overturns a belief that a whole field was built on. Let's see what that belief was, and how the paper gets around it. |
| 0.5 | Road map appears: five boxes in a row: **The puzzle · Why it's hard · The bet · The new idea · What it means**. | |

## Chapter 1 — The puzzle (≈ 2:30)

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. Four switches labeled A, B, C, D, all off. | We start with four switches, called A, B, C and D. |
| 1.2 | A card appears: **Rule 1: A on, or B off, or C on.** Arrows from the card to A, B and C. | And here is a rule. A rule names three switches, and says how it would like each of them. This one says: A on, or B off, or C on. |
| 1.3 | The word **"or"** pulses. Three small check boxes beside the three wishes. | The important word is "or". The rule is happy if at least one of its three wishes comes true. It does not need all three. Just one. |
| 1.4 | Switches currently A off, B off, C off. Wish "B off" lights green; the rule card turns green with a check mark. | Right now, A is off and C is off, so those two wishes fail. But B is off, and the rule wanted B off. One wish came true, so the rule is happy. |
| 1.5 | B flips on. "B off" turns grey; all three wishes grey; the card turns red. | If we flip B on, now none of its wishes come true, and the rule is unhappy. |
| 1.6 | Rules 2 and 3 appear beside Rule 1. | A real puzzle has many rules. Here are three. |
| 1.7 | Text: **Can you set the switches so that every rule is happy?** | And the puzzle is: can you set the switches so that every rule is happy at the same time? |
| 1.8 | Pause. Then the switches move one at a time to A on, B on, C on, D off; each rule turns green as it becomes happy. | Let's try. A on makes rule one happy. B on makes rule two happy. C on makes rule three happy. And D can stay off. Every rule is happy. We found a solution. |
| 1.9 | Caption card: **This puzzle is called 3-SAT.** ("3" for three switches per rule, "SAT" for *satisfy*.) | This puzzle has a name: 3-SAT. Three, because each rule names three switches. SAT, short for satisfy, because we want to satisfy every rule. |
| 1.10 | Icons appear around the puzzle: a timetable, a computer chip, a map route, a Sudoku grid, each with an arrow into the switches. | It looks like a toy, but a huge range of real problems can be rewritten as this puzzle: making timetables, checking that a computer chip is designed correctly, planning routes, even solving Sudoku. That is why computer scientists have studied it more than almost any other problem. |
| 1.11 | The single solution splits into a stack of solutions with a counter: "1, 2, 3 …". | The paper actually answers a harder question. It doesn't just find one good setting. It counts how many good settings there are. If you can count them, you can certainly tell whether there is at least one. |
| 1.12 | **Recap card:** "Switches, rules that want at least one wish, and the question: how many settings make every rule happy?" | So: switches, rules, and one question. How many ways are there to make every rule happy? |

## Chapter 2 — Why it gets hard so fast (≈ 1:25)

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. One switch, two rows beside it: "off", "on". Counter: **2 settings**. | The obvious method is to try every possible setting and check the rules each time. How many settings are there? With one switch, two: off, or on. |
| 2.2 | A second switch is added; each row splits into two. Counter: **4**. | Add a second switch, and each of those two settings splits in two. Four settings. |
| 2.3 | Third switch, rows split again. Counter: **8**. Then 16. | A third switch: eight. A fourth: sixteen. |
| 2.4 | Text "×2" beside each new switch. | Every switch you add doubles the number of settings. |
| 2.5 | Graph builds (*plain-doubling*): time to try every setting at a billion per second, against number of switches. Dots appear one by one at 30, 55 and 88. | Doubling sounds harmless, so let's put numbers on it. Suppose a computer checks a billion settings every second. With thirty switches it needs about one second. With fifty-five switches, a year. With eighty-eight switches, longer than the universe has existed. |
| 2.6 | Label "real puzzles: thousands to millions of switches" far off the right edge of the graph. | Real puzzles have thousands, or millions, of switches. |
| 2.7 | The graph's line is highlighted. Card: **exponential growth = the work is multiplied by the same factor for every switch you add.** | This kind of growth has a name. When every extra switch multiplies the work by the same factor, here by two, we call the growth exponential. |
| 2.8 | A small gauge appears in the corner labeled **factor per switch: ×2**. It stays on screen for the rest of the video. | Keep an eye on this number: how much the work is multiplied by each extra switch. It's the measuring stick for the rest of this video. For trying everything, it's times two. |
| 2.9 | **Recap card:** "Trying everything doubles the work with every switch: exponential growth, factor ×2." | So trying everything is exponential, with a factor of two per switch. |

## Chapter 3 — Fifty years of shortcuts (≈ 1:35)

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, second box still lit. The puzzle with one unhappy (red) rule. | Of course, people have found smarter methods than trying everything. Here is the simplest shortcut. |
| 3.2 | The red rule's three wishes. Three branches grow from it: "first wish comes true" / "first fails, second comes true" / "first two fail, third comes true". | Take any rule. Either its first wish comes true; or the first fails and the second comes true; or the first two fail and the third comes true. There is no other way to make it happy. |
| 3.3 | Each branch shows how many switches it fixes: 1, 2, 3. | So instead of trying both settings of one switch at a time, we explore these three cases, and each case settles one, two or three switches at once. |
| 3.4 | The gauge ticks from ×2 down to ×1.84. | That alone brings the factor per switch down from two to about one point eight four. |
| 3.5 | Step chart builds over time (*plain-history*): 1985 ×1.62, 1999 ×1.33, 2014 ×1.31, 2026 ×1.307. The gauge follows. | Researchers kept improving the tricks. By 1985 the factor was down to one point six. By 1999, one point three three. Today the best known is about one point three. |
| 3.6 | Two big numbers side by side for 100 switches: "about 10^30 steps" vs "about 400 billion steps". | That is a huge improvement. For a hundred switches, it is the difference between a one followed by thirty zeros, and about four hundred billion. |
| 3.7 | Back on the chart: the line is flat between steps; text "still a fixed factor". | But notice what never changed. Each method still multiplies the work by a fixed factor for every switch. The factor got smaller. It never started to shrink as the puzzle grows. |
| 3.8 | **Recap card:** "Shortcuts lowered the factor from ×2 to ×1.3, but it's still a fixed factor: still exponential." | Every shortcut so far is still exponential. Just a gentler exponential. |

## Chapter 4 — The bet called ETH (≈ 1:20)

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box lit. The history chart, with a dashed line at ×1 along the bottom. | So here is the natural question. Can the factor be pushed all the way down toward one? |
| 4.2 | Text at the dashed line: "×1 = the work stops multiplying". | A factor of one would mean adding a switch no longer multiplies the work at all. |
| 4.3 | Portrait-free name card: *Russell Impagliazzo & Ramamohan Paturi, 2001*. A shaded floor rises a little above ×1, with a "?" on it. | In 2001, two computer scientists, Russell Impagliazzo and Ramamohan Paturi, proposed an answer: no. There is some floor, a bit above one. Maybe one point zero one, maybe one point two, nobody knows exactly where. But no method, however clever, will ever get below it. |
| 4.4 | Card: **The Exponential Time Hypothesis (ETH):** "the factor per switch can never get arbitrarily close to ×1". | This is the Exponential Time Hypothesis, or ETH. A hypothesis, because nobody proved it. It's a bet. |
| 4.5 | A stone labeled ETH at the bottom of the screen; blocks stack on it, each labeled "if ETH is true, then …". | But it was a bet that almost everyone took. Researchers built a large body of results on top of it, each of the form: if ETH is true, then this other problem cannot be solved faster than such and such. |
| 4.6 | **Recap card:** "ETH: exponential growth is unavoidable for this puzzle. A foundation stone, never proved." | ETH says the wall is real: this puzzle will always be exponential. Many results stand on it. |

## Chapter 5 — The new claim (≈ 2:00)

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. The gauge, reading ×1.3. | The new paper claims a method whose factor per switch is not fixed at all. It keeps shrinking as the puzzle grows. |
| 5.2 | Before the claim, we need a comparison. Graph axes appear (*plain-shapes*): "average work per switch" against "number of switches", with only the flat ×2 line drawn. | To see what that means, let's compare three kinds of growth, using our measuring stick: the average work per switch. First, exponential growth. The factor stays the same forever: a flat line. |
| 5.3 | Second line (green) drawn: drops to ×1 almost immediately. Beside it: "10 switches → 1,000 steps; 20 switches → 8,000". | Now a very different kind of growth: the kind computer scientists consider fast, called polynomial. Here, doubling the number of switches multiplies the work by a fixed amount, like eight, instead of squaring it. Spread over all the switches, the work per switch quickly drops to almost one. |
| 5.4 | Third line (blue) drawn slowly between them, sinking gradually. | And in between, a third kind: the factor per switch keeps shrinking toward one, but slowly. This is called subexponential. Faster than any exponential, slower than any polynomial. |
| 5.5 | The blue line is highlighted. Card: **The claim: counting the good settings of this puzzle takes subexponential time.** | That's what the paper claims for our puzzle. A method to count all the good settings, with a cost whose factor per switch sinks toward one. |
| 5.6 | The ETH floor from chapter 4 appears; the blue line sinks through it. The ETH stone cracks. | And here's why that matters. If the factor keeps sinking, it eventually goes below any floor you pick. So there is no floor. ETH would be false. |
| 5.7 | The one formula of the video: "cost ≈ 2 to the power n ÷ √(log n)", with "n = number of switches". | For those who like symbols: the cost is roughly two to the power n, divided by the square root of the logarithm of n. The square root of log n grows forever, very slowly, and that's what makes the factor shrink. |
| 5.8 | **Recap card:** "Exponential: fixed factor. Subexponential: factor sinks slowly. The paper claims subexponential, so ETH is false." | So: a factor that sinks below any floor. That's the claim. Now, how could that possibly work? |

## Chapter 6 — How the method works (≈ 8:25)

*This chapter is split into five short parts, each with its own small title.*

### 6a. Turning checking into arithmetic

| # | On screen | Narration |
|---|---|---|
| 6a.1 | Road map, fourth box lit; sub-title "Step 1: turn checking into arithmetic". A smaller puzzle: three switches A, B, C, two rules. | The first idea is to turn the puzzle into ordinary arithmetic. We'll use a smaller puzzle: three switches, and two rules. Rule one: A on, or B off, or C on. Rule two: B on, or C on. |
| 6a.2 | One setting (all off) appears. Rule 1 gets a big **1**, rule 2 a big **0**. | For any setting, give each rule a score: one if the rule is happy, zero if it is not. With every switch off, rule one is happy, because it wants B off, so it scores one. Rule two wants B or C on, so it scores zero. |
| 6a.3 | The two scores multiply: 1 × 0 = **0**. | Now multiply the scores. One times zero is zero. |
| 6a.4 | A second setting where both are happy: 1 × 1 = **1**. | When is the product one? Only when every rule scores one, that is, when every rule is happy. A single unhappy rule makes the whole product zero. |
| 6a.5 | The full table builds row by row, all eight settings, products 0 1 0 1 0 1 1 1. A total appears: **5**. | So go through all eight settings, write down each product, and add them up. The total, five, is exactly the number of good settings. |
| 6a.6 | Recap line: "count = add up, over all settings, the product of the rule scores". | We've turned counting into a big sum of products. That alone doesn't save any work: we still visited every setting. But sums and products are things algebra knows how to rearrange. |

### 6b. The dream: independent teams

| # | On screen | Narration |
|---|---|---|
| 6b.1 | Sub-title "Step 2: the dream". Forty switches split into two circles of twenty, with rules drawn only inside each circle. | Here's the dream. Suppose the switches split into two teams, and no rule mixes the teams: every rule only talks about switches in one team. |
| 6b.2 | Team 1 counts its own good settings: "say 300". Team 2: "say 500". | Then the teams can't affect each other. Count the good settings of team one on its own. Say there are three hundred. Count team two on its own: say five hundred. |
| 6b.3 | 300 × 500 = 150,000 good settings overall. | Every good setting of team one can be combined with every good setting of team two. So the total is three hundred times five hundred. |
| 6b.4 | Bar graph (*plain-teams*): 1.1 trillion settings vs 2.1 million. | And the work collapses. Trying all forty switches at once means about a trillion settings. Two teams of twenty, counted separately, need about two million. |
| 6b.5 | Real puzzle: red rules cross between the circles. | Of course, real puzzles aren't like this. However you split the switches, some rules reach across. |

### 6c. Teams that share only a total

| # | On screen | Narration |
|---|---|---|
| 6c.1 | Sub-title "Step 3: sharing only a total". Two teams with one crossing rule: "A on, or X on, or Y on", where A is in team 1 and X, Y in team 2. | But there's a middle ground. Look at this rule. It crosses between teams: it mentions A from team one, and X and Y from team two. |
| 6c.2 | A small box between the teams: "how many of X, Y are on: 0, 1 or 2". | Notice what the rule needs to know about team two. Not which of X and Y is on: only how many of them are on. Zero, one, or two. Let's call that number a total. |
| 6c.3 | The total is fixed at 0, then 1, then 2; each time the crossing rule becomes a rule inside team 1, and the teams separate. | Now fix the total, say at zero. Then the crossing rule only cares about team one, and the teams separate again. Count the good settings of team one, count the good settings of team two that have exactly that total, and multiply. Then do the same with the total fixed at one, and at two. Add the three answers up. |
| 6c.4 | Recap: "If teams only share a few totals, count separately for each value of the totals, then add". | So teams that share only a few totals can still be counted almost separately. The price: one round for every possible value of the totals. That's affordable, as long as there are only a few totals. |

### 6d. The dial

| # | On screen | Narration |
|---|---|---|
| 6d.1 | Sub-title "Step 4: the dial". A dial icon, set to 0, beside the tangled puzzle. | In real puzzles, rules need to know much more than a few totals. So the paper does something surprising. It doesn't change the puzzle. It changes the arithmetic. |
| 6d.2 | Inside one rule, the switch C is replaced by a mixture: "C" morphs into "a blend of C and other switches". | Remember the sum of products from step one. The paper adds a dial to it. Inside every rule, each switch is replaced by a blend of switches, and the dial controls the blend. |
| 6d.3 | Dial at 0: blends are just the original switches. A big green "= the true count". | At zero, there is no blending at all: the sum is exactly our count. |
| 6d.4 | Dial turns to 1: the picture of the two teams with only a totals box between them (*plain-dial*). | And at some special dial settings, one, two, three, and so on, the blends are arranged so that every rule sees switches from its own team, plus only a few totals from the other teams. Exactly the situation of step three. |
| 6d.5 | Card: "At dial 1, 2, 3, …: fast to compute. But the answer is not a count: just a number." | So at those settings, the sum is fast to compute. But there's a catch: with the blending switched on, the result isn't counting anything any more. It's just a number. The count we want sits at zero, where the shortcut doesn't work. |
| 6d.6 | Recap: "Fast at 1, 2, 3, …; the answer we want is at 0." | We can compute quickly at one, two, three. We need the answer at zero. How do we get there? |

### 6e. From the easy points back to zero

| # | On screen | Narration |
|---|---|---|
| 6e.1 | Sub-title "Step 5: back to zero". Axes: horizontal "dial", vertical "the number". A curve draws itself as a dot moves along the dial. | Picture turning the dial slowly and watching the number change. It traces a curve. The paper shows that this curve is of a simple kind, a polynomial, which means it can only wiggle a limited number of times. |
| 6e.2 | Three orange dots at 1, 2, 3. The curve hides; a question mark sits at 0. | We know three points on the curve: at one, two and three. We want its height at zero. |
| 6e.3 | Several grey curves pass through the three dots, each landing at a different height at 0 (*plain-curve*, left). | But three points are not enough. Here are several curves, all allowed the same number of wiggles, all passing through the same three points. At zero, they disagree. |
| 6e.4 | A hill appears, a walker on it; the steepness at the walker's position is drawn as a short tangent line. Label: "slope = how steeply it climbs". | So the method collects more information at each point. Not just the height, but the slope: how steeply the curve is climbing there, like the steepness of a hill under your feet. |
| 6e.5 | Short tangent segments at the three dots. All grey curves vanish but one (*plain-curve*, right). | Once the slopes at one, two and three are known too, only one curve fits. And at zero, it lands on fourteen. |
| 6e.6 | A real check: "this is a real example from our code, with 6 switches: the count, by brute force, is 14". | This is a real example, computed by our own code, with six switches. Trying every setting confirms the answer: fourteen. |
| 6e.7 | Text: "Wigglier curves need more: slope, bend, and so on". | For a bigger puzzle the curve can wiggle more, so you need more information at each point: the slope, how the curve bends, and so on. But the principle is the same: enough information at the easy points pins down the whole curve, and with it, the count. |

### 6f. The balancing act, and the rest

| # | On screen | Narration |
|---|---|---|
| 6f.1 | A seesaw: left side "few wiggles", right side "many easy points". | Here is the hard part, and the heart of the paper. Every extra piece of information costs work. So the method only pays off if the curve wiggles little, while there are many easy points to measure it at. Those two goals pull against each other. |
| 6f.2 | The seesaw balances. Caption: "the paper's main invention". | The paper's main invention is a construction that achieves both at once: a clever way of blending in which most of the mixing cancels itself out, and only a small leftover needs to be tracked with totals. |
| 6f.3 | Tidy puzzles (each switch in few rules) on the left; arbitrary puzzles on the right, with an arrow "split into tidy pieces". | Finally, all of this works best when each switch appears in only a few rules. The paper shows that any puzzle can be broken into tidy pieces like that, without changing the count. |
| 6f.4 | Recap montage: scores → teams → totals → dial → curve. | Let's put it together. Turn counting into arithmetic. Add a dial. At special settings, the puzzle splits into teams that share only a few totals, so it's fast. Measure the curve there, and follow it back to zero, where the true count lives. |
| 6f.5 | The gauge appears and sinks slowly below ×1.3, ×1.2, … | Adding up all the costs, each part grows more slowly than any fixed factor per switch. And that is the claim: subexponential. |

## Chapter 7 — The catch (≈ 1:10)

| # | On screen | Narration |
|---|---|---|
| 7.1 | Road map, fifth box lit. Question: "So is this a fast new puzzle solver?" | So, is this a fast new way to solve puzzles? No. And it isn't close. |
| 7.2 | Graph (*plain-catch*) builds: the method's factor per switch starting near ×2.8, sinking; flat lines at ×2 and ×1.307. | The method only wins as puzzles grow without limit. We took the explicit numbers in the paper's overview and worked out when it starts to pay off. |
| 7.3 | The crossing with ×2 lights up: "the number of switches has about 18 billion digits". | It beats simply trying everything when the number of switches has about eighteen billion digits. Not eighteen billion switches. A number of switches eighteen billion digits long. |
| 7.4 | The crossing with ×1.307: "about 340 billion digits". Beside it: "atoms in the observable universe: a number with about 80 digits". | To beat the best older method, about three hundred and forty billion digits. For comparison, the number of atoms in the observable universe has about eighty digits. |
| 7.5 | Note: "rough figures from an analysis that wasn't trying to be efficient". | These are rough figures, from an analysis that wasn't trying to be efficient, so the true crossover could be much earlier. But nobody expects this method to run on a real computer. |
| 7.6 | **Recap card:** "Not practical. What matters is what it proves is possible." | Its importance is not what it does. It's what it proves is possible. |

## Chapter 8 — What it means, and what it doesn't (≈ 1:15)

| # | On screen | Narration |
|---|---|---|
| 8.1 | The ETH stone cracked; some blocks above it wobble, others are propped up by new pillars labeled "other assumptions". | If the proof is right, ETH is false, and so are its stronger cousins. Results that started with "if ETH is true" lose their footing. Some can be rescued from other assumptions that are still believed. Others will need rethinking. |
| 8.2 | Card: **P vs NP**, one of the seven Millennium Prize Problems, $1,000,000. | What about the most famous question in computer science, P versus NP? It's one of the seven Millennium Prize Problems, with a million-dollar prize. |
| 8.3 | The three-growth graph returns; the green polynomial line is labeled "P = NP would need this". | Roughly, it asks whether puzzles like ours can be solved with polynomial growth, the fast kind. |
| 8.4 | The blue subexponential line is labeled "what the paper claims", clearly above the green line. | The new method is subexponential, which is still slower than polynomial. So P versus NP stays open. |
| 8.5 | Two crossed-out icons: a padlock (encryption) and a laptop running a solver. | It doesn't break encryption: everyday encryption doesn't depend on ETH, and the method is far too slow anyway. And it doesn't give faster puzzle solvers: practical solvers already handle huge real-world puzzles with tricks that work well in practice. |
| 8.6 | **Recap card:** "Changes what's possible in principle. Not P vs NP, not encryption, not practice." | What it changes is our understanding of what is possible in principle. |

## Chapter 9 — Is it true? (≈ 1:05)

| # | On screen | Narration |
|---|---|---|
| 9.1 | Card: "Preprint, not yet peer reviewed. Written by an AI model at OpenAI." | Is it true? It's too early to say for sure. The paper is a preprint, not yet checked by peer review, and it was written by an AI model. |
| 9.2 | A proof checker icon: "Lean: a computer checks every logical step". Label: "covers a slightly weaker, still ETH-breaking version". | OpenAI reports that part of it has been checked by computer, in a system called Lean, where a machine verifies every logical step. That check covers a slightly weaker version of the result, which would still break ETH. |
| 9.3 | Names: Impagliazzo, Paturi, Williams: "examining the proof". | And a group of experts, including Impagliazzo and Paturi, who proposed ETH in the first place, is examining the proof. |
| 9.4 | Our toy code running, with checks turning green. | We also ran the method's main steps on small puzzles with our own code, and it produces the exact counts. That can't confirm the proof for large puzzles, but it shows the ideas fit together. |

## Chapter 10 — Closing (≈ 0:50)

| # | On screen | Narration |
|---|---|---|
| 10.1 | The full road map, all five boxes lit, then the switches from the opening. | Let's recap. A puzzle of switches and rules, where trying everything doubles the work with every switch. Fifty years of shortcuts that made the growth gentler, but never changed its kind. A bet, ETH, that it never could. |
| 10.2 | The dial turns; the curve lands on the count. | And now a paper that blends the puzzle with a dial, solves it at easy points, and follows a curve back to the true count, with a cost whose factor keeps sinking. |
| 10.3 | Final title card, links: explainer page, technical walkthrough. | If it holds up, the wall is still there for every puzzle we could ever build. But in principle, it was never a wall at all. |

---

## New words, and where each is introduced

| Word | Introduced in | How |
|---|---|---|
| switch, rule, setting | 1.1–1.2 | shown first, then named |
| happy rule, "at least one wish" | 1.3–1.5 | a happy and an unhappy example |
| 3-SAT | 1.9 | named after solving an example |
| counting vs finding | 1.11 | stack of solutions |
| exponential growth | 2.7 | after the doubling demo |
| factor per switch (the measuring stick) | 2.8 | a gauge that stays on screen |
| ETH, hypothesis | 4.3–4.4 | floor picture, then the name |
| polynomial growth | 5.3 | numeric example, 10 → 20 switches |
| subexponential | 5.4 | drawn between the two others |
| score, product, sum | 6a | worked table, row by row |
| team | 6b | picture first |
| total | 6c | a crossing rule that only needs "how many are on" |
| dial, blend | 6d | built on the sum of 6a |
| curve, polynomial (as a curve), wiggles | 6e.1 | traced by turning the dial |
| slope | 6e.4 | a hill under your feet |
| P vs NP, Millennium Prize | 8.2–8.3 | built on polynomial growth from 5.3 |
| Lean, peer review | 9.1–9.2 | one-line definitions |

## Notes for production

- **Pacing:** about 145 words per minute of narration. Each beat ends with at least 1.5 s of silence; each recap card stays up 3 s after the narration ends. Animations play *while* the narrator describes them, not before.
- **Graphs:** chapters 2, 3, 5, 6b, 6e and 7 reuse the eight figures of the explainer page, redrawn in manim so that they build up step by step.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** the narrator says "E T H", "three-sat" and "Pa-toori"; the captions show ETH, 3-SAT and Paturi (`PRONOUNCE` in `eth_video.py`).

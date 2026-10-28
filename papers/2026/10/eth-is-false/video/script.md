# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `eth-is-false.mp4`. The words come from [`storyboard.md`](storyboard.md), the reviewed script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** Here is a switch. It can be on, or off.

**[00:00:05]** With a few dozen switches, and a list of rules about them, you get one of the most famous puzzles in computer science.

**[00:00:14]** For fifty years, every method for solving it has hit the same wall.

**[00:00:20]** The work explodes as the puzzle grows.

**[00:00:24]** In October 2026, a paper from OpenAI, written by one of its AI models, claimed a way around that wall.

**[00:00:34]** Not a practical one. But if it is right, it overturns a belief that a whole field was built on.

**[00:00:41]** Let's see what that belief was, and how the paper gets around it.

## 1. The puzzle

**[00:00:54]** We start with four switches, called A, B, C and D.

**[00:01:00]** And here is a rule. A rule names three switches, and says how it would like each of them.

**[00:01:07]** This one says: A on, or B off, or C on.

**[00:01:13]** The important word is "or". The rule is happy if at least one of its three wishes comes true.

**[00:01:20]** It does not need all three. Just one.

**[00:01:25]** Right now, A is off and C is off, so those two wishes fail. But B is off, and the rule wanted B off.

**[00:01:34]** One wish came true, so the rule is happy.

**[00:01:40]** If we flip B on, now none of its wishes come true, and the rule is unhappy.

**[00:01:47]** A real puzzle has many rules. Here are three.

**[00:01:53]** And the puzzle is: can you set the switches so that every rule is happy at the same time?

**[00:02:01]** Let's try. A on makes rule one happy. B on makes rule two happy. C on makes rule three happy. And D can stay off.

**[00:02:11]** Every rule is happy. We found a solution.

**[00:02:16]** This puzzle has a name: 3-SAT. Three, because each rule names three switches.

**[00:02:22]** SAT, short for satisfy, because we want to satisfy every rule.

**[00:02:30]** It looks like a toy, but a huge range of real problems can be rewritten as this puzzle: making timetables,

**[00:02:38]** checking that a computer chip is designed correctly, planning routes, even solving Sudoku.

**[00:02:45]** That is why computer scientists have studied it more than almost any other problem.

**[00:02:52]** The paper actually answers a harder question. It doesn't just find one good setting.

**[00:02:58]** It counts how many good settings there are. If you can count them, you can certainly tell whether there is at least one.

**[00:03:08]** So: switches, rules, and one question. How many ways are there to make every rule happy?

## 2. Why it gets hard so fast

**[00:03:23]** The obvious method is to try every possible setting and check the rules each time. How many settings are there?

**[00:03:31]** With one switch, two: off, or on.

**[00:03:36]** Add a second switch, and each of those two settings splits in two. Four settings.

**[00:03:43]** A third switch: eight. A fourth: sixteen.

**[00:03:49]** Every switch you add doubles the number of settings.

**[00:03:54]** Doubling sounds harmless, so let's put numbers on it. Suppose a computer checks a billion settings every second.

**[00:04:02]** With thirty switches it needs about one second. With fifty-five switches, a year.

**[00:04:08]** With eighty-eight switches, longer than the universe has existed.

**[00:04:14]** Real puzzles have thousands, or millions, of switches.

**[00:04:20]** This kind of growth has a name.

**[00:04:23]** When every extra switch multiplies the work by the same factor, here by two, we call the growth exponential.

**[00:04:32]** Keep an eye on this number: how much the work is multiplied by each extra switch.

**[00:04:38]** It's the measuring stick for the rest of this video. For trying everything, it's times two.

**[00:04:47]** So trying everything is exponential, with a factor of two per switch.

## 3. Fifty years of shortcuts

**[00:05:01]** Of course, people have found smarter methods than trying everything. Here is the simplest shortcut.

**[00:05:09]** Take any rule.

**[00:05:11]** Either its first wish comes true; or the first fails and the second comes true; or the first two fail and the third comes true.

**[00:05:20]** There is no other way to make it happy.

**[00:05:25]** So instead of trying both settings of one switch at a time,

**[00:05:29]** we explore these three cases, and each case settles one, two or three switches at once.

**[00:05:37]** That alone brings the factor per switch down from two to about one point eight four.

**[00:05:44]** Researchers kept improving the tricks. By 1985 the factor was down to one point six. By 1999, one point three three.

**[00:05:56]** Today the best known is about one point three.

**[00:06:00]** That is a huge improvement.

**[00:06:03]** For a hundred switches, it is the difference between a one followed by thirty zeros, and about four hundred billion.

**[00:06:13]** But notice what never changed. Each method still multiplies the work by a fixed factor for every switch.

**[00:06:21]** The factor got smaller. It never started to shrink as the puzzle grows.

**[00:06:29]** Every shortcut so far is still exponential. Just a gentler exponential.

## 4. The bet called ETH

**[00:06:44]** So here is the natural question. Can the factor be pushed all the way down toward one?

**[00:06:52]** A factor of one would mean adding a switch no longer multiplies the work at all.

**[00:06:59]** In 2001, two computer scientists, Russell Impagliazzo and Ramamohan Paturi, proposed an answer: no.

**[00:07:09]** There is some floor, a bit above one. Maybe one point zero one, maybe one point two, nobody knows exactly where.

**[00:07:19]** But no method, however clever, will ever get below it.

**[00:07:24]** This is the Exponential Time Hypothesis, or ETH. A hypothesis, because nobody proved it. It's a bet.

**[00:07:35]** But it was a bet that almost everyone took. Researchers built a large body of results on top of it, each of the form:

**[00:07:44]** if ETH is true, then this other problem cannot be solved faster than such and such.

**[00:07:53]** ETH says the wall is real: this puzzle will always be exponential. Many results stand on it.

## 5. The new claim

**[00:08:09]** The new paper claims a method whose factor per switch is not fixed at all. It keeps shrinking as the puzzle grows.

**[00:08:19]** To see what that means, let's compare three kinds of growth, using our measuring stick: the average work per switch.

**[00:08:28]** First, exponential growth. The factor stays the same forever: a flat line.

**[00:08:35]** Now a very different kind of growth: the kind computer scientists consider fast, called polynomial.

**[00:08:43]** Here, doubling the number of switches multiplies the work by a fixed amount, like eight, instead of squaring it.

**[00:08:52]** Spread over all the switches, the work per switch quickly drops to almost one.

**[00:08:59]** And in between, a third kind: the factor per switch keeps shrinking toward one, but slowly.

**[00:09:07]** This is called subexponential. Faster than any exponential, slower than any polynomial.

**[00:09:16]** That's what the paper claims for our puzzle.

**[00:09:19]** A method to count all the good settings, with a cost whose factor per switch sinks toward one.

**[00:09:27]** And here's why that matters. If the factor keeps sinking, it eventually goes below any floor you pick.

**[00:09:35]** So there is no floor. ETH would be false.

**[00:09:40]** For those who like symbols: the cost is roughly two to the power n, divided by the square root of the logarithm of n.

**[00:09:49]** The square root of log n grows forever, very slowly, and that's what makes the factor shrink.

**[00:09:58]** So: a factor that sinks below any floor. That's the claim. Now, how could that possibly work?

## 6a. Turning checking into arithmetic

**[00:10:15]** The first idea is to turn the puzzle into ordinary arithmetic.

**[00:10:20]** We'll use a smaller puzzle: three switches, and two rules. Rule one: A on, or B off, or C on. Rule two: B on, or C on.

**[00:10:34]** For any setting, give each rule a score: one if the rule is happy, zero if it is not.

**[00:10:41]** With every switch off, rule one is happy, because it wants B off, so it scores one.

**[00:10:48]** Rule two wants B or C on, so it scores zero.

**[00:10:54]** Now multiply the scores. One times zero is zero.

**[00:11:00]** When is the product one? Only when every rule scores one, that is, when every rule is happy.

**[00:11:08]** A single unhappy rule makes the whole product zero.

**[00:11:13]** So go through all eight settings, write down each product, and add them up.

**[00:11:19]** The total, five, is exactly the number of good settings.

**[00:11:25]** We've turned counting into a big sum of products. That alone doesn't save any work: we still visited every setting.

**[00:11:34]** But sums and products are things algebra knows how to rearrange.

## 6b. The dream: independent teams

**[00:11:41]** Here's the dream.

**[00:11:42]** Suppose the switches split into two teams, and no rule mixes the teams: every rule only talks about switches in one team.

**[00:11:54]** Then the teams can't affect each other. Count the good settings of team one on its own. Say there are three hundred.

**[00:12:01]** Count team two on its own: say five hundred.

**[00:12:06]** Every good setting of team one can be combined with every good setting of team two.

**[00:12:12]** So the total is three hundred times five hundred.

**[00:12:17]** And the work collapses. Trying all forty switches at once means about a trillion settings.

**[00:12:24]** Two teams of twenty, counted separately, need about two million.

**[00:12:30]** Of course, real puzzles aren't like this. However you split the switches, some rules reach across.

## 6c. Teams that share only a total

**[00:12:40]** But there's a middle ground. Look at this rule.

**[00:12:44]** It crosses between teams: it mentions A from team one, and X and Y from team two.

**[00:12:53]** Notice what the rule needs to know about team two. Not which of X and Y is on: only how many of them are on.

**[00:13:01]** Zero, one, or two. Let's call that number a total.

**[00:13:07]** Now fix the total, say at zero. Then the crossing rule only cares about team one, and the teams separate again.

**[00:13:16]** Count the good settings of team one, count the good settings of team two that have exactly that total, and multiply.

**[00:13:24]** Then do the same with the total fixed at one, and at two. Add the three answers up.

**[00:13:32]** So teams that share only a few totals can still be counted almost separately.

**[00:13:38]** The price: one round for every possible value of the totals. That's affordable, as long as there are only a few totals.

## 6d. The dial

**[00:13:50]** In real puzzles, rules need to know much more than a few totals. So the paper does something surprising.

**[00:13:58]** It doesn't change the puzzle. It changes the arithmetic.

**[00:14:04]** Remember the sum of products from step one. The paper adds a dial to it.

**[00:14:09]** Inside every rule, each switch is replaced by a blend of switches, and the dial controls the blend.

**[00:14:19]** At zero, there is no blending at all: the sum is exactly our count.

**[00:14:25]** And at some special dial settings, one, two, three, and so on,

**[00:14:32]** the blends are arranged so that every rule sees switches from its own team, plus only a few totals from the other teams.

**[00:14:41]** Exactly the situation of step three.

**[00:14:45]** So at those settings, the sum is fast to compute.

**[00:14:49]** But there's a catch: with the blending switched on, the result isn't counting anything any more. It's just a number.

**[00:14:58]** The count we want sits at zero, where the shortcut doesn't work.

**[00:15:04]** We can compute quickly at one, two, three. We need the answer at zero. How do we get there?

## 6e. From the easy points back to zero

**[00:15:14]** Picture turning the dial slowly and watching the number change. It traces a curve.

**[00:15:20]** The paper shows that this curve is of a simple kind, a polynomial, which means it can only wiggle a limited number of times.

**[00:15:31]** We know three points on the curve: at one, two and three. We want its height at zero.

**[00:15:39]** But three points are not enough.

**[00:15:42]** Here are several curves, all allowed the same number of wiggles, all passing through the same three points.

**[00:15:49]** At zero, they disagree.

**[00:15:53]** So the method collects more information at each point.

**[00:15:57]** Not just the height, but the slope: how steeply the curve is climbing there, like the steepness of a hill under your feet.

**[00:16:07]** Once the slopes at one, two and three are known too, only one curve fits. And at zero, it lands on fourteen.

**[00:16:18]** This is a real example, computed by our own code, with six switches. Trying every setting confirms the answer: fourteen.

**[00:16:29]** For a bigger puzzle the curve can wiggle more,

**[00:16:33]** so you need more information at each point: the slope, how the curve bends, and so on.

**[00:16:40]** But the principle is the same: enough information at the easy points pins down the whole curve, and with it, the count.

## 6f. The balancing act, and the rest

**[00:16:51]** Here is the hard part, and the heart of the paper. Every extra piece of information costs work.

**[00:16:58]** So the method only pays off if the curve wiggles little, while there are many easy points to measure it at.

**[00:17:06]** Those two goals pull against each other.

**[00:17:10]** The paper's main invention is a construction that achieves both at once:

**[00:17:16]** a clever way of blending in which most of the mixing cancels itself out,

**[00:17:21]** and only a small leftover needs to be tracked with totals.

**[00:17:27]** Finally, all of this works best when each switch appears in only a few rules.

**[00:17:34]** The paper shows that any puzzle can be broken into tidy pieces like that, without changing the count.

**[00:17:42]** Let's put it together. Turn counting into arithmetic. Add a dial.

**[00:17:48]** At special settings, the puzzle splits into teams that share only a few totals, so it's fast.

**[00:17:55]** Measure the curve there, and follow it back to zero, where the true count lives.

**[00:18:03]** Adding up all the costs, each part grows more slowly than any fixed factor per switch.

**[00:18:09]** And that is the claim: subexponential.

## 7. The catch

**[00:18:17]** So, is this a fast new way to solve puzzles? No. And it isn't close.

**[00:18:25]** The method only wins as puzzles grow without limit.

**[00:18:29]** We took the explicit numbers in the paper's overview and worked out when it starts to pay off.

**[00:18:37]** It beats simply trying everything when the number of switches has about eighteen billion digits.

**[00:18:44]** Not eighteen billion switches. A number of switches eighteen billion digits long.

**[00:18:51]** To beat the best older method, about three hundred and forty billion digits.

**[00:18:58]** For comparison, the number of atoms in the observable universe has about eighty digits.

**[00:19:06]** These are rough figures, from an analysis that wasn't trying to be efficient, so the true crossover could be much earlier.

**[00:19:14]** But nobody expects this method to run on a real computer.

**[00:19:21]** Its importance is not what it does. It's what it proves is possible.

## 8. What it means, and what it doesn't

**[00:19:33]** If the proof is right, ETH is false, and so are its stronger cousins.

**[00:19:40]** Results that started with "if ETH is true" lose their footing.

**[00:19:45]** Some can be rescued from other assumptions that are still believed. Others will need rethinking.

**[00:19:53]** What about the most famous question in computer science, P versus NP?

**[00:19:58]** It's one of the seven Millennium Prize Problems, with a million-dollar prize.

**[00:20:05]** Roughly, it asks whether puzzles like ours can be solved with polynomial growth, the fast kind.

**[00:20:14]** The new method is subexponential, which is still slower than polynomial. So P versus NP stays open.

**[00:20:24]** It doesn't break encryption: everyday encryption doesn't depend on ETH, and the method is far too slow anyway.

**[00:20:33]** And it doesn't give faster puzzle solvers:

**[00:20:37]** practical solvers already handle huge real-world puzzles with tricks that work well in practice.

**[00:20:45]** What it changes is our understanding of what is possible in principle.

## 9. Is it true?

**[00:20:58]** Is it true? It's too early to say for sure.

**[00:21:02]** The paper is a preprint, not yet checked by peer review, and it was written by an AI model.

**[00:21:10]** OpenAI reports that part of it has been checked by computer, in a system called Lean, where a machine verifies every logical step.

**[00:21:20]** That check covers a slightly weaker version of the result, which would still break ETH.

**[00:21:28]** And a group of experts, including Impagliazzo and Paturi, who proposed ETH in the first place, is examining the proof.

**[00:21:40]** We also ran the method's main steps on small puzzles with our own code, and it produces the exact counts.

**[00:21:47]** That can't confirm the proof for large puzzles, but it shows the ideas fit together.

## 10. Closing

**[00:21:55]** Let's recap. A puzzle of switches and rules, where trying everything doubles the work with every switch.

**[00:22:03]** Fifty years of shortcuts that made the growth gentler, but never changed its kind. A bet, ETH, that it never could.

**[00:22:15]** And now a paper that blends the puzzle with a dial, solves it at easy points,

**[00:22:21]** and follows a curve back to the true count, with a cost whose factor keeps sinking.

**[00:22:28]** If it holds up, the wall is still there for every puzzle we could ever build.

**[00:22:33]** But in principle, it was never a wall at all.

Total running time: 22 min 42 s.

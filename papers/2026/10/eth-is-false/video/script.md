# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `eth-is-false.mp4`. The narrators read a spoken version of each caption, the `say` text next to it in `eth_video.py`. The video writes the number of satisfying assignments as #F, like the paper; this script writes $N(F)$.

## 1. The claim

**[00:00:03]** On 26 October 2026, OpenAI posted a preprint with a startling title.

**[00:00:12]** A 3-CNF formula is an AND of clauses; each clause is an OR of three literals.

**[00:00:19]** 3-SAT asks: can we set the $n$ variables to 0 or 1 so that every clause is true?

**[00:00:28]** The obvious method tries all $2^n$ assignments. Every new variable doubles the work.

**[00:00:37]** Decades of clever algorithms lowered the base, from $2^n$ to about $1.307^n$ … but every one of them is still exponential.

**[00:00:49]** The Exponential Time Hypothesis (Impagliazzo–Paturi, 2001) says this is unavoidable.

**[00:01:00]** The preprint claims a deterministic algorithm that *counts* the solutions of any 3-CNF in subexponential time and polynomial space.

**[00:01:11]** That is not $\mathsf{P}=\mathsf{NP}$: a time like $2^{n/\sqrt{\log n}}$ still grows faster than every polynomial.

## 2. Counting is a polynomial sum

**[00:01:25]** Turn each clause into a polynomial $\Phi_e$: it is 1 when the clause is true and 0 when it is false.

**[00:01:34]** The product $(1-X_a)X_b(1-X_c)$ equals 1 only on the single violating assignment $(0,1,0)$.

**[00:01:49]** Multiply over all clauses and add over all $2^n$ assignments: the result is the number of solutions, $N(F)$.

**[00:02:01]** The paper first treats formulas where every variable occurs in at most 3 clauses; then $\prod_e \Phi_e$ has degree at most $3n$.

**[00:02:12]** (General $k$-CNF formulas are reduced to this case at the end.) The question is how to evaluate the sum faster.

## 3. The dream: independent groups

**[00:02:24]** Suppose the $n$ variables split into $r$ groups, and no clause touches two groups.

**[00:02:31]** Then the count factors: count each group on its own and multiply. The cost is about $r\cdot 2^{2n/r}$ instead of $2^n$.

**[00:02:45]** Real formulas are tangled: some clauses cross between groups, and the sum no longer factors.

**[00:02:53]** The idea: deform the polynomial so that, at special parameter values, clauses talk across groups only through a few integer summaries.

## 4. Deform, then separate

**[00:03:07]** Introduce a parameter $T$. In clause $e$, replace each input $X_v$ by a linear form whose coefficients are polynomials in $T$.

**[00:03:18]** At $T=0$ every form is $X_v$ again, so $H(0)=N(F)$. With coefficient degree at most $R$, $H$ has degree at most $3nR$.

**[00:03:33]** The forms are built so that at $T=t\in\lbrace 1,\dots,Q\rbrace$ each clause reads its own group of variables, plus a few integer measurements $y=Cx$ of the other groups.

**[00:03:47]** Fix all the measurements $\vec y$, and the groups decouple again: each group is summed on its own, and the results multiply.

**[00:03:57]** Cost: (number of measurement values) $\times$ (assignments of one group). Subexponential, if there are few measurements and many groups.

**[00:04:09]** But this only works at $T=1,\dots,Q$. We still need $H(0)$.

## 5. From easy points back to T = 0

**[00:04:19]** We can now evaluate $H$ at $t=1,\dots,Q$ quickly. But the number we want is $H(0)=N(F)$.

**[00:04:27]** $Q$ values cannot determine a polynomial of degree up to $3nR$: many curves pass through the same points, with different values at $0$.

**[00:04:39]** Instead, compute several Taylor coefficients of $H$ at each point: value, slope, curvature, …

**[00:04:48]** With $J$ coefficients at each of $Q$ points and $QJ\gt \deg H$, only one polynomial fits: Hermite interpolation recovers $H$, hence $H(0)$.

**[00:05:03]** Each Taylor coefficient costs extra sums (an inclusion–exclusion over $\le J$ variables). That is cheap only if $R\ll Q$: low degree, many points.

## 6. Low degree, many points: the matrix trick

**[00:05:21]** Multiplying a term by $(1-T/s)$ keeps it at $T=0$ and deletes it at $T=s$, at the price of one degree. Each term can afford at most $R-1$ such factors.

**[00:05:37]** Give each occurrence (clause $e$, variable $v$) a label: at every point $s$, the pair (group of $v$, group assigned to $e$). A word of $Q$ pairs.

**[00:05:52]** The swap $\Pi_s$ exchanges the two entries of pair $s$. After swapping, the coordinate lives in the clause's own group at point $s$.

**[00:06:04]** Write every coordinate as a measured part plus a local part, using $M_0=V_0f(W_0)$ with $W_0=\frac12\sum_s(I-\Pi_s)$ and $\deg f\le R-1$.

**[00:06:23]** The swaps share an eigenbasis. On an eigenvector with $j$ antisymmetric factors, $M_0$ acts by the number $(-1)^jf(j)$.

**[00:06:36]** Across all basis vectors, $j$ is binomially distributed, with spread about $\sqrt Q$.

**[00:06:44]** Choose $f$ to interpolate $(-1)^j$ on $R$ values of $j$ around the peak. There $M_0$ acts as the identity; only the thin tails need measuring.

**[00:06:58]** Because $\deg f\le R-1$, each term of $M_0$ disagrees with the clause's group at no more than $R-1$ points, so a degree-$(R-1)$ multiplier removes it there.

**[00:07:12]** Taking $R\gg\sqrt Q$ makes the measured tails tiny, while $R\ll Q$ keeps the Taylor step cheap.

## 7. Paying the bill

**[00:07:23]** The total work is a product of three costs. With the chosen parameters each one is $2^{o(n)}$.

**[00:07:32]** Multiplied together: $2^{O(n(\log\log n)^2/\sqrt{\log n})}$ for bounded-occurrence formulas — and only polynomial space, since nothing is tabulated.

**[00:07:48]** General $k$-CNF formulas: split them into sparse formulas, compress the clauses into $O(n)$ sparse parity tests, and count the common solutions with the same machinery.

**[00:08:02]** A parity test passes when an integer sum is even. The Beigel–Tarui polynomial detects evenness modulo $2^\ell$, so the count is recovered exactly modulo $2^{n+1}$.

**[00:08:19]** With a sharper recursive analysis, the paper's main theorem reaches exponent $O(n\log\log n/\sqrt{\log n})$ for every fixed $k$.

## 8. What falls, and what does not

**[00:08:34]** If the proof holds, it refutes ETH and its relatives SETH, #ETH, Gap-ETH and NSETH, which underpin a large body of conditional lower bounds.

**[00:08:49]** The paper also derives subexponential exact counting for graph colorings and perfect matchings, and a new circuit lower bound for $\mathsf{E}^{\mathsf{NP}}$.

**[00:09:01]** It does not settle P vs NP: subexponential is still superpolynomial, and $2^{o(n)}$ bounds do not transfer through general reductions.

**[00:09:12]** It is also not a practical solver: with the explicit parameters of the paper's overview, the machinery only switches on when $\log_2 n$ is about $10^{10}$.

**[00:09:26]** Status: a preprint with a reported Lean formalization, now being examined by experts, including the hypothesis's originators.

Total running time: 9 min 43 s.

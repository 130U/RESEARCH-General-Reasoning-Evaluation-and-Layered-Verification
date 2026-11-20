# General Reasoning Evaluation and Layered Verification

**Duke University × Frontier AI Research Laboratory**  
Letao (Theodore) Ouyang · Researcher · Durham, North Carolina; Palo Alto, California · September 2023 – September 2026

**Confidentiality and disclosure.** I conducted this project through a Duke University collaboration with a frontier AI research laboratory from September 2023 to September 2026. The partner's name and proprietary system identifiers are withheld under a nondisclosure agreement. The project title, my role, locations, dates, system architecture and mathematical formulations are cleared for public disclosure. Production records and operating figures are withheld; the measurements in Section 6 are taken on a test set whose verdicts are known exactly.

## Summary

A model can reach the right answer through an unsupported step, and a grader that matches a reference solution will reject a correct proof that takes another route. I designed an acceptance rule that resolves both: a conclusion stands when its assumptions, derivations and execution evidence support it, whichever valid route was taken, and a failed step removes support from everything downstream. Checkable obligations are discharged by certificates that need no reference solution, LLM-assisted screening flags possible gaps, and specialists adjudicate what remains. I also derived what a grader must achieve before its verdicts can be used. A policy trained against a grader converges to that grader's positive predictive value, which on a test set of 3,600 submissions with known verdicts is 40% for final-answer matching and 100% for certificate checking.

## Problem and Approach

The question I took up in late 2023 was what should entitle a model's reasoning to be accepted. A correct answer can coexist with unsupported assumptions, misapplied rules or tool use that violates the task specification, and a fixed reference path will reject sound work that takes another route. I designed an acceptance rule around proof obligations: a conclusion stands when its assumptions, derivations and execution evidence support it, whichever valid route the model took, and a failed obligation removes support from everything that depends on it. Programmatic certificates discharge checkable obligations, LLM-assisted screening identifies possible gaps, and specialist scholars adjudicate disputed semantic questions.

Two things follow from defining acceptance this way. A certificate bounds how far a submission is from the truth using only a residual the submission exposes and a constant the task designer has verified, so the check never consults a reference solution and inherits none of its errors. And once a grader's two error rates are named, they can be priced: I derived the false-acceptance rate below which a leaderboard lead is certified, the level of true validity a policy can reach when the grader is its reward, and the screening sensitivity at which an LLM judge may decide instead of screen. I kept refining the design through September 2026. Sections 1 through 7 set out the acceptance criteria, the certificates, the thresholds, the measurements and the related literature.

The team produced roughly 500 scientific reasoning tasks a week. Each task included a detailed, step-by-step reference solution and repeated verification of the argument.

## Key Contributions

* **I developed a proof-obligation framework that defines when a model's reasoning should be accepted.** Starting in late 2023, I organized deliverables into dependency graphs ($`\Gamma_q \vdash C_q`$) that link each conclusion to its domain assumptions, method applicability, evidentiary support, compliant execution, uniform approximation bounds and claimed strength. Valid alternative derivations pass on the same terms as the reference route. When a step fails, the graph locates the first unsupported step and what it affects downstream. For tasks that admit formalization, checking local nodes and their dependencies within a sound inference system establishes the full conclusion.
* **I developed checkable error certificates and bounds on solution quality for programmatically verifiable task families.** The projected-residual optimality bound ($`0 \le f(x) - v^* \le \|P_{\ker\,A} r\|_2^2 / (2\mu)`$) splits feasibility, stationarity and the accuracy of a conclusion into separate verification obligations, and different proofs can pass by satisfying the same ones. The same template, a residual the submission exposes, a constant the designer verifies and an inequality between them, covers convex programs, linear systems, eigenpairs and fixed points. None of these checks needs a reference solution.
* **I established complementary forms of verification across mathematical certificates, code and rule checks, LLM-assisted screening and specialist adjudication, and later programs reused the layered design.** Code checks directly verifiable answers, required deliverables, tool permissions and other requirements specified in advance. LLM-as-a-Judge helps flag missing evidence, misapplied rules and gaps in reasoning, and disputed domain judgments go to scholars with relevant expertise. I derived when a screen may decide: at screening sensitivity $`\text{se}`$, a share $`1 - \alpha^*/(1 - \text{se})`$ of unflagged work still has to reach specialists to hold the system's false acceptance at $`\alpha^*`$.
* **I evaluated answers, visible reasoning and execution evidence together.** I cross-checked the model's displayed CoT against its actual tool calls, return values and intermediate outputs to test whether what it claimed had observable support. From elapsed time, attempt counts and changes in intermediate results I identified repeated operations, continued use of failed assumptions and attempts that added no evidence. I recorded correctness, compliance and efficiency as separate results, and a resource limit counted toward acceptance only when the task specification set it beforehand.
* **I derived how false acceptance ($`\alpha`$) and false rejection ($`\beta`$) reverse model rankings, and the condition under which a ranking is certified.** In the worked example, models with true validity rates of 72% and 64% score 73.12% and 76.96%, so the weaker one ranks first. A lead of $`g`$ over a rival scoring $`s_B`$ certifies the order of true validity exactly when the grader's false-acceptance rate is below $`g / (1 - s_B)`$.
* **I showed that a policy optimized against a grader converges to the grader's positive predictive value.** The observed score goes to 100% while true validity stops at $`\theta(1-\beta) / [\theta(1-\beta) + (1-\theta)\alpha]`$. False acceptance sets the ceiling, and false rejection removes valid routes from what the policy produces. The same analysis gives the bias in the binary cross-entropy gradient used to train process reward models ($`E[\nabla_s \ell(s,V) - \nabla_s \ell(s,Z) \mid h] = p(h) - \tilde{p}(h)`$).
* **I gave the tolerance-propagation rule ($`a\delta + 2\varepsilon`$) for bijective task transformations and its composition law for chains of transformations.** Together they say when a transformed task still supports a valid comparison and what tolerance its solutions are owed.
* **On a test set of 3,600 exact-arithmetic submissions from 600 strongly convex quadratic task families, every verdict known, final-answer matching accepted 75.0% of the invalid submissions and strict reference-path matching rejected 50.0% of the valid proofs.** Certificate checking accepted all 1,200 valid proofs and rejected all 2,400 invalid submissions, so strict error detection and acceptance of valid alternative routes held together on the same set.

## Manuscript

### 1. Correct answers can conceal invalid reasoning and reverse model rankings

Checking the final answer is enough only when the answer is the entire deliverable. In the samples analyzed for *ProcessBench*, the share of solutions with correct final answers that still contain a process error rises with difficulty: 3.5% on GSM8K, 18.8% on MATH, 32.2% on OlympiadBench and 51.8% on Omni-MATH (*[ProcessBench, Section 3.3](https://arxiv.org/html/2412.06559v2)*). Answer accuracy and the validity of a reasoning trace are distinct evaluation targets, and they come apart fastest on the problems that matter most. For a task that also requires a derivation or a specified execution process, I examine domain assumptions, method applicability, supporting evidence, tool compliance, intermediate results and the conclusion. I treat the model's displayed CoT and visible reasoning as observable outputs and cross-check them against execution records.

To see what this does to a score, suppose problems and model trajectories are drawn from a target capability distribution. Let $`Z = 1`$ indicate that the complete solution, including its reasoning steps and tool execution, is valid, and let $`V = 1`$ indicate that the evaluation protocol accepts it. For model $`m`$, define its true validity rate as $`\theta_m = \Pr_m(Z = 1)`$, its false acceptance rate as $`\alpha_m = \Pr_m(V = 1 \mid Z = 0)`$, and its false rejection rate as $`\beta_m = \Pr_m(V = 0 \mid Z = 1)`$. False acceptance can let through an unsupported derivation, or a tool call that produces the correct answer while violating a predefined execution requirement; false rejection can exclude a valid alternative derivation. By the law of total probability:

```math
s_m = E_m[V] = \alpha_m + (1 - \alpha_m - \beta_m)\theta_m, \qquad s_m - \theta_m = \alpha_m(1 - \theta_m) - \beta_m\theta_m \qquad (1.1)
```

The term $`\alpha_m(1 - \theta_m)`$ credits invalid trajectories, while $`-\beta_m\theta_m`$ penalizes valid ones. Adding problems reduces the sampling variance of $`\hat{s}_m`$ and leaves the structural gap $`s_m - \theta_m`$ in place. Models also differ in how closely they adhere to evidence requirements, verification steps and tool permissions, and the resulting differences in $`\alpha_m`$ and $`\beta_m`$ can reverse their ranking. Suppose Models A and B have true validity rates of $`\theta_A = 72\%`$ and $`\theta_B = 64\%`$. If invalid trajectories pass the final-answer check with probabilities $`\alpha_A = 4\%`$ and $`\alpha_B = 36\%`$, with $`\beta_A = \beta_B = 0\%`$, their observed scores are $`s_A = 73.12\%`$ and $`s_B = 76.96\%`$, and the model with the lower rate of fully valid solutions ranks higher. Any $`\alpha_B`$ above 25.3% reverses this pair.

Public leaderboards have shown the effect at scale. When EvalPlus extended HumanEval's tests 80-fold, pass@k fell by up to 19.3% to 28.9%, models changed places, and 18 of the original reference solutions, 11% of the problems, were found defective ([EvalPlus](https://arxiv.org/abs/2305.01210)).

**When a lead is certified.** Equation (1.1) can be read in the other direction. If a grader's false acceptance is known to be at most $`\bar{\alpha}`$ and its false rejection at most $`\bar{\beta}`$, a score pins true validity to an interval, and with $`\bar{\beta} = 0`$ a lead of $`g = s_A - s_B`$ certifies the order of true validity under one condition:

```math
\frac{s - \bar{\alpha}}{1 - \bar{\alpha}} \le \theta \le \frac{s}{1 - \bar{\beta}}, \qquad \theta_A > \theta_B \ \text{ for every admissible grader} \iff \bar{\alpha} < \frac{g}{1 - s_B} \qquad (1.2)
```

The condition is tight: at any larger $`\bar{\alpha}`$ there are error rates within the bound that reverse the order. A lead of three points over a rival scoring 80% is certified only when the grader's false acceptance is below 15%; over a rival scoring 50%, below 6%. The harder the evaluation, the better the grader has to be before a small lead means anything. This turns the reversal above from a warning into a test that can be applied to any published ranking whose grader has a measured error rate.

Process supervision extends evaluation to intermediate steps (*[Let's Verify Step by Step, Sections 2 and 3](https://arxiv.org/html/2305.20050v1)*). When I apply it to general post-training evaluation, I account for omissions in reference solutions, accept valid alternative methods, and enforce evidence and execution requirements defined before responses are generated. Structural simplification can explain a method or reveal redundant work. A slower solution, or one that takes more attempts, is still a correct solution, and a resource-related rejection requires a hard limit specified in advance.

### 2. Proof obligations organize layered review and allow alternative solutions

A task specification defines the domain assumptions and execution constraints $`\Gamma_q`$, the target conclusion $`C_q`$, and the proof obligations needed to establish it. A model trajectory $`\tau`$, which here means its visible reasoning and observable execution records, may get there through different intermediate lemmas, representations or orders of deduction. That is allowed, because review concerns the submitted material and whether it fulfills the task's obligations. A directed acyclic dependency graph (DAG) $`G`$ organizes the local soundness check for each node $`v_j`$, together with a global tool-compliance predicate $`𝒯_{\text{comp}}(\tau) \in \{0, 1\}`$:

```math
\Gamma_q \cup \{v_k : k \in \mathrm{pa}(j)\} \vdash v_j, \qquad \Gamma_q \cup \{v_j : j \in \mathrm{sink}(G)\} \vdash C_q, \qquad 𝒯_{\text{comp}}(\tau) = 1 \qquad (2.1)
```

The symbol $`\vdash`$ denotes valid derivability within a sound domain inference system, and the condition $`𝒯_{\text{comp}}(\tau) = 1`$ certifies that each external tool invocation $`t \in \tau`$ belongs to the task's permitted execution environment $`𝒜_q`$. If root nodes follow from verified assumptions $`\Gamma_q`$, every dependency is sound, with its local derivation verified in that system, and $`𝒯_{\text{comp}}(\tau) = 1`$, structural induction over a topological ordering of $`G`$ establishes the full conclusion.

This is the discipline of certifying algorithms carried over to model output. The producer may be arbitrarily complex and is not trusted; it has to hand over a witness, and the checker of that witness is simple enough to be trusted ([McConnell et al.](https://doi.org/10.1016/j.cosrev.2010.09.009)). A model is the least trusted producer there is, which makes the checker the place to spend rigor.

In production, I divided verification into three layers:
1. Code and rule checks cover the directly verifiable parts of an answer, required deliverables, and predefined restrictions on tools, execution environments and resources. Tool compliance requires $`𝒯_{\text{comp}}(\tau) = 1`$, and a call that violates an explicit hard requirement causes rejection ($`V = 0`$) even when the final answer is correct.
2. LLM-as-a-Judge assists with semantic screening. It flags insufficient evidence, misapplied rules, conclusions that exceed their premises and gaps in reasoning, and it links each concern to the relevant trace, tool response or intermediate output. The flags direct further review.
3. Scholars with relevant expertise take the questions that require domain judgment, admit several reasonable interpretations, or remain disputed after the first two checks. They examine the evidence, the applicability of the method and the conclusion, and a question that cannot be resolved from the available evidence stays open.

All three layers work from the same observable material. I cross-check the model's displayed CoT and visible reasoning against actual tool calls, intermediate outputs, elapsed time and attempt counts. For each attempt I look for new evidence, revised premises or a change in the state of the solution. That is how I identify repeated calls, continued use of failed assumptions and loops that make no progress. A conclusion whose execution records are missing is recorded as unverified. I record efficiency separately from correctness and compliance: long runtimes, repeated attempts or exhaustive methods are analyzed as efficiency, and they affect acceptance only when they violate a predefined hard limit.

Method applicability has its own check, because pointwise convergence at a fixed parameter value does not establish that an approximation remains valid within an optimization, an integral or an exchange of limits. A claim about the order of accuracy requires an approximation parameter, its domain of validity and a uniform error bound. Where such an issue cannot be decided programmatically, an LLM helps locate the concern and a specialist scholar reviews the assumptions and derivation. Specialist review settles the question with the standing of expert judgment; a certificate settles it by computation.

For feedback, I record the first failed obligation at node $`v_j`$ and mark its descendant subgraph $`\mathrm{desc}(v_j)`$ as unverified, since locally correct calculations under a false premise do not repair the full derivation. This treatment resolves the ambiguity after an error discussed in *[ProcessBench, Section 3.1](https://arxiv.org/html/2412.06559v2)*. A suspected error awaiting specialist review remains unresolved until that review is complete.

**When a screen may decide.** The division between the second and third layers has a quantitative form. Let $`\text{se}`$ be the screen's sensitivity on semantic obligations, the share of invalid steps it flags. Flagged work goes to specialists, and unflagged work goes to specialists with probability $`\rho`$. With the specialists' verdict as the reference, the system's false acceptance on those obligations, and the random escalation needed to hold it at a target $`\alpha^*`$, are:

```math
\alpha_{\text{sys}} = (1 - \text{se})(1 - \rho), \qquad \rho \ge 1 - \frac{\alpha^*}{1 - \text{se}} \qquad (2.2)
```

The best model tested by [Tyen et al.](https://arxiv.org/abs/2311.08516) located the first mistake in 52.87% of reasoning traces. At a sensitivity of that order and a target of $`\alpha^* = 5\%`$, 89% of unflagged work still has to reach a specialist, and the screen saves almost no expert time. At $`\text{se} = 0.80`$ the share is 75%, at $`0.90`$ it is 50%, and only at $`\text{se} \ge 0.95`$ can unflagged work pass without review. That is the rule behind the layer boundary: an LLM judge screens until its measured sensitivity clears $`1 - \alpha^*`$, and decides after. The randomly escalated share is also the calibration sample, because a screen whose unflagged output is never reviewed has no measured sensitivity at all. A checker earns decisive standing by a clean run: 59 known-invalid items rejected without exception bound its false acceptance at 5% with 95% confidence, and 299 bound it at 1%.

Related work approaches these questions from several directions. [ToolEval](https://arxiv.org/html/2307.16789v1) scores tool-using agents by pass rate and win rate, both assigned by an LLM evaluator, so its verdicts carry the standing of a screen. [Let's Verify Step by Step](https://arxiv.org/html/2305.20050v1) collected step-level human labels and withheld reference solutions so that labelers would not favor one route. [Math-Shepherd](https://arxiv.org/html/2312.08935v1) estimates the quality of a step from whether sampled continuations reach the correct answer, which scores a step by its outcome; the certificates of Section 3 check the mathematical validity of the evidence a submission actually presents. [ProcessBench](https://arxiv.org/html/2412.06559v2) has since measured how often correct answers conceal process errors on hard problems. My contribution is the organization of acceptance itself, through explicit proof obligations, a dependency structure over them and conditions that can be checked.

### 3. Error certificates that need no reference solution

A posteriori verification rests on one observation: to bound how far a candidate is from the truth, it is enough to have a residual the candidate exposes and a stability constant of the problem. The true solution never enters. I develop the template in full on an optimization family whose constraints and certificates can be checked explicitly, and then state it for the other task types it covers.

Consider the equality-constrained quadratic problem:

```math
v^* = \min_{Ax = b} f(x), \qquad f(x) = \frac{1}{2}x^\top H x + c^\top x, \qquad Z^\top H Z \succeq \mu I, \quad \mu > 0 \qquad (3.1)
```

Here $`H`$ is symmetric, $`Ax = b`$ is feasible, the columns of $`Z`$ form an orthonormal basis of $`\ker\,A`$, and $`\mu`$ is a verified lower bound on curvature along feasible directions. The objective has to be strongly convex only on the feasible manifold; $`H`$ may be indefinite across the constraints. For any feasible candidate $`x`$ satisfying $`Ax = b`$, choose any dual multiplier vector $`\nu`$ and define the stationarity residual $`r = Hx + c + A^\top \nu`$. Curvature gives the first inequality below for every feasible displacement $`d \in \ker\,A`$, and completing the square in $`d`$ gives an exact optimality error certificate:

```math
f(x + d) \ge f(x) + r^\top d + \frac{\mu}{2}\|d\|^2 \qquad (3.2)
```

```math
\inf_{d \in \ker\,A} \left( r^\top d + \frac{\mu}{2}\|d\|^2 \right) = -\frac{\|P_{\ker\,A} r\|_2^2}{2\mu} \qquad (3.3)
```

```math
0 \le f(x) - v^* \le \frac{\|P_{\ker\,A} r\|_2^2}{2\mu} \qquad (3.4)
```

The operator $`P_{\ker\,A}`$ is the orthogonal projection onto the space of feasible directions $`\ker\,A`$. It removes residual components normal to the constraints, which do not affect optimality along the feasible manifold (*[Boyd and Vandenberghe, Convex Optimization, Sections 5.5 and 9.1](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)*). A zero projected residual, $`P_{\ker\,A} r = 0`$, certifies exact optimality, and otherwise the certificate bounds the suboptimality gap in objective units. Two kinds of submission fare differently under this check:
- Solutions derived through Lagrange multipliers or by eliminating the equality constraints satisfy the same semantic obligations and pass verification.
- Reporting the correct optimal value $`v^*`$ alone leaves the obligations undischarged. Feasibility and the claimed objective value are checked separately. A submission that claims a KKT multiplier witness must also have its full stationarity equation $`Hx+c+A^\top\nu=0`$ verified, because the projected-residual bound cannot validate that multiplier: $`P_{\ker\,A}A^\top\nu=0`$ for every $`\nu`$. A valid equality-elimination proof need not supply a multiplier witness. Whether a checker validates the whole of a claimed witness is what the formal verification of certifying computations examines ([Alkassar et al.](https://arxiv.org/abs/1301.7462)), and Section 6 tests for it directly.

The same three parts, a residual, a verified constant and an inequality between them, give a certificate for each of the following task types.

**Table 1. Error certificates by task type.**

| Task type | Residual the submission exposes | Constant the task designer verifies | Certificate |
| --- | --- | --- | --- |
| Equality-constrained quadratic program (above) | $`P_{\ker\,A} r`$ | $`\mu = \lambda_{\min}(Z^\top H Z)`$ | $`f(x) - v^* \le \lVert P_{\ker\,A} r\rVert _2^2 / (2\mu)`$ |
| Convex program | A primal-feasible $`x`$ and a dual-feasible $`(\lambda, \nu)`$ | None | $`f(x) - v^* \le f(x) - g(\lambda, \nu)`$ |
| Linear system $`Ax = b`$ | $`b - Ax`$ | A lower bound on $`\sigma_{\min}(A)`$ | $`\lVert x - x^*\rVert _2 \le \lVert b - Ax\rVert _2 / \sigma_{\min}(A)`$ |
| Eigenpair of a symmetric matrix | $`A\hat{v} - \hat{\lambda}\hat{v}`$ | None | $`\min_i \left\lvert \lambda_i - \hat{\lambda}\right\rvert  \le \lVert A\hat{v} - \hat{\lambda}\hat{v}\rVert _2 / \lVert \hat{v}\rVert _2`$ |
| Fixed point of a contraction $`g`$ | $`g(x) - x`$ | A Lipschitz constant $`L < 1`$ | $`\lVert x - x^*\rVert  \le \lVert g(x) - x\rVert  / (1 - L)`$ |

Each row is a standard result of its field. What I take from them is the organization: every obligation type is paired with a certificate and a checker whose cost is a few matrix products, and acceptance becomes a computation on the submission alone. That removes the reference solution from the trusted base. Reference solutions are a source of grading error in their own right, as the 18 defective references found by [EvalPlus](https://arxiv.org/abs/2305.01210) show, and a grader that matches against them inherits every one.

I carry the lessons from this family over to the structure of general review: check the inputs and assumptions, compliance with the execution specification, support for the derivation, and whether the conclusion exceeds the evidence. Obligations that admit programmatic checks go to rules or certificate verifiers, and other semantic questions go through LLM-assisted screening and specialist review. Structural simplification may explain why a method needs less repeated work, and efficiency gains and validity certificates are evaluated separately.

### 4. Task transformations must propagate error bounds

Symbolic templates parameterize variable domains and answer formulas (*[GSM-Symbolic, Section 3.1](https://arxiv.org/html/2410.05229v1)*). Tasks with formalizable transformations also need verifiable rules for how those transformations affect feasible sets, objective values and acceptance tolerances. For bijective task transformations the tolerance-propagation rule below follows.

Let an original problem and its transformed variant have feasible sets $`F`$ and $`F'`$, objectives $`J`$ and $`J'`$, and finite infima $`v`$ and $`v'`$. Suppose the task designer verifies a bijection $`\Phi : F \to F'`$ such that every feasible $`u \in F`$ satisfies the uniform bound:

```math
\left\vert J'(\Phi(u)) - aJ(u) - b\right\vert \le \varepsilon, \quad a > 0 \qquad (4.1)
```

```math
av + b - \varepsilon \le v' \le av + b + \varepsilon \qquad (4.2)
```

```math
J(u) - v \le \delta \implies J'(\Phi(u)) - v' \le a\delta + 2\varepsilon \qquad (4.3)
```

Taking infima in (4.1) gives (4.2), and subtracting the lower bound on $`v'`$ from the upper bound on $`J'(\Phi(u))`$ gives (4.3). So after a unit conversion, parameter rescaling or numerical transformation with error bounded by $`\varepsilon`$, the result determines the acceptance tolerance for a previously $`\delta`$-optimal solution. Keeping the original tolerance $`\delta`$ can misclassify a valid transformed solution as a model failure, while relaxing it arbitrarily can conceal a real capability gap. When $`\varepsilon = 0`$, the bijection and positive scaling $`a > 0`$ also preserve whether an optimum is attained. Changes to boundary compactness or admissible control classes require a new attainment proof.

Variants are usually built by several transformations in a row. Applying the bound step by step to a chain with parameters $`(a_1, \varepsilon_1), \dots, (a_k, \varepsilon_k)`$ gives the composition law:

```math
a = \prod_{j=1}^{k} a_j, \qquad \varepsilon = \sum_{j=1}^{k} \Big( \prod_{l > j} a_l \Big) \varepsilon_j, \qquad J(u) - v \le \delta \implies J^{(k)} - v^{(k)} \le a\delta + 2\varepsilon \qquad (4.4)
```

Each error is magnified by every scaling applied after it, so the order of a chain is part of its specification. Take an exact unit conversion with $`a = 100`$, an exact rescaling with $`a = 0.5`$, and a numerical discretization with $`\varepsilon = 0.003`$, applied to a solution that is $`\delta = 0.01`$ optimal. With the discretization last, the chain has $`(a, \varepsilon) = (50, 0.003)`$ and the tolerance owed is $`0.506`$. With the discretization first, it has $`(50, 0.15)`$ and the tolerance is $`0.8`$. A grader that reuses the first tolerance for the second chain rejects valid work.

### 5. Grading errors change the post-training objective

Step-level labels can improve post-training only if they measure logical validity and compliance, because systematic grading errors pass into the targets used by process reward models (PRMs) and RLHF policies. Let $`h`$ denote the task input and the model's visible reasoning prefix through the current step. Let $`Z = 1`$ indicate that the step is valid under the problem's assumptions, and let $`V \in \{0, 1\}`$ be the grader's noisy acceptance label, with conditional false acceptance $`\alpha(h)`$ and false rejection $`\beta(h)`$. Writing $`p(h) = \Pr(Z = 1 \mid h)`$, a process evaluator with logit $`s`$ trained by binary cross-entropy is optimized toward the corrupted conditional target:

```math
\tilde{p}(h) = \alpha(h) + [1 - \alpha(h) - \beta(h)]p(h) \qquad (5.1)
```

```math
\frac{\partial \ell(s, V)}{\partial s} = \sigma(s) - V \qquad (5.2)
```

```math
E[\nabla_s \ell(s, V) - \nabla_s \ell(s, Z) \mid h] = p(h) - \tilde{p}(h) \qquad (5.3)
```

The expected gradient difference shows which way grading bias moves the training target:
- If false rejection dominates, $`\beta(h)p(h) > \alpha(h)[1-p(h)]`$, then $`\tilde{p}(h) < p(h)`$. The learned validity target shifts downward, which penalizes valid alternative proofs.
- If false acceptance dominates, $`\alpha(h)[1-p(h)] > \beta(h)p(h)`$, then $`\tilde{p}(h) > p(h)`$. The target shifts upward, rewarding flawed proofs or noncompliant tool calls. When the weighted contributions are equal, the effects cancel in the conditional mean.

When $`\alpha, \beta`$ are known constants with $`\alpha + \beta < 1`$, class-conditional noise correction removes the bias from the mean estimate (*[Learning with Noisy Labels, Sections 2 and 3](https://papers.nips.cc/paper_files/paper/2013/file/3871bd64012152bfb53fdf04b401193f-Paper.pdf)*). The estimator is the prevalence correction of [Rogan and Gladen](https://pubmed.ncbi.nlm.nih.gov/623091/), and it increases variance by the squared factor below:

```math
\hat{\theta}_{\text{corr}} = \frac{\bar{V} - \alpha}{1 - \alpha - \beta}, \qquad \mathrm{Var}(\hat{\theta}_{\text{corr}}) = \frac{\mathrm{Var}(\bar{V})}{(1 - \alpha - \beta)^2} \qquad (5.4)
```

For task families whose validity is exactly decidable by a sound and complete certificate verifier, $`\alpha=\beta=0`$ and there is nothing to correct.

**What a policy learns from a grader.** Equations (5.1) and (5.4) describe a grader that is only observed. Once its verdict is the reward, the policy moves toward whatever the grader accepts. Model that as reweighting the policy's trajectories by $`e^{\eta V}`$, with $`\eta`$ the strength of optimization. A policy that starts at true validity $`\theta`$ then has:

```math
\theta_\eta = \frac{\theta(1-\beta)e^{\eta} + \theta\beta}{\big[\theta(1-\beta) + (1-\theta)\alpha\big]e^{\eta} + \theta\beta + (1-\theta)(1-\alpha)} \ \xrightarrow{\ \eta \to \infty\ } \ \frac{\theta(1-\beta)}{\theta(1-\beta) + (1-\theta)\alpha} \qquad (5.5)
```

The limit is the grader's positive predictive value at the starting policy, and the observed score goes to 100% along the way. For Model B of Section 1 under final-answer matching:

**Table 2. Observed score and true validity of Model B under final-answer matching as optimization strengthens.**

| Optimization strength $`\eta`$ | 0 | 1 | 2 | 4 | Limit |
| --- | --- | --- | --- | --- | --- |
| Observed score | 77.0% | 90.1% | 96.1% | 99.5% | 100% |
| True validity | 64.0% | 74.9% | 79.9% | 82.7% | 83.2% |

Two results follow, one for each kind of error.

- *False acceptance sets the ceiling.* The policy can reach the grader's positive predictive value and no more: 83.2% for Model B, 98.5% for Model A. With $`\alpha = 0`$ the ceiling is 100% for any $`\beta < 1`$.
- *False rejection removes routes.* A valid route that the grader always rejects loses its share of valid work at rate $`e^{-\eta}`$. If two valid routes start equally common and the grader accepts only one, the other falls from 50% of valid work to 26.9%, 11.9% and 1.8% at $`\eta = 1, 2, 4`$. Training against a reference path teaches the model to stop producing correct proofs the reference did not anticipate.

The cost of false acceptance is the ceiling and the cost of false rejection is diversity. Certificate checking has neither cost on the families it decides, which is the argument for drawing process rewards from certified nodes. It also locates the limit of a theoretical result sometimes read as making process supervision unnecessary: [Jia, Rakhlin and Xie](https://arxiv.org/abs/2502.10581) show that outcome supervision is statistically no harder than process supervision, up to polynomial factors in the horizon, when the outcome reward is the objective. When a correct answer can rest on an invalid derivation, the outcome reward is wrong about validity, and a policy trained on it converges to the limit in equation (5.5).

### 6. A test set with exactly known verdicts

Measuring a grader's two error rates requires submissions whose validity is known without appeal to any grader. I built such a test set from 600 strongly convex quadratic task families. Using exact rational arithmetic, each family yields 6 algebraic submissions, for 3,600 in total:
- 1,200 valid certificates, 2 per family: one derived using Lagrange multipliers and one using equality elimination.
- 2,400 submissions with controlled defects, 4 per family: (1) an infeasible construction, $`Ax \neq b`$, that reports the exact optimal value $`v^*`$; (2) failure of stationarity along a feasible direction in $`\ker\,A`$ while reporting $`v^*`$; (3) a claimed multiplier that fails the stationarity equation while reporting $`v^*`$; and (4) an incorrect final objective value. The first three classes, comprising 1,800 submissions or 75% of all invalid submissions, report the correct final answer $`v^*`$.

The composition is the instrument's design: three ways of being wrong with the right answer, one way of being wrong with the wrong answer, and two ways of being right. I compared three deterministic acceptance protocols on all 3,600 submissions:

**Table 3. Three acceptance protocols on 3,600 submissions with known verdicts.**

| Acceptance protocol | False acceptance rate on invalid submissions (2,400) | False rejection rate on valid certificates (1,200) | Valid share of accepted submissions |
| --- | --- | --- | --- |
| Final-answer matching only | 75.0% (accepts 1,800 flawed solutions) | 0.0% | 40.0% |
| Strict reference-path matching | 0.0% | 50.0% (rejects 600 valid elimination proofs) | 100.0% |
| Certificate verification | 0.0% | 0.0% | 100.0% |

Certificate verification accepted 1,800 fewer invalid proofs than final-answer matching and retained 600 more valid alternative solutions than strict reference-path matching. Strict error detection and acceptance of valid alternative proofs held together on the same submissions, which neither baseline managed. The projected-residual bound in equation (3.4) also held at all 600 feasible perturbations, one per family, and the verifier rejected every submission of defect class (3), the multiplier that a partial witness check would have let through.

The last column is the ceiling of Section 5. A policy trained against final-answer matching on this mix moves from one third valid work to 40% and stops. Trained against the reference path it reaches 100% and loses the elimination route. Trained against certificate checking it reaches 100% with both routes intact.

### 7. Dependence within task families and the economics of certificates

Surface variations of one problem template do not provide independent observations of general reasoning ability. Suppose there are $`F`$ independent task families, each with $`K`$ variants, common marginal variance $`\sigma^2`$, and common pairwise within-family correlation $`\rho_w`$. The sample mean then carries the Kish design effect $`1 + (K - 1)\rho_w`$, and its variance and effective sample size $`n_{\text{eff}}`$ are:

```math
\mathrm{Var}(\bar{Z}) = \frac{\sigma^2}{FK}[1 + (K - 1)\rho_w], \qquad n_{\text{eff}} = \frac{FK}{1 + (K - 1)\rho_w} \qquad (7.1)
```

For $`F = 50`$ families with $`K = 8`$ variants each, there are $`400`$ responses, and if $`\rho_w = 0.6`$, those $`400`$ responses provide the same precision as $`n_{\text{eff}} \approx 77`$ independent observations. Training and test sets are therefore split by task family, and new tasks vary assumptions, evidentiary relationships or the structure of a derivation, beyond substituting numbers.

Certificates cost engineering once and almost nothing afterwards. Let $`C_0`$ be the upfront engineering cost of the proof-obligation certificates and verifier, $`c_e`$ the expert review cost per submission, $`c_v`$ the automated verifier's unit execution cost, and $`u`$ the fraction of submissions escalated to human adjudication at the same expert unit cost. The certificate workflow is the cheaper one when submission volume $`N`$ exceeds:

```math
C_0 + N(c_v + uc_e) < Nc_e \iff N > \frac{C_0}{(1 - u)c_e - c_v}, \qquad (1 - u)c_e > c_v \qquad (7.2)
```

For a certificate family whose engineering costs as much as 400 expert reviews, with 15% of submissions escalated and a verifier run costing 2% of a review, the break-even is 482 submissions. Past that volume every further submission releases 83% of an expert review, and those hours go to the semantic obligations that only specialists can settle. The cost model covers the certificate layer; model calls and calibration are costed with the layers they belong to.

The team produced roughly 500 scientific reasoning tasks a week under this design, and later programs reused its layered structure.

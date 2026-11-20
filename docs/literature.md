# Where this work sits

What should entitle a model's reasoning to be accepted? Process supervision shows that right answers hide wrong
steps. The literature on LLM judges measures how unreliable a learned grader is. Certifying algorithms show how to
trust a result without trusting its producer. Noisy-label theory corrects a score for a grader's errors. Each holds
part of the answer. This page records what each line establishes, where it stops, and what the article adds. The
complete list of 186 sources is in the [bibliography](bibliography.md).

## The short version

| Line of work | What it establishes | Where it stops | What the article adds |
| --- | --- | --- | --- |
| Outcome and process supervision: Uesato et al., Lightman et al., Math-Shepherd, ProcessBench | Correct answers conceal process errors, more often on harder problems; step-level labels help | A step is judged by a labeler, a rollout or a learned model, each with its own error | Acceptance defined by proof obligations over a dependency graph, with certificates where a step can be computed |
| LLM judges: MT-Bench, JudgeBench, Tyen et al. | Judges are biased and weak on correctness; the best model finds the first mistake about half the time | Accuracy is reported; what it permits is not | The threshold at which a screen may decide, and the escalation rate below it |
| Certifying algorithms and optimization certificates: McConnell et al., Alkassar et al., Boyd and Vandenberghe | A witness checked by a simple, trusted checker; duality and residual bounds | Applied to solvers, whose output format is fixed | The same discipline for model output, organized as a catalogue of certificates per task type |
| Benchmark validity: EvalPlus, GSM-Symbolic, Miller | Weak tests and defective references change rankings; variants are correlated | A corrected benchmark, case by case | The condition under which a published lead is certified, from the grader's error bound alone |
| Noisy labels: Natarajan et al., Rogan and Gladen | Unbiased correction for known class-conditional noise | The grader is observed, not optimized against | The limit of a policy trained on the grader: its positive predictive value |
| Reward overoptimization: Gao et al., and the reports on rule-based and learned verifiers | A policy optimized against a proxy eventually loses true reward | Empirical curves | A closed form with two separate costs: false acceptance sets a ceiling, false rejection removes routes |

## Timing

The framework dates from late 2023. Process supervision on mathematics (2022 and 2023), certifying algorithms and
the classical certificates precede it. ProcessBench, JudgeBench, the theoretical comparison of outcome and process
supervision, and the reports of learned verifiers being exploited during reinforcement learning appeared while the
program was running. They measure, on public data, the two error rates the framework is built around.

## Key sources

### Answers and the steps behind them

<a id="uesato2022"></a>
**Uesato et al. (2022), "Solving Math Word Problems with Process- and Outcome-Based Feedback."** [arXiv](https://arxiv.org/abs/2211.14275)
Outcome supervision matches process supervision on final-answer error, and only process-based feedback brings the
error rate of the reasoning trace among correct answers down, from 14.0% to 3.4%. This is the premise of Section 1
in its first careful measurement. The trace labels come from annotators whose own agreement is limited, which is
the problem the certificate layer removes where it applies.

<a id="lightman2023"></a>
**Lightman et al. (2023), "Let's Verify Step by Step."** [arXiv](https://arxiv.org/abs/2305.20050)
Step-level human labels train a process reward model that outperforms an outcome-trained one, and labelers were
kept from the reference solutions so that they would not favor one route. The second decision is the one I
generalize: acceptance that does not depend on the route. The labels remain human judgments of each step, with no
structure that says what a failed step does to the steps after it.

<a id="wang2023"></a>
**Wang et al. (2023), "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations."** [arXiv](https://arxiv.org/abs/2312.08935)
A step is labeled by whether sampled continuations from it reach the correct answer. The method scales, and it
scores a step by its outcome: a flawed step that still leads to the right answer is labeled good. That is a source
of false acceptance by construction, the regime in which D8 shows the training target shifts upward.

<a id="zheng2024"></a>
**Zheng et al. (2024), "ProcessBench: Identifying Process Errors in Mathematical Reasoning."** [arXiv](https://arxiv.org/abs/2412.06559)
Among solutions with correct final answers, the share containing a process error is 3.5% on GSM8K, 18.8% on MATH,
32.2% on OlympiadBench and 51.8% on Omni-MATH. Only the earliest error is labeled, because the status of later
steps is ambiguous. The dependency graph resolves that ambiguity: descendants of the first failed node are
unverified.

<a id="ling2023"></a>
**Ling et al. (2023), "Deductive Verification of Chain-of-Thought Reasoning."** [arXiv](https://arxiv.org/abs/2306.03872)
Each step cites its premises, so that a model can check the step against those premises alone. This is the closest
prior structure to the obligation graph. Its local checks are LLM judgments, and it has no layer whose verdicts are
computations.

<a id="jia2025"></a>
**Jia, Rakhlin and Xie (2025), "Do We Need to Verify Step by Step?"** [arXiv](https://arxiv.org/abs/2502.10581)
Reinforcement learning from outcome rewards is statistically no harder than from process rewards, up to polynomial
factors in the horizon. The result holds when the outcome reward is the objective. Where a correct answer can rest
on an invalid derivation, the outcome reward is wrong about validity, and D9 gives where a policy trained on it
ends.

### Learned judges

<a id="tyen2024"></a>
**Tyen et al. (2024), "LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location."** [arXiv](https://arxiv.org/abs/2311.08516)
The best model tested located the first mistake in 52.87% of reasoning traces. The paper measures the sensitivity
of a screen. D4 says what that sensitivity permits: at a target of 5%, 89% of unflagged work still has to reach a
specialist.

<a id="zheng2023"></a>
**Zheng et al. (2023), "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena."** [arXiv](https://arxiv.org/abs/2306.05685)
A strong judge agrees with human preferences at a high rate and shows position, verbosity and self-enhancement
biases. Agreement on preference is not accuracy on validity, and the paper's remedy for mathematics, showing the
judge a reference answer, ties the verdict to one route.

<a id="tan2024"></a>
**Tan et al. (2024), "JudgeBench: A Benchmark for Evaluating LLM-based Judges."** [arXiv](https://arxiv.org/abs/2410.12784)
On pairs with one objectively correct and one incorrect response, many strong judges perform close to chance.
Judges are weakest on exactly the judgments an acceptance rule needs, and their error rates move with the model
version, which is why the layer boundary is a measured threshold and not a fixed assignment.

<a id="turpin2023"></a>
**Turpin, Michael, Perez and Bowman (2023), "Language Models Don't Always Say What They Think."** [arXiv](https://arxiv.org/abs/2305.04388)
Biasing features change a model's answers while its explanations almost never mention them. Displayed reasoning is
an output to be checked against execution records, which is how the framework treats it.

### Trusting a result without trusting its producer

<a id="mcconnell2011"></a>
**McConnell, Mehlhorn, Näher and Schweitzer (2011), "Certifying Algorithms."** [doi](https://doi.org/10.1016/j.cosrev.2010.09.009)
A certifying algorithm returns a witness with its output, and a checker simple enough to be trusted validates the
witness. The survey develops the idea for algorithms with fixed output formats. A model is the least trusted
producer there is, and I carry the discipline to its output.

<a id="alkassar2014"></a>
**Alkassar, Böhme, Mehlhorn and Rizkallah (2014), "A Framework for the Verification of Certifying Computations."** [arXiv](https://arxiv.org/abs/1301.7462)
Trust in a certified computation needs a proved witness property and a verified checker, and formal verification
of a widely used checker found a test it had omitted. The multiplier defect of Section 6 is this class of omission,
which the test set probes directly.

<a id="boyd2004"></a>
**Boyd and Vandenberghe (2004), Convex Optimization.** [pdf](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf)
The duality-gap certificate and the strong-convexity bound on suboptimality from the gradient norm. The projected
residual certificate is the second restricted to the feasible directions of an equality-constrained problem, where
curvature is needed only on the kernel of the constraints.

<a id="cheung2017"></a>
**Cheung, Gleixner and Steffy (2017), "Verifying Integer Programming Results."** [arXiv](https://arxiv.org/abs/1611.08832)
Solver results are turned into lists of statements checked by a few inference rules in exact rational arithmetic.
This is the structural analogue of the obligation graph in optimization software, and the reason the test set of
Section 6 is built in exact arithmetic.

<a id="zhou2024"></a>
**Zhou et al. (2024), "Don't Trust: Verify."** [arXiv](https://arxiv.org/abs/2403.18120)
Informal solutions are autoformalized and checked in a proof assistant, with filters for the fidelity of the
formal statement. Formal checking moves the risk of false acceptance from the proof to the statement. Certificates
keep the statement in the task designer's hands: the obligation and its constant are fixed before any response
exists.

### Graders under optimization

<a id="liu2023"></a>
**Liu, Xia, Wang and Zhang (2023), "Is Your Code Generated by ChatGPT Really Correct?" (EvalPlus).** [arXiv](https://arxiv.org/abs/2305.01210)
Extending HumanEval's tests 80-fold lowered pass rates by up to 19.3% to 28.9%, changed the order of models and
exposed 18 defective reference solutions. A public leaderboard with a measured false-acceptance problem. D2 states
the test such a ranking has to pass.

<a id="gao2023"></a>
**Gao, Schulman and Hilton (2023), "Scaling Laws for Reward Model Overoptimization."** [arXiv](https://arxiv.org/abs/2210.10760)
True reward rises and then falls as a policy is optimized against a proxy reward model. The curves are empirical.
D9 gives a closed form for a binary grader and separates the two errors: false acceptance sets the ceiling and
false rejection removes valid routes.

<a id="huang2025"></a>
**Huang, Zeng, Zeng, Zhu and He (2025), "From Accuracy to Robustness: A Study of Rule- and Model-based Verifiers in Mathematical Reasoning."** [arXiv](https://arxiv.org/abs/2505.22203)
Rule-based answer verifiers are precise and reject a share of correct responses, and model-based verifiers recover
those and are exploited during reinforcement learning. The paper measures a false-rejection rate for one kind of
grader and a growing false-acceptance rate for the other, the two quantities D9 prices.

<a id="deepseek2025"></a>
**DeepSeek-AI (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning."** [arXiv](https://arxiv.org/abs/2501.12948)
The reward is rule-based answer accuracy and format, and process reward models were set aside because steps are
hard to define, step correctness is hard to judge, and a learned reward invites exploitation. Obligations answer
the first objection and certificates the second and third, on the task families they decide.

<a id="natarajan2013"></a>
**Natarajan, Dhillon, Ravikumar and Tewari (2013), "Learning with Noisy Labels."** [NeurIPS](https://papers.nips.cc/paper_files/paper/2013/file/3871bd64012152bfb53fdf04b401193f-Paper.pdf)
An unbiased corrected loss for class-conditional label noise with known rates. With the prevalence correction of
[Rogan and Gladen (1978)](https://pubmed.ncbi.nlm.nih.gov/623091/) it supplies equation (5.4). Both treat a grader
that is observed. Section 5 treats the grader that is the reward.

### Variants and evidence

<a id="mirzadeh2024"></a>
**Mirzadeh et al. (2024), "GSM-Symbolic."** [arXiv](https://arxiv.org/abs/2410.05229)
Symbolic templates with stated variable domains show large variance across instantiations. Templates fix domains
and answer formulas. Section 4 adds the rule for what a transformation does to the acceptance tolerance, and the
order-dependence of a chain.

<a id="miller2024"></a>
**Miller (2024), "Adding Error Bars to Evals."** [arXiv](https://arxiv.org/abs/2411.00640)
Clustered standard errors for grouped evaluation questions. The correction addresses sampling variance. The
structural gap between score and validity in equation (1.1) is unaffected by it, and the two corrections are applied
together.

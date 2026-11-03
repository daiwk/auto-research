# Initial A100 component run: failure record

<!-- source-sha256: 9d991a72409c80bdc08b06499e1f64a679a54572cec747dd473a677c25ad0bbc -->

[简体中文](../../../../post-training/2610.21601-waypoint-opd/validation/a100-initial-failure.md)

- Device: real NVIDIA A100. This is not a passing GPU receipt.
- Code checkpoint: `a6ac6598`.
- Observed error: `RuntimeError: waypoint-opd has no actual policy gradient` (the previous runner's nonzero-gradient assertion in `run_seed`).
- This run did not produce acceptable evidence of passing all six post-training checks. The batch runner retains the original logs; the fix does not overwrite them.
- The first failure did not record the seed, step, or gate values. The exception alone does not establish that all gates were zero.

## Cause analysis and limits

The old tiny teacher computed reward from the parity of the first sampled byte but multiplied it by length-averaged log probability across the entire continuation. Besides rescaling by length, this introduced Monte Carlo noise from actions unrelated to reward. With only 4 samples per update and two independent updates, early and late shifts had weak directional consistency. The earlier CPU gate means were on the order of 0.005, and student parameters changed on the order of $10^{-7}$. This explains the risk of losing a measurable policy gradient under a different device's sampling stream; it is not evidence that the paper's Waypoint gate is wrong.

The revised budget is fixed in advance: 8 teacher RL updates, 64 real single-action rollouts per update, REINFORCE aligned to the first-action reward, and snapshots always saved at 0/4/8. No selection by reward, gate, or student gradient and no retries. The original Waypoint component formula, gate thresholds, and nonzero student-gradient requirement are unchanged. The new configuration remains a byte-parity mechanism diagnostic, not a reproduction of text quality, math capability, or paper-scale training.

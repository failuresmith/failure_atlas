# [FM-004] Anthropomorphic Misinterpretation
**Pattern:** Control Flow & Logic

**The Failure**
Engineers treat an AI model's incorrect output as "deception" or "lying" rather than a statistical distribution error. This leads to incorrect mitigations—like trying to "punish" the model through prompting instead of fixing the underlying data or temperature.

**Mechanism**
"Intent Projection". Humans project agency onto non-agentic statistical systems. When a model "hallucinates" with high confidence, the observer collapses the distinct failure class of "Representation Error" into "Strategic Deception".

**Reproduction**
(Theoretical - No code reproduction currently exists for this behavioral pattern)

**Remediation**
Apply failure class disambiguation. Use internal probe vectors to distinguish between "distributional gaps" and "reasoning failures". Design evaluation pipelines that target specific mechanisms (like token-length bias) rather than narrative "intent".

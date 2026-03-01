# Talk Outline — Partisan Geometry in LLM Activation Space

## SLIDE 1: Title

## SLIDE 2: Three Fields, One Sentence Each
- Polarization: the measurement problem
- LLM simulation: representations, not text
- Mechanistic interpretability: per-head decomposition

## SLIDE 3: The Core Question
- Can activation geometry recover the pattern of partisan gaps?
- What we are NOT asking

## SLIDE 4: Survey-Side Measure
- Normalized partisan gap: a 0-to-1 scale
- Party classification: GSS 7-point scale
- Topic categories: 126 public issues, 73 private-life topics

## SLIDE 5: Activation-Side Measure
- Pre-projection concatenated head outputs at last token
- Per-head PCA reduction and Mahalanobis distance
- Bramson taxonomy: group divergence + group consensus

## SLIDE 6: Simulation Methods
- Politician simulation: 550 Congress members, three prompt conditions
- Demographic simulation: 5-trait and 83-trait profiles

## SLIDE 7: The Alignment Metric
- Pearson correlation of per-topic scores across all topics
- Relative ordering, not absolute magnitudes

## SLIDE 8: Main Result — Politician Simulation, Public Issues
- Scale matters: 70B+ models surpass r = 0.65
- Prompt framing matters more at small scale
- Uncensored fine-tuning beats doubling model size
- RLHF as an artificial social desirability norm

## SLIDE 9: Private-Life Topics
- Lower alignment overall, averaging r = 0.54
- Llama-3.1-8B exception: best score in entire study on private topics
- Instruct advantage larger on private topics than public

## SLIDE 10: Politician vs. Demographic Simulation
- Demographic correlations much weaker: best r = 0.31 (5-trait), r = 0.505 (83-trait)
- Elite knowledge encodes partisan structure more reliably than demographic inference
- Connection to top-down polarization theories

## SLIDE 11: Transition to Depth Analysis
- Does the layer of emergence tell us about the nature of the issue?

## SLIDE 12: Question Fundamentalness — Setup
- Structural centrality: which issues predict everything else?
- Five independent survey-side measures of centrality
- Connection to constraint in DiMaggio et al.
- LLM-side measure: same Mahalanobis score, new correlate

## SLIDE 13: Fundamentalness Results
- Deeper-layer polarization tracks structural centrality
- Stronger claim than the main correlation result
- Second-order structure learned from text alone

## SLIDE 14: Why This Matters for Polarization Research
- Baldassarri and Bearman's takeoff issues
- Emergent structural position, not intrinsic content
- Text ecosystem encodes decades of social interaction dynamics

## SLIDE 15: Contributions to the Polarization Literature
- New measurement modality: addresses Nemeth's three critiques
- RLHF finding: no precedent in polarization literature
- Fundamentalness: from replication to architecture

## SLIDE 16: Questions for This Group — LLM Social Simulation
- What exactly are we measuring?
- Does RLHF attenuation affect simulation validity?
- Can the politician-demographic gap be bridged?
- Generalizability beyond the US two-party case

## SLIDE 17: Summary
- Activation geometry mirrors the topology of partisan disagreement
- RLHF suppresses partisan structure more than scale restores it
- Deeper layers encode structurally central issues
- Elite knowledge outperforms demographic inference

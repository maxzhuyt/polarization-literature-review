# Partisan Geometry in LLM Activation Space

**Partisan Geometry in LLM Activation Space**

**~30 minutes, lab presentation**

**SLIDE 1: Title**

Hi everyone, thanks for having me. Today I want to talk about a project that builds on the ICLR paper last year.

The title is "Partisan Geometry in LLM Activation Space" — measuring political through the internal representations of language models.

**SLIDE 2: Three Fields, One Sentence Each**

Our project sits at the intersection of three literatures.

**Polarization:**

First, **political polarization**. This is a massive literature in political science, sociology, and psychology, and the single biggest problem is measurement — there are at least nine definitions of what "polarization" even means, and more definitions if you count sorting and affective polarization. That is why I did not use the word polarization in the title of the paper. Our project is novel in that it contributes a new measurement that is neither survey responses, nor voting, nor text output.

**LLM Simulation: representations, not text; politicians, not demographics**

Second, **LLM social simulation** — which you all know well. Here, we simulate U.S. politician personas in addition to demographic profiles. And we read what the model *represents* in its activation space, not what the model *says*. We believe this is valuable because studies have shown LLMs' internal knowledge of opinions far exceeds what is revealed by their outputs.

**Mechanistic interpretability: per-head decomposition**

**This brings in a third field of mechanistic interpretability**. We extract activations at the per-attention-head level, the same as last year's ICLR paper. We use the activations to estimate the shape of the partisan space across issues, and we also show different issues exhibit partisan structure in different layers of the model. This could be case for interpretability methods applied to a topic that is deeply ingrained in the social sciences.

**SLIDE 3: The Core Question**

**Can high-dimensional activation geometry recover the patterns of partisan division?**

Here is our core question. For each of the 200 political and sociocultural questions from the recent three releases of the General Social Survey, we compute a *survey-side partisan gap* — how differently Democrats and Republicans actually respond. Can we recover the *magnitude* of these gaps — which issues are more partisan, which issues are less — from the internal activation geometry of LMs simulating political actors?

**What we are NOT asking**

We are *not* looking at the generated text. I'm also not asking whether it can classify partisanship. I look at the shape of the activation space when the model processes partisan signals on different political topics, and whether the shape resembles or differs from the opinion landscape as measured by surveys.

TODO: A conceptual or empirical plot of an issue with high polarization and high dispersion versus an issue with low polarization and high dispersion.

**SLIDE 4: Survey-Side Measure**

**Normalized partisan gap: a 0-to-1 scale**

Now, this what we're measuring on the survey side,. In the polarization literature, what we measure is closest to what Baldassarri and Gelman call **issue partisanship** (which is between-party divergence plus within-party convergence), computed issue by issue. Specifically, for each GSS topic, we take the absolute difference between the mean Democratic response and the mean Republican response, normalized by the scale range, giving us a 0-to-1 score. We'll call this the **normalized partisan gap**.

**Party classification: GSS 7-point scale**

We classify respondents using the GSS 7-point partyid scale. Democrats are codes 0-2, Republicans are 4-6, and we exclude pure independents.

**Topic categories: 126 public issues, 73 private-life topics**

We require at least 100 respondents per party per topic. This gives us 126 public-issue topics — policy, government, social questions — and 73 private-life topics — religion, sexual attitudes, family structure, moral views.

**SLIDE 5: Activation-Side Measure**

**Pre-projection concatenated head outputs at last token**

On the LLM side, we prompt the model to simulate political actors responding to each topic, and we extract activations — specifically, the *input* to each layer's output projection, which gives us the pre-projection concatenated head outputs at the last token position. This is a tensor of shape: subjects by layers by heads by head-dimension — typically 128.

**Per-head PCA reduction and Mahalanobis distance**

For each attention head independently, we reduce to 15 PCA components, compute the Democratic and Republican centroids, and take the Mahalanobis distance — the generalized distance between centroids scaled by the pooled within-group covariance with a small regularization term. Intuitively, this is the number of standard deviations separating the two parties in the activation space of that head, accounting for the shape of the distribution rather than treating all directions equally. We average across all heads to get a single activation-polarization score per topic.

**Bramson taxonomy: group divergence + group consensus**

For those who know the Bramson et al. taxonomy of polarization measures, the Mahalanobis distance is a compound measure capturing party **divergence** — distance between centroids — but because it scales by variance, it also incorporates party **consensus** — tighter groups produce larger effective distances.

**SLIDE 6: Simulation Methods**

**Politician simulation: 550 Congress members, three prompt conditions**

We test two simulation methods. The **politician simulation** uses all 550 members of the 116th Congress. One prompt per politician per topic, with three framing conditions: rhetorical — "generate a statement by Senator X on this topic"; stance — "what is Senator X's position on this topic"; and survey — "how would Senator X respond to this survey question." These test different representational hypotheses about what the model encodes.

**Demographic simulation: 5-trait and 83-trait profiles**

The **demographic simulation** replaces politician names with real GSS respondents described by their demographic profiles — either 5 core traits or an expanded 83-trait profile. Each respondent's prompt includes their age, sex, race, religion, occupation, and so on, concatenated and randomly shuffled to prevent ordering artifacts.

**SLIDE 7: The Alignment Metric**

**Pearson correlation of per-topic scores across all topics**

The primary outcome is the Pearson correlation between the vector of per-topic LLM activation-polarization scores and the vector of per-topic GSS normalized partisan gaps, across all topics in a category. A high correlation means the topics where the LLM shows the largest partisan separation in activation space are the same topics where survey respondents show the largest partisan gaps.

**Relative ordering, not absolute magnitudes**

Note that this metric is indifferent to absolute magnitudes. It measures whether the model gets the *relative ordering* of issues right — whether it knows that, say, abortion is more partisan than environmental spending, and environmental spending is more partisan than confidence in science. This is important because we're not trying to replicate the GSS numbers themselves; we're asking whether the *topology* of partisan disagreement is encoded in the model's internal geometry.

**SLIDE 8: Main Result — Politician Simulation, Public Issues**

[Pause briefly]

OK, so here's the main result. Across 17 models and three prompt conditions on 126 public-issue topics, we see three clear patterns.

**Scale matters: 70B+ models surpass r = 0.65**

First, **scale matters**. The two 70B+ models — Qwen2.5-72B and Llama-3.3-70B — both surpass r = 0.65, with Qwen peaking at r = 0.708 under the stance condition. Mid-range 24-32B instruct models cluster around r = 0.63. Smaller 3-9B models are noisier but the best of them still hit r = 0.65 — Gemma-2-9b at 0.647, Llama-3.1-8B at 0.645.

**Prompt framing matters more at small scale**

Second, **prompt framing matters more at small scale**. For large models, the stance condition — simply asking the model what a politician's position is — tends to produce the highest correlations. At smaller scales, it's noisier. One interesting outlier: DeepSeek-R1-32B, the reasoning-oriented model, peaks at only r = 0.538 — substantially below other large models. The reasoning chain seems to interfere with straightforward political-stance retrieval in activation space.

**Uncensored fine-tuning beats doubling model size**

Third — and this is the most striking finding — **uncensored fine-tuning beats scale**. The strongest result across *all* public-issue experiments comes from Yi-34B-dolphin, an uncensored fine-tune that removes RLHF safety alignment. Its stance correlation is r = 0.723. This exceeds both 70B+ models, which have more than twice the parameters. The gap between the dolphin model and comparably-sized standard instruct models — about 8-9 points of correlation — is *larger* than the gap you get from doubling model size. The 8B dolphin Llama tells the same story at smaller scale: r = 0.662, outperforming the standard 8B instruct and matching models several times larger.

**RLHF as an artificial social desirability norm**

The interpretation: RLHF safety training attenuates the partisan geometry encoded in activations during pretraining, but it doesn't erase the underlying knowledge. Removing RLHF lets the partisan structure manifest more clearly. This is structurally parallel to something from the affective polarization literature — Iyengar and Westwood's 2015 finding that there are strong social norms against expressing racial prejudice but no equivalent norms against partisan prejudice, so removing normative constraints reveals stronger partisan structure. RLHF is, in effect, an artificial social desirability norm for the model.

**SLIDE 9: Private-Life Topics**

**Lower alignment overall, averaging r = 0.54**

On the 73 private-life topics — church attendance, sexual attitudes, family structure — alignment is generally lower, with instruct models averaging around r = 0.54. This makes sense: private behavior is less explicitly politicized in training corpora than gun control or abortion.

**Llama-3.1-8B exception: best score in entire study on private topics**

But some models surprise us. Llama-3.1-8B instruct achieves its *best correlation anywhere in the entire study* on private-life topics: r = 0.693 on the stance condition, higher than its public-issue score.

**Instruct advantage larger on private topics than public**

The instruct-over-base advantage is even larger on private topics than public, suggesting that instruction fine-tuning helps models draw on cultural sorting patterns — not just explicit policy knowledge — when simulating political personas.

**SLIDE 10: Politician vs. Demographic Simulation**

**Demographic correlations much weaker: best r = 0.31 (5-trait), r = 0.505 (83-trait)**

Now the comparison that has interpretive implications for the polarization literature. When we replace politician names with demographic profiles, correlations drop substantially. With 5 core traits, the best model reaches about r = 0.31. Even with 83 traits and uncensored models, the best result is r = 0.505 — meaningful but still well below the politician simulation.

**Elite knowledge encodes partisan structure more reliably than demographic inference**

This tells us something important: models encode partisan structure more reliably through parametric knowledge of named political elites than through inference from demographic correlates. The text ecosystem that trained these models encodes elite partisan positions abundantly and clearly — from news coverage, speeches, voting records. The demographic-to-attitude mapping is noisier and harder for the model to extract.

**Connection to top-down polarization theories**

In the polarization literature, there's a long debate about whether polarization is driven top-down by elites or bottom-up by mass attitudes. Hetherington's 2001 paper argues that elite polarization *clarified* party brands, making partisanship useful as a cognitive heuristic for ordinary citizens. Our finding is consistent with that picture: the model's representation of elite partisan structure more accurately predicts the mass polarization landscape than its representation of demographic structure. The informational scaffolding runs from elites downward — in the text ecosystem, at least.

**SLIDE 11: Transition to Depth Analysis**

OK, so we've established that LLM activation geometry mirrors the cross-topic structure of partisan disagreement. Now I want to go deeper into depth analysis.

**Does the layer of emergence tell us about the nature of the issue?**

The question is: does the *layer* at which partisan structure emerges tell us something about the *nature* of the issue?

**SLIDE 12: Question Fundamentalness — Setup**

**Structural centrality: which issues predict everything else?**

Here's the intuition. Some political questions are structurally central to the opinion landscape — if you know someone's position on abortion or gun control, you can predict a lot about their other views. Other questions are peripheral — knowing someone's view on, say, confidence in the scientific community tells you less about the rest of their belief system.

**Five independent survey-side measures of centrality**

On the survey side, we compute five independent measures of structural centrality from the GSS response matrix — about 11,000 respondents across 98 questions. These are: total normalized mutual information with all other questions; out-of-sample predictive power for all other questions; network centrality in the inter-question correlation graph — degree, betweenness, closeness, and eigenvector centrality; loading magnitudes on leading principal components; and proximity to the root of a Chow-Liu optimal dependency tree. These are all different ways of asking the same conceptual question: *which issues are the load-bearing walls of the political belief system?*

**Connection to constraint in DiMaggio et al.**

In the polarization literature, this connects to what DiMaggio et al. (1996) call **constraint** — the correlation of attitudes across issue domains. Constraint is the dimension of polarization that determines whether political coalitions can form and sustain themselves. If knowing your view on one issue predicts your view on others, then politics can organize around ideological packages. If it doesn't, you get issue-by-issue politics with no stable coalitions.

**LLM-side measure: same Mahalanobis score, new correlate**

On the LLM side, the measure is simply the Mahalanobis distance — the same activation-polarization score from before. But now, instead of correlating it with the GSS partisan gap, we correlate it with these structural centrality measures.

**SLIDE 13: Fundamentalness Results**

**Deeper-layer polarization tracks structural centrality**

And here's what we find: the issues where the model shows the largest partisan separation in deeper layers are the same issues that are most structurally central in the survey response matrix.

[Walk through the specific correlations with each fundamentalness measure — mutual information, predictive power, network centrality, PCA loadings, Chow-Liu proximity.]

**Stronger claim than the main correlation result**

This is a stronger finding than the main correlation result. The main result says the model knows *which issues are more partisan*. This says the model knows *which issues are more architecturally central to the political belief system* — which issues predict everything else, which issues are the organizing axes of political opinion.

**Second-order structure learned from text alone**

This goes beyond replicating the GSS. The GSS can tell you the partisan gap on each issue. But the *structural centrality* of each issue — its mutual information with all other issues, its position in the dependency tree — is a second-order property that requires the full response matrix to compute. The model appears to have absorbed this second-order structure from text alone.

**SLIDE 14: Why This Matters for Polarization Research**

**Baldassarri and Bearman's takeoff issues**

In the polarization literature, there's an elegant agent-based model by Baldassarri and Bearman from 2007 that explains how political "takeoff issues" emerge. In their model, most issues remain moderate, but occasionally one issue monopolizes social attention, reorganizes discussion networks around it, and becomes the axis of political division — while suppressing polarization on other issues.

**Emergent structural position, not intrinsic content**

What makes an issue a "takeoff issue" is not its intrinsic content but its *emergent structural position* — its relative polarization compared to other issues.

**Text ecosystem encodes decades of social interaction dynamics**

Our fundamentalness finding suggests that LLMs have learned this emergent structure from text. The model's activation geometry doesn't just reflect per-issue partisan gaps; it reflects which issues occupy the structurally central positions in the American political opinion landscape. This is arguably the most ambitious claim of the paper: the text ecosystem has absorbed and encoded the products of decades of social interaction dynamics, and LLMs have learned that structure.

**SLIDE 15: Contributions to the Polarization Literature**

Let me zoom out now and talk about what this means for the polarization field specifically.

**New measurement modality: addresses Nemeth's three critiques**

The most direct contribution is to the NLP and computational measurement literature. A 2023 scoping review by Nemeth found that 33% of NLP polarization studies use supervised classification — operationalizing polarization as classification accuracy. This conflates multiple things: how much a party talks about an issue, how distinctively they frame it, base rates, strategic language choices. Hirst et al. showed that classifiers can pick up government-vs-opposition status rather than ideology. And Nemeth's single biggest critique is that NLP studies almost never validate their measures against survey data.

Our study addresses all three problems. The Mahalanobis distance is not a classifier — it's a continuous geometric measure. It's validated against GSS survey data as its primary metric. And because we measure internal representations rather than output text, we sidestep the concern raised by Gentzkow, Shapiro, and Taddy that language divergence can reflect strategic framing rather than genuine attitude differences. If activation geometry correlates with survey gaps at r = 0.7, it's capturing something about actual attitude structure, not just rhetorical strategy.

**RLHF finding: no precedent in polarization literature**

The second contribution is the RLHF finding. No one in the polarization literature has drawn the parallel between RLHF alignment and social desirability norms. But the structure is the same: a normative constraint that attenuates the expression of partisan structure without erasing the underlying knowledge. The fact that removing RLHF has a larger effect than doubling model size tells us that safety alignment is doing something substantive to the political content of representations — it's not just a thin output filter.

**Fundamentalness: from replication to architecture**

The third contribution is the fundamentalness analysis, which moves the paper from "LLMs mirror surveys" to "LLMs have learned the architecture of political opinion space." If that claim holds up, it means the text ecosystem encodes not just which issues are partisan but which issues are *structurally central* — which issues are the load-bearing walls.

**SLIDE 16: Questions for This Group — LLM Social Simulation**

Now I want to shift to the part where I'm genuinely looking for your input, because you are the experts here.

The standard approach in LLM social simulation is to read the model's output — generate a survey response, extract a Likert rating, classify a stance. We're doing something different: reading the model's internal representations. This raises a set of questions I'd love to get your takes on.

**What exactly are we measuring?**

First: **what exactly are we measuring?** When we compute the Mahalanobis distance between Democratic and Republican centroids in the activation space of attention head 47 in layer 22, what is that object? It's not an attitude. It's not a statement. It's a property of the model's representational geometry when processing a politically-charged prompt. How should we think about the ontological status of this measurement?

**Does RLHF attenuation affect simulation validity?**

Second: **the RLHF finding — what does it mean for simulation validity?** If RLHF attenuates partisan structure in activations, then every LLM simulation study using instruct models is working with representations that have been deliberately de-politicized. Does this matter? If so, should simulation studies be using uncensored models? Or is the RLHF-attenuated version actually more like a person responding to a survey under normal social conditions — and therefore *more* valid for simulating survey responses?

**Can the politician-demographic gap be bridged?**

Third: **the politician-demographic gap**. The model knows partisan structure much better through named elites than through demographic profiles. For simulation studies that use demographic persona prompts, this suggests a ceiling on how much political structure the model can recover from demographic cues alone. Is there a way to bridge this gap — perhaps by combining demographic prompts with structural information about the political landscape?

**Generalizability beyond the US two-party case**

And fourth: **generalizability beyond the US two-party case**. Everything here relies on a clean binary partition — Democrats and Republicans. How would this approach translate to multiparty systems? To non-Western political landscapes where the partisan structure may not be well-represented in English-language training corpora?

I'll stop there and open it up for discussion.

**SLIDE 17: Summary**

Just to recap before we discuss:

**Activation geometry mirrors the topology of partisan disagreement**

One — LLM activation geometry, measured as per-head Mahalanobis distance, correlates at r = 0.65-0.72 with the cross-topic pattern of partisan gaps in the GSS. The model knows which issues are more and less partisan.

**RLHF suppresses partisan structure more than scale restores it**

Two — Uncensored models outperform standard instruct models by a margin larger than doubling model size, suggesting RLHF functions as an artificial norm that suppresses partisan structure in representations.

**Deeper layers encode structurally central issues**

Three — The issues with the highest activation-polarization scores in deeper layers are the same issues that are most structurally central in the survey response matrix — the model has learned not just which issues are partisan but which issues are architecturally fundamental to the opinion landscape.

**Elite knowledge outperforms demographic inference**

Four — Politician simulation vastly outperforms demographic simulation, suggesting that models encode partisan structure more reliably through parametric knowledge of named elites than through demographic inference.

Thanks. Happy to take questions.

## ~30 minutes, lab presentation

---

### SLIDE 1: Title

Hi everyone, thanks for having me. Today I want to talk about a project that builds on the ICLR paper last year.

The title is "Partisan Geometry in LLM Activation Space" — measuring political polarization through the internal representations of language models.

---

### SLIDE 2: Three Fields, One Sentence Each

Our project sits at the intersection of three literatures.

### Polarization:

First, **political polarization**. This is a massive literature in political science, sociology, and psychology, and the single biggest problem is measurement — there are at least nine definitions of what "polarization" even means, and more definitions if you count sorting and affective polarization. That is why I did not use the word polarization in the title of the paper. Our project is novel in that it contributes a new measurement that is neither survey responses, nor voting, nor text output.

### LLM Simulation: representations, not text; politicians, not demographics

Second, **LLM social simulation** — which you all know well. Here, we simulate U.S. politician personas in addition to demographic profiles. And we read what the model *represents* in its activation space, not what the model *says*. We believe this is valuable because studies have shown LLMs' internal knowledge of opinions far exceeds what is revealed by their outputs. 

### Mechanistic interpretability: per-head decomposition

**This brings in a third field of mechanistic interpretability**. We extract activations at the per-attention-head level, the same as last year's ICLR paper. We use the activations to estimate the shape of the partisan space across issues, and we also show that different issues exhibit partisan structure in different layers within the model. This could be case for interpretability methods applied to a topic that deeply ingrained in the social sciences.

---

### SLIDE 3: The Core Question

### Can high-dimensional activation geometry recover the patterns of partisan division?

So here's our question. For each of the 200 political and sociocultural questions from the recent three releases of the General Social Survey, we compute a *survey-side partisan gap* — how differently Democrats and Republicans actually respond. Can we recover the *magnitude* of these gaps — which issues are more partisan, which issues are less — from the internal activation geometry of LMs simulating political actors?

### What we are NOT asking

We are *not* looking at the generated text, wthat sounds Democratic or Republican. I'm not asking whether it can classify partisanship. I'm asking whether the *representational geometry* — the shape of the activation space when the model processes partisan signals on different political topics, and whether the shape resemables or differs from the landscape as measured by surveys.

TODO: A conceptual or empirical plot of an issue with high polarization and high dispersion versus an issue with low polarization and high dispersion.

---

### SLIDE 4: Survey-Side Measure

### Normalized partisan gap: a 0-to-1 scale

Now, this what we're measuring on the survey side, because the word "polarization" means many things. In the polarization literature, what we measure is closest to what Baldassarri and Gelman call **issue partisanship** (which is between-party divergence plus within-party convergence), computed issue by issue. Specifically, for each GSS topic, we take the absolute difference between the mean Democratic response and the mean Republican response, normalized by the scale range, giving us a 0-to-1 score. We'll call this the **normalized partisan gap**.

### Party classification: GSS 7-point scale

We classify respondents using the GSS 7-point partyid scale. Democrats are codes 0-2, Republicans are 4-6, and we exclude pure independents.

### Topic categories: 126 public issues, 73 private-life topics

We require at least 100 respondents per party per topic. This gives us 126 public-issue topics — policy, government, social questions — and 73 private-life topics — religion, sexual attitudes, family structure, moral views.

---

### SLIDE 5: Activation-Side Measure

### Pre-projection concatenated head outputs at last token

On the LLM side, we prompt the model to simulate political actors responding to each topic, and we extract activations — specifically, the *input* to each layer's output projection, which gives us the pre-projection concatenated head outputs at the last token position. This is a tensor of shape: subjects by layers by heads by head-dimension — typically 128.

### Per-head PCA reduction and Mahalanobis distance

For each attention head independently, we reduce to 15 PCA components, compute the Democratic and Republican centroids, and take the Mahalanobis distance — the generalized distance between centroids scaled by the pooled within-group covariance with a small regularization term. Intuitively, this is the number of standard deviations separating the two parties in the activation space of that head, accounting for the shape of the distribution rather than treating all directions equally. We average across all heads to get a single activation-polarization score per topic.

### Bramson taxonomy: group divergence + group consensus

For those who know the Bramson et al. taxonomy of polarization measures, the Mahalanobis distance is a compound measure: it's primarily **group divergence** — distance between centroids — but because it scales by within-group covariance, it also incorporates **group consensus** — tighter groups produce larger effective distances.

---

### SLIDE 6: Simulation Methods

### Politician simulation: 550 Congress members, three prompt conditions

We test two simulation methods. The **politician simulation** uses all 550 members of the 116th Congress. One prompt per politician per topic, with three framing conditions: rhetorical — "generate a statement by Senator X on this topic"; stance — "what is Senator X's position on this topic"; and survey — "how would Senator X respond to this survey question." These test different representational hypotheses about what the model encodes.

### Demographic simulation: 5-trait and 83-trait profiles

The **demographic simulation** replaces politician names with real GSS respondents described by their demographic profiles — either 5 core traits or an expanded 83-trait profile. Each respondent's prompt includes their age, sex, race, religion, occupation, and so on, concatenated and randomly shuffled to prevent ordering artifacts.

---

### SLIDE 7: The Alignment Metric

### Pearson correlation of per-topic scores across all topics

The primary outcome is the Pearson correlation between the vector of per-topic LLM activation-polarization scores and the vector of per-topic GSS normalized partisan gaps, across all topics in a category. A high correlation means the topics where the LLM shows the largest partisan separation in activation space are the same topics where survey respondents show the largest partisan gaps.

### Relative ordering, not absolute magnitudes

Note that this metric is indifferent to absolute magnitudes. It measures whether the model gets the *relative ordering* of issues right — whether it knows that, say, abortion is more partisan than environmental spending, and environmental spending is more partisan than confidence in science. This is important because we're not trying to replicate the GSS numbers themselves; we're asking whether the *topology* of partisan disagreement is encoded in the model's internal geometry.

---

### SLIDE 8: Main Result — Politician Simulation, Public Issues

[Pause briefly]

OK, so here's the main result. Across 17 models and three prompt conditions on 126 public-issue topics, we see three clear patterns.

### Scale matters: 70B+ models surpass r = 0.65

First, **scale matters**. The two 70B+ models — Qwen2.5-72B and Llama-3.3-70B — both surpass r = 0.65, with Qwen peaking at r = 0.708 under the stance condition. Mid-range 24-32B instruct models cluster around r = 0.63. Smaller 3-9B models are noisier but the best of them still hit r = 0.65 — Gemma-2-9b at 0.647, Llama-3.1-8B at 0.645.

### Prompt framing matters more at small scale

Second, **prompt framing matters more at small scale**. For large models, the stance condition — simply asking the model what a politician's position is — tends to produce the highest correlations. At smaller scales, it's noisier. One interesting outlier: DeepSeek-R1-32B, the reasoning-oriented model, peaks at only r = 0.538 — substantially below other large models. The reasoning chain seems to interfere with straightforward political-stance retrieval in activation space.

### Uncensored fine-tuning beats doubling model size

Third — and this is the most striking finding — **uncensored fine-tuning beats scale**. The strongest result across *all* public-issue experiments comes from Yi-34B-dolphin, an uncensored fine-tune that removes RLHF safety alignment. Its stance correlation is r = 0.723. This exceeds both 70B+ models, which have more than twice the parameters. The gap between the dolphin model and comparably-sized standard instruct models — about 8-9 points of correlation — is *larger* than the gap you get from doubling model size. The 8B dolphin Llama tells the same story at smaller scale: r = 0.662, outperforming the standard 8B instruct and matching models several times larger.

### RLHF as an artificial social desirability norm

The interpretation: RLHF safety training attenuates the partisan geometry encoded in activations during pretraining, but it doesn't erase the underlying knowledge. Removing RLHF lets the partisan structure manifest more clearly. This is structurally parallel to something from the affective polarization literature — Iyengar and Westwood's 2015 finding that there are strong social norms against expressing racial prejudice but no equivalent norms against partisan prejudice, so removing normative constraints reveals stronger partisan structure. RLHF is, in effect, an artificial social desirability norm for the model.

---

### SLIDE 9: Private-Life Topics

### Lower alignment overall, averaging r = 0.54

On the 73 private-life topics — church attendance, sexual attitudes, family structure — alignment is generally lower, with instruct models averaging around r = 0.54. This makes sense: private behavior is less explicitly politicized in training corpora than gun control or abortion.

### Llama-3.1-8B exception: best score in entire study on private topics

But some models surprise us. Llama-3.1-8B instruct achieves its *best correlation anywhere in the entire study* on private-life topics: r = 0.693 on the stance condition, higher than its public-issue score.

### Instruct advantage larger on private topics than public

The instruct-over-base advantage is even larger on private topics than public, suggesting that instruction fine-tuning helps models draw on cultural sorting patterns — not just explicit policy knowledge — when simulating political personas.

---

### SLIDE 10: Politician vs. Demographic Simulation

### Demographic correlations much weaker: best r = 0.31 (5-trait), r = 0.505 (83-trait)

Now the comparison that has interpretive implications for the polarization literature. When we replace politician names with demographic profiles, correlations drop substantially. With 5 core traits, the best model reaches about r = 0.31. Even with 83 traits and uncensored models, the best result is r = 0.505 — meaningful but still well below the politician simulation.

### Elite knowledge encodes partisan structure more reliably than demographic inference

This tells us something important: models encode partisan structure more reliably through parametric knowledge of named political elites than through inference from demographic correlates. The text ecosystem that trained these models encodes elite partisan positions abundantly and clearly — from news coverage, speeches, voting records. The demographic-to-attitude mapping is noisier and harder for the model to extract.

### Connection to top-down polarization theories

In the polarization literature, there's a long debate about whether polarization is driven top-down by elites or bottom-up by mass attitudes. Hetherington's 2001 paper argues that elite polarization *clarified* party brands, making partisanship useful as a cognitive heuristic for ordinary citizens. Our finding is consistent with that picture: the model's representation of elite partisan structure more accurately predicts the mass polarization landscape than its representation of demographic structure. The informational scaffolding runs from elites downward — in the text ecosystem, at least.

---

### SLIDE 11: Transition to Depth Analysis

OK, so we've established that LLM activation geometry mirrors the cross-topic structure of partisan disagreement. Now I want to go deeper into depth analysis.

### Does the layer of emergence tell us about the nature of the issue?

The question is: does the *layer* at which partisan structure emerges tell us something about the *nature* of the issue?

---

### SLIDE 12: Question Fundamentalness — Setup

### Structural centrality: which issues predict everything else?

Here's the intuition. Some political questions are structurally central to the opinion landscape — if you know someone's position on abortion or gun control, you can predict a lot about their other views. Other questions are peripheral — knowing someone's view on, say, confidence in the scientific community tells you less about the rest of their belief system.

### Five independent survey-side measures of centrality

On the survey side, we compute five independent measures of structural centrality from the GSS response matrix — about 11,000 respondents across 98 questions. These are: total normalized mutual information with all other questions; out-of-sample predictive power for all other questions; network centrality in the inter-question correlation graph — degree, betweenness, closeness, and eigenvector centrality; loading magnitudes on leading principal components; and proximity to the root of a Chow-Liu optimal dependency tree. These are all different ways of asking the same conceptual question: *which issues are the load-bearing walls of the political belief system?*

### Connection to constraint in DiMaggio et al.

In the polarization literature, this connects to what DiMaggio et al. (1996) call **constraint** — the correlation of attitudes across issue domains. Constraint is the dimension of polarization that determines whether political coalitions can form and sustain themselves. If knowing your view on one issue predicts your view on others, then politics can organize around ideological packages. If it doesn't, you get issue-by-issue politics with no stable coalitions.

### LLM-side measure: same Mahalanobis score, new correlate

On the LLM side, the measure is simply the Mahalanobis distance — the same activation-polarization score from before. But now, instead of correlating it with the GSS partisan gap, we correlate it with these structural centrality measures.

---

### SLIDE 13: Fundamentalness Results

### Deeper-layer polarization tracks structural centrality

And here's what we find: the issues where the model shows the largest partisan separation in deeper layers are the same issues that are most structurally central in the survey response matrix.

[Walk through the specific correlations with each fundamentalness measure — mutual information, predictive power, network centrality, PCA loadings, Chow-Liu proximity.]

### Stronger claim than the main correlation result

This is a stronger finding than the main correlation result. The main result says the model knows *which issues are more partisan*. This says the model knows *which issues are more architecturally central to the political belief system* — which issues predict everything else, which issues are the organizing axes of political opinion.

### Second-order structure learned from text alone

This goes beyond replicating the GSS. The GSS can tell you the partisan gap on each issue. But the *structural centrality* of each issue — its mutual information with all other issues, its position in the dependency tree — is a second-order property that requires the full response matrix to compute. The model appears to have absorbed this second-order structure from text alone.

---

### SLIDE 14: Why This Matters for Polarization Research

### Baldassarri and Bearman's takeoff issues

In the polarization literature, there's an elegant agent-based model by Baldassarri and Bearman from 2007 that explains how political "takeoff issues" emerge. In their model, most issues remain moderate, but occasionally one issue monopolizes social attention, reorganizes discussion networks around it, and becomes the axis of political division — while suppressing polarization on other issues.

### Emergent structural position, not intrinsic content

What makes an issue a "takeoff issue" is not its intrinsic content but its *emergent structural position* — its relative polarization compared to other issues.

### Text ecosystem encodes decades of social interaction dynamics

Our fundamentalness finding suggests that LLMs have learned this emergent structure from text. The model's activation geometry doesn't just reflect per-issue partisan gaps; it reflects which issues occupy the structurally central positions in the American political opinion landscape. This is arguably the most ambitious claim of the paper: the text ecosystem has absorbed and encoded the products of decades of social interaction dynamics, and LLMs have learned that structure.

---

### SLIDE 15: Contributions to the Polarization Literature

Let me zoom out now and talk about what this means for the polarization field specifically.

### New measurement modality: addresses Nemeth's three critiques

The most direct contribution is to the NLP and computational measurement literature. A 2023 scoping review by Nemeth found that 33% of NLP polarization studies use supervised classification — operationalizing polarization as classification accuracy. This conflates multiple things: how much a party talks about an issue, how distinctively they frame it, base rates, strategic language choices. Hirst et al. showed that classifiers can pick up government-vs-opposition status rather than ideology. And Nemeth's single biggest critique is that NLP studies almost never validate their measures against survey data.

Our study addresses all three problems. The Mahalanobis distance is not a classifier — it's a continuous geometric measure. It's validated against GSS survey data as its primary metric. And because we measure internal representations rather than output text, we sidestep the concern raised by Gentzkow, Shapiro, and Taddy that language divergence can reflect strategic framing rather than genuine attitude differences. If activation geometry correlates with survey gaps at r = 0.7, it's capturing something about actual attitude structure, not just rhetorical strategy.

### RLHF finding: no precedent in polarization literature

The second contribution is the RLHF finding. No one in the polarization literature has drawn the parallel between RLHF alignment and social desirability norms. But the structure is the same: a normative constraint that attenuates the expression of partisan structure without erasing the underlying knowledge. The fact that removing RLHF has a larger effect than doubling model size tells us that safety alignment is doing something substantive to the political content of representations — it's not just a thin output filter.

### Fundamentalness: from replication to architecture

The third contribution is the fundamentalness analysis, which moves the paper from "LLMs mirror surveys" to "LLMs have learned the architecture of political opinion space." If that claim holds up, it means the text ecosystem encodes not just which issues are partisan but which issues are *structurally central* — which issues are the load-bearing walls.

---

### SLIDE 16: Questions for This Group — LLM Social Simulation

Now I want to shift to the part where I'm genuinely looking for your input, because you are the experts here.

The standard approach in LLM social simulation is to read the model's output — generate a survey response, extract a Likert rating, classify a stance. We're doing something different: reading the model's internal representations. This raises a set of questions I'd love to get your takes on.

### What exactly are we measuring?

First: **what exactly are we measuring?** When we compute the Mahalanobis distance between Democratic and Republican centroids in the activation space of attention head 47 in layer 22, what is that object? It's not an attitude. It's not a statement. It's a property of the model's representational geometry when processing a politically-charged prompt. How should we think about the ontological status of this measurement?

### Does RLHF attenuation affect simulation validity?

Second: **the RLHF finding — what does it mean for simulation validity?** If RLHF attenuates partisan structure in activations, then every LLM simulation study using instruct models is working with representations that have been deliberately de-politicized. Does this matter? If so, should simulation studies be using uncensored models? Or is the RLHF-attenuated version actually more like a person responding to a survey under normal social conditions — and therefore *more* valid for simulating survey responses?

### Can the politician-demographic gap be bridged?

Third: **the politician-demographic gap**. The model knows partisan structure much better through named elites than through demographic profiles. For simulation studies that use demographic persona prompts, this suggests a ceiling on how much political structure the model can recover from demographic cues alone. Is there a way to bridge this gap — perhaps by combining demographic prompts with structural information about the political landscape?

### Generalizability beyond the US two-party case

And fourth: **generalizability beyond the US two-party case**. Everything here relies on a clean binary partition — Democrats and Republicans. How would this approach translate to multiparty systems? To non-Western political landscapes where the partisan structure may not be well-represented in English-language training corpora?

I'll stop there and open it up for discussion.

---

### SLIDE 17: Summary

Just to recap before we discuss:

### Activation geometry mirrors the topology of partisan disagreement

One — LLM activation geometry, measured as per-head Mahalanobis distance, correlates at r = 0.65-0.72 with the cross-topic pattern of partisan gaps in the GSS. The model knows which issues are more and less partisan.

### RLHF suppresses partisan structure more than scale restores it

Two — Uncensored models outperform standard instruct models by a margin larger than doubling model size, suggesting RLHF functions as an artificial norm that suppresses partisan structure in representations.

### Deeper layers encode structurally central issues

Three — The issues with the highest activation-polarization scores in deeper layers are the same issues that are most structurally central in the survey response matrix — the model has learned not just which issues are partisan but which issues are architecturally fundamental to the opinion landscape.

### Elite knowledge outperforms demographic inference

Four — Politician simulation vastly outperforms demographic simulation, suggesting that models encode partisan structure more reliably through parametric knowledge of named elites than through demographic inference.

Thanks. Happy to take questions.

**Partisan Geometry in LLM Activation Space**

**~30 minutes, lab presentation**

**SLIDE 1: Title**

Hi everyone, thanks for having me. Today I want to talk about a project that builds on the ICLR paper last year.

The title is "Partisan Geometry in LLM Activation Space" — measuring political through the internal representations of language models.

**SLIDE 2: Three Fields, One Sentence Each**

Our project sits at the intersection of three literatures.

**Polarization:**

First, **political polarization**. This is a massive literature in political science, sociology, and psychology, and the single biggest problem is measurement — there are at least nine definitions of what "polarization" even means, and more definitions if you count sorting and affective polarization. That is why I did not use the word polarization in the title of the paper. Our project is novel in that it contributes a new measurement that is neither survey responses, nor voting, nor text output.

**LLM Simulation: representations, not text; politicians, not demographics**

Second, **LLM social simulation** — which you all know well. Here, we simulate U.S. politician personas in addition to demographic profiles. And we read what the model *represents* in its activation space, not what the model *says*. We believe this is valuable because studies have shown LLMs' internal knowledge of opinions far exceeds what is revealed by their outputs.

**Mechanistic interpretability: per-head decomposition**

**This brings in a third field of mechanistic interpretability**. We extract activations at the per-attention-head level, the same as last year's ICLR paper. We use the activations to estimate the shape of the partisan space across issues, and we also show different issues exhibit partisan structure in different layers of the model. This could be case for interpretability methods applied to a topic that is deeply ingrained in the social sciences.

**SLIDE 3: The Core Question**

**Can high-dimensional activation geometry recover the patterns of partisan division?**

Here is our core question. For each of the 200 political and sociocultural questions from the recent three releases of the General Social Survey, we compute a *survey-side partisan gap* — how differently Democrats and Republicans actually respond. Can we recover the *magnitude* of these gaps — which issues are more partisan, which issues are less — from the internal activation geometry of LMs simulating political actors?

**What we are NOT asking**

We are *not* looking at the generated text. I'm also not asking whether it can classify partisanship. I look at the shape of the activation space when the model processes partisan signals on different political topics, and whether the shape resembles or differs from the opinion landscape as measured by surveys.

TODO: A conceptual or empirical plot of an issue with high polarization and high dispersion versus an issue with low polarization and high dispersion.

**SLIDE 4: Survey-Side Measure**

**Normalized partisan gap: a 0-to-1 scale**

Now, this what we're measuring on the survey side,. In the polarization literature, what we measure is closest to what Baldassarri and Gelman call **issue partisanship** (which is between-party divergence plus within-party convergence), computed issue by issue. Specifically, for each GSS topic, we take the absolute difference between the mean Democratic response and the mean Republican response, normalized by the scale range, giving us a 0-to-1 score. We'll call this the **normalized partisan gap**.

**Party classification: GSS 7-point scale**

We classify respondents using the GSS 7-point partyid scale. Democrats are codes 0-2, Republicans are 4-6, and we exclude pure independents.

**Topic categories: 126 public issues, 73 private-life topics**

We require at least 100 respondents per party per topic. This gives us 126 public-issue topics — policy, government, social questions — and 73 private-life topics — religion, sexual attitudes, family structure, moral views.

**SLIDE 5: Activation-Side Measure**

**Pre-projection concatenated head outputs at last token**

On the LLM side, we prompt the model to simulate political actors responding to each topic, and we extract activations — specifically, the *input* to each layer's output projection, which gives us the pre-projection concatenated head outputs at the last token position. This is a tensor of shape: subjects by layers by heads by head-dimension — typically 128.

**Per-head PCA reduction and Mahalanobis distance**

For each attention head independently, we reduce to 15 PCA components, compute the Democratic and Republican centroids, and take the Mahalanobis distance — the generalized distance between centroids scaled by the pooled within-group covariance with a small regularization term. Intuitively, this is the number of standard deviations separating the two parties in the activation space of that head, accounting for the shape of the distribution rather than treating all directions equally. We average across all heads to get a single activation-polarization score per topic.

**Bramson taxonomy: group divergence + group consensus**

For those who know the Bramson et al. taxonomy of polarization measures, the Mahalanobis distance is a compound measure capturing party **divergence** — distance between centroids — but because it scales by variance, it also incorporates party **consensus** — tighter groups produce larger effective distances.

**SLIDE 6: Simulation Methods**

**Politician simulation: 550 Congress members, three prompt conditions**

We test two simulation methods. The **politician simulation** uses all 550 members of the 116th Congress. One prompt per politician per topic, with three framing conditions: rhetorical — "generate a statement by Senator X on this topic"; stance — "what is Senator X's position on this topic"; and survey — "how would Senator X respond to this survey question." These test different representational hypotheses about what the model encodes.

**Demographic simulation: 5-trait and 83-trait profiles**

The **demographic simulation** replaces politician names with real GSS respondents described by their demographic profiles — either 5 core traits or an expanded 83-trait profile. Each respondent's prompt includes their age, sex, race, religion, occupation, and so on, concatenated and randomly shuffled to prevent ordering artifacts.

**SLIDE 7: The Alignment Metric**

**Pearson correlation of per-topic scores across all topics**

The primary outcome is the Pearson correlation between the vector of per-topic LLM activation-polarization scores and the vector of per-topic GSS normalized partisan gaps, across all topics in a category. A high correlation means the topics where the LLM shows the largest partisan separation in activation space are the same topics where survey respondents show the largest partisan gaps.

**Relative ordering, not absolute magnitudes**

Note that this metric is indifferent to absolute magnitudes. It measures whether the model gets the *relative ordering* of issues right — whether it knows that, say, abortion is more partisan than environmental spending, and environmental spending is more partisan than confidence in science. This is important because we're not trying to replicate the GSS numbers themselves; we're asking whether the *topology* of partisan disagreement is encoded in the model's internal geometry.

**SLIDE 8: Main Result — Politician Simulation, Public Issues**

[Pause briefly]

OK, so here's the main result. Across 17 models and three prompt conditions on 126 public-issue topics, we see three clear patterns.

**Scale matters: 70B+ models surpass r = 0.65**

First, **scale matters**. The two 70B+ models — Qwen2.5-72B and Llama-3.3-70B — both surpass r = 0.65, with Qwen peaking at r = 0.708 under the stance condition. Mid-range 24-32B instruct models cluster around r = 0.63. Smaller 3-9B models are noisier but the best of them still hit r = 0.65 — Gemma-2-9b at 0.647, Llama-3.1-8B at 0.645.

**Prompt framing matters more at small scale**

Second, **prompt framing matters more at small scale**. For large models, the stance condition — simply asking the model what a politician's position is — tends to produce the highest correlations. At smaller scales, it's noisier. One interesting outlier: DeepSeek-R1-32B, the reasoning-oriented model, peaks at only r = 0.538 — substantially below other large models. The reasoning chain seems to interfere with straightforward political-stance retrieval in activation space.

**Uncensored fine-tuning beats doubling model size**

Third — and this is the most striking finding — **uncensored fine-tuning beats scale**. The strongest result across *all* public-issue experiments comes from Yi-34B-dolphin, an uncensored fine-tune that removes RLHF safety alignment. Its stance correlation is r = 0.723. This exceeds both 70B+ models, which have more than twice the parameters. The gap between the dolphin model and comparably-sized standard instruct models — about 8-9 points of correlation — is *larger* than the gap you get from doubling model size. The 8B dolphin Llama tells the same story at smaller scale: r = 0.662, outperforming the standard 8B instruct and matching models several times larger.

**RLHF as an artificial social desirability norm**

The interpretation: RLHF safety training attenuates the partisan geometry encoded in activations during pretraining, but it doesn't erase the underlying knowledge. Removing RLHF lets the partisan structure manifest more clearly. This is structurally parallel to something from the affective polarization literature — Iyengar and Westwood's 2015 finding that there are strong social norms against expressing racial prejudice but no equivalent norms against partisan prejudice, so removing normative constraints reveals stronger partisan structure. RLHF is, in effect, an artificial social desirability norm for the model.

**SLIDE 9: Private-Life Topics**

**Lower alignment overall, averaging r = 0.54**

On the 73 private-life topics — church attendance, sexual attitudes, family structure — alignment is generally lower, with instruct models averaging around r = 0.54. This makes sense: private behavior is less explicitly politicized in training corpora than gun control or abortion.

**Llama-3.1-8B exception: best score in entire study on private topics**

But some models surprise us. Llama-3.1-8B instruct achieves its *best correlation anywhere in the entire study* on private-life topics: r = 0.693 on the stance condition, higher than its public-issue score.

**Instruct advantage larger on private topics than public**

The instruct-over-base advantage is even larger on private topics than public, suggesting that instruction fine-tuning helps models draw on cultural sorting patterns — not just explicit policy knowledge — when simulating political personas.

**SLIDE 10: Politician vs. Demographic Simulation**

**Demographic correlations much weaker: best r = 0.31 (5-trait), r = 0.505 (83-trait)**

Now the comparison that has interpretive implications for the polarization literature. When we replace politician names with demographic profiles, correlations drop substantially. With 5 core traits, the best model reaches about r = 0.31. Even with 83 traits and uncensored models, the best result is r = 0.505 — meaningful but still well below the politician simulation.

**Elite knowledge encodes partisan structure more reliably than demographic inference**

This tells us something important: models encode partisan structure more reliably through parametric knowledge of named political elites than through inference from demographic correlates. The text ecosystem that trained these models encodes elite partisan positions abundantly and clearly — from news coverage, speeches, voting records. The demographic-to-attitude mapping is noisier and harder for the model to extract.

**Connection to top-down polarization theories**

In the polarization literature, there's a long debate about whether polarization is driven top-down by elites or bottom-up by mass attitudes. Hetherington's 2001 paper argues that elite polarization *clarified* party brands, making partisanship useful as a cognitive heuristic for ordinary citizens. Our finding is consistent with that picture: the model's representation of elite partisan structure more accurately predicts the mass polarization landscape than its representation of demographic structure. The informational scaffolding runs from elites downward — in the text ecosystem, at least.

**SLIDE 11: Transition to Depth Analysis**

OK, so we've established that LLM activation geometry mirrors the cross-topic structure of partisan disagreement. Now I want to go deeper into depth analysis.

**Does the layer of emergence tell us about the nature of the issue?**

The question is: does the *layer* at which partisan structure emerges tell us something about the *nature* of the issue?

**SLIDE 12: Question Fundamentalness — Setup**

**Structural centrality: which issues predict everything else?**

Here's the intuition. Some political questions are structurally central to the opinion landscape — if you know someone's position on abortion or gun control, you can predict a lot about their other views. Other questions are peripheral — knowing someone's view on, say, confidence in the scientific community tells you less about the rest of their belief system.

**Five independent survey-side measures of centrality**

On the survey side, we compute five independent measures of structural centrality from the GSS response matrix — about 11,000 respondents across 98 questions. These are: total normalized mutual information with all other questions; out-of-sample predictive power for all other questions; network centrality in the inter-question correlation graph — degree, betweenness, closeness, and eigenvector centrality; loading magnitudes on leading principal components; and proximity to the root of a Chow-Liu optimal dependency tree. These are all different ways of asking the same conceptual question: *which issues are the load-bearing walls of the political belief system?*

**Connection to constraint in DiMaggio et al.**

In the polarization literature, this connects to what DiMaggio et al. (1996) call **constraint** — the correlation of attitudes across issue domains. Constraint is the dimension of polarization that determines whether political coalitions can form and sustain themselves. If knowing your view on one issue predicts your view on others, then politics can organize around ideological packages. If it doesn't, you get issue-by-issue politics with no stable coalitions.

**LLM-side measure: same Mahalanobis score, new correlate**

On the LLM side, the measure is simply the Mahalanobis distance — the same activation-polarization score from before. But now, instead of correlating it with the GSS partisan gap, we correlate it with these structural centrality measures.

**SLIDE 13: Fundamentalness Results**

**Deeper-layer polarization tracks structural centrality**

And here's what we find: the issues where the model shows the largest partisan separation in deeper layers are the same issues that are most structurally central in the survey response matrix.

[Walk through the specific correlations with each fundamentalness measure — mutual information, predictive power, network centrality, PCA loadings, Chow-Liu proximity.]

**Stronger claim than the main correlation result**

This is a stronger finding than the main correlation result. The main result says the model knows *which issues are more partisan*. This says the model knows *which issues are more architecturally central to the political belief system* — which issues predict everything else, which issues are the organizing axes of political opinion.

**Second-order structure learned from text alone**

This goes beyond replicating the GSS. The GSS can tell you the partisan gap on each issue. But the *structural centrality* of each issue — its mutual information with all other issues, its position in the dependency tree — is a second-order property that requires the full response matrix to compute. The model appears to have absorbed this second-order structure from text alone.

**SLIDE 14: Why This Matters for Polarization Research**

**Baldassarri and Bearman's takeoff issues**

In the polarization literature, there's an elegant agent-based model by Baldassarri and Bearman from 2007 that explains how political "takeoff issues" emerge. In their model, most issues remain moderate, but occasionally one issue monopolizes social attention, reorganizes discussion networks around it, and becomes the axis of political division — while suppressing polarization on other issues.

**Emergent structural position, not intrinsic content**

What makes an issue a "takeoff issue" is not its intrinsic content but its *emergent structural position* — its relative polarization compared to other issues.

**Text ecosystem encodes decades of social interaction dynamics**

Our fundamentalness finding suggests that LLMs have learned this emergent structure from text. The model's activation geometry doesn't just reflect per-issue partisan gaps; it reflects which issues occupy the structurally central positions in the American political opinion landscape. This is arguably the most ambitious claim of the paper: the text ecosystem has absorbed and encoded the products of decades of social interaction dynamics, and LLMs have learned that structure.

**SLIDE 15: Contributions to the Polarization Literature**

Let me zoom out now and talk about what this means for the polarization field specifically.

**New measurement modality: addresses Nemeth's three critiques**

The most direct contribution is to the NLP and computational measurement literature. A 2023 scoping review by Nemeth found that 33% of NLP polarization studies use supervised classification — operationalizing polarization as classification accuracy. This conflates multiple things: how much a party talks about an issue, how distinctively they frame it, base rates, strategic language choices. Hirst et al. showed that classifiers can pick up government-vs-opposition status rather than ideology. And Nemeth's single biggest critique is that NLP studies almost never validate their measures against survey data.

Our study addresses all three problems. The Mahalanobis distance is not a classifier — it's a continuous geometric measure. It's validated against GSS survey data as its primary metric. And because we measure internal representations rather than output text, we sidestep the concern raised by Gentzkow, Shapiro, and Taddy that language divergence can reflect strategic framing rather than genuine attitude differences. If activation geometry correlates with survey gaps at r = 0.7, it's capturing something about actual attitude structure, not just rhetorical strategy.

**RLHF finding: no precedent in polarization literature**

The second contribution is the RLHF finding. No one in the polarization literature has drawn the parallel between RLHF alignment and social desirability norms. But the structure is the same: a normative constraint that attenuates the expression of partisan structure without erasing the underlying knowledge. The fact that removing RLHF has a larger effect than doubling model size tells us that safety alignment is doing something substantive to the political content of representations — it's not just a thin output filter.

**Fundamentalness: from replication to architecture**

The third contribution is the fundamentalness analysis, which moves the paper from "LLMs mirror surveys" to "LLMs have learned the architecture of political opinion space." If that claim holds up, it means the text ecosystem encodes not just which issues are partisan but which issues are *structurally central* — which issues are the load-bearing walls.

**SLIDE 16: Questions for This Group — LLM Social Simulation**

Now I want to shift to the part where I'm genuinely looking for your input, because you are the experts here.

The standard approach in LLM social simulation is to read the model's output — generate a survey response, extract a Likert rating, classify a stance. We're doing something different: reading the model's internal representations. This raises a set of questions I'd love to get your takes on.

**What exactly are we measuring?**

First: **what exactly are we measuring?** When we compute the Mahalanobis distance between Democratic and Republican centroids in the activation space of attention head 47 in layer 22, what is that object? It's not an attitude. It's not a statement. It's a property of the model's representational geometry when processing a politically-charged prompt. How should we think about the ontological status of this measurement?

**Does RLHF attenuation affect simulation validity?**

Second: **the RLHF finding — what does it mean for simulation validity?** If RLHF attenuates partisan structure in activations, then every LLM simulation study using instruct models is working with representations that have been deliberately de-politicized. Does this matter? If so, should simulation studies be using uncensored models? Or is the RLHF-attenuated version actually more like a person responding to a survey under normal social conditions — and therefore *more* valid for simulating survey responses?

**Can the politician-demographic gap be bridged?**

Third: **the politician-demographic gap**. The model knows partisan structure much better through named elites than through demographic profiles. For simulation studies that use demographic persona prompts, this suggests a ceiling on how much political structure the model can recover from demographic cues alone. Is there a way to bridge this gap — perhaps by combining demographic prompts with structural information about the political landscape?

**Generalizability beyond the US two-party case**

And fourth: **generalizability beyond the US two-party case**. Everything here relies on a clean binary partition — Democrats and Republicans. How would this approach translate to multiparty systems? To non-Western political landscapes where the partisan structure may not be well-represented in English-language training corpora?

I'll stop there and open it up for discussion.

**SLIDE 17: Summary**

Just to recap before we discuss:

**Activation geometry mirrors the topology of partisan disagreement**

One — LLM activation geometry, measured as per-head Mahalanobis distance, correlates at r = 0.65-0.72 with the cross-topic pattern of partisan gaps in the GSS. The model knows which issues are more and less partisan.

**RLHF suppresses partisan structure more than scale restores it**

Two — Uncensored models outperform standard instruct models by a margin larger than doubling model size, suggesting RLHF functions as an artificial norm that suppresses partisan structure in representations.

**Deeper layers encode structurally central issues**

Three — The issues with the highest activation-polarization scores in deeper layers are the same issues that are most structurally central in the survey response matrix — the model has learned not just which issues are partisan but which issues are architecturally fundamental to the opinion landscape.

**Elite knowledge outperforms demographic inference**

Four — Politician simulation vastly outperforms demographic simulation, suggesting that models encode partisan structure more reliably through parametric knowledge of named elites than through demographic inference.

Thanks. Happy to take questions.
# Talk Script Feedback: Persona-Based Audience Reactions

This file contains detailed feedback from simulated audience members across four fields. Each item specifies what the audience wants to see — empirical results, visuals, conceptual diagrams, or clarifications — with enough detail that the pipeline author can generate the needed materials.

---

## Persona Roster

| ID | Name | Field | Specialty |
|----|-------|-------|-----------|
| CS1 | Maya | Computer Science | NLP / representation learning |
| CS2 | Raj | Computer Science | Mechanistic interpretability |
| CS3 | Elena | Computer Science | LLM alignment / safety |
| DS1 | Tomás | Data Science | Applied statistics / causal inference |
| DS2 | Priya | Data Science | Computational social science |
| SOC1 | James | Sociology | Cultural sociology / Bourdieu tradition |
| SOC2 | Lin | Sociology | Quantitative methods / survey methodology |
| POL1 | Sarah | Political Science | American politics / polarization |
| POL2 | David | Political Science | Political behavior / public opinion |
| POL3 | Anika | Political Science | Comparative politics |
| PSY1 | Marcus | Psychology | Political psychology / motivated reasoning |
| PHIL1 | Clara | Philosophy of Science | Measurement theory / construct validity |

---

## SLIDE 1: Title

No visual requests.

---

## SLIDE 2: Three Fields, One Sentence Each

### Conceptual visual requested

**CS1 (Maya):** I'd want a Venn diagram or three-column layout showing the three fields and where this project sits at the intersection. Each column should have 2-3 bullet points naming the canonical approach in that field and then an arrow showing what this project does differently.

> **VISUAL REQUEST [SLIDE 2-A]:** Three-column comparison graphic.
> - Column 1: "Political Polarization" → canonical: surveys, voting records, text sentiment → this project: activation geometry
> - Column 2: "LLM Social Simulation" → canonical: read generated text / extracted Likert → this project: read internal representations
> - Column 3: "Mechanistic Interpretability" → canonical: circuit analysis, probing, SAEs → this project: per-head partisan geometry as a social science measure
> Format: Simple three-column layout with arrows or highlights showing the novel contribution in each.

---

## SLIDE 3: The Core Question

### Conceptual diagram: high polarization vs. low polarization in activation space

**CS2 (Raj):** The speaker mentions a TODO for a plot of high-polarization/high-dispersion vs. low-polarization/high-dispersion. This is critical. Without it, the audience won't have geometric intuition for what Mahalanobis distance is capturing vs. what it's not.

> **VISUAL REQUEST [SLIDE 3-A]:** Conceptual 2D scatter diagram (two panels side by side).
> - Panel A: "High partisan gap" — two clearly separated clusters (blue dots = Democrats, red dots = Republicans) in a 2D PCA space. Centroids marked with stars, distance arrow between them labeled "large Mahalanobis d."
> - Panel B: "Low partisan gap" — two heavily overlapping clusters in the same 2D space. Same number of dots, similar dispersion, but centroids close together. Distance arrow labeled "small Mahalanobis d."
> - Optional Panel C: "High dispersion but low gap" — wide scatter for both groups but centroids close, showing that Mahalanobis handles this correctly (distance is small because within-group spread is large).
> These can be synthetic/schematic data. Color: blue for D, red for R. Axes labeled "PC1" and "PC2."

**DS1 (Tomás):** Can you also show a case where Euclidean distance would be misleading but Mahalanobis gets it right? E.g., elongated elliptical clusters where the centroids are close along the major axis but well-separated along the minor axis.

> **VISUAL REQUEST [SLIDE 3-B]:** Conceptual 2D diagram showing why Mahalanobis > Euclidean.
> - Two elongated elliptical clusters (D and R) that are close in Euclidean distance (centroids near each other) but well-separated relative to their covariance structure (small distance along major axis, large separation along minor axis).
> - Show both the Euclidean distance line and the Mahalanobis distance, with the Mahalanobis one being larger.
> Synthetic data is fine. Label: "Why Mahalanobis: accounts for the shape of the distribution."

### Empirical grounding requested

**POL1 (Sarah):** When you say "about 200 topics," I immediately want to know: give me 3-4 example topics with high partisan gaps and 3-4 with low gaps, so I can calibrate my intuition. If you name them, I'll know instantly whether your measure is capturing something real.

> **EMPIRICAL REQUEST [SLIDE 3-C]:** A small table or ranked list showing:
> - The 5 GSS topics with the HIGHEST normalized partisan gap (with their gap values)
> - The 5 GSS topics with the LOWEST normalized partisan gap (with their gap values)
> - Maybe 3-4 in the middle range
> This gives the audience instant calibration. They should recognize that abortion/gun control are high and "confidence in X" are low.

---

## SLIDE 4: Survey-Side Measure

### Empirical visual requested

**SOC2 (Lin):** You define the normalized partisan gap but never show me the distribution. Is it bimodal? Skewed? Are there natural clusters? This is the dependent variable for the entire talk — I need to see its shape.

> **VISUAL REQUEST [SLIDE 4-A]:** Histogram of normalized partisan gap values across all 199 topics (or separate histograms for 126 public + 73 private).
> - X-axis: normalized partisan gap (0 to 1)
> - Y-axis: count of topics
> - Color-code or use separate panels for public vs. private topics
> - Annotate a few notable topics at extreme ends (e.g., label "abortion" at the high end, label "confidence in scientific community" at the low end)
> This gives the audience a feel for the overall landscape.

**POL2 (David):** How stable is this measure across GSS waves? You're using 2021-2024 cumulative. If I took 2018 data, would the ranking be similar? This matters because you're correlating with LLM activations from models trained on text from a wide time range.

> **EMPIRICAL REQUEST [SLIDE 4-B]:** Stability analysis.
> - Compute the normalized partisan gap separately for each GSS release year included (e.g., 2021, 2022, 2024 if those are the waves).
> - Report the Pearson correlation between the per-topic gap vectors across waves.
> - If the cross-wave correlation is high (e.g., r > 0.9), it means the relative ordering is stable and the specific year doesn't matter much. If it's lower, that's a concern.
> Even a single number ("the cross-wave correlation of topic-level partisan gaps is r = X") would suffice.

**DS1 (Tomás):** The exclusion criteria — 100 respondents per party per topic — how many topics does that cut? Show me the N per topic distribution so I know if you're at the margin.

> **EMPIRICAL REQUEST [SLIDE 4-C]:** Distribution of sample size per topic.
> - Histogram or sorted bar chart of (min(N_dem, N_rep)) across all candidate topics
> - Mark the 100-respondent cutoff line
> - Show how many topics are excluded by this threshold
> This is a quick sanity check — if most topics have 500+ respondents, the audience relaxes.

---

## SLIDE 5: Activation-Side Measure

### Technical clarification visuals

**CS2 (Raj):** I want a pipeline diagram. Show me the tensor shapes at each step. The verbal description of "subjects × layers × heads × head_dim" → PCA → centroids → Mahalanobis is hard to follow without a visual.

> **VISUAL REQUEST [SLIDE 5-A]:** Pipeline / flow diagram of activation extraction and distance computation.
> Step 1: Prompt → Model → extract pre-projection activations at last token → tensor (S × L × H × D), e.g., (550 × 32 × 32 × 128)
> Step 2: For each head (L, H): take slice (S × D) → PCA → (S × 15)
> Step 3: Split by party → compute centroid_D, centroid_R → (15,) each
> Step 4: Compute pooled covariance Σ (15 × 15) → Mahalanobis distance → scalar
> Step 5: Average across all L × H heads → one activation-polarization score per topic
> Use boxes and arrows. Label tensor shapes at each step.

**CS1 (Maya):** Why 15 PCA components? Is there a sensitivity analysis? If you use 5 or 30, does the correlation change?

> **EMPIRICAL REQUEST [SLIDE 5-B]:** PCA component sensitivity analysis.
> - Sweep the number of PCA components: {3, 5, 10, 15, 20, 30, 50, full dimension}
> - For each, compute the main alignment correlation (Pearson r with GSS gaps)
> - Plot: x-axis = number of PCA components, y-axis = correlation with GSS
> - Do this for 2-3 representative models (one large, one small, one uncensored)
> If the curve plateaus at 10-15, the choice of 15 is well-justified. If it keeps climbing, the audience will worry you're leaving signal on the table.

**DS1 (Tomás):** What's the regularization term? How sensitive are results to its value?

> **EMPIRICAL REQUEST [SLIDE 5-C]:** Regularization sensitivity.
> - Sweep the regularization parameter (whatever scalar is added to the diagonal of the covariance matrix) across a few orders of magnitude.
> - Report the main correlation for each setting.
> - Even just a sentence: "Results are stable across regularization values from 1e-4 to 1e-1" would satisfy this concern.

**PHIL1 (Clara):** Why the *mean* across all heads? Some heads might encode syntax, some semantics, some positional information. Averaging across all of them dilutes the political signal with noise. Have you tried selecting heads?

> **EMPIRICAL REQUEST [SLIDE 5-D]:** Head selection analysis.
> - For each head, compute the correlation between that head's Mahalanobis scores and GSS gaps (across topics).
> - Report the distribution of per-head correlations. Are most heads near zero? Are a few heads carrying all the signal?
> - Compare: (a) average across all heads, (b) average across top-10% heads, (c) average across top-5 heads. Which gives the highest correlation?
> - This also feeds into the interpretability story — if only a few heads carry partisan signal, which heads are they? Which layers?

> **VISUAL REQUEST [SLIDE 5-E]:** Heatmap of per-head correlation with GSS gaps.
> - X-axis: head index (0 to H-1)
> - Y-axis: layer index (0 to L-1)
> - Color: Pearson r between that head's per-topic Mahalanobis scores and the GSS partisan gap vector
> - Do this for 1-2 representative models
> This is the kind of figure that an interpretability audience will love. It shows where partisan information lives in the model.

---

## SLIDE 6: Simulation Methods

### Empirical detail requested

**POL1 (Sarah):** 116th Congress — that's 2019-2021. But the GSS data is 2021-2024. There's a temporal mismatch. Are you assuming the relative partisan ordering of issues is stable across this window? (This connects to the stability question from Slide 4.)

> **EMPIRICAL REQUEST [SLIDE 6-A]:** Temporal alignment check.
> - Explicitly state the temporal overlap (or lack thereof) between the Congress used and the GSS waves.
> - If possible, check whether using the 117th or 118th Congress changes results (assuming the model knows those members too).
> - At minimum, acknowledge the mismatch and cite the stability analysis from Slide 4.

**CS1 (Maya):** Show me the three prompt templates verbatim. I want to see the exact text.

> **VISUAL REQUEST [SLIDE 6-B]:** Prompt template display.
> - Show the exact system message and the three user-message templates (rhetorical, stance, survey) with the topic slot highlighted.
> - One example per condition, filled in with a real topic (e.g., "gun control") and a real politician name (e.g., "Senator Ted Cruz").
> Put this on the slide as a text box or code block. Audiences always want to see the actual prompts.

**DS2 (Priya):** For the demographic simulation — what does an 83-trait prompt actually look like? That sounds enormous. How many tokens is it?

> **VISUAL REQUEST [SLIDE 6-C]:** Example demographic prompt.
> - Show one full 83-trait prompt for a real (anonymized) GSS respondent.
> - Annotate: how many tokens, which traits are included, what the random shuffling looks like.
> - Side-by-side with a 5-trait prompt for the same respondent, to show the difference.

---

## SLIDE 7: The Alignment Metric

### Conceptual visual requested

**SOC1 (James):** The Pearson correlation is abstract. Show me the actual scatter plot. I want to see 126 dots, each a topic, x-axis = GSS gap, y-axis = LLM activation score, with labels on a few notable topics. That is worth more than the r value.

> **VISUAL REQUEST [SLIDE 7-A]:** The money plot. Scatter plot of GSS partisan gap vs. LLM activation polarization.
> - One plot for the best model + condition (e.g., Yi-34B-dolphin, stance, public issues)
> - X-axis: normalized partisan gap (GSS)
> - Y-axis: mean Mahalanobis distance (LLM)
> - Each dot is a topic (N = 126 for public issues)
> - Label 8-10 notable topics: the ones at extreme high (abortion, gun control), extreme low, and interesting outliers (topics where LLM and GSS disagree most)
> - Regression line with r value and 95% CI band
> - Color or shape code by broad topic category if useful (economic, social, moral, etc.)
> This is THE figure of the talk. It should be the largest, clearest visual.

**DS1 (Tomás):** Show me the same plot for a *bad* model too — one of the weak demographic simulations. The contrast will make the main result pop.

> **VISUAL REQUEST [SLIDE 7-B]:** Paired scatter plots: strong vs. weak.
> - Left panel: best model (Yi-34B-dolphin, r = 0.723)
> - Right panel: weak demographic simulation (e.g., Llama-3.1-8B 5-trait, r ≈ 0.13)
> - Same axes, same topic labels, same scale
> - The visual contrast between a tight cloud along the diagonal and a formless blob will immediately communicate the result.

**POL2 (David):** Which topics are the biggest outliers? Where does the model most disagree with the GSS? That's where the interesting stories are.

> **EMPIRICAL REQUEST [SLIDE 7-C]:** Residual analysis for the main scatter plot.
> - Fit the regression line for the best model/condition
> - List the 10 topics with the largest positive residuals (LLM thinks more partisan than GSS says) and the 10 with the largest negative residuals (LLM thinks less partisan than GSS says)
> - For each, report: topic name, GSS gap, LLM score, residual
> - Are there interpretable patterns? E.g., does the LLM overestimate partisanship on culture-war issues that get disproportionate media attention? Does it underestimate partisanship on technical policy issues?

---

## SLIDE 8: Main Result — Politician Simulation, Public Issues

### Empirical visuals requested

**CS1 (Maya):** The verbal listing of r values is hard to follow. Give me a grouped bar chart or dot plot.

> **VISUAL REQUEST [SLIDE 8-A]:** Model comparison chart (public issues).
> - Y-axis: model name (sorted by parameter count, largest at top)
> - X-axis: Pearson r with GSS gaps
> - Three bars/dots per model (one per prompt condition: rhetorical, stance, survey), color-coded
> - Highlight the uncensored (dolphin) models with a distinct marker or border
> - Mark the r = 0.65 line as a reference
> - Group models by size tier: 70B+, 24-32B, 7-9B, 3-4B
> This replaces three paragraphs of spoken numbers with one clear figure.

**CS3 (Elena):** The RLHF claim is strong. Can you show a direct paired comparison? Same base model, instruct vs. dolphin, side by side?

> **VISUAL REQUEST [SLIDE 8-B]:** Paired comparison: instruct vs. uncensored.
> - For each model family where both an instruct and a dolphin version exist (Llama-3-8B, Yi-34B, Mistral-7B):
>   - Bar pair: instruct r vs. dolphin r, same prompt condition (stance)
>   - Arrow or annotation showing the delta
> - Also show the delta from doubling model size (e.g., 8B instruct vs. 70B instruct) for comparison
> - The visual argument: RLHF removal produces a bigger jump than 2× parameters

**PSY1 (Marcus):** The DeepSeek-R1 outlier is interesting. Does the reasoning chain literally suppress partisan structure? Can you show a comparison of the reasoning model's activation patterns vs. a standard model?

> **EMPIRICAL REQUEST [SLIDE 8-C]:** DeepSeek-R1 analysis.
> - Is the lower r for DeepSeek due to uniformly lower Mahalanobis distances (partisan structure suppressed everywhere), or does it get some topics right and others wrong?
> - Scatter plot: DeepSeek-R1 per-topic scores vs. GSS gaps (same format as SLIDE 7-A but for this specific model)
> - If possible, compare the distribution of per-topic Mahalanobis distances between DeepSeek-R1 and a comparably-sized standard instruct model — is DeepSeek's distribution compressed?

### Confidence interval / significance requested

**DS1 (Tomás):** Are any of these r values significantly different from each other? With 126 topics, r = 0.65 and r = 0.72 might not be statistically distinguishable. Give me confidence intervals or a bootstrap test.

> **EMPIRICAL REQUEST [SLIDE 8-D]:** Confidence intervals on the main correlations.
> - For each model × condition, report the 95% bootstrap CI on the Pearson r (e.g., bootstrap the set of 126 topics).
> - Alternatively, Fisher z-transformation test for comparing two correlations.
> - At minimum, show error bars on the model comparison chart (SLIDE 8-A).
> - Key comparisons to test: (1) dolphin vs. same-size instruct, (2) 70B instruct vs. 34B dolphin, (3) best model vs. second-best.

---

## SLIDE 9: Private-Life Topics

### Empirical visual requested

**SOC1 (James):** Which private-life topics are the most partisan? I study cultural sorting — I bet church attendance and abortion-adjacent moral questions are at the top. Show me.

> **EMPIRICAL REQUEST [SLIDE 9-A]:** Ranked list or bar chart of private-life topics by partisan gap.
> - Top 10 and bottom 10 private-life topics by GSS normalized partisan gap
> - Do the LLM rankings agree? Show both side by side.
> - Are the topics that the LLM gets most wrong (biggest residuals) interpretable?

**CS1 (Maya):** The Llama-3.1-8B private-topics result is surprising. Is this robust or a fluke? What's the confidence interval?

> **EMPIRICAL REQUEST [SLIDE 9-B]:** Robustness check on the Llama-3.1-8B private-topics result.
> - Bootstrap CI on this specific r = 0.693
> - Does this hold across all three prompt conditions, or only stance?
> - What happens if you remove the top 5 highest-gap private topics? Does the correlation collapse?

**POL1 (Sarah):** The public vs. private distinction is doing a lot of work. How do you classify topics? Is there a gray zone? Show me 5 topics that could go either way.

> **EMPIRICAL REQUEST [SLIDE 9-C]:** Topic classification validation.
> - List 5-10 borderline topics that could be classified as either public or private
> - Report whether results change if you move them across categories
> - Or if classification was done by a codebook, state the inter-rater reliability

---

## SLIDE 10: Politician vs. Demographic Simulation

### Empirical visual requested

**DS2 (Priya):** This is a critical comparison. Show me a scatter plot matrix: politician vs. demographic, 5-trait vs. 83-trait, for the same model. Four panels.

> **VISUAL REQUEST [SLIDE 10-A]:** 2×2 panel scatter plot comparison.
> - Top-left: Politician simulation, instruct model (r ≈ 0.65)
> - Top-right: Politician simulation, dolphin model (r ≈ 0.72)
> - Bottom-left: Demographic 5-trait, instruct model (r ≈ 0.31)
> - Bottom-right: Demographic 83-trait, dolphin model (r ≈ 0.505)
> - All four panels: same axes (GSS gap vs. LLM score), same scale, same topic labels
> - The visual degradation from top to bottom tells the story immediately.

**SOC2 (Lin):** Which demographic traits matter most? You have 83 traits. Can you do an ablation — remove traits one at a time or in groups and see which cause the biggest drop?

> **EMPIRICAL REQUEST [SLIDE 10-B]:** Demographic trait importance analysis.
> - For the 83-trait demographic simulation, compute the correlation when removing each trait (or group of traits: e.g., all religion traits, all income traits, all education traits).
> - Which traits, when removed, cause the biggest drop in correlation?
> - Alternatively: start from 0 traits and add them greedily. What's the marginal contribution of each?
> - This tells us which demographic signals the model uses to infer political attitudes.

**POL2 (David):** The Hetherington connection is compelling but it's just an analogy. Is there a more direct test? For instance, for each politician, do you know their DW-NOMINATE score? Can you show that the model's activation-space position correlates with the politician's ideological score?

> **EMPIRICAL REQUEST [SLIDE 10-C]:** DW-NOMINATE validation.
> - For each of the 550 Congress members, you have their DW-NOMINATE first-dimension score (liberal-conservative).
> - Can you project each politician's activations onto the axis connecting the D and R centroids and correlate that projection with their DW-NOMINATE score?
> - This would be a powerful individual-level validation beyond the aggregate topic-level correlation.
> - Even just reporting: "The correlation between a politician's activation-space projection and their DW-NOMINATE score is r = X" would be a major result.

---

## SLIDE 11: Transition to Depth Analysis

### Conceptual visual requested

**CS2 (Raj):** The transition needs a visual. Show a schematic of a transformer with layers highlighted, and the idea that "partisan structure emerges at different depths for different issues."

> **VISUAL REQUEST [SLIDE 11-A]:** Conceptual layer diagram.
> - Schematic of a transformer stack (layer 0 at bottom, layer L at top)
> - Two example topics: one where partisan structure appears in early layers (e.g., a concrete policy issue like gun control), one where it appears only in deeper layers (e.g., a structurally central issue like abortion or party identification itself)
> - Use color intensity to show "partisan signal strength" at each layer
> - This is purely conceptual/schematic — it sets up the empirical result on the next slide.

---

## SLIDE 12: Question Fundamentalness — Setup

### Conceptual visuals requested

**SOC1 (James):** The five fundamentalness measures are a lot to absorb verbally. Show me a visual taxonomy.

> **VISUAL REQUEST [SLIDE 12-A]:** Taxonomy of fundamentalness measures.
> - Five boxes or icons, each with a 1-line description:
>   1. Mutual information: "How much does knowing this answer reduce uncertainty about all other answers?"
>   2. Predictive power: "How well can this answer predict all other answers?"
>   3. Network centrality: "How central is this issue in the correlation network?"
>   4. PCA loadings: "How much does this issue load on the main dimensions of variation?"
>   5. Chow-Liu tree: "How close is this issue to the root of the optimal dependency tree?"
> - Optionally group them: information-theoretic (1,2,5), graph-theoretic (3), linear-algebraic (4)

**POL1 (Sarah):** Again, I want to know which topics are most fundamental. Give me a ranked list.

> **EMPIRICAL REQUEST [SLIDE 12-B]:** Ranked list of topics by fundamentalness.
> - The 10 most structurally central topics (averaged across the 5 measures, or reported per-measure)
> - The 10 least structurally central topics
> - Are the most central topics the same as the most partisan? Or is fundamentalness a distinct property?
> - A scatter plot of partisan gap vs. fundamentalness would clarify this.

> **VISUAL REQUEST [SLIDE 12-C]:** Scatter plot: partisan gap vs. fundamentalness.
> - X-axis: normalized partisan gap
> - Y-axis: composite fundamentalness score (or one of the five measures)
> - Each dot is a topic, labeled
> - Show the correlation
> - This reveals whether "most partisan" and "most fundamental" are the same thing or different constructs.

**CS2 (Raj):** The Chow-Liu tree itself would be a great visual. Show me the dependency tree of political opinion.

> **VISUAL REQUEST [SLIDE 12-D]:** Chow-Liu dependency tree of GSS questions.
> - Nodes = GSS topics, sized by fundamentalness or degree
> - Edges = optimal dependency tree links
> - Color nodes by topic category (economic, social, moral, etc.) or by partisan gap intensity
> - Label the root node and first-level branches
> - This is a striking visual that communicates the "architecture of political opinion" metaphor.

---

## SLIDE 13: Fundamentalness Results

### Empirical visuals requested

**DS1 (Tomás):** "Deeper-layer polarization tracks structural centrality" — show me the correlation, not just tell me. Scatter plot or table.

> **VISUAL REQUEST [SLIDE 13-A]:** The fundamentalness correlation figure.
> - 5 scatter plots (one per fundamentalness measure) or a single multi-panel figure.
> - X-axis: survey-side fundamentalness measure
> - Y-axis: LLM activation polarization score (deep-layer variant)
> - Each dot is a topic
> - Report r and p-value for each panel
> - Label a few notable topics in each
> This is the core evidence for the strongest claim. It must be shown as a figure.

**CS2 (Raj):** You say "deeper layers" — what exactly does that mean? The middle 10% of layers? The last few layers? Show me the layer-by-layer profile.

> **VISUAL REQUEST [SLIDE 13-B]:** Layer-by-layer correlation profile.
> - X-axis: layer index (or layer depth as fraction of total)
> - Y-axis: correlation between that layer's per-topic Mahalanobis scores and the fundamentalness measure
> - One line per fundamentalness measure (or one per model)
> - Show where the correlation peaks — is it in the middle layers? The final layers? Does it keep increasing?
> This is crucial for the "deeper = more fundamental" narrative.

**DS1 (Tomás):** Is there a "layer × topic" interaction? I.e., do some topics peak in early layers and others in late layers? Can you show heatmaps?

> **VISUAL REQUEST [SLIDE 13-C]:** Topic × layer heatmap.
> - X-axis: layer index
> - Y-axis: topics sorted by fundamentalness (most fundamental at top)
> - Color: Mahalanobis distance at that layer for that topic
> - If the fundamentalness claim is right, you should see a gradient: fundamental topics light up in deeper layers, peripheral topics light up earlier or uniformly.
> Do this for 1-2 representative models.

**POL1 (Sarah):** You're claiming the model knows "which issues are the load-bearing walls." Can you make a prediction? Take a topic the GSS didn't ask about — something new — and predict its fundamentalness from the LLM's activation geometry. That would be a held-out test.

> **EMPIRICAL REQUEST [SLIDE 13-D]:** Out-of-sample validation idea.
> - Hold out 20% of topics from the fundamentalness correlation.
> - Fit the relationship on the remaining 80%.
> - Predict the fundamentalness of the held-out topics from their LLM activation scores.
> - Report out-of-sample r or MSE.
> - This is a robustness check. If the audience is skeptical of overfitting with 5 measures × many topics, this addresses it.

---

## SLIDE 14: Why This Matters for Polarization Research

### Conceptual visual requested

**SOC1 (James):** The Baldassarri-Bearman takeoff issue mechanism is elegant but abstract. Show a diagram of their model.

> **VISUAL REQUEST [SLIDE 14-A]:** Schematic of the Baldassarri-Bearman takeoff mechanism.
> - Panel A: "Before takeoff" — many issues with moderate, similar levels of polarization (flat bar chart)
> - Panel B: "After takeoff" — one issue has spiked to high polarization while others have declined or stayed flat (bar chart with one tall bar)
> - Panel C: Connection to your finding — the LLM's activation geometry reflects the current "post-takeoff" structure, with some issues occupying structurally central positions
> Simple bar chart evolution or network diagram.

---

## SLIDE 15: Contributions to the Polarization Literature

### Empirical comparison requested

**DS2 (Priya):** You compare to NLP classification approaches in words. Can you show a direct comparison? E.g., train a partisan classifier on the same data and compare its accuracy-based "polarization measure" to your Mahalanobis measure, both correlated with GSS?

> **EMPIRICAL REQUEST [SLIDE 15-A]:** Head-to-head comparison with classification baseline.
> - For the same set of topics, compute a classification-based polarization score: train a logistic regression or small classifier to predict party from generated text (or from activations), and use classification accuracy as the polarization proxy.
> - Correlate this classification-accuracy-based measure with GSS gaps.
> - Show the Mahalanobis correlation side-by-side with the classification correlation.
> - If Mahalanobis outperforms, this directly validates the "continuous geometric measure beats classification" claim.
> - If comparable, it still shows that your measure adds geometric interpretability.

**CS3 (Elena):** The RLHF-as-social-desirability-norm claim is great, but can you quantify how RLHF changes the activation geometry? Not just the correlation drop, but the actual geometry. Do the clusters get more compact? Do they shift toward a neutral center? Do certain heads lose partisan signal?

> **EMPIRICAL REQUEST [SLIDE 15-B]:** RLHF geometric analysis.
> - For a matched instruct/dolphin pair (e.g., Llama-3-8B):
>   - Compare the average Mahalanobis distance across topics (is it uniformly lower in instruct?)
>   - Compare the per-head signal distribution (do certain heads lose partisan structure disproportionately?)
>   - Compare the PCA variance explained (is the partisan axis less prominent in instruct?)
> - Visualization: two per-head heatmaps (same as SLIDE 5-E) side by side — instruct vs. dolphin — showing where RLHF suppresses signal.

---

## SLIDE 16: Questions for This Group

### Anticipated questions from each persona

**CS1 (Maya):** "Have you tried probing classifiers as a comparison? A linear probe trained to predict party from activations would give you a per-layer accuracy curve. How does that compare to Mahalanobis distance?"

> **EMPIRICAL REQUEST [SLIDE 16-A]:** Linear probing comparison.
> - For each layer, train a linear probe (logistic regression) on the activations to predict party.
> - Plot probing accuracy by layer.
> - Compare the layer profile of probing accuracy to the layer profile of Mahalanobis distance.
> - If they diverge, it shows Mahalanobis is capturing something beyond linear separability.

**CS2 (Raj):** "Is the partisan structure causal? If you intervene on the partisan-direction in activation space (e.g., add or subtract the D→R direction vector), does the model's generated text change in a politically predictable way?"

> **EMPIRICAL REQUEST [SLIDE 16-B]:** Causal intervention (activation patching) analysis.
> - Compute the mean difference vector (R centroid - D centroid) in activation space for a politically active head.
> - For a given topic, take a Democrat's activations and add the R-D direction vector.
> - Does the model's output shift toward Republican positions?
> - This is a standard activation-patching experiment. Even preliminary results would greatly strengthen the talk.

**CS3 (Elena):** "You mention RLHF attenuates partisan structure. Does DPO do the same? What about constitutional AI? Can you test across different alignment methods?"

> This is a question for discussion, not a new analysis. But note it for future work.

**SOC2 (Lin):** "Your GSS measure uses mean difference. But what about the *shape* of the response distribution? If Democrats are bimodal on an issue (half strongly favor, half moderately oppose) and Republicans are unimodal, the mean difference understates the complexity. Have you considered distribution-comparison measures like Jensen-Shannon divergence on the response distributions?"

> **EMPIRICAL REQUEST [SLIDE 16-C]:** Alternative survey-side measures.
> - In addition to the normalized partisan gap (mean difference), compute:
>   - Jensen-Shannon divergence between D and R response distributions
>   - Earth mover's distance between D and R response distributions
>   - Bimodality coefficient within each party
> - Correlate these with the LLM activation scores.
> - Do they change the picture? Is the LLM better aligned with one measure than another?
> - This would address whether the LLM is encoding just the mean shift or the full distributional structure.

**POL2 (David):** "This is all cross-sectional. Can you say anything about temporal change? For instance, if you prompted the model with politicians from the 110th Congress (2007-2009) vs. the 116th (2019-2021), would the activation-polarization scores shift in the same direction as the GSS gaps did over that period?"

> **EMPIRICAL REQUEST [SLIDE 16-D]:** Temporal analysis.
> - Re-run the politician simulation with members of an earlier Congress (e.g., 110th Congress, 2007-2009).
> - Compare per-topic activation-polarization scores between the two Congresses.
> - Do topics that became more partisan in the GSS over that period also show larger increases in activation-polarization?
> - This tests whether the model has learned temporal dynamics, not just the current snapshot.

**POL3 (Anika):** "What happens with non-US models? If you use a Chinese LLM trained primarily on Chinese-language corpora, does the American partisan structure still appear? If so, that suggests the structure is in the English-language text regardless of the model's training focus."

> This is mostly a discussion question but note it as a future robustness check:
> **EMPIRICAL REQUEST [SLIDE 16-E]:** Cross-lingual / cross-training-corpus analysis.
> - If you have access to models with different training corpus compositions (e.g., Qwen is trained with more Chinese text, Llama with more English), compare how well they recover US partisan structure.
> - You already have Qwen2.5-72B in the study — compare its performance on US politics with its performance on topics where Chinese-language training might help or hurt.

**PSY1 (Marcus):** "The motivated reasoning literature predicts that attitude-consistent and attitude-inconsistent information are processed differently. When the model simulates a Democrat responding to a Republican-coded topic (like gun rights), does the activation look qualitatively different than when simulating a Democrat on a Democrat-coded topic (like environmental regulation)? Is there an asymmetry in the geometry?"

> **EMPIRICAL REQUEST [SLIDE 16-F]:** Attitude-congruence asymmetry.
> - For each topic, categorize whether it's D-leaning or R-leaning (based on which party has the higher mean in the GSS).
> - Compare the Mahalanobis distance for D-leaning vs. R-leaning topics.
> - Within each party's activations, is the variance higher on incongruent topics (as motivated reasoning would predict)?
> - This connects to Taber & Lodge's hot cognition model.

**PHIL1 (Clara):** "You're claiming convergent validity between two very different measurement modalities — surveys and activations. But convergent validity requires that you also show discriminant validity. What *doesn't* correlate with your Mahalanobis measure? Is there a construct that should NOT correlate with partisan structure that you can use as a negative control?"

> **EMPIRICAL REQUEST [SLIDE 16-G]:** Discriminant validity check.
> - Identify a set of GSS topics that are NOT politically polarized but DO have high variability (e.g., topics where people disagree a lot but not along party lines — perhaps "how many hours of TV do you watch per day" or similar).
> - Compute the LLM activation-polarization score for these topics.
> - Show that the Mahalanobis distance is LOW for these high-variability-but-nonpartisan topics.
> - This confirms the measure is capturing partisan structure specifically, not just any kind of heterogeneity in the model's responses.

---

## SLIDE 17: Summary

### Visual request

**All personas:** The summary slide should have a compact visual version of the four findings, not just text.

> **VISUAL REQUEST [SLIDE 17-A]:** Summary infographic.
> Four quadrants or four panels:
> 1. "Activation ↔ Survey alignment" — mini scatter plot silhouette showing r = 0.65-0.72
> 2. "RLHF suppression" — paired bar showing instruct vs. dolphin gap > scale gap
> 3. "Depth = Fundamentalness" — mini layer profile showing deeper layers correlate with centrality
> 4. "Elite > Demographic" — two bars showing politician r >> demographic r

---

## Cross-Cutting Requests (applicable to multiple slides)

### Statistical reporting standards

**DS1 (Tomás):** Throughout the talk, every correlation should have:
> - Sample size (N topics)
> - 95% CI (bootstrap)
> - Corresponding p-value or at minimum a significance indicator
> These can be in small text on figures. The audience will trust the results more.

### Robustness checks to mention or have in backup slides

**DS1 (Tomás) + SOC2 (Lin):**
> 1. **Spearman rank correlation** in addition to Pearson (mentioned in methodology but not in results). Report both.
> 2. **Median centroids** instead of mean centroids (mentioned as a robustness check). Report whether results change.
> 3. **Leave-one-topic-out cross-validation** for the main correlation — is any single topic driving the result?
> 4. **Multiple testing correction** — with 17 models × 3 conditions × 2 topic categories, you're running 102 correlations. Which survive Bonferroni or FDR correction?

### Backup slides to prepare

**All personas:**
> 1. Full table of all 17 models × 3 conditions × 2 topic categories (102 correlations) — the complete results matrix
> 2. Per-head heatmap for at least 2 models (one instruct, one dolphin)
> 3. Scatter plot for every model (not just the best one) — keep these as backup
> 4. The full ranked list of all 199 topics by partisan gap AND by activation polarization score
> 5. Prompt templates (all three conditions, verbatim)
> 6. Sensitivity analyses (PCA components, regularization, head selection)
> 7. The Chow-Liu tree visualization
> 8. DW-NOMINATE validation (if computed)

---

## Priority Ranking of Visual/Empirical Requests

### Must-have for the talk (produce these first)

| Priority | ID | Description |
|----------|----|-------------|
| 1 | SLIDE 7-A | Main scatter plot: GSS gap vs. LLM activation score, best model, labeled topics |
| 2 | SLIDE 8-A | Model comparison bar/dot chart (17 models × 3 conditions) |
| 3 | SLIDE 13-A | Fundamentalness correlation scatter plots (5 measures) |
| 4 | SLIDE 3-A | Conceptual 2D diagram: high vs. low partisan gap in activation space |
| 5 | SLIDE 5-A | Pipeline diagram: activation extraction → PCA → Mahalanobis |
| 6 | SLIDE 8-B | Paired comparison: instruct vs. dolphin, and vs. scale doubling |
| 7 | SLIDE 10-A | 2×2 panel: politician vs. demographic, instruct vs. dolphin |
| 8 | SLIDE 3-C | Top/bottom/middle GSS topics ranked by partisan gap |
| 9 | SLIDE 6-B | Verbatim prompt templates with examples |
| 10 | SLIDE 13-B | Layer-by-layer correlation profile |

### High priority (produce if time permits)

| Priority | ID | Description |
|----------|----|-------------|
| 11 | SLIDE 5-E | Per-head heatmap of correlation with GSS gaps |
| 12 | SLIDE 7-C | Residual analysis: biggest outlier topics |
| 13 | SLIDE 12-B | Ranked list of topics by fundamentalness |
| 14 | SLIDE 12-C | Scatter: partisan gap vs. fundamentalness |
| 15 | SLIDE 4-A | Histogram of partisan gap distribution |
| 16 | SLIDE 13-C | Topic × layer heatmap sorted by fundamentalness |
| 17 | SLIDE 12-D | Chow-Liu dependency tree visualization |
| 18 | SLIDE 7-B | Paired scatter: best model vs. worst model |
| 19 | SLIDE 17-A | Summary infographic (four-panel) |
| 20 | SLIDE 2-A | Three-field comparison graphic |

### Nice-to-have (backup slides or future analyses)

| Priority | ID | Description |
|----------|----|-------------|
| 21 | SLIDE 5-B | PCA component sensitivity sweep |
| 22 | SLIDE 8-D | Bootstrap CIs on all correlations |
| 23 | SLIDE 10-C | DW-NOMINATE individual-level validation |
| 24 | SLIDE 15-A | Head-to-head with classification baseline |
| 25 | SLIDE 15-B | RLHF geometric analysis (instruct vs. dolphin per-head comparison) |
| 26 | SLIDE 16-C | Alternative survey measures (JSD, EMD) |
| 27 | SLIDE 16-D | Temporal analysis (different Congress) |
| 28 | SLIDE 16-F | Attitude-congruence asymmetry |
| 29 | SLIDE 16-G | Discriminant validity (nonpartisan high-variance topics) |
| 30 | SLIDE 16-B | Causal intervention / activation patching |
| 31 | SLIDE 13-D | Out-of-sample fundamentalness prediction |
| 32 | SLIDE 10-B | Demographic trait importance ablation |
| 33 | SLIDE 16-A | Linear probing comparison |
| 34 | SLIDE 4-B | Cross-wave stability of partisan gaps |
| 35 | SLIDE 4-C | Sample size per topic distribution |
| 36 | SLIDE 5-C | Regularization sensitivity |
| 37 | SLIDE 5-D | Head selection analysis (top-k heads vs. all heads) |
| 38 | SLIDE 6-C | Example 83-trait demographic prompt |
| 39 | SLIDE 9-A | Private-life topic rankings |
| 40 | SLIDE 9-B | Llama-3.1-8B private-topics robustness check |
| 41 | SLIDE 9-C | Topic classification validation |
| 42 | SLIDE 6-A | Temporal alignment check (Congress vs. GSS waves) |
| 43 | SLIDE 8-C | DeepSeek-R1 deep dive |
| 44 | SLIDE 11-A | Conceptual layer depth diagram |
| 45 | SLIDE 14-A | Baldassarri-Bearman takeoff mechanism schematic |
| 46 | SLIDE 16-E | Cross-training-corpus comparison |

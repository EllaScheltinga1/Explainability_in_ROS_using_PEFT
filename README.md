# Personalising Explanations for Failures in ROS using PEFT

## Overview
This repository contains supplementary results and additional insights for our paper:

**Personalising Explanations for Failures in Robot Operating System using Parameter-Efficient Fine-Tuning**

By Ella Scheltinga and Chris Pek

## Additional Results
### Test 1 & 2

#### Table 1: Mean Suitability Ratings for Target Audience for Different Personalizations

| Personalisation Type       | Mean  | Std. Dev | p-value         |
| -------------------------- | ----- | -------- | --------------- |
| **Expert Suitability**     |       |          |                 |
| Original                   | 6.13  | 0.387    | -               |
| Expert short               | 6.19  | 0.341    | 0.157           |
| Non-expert short           | 4.66  | 0.623    | **1.55e-72***   |
| Expert medium              | 6.51  | 0.212    | **2.42e-24**    |
| Non-expert medium          | 3.87  | 0.731    | **1.88e-100***  |
| Expert long                | 6.49  | 0.328    | **3.65e-17**    |
| Non-expert long            | 2.36  | 0.597    | **2.59e-146***  |
| **Non-expert Suitability** |       |          |                 |
| Original                   | 4.10  | 0.522    | -               |
| Expert short               | 3.66  | 0.726    | **8.72e-73***   |
| Non-expert short           | 5.52  | 0.435    | **1.14e-70**    |
| Expert medium              | 3.20  | 0.595    | **5.97e-115***  |
| Non-expert medium          | 5.85  | 0.330    | **2.63e-90**    |
| Expert long                | 2.45  | 0.680    | **1.05e-132***  |
| Non-expert long            | 6.12  | 0.251    | **7.52e-104**   |
| **Short Suitability**      |       |          |                 |
| Original                   | 4.03  | 0.900    | -               |
| Expert short               | 5.89  | 0.517    | **6.86e-66**    |
| Non-expert short           | 5.74  | 0.548    | **5.28e-56**    |
| Expert long                | 1.99  | 0.209    | **2.57e-179***  |
| Non-expert long            | 2.10  | 0.250    | **6.56e-179***  |
| **Medium Suitability**     |       |          |                 |
| Original                   | 5.65  | 0.480    | -               |
| Expert medium              | 5.70  | 0.468    | 0.167           |
| Non-expert medium          | 5.68  | 0.362    | 0.447           |
| **Long Suitability**       |       |          |                 |
| Original                   | 5.33  | 0.972    | -               |
| Expert short               | 3.52  | 0.998    | **6.78e-181***  |
| Non-expert short           | 3.30  | 0.847    | **4.09e-180***  |
| Expert long                | 6.45  | 0.298    | **3.24e-33**    |
| Non-expert long            | 6.25  | 0.263    | **9.06e-25**    |

### Test 3
#### Table 2: Mean Ratings for Personalisation Types Across Evaluation Criteria

| Personalisation Type        | Crit 1: Relevance to Question | Crit 2: Contextual Accuracy | Crit 3: Enhancement of Understanding | Crit 4: Explanation Clarity | Crit 5: Contextual Explanation Quality |
| --------------------------- | ----------------------------- | --------------------------- | ------------------------------------ | --------------------------- | -------------------------------------- |
| Original                    | 6.49                          | 6.51                        | 6.62                                 | 6.28                        | 6.48                                   |
| Expert short                | 6.36                          | 6.55                        | 6.68                                 | **6.47**                    | 6.49                                   |
| Expert medium               | 6.27                          | **6.75**                    | **6.88**                             | **6.55**                    | **6.84**                               |
| Expert long                 | 5.93                          | 6.56                        | 6.81                                 | 6.20                        | **6.75**                               |
| Expert long (improved)      | **6.39**                      | 6.52                        | **6.88**                             | **6.51**                    | 6.75                                   |
| Non-expert short            | 5.91                          | 6.28                        | 6.06                                 | 6.08                        | 5.95                                   |
| Non-expert short (improved) | **6.27**                      | 6.34                        | **6.41**                             | **6.40**                    | **6.24**                               |
| Non-expert medium           | 6.26                          | 6.45                        | 6.53                                 | **6.40**                    | 6.43                                   |
| Non-expert long             | 5.53                          | 6.29                        | 6.38                                 | 6.14                        | 6.55                                   |
| Non-expert long (improved)  | **6.27**                      | 6.34                        | **6.52**                             | **6.40**                    | 6.45                                   |


### Test 4
##### Table 3: Wilcoxon Signed Rank Test Results for Original vs Personalised Explanation Ratings

| Question | Criterion | p-value  | Better Version  |
|----------|----------|----------|----------------|
| 1        | 1        | 0.6148   | Personalised   |
|          | 2        | 0.1987   | Personalised   |
|          | 3        | **0.0215** | **Personalised**   |
|          | 4        | 0.6559   | Personalised   |
|          | 5        | **0.0277** | **Personalised**   |
|          | 6        | 0.4537   | Personalised   |
| 2        | 1        | 0.1573   | Personalised   |
|          | 2        | 0.5271   | Personalised   |
|          | 3        | 0.1317   | Personalised   |
|          | 4        | **0.0017** | **Personalised**   |
|          | 5        | 0.0511   | Personalised   |
|          | 6        | **0.0129** | **Personalised**   |
| 3        | 1        | 0.5637   | Original       |
|          | 2        | 0.3951   | Personalised   |
|          | 3        | 0.2795   | Personalised   |
|          | 4        | 0.9521   | Original       |
|          | 5        | 0.1206   | Personalised   |
|          | 6        | 0.5839   | Personalised   |
| 4        | 1        | 0.7055   | Personalised   |
|          | 2        | 0.4487   | Original       |
|          | 3        | **0.0032** | **Personalised**   |
|          | 4        | **0.0013** | **Personalised**   |
|          | 5        | 0.1552   | Personalised   |
|          | 6        | 0.5881   | Personalised   |
| 5        | 1        | **0.0067** | **Personalised**   |
|          | 2        | 0.4142   | Personalised   |
|          | 3        | **0.0044** | **Personalised**   |
|          | 4        | **0.0009** | **Personalised**   |
|          | 5        | **0.0240** | **Personalised**   |
|          | 6        | **0.0049** | **Personalised**   |






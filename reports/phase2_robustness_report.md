# Phase 2: Model Robustness and Adversarial Testing

Generated (UTC): 2026-10-24T16:09:30.225187+00:00

## Objective
Evaluate the Phase 1 MNIST MLP under image perturbations and FGSM.

## Clean Baseline
- Test accuracy: 97.76%
- Test loss: 0.0782
- Correct predictions: 9776/10000

## Experiment Results

| Experiment | Condition | Accuracy | Loss | Accuracy drop (percentage points) |
|---|---|---:|---:|---:|
| Clean baseline | none | 97.76% | 0.0782 | 0.00 |
| Gaussian noise | sigma=0.1 | 96.13% | 0.1238 | 1.63 |
| Gaussian noise | sigma=0.2 | 86.22% | 0.4434 | 11.54 |
| Gaussian noise | sigma=0.3 | 65.66% | 1.2873 | 32.10 |
| Rotation | angle=-15 | 92.46% | 0.2816 | 5.30 |
| Rotation | angle=15 | 93.66% | 0.2328 | 4.10 |
| Rotation | angle=30 | 75.26% | 1.0357 | 22.50 |
| Brightness | factor=0.5 | 97.77% | 0.0925 | -0.01 |
| Brightness | factor=0.75 | 97.80% | 0.0745 | -0.04 |
| Brightness | factor=1.25 | 97.71% | 0.0814 | 0.05 |
| FGSM | epsilon=0.05 | 55.89% | 1.7717 | 41.87 |
| FGSM | epsilon=0.1 | 9.88% | 6.6495 | 87.88 |
| FGSM | epsilon=0.2 | 0.46% | 15.3325 | 97.30 |

## Artifacts
- `robustness_metrics.csv`
- `robustness_metrics.json`
- `robustness_accuracy_comparison.png`
- `robustness_examples.png`
- `phase2_clean_confusion_matrix.png`

## Limitations
- Results apply to the tested MNIST test set and perturbation strengths.
- Random noise results may vary between runs.
- FGSM results do not represent all possible adversarial attacks.
- The model was evaluated without adversarial retraining.
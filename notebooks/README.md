
# AI Quality Engineering: MNIST Digit Recognition

A hands-on AI Quality Engineering project that builds, evaluates, and progressively hardens a handwritten-digit recognition model.

## Project Objective

Build a baseline machine learning model and evaluate its quality using a structured workflow. Later phases will extend the project to robustness, adversarial testing, data drift, performance benchmarking, API security, automated testing, and monitoring.

## Phase 1: Baseline Model

### Dataset

- Dataset: MNIST handwritten digits
- Training samples: 54,000
- Validation samples: 6,000
- Test samples: 10,000
- Image dimensions: 28 × 28 pixels
- Classes: digits 0–9

The original 60,000 MNIST training samples were split into training and validation sets. The separate 10,000-image test set was reserved for final evaluation.

### Model Architecture

A fully connected neural network (MLP):

- Input: 784 features
- Hidden layer 1: 128 neurons with ReLU
- Hidden layer 2: 64 neurons with ReLU
- Dropout: 20%
- Output: 10 digit classes

### Training Configuration

- Framework: PyTorch
- Optimizer: Adam
- Learning rate: 0.001
- Loss function: CrossEntropyLoss
- Batch size: 128
- Epochs: 10
- Random seed: 42

### Baseline Results

| Metric | Result |
|---|---:|
| Test accuracy | 97.76% |
| Test loss | 0.0782 |
| Correct predictions | 9,776 / 10,000 |
| Incorrect predictions | 224 / 10,000 |
| Macro F1-score | 97.75% |

### Classification and Error Analysis

The classification report shows strong performance across all ten classes. Digit 7 had the lowest F1-score at 97.02%, followed by digit 8 at 97.18% and digit 2 at 97.26%.

Training loss continued to decrease during the ten epochs, while validation loss began to rise slightly in later epochs. This suggests possible mild overfitting and motivates future checkpoint selection and regularization experiments.

See `reports/baseline_confusion_matrix.png` for class-level prediction errors.

## Repository Structure

```text
ai-quality-engineering-mnist-digit-recognition-project/
├── notebooks/
│   └── phase1_mnist_baseline.ipynb
├── data/
├── models/
│   └── mnist_baseline.pth
├── reports/
│   ├── baseline_metrics.json
│   └── baseline_confusion_matrix.png
├── src/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Environment Setup

Python 3.11 is recommended.

Create and activate a virtual environment on Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Open `notebooks/phase1_mnist_baseline.ipynb` in VS Code and select the project's `.venv` Python kernel.

Run the notebook cells in order. The first dataset-loading run downloads MNIST.

## AI Quality Engineering Roadmap

- [x] Phase 1: Baseline training and quality evaluation
- [ ] Phase 2: Robustness, adversarial testing, and drift
- [ ] Phase 3: Performance benchmarking and quantization
- [ ] Phase 4: Prediction API, validation, authentication, and rate limiting
- [ ] Phase 5: Automated tests and continuous integration
- [ ] Phase 6: Monitoring, simulated canary/A-B testing, and rollback

## Current Limitations

- The current model is a baseline MLP, not a production deployment.
- Results reflect one training run and configuration.
- Robustness under distribution shift and adversarial perturbations has not yet been established.
- API security, performance, and deployment behavior will be evaluated in later phases.

## License

Choose an appropriate license before distributing or reusing this project.

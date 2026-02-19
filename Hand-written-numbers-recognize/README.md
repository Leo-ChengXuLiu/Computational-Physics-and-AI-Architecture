# 🧠 Deep Learning Architecture: CNN & MLP for Pattern Recognition

A foundational machine learning pipeline for training, evaluating, and deploying neural network architectures (MLP & CNN) for high-accuracy image classification.

## Architecture

```text
┌─────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────────────┐
│  MNIST Data │───▶│  Model Training  │───▶│ Saved Models │───▶│  Inference   │
│ (28x28 img) │    │  (Training.py)   │    │ (.keras/.h5) │    │ (Recognize)  │
└─────────────┘    └──────────────────┘    └──────────────┘    └──────────────┘
                             │                                         ▲
                             ▼                                         │
                    MLP vs. CNN Topologies                      User Input Image
```

**Pipeline:** Data Preprocessing → Model Compilation (Loss/Optimizer) → Training Epochs → Real-time Inference

## Modules

| File / Module | Purpose |
|---|---|
| `Training.py` | Core architecture script: dataset loading, tensor reshaping, and model training. |
| `Hand written recognize.py` | Independent inference engine: loads pre-trained weights to classify external images. |
| `my_mnist_model_conv.keras` | Saved weights for the **Convolutional Neural Network (CNN)**. |
| `my_mnist_model.keras` | Saved weights for the **Multi-Layer Perceptron (MLP)**. |
| `test_digit.png` | Sample input visual data for inference testing. |

## Prerequisites

- **Python 3.8+**
- TensorFlow & Keras
- NumPy
- OpenCV or PIL (for image matrix transformations)

## Setup & Execution

```bash
# 1. Install required dependencies
pip install tensorflow numpy opencv-python pillow

# 2. (Optional) Train the models from scratch
python Training.py

# 3. Run the inference engine on a target image
python "Hand written recognize.py"
```

## Skills Demonstrated

- **Neural Network Architecture** — Designed both dense feed-forward (MLP) and spatial-feature extraction (CNN) models.
- **Tensor Manipulation** — Handled multi-dimensional arrays and reshaped visual data for algorithmic processing.
- **Optimization & Deployment** — Managed backpropagation, loss functions, and decoupled model training from inference for production readiness.
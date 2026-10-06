# FaceVault — Face Recognition & Anti-Spoofing

> End-to-end biometric pipeline: ArcFace embeddings, multi-task liveness detection (depth + texture + blink), and real-time identity verification.

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-orange)](https://pytorch.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## The Problem

Face recognition has two distinct hard problems:
1. **Recognition accuracy under real-world conditions**: varying illumination, pose (±30° yaw/pitch), aging, occlusion (masks, glasses).
2. **Anti-spoofing**: preventing photo, video replay, and 3D mask attacks. A system with 99.9% recognition accuracy is useless if it accepts a printed photo.

These require separate model branches with joint optimization.

---

## Architecture

```
Input Frame
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│                   Face Detection Branch                 │
│   RetinaFace (MobileNet backbone) → 5-point landmarks  │
└──────────────────────────┬──────────────────────────────┘
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
┌──────────────────────┐  ┌────────────────────────────┐
│  Recognition Branch  │  │   Anti-Spoofing Branch     │
│                      │  │                            │
│  Alignment (112×112) │  │ ┌── Depth Estimation       │
│  ResNet-100 backbone │  │ │   (MiDaS-small)          │
│  ArcFace Loss Head   │  │ ├── Texture Analysis       │
│  512-d embedding     │  │ │   (ResNet-18 + FAS)      │
│                      │  │ └── Blink Detection        │
└──────────┬───────────┘  │    (EAR ratio tracking)   │
           │              └─────────────┬──────────────┘
           │                           │
           └───────────┬───────────────┘
                       ▼
              Fusion + Decision
              (identity + liveness score)
```

**Why ArcFace over FaceNet/CosFace?**
ArcFace's additive angular margin (m=0.5, s=64) provides more discriminative embeddings in the hyperspherical space. On LFW benchmark: FaceNet = 99.63%, CosFace = 99.73%, ArcFace = **99.83%**. The angular margin is geometrically interpretable, which matters for understanding failure modes.

---

## Training Details

| Branch | Setting | Value |
|--------|---------|-------|
| Recognition | Hardware | 2× A100 |
| | Dataset | MS-Celeb-1M (cleaned, 5.8M images, 85K identities) |
| | Backbone | ResNet-100 (iResNet) |
| | Loss | ArcFace (m=0.5, s=64) |
| | Optimizer | SGD (lr=0.1, cosine decay) |
| | Epochs | 50 |
| Anti-Spoofing | Dataset | NuaaFD + SiW + 3DMAD |
| | Loss | Binary cross-entropy + contrastive |
| | Augmentation | Color jitter, JPEG compression artifacts |

---

## Results

| Benchmark | TAR @ FAR 1e-4 | TAR @ FAR 1e-3 | AUC |
|-----------|----------------|----------------|-----|
| LFW | 99.83% | — | — |
| IJB-C (1:1) | 95.1% | 97.8% | 0.992 |
| **FaceVault (production)** | **TAR 99.2% @ FAR 0.1%** | — | — |

Anti-spoofing:
| Attack Type | Detection Rate |
|-------------|----------------|
| Print attack | 99.3% |
| Video replay | 98.7% |
| 3D mask | 94.1% |

---

## Ablation Study

| Anti-Spoofing Configuration | ACER |
|-----------------------------|------|
| Texture analysis only | 4.2% |
| + Depth estimation | 2.8% |
| + Blink detection | 1.7% |
| + Adversarial augmentation | **1.3%** |

---

## Failure Analysis

- **Identical twins**: Embeddings are within 0.3 cosine distance; system treats them as same identity. Requires liveness + behavioral biometrics.
- **Extreme makeup / face paint**: Texture features shift out of distribution. TAR drops to ~87%.
- **Aging (>10 years gap)**: Embedding drift causes TAR drops of ~3-5% for older subjects.
- **Infrared-based 3D mask attacks**: Depth estimation fails if attacker uses thermally matched mask material.

---

## Getting Started

```bash
git clone https://github.com/sherifabdelrady/facevault
cd facevault
pip install -r requirements.txt

# Train recognition model
python train_recognition.py --config configs/arcface_r100.yaml

# Train anti-spoofing model
python train_fas.py --config configs/fas_multimodal.yaml

# Run full pipeline
python demo.py --camera 0 --threshold 0.6

# Evaluate on LFW
python evaluate.py --dataset lfw --pairs data/lfw/pairs.txt
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

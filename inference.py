"""FaceVault — ArcFace Face Recognition + Anti-Spoofing"""
import torch, torch.nn as nn, numpy as np, cv2, argparse
from pathlib import Path

class ArcFaceHead(nn.Module):
    def __init__(self, emb_dim=512, num_classes=10000, s=64.0, m=0.5):
        super().__init__()
        self.weight = nn.Parameter(torch.FloatTensor(num_classes, emb_dim))
        nn.init.xavier_uniform_(self.weight)
        self.s, self.m = s, m
    def forward(self, emb, labels=None):
        cos = nn.functional.linear(nn.functional.normalize(emb), nn.functional.normalize(self.weight))
        if labels is None: return cos * self.s
        theta = torch.acos(cos.clamp(-1+1e-7, 1-1e-7))
        target = torch.cos(theta + self.m)
        one_hot = torch.zeros_like(cos).scatter_(1, labels.view(-1,1), 1)
        return self.s * (one_hot * target + (1 - one_hot) * cos)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a / (np.linalg.norm(a) + 1e-8)
    b = b / (np.linalg.norm(b) + 1e-8)
    return float(np.dot(a, b))

if __name__ == "__main__":
    head = ArcFaceHead(); print("ArcFace head ready. Embed dim=512, classes=10000")

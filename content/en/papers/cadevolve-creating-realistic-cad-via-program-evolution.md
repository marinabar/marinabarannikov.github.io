---
title: "CADEvolve: Creating Realistic CAD via Program Evolution"
date: 2026-02-18T09:54:57+00:00
build:
  render: false
  list: true
params:
  authors: "Maksim Elistratov, Marina Barannikov, Gregory Ivanov, Valentin Khrulkov, Anton Konushin, Andrey Kuznetsov, Dmitrii Zhemchuzhnikov"
  venue: "arXiv preprint"
  arxiv_id: "2602.16317"
  links:
    arxiv: "https://arxiv.org/abs/2602.16317"
    pdf: "https://arxiv.org/pdf/2602.16317"
  image: "papers/cadevolve-creating-realistic-cad-via-program-evolution.png"

---

Computer-Aided Design (CAD) delivers rapid, editable modeling for engineering and manufacturing. Recent AI progress now makes full automation feasible for various CAD tasks. However, progress is bottlenecked by data: public corpora mostly contain sketch-extrude sequences, lack complex operations, multi-operation composition and design intent, and thus hinder effective fine-tuning. Attempts to bypass this with frozen VLMs often yield simple or invalid programs due to limited 3D grounding in current foundation models. We present CADEvolve, an evolution-based pipeline and dataset that starts from simple primitives and, via VLM-guided edits and validations, incrementally grows CAD programs toward industrial-grade complexity. The result is 8k complex parts expressed as executable CadQuery parametric generators. After multi-stage post-processing and augmentation, we obtain a unified dataset of 1.3m scripts paired with rendered geometry and exercising the full CadQuery operation set. A VLM fine-tuned on CADEvolve achieves state-of-the-art results on the Image2CAD task across the DeepCAD, Fusion 360, and MCB benchmarks.

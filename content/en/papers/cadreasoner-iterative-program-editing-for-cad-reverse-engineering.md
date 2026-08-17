---
title: "CADReasoner: Iterative Program Editing for CAD Reverse Engineering"
date: 2026-02-18T10:27:29+00:00
build:
  render: false
  list: true
params:
  authors: "Soslan Kabisov, Vsevolod Kirichuk, Andrey Volkov, Gennadii Savrasov, Marina Barannikov, Anton Konushin, Andrey Kuznetsov, Dmitrii Zhemchuzhnikov"
  venue: "arXiv preprint"
  arxiv_id: "2603.29847"
  links:
    arxiv: "https://arxiv.org/abs/2603.29847"
    pdf: "https://arxiv.org/pdf/2603.29847"
  image: "papers/cadreasoner-iterative-program-editing-for-cad-reverse-engineering.png"

---

Computer-Aided Design (CAD) powers modern engineering, yet producing high-quality parts still demands substantial expert effort. Many AI systems tackle CAD reverse engineering, but most are single-pass and miss fine geometric details. In contrast, human engineers compare the input shape with the reconstruction and iteratively modify the design based on remaining discrepancies. Agent-based methods mimic this loop with frozen VLMs, but weak 3D grounding of current foundation models limits reliability and efficiency. We introduce CADReasoner, a model trained to iteratively refine its prediction using geometric discrepancy between the input and the predicted shape. The model outputs a runnable CadQuery Python program whose rendered mesh is fed back at the next step. CADReasoner fuses multi-view renders and point clouds as complementary modalities. To bridge the realism gap, we propose a scan-simulation protocol applied during both training and evaluation. Across DeepCAD, Fusion 360, and MCB benchmarks, CADReasoner attains state-of-the-art results on clean and scan-sim tracks.

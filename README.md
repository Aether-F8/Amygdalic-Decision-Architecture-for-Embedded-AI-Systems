# Amygdalic Decision Architecture for Embedded AI Systems

📄 **DOI:** https://doi.org/10.31224/6620

---

## Abstract

This repository is a research companion for the paper **"Amygdalic Decision Architecture for Embedded AI Systems"** by **S. Sudhakar**.  
The core idea is to design an embedded AI decision loop inspired by the *amygdala-like* function in biological systems: a fast, risk-aware gating layer that filters actions before execution.

In practical terms, the architecture separates:
1. **Proposal generation** (what the AI *wants* to do),
2. **Safety and feasibility checks** (what it is *allowed* to do under constraints), and
3. **Bounded action selection** (what it will *actually* do on-device).

This helps embedded systems remain responsive while avoiding unsafe or out-of-bounds behavior under tight compute, memory, and power budgets.

---

## Intuition (VERY IMPORTANT)

### What problem is being solved?
Embedded AI systems (robots, drones, edge controllers, automotive modules) must make decisions in real time, often with incomplete information and strict hardware limits. A raw AI policy may choose actions that are optimal in simulation but unsafe or infeasible in the field.

### Why existing methods fail
- **Pure end-to-end policies** may ignore hard operational limits (thermal, current, speed, safety zones).
- **Cloud-heavy decision pipelines** add latency and can fail when connectivity drops.
- **Post-hoc safety checks** can be too late in fast control loops.
- **Large models** are difficult to deploy on low-power edge hardware.

### What is the core innovation?
The paper’s central innovation is a **bounded, safety-aware decision architecture** where an amygdalic-like interlock constrains candidate actions before execution.

Think of it as:
- A planner says: *"These are possible actions."*
- An amygdalic safety gate says: *"These actions are forbidden right now."*
- A selector chooses the best action from the remaining safe set.

If nothing is safe, the system falls back to a pre-defined conservative behavior.

---

## Architecture Overview

### 1) Amygdalic decision system
The term **amygdalic** refers to a fast, protective decision layer analogous to reflexive threat screening. In engineering form, this is a lightweight safety interlock that runs inline with policy inference.

### 2) Embedded constraints
Action feasibility is bounded by real-world limits, e.g.:
- Actuator ranges (torque, speed, current)
- Power and thermal envelopes
- Geofencing / collision margins
- Timing deadlines and control-loop rates

### 3) Safety interlock concept
A typical flow:
1. Model proposes candidate actions with utility/confidence.
2. Constraint filter removes actions violating hard constraints.
3. Selector picks best safe action.
4. If no action is valid, trigger fallback (safe stop, degrade mode, hold state).

This supports deterministic behavior and reduces catastrophic action risk in embedded deployments.

---

## Applications

- **Embedded AI systems:** always-on control modules with strict latency budgets
- **Robotics:** mobile robots, manipulators, collaborative systems needing bounded motion policies
- **Edge devices:** smart sensors, autonomous edge controllers, low-power cyber-physical systems

---

## Repository Structure

```text
amygdalic-decision-architecture/
├── README.md                    # Project overview, concept summary, and usage
├── paper.pdf                    # Placeholder for the paper PDF (add manually)
├── citation.bib                 # BibTeX citation
├── code/
│   └── decision_model.py        # Starter bounded decision architecture skeleton
├── data/                        # Placeholder for datasets / logs / test traces
└── figures/                     # Placeholder for architecture diagrams and plots
```

---

## Future Work / Extensions

1. **Formal verification of safety filter** (SMT/model checking for constraint completeness).
2. **Learning-aware constraints** where bounds adapt with calibrated uncertainty.
3. **Multi-objective bounded selection** balancing safety, energy, and task utility.
4. **Hardware-aware co-design** (quantized models + real-time schedulability guarantees).
5. **Runtime assurance stack** combining anomaly detection with deterministic fallback policies.

---

## Citation

If you use this repository, cite:

```bibtex
@article{sudhakar2024amygdalic,
  title   = {Amygdalic Decision Architecture for Embedded AI Systems},
  author  = {Sudhakar, S.},
  year    = {2024},
  doi     = {10.31224/6620},
  url     = {https://doi.org/10.31224/6620}
}
```

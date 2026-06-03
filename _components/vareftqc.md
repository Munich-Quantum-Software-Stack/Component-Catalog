---
title: VarEFTQC
languages:
  - Python
frameworks:
  - PennyLane
  - OpenQASM
links:
  docs: https://github.com/nicomeyer96/vareftqc/blob/main/README.md
  github: https://github.com/nicomeyer96/vareftqc
maintainers:
  - Fraunhofer IIS (Quantum Compilation Group)
---

The VarEFTQC library implements a variational co-design pipeline that jointly learns noise-tailored
quantum error-correcting encodings and physical realizations of logical gate sets in the codespace.
It can construct non-additive codes that reduce information loss compared to established stabilizer
codes while searching for transversal or otherwise low-depth implementations of target gate sets.
This makes it particularly useful for discovering hardware-adapted gadgets in the early
fault-tolerant quantum computing regime.

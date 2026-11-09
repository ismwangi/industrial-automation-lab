# Industrial Automation Lab

A hands-on engineering portfolio documenting practical work and learning in industrial automation, PLC programming, control systems, and engineering simulation.

This repository contains self-directed demonstrations, experiments, and technical documentation. It is separate from any employer or customer projects; no confidential or proprietary material is included.

## Project 01 — Automatic Water Tank Level Control System

A simulated tank-level control system designed to demonstrate the engineering workflow from requirements to PLC logic, process simulation, and testing.

### Project components

- Functional description and sequence of operation
- Digital and analogue I/O mapping
- PLC control logic in IEC 61131-3 Structured Text (CODESYS-compatible)
- Python process and controller reference simulation
- Alarm handling for low, high, high-high, and instrument-fault conditions
- Automated Python tests for normal operation and selected fault conditions
- GitHub Actions workflow for repeatable Python checks

**Status:** Initial design documents, a PLC function block, a Python process/controller reference model, automated tests, and a GitHub Actions workflow are committed. The workflow is configured for Python 3.11 and 3.12, but its first hosted run has not yet been verified. The Structured Text has not yet been compiled in CODESYS.

## Repository structure

```text
industrial-automation-lab/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── docs/
│   ├── functional-description.md
│   └── io-mapping.md
├── plc/
│   └── FB_TankLevelControl.st
├── simulation/
│   ├── __init__.py
│   ├── README.md
│   └── tank_simulation.py
├── tests/
│   └── test_tank_simulation.py
└── README.md
```

## Tools and technologies

- CODESYS / IEC 61131-3 Structured Text — function block drafted; compilation not yet verified
- Python — process model, reference controller, and automated tests
- Control systems and instrumentation
- Git and GitHub for version control and documentation

## Automated checks

GitHub Actions is configured to run the Python unit tests on pushes and pull requests targeting `main`, using Python 3.11 and 3.12. It also runs the simulation script as a smoke test. Check the repository's Actions tab for the actual result of the first hosted run.

To run the checks locally from the repository root:

```bash
python -m unittest discover -s tests -v
python simulation/tank_simulation.py
```

## Engineering approach

Each project aims to document:

1. The problem and design requirements
2. The system architecture and I/O
3. The control strategy and implementation
4. Testing, observed results, and limitations
5. Possible improvements

## Disclaimer

Projects in this repository are educational and portfolio demonstrations. They are not certified for deployment in safety-critical or production environments. Any real-world implementation requires appropriate engineering review, risk assessment, and validation.

---

Maintained by [ismwangi](https://github.com/ismwangi).

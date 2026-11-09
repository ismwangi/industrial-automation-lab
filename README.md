# Industrial Automation Lab

A hands-on engineering portfolio documenting practical work and learning in industrial automation, PLC programming, control systems, and engineering simulation.

This repository will contain self-directed demonstrations, experiments, and technical documentation. It is separate from any employer or customer projects; no confidential or proprietary material is included.

## Project roadmap

### 1. Automatic Water Tank Level Control System

A simulated tank-level control system designed to demonstrate the engineering workflow from requirements to PLC logic and testing.

Planned deliverables:

- Functional description and sequence of operation
- Digital and analogue I/O list
- PLC control logic in IEC 61131-3 Structured Text (CODESYS-compatible)
- Python process simulation for tank filling and draining
- Alarm handling for low and high tank levels
- Test cases covering normal operation and fault conditions
- System architecture and HMI concept documentation

**Status:** Initial design documents, a PLC function block, a Python process/controller reference model, and automated test cases are committed. The Structured Text still needs compilation and testing in CODESYS. The committed Python test suite has not yet been run from a repository checkout.

## Repository structure

The structure will grow as the project is implemented. The initial target is:

```text
industrial-automation-lab/
├── docs/
│   ├── functional-description.md
│   └── io-mapping.md
├── plc/
│   └── tank_control.st
├── simulation/
│   └── tank_simulation.py
├── tests/
└── README.md
```

## Tools and technologies

- CODESYS / IEC 61131-3 Structured Text (PLC function block drafted; compilation not yet verified)
- Python
- Control systems and instrumentation
- Git and GitHub for version control and documentation

Tools will be listed as they are actually used in each project.

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

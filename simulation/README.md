# Tank Simulation

The dependency-free Python model contains a bounded tank process and a scan-based software reference model of the PLC control behavior.

## Run the demonstration
From the repository root:
```bash
python simulation/tank_simulation.py
```
The script prints CSV-formatted time, level, pump command, and high-high trip state.

## Run automated tests
```bash
python -m unittest discover -s tests -v
```

## Assumptions
- Tank level is 0–100%.
- Pump inflow is 8 percentage points per second.
- A constant outlet disturbance removes 1.5 percentage points per second.
- The transmitter maps 0–100% linearly to 4–20 mA.
- Rates are arbitrary demonstration values, not measured process data.

## Important distinction
The Python controller is a reference model, not an IEC 61131-3 runtime. Passing Python tests does not prove that the Structured Text compiles or behaves identically on a particular PLC. Compile and test the Structured Text in CODESYS separately.

Educational simulation only; never connect this model to real equipment.

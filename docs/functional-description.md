# Automatic Water Tank Level Control — Functional Description

**Project type:** Educational simulation  
**Status:** Initial design specification  
**Controller implementation:** Planned in CODESYS-compatible IEC 61131-3 Structured Text

## 1. Purpose

Design a small automatic water-filling system that maintains the level in a storage tank within an operator-configurable operating band. The project demonstrates requirements definition, I/O design, PLC sequencing, alarm handling, simulation, and testing.

This is a portfolio demonstration, not a design approved for real plant deployment.

## 2. Initial design assumptions

The first version uses the following deliberately simple process model:

- One tank with a simulated level range of 0–100%.
- One analogue level transmitter represented as a 4–20 mA signal.
- One inlet pump controlled by the PLC.
- One normally-closed inlet solenoid valve, energized to permit filling.
- One outlet valve represented as a process disturbance in the simulator (not PLC-controlled in version 1).
- Local Start and Stop commands.
- Auto and Manual operating modes.
- Low-level and high-level alarms.

These are project assumptions and can be revised as the design develops.

## 3. Automatic operating sequence

1. The operator selects Auto mode.
2. The operator issues Start.
3. The controller checks that the level signal is valid and that no stop or trip condition is active.
4. If the tank level is at or below the low setpoint, the controller starts the inlet pump and opens the inlet valve.
5. Filling continues until the level reaches or exceeds the high setpoint.
6. At the high setpoint, the pump stops and the inlet valve closes.
7. The system remains idle until the level falls to or below the low setpoint.
8. Stop command or an invalid level signal stops filling and closes the inlet valve.

The low and high setpoints create a control deadband to prevent rapid switching around one threshold.

## 4. Manual mode

In Manual mode, the operator may request the pump and inlet valve to run, subject to permissives and protective interlocks. The first software version will keep the same essential protections in both modes:

- Invalid analogue level signal prevents filling.
- High-high level condition stops filling.
- Stop command stops filling.

Manual mode is not intended to bypass protective functions.

## 5. Alarms and fault response

| Condition | Response |
|---|---|
| Low level | Indicate low-level alarm; normal automatic filling demand is generated |
| High level | Indicate high-level condition; stop filling at the high setpoint |
| High-high level | Stop pump and close inlet valve; latch alarm until acknowledged/reset conditions are satisfied |
| Invalid level signal | Stop filling and indicate instrument fault |
| Stop command | Stop pump and close inlet valve |

Alarm thresholds and reset behavior will be finalized alongside the PLC implementation and tests.

## 6. Operator interface concept

The planned HMI will show:

- Tank level as a numeric percentage and bar indicator
- Auto/Manual mode
- Start and Stop status
- Pump and inlet valve status
- Low, high, high-high, and instrument-fault indications
- Configurable low and high setpoints
- Alarm acknowledgement/reset controls

## 7. Items to validate during implementation

- Setpoint ordering and allowable ranges
- Analogue scaling and signal-failure detection
- Start/stop and mode-transition behavior
- High-high trip and reset conditions
- Pump/valve command consistency
- Simulation behavior at empty and full tank limits

## 8. Safety note

The simulation is for learning only. A real installation would require a site-specific hazard and risk assessment, correctly rated equipment, independent protection where required, fail-safe design, and qualified engineering review.

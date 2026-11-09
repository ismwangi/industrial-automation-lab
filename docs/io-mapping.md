# Automatic Water Tank Level Control — I/O Mapping

**Status:** Initial design proposal  
**Controller:** Generic PLC; final hardware addresses are not assigned.

The table describes logical signals. Physical channel numbers must be assigned only after a specific PLC and I/O module configuration is selected.

## 1. Digital inputs

| Tag | Type | Description | Normal interpretation |
|---|---|---|---|
| `DI_Start` | BOOL | Momentary start pushbutton | TRUE while pressed |
| `DI_Stop_OK` | BOOL | Stop circuit healthy | TRUE = healthy; FALSE = stop requested |
| `DI_AutoMode` | BOOL | Auto mode selector | TRUE = Auto; FALSE = Manual |
| `DI_ManualFill` | BOOL | Manual fill request | TRUE = request filling |
| `DI_AlarmReset` | BOOL | Alarm reset pushbutton | TRUE while pressed |

## 2. Analogue inputs

| Tag | Type | Description | Engineering range |
|---|---|---|---|
| `AI_TankLevel_mA` | REAL | Level transmitter current | 4–20 mA |
| `AI_TankLevel_pct` | REAL | Scaled tank level | 0–100% |

The transmitter is assumed to be linear: 4 mA represents 0% and 20 mA represents 100%. The PLC logic must detect out-of-range current before using the scaled value.

## 3. Digital outputs

| Tag | Type | Description | Energized state |
|---|---|---|---|
| `DO_InletPump` | BOOL | Inlet pump run command | TRUE = run request |
| `DO_InletValve` | BOOL | Inlet solenoid command | TRUE = open request |
| `DO_RunLamp` | BOOL | System running indication | TRUE = illuminated |
| `DO_AlarmLamp` | BOOL | Common alarm indication | TRUE = illuminated |

Output commands do not prove that a motor or valve physically operated. A real system would normally include suitable feedback signals and electrical protection.

## 4. Internal PLC variables

| Tag | Type | Purpose |
|---|---|---|
| `TankLevel_pct` | REAL | Validated scaled tank level |
| `LowSetpoint_pct` | REAL | Automatic fill start threshold |
| `HighSetpoint_pct` | REAL | Automatic fill stop threshold |
| `HighHighSetpoint_pct` | REAL | Independent software trip threshold |
| `SystemRunning` | BOOL | Run latch/state |
| `FillDemand` | BOOL | Automatic fill demand |
| `LevelSignalValid` | BOOL | Analogue signal health |
| `HighHighTrip` | BOOL | High-high trip state |

## 5. Initial setpoint proposal

| Parameter | Initial value |
|---|---:|
| Low setpoint | 30% |
| High setpoint | 80% |
| High-high threshold | 90% |

These are demonstration values, not process recommendations. The implementation must validate that the low setpoint is below the high setpoint and the high setpoint is below the high-high threshold.

## 6. Hardware allocation

No physical PLC addresses are assigned yet. Address allocation will depend on the selected controller, expansion modules, and wiring design. Keep symbolic tags separate from physical addresses so the program can be adapted to different hardware.

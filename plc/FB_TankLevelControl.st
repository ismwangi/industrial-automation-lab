FUNCTION_BLOCK FB_TankLevelControl
VAR_INPUT
    StartCmd             : BOOL;
    StopCircuitHealthy   : BOOL;   (* TRUE = stop circuit healthy *)
    AutoMode             : BOOL;   (* TRUE = automatic, FALSE = manual *)
    ManualFillCmd        : BOOL;
    AlarmResetCmd        : BOOL;
    LevelSignal_mA       : REAL;   (* 4–20 mA transmitter *)
    LowSetpoint_pct      : REAL := 30.0;
    HighSetpoint_pct     : REAL := 80.0;
    HighHighSetpoint_pct : REAL := 90.0;
END_VAR

VAR_OUTPUT
    TankLevel_pct       : REAL;
    LevelSignalValid    : BOOL;
    SystemRunning       : BOOL;
    FillDemand          : BOOL;
    HighHighTrip        : BOOL;
    LowLevelAlarm       : BOOL;
    HighLevelAlarm      : BOOL;
    InstrumentFault     : BOOL;
    PumpRunCmd          : BOOL;
    InletValveOpenCmd   : BOOL;
    CommonAlarm         : BOOL;
END_VAR

VAR
    RunLatch            : BOOL;
    SetpointsValid      : BOOL;
    FillRequest         : BOOL;
END_VAR

(* Validate transmitter signal before scaling. *)
LevelSignalValid := (LevelSignal_mA >= 3.6) AND (LevelSignal_mA <= 21.0);
InstrumentFault := NOT LevelSignalValid;

IF LevelSignalValid THEN
    TankLevel_pct := ((LevelSignal_mA - 4.0) / 16.0) * 100.0;

    (* Clamp small permitted under/over-range values to display limits. *)
    IF TankLevel_pct < 0.0 THEN
        TankLevel_pct := 0.0;
    ELSIF TankLevel_pct > 100.0 THEN
        TankLevel_pct := 100.0;
    END_IF;
ELSE
    TankLevel_pct := 0.0;
END_IF;

SetpointsValid :=
    (LowSetpoint_pct >= 0.0) AND
    (LowSetpoint_pct < HighSetpoint_pct) AND
    (HighSetpoint_pct < HighHighSetpoint_pct) AND
    (HighHighSetpoint_pct <= 100.0);

(* Start is latched; an unhealthy stop circuit always drops the latch. *)
IF NOT StopCircuitHealthy THEN
    RunLatch := FALSE;
ELSIF StartCmd THEN
    RunLatch := TRUE;
END_IF;

(* High-high trip is latched and requires a deliberate reset below
   the normal high setpoint, with a healthy signal and stop circuit. *)
IF LevelSignalValid AND (TankLevel_pct >= HighHighSetpoint_pct) THEN
    HighHighTrip := TRUE;
END_IF;

IF AlarmResetCmd AND LevelSignalValid AND StopCircuitHealthy
   AND (TankLevel_pct < HighSetpoint_pct) THEN
    HighHighTrip := FALSE;
END_IF;

LowLevelAlarm := LevelSignalValid AND (TankLevel_pct <= LowSetpoint_pct);
HighLevelAlarm := LevelSignalValid AND (TankLevel_pct >= HighSetpoint_pct);

SystemRunning := RunLatch AND StopCircuitHealthy;
FillRequest := FALSE;

IF SystemRunning AND LevelSignalValid AND SetpointsValid AND NOT HighHighTrip THEN
    FillDemand := FALSE;
    IF AutoMode THEN
        (* Hysteresis: start at/below low threshold; stop at/above high. *)
        IF TankLevel_pct <= LowSetpoint_pct THEN
            FillDemand := TRUE;
        ELSIF TankLevel_pct >= HighSetpoint_pct THEN
            FillDemand := FALSE;
        END_IF;
        FillRequest := FillDemand;
    ELSE
        FillRequest := ManualFillCmd;
    END_IF;
ELSE
    FillDemand := FALSE;
    FillRequest := FALSE;
END_IF;

(* Fail-closed command behavior for stop, bad signal, bad setpoints,
   or a latched high-high trip. *)
PumpRunCmd := FillRequest;
InletValveOpenCmd := FillRequest;
CommonAlarm := InstrumentFault OR HighHighTrip OR HighLevelAlarm;
END_FUNCTION_BLOCK

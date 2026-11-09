"""Educational water-tank process and control simulation."""
from dataclasses import dataclass

@dataclass
class ControllerInputs:
    start: bool = False
    stop_circuit_healthy: bool = True
    auto_mode: bool = True
    manual_fill: bool = False
    alarm_reset: bool = False
    level_signal_ma: float = 4.0
    low_setpoint_pct: float = 30.0
    high_setpoint_pct: float = 80.0
    high_high_setpoint_pct: float = 90.0

@dataclass
class ControllerOutputs:
    tank_level_pct: float = 0.0
    level_signal_valid: bool = False
    system_running: bool = False
    fill_demand: bool = False
    high_high_trip: bool = False
    low_level_alarm: bool = False
    high_level_alarm: bool = False
    instrument_fault: bool = True
    pump_run_cmd: bool = False
    inlet_valve_open_cmd: bool = False
    common_alarm: bool = True

class TankLevelController:
    """Scan-based software reference model of the PLC function block."""
    def __init__(self):
        self._run_latch = False
        self._fill_demand = False
        self._high_high_trip = False

    def scan(self, inputs: ControllerInputs) -> ControllerOutputs:
        valid = 3.6 <= inputs.level_signal_ma <= 21.0
        level = min(100.0, max(0.0, ((inputs.level_signal_ma - 4.0) / 16.0) * 100.0)) if valid else 0.0
        setpoints_valid = 0.0 <= inputs.low_setpoint_pct < inputs.high_setpoint_pct < inputs.high_high_setpoint_pct <= 100.0

        if not inputs.stop_circuit_healthy:
            self._run_latch = False
        elif inputs.start:
            self._run_latch = True

        if valid and level >= inputs.high_high_setpoint_pct:
            self._high_high_trip = True
        if inputs.alarm_reset and valid and inputs.stop_circuit_healthy and level < inputs.high_setpoint_pct:
            self._high_high_trip = False

        running = self._run_latch and inputs.stop_circuit_healthy
        fill = False
        if running and valid and setpoints_valid and not self._high_high_trip:
            if inputs.auto_mode:
                if level <= inputs.low_setpoint_pct:
                    self._fill_demand = True
                elif level >= inputs.high_setpoint_pct:
                    self._fill_demand = False
                fill = self._fill_demand
            else:
                self._fill_demand = False
                fill = inputs.manual_fill
        else:
            self._fill_demand = False

        low_alarm = valid and level <= inputs.low_setpoint_pct
        high_alarm = valid and level >= inputs.high_setpoint_pct
        fault = not valid
        return ControllerOutputs(
            tank_level_pct=level, level_signal_valid=valid, system_running=running,
            fill_demand=self._fill_demand, high_high_trip=self._high_high_trip,
            low_level_alarm=low_alarm, high_level_alarm=high_alarm,
            instrument_fault=fault, pump_run_cmd=fill,
            inlet_valve_open_cmd=fill,
            common_alarm=fault or self._high_high_trip or high_alarm,
        )

class TankProcess:
    """Simple bounded tank model with constant inflow and outlet disturbance."""
    def __init__(self, initial_level_pct=20.0, fill_rate_pct_s=8.0, drain_rate_pct_s=1.5):
        self.level_pct = float(initial_level_pct)
        self.fill_rate_pct_s = float(fill_rate_pct_s)
        self.drain_rate_pct_s = float(drain_rate_pct_s)

    @property
    def transmitter_current_ma(self):
        return 4.0 + (self.level_pct / 100.0) * 16.0

    def step(self, fill_command: bool, dt_s=0.1):
        if dt_s <= 0:
            raise ValueError("dt_s must be greater than zero")
        net_rate = (self.fill_rate_pct_s if fill_command else 0.0) - self.drain_rate_pct_s
        self.level_pct = min(100.0, max(0.0, self.level_pct + net_rate * dt_s))
        return self.level_pct

def run_demo(duration_s=60.0, dt_s=0.5):
    process, controller = TankProcess(), TankLevelController()
    print("time_s,level_pct,pump_cmd,high_high_trip")
    for index in range(int(duration_s / dt_s) + 1):
        time_s = index * dt_s
        inputs = ControllerInputs(start=(index == 0), level_signal_ma=process.transmitter_current_ma)
        outputs = controller.scan(inputs)
        print(f"{time_s:.1f},{process.level_pct:.2f},{int(outputs.pump_run_cmd)},{int(outputs.high_high_trip)}")
        process.step(outputs.pump_run_cmd, dt_s)

if __name__ == "__main__":
    run_demo()

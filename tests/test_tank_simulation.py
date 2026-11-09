import unittest
from simulation.tank_simulation import ControllerInputs, TankLevelController, TankProcess

def ma_for_level(level_pct):
    return 4.0 + level_pct / 100.0 * 16.0

class TankControllerTests(unittest.TestCase):
    def test_analogue_scaling(self):
        out = TankLevelController().scan(ControllerInputs(level_signal_ma=12.0))
        self.assertTrue(out.level_signal_valid)
        self.assertAlmostEqual(out.tank_level_pct, 50.0)

    def test_invalid_signal_stops_outputs(self):
        out = TankLevelController().scan(ControllerInputs(start=True, level_signal_ma=2.0))
        self.assertTrue(out.instrument_fault)
        self.assertFalse(out.pump_run_cmd)
        self.assertFalse(out.inlet_valve_open_cmd)

    def test_auto_fill_hysteresis(self):
        plc = TankLevelController()
        low = plc.scan(ControllerInputs(start=True, level_signal_ma=ma_for_level(25)))
        middle = plc.scan(ControllerInputs(level_signal_ma=ma_for_level(55)))
        high = plc.scan(ControllerInputs(level_signal_ma=ma_for_level(82)))
        self.assertTrue(low.pump_run_cmd)
        self.assertTrue(middle.pump_run_cmd)
        self.assertFalse(high.pump_run_cmd)

    def test_stop_circuit_drops_run_and_fill(self):
        plc = TankLevelController()
        plc.scan(ControllerInputs(start=True, level_signal_ma=ma_for_level(20)))
        out = plc.scan(ControllerInputs(stop_circuit_healthy=False, level_signal_ma=ma_for_level(20)))
        self.assertFalse(out.system_running)
        self.assertFalse(out.pump_run_cmd)

    def test_manual_fill_request(self):
        out = TankLevelController().scan(ControllerInputs(start=True, auto_mode=False, manual_fill=True, level_signal_ma=ma_for_level(50)))
        self.assertTrue(out.pump_run_cmd)

    def test_invalid_setpoints_inhibit_fill(self):
        out = TankLevelController().scan(ControllerInputs(start=True, low_setpoint_pct=80, high_setpoint_pct=30, high_high_setpoint_pct=90, level_signal_ma=ma_for_level(20)))
        self.assertFalse(out.pump_run_cmd)

    def test_high_high_trip_latches_and_resets(self):
        plc = TankLevelController()
        trip = plc.scan(ControllerInputs(start=True, level_signal_ma=ma_for_level(95)))
        self.assertTrue(trip.high_high_trip)
        self.assertFalse(trip.pump_run_cmd)
        held = plc.scan(ControllerInputs(level_signal_ma=ma_for_level(70)))
        self.assertTrue(held.high_high_trip)
        reset = plc.scan(ControllerInputs(alarm_reset=True, level_signal_ma=ma_for_level(70)))
        self.assertFalse(reset.high_high_trip)

    def test_trip_cannot_reset_above_high_setpoint(self):
        plc = TankLevelController()
        plc.scan(ControllerInputs(start=True, level_signal_ma=ma_for_level(95)))
        out = plc.scan(ControllerInputs(alarm_reset=True, level_signal_ma=ma_for_level(85)))
        self.assertTrue(out.high_high_trip)

    def test_process_level_is_bounded(self):
        process = TankProcess(initial_level_pct=99.0)
        process.step(True, 10.0)
        self.assertEqual(process.level_pct, 100.0)
        process = TankProcess(initial_level_pct=1.0)
        process.step(False, 10.0)
        self.assertEqual(process.level_pct, 0.0)

if __name__ == "__main__":
    unittest.main()

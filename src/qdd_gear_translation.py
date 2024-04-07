class gear_reduction:
    def __init__(self, gear_ratio, gear_efficiency = 0.98):
        self.gear_ratio = gear_ratio
        self.gear_efficiency = gear_efficiency

    def gear_translation(self, input_speed, input_torque):
        output_speed = input_speed / self.gear_ratio
        output_torque = input_torque * self.gear_ratio * self.gear_efficiency
        return output_speed, output_torque
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# NOTE: This code provides an example implementation of a Fuzzy Inference System (FIS) for illustrative purposes only.
class FuzzyControlSystem:
    def __init__(self):
        # Define input and output variables
        self.input_variable1 = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'Input Variable 1')
        self.input_variable2 = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'Input Variable 2')

        self.output_variable = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Output Variable')

        # Generate membership functions and rules
        self._generate_membership_functions()
        self._define_rules()
        self._create_control_system()

    def _generate_membership_functions(self):
        # Define membership functions for input variables
        self.input_variable1['low'] = fuzz.trapmf(self.input_variable1.universe, [0, 0, 0.3, 0.4])
        self.input_variable1['high'] = fuzz.trapmf(self.input_variable1.universe, [0.7, 0.9, 1, 1])

        self.input_variable2['low'] = fuzz.trapmf(self.input_variable1.universe, [0, 0.05, 0.10, 0.15])
        self.input_variable2['high'] = fuzz.trapmf(self.input_variable1.universe, [0.7, 0.9, 1, 1])

        # Define membership functions for output variable
        self.output_variable['low'] = fuzz.trapmf(self.output_variable.universe, [0, 0, 0.1, 0.2])
        self.output_variable['high'] = fuzz.trapmf(self.output_variable.universe, [0.8, 0.9, 1, 1])

    def _define_rules(self):
        # Define rules for the FIS
        rule1 = ctrl.Rule(self.input_variable1['low'] & self.input_variable2['low'], self.output_variable['low'])
        rule2 = ctrl.Rule(self.input_variable1['high'] & self.input_variable2['high'], self.output_variable['high'])
        rule3 = ctrl.Rule(self.input_variable1['low'] & self.input_variable2['high'], self.output_variable['low'])
        rule4 = ctrl.Rule(self.input_variable1['high'] & self.input_variable2['low'], self.output_variable['low'])

        # Combine rules
        self.rules = [rule1, rule2, rule3, rule4]


    def _create_control_system(self):
        # Create control system
        self.control_system = ctrl.ControlSystem(self.rules)

        # Create control system simulation
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    # Set input values and compute corresponding output value
    def set_input(self, input_value_1, input_value_2):
        # Set input variables and start computation
        self.simulation.input['Input Variable 1'] = input_value_1
        self.simulation.input['Input Variable 2'] = input_value_2
        self.simulation.compute()

        # Return computed output value
        return self.simulation.output['Output Variable']
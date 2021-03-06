from csvwriter import SaveData


class Conversions():
    '''
    We're going to use grams as the base unit for everything here.
    To get an amount dispensed, we first convert it to a weight if it's
    a volume, and then to grams to get the final amount we actually want
    '''

    MASS = {'g': 1.0, 'kg': 1000.0, 'lb': 453.592, 'oz': 28.3495}
    # the base unit for volumes will be 'ml', which we'll convert back
    # to weights using the density of the foods
    VOLUMES = {'ml': 1.0, 'cups': 240, 'pint': 472.176, 'quart': 946.353,
               'fl-oz': 29.5735, 'tbls': 14.7868}
    # testing densities, in g/ml
    DENSITIES = {'rice': 2.0, 'pasta': 0.35, 'water': 1.0}

    # testing prices, in dollars/g
    PRICES = {'rice': 0.01, 'pasta': 0.025, 'water': .001}

    def __init__(self):
        # nothing to actually do here
        raise Exception("Don't create this class")


class State():
    '''
    Holds the state for the gui
    '''
    def __init__(self):

        # static settings
        self.max_amount_desired = 9999

        # Already dispensed:
        self.amount_dispensed = 0.0

        # To be dispensed:
        self.amount_desired = 0.0

        # System state
        self.amount_requested = 0.0
        self.container_mass = 0.0

        # General settings
        self.selected_unit = next(iter(Conversions.MASS.keys()))
        self.selected_product = next(iter(Conversions.DENSITIES.keys()))
        self.weight_unit = next(iter(Conversions.MASS.keys()))
        self.volume_unit = next(iter(Conversions.VOLUMES.keys()))
        self.csv_filename = 'pid_data.csv'
        self.data_writer = SaveData(self.csv_filename)

        # Hardware things
        self.port = '/dev/ttyACM0'
        self.kp = 0.0095
        self.ki = 0.002
        self.kd = 0.0
        self.error_integral = 0
        self.prev_error = 0
        self.control_accuracy = 10  # in base units, g
        self.max_motor_cmd = 1.9
        self.refresh_period = 50  # ms

    def price_to_str(price):
        return '${:,.2f}'.format(price)

    def amnt_to_str(amnt):
        return '{:,.2f}'.format(amnt)

    def convert_units(self, amount):
        '''Get the value converted to the currently desired units'''
        if self.selected_unit in Conversions.VOLUMES:
            return amount \
                * Conversions.VOLUMES[self.selected_unit] \
                * Conversions.DENSITIES[self.selected_product]
        else:
            return amount / Conversions.MASS[self.selected_unit]

    def convert_to_base(self, amount):
        if self.selected_unit in Conversions.VOLUMES:
            return amount * Conversions.VOLUMES[self.selected_unit] \
                / Conversions.DENSITIES[self.selected_product]
        else:
            return amount * Conversions.MASS[self.selected_unit]

    def get_dispensed_amount(self):
        return State.amnt_to_str(self.convert_units(self.amount_dispensed))

    def get_desired_amount(self):
        return State.amnt_to_str(self.convert_units(self.amount_desired))

    def get_price(self, amount):
        return amount \
            * Conversions.PRICES[self.selected_product]

    def get_dispensed_price(self):
        return State.price_to_str(self.get_price(self.amount_dispensed))

    def get_desired_price(self):
        return State.price_to_str(self.get_price(self.amount_desired))

    def get_motor_feedback_command(self, error):
        self.error_integral += error*(self.refresh_period / 1000)
        error_deriv = (error - self.prev_error)/(self.refresh_period / 1000)
        motor_cmd = self.kp*error \
            + self.kd*error_deriv \
            + self.ki*(self.error_integral)
        self.prev_error = error
        final_cmd = min(motor_cmd, self.max_motor_cmd)
        self.data_writer.write_data([motor_cmd, final_cmd, error,
                                     self.error_integral,
                                     error_deriv,
                                     self.amount_requested,
                                     self.amount_dispensed
                                     - self.container_mass])
        return final_cmd

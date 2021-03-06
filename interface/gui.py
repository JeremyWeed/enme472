#! /usr/bin/env python3

import PySimpleGUI as sg
from model import Conversions as convs
from model import State
from comm import Comm
import time
from csvwriter import SaveData


# helpful color sites:
# https://sendwithses.gitbook.io/helpdocs/random-stuff/easy-to-remember-color-guide-for-non-designers
# https://www.sessions.edu/color-calculator/


class GUI():

    MAX_VALUE = 9999.99
    FONT = ('Mono', 15)
    GREEN = '#66ff99'
    RED = '#ff6666'
    TEXT_COLOR = '#1a2a3a'
    SCREEN_SIZE = (800, 480)
    # SCREEN_SIZE = (800, 800)
    # SCREEN_SIZE = (640, 480)
    LEFT_SIZE = (200, 480)
    RIGHT_SIZE = (SCREEN_SIZE[0] - LEFT_SIZE[0], SCREEN_SIZE[1] - LEFT_SIZE[1])
    BACKGROUND_COLOR = '#dddddd'
    BUTTON_COLOR = (TEXT_COLOR, '#6666ff')

    products = None
    numerals = set([str(x) for x in range(10)])

    def __init__(self):

        # State variables (these should probably be somewhere else)
        self.state = State()
        self.amount_val = 0
        self.dispensed_val = 0
        self.selected_unit = next(iter(convs.MASS.keys()))

        # gui elements
        self.amount = sg.Text('0.00', size=(8, 1), justification='right',
                              font=self.FONT)
        self.price = sg.Text('$0.00', size=(11, 1), justification='right',
                             font=self.FONT)
        self.units = sg.InputCombo(list(convs.MASS.keys()), font=self.FONT,
                                   default_value=self.state.selected_unit,
                                   size=(6, 1), change_submits=True,
                                   readonly=True)
        self.output = sg.Frame('Weight/Volume:', [[self.amount, self.units]],
                               background_color=self.BACKGROUND_COLOR)
        self.prices = sg.Frame('Estm. Price:', [[self.price]],
                               background_color=self.BACKGROUND_COLOR)
        self.input = sg.Frame('Enter Value:',
                              [[sg.Button(str(x), font=self.FONT)
                                for x in range(1, 4)],
                               [sg.Button(str(x), font=self.FONT)
                                for x in range(4, 7)],
                               [sg.Button(str(x), font=self.FONT)
                                for x in range(7, 10)],
                               [sg.Button('Clear', font=self.FONT),
                                sg.Button('0', size=(1, 1),
                                          font=self.FONT)]],
                              background_color=self.BACKGROUND_COLOR)
        self.right_side = sg.Column([[self.output],
                                     [self.prices],
                                     [self.input]],
                                    background_color=self.BACKGROUND_COLOR)
        self.product_buttons = [sg.Button(x, font=self.FONT)
                                for x in convs.DENSITIES.keys()]
        self.product_selector = sg.Frame('Select Product:',
                                         [self.product_buttons],
                                         background_color=self.BACKGROUND_COLOR)
        self.dispense_by = sg.Frame('Dispense by:',
                                    [[sg.Button('Weight', font=self.FONT),
                                      sg.Button('Volume', font=self.FONT)]],
                                    background_color=self.BACKGROUND_COLOR)
        self.actuate = sg.Column([[sg.Button(
            'Dispense',
            button_color=(self.TEXT_COLOR,
                          self.GREEN),
            font=self.FONT),
                                   sg.Button('Stop',
                                             button_color=(self.TEXT_COLOR,
                                                           self.RED),
                                             font=self.FONT),
                                   sg.Button('Tare', font=self.FONT)]],
                                 background_color=self.BACKGROUND_COLOR)
        self.debug_scale = sg.Text('VALUE', font=self.FONT)
        self.debug = sg.Frame('DEBUG', [[sg.Text('Scale:', font=self.FONT),
                                         self.debug_scale]],
                              background_color=self.BACKGROUND_COLOR)
        self.dispensed_amount = sg.Text('0.00', size=(7, 1),
                                        justification='right', font=self.FONT)
        self.dispensed_price = sg.Text('$0.00', font=self.FONT)
        self.dispensed_unit = sg.Text(self.selected_unit, font=self.FONT)
        self.dispensed = sg.Frame('', [[sg.Text('Dispensed:', font=self.FONT),
                                        self.dispensed_amount,
                                        self.dispensed_unit],
                                       [sg.Text('Final Price:',
                                                font=self.FONT),
                                        self.dispensed_price]],
                                  background_color=self.BACKGROUND_COLOR)
        self.left_side = sg.Column([[self.dispensed],
                                    [self.actuate],
                                    [self.dispense_by],
                                    [self.product_selector],
                                    [self.debug]],
                                   background_color=self.BACKGROUND_COLOR)
        self.layout = [[self.left_side,
                       self.right_side]]
        # sg.Frame('real-time controls',
        # [[sg.RealtimeButton('Dispense')]])
        self.arduino = Comm(self.state.port)

    def update_amount(self, value):
        self.amount.Update('{:,.2f}'.format(value))

    def update_price(self, price):
        self.price.Update('${:,.2f}'.format(price))

    def run(self):
        window = sg.Window('test', size=self.SCREEN_SIZE,
                           font=self.FONT,
                           button_color=self.BUTTON_COLOR,
                           background_color=self.BACKGROUND_COLOR,
                           ).Layout(self.layout).Finalize()
        while True:

            time.sleep(self.state.refresh_period/1000)
            button, values = window.Read(timeout=0)
            if button is None:
                break

            self.state.amount_dispensed = self.arduino.get_weight() \
                - self.state.container_mass
            self.debug_scale.Update('{:d}'
                                    .format(self.arduino.get_scale_raw()))
            if button != '__TIMEOUT__':
                if button == 0:
                    self.state.selected_unit = values[0]

                if button in self.numerals:
                    self.state.amount_desired = \
                        self.state.convert_to_base(
                            min(self.state.max_amount_desired,
                                self.state.convert_units(
                                    self.state.amount_desired)
                                * 10
                                + 0.01 * int(button)))

                elif button == 'Clear':
                    self.state.amount_desired = 0

                elif button == 'Tare':
                    self.state.container_mass = self.arduino.get_weight()

                elif button == 'Dispense':
                    self.state.amount_requested = self.state.amount_desired \
                        + self.state.amount_dispensed \
                        + self.state.container_mass
                    self.state.amount_desired = 0
                    self.state.error_integral = 0
                    self.trial_time = time.time()

                elif button == 'Stop':
                    self.state.amount_requested = 0
                    self.arduino.send_stop()

                elif button in convs.PRICES.keys():
                    self.state.selected_product = button

                elif button == 'Weight':
                    self.state.selected_unit = self.state.weight_unit
                    self.units.Update(values=list(convs.MASS.keys()))

                elif button == 'Volume':
                    self.state.selected_unit = self.state.volume_unit
                    self.units.Update(values=list(convs.VOLUMES.keys()))

                self.amount.Update(self.state.get_desired_amount())
                self.price.Update(self.state.get_desired_price())
                self.dispensed_unit.Update(self.state.selected_unit)
            self.dispensed_amount.Update(self.state.get_dispensed_amount())
            self.dispensed_price.Update(self.state.get_dispensed_price())

            if self.state.amount_requested > 0:
                error = self.state.amount_requested \
                    - self.state.amount_dispensed - self.state.container_mass
                print('error: {}'.format(error))
                print('requested: {}'.format(self.state.amount_requested))
                print('cont mass: {}'.format(self.state.container_mass))
                if error < self.state.control_accuracy or error < 0:
                    self.state.amount_requested = 0
                    self.arduino.send_stop()
                    print('Trial time: {}'.format(time.time() - self.trial_time))
                else:
                    motor_cmd = self.state.get_motor_feedback_command(error)
                    print('motor: {}'.format(motor_cmd))
                    self.arduino.send_speed(motor_cmd)
        window.Close()


if __name__ == '__main__':
    GUI().run()

#! /usr/bin/env python3

import PySimpleGUI as sg
from model import Conversions as convs
from model import State
from comm import Comm


# helpful color sites:
# https://sendwithses.gitbook.io/helpdocs/random-stuff/easy-to-remember-color-guide-for-non-designers
# https://www.sessions.edu/color-calculator/


class GUI():

    MAX_VALUE = 9999.99
    FONT = ('Mono', 15)
    GREEN = '#66ff99'
    RED = '#ff6666'
    TEXT_COLOR = '#1a2a3a'
    # SCREEN_SIZE = (800, 480)
    SCREEN_SIZE = (800, 800)
    REFRESH_PERIOD = 50  # ms
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
                                   default_value=self.selected_unit,
                                   size=(3, 1), change_submits=True,
                                   readonly=True)
        self.output = sg.Frame('Weight/Volume:', [[self.amount, self.units]])
        self.prices = sg.Frame('Estm. Price:', [[self.price]])
        self.input = sg.Frame('Enter Value:',
                              [[sg.Button(str(x), font=self.FONT)
                                for x in range(1, 4)],
                               [sg.Button(str(x), font=self.FONT)
                                for x in range(4, 7)],
                               [sg.Button(str(x), font=self.FONT)
                                for x in range(7, 10)],
                               [sg.Button('Clear', font=self.FONT),
                                sg.Button('0', size=(1, 1),
                                          font=self.FONT)]])
        self.right_side = sg.Column([[self.output],
                                     [self.prices],
                                     [self.input]])
        self.product_buttons = [sg.Button(x, font=self.FONT)
                                for x in convs.DENSITIES.keys()]
        self.product_selector = sg.Frame('Select Product:',
                                         [self.product_buttons])
        self.dispense_by = sg.Frame('Dispense by:',
                                    [[sg.Button('Weight', font=self.FONT),
                                      sg.Button('Volume', font=self.FONT)]])
        self.actuate = sg.Column([[sg.Button('Dispense',
                                             button_color=(self.TEXT_COLOR,
                                                           self.GREEN),
                                             font=self.FONT),
                                   sg.Button('Stop',
                                             button_color=(self.TEXT_COLOR,
                                                           self.RED),
                                             font=self.FONT)]])
        self.tare = sg.Button('tare', font=self.FONT)
        self.debug_scale = sg.Text('VALUE', font=self.FONT)
        self.debug = sg.Frame('DEBUG', [[sg.Text('Scale:', font=self.FONT),
                                         self.debug_scale]])
        self.dispensed_amount = sg.Text('0.00', size=(7, 1),
                                        justification='right', font=self.FONT)
        self.dispensed_price = sg.Text('$0.00', font=self.FONT)
        self.dispensed_unit = sg.Text(self.selected_unit, font=self.FONT)
        self.dispensed = sg.Frame('', [[sg.Text('Dispensed:', font=self.FONT),
                                        self.dispensed_amount,
                                        self.dispensed_unit],
                                       [sg.Text('Final Price:',
                                                font=self.FONT),
                                        self.dispensed_price]])
        self.left_side = sg.Column([[self.dispensed],
                                    [self.product_selector],
                                    [self.dispense_by],
                                    [self.tare],
                                    [self.actuate],
                                    [self.debug]])
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
                           button_color=self.BUTTON_COLOR
                           ).Layout(self.layout).Finalize()
        while True:
            button, value = window.Read(timeout=self.REFRESH_PERIOD)
            if button is None:
                break
            if button != '__TIMEOUT__':
                if button in self.numerals:
                    self.state.amount_desired = self.state.amount_desired * 10\
                        + 0.01 * int(button)
                    self.state.amount_desired = \
                        min(self.state.max_amount_desired,
                            self.state.amount_desired)
                elif button == 'Clear':
                    self.state.amount_desired = 0
                elif button == 'Tare':
                    pass
                elif button == 'Dispense':
                    pass
                elif button == 'Stop':
                    pass
                elif button in convs.PRICES.keys():
                    pass
                elif button == 'Enter':
                    self.dispensed_val += self.amount_val
                    self.amount_val = 0
                self.amount.Update(self.state.get_desired_amount())
                self.dispensed.Update(self.state.get_dispensed_amount())
                self.price.Update(self.state.get_desired_price())
                self.dispensed_price.Update(self.state.get_dispensed_price())
            self.debug_scale.Update('{:d}'
                                    .format(self.arduino.get_scale_raw()))

        window.Close()


if __name__ == '__main__':
    GUI().run()

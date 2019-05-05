#! /usr/bin/env python3

import PySimpleGUI as sg
from conversions import Conversions as convs

# helpful color sites:
# https://sendwithses.gitbook.io/helpdocs/random-stuff/easy-to-remember-color-guide-for-non-designers
# https://www.sessions.edu/color-calculator/


class GUI():

    MAX_VALUE = 9999.99
    FONT = ('Mono', 15)
    GREEN = '#66ff99'
    RED = '#ff6666'
    TEXT_COLOR = '#1a2a3a'

    products = None
    numerals = set([str(x) for x in range(10)])

    def __init__(self):

        # State variables (these should probably be somewhere else)
        self.amount_val = 0
        self.dispensed_val = 0

        # gui elements
        self.amount = sg.Text('0.00', size=(8, 1), justification='right',
                              font=self.FONT)
        self.dispensed = sg.Text('0.00', size=(7, 1),
                                 justification='right', font=self.FONT)
        self.price = sg.Text('$0.00', size=(11, 1), justification='right',
                             font=self.FONT)
        self.units = sg.InputCombo(list(convs.MASS.keys()), font=self.FONT,
                                   default_value=next(iter(convs.MASS.keys())))
        self.output = sg.Frame('Weight/Volume:', [[self.amount, self.units]])
        self.prices = sg.Frame('Price:', [[self.price]])
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
        self.left_side = sg.Column([[self.product_selector],
                                    [self.dispense_by],
                                    [self.actuate]])
        self.layout = [[self.left_side,
                       self.right_side]]
        # sg.Frame('real-time controls',
        # [[sg.RealtimeButton('Dispense')]])

    def update_amount(self, value):
        self.amount.Update('{:,.2f}'.format(value))

    def update_price(self, price):
        self.price.Update('${:,.2f}'.format(price))

    def run(self):
        window = sg.Window('test').Layout(self.layout).Finalize()
        while True:
            button, value = window.Read(timeout=10)
            if button is None:
                break
            if button != '__TIMEOUT__':
                if button in self.numerals:
                    self.amount_val = min(self.amount_val*10 + .01*int(button),
                                          self.MAX_VALUE)
                if button == 'Clear':
                    self.amount_val = 0
                if button == 'Enter':
                    self.dispensed_val += self.amount_val
                    self.amount_val = 0
                self.amount.Update('{:,.2f}'.format(self.amount_val))
                # self.dispensed.Update('{:,.2f}'.format(self.dispensed_val))
                print(self.amount_val)

        window.Close()


if __name__ == '__main__':
    GUI().run()

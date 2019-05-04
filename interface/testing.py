import PySimpleGUI as sg

# helpful color sites:
# https://sendwithses.gitbook.io/helpdocs/random-stuff/easy-to-remember-color-guide-for-non-designers
# https://www.sessions.edu/color-calculator/
MAX_VALUE = 9999.99
FONT = ('Mono', 15)

weight = sg.Text('weight', size=(10, 1), justification='right', font=FONT)
dispensed = sg.Text('Dispensed', size=(10, 1), justification='right',
                    font=FONT)
weight_val = 0
dispense = 0
numerals = set([str(x) for x in range(10)])
layout = [[sg.Text('Weight:'), weight,
           sg.Text('Amount Dispensed:'), dispensed],
          [sg.Frame('buttons',
                    [[sg.Button(str(x), font=FONT)
                      for x in range(1, 4)],
                     [sg.Button(str(x), font=FONT)
                      for x in range(4, 7)],
                     [sg.Button(str(x), font=FONT)
                      for x in range(7, 10)],
                     [sg.Button('Clear', font=FONT),
                      sg.Button('0', size=(1, 1), font=FONT)],
                     [sg.Button('Enter', font=FONT)]]),
          sg.Frame('real-time controls',
                   [[sg.RealtimeButton('Dispense')]])]]
window = sg.Window('test').Layout(layout).Finalize()
while True:
    button, value = window.Read(timeout=10)
    if button is None:
        break
    if button != '__TIMEOUT__':
        if button in numerals:
            weight_val = min(weight_val*10 + .01*int(button), MAX_VALUE)
        if button == 'Clear':
            weight_val = 0
        if button == 'Enter':
            dispense += weight_val
            weight_val = 0
        weight.Update('{:,.2f}'.format(weight_val))
        dispensed.Update('{:,.2f}'.format(dispense))
        print(weight_val)

window.Close()

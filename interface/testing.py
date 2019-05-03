import PySimpleGUIWx as sg

sg.ChangeLookAndFeel('')
layout = [[sg.Frame('buttons', [[sg.Button(str(x)) for x in range(1, 4)],
                                [sg.Button(str(x)) for x in range(4, 7)],
                                [sg.Button(str(x)) for x in range(7, 10)],
                                [sg.Button('0')]])]]
window = sg.Window('test').Layout(layout).Finalize()
while True:
    button, value = window.Read()
    print(button)

from imports import *

radio.set_group(1)      # the radio frequency we will be using, leave on 1
myID = 4                # The ID # given to you by the teacher
signalStrength = -999   # keeps track of the signal strength to let you know when you dont have a signal anymore
hasSignal = False       # this flag will be true when you are receiving a signal
wasFound = False        # this flag will be true when you have found the transmitter
showNum = False         # this flag with be true when displaying the signal strength as a number

# gets called when the device recieves a signal from the transmitter
# a signal is sent from the transmitter every 500ms
def on_received_number(receivedNumber):
    global hasSignal, signalStrength, wasFound
    # the transmitter will send a 0 every 500ms
    if radio.received_number == 0:
        hasSignal = True
        signalStrength = radio.received_packet(RadioPacketProperty.SIGNAL_STRENGTH)
    # the transmitter will echo back your ID when it records it as found
    elif receivedNumber == myID:
        wasFound = True
radio.on_received_number(on_received_number)

# for debugging, will display the signal strength value
def on_button_pressed_a():
    global showNum
    showNum = not showNum
input.on_button_pressed(Button.A, on_button_pressed_a)

# transmit your ID to the transmitter
def on_button_pressed_b():
    global myID
    radio.send_number(myID)
input.on_button_pressed(Button.B, on_button_pressed_b)

# draws the bar graph and signal lost / winner icons
def drawScreen():
    if wasFound:
        basic.show_icon(IconNames.HAPPY)
    elif signalStrength == -999:
        basic.show_icon(IconNames.NO)
    elif showNum:
        basic.show_number(signalStrength)
    else:
        led.plot_bar_graph(Math.map(signalStrength, -128, -28, 0, 9), 9)

# heartbeat, checks that we still have a signal, otherwise will display that we lost it
def on_every_interval():
    global hasSignal, signalStrength
    if hasSignal:
        hasSignal = False
    else:
        signalStrength = -999
loops.every_interval(1000, on_every_interval)

def on_forever():
    DrawScreen()
basic.forever(on_forever)

import usb_cdc
import board
import analogio

knob1 = analogio.AnalogIn(board.A0)
knob2 = analogio.AnalogIn(board.A1)

while True:
    # wait for data from
    usb_cdc.data.readline()
    msg = f"{knob1},{knob2}\n"
    usb_cdc.data.write(msg.encode())

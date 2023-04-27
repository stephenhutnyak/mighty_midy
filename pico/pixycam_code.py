from pixycam import PixyCam
import usb_cdc

camera = PixyCam()

while True:
    # wait for data from
    usb_cdc.data.readline()
    blocks = camera.getBlocks(1)
    if len(blocks) == 0:
        msg = f"-1,-1\n"
    else:
        block = blocks[0]

        msg = f"{block.x},{block.y}\n"
    usb_cdc.data.write(msg.encode())

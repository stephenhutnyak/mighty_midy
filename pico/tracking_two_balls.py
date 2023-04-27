from pixycam import PixyCam
import usb_cdc

camera = PixyCam()

while True:
    # wait for data from
    usb_cdc.data.readline()
    red_blocks = camera.getBlocks(1)
    blue_blocks = camera.getBlocks(2)

    if len(red_blocks) == 0:
        red_x, red_y = -1, -1
    if len(blue_blocks) == 0:
        blue_x, blue_y = -1, -1
    if len(red_blocks) != 0:
        red_ball = red_blocks[0]
        red_x, red_y = red_ball.x, red_ball.y
    if len(blue_blocks) != 0:
        blue_ball = blue_blocks[0]
        blue_x, blue_y = blue_ball.x, blue_ball.y

    msg = f"{red_x},{red_y},{blue_x},{blue_y}\n"
    usb_cdc.data.write(msg.encode())
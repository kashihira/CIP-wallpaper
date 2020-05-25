"""
Final project:
Objective: create custom background wallpaper with QR code which provide introduction url.

milestone0: Select the original wallpaper, position of QR code and configuration file for QR code
milestone1: show the original background wallpaper image
milestone2: read information from configuration file and create the QR Code
    the first line of configuration file is url or e-mail you want to introduce to others.
milestone3: paste the QR code onto wallpaper at desired position which you select in advance
ToDo: adjust the position of QR code by moving the mouse, and release the key of mouse to fix and save.

"""
import qrcode
from simpleimage import SimpleImage
import time
import os

CONF_FILE = 'conf.txt'
TEMP_FILE = 'qr_temp.jpg'
OUTPUT_FILE = 'wallpaper.jpg'
DEFAULT_WALLPAPER = 'finalProject.png'
DEBUG_MODE = False


def main():
    # initialization: delete qr_temp.jpg and wallpaper.jpg if existed
    init()
    # input the background wallpaper
    fn = input_wallpaper()
    # input the position option for pasted QR code
    pos = input_position()
    # load background wallpaper image
    back_img = SimpleImage(fn)
    if DEBUG_MODE:
        print("Back: width= " + str(back_img.width) + " Height= " + str(back_img.height))
    # create QR code
    ver = adjust_size(back_img.height)
    cfn = input('Please select a QR code configuration file: ')
    back_img.show()
    time.sleep(1/2)
    create_qrcode(ver, cfn)
    time.sleep(1/5)
    qr_img = SimpleImage(TEMP_FILE)
    qr_img.show()
    if DEBUG_MODE:
        print("QR: width= " + str(qr_img.width) + " Height= " + str(qr_img.height))
    # paste QR code onto the position user select on wallpaper
    paste_qrcode(pos, qr_img, back_img)
    # show the custom wallpaper
    back_img.show()
    # save new wallpaper in local
    back_img.pil_image.save(OUTPUT_FILE)


def input_wallpaper():
    """
    input the background wallpaper
    """
    fn = input('Please select a background wallpaper: ')
    if fn == '':
        print('    Use the default background wallpaper.')
        fn = DEFAULT_WALLPAPER
    else:
        if os.path.exists(fn) is False:
            print('    wallpaper file is not existed, use the default background wallpaper')
            fn = DEFAULT_WALLPAPER
    return fn


def input_position():
    """
    input the position option for pasted QR code
    """
    option = input('Please select the position (1:left-top, 2:right-top, 3:left-bottom, 4:right-bottom) for QR code: ')
    if option == '':
        pos = 1
        print('    Use the default position, option 1: left-top on background.')
    else:
        pos = int(option)
    if pos > 4 or pos < 1:
        pos = 1
    return pos


def adjust_size(back_height):
    """
    adjust scale(version) for QR code to 1-40.

    Parameters
    ------
    back_height: int
      height of background wallpaper
    """
    ver = int(back_height/300+0.5)
    if ver == 0:
        ver += 1
    elif ver > 39:
        ver = 39
    return ver


def paste_qrcode(pos, qr_img, back_img):
    """
    paste the QR code onto the background.

    Parameters
    ------
    pos: int
      option number for the position which QR code will be pasted
    qr_img: SimpleImage
      image for QR Code
    back_img: SimpleImage
      image for background

    Returns
    ------
    back_img will be modified
    """
    back_width = back_img.width
    back_height = back_img.height
    qr_width = qr_img.width
    qr_height = qr_img.height
    dw = back_width - qr_width
    dh = back_height - qr_height
    for x in range(qr_width):
        for y in range(qr_height):
            pixel = qr_img.get_pixel(x, y)
            if pos == 1:
                x1 = x
                y1 = y
                back_img.set_pixel(x1, y1, pixel)
            elif pos == 2:
                x1 = x + dw
                y1 = y
                back_img.set_pixel(x1, y1, pixel)
            elif pos == 3:
                x1 = x
                y1 = y + dh
                back_img.set_pixel(x1, y1, pixel)
            elif pos == 4:
                x1 = x + dw
                y1 = y + dh
                back_img.set_pixel(x1, y1, pixel)


def init():
    """delete the temporary file and old output file if exists"""
    delete_file(TEMP_FILE)
    delete_file(OUTPUT_FILE)


def delete_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except OSError:
            pass


def create_qrcode(ver, fn):
    """
    read url info from configuration file

    Parameters
    ------
    ver: int
      version parameter for qrcode library. we use this to adjust the size of QR code image along the size of wallpaper.
    fn: str
      filename of configuration file.
    """
    if fn == '':
        print('    Use the default configuration file.')
        fn = CONF_FILE
    if os.path.exists(fn) is False:
        print('    Configuration file is not existed, use the default configuration.')
        fn = CONF_FILE
    conf_list = []
    for line in open(fn):
        line = line.strip()
        conf_list.append(line)
    if DEBUG_MODE:
        print('    QR code:' + conf_list[0])
    # we need to adjust size of QR code depend on the height of wallpaper
    if DEBUG_MODE:
        print('qr version = ' + str(ver))
    bsize = 2
    if ver == 2:
        bsize = 3
    elif ver > 2:
        bsize = 2*(ver-1)
    qr = qrcode.QRCode(
        version=ver,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=bsize,
        border=8
    )
    # create the QR code from info read from conf.txt,
    qr.add_data(conf_list[0])
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(TEMP_FILE)


if __name__ == '__main__':
    main()

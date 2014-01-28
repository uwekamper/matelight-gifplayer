#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import socket
import colorsys # for HSV-to-RGB-conversion
from PIL import Image, GifImagePlugin, ImageSequence, ImageOps
import time
import sys

# UDP_IP = "10.0.0.200"
UDP_PORT = 1337

ROWS = 16
COLS = 40

BRIGHTNESS = 1.0
GAMMA = 2.0
    
def send_array(data, hostname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (hostname, UDP_PORT))

def prepare_message(data, unpack=False):
    """Prepares the pixel data for transmission over UDP
    """
    # 4 bytes for future use as a crc32 checksum in network byte order.
    checksum = bytearray([0,0,0,0])
    data_as_bytes = bytearray()
    if unpack:
        for r, g, b, a in data:
            r = int(((r/255.0) ** GAMMA) * 255)
            g = int(((g/255.0) ** GAMMA) * 255)
            b = int(((b/255.0) ** GAMMA) * 255)
            data_as_bytes += bytearray([r,g,b])
    else:
        data_as_bytes = bytearray(data)
        
    while len(data_as_bytes) < 1920:
        data_as_bytes += bytearray([0,0,0])
    
    message = data_as_bytes + checksum
    return message

def make_gradient(hue):
    """This creates a gradient for on hue value.
    """
    array = []
    num_pixels = ROWS * COLS
    step_size = 255.0 / float(num_pixels)
    for i in range(num_pixels):
        h = float(hue) / 360.0
        s = 1.0
        v = (i * step_size) / 255.0
        color = int(i * step_size)
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        r = r ** GAMMA
        g = g ** GAMMA
        b = b ** GAMMA
        array += [int(r * 255 * BRIGHTNESS), int(g * 255 * BRIGHTNESS), int(b * 255 * BRIGHTNESS)]
    return array
    
def cycle_hue():
    """Cycles through all possible hue values and send it to the Mate 
    Light
    """
    for hue in range(360):
        data = make_gradient(hue)
        message = prepare_message(data)
        send_array(message)
        
def show_gif(filename, hostname):
    img = Image.open(filename)
    palette = img.getpalette()
    last_frame = Image.new("RGBA", img.size)
    frames = []

    for frame in ImageSequence.Iterator(img):
        #This works around a known bug in Pillow
        #See also: http://stackoverflow.com/questions/4904940/python-converting-gif-frames-to-png
        frame.putpalette(palette)
        c = frame.convert("RGBA")
        sleep_time = img.info['duration'] / 1000.0

        if  'transparency' in img.info and img.info['background'] != img.info['transparency']:
            last_frame.paste(c, c)
        else:
            last_frame = c

        tw = 40
        th = 16
        im = last_frame.copy()
        if (tw, th) != (None, None):
            im = ImageOps.fit(im, (tw, th), Image.ANTIALIAS)
            #im.thumbnail((tw, th), Image.NEAREST)
        data=list(im.getdata())
        message = prepare_message(data, unpack=True)
        send_array(message, hostname)     
        time.sleep(sleep_time)   
        # data = np.array(im.getdata(), dtype=np.uint8)
            
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
    	print "Usage: mategif.py HOSTNAME/IPADDRESS FILENAME"
    else:
        hostname = sys.argv[1]
        filename = sys.argv[2]
        print "Transmitting '%s' to %s (press Ctrl+C to abort) ..." % (filename, hostname)
        try:
            while True:
                show_gif(filename, hostname)
        except KeyboardInterrupt:
            print " Goodbye!"
    

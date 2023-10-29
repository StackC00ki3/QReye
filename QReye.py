#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from PIL import Image


def banner():
    banner = """
   ███████    ███████                           
  ██░░░░░██  ░██░░░░██           ██   ██        
 ██     ░░██ ░██   ░██   █████  ░░██ ██   █████ 
░██      ░██ ░███████   ██░░░██  ░░███   ██░░░██
░██    ██░██ ░██░░░██  ░███████   ░██   ░███████
░░██  ░░ ██  ░██  ░░██ ░██░░░░    ██    ░██░░░░ 
 ░░███████ ██░██   ░░██░░██████  ██     ░░██████
  ░░░░░░░ ░░ ░░     ░░  ░░░░░░  ░░       ░░░░░░    v0.1
    """
    print(banner + "\n\t\tpython QReye.py -h [FOR HELP]\n")


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]


def QReye(file):
    broken_qr = Image.open(file)
    eye = Image.open("eye.png")

    pix = broken_qr.load()

    width, height = broken_qr.size

    qr_min_x = width
    qr_min_y = height

    qr_max_x = 0
    qr_max_y = 0

    WHITE = (255, 255, 255, 255)

    widths = {}

    for y in range(height):
        bw = 0

        for x in range(width):
            if pix[x, y] != WHITE:
                if bw != 0:
                    if bw in widths.keys():
                        widths[bw] += 1

                    else:
                        widths[bw] = 1

                bw = 0

                # (r,g,b,a) = pix[x, y]

                # print(r, g, b,a)
                qr_min_x = min(qr_min_x, x)
                qr_min_y = min(qr_min_y, y)
                qr_max_x = max(qr_max_x, x)
                qr_max_y = max(qr_max_y, y)

            else:
                bw += 1

    print(f"QR code start pos: ({qr_min_x}, {qr_min_y})")
    print(f"QR code end pos: ({qr_max_x}, {qr_max_y})")

    module_gap = get_key(widths, max(widths.values()))[0]
    print(f"module gap: {module_gap} pixels")

    # Eye's width and height
    eye_height = 0
    eye_width = 0

    if pix[qr_min_x, qr_min_y] == WHITE:
        print("[+] Fixing the missing eye in upper left corner")
        x = qr_min_x
        y = qr_min_y
        while pix[x + 1, y + 1] == WHITE:
            x += 1
            y += 1
        eye_width = x - module_gap - qr_min_x
        eye_height = y - module_gap - qr_min_y
        broken_qr.paste(eye.resize((eye_width, eye_height)), (qr_min_x, qr_min_y))
        # img.paste(finder_pattern.resize((module_distance*7,module_distance*7)),(qr_min_x,qr_min_y))
        # img.show()

    if pix[qr_min_x, qr_max_y] == WHITE:
        print("[+] Fixing the missing eye in lower left corner")
        if eye_width == 0 or eye_height == 0:
            x = qr_min_x
            y = qr_max_y
            while pix[x + 1, y - 1] == WHITE:
                x += 1
                y -= 1
            eye_width = x - module_gap - qr_min_x
            eye_height = qr_max_y - y - module_gap
        broken_qr.paste(
            eye.resize((eye_width, eye_height)), (qr_min_x, qr_max_y - eye_height)
        )
        # img.show()

    if pix[qr_max_x, qr_min_y] == WHITE:
        print("[+] Fixing the missing eye in upper right corner")
        if eye_width == 0 or eye_height == 0:
            x = qr_max_x
            y = qr_min_y
            while pix[x - 1, y - 1] == WHITE:
                x -= 1
                y -= 1
            eye_width = qr_max_x - x - module_gap
            eye_height = y - module_gap - qr_min_y
        broken_qr.paste(
            eye.resize((eye_width, eye_height)), (qr_max_x - eye_width, qr_min_y)
        )
        # img.show()

    # Check whether the detection position is broken
    if eye_width != 0 and eye_height != 0:
        if pix[qr_min_x + eye_width / 2, qr_min_y + eye_height / 2] == WHITE:
            print("[*] Fixing the broken eye in upper left corner")
            broken_qr.paste(eye.resize((eye_width, eye_height)), (qr_min_x, qr_min_y))
        if pix[qr_min_x + eye_width / 2, qr_max_y - eye_height / 2] == WHITE:
            print("[*] Fixing the broken eye in lower left corner")
            broken_qr.paste(
                eye.resize((eye_width, eye_height)), (qr_min_x, qr_max_y - eye_height)
            )
        if pix[qr_max_x - eye_width / 2, qr_min_y + eye_height / 2] == WHITE:
            print("[*] Fixing the broken eye in upper right corner")
            broken_qr.paste(
                eye.resize((eye_width, eye_height)), (qr_max_x - eye_width, qr_min_y)
            )

    # Render fixed qr code
    print("[X] Rendering the fixed QR code")
    broken_qr.show()


if __name__ == "__main__":
    banner()

    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", type=str, help="QR image file to fix")
    args = parser.parse_args()
    if args.FILE:
        QReye(args.FILE)

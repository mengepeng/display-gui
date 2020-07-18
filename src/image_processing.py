#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import cv2

def get_base_path(relative):
    base_path = os.path.abspath("..")
    return os.path.join(base_path, relative)


def get_image_path(filename):
    return get_base_path(os.path.join('resource', filename))


def processing_image(img):
    # here is just a simple example
    img_res = cv2.putText(img, "@mengepeng", (100, 100),
                          cv2.FONT_HERSHEY_SIMPLEX,
                          2.0, (0, 0, 255), 5, cv2.LINE_AA, False)

    return img_res


# ########## test ##########
if __name__ == '__main__':
    img_path = get_image_path('image1.jpg')
    print(img_path)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    image = cv2.imread(img_path)
    image_res = processing_image(image)
    cv2.imshow('image', image_res)
    while (cv2.waitKey(1) & 0xFF) != 27:
        if cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) <= 0:
            break
    cv2.destroyAllWindows()

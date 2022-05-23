#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from gluon import *


def NextSequence(str):
    
    if not str: return str

    def shiftChar(str, ind, charset):
        c = str[ind]
        i = charset.find(c)
        if i == len(charset)-1:
            new_c = charset[0]
        else:
            new_c = charset[i+1]
        return f"{str[:len(str)+ind:]}{new_c}{str[ind+1:] if ind < -1 else ''}"
    
    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    
    ind = -1
    # cur_char = str[ind]
    at_end = True
    while at_end and (abs(ind) <= len(str)):
        cur_char = str[ind]
        if cur_char in ascii_lowercase:
            str = shiftChar(str, ind, ascii_lowercase)
        else:
            if cur_char in ascii_uppercase:
                str = shiftChar(str, ind, ascii_uppercase)
            else:
                if cur_char in digits:
                    str = shiftChar(str, ind, digits)
        at_end = cur_char in 'zZ9'
        ind -= 1
    return str
    
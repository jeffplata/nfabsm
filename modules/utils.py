#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from gluon import *


def NextSequence(s):
    
    if not s: return s

    def shiftChar(s, ind, charset):
        c = s[ind]
        i = charset.find(c)
        if i == len(charset)-1:
            new_c = charset[0]
        else:
            new_c = charset[i+1]
        return f"{s[:len(s)+ind:]}{new_c}{s[ind+1:] if ind < -1 else ''}"
    
    ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    
    ind = -1
    # cur_char = s[ind]
    at_end = True
    while at_end and (abs(ind) <= len(s)):
        cur_char = s[ind]
        if cur_char in ascii_lowercase:
            s = shiftChar(s, ind, ascii_lowercase)
        else:
            if cur_char in ascii_uppercase:
                s = shiftChar(s, ind, ascii_uppercase)
            else:
                if cur_char in digits:
                    s = shiftChar(s, ind, digits)
        at_end = cur_char in 'zZ9'
        ind -= 1
    return s
    
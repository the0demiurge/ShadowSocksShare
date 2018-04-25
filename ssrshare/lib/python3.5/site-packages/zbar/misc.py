'''
This file contains some useful barcode converter, and checksum calculation.

UPC-A checksum calculation
conversions:
    EAN-8 to EAN13
    UPC-E to UPC-A.

Written by Rounak Singh
'''

import numpy

def rgb2gray(rgb):
    '''
        converts rgb to grayscale image
        rgb is of type numpy.ndarray
    '''
    return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.114]).astype(numpy.uint8)

def upca_to_ean13(upca):
    '''
    Takes unicode UPC-A.
    Returns unicode EAN-13
    '''
    # Check length and type of ean8
    if len(upca)!=12:
        raise ValueError("full UPC-A should be of length 12")
    else:
        try:
            upca=int(upca)
        except ValueError:
            raise ValueError('UPC-A should be numerical digits')
    return '{0:013d}'.format(upca)

def ean8_to_ean13(ean8):
    '''
    Takes unicode EAN-8.
    Returns unicode EAN-13
    '''
    # Check length and type of ean8
    if len(ean8)!=8:
        raise ValueError("EAN-8 should be of length 8")
    else:
        try:
            ean8=int(ean8)
        except ValueError:
            raise ValueError('EAN-8 should be numerical digits')
    return '{0:013d}'.format(ean8)


def _upca_checksum(digits):
    odd_digits = digits[0::2]
    even_digits = digits[1::2]
    return (sum(odd_digits)*3 + sum(even_digits)) % 10

def upca_get_check_digit(upca):
    '''
    calculates the checksum of upca
    UPC-A code must be passed as str.
    Check Digit is returned as int.
    Error: returns None
    '''

    # return a list of digits from a number
    try:
        digits = list(map(int, upca))
    except ValueError:
        raise ValueError("UPC-A should be numerical digits")
    if len(digits) == 12:
        digits = digits[:-1]
    elif len(digits) != 11:
        raise ValueError("UPC-A should be of length 11 (without optional check digit)")

    checksum = _upca_checksum(digits)
    check_digit = 0 if checksum == 0 else 10 - checksum
    return check_digit

def upca_is_valid(upca):
    '''
    verifies that the checksum of full upca (12 digits) is valid.
    UPC-A must be passed as str
    return type is Boolean
    '''

    if len(upca) != 12:
        raise ValueError("UPC-A should be of length 12 (with check digit)")
    try:
        digits = list(map(int, upca))
    except ValueError:
        raise ValueError("UPC-A should be numerical digits")
    checksum = _upca_checksum(digits)
    return checksum == 0

def upce_2_upca(upc_e):
    '''
    This function converts a UPC-E code into UPC-A
    UPC-E must be passed as str.
    UPC-A is returned as str
    if any error then None is returned.
    Ref:
    http://www.taltech.com/barcodesoftware/symbologies/upc
    http://stackoverflow.com/questions/31539005/how-to-convert-a-upc-e-barcode-to-a-upc-a-barcode

    '''

    # converting to strings
    upc_e=str(upc_e)

    # Checking if the barcodes have numbers only
    try:
        int(upc_e)
    except ValueError:
        raise ValueError("UPC-E should be numerical digits")
    # If the first digit of UPC-E is not 0
    if upc_e[0] != '0':
        raise ValueError("First digit of UPC-E should be zero")

    upc_a='0'+upc_e[1]+upc_e[2]
    zeros='0000'

    if upc_e[6] == '0' or upc_e[6] == '1' or upc_e[6] == '2':
        upc_a+=upc_e[6]+zeros+upc_e[3:-2]
    elif upc_e[6]== '3':
        upc_a+=upc_e[3]+zeros+'0'+upc_e[4:-2]
    elif upc_e[6]== '4':
        upc_a+=upc_e[3:5]+zeros+'0'+upc_e[5]
    else:
        upc_a+=upc_e[3:6]+zeros+upc_e[6]

    # Add checksum digit
    upc_a+=upc_e[-1]

    # verify UPC-E code if valid using Checksum
    if upca_is_valid(upc_a):
        return upc_a
    else:
        msg='UPC-E is invalid. Please verify the checksum digit. \nValid checksum digit = '+upca_get_check_digit(upc_a) + \
            '\nSo, valid UPC-A is '+ upc_a[:-1] + upca_get_check_digit(upc_a)
        raise ValueError(msg)


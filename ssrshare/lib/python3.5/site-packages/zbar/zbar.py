# The MIT License (MIT)
#
# Copyright (c) 2014-2015 WUSTL ZPLAB
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Authors: Zach Pincus

import ctypes
import numpy
import sys
import os.path
import glob
import collections

__all__ = ['ZBAR_SYMBOLS', 'ZBAR_CONFIGS', 'Scanner', 'Symbol']


def load_zbar():
    if sys.platform == 'win32':
        loader = ctypes.windll
        functype = ctypes.WINFUNCTYPE
    else:
        loader = ctypes.cdll
        functype = ctypes.CFUNCTYPE

    zbar = None
    errors = []
    possible_zbar_libs = glob.glob(os.path.join(os.path.dirname(__file__), '_zbar.*'))
    for lib in possible_zbar_libs:
        try:
            zbar = loader.LoadLibrary(lib)
            break
        except Exception:
            # Get exception instance in Python 2.x/3.x compatible manner
            e_type, e_value, e_tb = sys.exc_info()
            del e_tb
            errors.append((lib, e_value))

    if zbar is None:
        if errors:
            # No zbar library loaded, and load-errors reported for some
            # candidate libs
            err_txt = ['%s:\n%s' % (l, str(e.args[0])) for l, e in errors]
            raise RuntimeError('One or more zbar libraries were found, but '
                               'could not be loaded due to the following errors:\n'
                               '\n\n'.join(err_txt))
        else:
            # No errors, because no potential libraries found at all!
            raise RuntimeError('Could not find a zbar library in ' + __file__)

    return zbar

_ZB = load_zbar()

API = {
    'zbar_image_scanner_create': (ctypes.c_void_p, ()),
    'zbar_image_scanner_destroy': (None, (ctypes.c_void_p,)),
    'zbar_image_scanner_set_config': (None, (ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_int)),
    'zbar_scan_image': (ctypes.c_int, (ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p)),
    'zbar_image_scanner_first_symbol': (ctypes.c_void_p, (ctypes.c_void_p,)),
    'zbar_symbol_next': (ctypes.c_void_p, (ctypes.c_void_p,)),
    'zbar_symbol_get_type': (ctypes.c_uint, (ctypes.c_void_p,)),
    'zbar_get_symbol_name': (ctypes.c_char_p, (ctypes.c_uint,)),
    'zbar_symbol_get_data': (ctypes.c_void_p, (ctypes.c_void_p,)),
    'zbar_symbol_get_data_length': (ctypes.c_uint, (ctypes.c_void_p,)),
    'zbar_symbol_get_quality': (ctypes.c_int, (ctypes.c_void_p,)),
    'zbar_symbol_get_loc_size': (ctypes.c_uint, (ctypes.c_void_p,)),
    'zbar_symbol_get_loc_x': (ctypes.c_int, (ctypes.c_void_p, ctypes.c_uint)),
    'zbar_symbol_get_loc_y': (ctypes.c_int, (ctypes.c_void_p,ctypes.c_uint)),
    }

def register_api(lib, api):
    for f, (restype, argtypes) in api.items():
        func = getattr(lib, f)
        func.restype = restype
        func.argtypes = argtypes

register_api(_ZB, API)

ZBAR_SYMBOLS = {
    'ZBAR_NONE'        :      0, # /**< no symbol decoded */
    'ZBAR_PARTIAL'     :      1, # /**< intermediate status */
    'ZBAR_EAN8'        :      8, # /**< EAN-8 */
    'ZBAR_UPCE'        :      9, # /**< UPC-E */
    'ZBAR_ISBN10'      :     10, # /**< ISBN-10 (from EAN-13). @since 0.4 */
    'ZBAR_UPCA'        :     12, # /**< UPC-A */
    'ZBAR_EAN13'       :     13, # /**< EAN-13 */
    'ZBAR_ISBN13'      :     14, # /**< ISBN-13 (from EAN-13). @since 0.4 */
    'ZBAR_I25'         :     25, # /**< Interleaved 2 of 5. @since 0.4 */
    'ZBAR_CODE39'      :     39, # /**< Code 39. @since 0.4 */
    'ZBAR_PDF417'      :     57, # /**< PDF417. @since 0.6 */
    'ZBAR_QRCODE'      :     64, # /**< QR Code. @since 0.10 */
    'ZBAR_CODE128'     :    128, # /**< Code 128 */
    'ZBAR_SYMBOL'      : 0x00ff, # /**< mask for base symbol type */
    'ZBAR_ADDON2'      : 0x0200, # /**< 2-digit add-on flag */
    'ZBAR_ADDON5'      : 0x0500, # /**< 5-digit add-on flag */
    'ZBAR_ADDON'       : 0x0700, # /**< add-on flag mask */
}

ZBAR_CONFIGS = {
    'ZBAR_CFG_ENABLE':     0,       #/**< enable symbology/feature */
    'ZBAR_CFG_ADD_CHECK':  1,       #/**< enable check digit when optional */
    'ZBAR_CFG_EMIT_CHECK': 2,       #/**< return check digit when present */
    'ZBAR_CFG_ASCII':      3,       #/**< enable full ASCII character set */
    'ZBAR_CFG_NUM':        4,       #/**< number of boolean decoder configs */
    'ZBAR_CFG_MIN_LEN':  0x20,      #/**< minimum data length for valid decode */
    'ZBAR_CFG_MAX_LEN':  0x21,      #/**< maximum data length for valid decode */
    'ZBAR_CFG_POSITION': 0x80,      #/**< enable scanner to collect position data */
    'ZBAR_CFG_X_DENSITY':0x100,     #/**< image scanner vertical scan density */
    'ZBAR_CFG_Y_DENSITY':0x101,     #/**< image scanner horizontal scan density */
}


Symbol = collections.namedtuple('Symbol', ['type', 'data', 'quality', 'position'])

class Scanner(object):
    def __init__(self, config=None):
        """Create a barcode-scanner object.

        By default, scanning for all barcode types is enabled, and reporting of
        their locations is enabled. This can be controlled by the config parameter.

        Parameters:
            config: None or a list of (symbol_type, config_type, value) triples.
                * symbol_type must be one of ZBAR_SYMBOLS, which refers to a
                  class of barcodes. ZBAR_NONE will cause the configuration
                  option to apply to all barcode types.
                * config_type must be one of ZBAR_CONFIGS, defined in zbar.h.
                  Of particular interest are ZBAR_CFG_ENABLE (enable specific
                  symbol type), ZBAR_CFG_ADD_CHECK (enable check-digit
                  verification) and ZBAR_CFG_MIN_LEN and ZBAR_CFG_MAX_LEN (only
                  return decoded barcodes with the specified data length).
                  NB: Enabling/disabling specific barcode types is complex and
                  not particularly well supported by zbar (some barcode types
                  will be scanned-for by default unless disabled; some require
                  specific enablement; some types like ISBN and UPC that are
                  subclasses of EAN barcodes require EAN to also be enabled).
                  Thus is is STRONGLY recommended to use the default config
                  and filter for barcode types after the fact.
                * value should be 1 for boolean options, or an integer for the
                  other options.
        """
        self._scanner = _ZB.zbar_image_scanner_create()
        if config is None:
            config = [('ZBAR_NONE', 'ZBAR_CFG_ENABLE', 1), ('ZBAR_NONE', 'ZBAR_CFG_POSITION', 1)]

        for symbol_type, config_type, value in config:
            _ZB.zbar_image_scanner_set_config(self._scanner, ZBAR_SYMBOLS[symbol_type], ZBAR_CONFIGS[config_type], value)

    def __del__(self):
        _ZB.zbar_image_scanner_destroy(self._scanner)
        del self._scanner

    def scan(self, image):
        """Scan an image and return a list of barcodes identified.

        Parameters:
            image: must be a 2-dimensional numpy array of dtype uint8.

        Returns: list of Symbol namedtuples.

        Each Symbol has 'type', 'data', 'quality', and 'position' attributes.
            * 'type' refers to the barcode's type (e.g. 'QR-Code')
            * 'data' is a bytes instance containing the barcode payload
            * 'quality' is a numerical score
            * 'position' is either an empty list (if position recording was
               disabled), or a list of (x, y) indices into the image that define
               the barcode's location.
        """
        image = numpy.asarray(image)
        if not image.dtype == numpy.uint8 and image.ndim == 2:
            raise ValueError('Image must be 2D uint8 type')
        if image.flags.c_contiguous:
            height, width = image.shape
        else:
            image = numpy.asfortranarray(image)
            width, height = image.shape
        num_symbols = _ZB.zbar_scan_image(self._scanner, width, height, image.ctypes.data)
        symbols = []
        symbol = _ZB.zbar_image_scanner_first_symbol(self._scanner)
        while(symbol):
            sym_type = _ZB.zbar_symbol_get_type(symbol)
            sym_name = _ZB.zbar_get_symbol_name(sym_type).decode('ascii')
            sym_data_ptr = _ZB.zbar_symbol_get_data(symbol)
            sym_data_len = _ZB.zbar_symbol_get_data_length(symbol)
            sym_data = ctypes.string_at(sym_data_ptr, sym_data_len)
            sym_quality = _ZB.zbar_symbol_get_quality(symbol)
            sym_loc = []
            for i in range(_ZB.zbar_symbol_get_loc_size(symbol)):
                x = _ZB.zbar_symbol_get_loc_x(symbol, i)
                y = _ZB.zbar_symbol_get_loc_y(symbol, i)
                sym_loc.append((x, y))
            symbols.append(Symbol(sym_name, sym_data, sym_quality, sym_loc))
            symbol = _ZB.zbar_symbol_next(symbol)
        assert len(symbols) == num_symbols
        return symbols

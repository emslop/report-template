#!/usr/bin/env python3
"""Restore the illustrative PNG; do not compile the presentation."""
from pathlib import Path
import base64
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]

def restore():
    source = ROOT / 'images' / 'example-system.png.b64'
    target = ROOT / 'images' / 'example-system.png'
    data = base64.b64decode(''.join(source.read_text(encoding='ascii').split()), validate=True)
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Invalid PNG signature')
    offset = 8
    complete = False
    while offset < len(data):
        size = struct.unpack_from('>I', data, offset)[0]
        end = offset + 8 + size
        kind = data[offset + 4:offset + 8]
        crc = struct.unpack_from('>I', data, end)[0]
        if (zlib.crc32(data[offset + 4:end]) & 0xffffffff) != crc:
            raise ValueError('PNG checksum mismatch')
        offset = end + 4
        if kind == b'IEND':
            complete = True
            break
    if not complete or offset != len(data):
        raise ValueError('Incomplete PNG')
    target.write_bytes(data)

if __name__ == '__main__':
    restore()

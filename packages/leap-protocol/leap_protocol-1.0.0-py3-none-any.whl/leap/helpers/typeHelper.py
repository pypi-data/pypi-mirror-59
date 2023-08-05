import struct


def encode_types(item, typeof):
  if typeof == "u8":
    return "{:02x}".format(clamp(item, 0x00, 0xff))
  elif typeof == "u16":
    return "{:04x}".format(clamp(item, 0x0000, 0xffff))
  elif typeof == "u32":
    return "{:08x}".format(clamp(item, 0x00000000, 0xffffffff))
  elif typeof == "u64":
    return "{:016x}".format(clamp(item, 0x0000000000000000, 0xffffffffffffffff))
  if typeof == "i8":
    item = clamp(item, -0x80, 0x7F)
    return "{:02x}".format(item + 0x100 if item < 0 else item)
  elif typeof == "i16":
    item = clamp(item, -0x8000, 0x7FFF)
    return "{:04x}".format(item + 0x10000 if item < 0 else item)
  elif typeof == "i32":
    item = clamp(item, -0x80000000, 0x7FFFFFFF)
    return "{:08x}".format(item + 0x100000000 if item < 0 else item)
  elif typeof == "i64":
    item = clamp(item, -0x8000000000000000, 0x7FFFFFFFFFFFFFFF)
    return "{:016x}".format(item + 0x10000000000000000 if item < 0 else item)
  elif typeof == "string":
    return item
  elif typeof == "bool":
    return "1" if item == True else "0"
  elif typeof == "float":
    return ''.join(format(x, '02x') for x in struct.pack('>f', item))
  elif typeof == "double":
    return ''.join(format(x, '02x') for x in struct.pack('>d', item))
  elif isinstance(typeof, list):
    if item in typeof:
      x = typeof.index(item)
      return "{:02x}".format(clamp(x, 0x00, 0xff))
    else:
      return ""
  else:
    return ""

def decode_unsigned(item, bits):
  try:
    return clamp(int(item, 16), 0, (0x1 << bits) - 1)
  except:
    return 0

def decode_signed(item, bits):
  try:
    value = int(item, 16)
    min_value = 0x1 << (bits - 1)
    if value > min_value:
      value -= 0x1 << (bits)

    return clamp(value, -min_value, min_value -1)
  except:
    return 0

def decode_types(item, typeof):
  if typeof == "u8":
    return decode_unsigned(item, 8)
  elif typeof == "u16":
    return decode_unsigned(item, 16)
  elif typeof == "u32":
    return decode_unsigned(item, 32)
  elif typeof == "u64":
    return decode_unsigned(item, 64)
  if typeof == "i8":
    return decode_signed(item, 8)
  elif typeof == "i16":
    return decode_signed(item, 16)
  elif typeof == "i32":
    return decode_signed(item, 32)
  elif typeof == "i64":
    return decode_signed(item,64)
  elif typeof == "string":
    return item
  elif typeof == "bool":
    return True if item == "1" else False
  elif typeof == "float":
    [x] = struct.unpack('>f', bytearray.fromhex(item))
    return x
  elif typeof == "double":
    [x] = struct.unpack('>d', bytearray.fromhex(item))
    return x
  elif isinstance(typeof, list):
    x = decode_unsigned(item, 8)
    if x < len(typeof):
      return typeof[x]
    else:
      return None
  else:
    return None

def clamp(value, min_value, max_value):
  return max(min_value, min(value, max_value))


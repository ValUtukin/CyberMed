def str_to_bytearray(hex_string):
    # Split the string (1e 0c 35 etc.) into a list of hex values [1e, 0c, 35, etc.]
    hex_values = hex_string.split()
    # Convert each hex value back to its original byte representation using fromhex()
    bytes_list = [bytes.fromhex(hex_value) for hex_value in hex_values]
    # Concatenate the byte values into a single bytearray
    original_bytearray = bytearray().join(bytes_list)
    return original_bytearray


data = bytearray([31, 13, 43, 45, 67])

appended_str = " ".join(format(x, '02x') for x in data)
print(f"Hex str: {appended_str}")
byte_seq = str_to_bytearray(appended_str)
print(" ".join(format(x, '02x') for x in byte_seq))



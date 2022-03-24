# return block pt
from sympy import jacobi

def char_to_int(byte_pt):
    pt_value = []
    for char in byte_pt:
        pt_value.append(ord(char))
    return pt_value

# return plaintext bytes
#def ciphertext_to_plainvalue(ct_text):
#    return [ord(char) for char in ct_text]

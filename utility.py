# return block pt
from sympy import jacobi

def plaintext_to_blockvalue(byte_pt):
    pt_value = []
    for char in byte_pt:
        pt_value.append(str(ord(char)))
    return pt_value

# return plaintext bytes
def block_to_plaintext(char_ct):
    pt_result = ""
    for value in char_ct:
        pt_result += chr(value)
    return pt_result

if __name__ == "__main__":
    f = open("test.txt", "rb")
    pt = f.read()
    f.close()
    plaintext_to_blockvalue(pt, 10)

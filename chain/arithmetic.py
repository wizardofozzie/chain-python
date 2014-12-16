def get_code_string(base):
    if base == 2: return '01'
    elif base == 10: return '0123456789'
    elif base == 16: return "0123456789abcdef"
    elif base == 58: return "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    elif base == 256: return ''.join([chr(x) for x in range(256)])
    else: raise ValueError("Invalid base!")

def encode(val,base,minlen=0):
    code_string = get_code_string(base)
    result = ""    
    while val > 0:
        result = code_string[val % base] + result
        val /= base
    if len(result) < minlen:
        result = code_string[0]*(minlen-len(result))+result
    return result

def decode(string,base):
    code_string = get_code_string(base)
    result = 0
    if base == 16: string = string.lower()
    while len(string) > 0:
        result *= base
        result += code_string.find(string[0])
        string = string[1:]
    return result

def changebase(string,frm,to,minlen=0):
    return encode(decode(string,frm),to,minlen)

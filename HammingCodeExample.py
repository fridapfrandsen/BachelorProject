import random

def HammingAdd(d):
    r = []
    i = 0
    while (pow(2, i) < (d + len(r))): 
        r.append(pow(2, i))
        i += 1
    return r

def HammingRemove(n):
    r = []
    i= 0
    while (pow(2, i) < (n)): 
        r.append(pow(2, i))
        i += 1
    return r


def InsertParityBits(message):
    length = len(message)
    code = message
    hamming_list = HammingAdd(length)
    for i in range(0, len(hamming_list)):
        code.insert(hamming_list[i] - 1, 0)
    return code



def CalculateParityBits(code):
    code = InsertParityBits(code)
    result = 0
    for i in range(0, len(code)):
        if code[i] == 1:
            result = result ^ (i+1)
    bin_resultat = bin(result)[2:]
    parity_chek_len = len(bin_resultat)
    for j in range(0,parity_chek_len):
        code[pow(2,j)-1]=int(bin_resultat[parity_chek_len-j-1])
    return code

def MakeError(code):
    error_location = random.randint(0, len(code) - 1)
    code[error_location] = (code[error_location] + 1) % 2
    return code

def Decode(code):
    result = 0
    for i in range(0, len(code)):
        if code[i]==1:
            result = result ^ (i+1)
    if result == 0:
        return code
    else:
        code[result-1]= (code[result-1]+1)%2
        return code

def RemoveParityBits(code):
    length = len(code)
    message = code
    hamming_list = HammingRemove(length)
    for i in range(0, len(hamming_list)):
        message.pop(hamming_list[len(hamming_list) - i - 1] - 1)
    return message





message = [0, 1, 1, 1]
print("Send message: ", message)

encoded = CalculateParityBits(message)
print("Encoded code: ", encoded)

code_with_error = MakeError(encoded)
print("Received code: ", code_with_error)

decoded = Decode(code_with_error)
print("Decoded code: ", decoded)

final_message = RemoveParityBits(decoded)
print("Received message: ", final_message)


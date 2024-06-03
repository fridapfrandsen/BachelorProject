from HammingCodeSevenFour import *

hamming74 = HammingCodeSevenFour()
message = "0011"
encoded = hamming74.Encode(message)
codeword_with_error = hamming74.MakeError(encoded)
decoded = hamming74.Decode(codeword_with_error)




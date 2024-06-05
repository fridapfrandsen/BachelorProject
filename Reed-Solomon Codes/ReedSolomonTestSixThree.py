from ReedSolomonPrimeField import *

RS_6_3 = ReedSolomonPrimeField(6, 3, 3)
message = [6, 2, 5]
encoded_message = RS_6_3.EncodeMessage(message)
error_codeword = RS_6_3.MakeError(encoded_message)
decoded_message = RS_6_3.DecodeMessage(error_codeword)
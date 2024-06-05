from ReedSolomonPrimeField import *

RS_10_5 = ReedSolomonPrimeField(10, 5, 2)
message = [1, 0, 1, 1, 0]
encoded_message = RS_10_5.EncodeMessage(message)
error_codeword = RS_10_5.MakeError(encoded_message)
decoded_message = RS_10_5.DecodeMessage(error_codeword)
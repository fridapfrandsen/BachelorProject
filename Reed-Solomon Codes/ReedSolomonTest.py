from ReedSolomonPrimeField import *

RS_7_3 = ReedSolomonPrimeField(7, 3, 3)
message = [6, 2, 5]
encoded_message = RS_7_3.EncodeMessage(message)
error_codeword = RS_7_3.MakeError(encoded_message)
decoded_message = RS_7_3.DecodeMessage(error_codeword)

# RS_11_5 = ReedSolomonPrimeField(11, 5, 2)
# message = [3, 4, 7, 0, 1]
# encoded_message = RS_11_5.EncodeMessage(message)
# error_codeword = [4, 0, 2, 3, 9, 7, 6, 3, 0, 0]
# # error_codeword = RS_11_5.MakeError(encoded_message)
# decoded_message = RS_11_5.DecodeMessage(error_codeword)


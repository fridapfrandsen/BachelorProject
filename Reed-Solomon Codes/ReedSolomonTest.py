from ReedSolomonPrimeField import *
import random

RS_7_3 = ReedSolomonPrimeField(6, 3, 3)
message = [6, 2, 5]
encoded_message = RS_7_3.EncodeMessage(message)
error_codeword = RS_7_3.MakeError(encoded_message)
decoded_message = RS_7_3.DecodeMessage(error_codeword)

RS_11_5 = ReedSolomonPrimeField(10, 5, 2)
message = [1, 0, 1, 1, 0]
encoded_message = RS_11_5.EncodeMessage(message)
error_codeword = [4, 0, 2, 3, 9, 7, 6, 3, 0, 0]
error_codeword = RS_11_5.MakeError(encoded_message)
decoded_message = RS_11_5.DecodeMessage(error_codeword)


RS_11_5 = ReedSolomonPrimeField(100, 50, 2)
message = [random.choice([0, 1]) for _ in range(50)]
encoded_message = RS_11_5.EncodeMessage(message)
error_codeword = RS_11_5.MakeError(encoded_message)
decoded_message = RS_11_5.DecodeMessage(error_codeword)
if message == decoded_message:
    print(True)
else:
    print(False)

from ReedSolomonPrimeField import *
import random

RS_100_50 = ReedSolomonPrimeField(100, 50, 2)
message = [random.choice([0, 1]) for _ in range(50)]
encoded_message = RS_100_50.EncodeMessage(message)
error_codeword = RS_100_50.MakeError(encoded_message)
decoded_message = RS_100_50.DecodeMessage(error_codeword)
if message == decoded_message:
    print(True)
else:
    print(False)

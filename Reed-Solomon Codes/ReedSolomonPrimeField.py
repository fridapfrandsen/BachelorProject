from fieldmath import *
from sympy import symbols, div, GF, poly
import numpy as np
import random as rand

class ReedSolomonPrimeField:
    def __init__(self, code_length, message_length, primitive_element):
        self.n = code_length
        self.field_size = code_length + 1  # Length of codeword
        self.k = message_length  # Length of message
        self.primitive_element = primitive_element  # Primitive element in the field
        self.field_size = code_length +1
        self.field = PrimeField(self.field_size) 
        self.l_null = self.n - 1 - int((self.n - self.k)/2)
        self.l_one = self.l_null - (self.k - 1)
        self.d = self.n - self.k + 1  # Minimum distance is the singleton bound


    def GenerateElements(self):
        elements = [0] * (self.field_size -1)
        for i in range(self.field_size -1):
            elements[i] = self.primitive_element**i % self.field_size
        return elements


    # Encoding method

    def EncodeMessage(self, message):
        print(f"Message to be encoded is {message}")
        elements = self.GenerateElements()
        encoded_message = [0] * len(elements)
        for i in range(len(elements)):
            for j in range(len(message)):
                encoded_message[i] = (encoded_message[i] + message[j]*(elements[i]**j)) % self.field_size
        print(f"Encoded codeword is {encoded_message}")
        return encoded_message
    

    # Generate t errors

    def MakeError(self, codeword):
        error_codeword = codeword.copy()
        t = 1
        while t < self.d / 2:
            error_position = rand.randint(0, len(codeword) - 1)
            error_codeword[error_position] = ((error_codeword[error_position]) + rand.randint(0, self.field_size)) % self.field_size
            print(f"Possible error at: {error_position + 1}")
            t += 1

        return error_codeword


    # Decoding process

    def GenerateErrorCorrectionMatrix(self, received_word):
        elements = self.GenerateElements()
        error_correction_matrix = Matrix(self.n, self.l_null + self.l_one + 2, self.field)
        for i in range(self.l_null + 1):
            for j in range(len(elements)):
                error_correction_matrix.set(j, i, (elements[j]**i) % self.field_size)
        for i in range(self.l_one + 1):
            for j in range(len(elements)):
                error_correction_matrix.set(j, i + self.l_null + 1, ((elements[j]**i)*received_word[j]) % self.field_size)
        error_correction_matrix.reduced_row_echelon_form()
        return error_correction_matrix
    
    def FindErrorPolynomial(self, received_word):
        error_correction_matrix = self.GenerateErrorCorrectionMatrix(received_word)
        Q0 = [0] * (self.l_null + 1)
        Q1 = [0] * (self.l_one + 1)
        rows_with_values = error_correction_matrix.column_count() - error_correction_matrix.row_count()
        for i in range(rows_with_values):
            for j in range(len(Q0)):
                Q0[len(Q0)-j-1] -= error_correction_matrix.get(j, error_correction_matrix.column_count() - ( i + 1))
        for i in range(rows_with_values):
            for j in range(len(Q0), error_correction_matrix.row_count() ):
                Q1[(len(Q0)-1)-j] -= error_correction_matrix.get(j, error_correction_matrix.column_count() - ( i + 1))
        for i in range(rows_with_values):
            Q1[i] = 1
        for i in range(len(Q0)):
            Q0[i] = Q0[i] % self.field_size
        for i in range(len(Q1)):
            Q1[i] = Q1[i] % self.field_size
        return (Q0, Q1)
    
    def PolynomialDivision(self, received_word):
        self.g = 0
        self.f = 0
        (Q0,Q1) = self.FindErrorPolynomial(received_word)
        for i in range(len(Q0)):
            Q0[i] = (-Q0[i]) % self.field_size
        x = symbols('x')
        for i in range(len(Q0)):
            self.g += Q0[i]*x**(len(Q0)-i-1)
        for i in range(len(Q1)):
            self.f += Q1[i]*x**(len(Q1)-i-1)
        q, r = div(self.g, self.f, domain=GF(self.field_size))
        if r != 0:
            raise ValueError("Polynomial division did not result in a zero remainder")
        g = poly(q,x).all_coeffs()
        for i in range(len(g)):
            g[i] = g[i] % self.field_size
        g = g[::-1]
        while len(g) < self.k:
            g.append(0)
        return g
    
    def DecodeMessage(self, received_word):
        print(f"Received codeword is {received_word}")
        decoded_message = self.PolynomialDivision(received_word)
        print(f"Decoded message is {decoded_message}")
        return decoded_message
    




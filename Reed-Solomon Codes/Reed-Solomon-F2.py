from fieldmath import PrimeField
from fieldmath import Matrix
from sympy import symbols, div, GF, Poly, sympify
import numpy as np
import galois


class ReedSolomonF2:
    def __init__(self, k, powerOfTow):
        self.n = 2**powerOfTow - 1
        self.k = k
        self.field = galois.GF(2**powerOfTow)
        self.powerOfTow = powerOfTow
        self.x = symbols('x')
        self.irrPoly = self.field.irreducible_poly
        self.irr_poly_str = str(self.irrPoly).replace('^', '**')
        self.irr_poly_sympy = Poly(sympify(self.irr_poly_str), self.x)
        self.lNull = self.n - 1 - int((self.n - self.k)/2)
        self.lOne = self.lNull - (self.k - 1)

    def elements(self):
        x = symbols('x')
        elemntList = [0] * (self.n)
        for i in range(self.n):
            q, elemntList[i] = div(x**i, self.irr_poly_sympy, domain=GF(2))
        return elemntList

    def encodeMessage(self, message):
        x = symbols('x')
        elements = self.elements()
        messagePoly = 0
        for i in range(len(message)):
            messagePoly += message[i]*x**i
        encodedMessage = [0] * self.n
        for i in range(len(elements)):
            substitutedPoly = messagePoly.as_expr().subs(x, elements[i].as_expr())
            q, encodedMessage[i] = div(Poly(substitutedPoly, x, domain=GF(2)), self.irr_poly_sympy, domain=GF(2))
        return encodedMessage
    
    # def generateMatrix(self, receivedWord):
    #     x = symbols('x')
    #     self.receivedWord = receivedWord
    #     elements = self.elements()
    #     self.Matrix = Matrix(self.n, self.lNull + self.lOne + 2, self.field)
    #     for i in range(self.lNull + 1):
    #         for j in range(len(elements)):
    #             self.Matrix.set(j, i, (elements[j]**i) % self.fieldPrime)
    #     for i in range(self.lOne + 1):
    #         for j in range(len(elements)):
    #             self.Matrix.set(j, i + self.lNull + 1, ((elements[j]**i)*receivedWord[j]) % self.fieldPrime)
    #     self.Matrix.reduced_row_echelon_form()
    #     return self.Matrix
       


ReedSolomon = ReedSolomonF2(5, 3)
print(ReedSolomon.elements())
print(ReedSolomon.encodeMessage([1, 0, 1, 1, 0]))
x = symbols('x')
# print(ReedSolomon.generateMatrix([Poly(1, x, modulus=2), Poly(x**2 + x, x, modulus=2), Poly(x, x, modulus=2), Poly(0, x, modulus=2), Poly(x**2, x, modulus=2), Poly(0, x, modulus=2), Poly(x+1, x, modulus=2)]))



from fieldmath import PrimeField
from fieldmath import Matrix
from sympy import symbols, div, GF, poly
import numpy as np

class ReedSolomonEncoding:
    def __init__(self, k, fieldPrime, primitivElement):
        self.n = fieldPrime - 1
        self.k = k
        self.primitivElement = primitivElement
        self.fieldPrime = fieldPrime
        self.field = PrimeField(fieldPrime)
        self.lNull = self.n - 1 - int((self.n - self.k)/2)
        self.lOne = self.lNull - (self.k - 1)

    def elements(self):
        elemntList = [0] * (self.fieldPrime -1)
        for i in range(self.fieldPrime -1):
            elemntList[i] = self.primitivElement**i % self.fieldPrime
        return elemntList

    def encodeMessage(self, message):
        self.message = message
        elements = self.elements()
        encodeMassage = [0] * len(elements)
        for i in range(len(elements)):
            for j in range(len(self.message)):
                encodeMassage[i] = (encodeMassage[i] + message[j]*(elements[i]**j)) % self.fieldPrime
        return encodeMassage
    
    def generateMatrix(self, receivedWord):
        self.receivedWord = receivedWord
        elements = self.elements()
        self.Matrix = Matrix(self.n, self.lNull + self.lOne + 2, self.field)
        for i in range(self.lNull + 1):
            for j in range(len(elements)):
                self.Matrix.set(j, i, (elements[j]**i) % self.fieldPrime)
        for i in range(self.lOne + 1):
            for j in range(len(elements)):
                self.Matrix.set(j, i + self.lNull + 1, ((elements[j]**i)*receivedWord[j]) % self.fieldPrime)
        self.Matrix.reduced_row_echelon_form()
        return self.Matrix
    
    def findPolynomial(self, receivedWord):
        self.Matrix = self.generateMatrix(receivedWord)
        Q0 = [0] * (self.lNull + 1)
        Q1 = [0] * (self.lOne + 1)
        rowsWithValues = self.Matrix.column_count() - self.Matrix.row_count()
        for i in range(rowsWithValues):
            for j in range(len(Q0)):
                Q0[len(Q0)-j-1] -= self.Matrix.get(j, self.Matrix.column_count() - ( i + 1))
        for i in range(rowsWithValues):
            for j in range(len(Q0), self.Matrix.row_count() ):
                Q1[j-(len(Q0)+1)] -= self.Matrix.get(j, self.Matrix.column_count() - ( i + 1))
        for i in range(rowsWithValues):
            Q1[i] = 1
        for i in range(len(Q0)):
            Q0[i] = Q0[i] % self.fieldPrime
        for i in range(len(Q1)):
            Q1[i] = Q1[i] % self.fieldPrime
        return (Q0, Q1)
    
    def polydivision(self, receivedWord):
        self.g = 0
        self.f = 0
        (Q0,Q1) = self.findPolynomial(receivedWord)
        for i in range(len(Q0)):
            Q0[i] = (-Q0[i]) % self.fieldPrime
        x = symbols('x')
        for i in range(len(Q0)):
            self.g += Q0[i]*x**(len(Q0)-i-1)
        for i in range(len(Q1)):
            self.f += Q1[i]*x**(len(Q1)-i-1)
        print(self.f , self.g)
        q, r = div(self.g, self.f, domain=GF(self.fieldPrime))
        g = poly(q,x).coeffs()
        for i in range(len(g)):
            g[i] = g[i] % self.fieldPrime
        return g



ReedSolomon = ReedSolomonEncoding(3, 7, 3)
print("elements:", ReedSolomon.elements())
message = [1, 4, 2]
encoded_message = ReedSolomon.encodeMessage(message)
print("Encoded message:", encoded_message)
thisMatrix = ReedSolomon.generateMatrix([0,3,3,1,0,1])
print("Encoded message:", "\n", thisMatrix)
rowsWithValues = ReedSolomon.findPolynomial([0,3,3,1,0,1])
print("Polynomials", "\n", rowsWithValues)
polydiv = ReedSolomon.polydivision([0,3,3,6,0,1])
print("Polynomials dividet", "\n", polydiv)


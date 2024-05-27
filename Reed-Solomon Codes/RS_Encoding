import fieldmath
from fieldmath import *
import random

class ReedSolomon:

    def __init__(self, field, primitivElement, messageLenght, parityNumber):

        # The field
        self.f = field

        # Primitive element that generates the field
        self.generator = primitivElement

        # Length of message to be sent
        self.messageLen = messageLenght

        # Number of parity bits to be added to the message
        self.parityLen = parityNumber

        # Length of codeword
        self.codewordLen = messageLenght + parityNumber      


    # Method for creating generator polynomial
    def makeGeneratorPolynomial(self):
        result = [self.f.one()] + [self.f.zero()] * (self.parityLen - 1)

        powerOfGenerator = self.f.one()
        for i in range(self.parityLen):
            for j in reversed(range(self.parityLen)):
                result[j] = self.f.multiply(self.f.negate(powerOfGenerator), result[j])
                if j >= 1:
                    result[j] = self.f.add(result[j - 1], result[j])
            genpow = self.f.multiply(self.generator, powerOfGenerator)
        return result



    # Method for encoding message
    def encode(self, message):

        # Produce the generator polynomial
        generatorPoly = self.makeGeneratorPolynomial()

        eccPoly = [self.f.zero()] * self.parityLen

        for msgval in reversed(message):
            factor = self.f.add(msgval, eccPoly[-1])
            del eccPoly[-1]
            eccPoly.insert(0, self.f.zero())
            for j in range(self.parityLen):
                eccPoly[j] = self.f.subtract(eccPoly[j], self.f.multiply(generatorPoly[j], factor))

        return [self.f.negate(val) for val in eccPoly] + message


    # Method to create an error in the code
    def makeError(self, codeword):
        error_location = random.randint(0, len(codeword) - 1)
        codeword[error_location] = (codeword[error_location] + 1) % self.f.modulus
        return codeword
    

    # Decoding methods

    # Method to evaluate a polynomial at given point e.g. powers of the primitive element
    def evaluatePoly(self, polynomial, point):
        result = self.f.zero()
        for polyval in reversed(polynomial):
              result = self.f.multiply(point, result)
              result = self.f.add(polyval, result)
        return result
    
    # Method to return given element in field raised to a given power
    def pow(self, base, exp):
        result = self.f.one()
        for _ in range(exp):
            result = self.f.multiply(base, result)
        return result  


    # Method to calculate the syndromes
    def calculateSyndromes(self, receivedWord):
        result = []
        powerOfGenerator = self.f.one()
        for i in range(self.parityLen):
            result.append(self.evaluatePoly(receivedWord, powerOfGenerator))
            powerOfGenerator = self.f.multiply(self.generator, powerOfGenerator)
        return result
    

    # Method to calculate Error Locator Polynomial
    def errorLocatorPoly(self, syndromes, numberOfErrorsToCorrect):
        matrix = fieldmath.Matrix(numberOfErrorsToCorrect, numberOfErrorsToCorrect + 1, self.f)
        for r in range(matrix.row_count()):
            for c in range(matrix.column_count()):
                val = syndromes[r + c]
                if c == matrix.column_count() - 1:
                    val = self.f.negate(val)
                matrix.set(r, c, val)
        
        matrix.reduced_row_echelon_form()

        result = [self.f.one()] + [self.f.zero()] * numberOfErrorsToCorrect

        c = 0
        for r in range(matrix.row_count()):
          while True:
            if c == matrix.column_count():
                return result
            elif self.f.equals(matrix.get(r, c), self.f.zero()):
                c += 1
            elif c == matrix.column_count() - 1:
                return None
            else:
                break
		
            result[-1 - c] = matrix.get(r, numberOfErrorsToCorrect)
        
        return result
    
    # Method to find the error locations (roots of error locator polynomial)
    def findErrorLocations(self, errorLocatorPoly, maxSolutions):
        locationsFound = []
        generatorReciprocal = self.f.reciprocal(self.generator)
        powerOfGeneratorReciprocal = self.f.one()
        for i in range(self.codewordLen):
            polyval = self.evaluatePoly(errorLocatorPoly, powerOfGeneratorReciprocal)
            if self.f.equals(polyval, self.f.zero()):
                if len(locationsFound) >= maxSolutions:
                    return None
                locationsFound.append(i)
            powerOfGeneratorReciprocal = self.f.multiply(generatorReciprocal, powerOfGeneratorReciprocal)
        return locationsFound
    
    # Method to calculate error values at the error locations
    def calculateErrorValues(self, errorLocations, syndromes):
        matrix = fieldmath.Matrix(len(syndromes), len(errorLocations) + 1, self.f)
        for c in range(matrix.column_count() - 1):
          powerOfGenerator = self.pow(self.generator, errorLocations[c])
          powerOfPowerOfGenerator = self.f.one()
          for r in range(matrix.row_count()):
            matrix.set(r, c, powerOfPowerOfGenerator)
            powerOfPowerOfGenerator = self.f.multiply(powerOfGenerator, powerOfPowerOfGenerator)
        for r in range(matrix.row_count()):
            matrix.set(r, matrix.column_count() - 1, syndromes[r])
        
        matrix.reduced_row_echelon_form()
        if not self.f.equals(matrix.get(matrix.column_count() - 1, matrix.column_count() - 1), self.f.zero()):
            return None

        result = []
        for i in range(len(errorLocations)):
            if not self.f.equals(matrix.get(i, i), self.f.one()):
                return None
            result.append(matrix.get(i, matrix.column_count() - 1))
        return result


    # Method to correct the codeword
    def fixErrors(self, receivedWord, errorLocations, errorValues):
        result = list(receivedWord)
        for (loc, val) in zip(errorLocations, errorValues):
            result[loc] = self.f.subtract(result[loc], val)
        return result
    
    # Method to decode the received word back to the message
    def decode(self, receivedWord, numberOfErrorsToCorrect=None):
        
        if numberOfErrorsToCorrect is None:
            numberOfErrorsToCorrect = self.parityLen // 2
        if len(receivedWord) != self.codewordLen:
            raise ValueError("Invalid codeword length")
        if not (0 <= numberOfErrorsToCorrect <= self.parityLen // 2):
            raise ValueError("Too many errors to correct")

        syndromes = self.calculateSyndromes(receivedWord)
        if any(not self.f.equals(val, self.f.zero()) for val in syndromes):
            if numberOfErrorsToCorrect == 0:
                return None

            errorLocatorPoly = self.errorLocatorPoly(syndromes, numberOfErrorsToCorrect)
            if errorLocatorPoly is None:
                return None
                
            errorLocations = self.findErrorLocations(errorLocatorPoly, numberOfErrorsToCorrect)
            if errorLocations is None or len(errorLocations) == 0:
                return None
                
            errorValues = self.calculateErrorValues(errorLocations, syndromes)
            if errorLocatorPoly is None:
                return None
                
            codeword = self.fixErrors(receivedWord, errorLocations, errorValues)

            newsyndromes = self.calculateSyndromes(codeword)
            if any(not self.f.equals(val, self.f.zero()) for val in newsyndromes):
                raise AssertionError()
                
        return codeword[self.parityLen : ]



RS = ReedSolomon(PrimeField(7), 3, 3, 3)
codeword = RS.encode(([0, 4, 2]))
print(RS)
print("Codeword:", codeword)
receivedWord = RS.makeError(codeword)
print("Received Word:", receivedWord)
syndromes = RS.calculateSyndromes(receivedWord)
print("Syndromes:", syndromes)
errorLocatorPoly = RS.errorLocatorPoly(syndromes, 1)
print("Error locator polynomial:", errorLocatorPoly)
errorLocations = RS.findErrorLocations(errorLocatorPoly, 1)
print("Error locations:", errorLocations)
decodedWord = RS.decode(receivedWord, 1)
print("Decodedo word:", decodedWord)







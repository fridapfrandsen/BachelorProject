from fieldmath import PrimeField
from fieldmath import Matrix
import numpy as np

class HammingEncoding:
    def __init__(self, parity_check_matrix):
        self.H = np.array(parity_check_matrix)
        self.genMatrix = None
        self.encodeMessage = None
        self.decodeMessage = None
        self.field = PrimeField(2)
        self.rows, self.cols = self.H.shape
        self.ParityMatrix = Matrix(self.rows, self.cols, self.field)
        for i in range(self.rows):
            for j in range(self.cols):
                self.ParityMatrix.set(i, j, int(self.H[i, j]))

    def generateMatrix(self):
        # rows, cols = self.H.shape
        # matrix = Matrix(rows, cols, self.field)
        # for i in range(rows):
        #     for j in range(cols):
        #         matrix.set(i, j, int(self.H[i, j]))
        self.genMatrix = Matrix(self.cols - self.rows, self.cols, self.field)
        for i in range(self.cols - self.rows):
            for j in range(self.rows):
                self.genMatrix.set(i, j+self.rows+1, int(self.H[j, i]))
        for i in range(self.cols - self.rows):
            for j in range(self.cols - self.rows):
                if (i == j):
                    self.genMatrix.set(i, j, 1)  
                else:
                    self.genMatrix.set(i, j, 0) 
        return self.genMatrix
        
    def encode(self, message):
        messageMatrix = Matrix(1, len(message), self.field)
        for i in range(len(message)):
            messageMatrix.set(0, i, message[i])
        self.encodeMessage = messageMatrix.multiply(self.genMatrix)
        return self.encodeMessage
    
    def decode(self, received):
        receivedMatrix = Matrix(1, len(received), self.field)
        for i in range(len(received)):
            receivedMatrix.set(0, i, received[i])
        print("parity chek:", self.ParityMatrix)
        print("besked med fejl:", receivedMatrix.transpose())
        syndrome = self.ParityMatrix.multiply(receivedMatrix.transpose())
        print("Syndrome:\n", syndrome)
        errorPos = -1
        for col in range(self.cols):
            match = True
            for row in range(self.rows):
                if syndrome.get(row, 0) != self.ParityMatrix.get(row, col):
                    match = False
                    break
            if match:
                errorPos = col
                break
        receivedMatrix.set(0, errorPos, 1 - receivedMatrix.get(0, errorPos))
        self.decodeMessage = receivedMatrix.clone()
        return self.decodeMessage


x = HammingEncoding([[1, 1, 1, 0, 1, 0, 0],[1, 1, 0, 1, 0, 1, 0],[1, 0, 1, 1, 0, 0, 1]])

print("Paritychek:", "\n" , x.ParityMatrix)
x.generateMatrix()
print("Generatur Matrix:", "\n" ,x.genMatrix)
x.encode([1, 1, 0, 1])
print("Encoded message:",x.encodeMessage)
x.decode([1, 1, 0, 0, 0, 1, 0])
print("Decoded message:",x.decodeMessage)

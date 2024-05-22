
import numpy
from sympy import Matrix
from sympy import symbols
from types import FunctionType
import test as matrixMod


# M = Matrix([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]) 
# print(M)
# print("Matrix : {} ".format(M)) 
   
# # Use sympy.rref() method  
# M_rref = M.rref()   
      
# print("The Row echelon form of matrix M and the pivot columns : {}".format(M_rref))


# we wish to work in F_7 with k=3

# our primitiv element 3

F = 11 
k = 5
primitivElement = 2
massage = [1,1,1,1,1]

print("Massage is: ", massage)

def elements(f):
    lisfOfElements = []
    for i in range(0,f-1):
        lisfOfElements.append((primitivElement**i)%f)
    return lisfOfElements




print("Elements in F",F,"is:" , elements(F))

def encode(m):
    elementList = elements(F)
    encodeMassage = [0] * len(elementList)
    for i in range(0,len(elementList)):
        for j in range(0,len(massage)):
            encodeMassage[i] = (encodeMassage[i] + m[j]*(elementList[i]**j))%F
    return encodeMassage


print("Encode message: ", encode(massage))
messageWithError = [5, 9, 0, 9, 0, 1, 0, 7, 0, 5]
print("message with error:", messageWithError)


#decode

n = F - 1
d = n - k + 1
t = int((n-k)/2)
lNul = n - 1 - t
lEt = lNul - (k - 1)

print("n: ", n ,", d: ", d ,", t: " , t ,", lNul: " , lNul, ", lEt: ",lEt )

def generatMatrix(messageEncoded):
    emptyMatrix = emptyMatrix = [[0] * (lNul + lEt + 2) for _ in range(len(messageEncoded))]
    elementList = elements(F)
    for j in range(0,lNul+1):
        for i in range(0, len(messageEncoded)):
            emptyMatrix[i][j] = (elementList[i]**j)%F
    for j in range(lNul+1,lNul + lEt + 2):
        for i in range(0, len(messageEncoded)):
            emptyMatrix[i][j] = (messageEncoded[i]*emptyMatrix[i][j-(lNul+1)])%F
    return emptyMatrix

print("Generated matrix:", Matrix(generatMatrix(messageWithError)))

def reducedMatrix(messageEncoded):
    A = Matrix(generatMatrix(messageEncoded))
    return matrixMod._rref_mod(A, n=F)
    
print(format(reducedMatrix(messageWithError)))

def findPolynomial(messageEncoded):
    redu = reducedMatrix(messageWithError)
    redMat = redu[0]
    values = len(redMat[0,:])-len(redMat[:,0])
    print(values)
    Q0 = [0]*(lNul+1)
    Q1 = [0]*(lEt+1)
    for j in range(values):
        for i in range(0, lNul+1):
            Q0[i] -= redMat[i, -(j+1)]
    for j in range(values):
        for i in range(lNul+1, len(redMat[:,0])):
            Q1[i-(lNul+1)] -= redMat[i, -(j+1)]
    for i in range(values):
        Q1[-(i+1)]=1
    for i in range(len(Q0)):
        Q0[i] = Q0[i]%F
    for i in range(len(Q1)):
        Q1[i] = Q1[i]%F
    print("Q0 :", Q0)
    print("Q1 :", Q1)
    return (Q0, Q1)

findPolynomial(messageWithError)

def polydivision(messageEncoded):
    (Q0,Q1) = findPolynomial(messageEncoded)
    for i in range(len(Q0)):
        Q0[i] = (-Q0[i])%F
    Q0tup = tuple(Q0)
    Q1tup = tuple(Q1)
    gx = numpy.polynomial.polynomial.polydiv(Q0tup,Q1tup)
    gxlist = list(gx)[0]
    for i in range(len(gxlist)):
        gxlist[i] = int(gxlist[i])%F
    return gxlist


print(polydivision(messageWithError))



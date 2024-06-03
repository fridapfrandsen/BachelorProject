import galois
import numpy as np


GFpn = galois.GF(2**8)
print(GFpn.properties)
print(GFpn.primitive_element)

GFp = galois.GF(11)
print(GFp.properties)

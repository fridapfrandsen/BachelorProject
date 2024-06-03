import numpy as np
import random as rand

class HammingCodeSevenFour:
    def __init__(self):
        # Defines the generator matrix for the (7,4)-Code
        self.G = np.array([[1, 0, 0, 0, 1, 1, 1],
                           [0, 1, 0, 0, 1, 1, 0],
                           [0, 0, 1, 0, 1, 0, 1],
                           [0, 0, 0, 1, 0, 1, 1]])
        
        # Defines the parity check matric for the (7,4)-Code
        self.H = np.array([[1, 1, 1, 0, 1, 0, 0],
                           [1, 1, 0, 1, 0, 1, 0],
                           [1, 0, 1, 1, 0, 0, 1]])
        
    def Encode(self, message):
        # Raise error if message is not of length 4 or not binary
        if len(message) != 4 or not all(bit in "01" for bit in message):
            raise ValueError("Message should be a 4-bit binary string.")
        
        print(f"Message to be encoded is {message}")

        # Convert message to array
        message = np.array(list(map(int, message)))

        # Encode by multiplying the codeword with the generator matrix
        codeword_array = np.dot(message, self.G) % 2

        # Convert codeword to string
        codeword = "".join(map(str, codeword_array))

        print(f"The encoded codeword is {codeword}")

        return codeword
    
    def MakeError(self, codeword):
        # Raise error if codeword is not of length 7 or not binary
        if len(codeword) != 7 or not all(bit in "01" for bit in codeword):
            raise ValueError("Codeword should be a 7-bit binary string.")
        
        # Find a random position in the codeword
        error_position = rand.randint(0, 6)

        # Convert codeword to list
        codeword = list(codeword)

        # Switch the bit at the error position
        codeword[error_position] = str((int(codeword[error_position]) + 1) % 2)

        # Convert codeword back to string
        error_codeword = ''.join(codeword)

        print(f"Bit flipped at position: {error_position + 1}")
        print(f"Received codeword is {error_codeword}")

        return error_codeword
    
    def Decode(self, received_codeword):
        if len(received_codeword) != 7 or not all(bit in "01" for bit in received_codeword):
            raise ValueError("Received word should be a 7-bit binary string.")
        
        # Convert received codeword to array
        received_codeword = np.array(list(map(int, received_codeword)))

        # Calculate the syndrome
        syndrome = np.dot(self.H, received_codeword) % 2

        # Convert syndrome to integer value
        syndrome_str = "".join(map(str, syndrome))
        syndrome_int = int(syndrome_str, 2)

        # Check whether the syndrome is zero and if not, which coloumn it corresponds to
        error_position = - 1
        if syndrome_int != 0:
            for i, column in enumerate(self.H.T):
                if np.array_equal(syndrome, column):
                    error_position = i
                    break
            print(f"Error found at position: {error_position + 1}")
            # Fix the error
            received_codeword[error_position] = (received_codeword[error_position] + 1) % 2
        else:
            print("No errors found")

        decoded_codeword = "".join(map(str, received_codeword))
        decoded_message = "".join(map(str, received_codeword[:4]))

        print(f"Decoded codeword is {decoded_codeword}")
        print(f"Decoded message is {decoded_message}")

        return decoded_message
    

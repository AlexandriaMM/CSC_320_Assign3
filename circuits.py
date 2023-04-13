__author__ = ""
__Copyright__ = "Copyright @2022"


class circuit(object):  # base class, represents circuit w/two input bits
    def __init__(self, in1, in2):  # assigns values to given variables
        self.in1_ = in1  # so in our case, we assign values to in1 and in2
        self.in2_ = in2


class andgate(circuit):
    def getCircuitOutput(self):  # returns 1 if both inputs = 1, else returns 0
        if self.in1_ == 1 and self.in2_ == 1:
            return 1
        else:
            return 0


class orgate(circuit):  # returns 1 is at least one input is 1, else returns 0
    def getCircuitOutput(self):
        if self.in1_ == 0 and self.in2_ == 0:
            return 0
        else:
            return 1


class notgate(circuit):  # if input = 1, returns 0, and vice versa
    def __init__(self, in1):
        self.in1_ = in1

    def getCircuitOutput(self):
        if self.in1_ == 1:
            return 0
        elif self.in1_ == 0:
            return 1


# Hint: you may implement some multi-input logic gates to help you build the circuit,
# for example, below is a 3-input andgate3 boolean algebra: Y=ABC
class andgate3(circuit): # returns 1 is all inputs are 1, else returns 0
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.in2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(out_andg0, self.in3_)
        out_andg1 = andg1.getCircuitOutput()

        return out_andg1

class xorgate(circuit):  # created xor gate for adder
    def getCircuitOutput(self):  # returns 0 if both inputs = 1 or both inputs = 0, else returns 0
        if (self.in1_ == 1 and self.in2_ == 1) or (self.in1_ == 0 and self.in2_ == 0):
            return 0
        else:
            return 1
        
class norgate(circuit): 
    def getCircuitOutput(self):
        if (self.in0_ == 0 and self.in1_ == 0):
            return 1
        else:
            return 0


# 2to1 mux implemented by notgate, andgates and orgates
class mux_2to1(circuit):
    def __init__(self, in0, in1, select):
        self.in0_ = in0  # first input signal
        self.in1_ = in1  # second input signal
        self.select_ = select  # select signal

    def getCircuitOutput(self):
        not_select = notgate(self.select_)  # use notgate on select for first andgate
        and0 = andgate(self.in0_, not_select.getCircuitOutput())  # first andgate takes not select and first input
        and1 = andgate(self.in1_, self.select_)  # second andgate takes select and second input
        or0 = orgate(and0.getCircuitOutput(), and1.getCircuitOutput())  # orgate takes both andgates

        return or0.getCircuitOutput()  # returns the output of the orgate

# 4to1 mux implemented by 2to1 muxes
class mux_4to1(circuit):
    def __init__(self, in0, in1, in2, in3, select0, select1):
        self.in0_ = in0  # first input signal
        self.in1_ = in1  # second input signal
        self.in2_ = in2  # third input signal
        self.in3_ = in3  # fourth input signal
        self.select0_ = select0  # select signal
        self.select1_ = select1  # select signal

    def getCircuitOutput(self):
        mux0 = mux_2to1(self.in0_, self.in1_, self.select0_)  # takes in0 and in1 into a 2to1 mux, with select0
        mux1 = mux_2to1(self.in2_, self.in3_, self.select0_)  # takes in2 and in3 into a second 2to1 mux, with select 0
        mux2 = mux_2to1(mux0.getCircuitOutput(), mux1.getCircuitOutput())  # gets the outputs of the first two 2to1 muxs and puts them into another 2to1, with new select
        return mux2.getCircuitOutput()  # returns output of final 2to1 mux


# fulladder implemented with logic gates
class fulladder(circuit):  # takes in two bits and a carry-in, outputs a sum and a carry-out
    def __init__(self, in0, in1, in2):
        self.in0_ = in0  # first input signal
        self.in1_ = in1  # second input signal
        self.in2_ = in2  # third input signal

    def getCircuitOutput(self):
        xor0 = xorgate(self.in0_, self.in1_)  # puts two bits into xor
        sum_bit = xorgate(xor0.getCircuitOutput(), self.in2_)  # puts first xor and carry-in into second xor to give sum

        and0 = andgate(xor0.getCircuitOutput(), self.in2_)  # puts first xor and second bit into andgate
        and1 = andgate(self.in0_, self.in1_)  # puts two input bits into andgate
        carry_out = orgate(and0.getCircuitOutput(), and1.getCircuitOutput())  # combines andgates into orgate to produce carry-out

        return sum_bit, carry_out  # returns sum and carry-out


# 1 bit ALU implemented with logic gates
class ALU_1bit(object):
    def __init__(self, in0, in1, carryin, m0, m1): #takes 2 inputs, a carryin, and 2 inputs for the multiplexor
        self.in0_ = in0 #first input signal
        self.in1_ = in1 #second input signal
        self.carryin_ = carryin #carryin
        self.m0_ = m0 #multiplexor input1
        self.m1_ = m1 #multiplexor input2

    def getCircuitOutput(self):
        fulladder0 = fulladder(self.in0_, self.in1_, self.carryin_)
        carryout0 = fulladder0.getCircuitOutput() 
        and0 = andgate(self.in0_, self.in1_)
        nor0 = norgate(self.in0_, self.in1_)
        xor0 = xorgate(self.in0_, self.in1_)
        mux0 = mux_4to1(fulladder0.getCircuitOutput, and0.getCircuitOutput, nor0.getCircuitOutput, xor0.getCircuitOutput, self.m0_, self.m1_)
        
        return mux0.getCircuitOutput, carryout0[1]




class aluControl(circuit):
    def __init__(self, in0, in1, in2, in3, in4, in5, aluOp0, aluOp1):
        self.in0_ = in0
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5
        self.aluOp0_ = aluOp0
        self.aluOp1_ = aluOp1

    def getCircuitOutput(self):
        in0_or_in3 = orgate(self.in0_, self.in3_) # or gate between in0 and in3
        in1_and_alu1 = andgate(self.in1_, self.aluOp1_) # and gate between in1 and ALUOp1

        operation0 = andgate(in0_or_in3, self.aluOp1_) # and gate between in0_or_in3 gate and ALUOp1, return me
        operation1 = orgate(notgate(self.in2_), notgate(self.aluOp1_))  # or gate between not in2 and not ALUOp1, return me
        operation2 = orgate(in1_and_alu1, self.aluOp0_) # or gate on in1_and_alu1 gate and ALUOp0, return me
        operation3 = andgate(self.aluOp0_, notgate(self.aluOp0_)) # or gate on ALUOp0 and not ALUOp0, return me

        return operation0, operation1, operation2, operation3

    '''
    Implement the ALU control circuit shown in Figure D.2.2 on page 7 of the slides 10_ALU_Control.pdf.
    There are eight inputs: aluOp1, aluOp2, f5, f4, f3, f2, f1, f0., 
    There are four outputs of the circuit, you may put them in a python list and return as a whole.
    '''


class ALU_32bit(object):
    def __init__(self, in0, in1, carryin, m0, m1):
        self.in0_ = in0
        self.in1_ = in1
        self.carryin_ = carryin
        self.m0_ = m0
        self.m1_ = m1

    def getCircuitOutput(self):
        if len(self.in0_) == len(self.in1_) and len(self.in0_) == 32: #checking if two lists are equal and length is 32 bits
            reversedIn0 = self.in0_.reverse() #reversing first list so that we are reading the digits from right to left
            reversedIn1 = self.in1_.reverse() #reversing second list so that we are reading the digits from right to left
            for i in reversedIn0: #looping through two lists from input
                in0 = reversedIn0[i] #setting 1 bit from list 1
                in1 = reversedIn1[i] #setting 1 bit from list 2
                oldALU = ALU_1bit(in0, in1, self.carryin_, self.m0_, self.m1_) #creating old ALU
                carryout = oldALU.getCircuitOutput()[1] #getting carryout from old ALU
                if i >= len(self.in0_) - 1: #if loop iteration is less than list length - 1
                    newALU = ALU_1bit(reversedIn0[i+1], reversedIn1[i+1], carryout ,self.m0_, self.m1_) #using carryout from oldALU as carryin for newALU
                    newCarryOut = newALU.getCircuitOutput()[1] #getting carryout from new ALU
                    self.carryin_= newCarryOut #setting carryin for the next iteration
                else:
                    return oldALU.getCircuitOutput()
    '''
    Implement a 32 bit ALU by using the 1 bit ALU.
    Your 32-bit ALU should be able to compute 32-bit AND, OR, addition, subtraction, slt(set on if less than).
    The inputs are:

    two python lists with lenth 32, e.g.:
    A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    please note that bit 0 is at the end of the list, which means that bit 0 of A is A[31], bit 31 of A is A[0], bit 0 of B is B[31] and bit 31 of B is B[0].

    carryIn for the 0th 1-bit ALU, which take care of the bit 0.

    aluctrs, which could be a list of alu control signals:
    aluctrs[0] controls the all the 2to1 mux in each 1-bit ALU for bits of input A,
    aluctrs[1] controls the all the 2to1 mux in each 1-bit ALU for bits of input B.
    aluctrs[2] and aluctrs[3] controls all the 4to1 mux in each 1-bit ALU for choose what as output, 00 choose out from AND, 01 choose out from OR, 10 choose out from adder, 11 choose the less.

    Please note that the carryOut output of each 1-bit ALU except the 31th one should be the carryIn the next 1 bit ALU, you may use for loop here for the computation of the sequential 1-bit ALU.

    And please also note that in order to make slt work, we need to use the sum output from the adder of the 31th 1-bit ALU and make it as the less input of the 0th 1bit ALU.


    '''

class mainCtrol(circuit):
    def __init__(self, op5, op4, op3, op2, op1, op0):
        return
    
    
class registerFile(circuit):
    def __init__ (self, reg_initial_value):
        return
    
    def setRegValue(self, o_regDecoder, valueToSet):
        return
    
    def getRegValue(self, o_regDecoder):
        return
    
    def getAllRegValues(self):
        return
    

class decoderReg(circuit):
    def __init__(self, Instr_RegField):
        return
    
    def getCircuitOutput(self):
        return
    

class simpleMIPS(circuit):
    def __init__(self, registers):
        return

    def getCircuitOutput(self, instru):
        return   

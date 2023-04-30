__author__ = "Joshua Buxton, Jim Collado, Alexandria Macko-Millard, Zach Paul"
__Copyright__ = "Copyright @2022"


class circuit(object):  # base class, represents circuit w/two input bits
    def __init__(self, in1, in2):  # assigns values to given variables
        self.in1_ = in1  # so in our case, we assign values to in1 and in2
        self.in2_ = in2


class andgate(circuit):
    def __init__(self, in1_, in2_):
        self.in1_ = in1_
        self.in2_ = in2_

    def getCircuitOutput(self):  # returns 1 if both inputs = 1, else returns 0
        if self.in1_ == 1 and self.in2_ == 1:
            return 1
        else:
            return 0


class orgate(circuit):  # returns 1 is at least one input is 1, else returns 0
    def __init__(self, in1_, in2_):
        self.in1_ = in1_
        self.in2_ = in2_

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
class andgate3(circuit): # returns 1 if all inputs are 1, else returns 0
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

class andgate6(circuit): # takes 6 inputs, returns 1 if all are 1, else returns 0
    def __init__(self, in1, in2, in3, in4, in5, in6):  # Initialize variables
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5
        self.in6_ = in6

    def getCircuitOutput(self):
        andg0 = andgate3(self.in1_, self.in2_, self.in3_)  # Take first 3 inputs and put them through an andgate
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate3(out_andg0, self.in4_, self.in5_) # Take previous andgate and the next two inputs into another andgate
        out_andg1 = andg1.getCircuitOutput()

        andg2 = andgate3(out_andg0, out_andg1, self.in6_)  # Finally, take the two andgates and the last input and put them through one final andgate
        out_andg2 = andg2.getCircuitOutput()

        return out_andg2
class xorgate(circuit):
    def __init__(self, in1_, in2_):
        self.in1_ = in1_
        self.in2_ = in2_

    def getCircuitOutput(self):  # returns 0 if both inputs = 1 or both inputs = 0, else returns 0
        if (self.in1_ == 1 and self.in2_ == 1) or (self.in1_ == 0 and self.in2_ == 0):
            return 0
        else:
            return 1
        
class norgate(circuit):
    def __init__(self, in1_, in2_):
        self.in1_ = in1_
        self.in2_ = in2_

    def getCircuitOutput(self): #returns 1 only if both inputs are 0, else returns 0
        if (self.in1_ == 0 and self.in2_ == 0):
            return 1
        else:
            return 0
        
class slt(circuit):
    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2

    def getCircuitOutput(self):
        val = fulladder(self.in1, self.in2, 1).getCircuitOutput()
        if val[1] == 1:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        else:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# 2to1 mux implemented by notgate, andgates and orgates
class mux_2to1(circuit):
    def __init__(self, in0, in1, select):
        self.in0_ = in0  # first input signal
        self.in1_ = in1  # second input signal
        self.select_ = select  # select signal

    def getCircuitOutput(self):
        not_select = notgate(self.select_).getCircuitOutput()  # use notgate on select for first andgate
        and0 = andgate(self.in0_, not_select).getCircuitOutput()  # first andgate takes not select and first input
        and1 = andgate(self.in1_, self.select_).getCircuitOutput()  # second andgate takes select and second input
        or0 = orgate(and0, and1).getCircuitOutput()  # orgate takes both andgates

        return or0  # returns the output of the orgate

# 4to1 mux implemented by 2to1 muxes
class mux_4to1(circuit):
    def __init__(self, in0, in1, in2, select0, select1):
        self.in0_ = in0  # first input signal
        self.in1_ = in1  # second input signal
        self.in2_ = in2  # third input signal
        self.select0_ = select0  # select signal
        self.select1_ = select1  # select signal

    def getCircuitOutput(self):
        if self.select0_ == 0 and self.select1_ == 0:
            return self.in0_
        elif self.select0_ == 0 and self.select1_ == 1:
            return self.in1_
        elif self.select0_ == 1 and self.select1_ == 0:
            return self.in2_

# fulladder implemented with logic gates
class fulladder(circuit):  # takes in two bits and a carry-in, outputs a sum and a carry-out
    def __init__(self, in0, in1, in2):
        self.in0_ = in0  # first input signal
        self.in1_ = in1  # second input signal
        self.in2_ = in2  # third input signal

    def getCircuitOutput(self):
        xor0 = xorgate(self.in0_, self.in1_).getCircuitOutput()  # puts two bits into xor
        sum_bit = xorgate(xor0, self.in2_).getCircuitOutput()  # puts first xor and carry-in into second xor to give sum

        and0 = andgate(xor0, self.in2_).getCircuitOutput()  # puts first xor and second bit into andgate
        and1 = andgate(self.in0_, self.in1_).getCircuitOutput()  # puts two input bits into andgate
        carry_out = orgate(and0, and1).getCircuitOutput()  # combines andgates into orgate to produce carry-out

        return sum_bit, carry_out  # returns sum and carry-out


# 1 bit ALU implemented with logic gates
class ALU_1bit(object):
    def __init__(self, in0, in1, carryIn, aluControlOutput): #takes 2 inputs, a carryin, and 2 inputs for the multiplexor
        self.in0_ = in0 #first input signal
        self.in1_ = in1 #second input signal
        self.carryin_ = carryIn #carryin
        self.inva = aluControlOutput[0] #inverse a
        self.invb = aluControlOutput[1] #inverse b
        self.m0_ = aluControlOutput[2] #multiplexor input1
        self.m1_ = aluControlOutput[3] #multiplexor input2

    def getCircuitOutput(self):
        #checking value of invb and setting input value of fulladder accordingly
        if self.invb == 0:
            fulladder0 = fulladder(self.in0_, self.in1_, self.carryin_)
        elif self.invb == 1:
            fulladder0 = fulladder(self.in0_, notgate(self.in1_).getCircuitOutput(), self.carryin_)
        carryout0 = fulladder0.getCircuitOutput() #getting carryout from the full adder
        and0 = andgate(self.in0_, self.in1_) #puts 2 input bits into an and gate
        or0 = orgate(self.in0_, self.in1_) #puts 2 input bits into an or gate
        #passing logic gate output, fulladder output, and input values into 4 to 1 mux
        mux0 = mux_4to1(and0.getCircuitOutput(), or0.getCircuitOutput(), fulladder0.getCircuitOutput()[0], self.m0_, self.m1_)
        
        return mux0.getCircuitOutput(), carryout0[1] #returning mux output and carryout




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
        in0_or_in3 = orgate(self.in0_, self.in3_).getCircuitOutput() # or gate between in0 and in3
        in1_and_alu1 = andgate(self.in1_, self.aluOp1_).getCircuitOutput() # and gate between in1 and ALUOp1

        not_in2 = notgate(self.in2_).getCircuitOutput()
        not_aluOp1 = notgate(self.aluOp1_).getCircuitOutput()
        not_aluOp0 = notgate(self.aluOp0_).getCircuitOutput()

        operation0 = andgate(in0_or_in3, self.aluOp1_).getCircuitOutput()  # and gate between in0_or_in3 gate and ALUOp1, return me
        operation1 = orgate(not_in2, not_aluOp1).getCircuitOutput()  # or gate between not in2 and not ALUOp1, return me
        operation2 = orgate(in1_and_alu1, self.aluOp0_).getCircuitOutput()  # or gate on in1_and_alu1 gate and ALUOp0, return me
        operation3 = andgate(self.aluOp0_, not_aluOp0).getCircuitOutput()  # or gate on ALUOp0 and not ALUOp0, return me

        return operation0, operation1, operation2, operation3

    '''
    Implement the ALU control circuit shown in Figure D.2.2 on page 7 of the slides 10_ALU_Control.pdf.
    There are eight inputs: aluOp1, aluOp2, f5, f4, f3, f2, f1, f0., 
    There are four outputs of the circuit, you may put them in a python list and return as a whole.
    '''


class ALU_32bit(object):
    def __init__(self, in0, in1, aluControlOutput):
        self.in0_ = list(in0)
        self.in1_ = list(in1)
        self.aluControlOutput = aluControlOutput
        self.carryin_ = aluControlOutput[1]
        self.m0_ = aluControlOutput[2]
        self.m1_ = aluControlOutput[3]
        self.returnVal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getCircuitOutput(self):
        self.in0_.reverse() #reversing first list so that we are reading the digits from right to left
        self.in1_.reverse() #reversing second list for same reason
        carryin = self.aluControlOutput[1]
        for i in range(32): #looping through two lists from input
            in0 = self.in0_[i] #setting 1 bit from list 1
            in1 = self.in1_[i] #setting 1 bit from list 2
            if i == 0:
                oldALU = list(ALU_1bit(in0, in1, carryin, self.aluControlOutput).getCircuitOutput()) #creating old ALU
            else:
                oldALU = list(ALU_1bit(in0, in1, carryout, self.aluControlOutput).getCircuitOutput()) #creating old ALU
            self.returnVal[i] = oldALU[0]
            carryout = oldALU[1] #getting carryout from old ALU
        self.returnVal.reverse() #reversing to correctly order the list
        return self.returnVal
    
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
        self.op5 = op5
        self.op4 = op4
        self.op3 = op3
        self.op2 = op2
        self.op1 = op1
        self.op0 = op0

    def getCircuitOutput(self):
        notOp0 = notgate(self.op0).getCircuitOutput()  # These are each of our variables put through a notgate for our future andgates
        notOp1 = notgate(self.op1).getCircuitOutput()
        notOp2 = notgate(self.op2).getCircuitOutput()
        notOp3 = notgate(self.op3).getCircuitOutput()
        notOp4 = notgate(self.op4).getCircuitOutput()
        notOp5 = notgate(self.op5).getCircuitOutput()

        # 6 input andgates from FIGURE D.2.5 from the simple processor implementation slides, going from left to right on the diagram
        and0 = andgate6(notOp0, notOp1, notOp2, notOp3, notOp4, notOp5).getCircuitOutput()  # First 6 input andgate
        and1 = andgate6(self.op0, self.op1, notOp2, notOp3, notOp4, self.op5).getCircuitOutput()  # Second 6 input andgate
        and2 = andgate6(self.op0, self.op1, notOp2, self.op3, notOp4, self.op5).getCircuitOutput()  # Third 6 input andgate
        and3 = andgate6(notOp0, notOp1, self.op2, notOp3, notOp4, notOp5).getCircuitOutput()  # Fourth 6 input andgate

        # Our 9 outputs, as described in the diagram
        regDst = and0
        aluSrc = orgate(and1, and2).getCircuitOutput()
        memtoReg = and1
        regWrite = orgate(and0, and1).getCircuitOutput()
        memRead = and1
        memWrite = and2
        branch = and3
        aluOp1 = and0
        aluOp0 = and3

        return regDst, aluSrc, memtoReg, regWrite, memRead, memWrite, branch, aluOp1, aluOp0
    
    
class registerFile(circuit):
    def __init__ (self, reg_initial_value):
        self.registers = [reg_initial_value for i in range(32)]
    
    def setRegValue(self, o_regDecoder, valueToSet):
        for i in range(32):
            if o_regDecoder[i] == 1:
                self.registers[31 - i] = valueToSet
    
    def getRegValue(self, o_regDecoder):
        for i in range(32):
            if o_regDecoder[i] == 1:
                return self.registers[31 - i]
    
    def getAllRegValues(self):
        return self.registers

#takes 2 inputs and gives 4 output values    
class DEC_2to4(circuit):
    def __init__(self, in0, in1):
        self.in0 = in0
        self.in1 = in1

    def getCircuitOutput(self):
        not0 = notgate(self.in0).getCircuitOutput() #not first input value
        not1 = notgate(self.in1).getCircuitOutput() #not second input value

        out0 = andgate(not0, not1).getCircuitOutput() #first output created from not of 2 inputs
        out1 = andgate(self.in0, not1).getCircuitOutput() #second output created from first input, not second input
        out2 = andgate(self.in1, not0).getCircuitOutput() #third output created from first input, not first input
        out3 = andgate(self.in0, self.in1).getCircuitOutput() #fourth output created from first input and second input

        return out0, out1, out2, out3

class DEC_3to8(circuit):
    def __init__(self, in0, in1, in2, e):
        self.in0 = in0
        self.in1 = in1
        self.in2 = in2
        self.e = e

    def getCircuitOutput(self):
        not0 = notgate(self.in0).getCircuitOutput() #not first input
        not1 = notgate(self.in1).getCircuitOutput() #not second input
        not2 = notgate(self.in2).getCircuitOutput() #not third input

        if (self.e == 0):
            return 0, 0, 0, 0, 0, 0, 0, 0
        else:
            #passing input values into 3 input and-gates to get output
            out0 = andgate3(not0, not1, not2).getCircuitOutput()
            out1 = andgate3(not0, not1, self.in2).getCircuitOutput()
            out2 = andgate3(not0, self.in1, not2).getCircuitOutput()
            out3 = andgate3(not0, self.in1, self.in2).getCircuitOutput()
            out4 = andgate3(self.in0, not1, not2).getCircuitOutput()
            out5 = andgate3(self.in0, not1, self.in2).getCircuitOutput()
            out6 = andgate3(self.in0, self.in1, not2).getCircuitOutput()
            out7 = andgate3(self.in0, self.in1, self.in2).getCircuitOutput()

            return out0, out1, out2, out3, out4, out5, out6, out7
    

class decoderReg(circuit):
    def __init__(self, Instr_RegField):
        #passing in 5 bit input to represent register number and instruction value
        self.in0 = Instr_RegField[0]
        self.in1 = Instr_RegField[1]
        self.in2 = Instr_RegField[2]
        self.in3 = Instr_RegField[3]
        self.in4 = Instr_RegField[4]
        self.Instr_RegField = Instr_RegField
    
    def getCircuitOutput(self):
        binary = [str(element) for element in self.Instr_RegField]
        newBinary = int(''.join(binary))

        decimal, i = 0, 0
        while (newBinary != 0):
            dec = newBinary % 10
            decimal = decimal + dec * pow(2, i)
            newBinary = newBinary//10
            i += 1
        print(decimal)
        list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        list[31 - decimal] = 1
        return list

class simpleMIPS(circuit):
    def __init__(self, registers):
        self.registers = registers

    def getCircuitOutput(self, instru):
        self.instru = instru
        opcode = self.instru[0:6]
        rs = self.instru[6:11]
        rt = self.instru[11:16]
        rd = self.instru[16:21]
        shamt = self.instru[21:26]
        funct = self.instru[26:]
        funct.reverse()

        ALUOp1 = mainCtrol(*opcode).getCircuitOutput()[7]
        ALUOp0 = mainCtrol(*opcode).getCircuitOutput()[8]

        register1 = decoderReg(rs).getCircuitOutput()
        reg1Val = self.registers.getRegValue(register1)
        register2 = decoderReg(rt).getCircuitOutput()
        reg2Val = self.registers.getRegValue(register2)

        writeRegister = decoderReg(rd).getCircuitOutput()

        aluControlOutput = list(aluControl(*funct, ALUOp0, ALUOp1).getCircuitOutput())

        aluControlOutput.reverse()

        if (aluControlOutput != [0, 1, 1, 1]):
            new = ALU_32bit(reg1Val, reg2Val, aluControlOutput).getCircuitOutput()
        else:
            new = slt(reg1Val, reg2Val).getCircuitOutput()
        self.registers.setRegValue(writeRegister, new)

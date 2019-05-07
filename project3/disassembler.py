"""Names:
Taylor Robbins
Mirna Elizondo
"""
import sys

# lists to be accessed
opcodeStr = []
instrSpaced = []
addrs = []
arg1 = []
arg2 = []
arg3 = []
argStr1 = []
argStr2 = []
argStr3 = []
binMem = []
opcode = []
mem = []
dest = []
src1 = []
src2 = []
instructions = []
num_instrs = 0
Memory = 96
counter = 0

# masks
specialMask = 0x1FFFF
rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
imMask = 0x3FFC00
shmtMask = 0xFC00
addrMask = 0x1FF000
addr2Mask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0
signMask = 0x800
flipBits = 0xFFF


class Disassembler:

    def __init__(self):
        pass

    def run(self):
        global opcodeStr
        global arg1
        global arg2
        global arg3
        global argStr1
        global argStr2
        global argStr3
        global mem
        global binMem
        global opcode
        global inputFile
        global outputFile
        global instructions
        global instrSpaced
        global Memory
        global counter

        # used for input file reading and output file writing
        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                inputFile = sys.argv[i + i]
            elif sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
                outputFile = sys.argv[i + 1]

        # reading in the instructions while stripping the end of any white space.
        instructions = [line.rstrip() for line in open(inputFile, 'rb')]
        outputFile = open(outputFile + "_dis.txt", 'w')

        # for signed immediate values of specified bit length
        def twos_complement(imm):
            if imm.bit_length() == 26:
                sign_mask = 0x2000000
                if imm & sign_mask >> 25 == 1:
                    imm = imm ^ 0x3FFFFFF
                    imm += 1
                    imm *= -1
            elif imm.bit_length() == 19:
                sign_mask = 0x40000
                if imm & sign_mask >> 18 == 1:
                    imm = imm ^ 0x7FFFF
                    imm += 1
                    imm *= -1
            return imm

        # Converting the Binary to a spaced string (From Greg) "R" for Instruction Formatting.
        def spaced(s):
            return s[0:32]

        def spaced_r(s):
            return s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]

        def spaced_d(s):
            return s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + s[22:27] + " " + s[27:32]

        def spaced_i(s):
            return s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]

        def spaced_b(s):
            return s[0:6] + " " + s[6:32]

        def spaced_cb(s):
            return s[0:8] + " " + s[8:27] + " " + s[27:32]

        def spaced_im(s):
            return s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + s[27:32]

        def spaced_break(s):
            return s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:32]

        for i in range(len(instructions)):
            opcode.append(int(instructions[i], base=2) >> 21)
        for i in range(len(opcode)):
            if int(opcode[i]) == 1112:
                opcodeStr.append("ADD")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("R" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " "
                                 + argStr1[i] + ", " + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1624:
                opcodeStr.append("SUB")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("R" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) >= 1160 and opcode[i] <= 1161:
                opcodeStr.append("ADDI")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & imMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("R" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("#" + str(twos_complement(arg2[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(twos_complement(arg2[i]))
                addrs.append(-1)
                instrSpaced.append(spaced_i(str(instructions[i])))
                outputFile.write(instrSpaced[i] + " \t" + str(Memory) + "  \t" + opcodeStr[i] + "\t" + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) >= 1672 and opcode[i] <= 1673:
                opcodeStr.append("SUBI")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append(twos_complement(int(instructions[i], base=2) & imMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("R" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("#" + str(twos_complement(arg2[i])))
                instrSpaced.append(spaced_i(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(twos_complement(arg2[i]))
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + " \t" + str(Memory) + "  \t" + opcodeStr[i] + "\t" + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1691:
                opcodeStr.append("LSL")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & shmtMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("#" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1690:
                opcodeStr.append("LSR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & shmtMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("#" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1692:
                opcodeStr.append("ASR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & shmtMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("#" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1104:
                opcodeStr.append("AND")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("R" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1360:
                opcodeStr.append("ORR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("R" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1872:
                opcodeStr.append("EOR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("R" + str(arg1[i]))
                argStr3.append("R" + str(arg2[i]))
                instrSpaced.append(spaced_r(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1986:
                opcodeStr.append("LDUR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append(twos_complement(int(instructions[i], base=2) & addrMask) >> 12)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("R" + str(arg3[i]))
                argStr2.append("[R" + str(arg1[i]))
                argStr3.append("#" + str(arg2[i]) + "]")
                instrSpaced.append(spaced_d(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(arg2[i])
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + "\t" + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) == 1984:
                opcodeStr.append("STUR")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append(twos_complement(int(instructions[i], base=2) & addrMask) >> 12)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("R" + str(arg3[i]))
                argStr2.append("[R" + str(arg1[i]))
                argStr3.append("#" + str(arg2[i]) + "]")
                instrSpaced.append(spaced_d(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(arg2[i])
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + "\t" + argStr1[i] + ", "
                                 + argStr2[i] + ", " + argStr3[i] + "\n")
            elif int(opcode[i]) >= 1440 and opcode[i] <= 1447:
                opcodeStr.append("CBZ")
                arg1.append((int(instructions[i], base=2) & 0x00FFFFE0) >> 5)
                arg2.append(int(instructions[i], base=2))
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg1[i] = twos_complement(arg1[i])
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("#" + str(twos_complement(arg1[i])))
                argStr3.append("")
                instrSpaced.append(spaced_cb(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(twos_complement(arg1[i]))
                src2.append(-1)
                addrs.append(arg1[i])
                outputFile.write(instrSpaced[i] + "  \t" + str(Memory) + "  \t" + opcodeStr[i] + " " + argStr1[i] +
                                 ", " + argStr2[i] + "\n")
            elif int(opcode[i]) >= 1448 and opcode[i] <= 1455:
                opcodeStr.append("CBNZ")
                arg1.append((int(instructions[i], base=2) & 0x00FFFFE0) >> 5)
                arg2.append(twos_complement(int(instructions[i], base=2) & imMask) >> 10)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                arg1[i] = twos_complement(arg1[i])
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("#" + str(twos_complement(arg1[i])))
                argStr3.append("")
                instrSpaced.append(spaced_cb(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(twos_complement(arg1[i]))
                src2.append(-1)
                addrs.append(arg1[i])
                outputFile.write(instrSpaced[i] + "  \t" + str(Memory) + "  \t" + opcodeStr[i] + argStr1[i] + ", "
                                 + argStr2[i] + "\n")
            elif int(opcode[i]) >= 1684 and opcode[i] <= 1687:
                opcodeStr.append("MOVZ")
                arg1.append((int(instructions[i], base=2) & imsftMask) >> 17)
                arg2.append((int(instructions[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("" + "LSL " + str(arg1[i]))
                argStr3.append("" + str(arg2[i]))
                instrSpaced.append(spaced_im(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "  \t" + str(Memory) + "  \t" + opcodeStr[i] + argStr1[i] + ", " +
                                 argStr3[i] + ", " + argStr2[i] + "\n")
            elif int(opcode[i]) >= 1940 and opcode[i] <= 1943:
                opcodeStr.append("MOVK")
                arg1.append((int(instructions[i], base=2) & imsftMask) >> 17)
                arg2.append((int(instructions[i], base=2) & imdataMask) >> 5)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("\tR" + str(arg3[i]))
                argStr2.append("" + "LSL " + str(arg1[i]))
                argStr3.append("" + str(arg2[i]))
                instrSpaced.append(spaced_im(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(arg1[i])
                src2.append(arg2[i])
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "  \t" + str(Memory) + "  \t" + opcodeStr[i] + argStr1[i] + ", " +
                                 argStr3[i] + " " + argStr2[i] + "\n")
            elif int(opcode[i]) >= 160 and opcode[i] <= 191:
                opcodeStr.append("B")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append(twos_complement(int(instructions[i], base=2) & imMask) >> 10)
                arg3.append((int(instructions[i], base=2) & 0x3FFFFFF))
                arg3[i] = twos_complement(arg3[i])
                argStr1.append("\t#" + str(arg3[i]))
                argStr2.append("")
                argStr3.append("")
                instrSpaced.append(spaced_b(str(instructions[i])))
                mem.append(Memory)
                dest.append(arg3[i])
                src1.append(-1)
                src2.append(-1)
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "   \t" + str(Memory) + "  \t" + opcodeStr[i] + "   " + argStr1[i]
                                 + "\n")
            elif int(opcode[i]) == 2038:
                opcodeStr.append("BREAK")
                arg1.append((int(instructions[1], base=2) & specialMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append(" ")
                argStr2.append(" ")
                argStr3.append(" ")
                instrSpaced.append(spaced_break(str(instructions[i])))
                mem.append(Memory)
                num_instrs = len(instructions)
                dest.append(-1)
                src1.append(-1)
                src2.append(-1)
                addrs.append(-1)
                outputFile.write(instrSpaced[i] + "\t" + str(Memory) + "  \t" + opcodeStr[i] + "" + "\n")
            elif int(opcode[i]) == 0:
                opcodeStr.append("NOP")
                arg1.append((int(instructions[1], base=2) & specialMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append(" ")
                argStr2.append(" ")
                argStr3.append(" ")
                dest.append(-1)
                src1.append(-1)
                src2.append(-1)
                addrs.append(-1)
                instrSpaced.append(spaced(str(instructions[i])))
                outputFile.write(instrSpaced[i] + "    \t" + str(Memory) + "  \t" + opcodeStr[i] + "\n")
                mem.append(Memory)
            else:  # Anything that is not an instruction
                opcodeStr.append("-")
                arg1.append((int(instructions[i], base=2) & rnMask) >> 5)
                arg2.append((int(instructions[i], base=2) & rmMask) >> 16)
                arg3.append((int(instructions[i], base=2) & rdMask) >> 0)
                argStr1.append("")
                argStr2.append("")
                argStr3.append("")
                instrSpaced.append(spaced(str(instructions[i])))
                outputFile.write(instrSpaced[i] + "    \t" + str(Memory) + "  \t" + opcodeStr[i] + str(counter) + "\n")
            Memory += 4


if __name__ == '__main__':
    test = Disassembler()
    test.run()

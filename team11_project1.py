import sys
import os

"""Taylor Robbins - tr1231
   Mirna Elizondo - m_e172"""

opcodeStr = []
instrSpaced = []
arg1 = []
arg2 = []
arg3 = []
argStr1 = []
argStr2 = []
argStr3 = []
binMem = []
opcode = []
opcodeStr = []
mem = []
instructions = []

specialMask = 0x1FFFF
rnMask = 0x3E0
rmMask = 0x1F0000
rdMask = 0x1F
imMask = 0x3FFC00
imbMask = 0x3FFFFFC
imcbMask = 0x00FFFFE
shmtMask = 0xFC00
addrMask = 0x1FF000
addr2Mask = 0xFFFFE0
imsftMask = 0x600000
imdataMask = 0x1FFFE0
breakerMask = 0x1FFFFF


class Disassemble:

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
        global input_file
        global output_file
        global instructions
        mem_loc = 96
        cntr = 0

        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                input_file = sys.argv[i + 1]
                print input_file
            elif sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
                output_file = sys.argv[i + 1]

        def get_instr(input_file):
            with open(input_file, 'r') as f:
                for line in f:
                    instructions.append(line)

        def bin2spaced_r(s):
            spacedstr = s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]
            return spacedstr

        def bin2spaced_i(s):
            spacedstr = s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]
            return spacedstr

        def bin2spaced_b(s):
            spacedstr = s[0:6] + " " + s[6:32]
            return spacedstr

        def bin2spaced_cb(s):
            spacedstr = s[0:8] + " " + s[8:27] + " " + s[27:32]
            return spacedstr

        def bin2spaced_d(s):
            spacedstr = s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + s[22:27] + " " + s[27:32]
            return spacedstr

        def bin2spaced_im(s):
            spacedstr = s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + s[27:32]
            return spacedstr

        def bin2Spaced_break(s):
            spacedStr = s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:26] + " " + s[26:32]
            return spacedStr

        def bin2spaced(s):
            spacedStr = s[0:32]
            return spacedStr

        def imm_twos_converter(imm):
            if(imm & 0x800) >> 11 == 1:
                imm = imm ^ 0xFFF
                imm += 1
            else:
                pass
            return imm
        get_instr(input_file)

        with open(output_file, 'w') as o:
            for index in range(len(instructions)):
                opcode.append(int(instructions[index][0:11], base=2))

                if int(opcode[index]) == 1112:
                    opcodeStr.append("ADD")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("R" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                    o.write(
                        instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index] + ", " +
                        argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1624:
                    opcodeStr.append("SUB")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("R" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index]
                            + ", " + argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) >= 1160 and opcode[index] <= 1161:

                    opcodeStr.append("ADDI")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_i(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "" + argStr1[index]
                            + ", " + argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1672:
                    opcodeStr.append("SUBI")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_i(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "" + argStr1[index]
                            + ", " + argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1691:
                    opcodeStr.append("LSL")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & shmtMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index]
                            + ", " + argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1690:
                    opcodeStr.append("LSR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & shmtMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[i]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index]
                            + ", " + argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1104:
                    opcodeStr.append("AND")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("R" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index] + ", "+
                            argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1360:
                    opcodeStr.append("ORR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("R" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index]
                            + ", " +argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1872:
                    opcodeStr.append("EOR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("R" + str(arg1[index]))
                    argStr3.append("R" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index]
                            + ", " +argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1986:
                    opcodeStr.append("LDUR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & addrMask) >> 12)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("R" + str(arg3[index]))
                    argStr2.append("[R" + str(arg1[index]))
                    argStr3.append("#" + str(arg2[index]) + "]")
                    instrSpaced.append(bin2spaced_d(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" +
                            argStr1[index] + ", " +argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) == 1984:
                    opcodeStr.append("STUR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & addr2Mask) >> 12)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("R" + str(arg3[index]))
                    argStr2.append("[R" + str(arg1[index]))
                    argStr3.append("#" + str(arg2[index]) + "]")
                    instrSpaced.append(bin2spaced_d(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" + argStr1[index]
                            + ", " +argStr2[index] + ", " + argStr3[index] + "\n")

                elif int(opcode[index]) >= 1440 and opcode[index] <= 1447:
                    opcodeStr.append("CBZ")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("#" + str(arg1[index]))
                    argStr3.append("")
                    instrSpaced.append(bin2spaced_cb(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" +
                            argStr1[index] + ", " + argStr2[index] + "\n")

                elif int(opcode[index]) >= 1448 and opcode[index] <= 1455:
                    opcodeStr.append("CBNZ")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("#" + str(arg1[index]))
                    argStr3.append("")
                    instrSpaced.append(bin2spaced_cb(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "" + argStr1[index]
                            + ", " +argStr2[index] + "\n")

                elif int(opcode[index]) >= 1684 and opcode[index] <= 1687:
                    opcodeStr.append("MOVZ")
                    arg1.append((int(instructions[index], base=2) & imsftMask) >> 21)
                    arg2.append((int(instructions[index], base=2) & imdataMask) >> 5)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("" + str(arg1[index]))
                    argStr3.append("" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_im(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + argStr1[index]
                            + ", " +argStr3[index] + ", LSL " + argStr2[index] + "\n")

                elif int(opcode[index]) >= 1940 and opcode[index] <= 1943:
                    opcodeStr.append("MOVK")
                    arg1.append((int(instructions[index], base=2) & imsftMask) >> 17)
                    arg2.append((int(instructions[index], base=2) & imdataMask) >> 5)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("" + str(arg1[index]))
                    argStr3.append("" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_im(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + argStr1[index]
                            + ", " +argStr3[index] + ", LSL " + argStr2[index] + "\n")

                elif int(opcode[index]) >= 160 and opcode[index] <= 191:
                    opcodeStr.append("B")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & 0x3FFFFF) >> 0)
                    argStr1.append("\t#" + str(arg3[index]))
                    argStr2.append("")
                    argStr3.append("")
                    instrSpaced.append(bin2spaced_b(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "\t" +
                            argStr1[index] + "\n")

                elif int(opcode[index]) == 2038:
                    opcodeStr.append("BREAK")
                    arg1.append((int(instructions[index], base=2) & breakerMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("")
                    argStr2.append("")
                    argStr3.append("")
                    instrSpaced.append(bin2Spaced_break(instructions[index]))
                    o.write(instrSpaced[index] + "\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + "" + argStr1[index]
                            + "\n")

                else:  # Anything that is not ADD or SU
                    opcodeStr.append("-")
                    cntr += 1
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("" + str(arg3[index]))
                    argStr2.append("" + str(arg1[index]))
                    argStr3.append("")
                    instrSpaced.append(bin2spaced(instructions[index]))
                    o.write(instrSpaced[index] + "\t\t" + str(mem_loc) + "\t\t" + opcodeStr[index] + str(cntr) +
                            "\n")

                mem_loc += 4

if __name__ == '__main__':
    test = Disassemble()
    test.run()

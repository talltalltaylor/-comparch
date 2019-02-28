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

        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                input_file = sys.argv[i + 1]
                print input_file
            elif sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
                output_file = sys.argv[i + 1]

        def get_instr(input_f):
            with open(input_f, 'r') as f:
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
                if opcode[index] == 1112:
                    opcodeStr.append("ADD")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1624:
                    opcodeStr.append("SUB")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1360:
                    opcodeStr.append("ORR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1104:
                    opcodeStr.append("AND")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1872:
                    opcodeStr.append("EOR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1690:
                    opcodeStr.append("LSR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & shmtMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\t#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1691:
                    opcodeStr.append("LSL")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & shmtMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\t#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif opcode[index] == 1692:
                    opcodeStr.append("ASR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & shmtMask) >> 10)
                    argStr1.append("\tR" + str(arg1[index]))
                    argStr2.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))
                elif 1160 <= opcode[index] <= 1161:
                    opcodeStr.append("ADDI")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\t#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_i(instructions[index]))
                elif 1672 <= opcode[index] <= 1673:
                    opcodeStr.append("SUBI")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imMask) >> 10)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\t#" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_i(instructions[index]))
                elif 160 <= opcode[index] <= 191:
                    opcodeStr.append("B")
                    arg1.append('')
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imbMask))
                    arg3.append('')
                    argStr1.append(str(arg1[index]))
                    argStr2.append("\t#" + str(arg2[index]))
                    argStr3.append(str(arg3[index]))
                    instrSpaced.append(bin2spaced_b(instructions[index]))
                elif 1440 <= opcode[index] <= 1447:
                    opcodeStr.append("CBZ")
                    arg1.append((int(instructions[index], base=2) & rdMask) >> 0)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imcbMask) >> 5)
                    arg3.append('')
                    argStr1.append("\tR" + str(arg1[index]))
                    argStr2.append("\t#" + str(arg2[index]))
                    argStr3.append(str(arg3[index]))
                    instrSpaced.append(bin2spaced_cb(instructions[index]))
                elif 1448 <= opcode[index] <= 1455:
                    opcodeStr.append("CBNZ")
                    arg1.append((int(instructions[index], base=2) & rdMask) >> 0)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & imcbMask) >> 5)
                    arg3.append('')
                    argStr1.append("\tR" + str(arg1[index]))
                    argStr2.append("\t#" + str(arg2[index]))
                    argStr3.append(str(arg3[index]))
                    instrSpaced.append(bin2spaced_cb(instructions[index]))
                elif opcode[index] == 1984:
                    opcodeStr.append("STUR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & addrMask) >> 12)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\t[R" + str(arg1[index]) + " ")
                    argStr3.append(" #" + str(arg2[index]) + "]")
                    instrSpaced.append(bin2spaced_d(instructions[index]))
                elif opcode[index] == 1986:
                    opcodeStr.append("LDUR")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append(imm_twos_converter(int(instructions[index], base=2) & addrMask) >> 12)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\t[R" + str(arg1[index]) + " ")
                    argStr3.append(" #" + str(arg2[index]) + "]")
                    instrSpaced.append(bin2spaced_d(instructions[index]))
                elif 1684 <= opcode[index] <= 1687:
                    opcodeStr.append("MOVZ")
                    arg1.append((int(instructions[index], base=2) & imsftMask) >> 21)
                    arg2.append((int(instructions[index], base=2) & imdataMask) >> 5)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\t[R" + str(arg1[index]) + " ")
                    argStr3.append(" #" + str(arg2[index]) + "]")
                    instrSpaced.append(bin2spaced_im(instructions[index]))
                else:
                    opcodeStr.append("NOT YET CLASSIFIED")
                    arg1.append((int(instructions[index], base=2) & rnMask) >> 5)
                    arg2.append((int(instructions[index], base=2) & rmMask) >> 16)
                    arg3.append((int(instructions[index], base=2) & rdMask) >> 0)
                    argStr1.append("\tR" + str(arg3[index]))
                    argStr2.append("\tR" + str(arg1[index]))
                    argStr3.append("\tR" + str(arg2[index]))
                    instrSpaced.append(bin2spaced_r(instructions[index]))

                o.write(instrSpaced[index] + "    " + str(mem_loc) + "   " + opcodeStr[index] + argStr1[index] + ", "
                        + argStr2[index] + " " + argStr3[index] + "\n")
                mem_loc += 4


if __name__ == '__main__':
        test = Disassemble()
        test.run()

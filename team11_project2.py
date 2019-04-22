"""Taylor Robbins
   Mirna Elizondo"""

import disassembler
import sys


class Simulator:

    def __init__(self):
        pass

    def run(self):
        global output_file
        global Memory
        Memory = 96

        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                input_file = sys.argv[i + i]
            elif sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
                output_file = sys.argv[i + 1]

        output_file = open(output_file + "_sim.txt", 'w')
        d = disassembler.Disassembler()
        d.run()

        i = 0
        cycle = 1
        r_32 = [0] * 32
        data = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        data_start = disassembler.Memory
        data_rows = [data_start, data_start + 32, data_start + 64, data_start + 96]

        def write_regs():
            output_file.write(
                "r00: " + str(r_32[0]) + "\t" + str(r_32[1]) + "\t" + str(r_32[2]) + "\t" + str(r_32[3]) + "\t" +
                str(r_32[4]) + "\t" + str(r_32[5]) + "\t" + str(r_32[6]) + "\t" + str(r_32[7]) + "\t" + "\n" +
                "r08: " + str(r_32[8]) + "\t" + str(r_32[9]) + "\t" + str(r_32[10]) + "\t" + str(r_32[11]) + "\t" +
                str(r_32[12]) + "\t" + str(r_32[13]) + "\t" + str(r_32[14]) + "\t" + str(r_32[15]) + "\t" + "\n" +
                "r16: " + str(r_32[16]) + "\t" + str(r_32[17]) + "\t" + str(r_32[18]) + "\t" + str(r_32[19]) + "\t" +
                str(r_32[20]) + "\t" + str(r_32[21]) + "\t" + str(r_32[22]) + "\t" + str(r_32[23]) + "\t" + "\n" +
                "r24: " + str(r_32[24]) + "\t" + str(r_32[25]) + "\t" + str(r_32[26]) + "\t" + str(r_32[27]) + "\t" +
                str(r_32[28]) + "\t" + str(r_32[29]) + "\t" + str(r_32[30]) + "\t" + str(r_32[31]) + "\t" + "\n")

        while True:
            if disassembler.opcodeStr[i] == "ADDI":
                num = disassembler.arg1[i]
                r_32[int(disassembler.arg3[i])] = r_32[num] + int(disassembler.arg2[i])
                output_file.write("====================" + "\n" + "cycle:" + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "ADDI" + "\t" +
                                  str(disassembler.argStr1[i]) + "\t" + str(disassembler.argStr2[i])
                                  + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "B":
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "B" + "\t" + str(disassembler.argStr1[i]) + "\t" +
                                  str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
                offset = disassembler.arg3[i]
                i += offset - 1
            elif disassembler.opcodeStr[i] == "ADD":
                num = disassembler.arg1[i]
                num2 = disassembler.arg2[i]
                r_32[disassembler.arg3[i]] = r_32[num] + r_32[num2]
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "ADD" + "\t" + str(disassembler.argStr1[i])
                                  + "\t" + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data: " + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "SUB":
                num = disassembler.arg1[i]
                num2 = disassembler.arg2[i]
                r_32[disassembler.arg3[i]] = r_32[num] - r_32[num2]
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "SUB" + "\t" + str(disassembler.argStr1[i])
                                  + "\t" + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "SUBI":
                num = disassembler.arg1[i]
                r_32[int(disassembler.arg3[i])] = r_32[num] - int(disassembler.arg2[i])
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "SUBI" + "\t" + str(disassembler.argStr1[i])
                                  + "\t" + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "AND":
                r_32[disassembler.arg3[i]] = disassembler.arg1[i] & disassembler.arg2[i]
                print(r_32[disassembler.arg3[i]])

                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "AND" + "\t" + str(disassembler.argStr1[i])
                                  + "\t" + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "ORR":
                r_32[disassembler.arg3[i]] = r_32[disassembler.arg2[i]] | r_32[disassembler.arg1[i]]
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "ORR" + "\t" + str(disassembler.argStr1[i])
                                  + "\t" + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "EOR":
                r_32[disassembler.arg3[i]] = r_32[disassembler.arg2[i]] ^ r_32[disassembler.arg1[i]]
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "EOR" + "\t" + str(disassembler.argStr1[i])
                                  + "\t" + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "MOVZ":
                num = disassembler.arg1[i]
                num2 = (pow(2, num))
                r_32[disassembler.arg3[i]] = num2 * disassembler.arg2[i]

                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "MOVZ" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr3[i]) + "\t" + str(disassembler.argStr2[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "MOVK":
                # arg2 or the lsl number needs to be 2^arg3 and then multiplied by the value in arg1 stored in arg3
                num = disassembler.arg1[i]
                num2 = (pow(2, num))
                r_32[disassembler.arg3[i]] = num2 * disassembler.arg2[i]
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "MOVK" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr3[i]) + "\t" + str(disassembler.argStr2[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "STUR":
                store = r_32[disassembler.arg3[i]]
                addr = r_32[disassembler.arg1[i]] + disassembler.arg2[i] * 4

                while addr > data_rows[-1]:
                    data_rows.append(data_rows[-1] + 32)
                    data.append([0, 0, 0, 0, 0, 0, 0, 0])

                for index in range(len(data_rows)):
                    if addr > data_rows[index]:
                        continue
                    elif addr < data_rows[index]:
                        row_index = int(index - 1)
                        data_index = int((addr - data_rows[row_index]) / 4)
                        data[row_index][data_index] = store

                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "STUR" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "LDUR":
                addr = r_32[disassembler.arg1[i]] + disassembler.arg2[i] * 4
                for j in range(len(data_rows)):
                    if addr > data_rows[j]:
                        continue
                    elif addr < data_rows[j]:
                        row_index = int(j - 1)
                        data_index = int((addr - data_rows[row_index]) / 4)
                        r_32[disassembler.arg3[i]] = data[row_index][data_index]
                    elif addr > data_rows[-1]:
                        print("Address Out of Range, man")
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "LDUR" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "CBZ":
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" "CBZ" + "\t" + str(disassembler.argStr1[i]) + "\t" +
                                  str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue

                if r_32[disassembler.arg3[i]] == 0:
                    offset = disassembler.arg1[i]
                    i += offset - 1
            elif disassembler.opcodeStr[i] == "CBNZ":

                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "CBNZ" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
                if r_32[disassembler.arg3[i]] != 0:
                    offset = disassembler.arg1[i]
                    i += offset - 1
            elif disassembler.opcodeStr[i] == "ASR":
                num = disassembler.arg2[i]
                num2 = (pow(2, num))
                r_32[disassembler.arg3[i]] = int(disassembler.arg1[i] / num)
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "ASR" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "LSL ":
                num = disassembler.arg2[i]
                num2 = (pow(2, num))
                r_32[disassembler.arg3[i]] = num2 * r_32[disassembler.arg1[i]]
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "LSL" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "LSR ":
                num = disassembler.arg2[i]
                num2 = (pow(2, num))
                r_32[disassembler.arg3[i]] = disassembler.arg1[i] / num
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "LSR" + "\t" + str(disassembler.argStr1[i]) + "\t"
                                  + str(disassembler.argStr2[i]) + "\t" + str(disassembler.argStr3[i]) + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "NOP":
                output_file.write("====================" + "\n" + "cycle " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "NOP" + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
            elif disassembler.opcodeStr[i] == "BREAK":
                output_file.write("====================" + "\n" + "cycle: " + str(cycle) + "\t" +
                                  str(disassembler.mem[i]) + "\t" + "BREAK" + "\n")
                output_file.write("\n" + "registers:" + "\n")
                write_regs()
                output_file.write("\n" + "data:" + "\n")
                for data_list in data:
                    for addi in data_list:
                        if addi != 0:
                            for row, address in zip(data_rows, data):
                                output_file.write(str(row) + ': ')
                                for add in address:
                                    output_file.write(str(add) + '\t')
                                output_file.write('\n')
                        else:
                            continue
                break

            i += 1
            cycle += 1
            Memory += 4


if __name__ == '__main__':
    test = Simulator()
    test.run()

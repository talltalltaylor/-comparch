import disassembler
import sys

cycle = 0
pre_issue_buff = [-1, -1, -1, -1]
pre_alu_buff = [-1, -1]
pre_mem_buff = [-1, -1]
post_mem_buff = [30, 3]
post_alu_buff = [-10, 5]
r = [0] * 32

class Simulator:

    class WB:

        def __init__(self):
            pass

        @staticmethod
        def run():

            if post_alu_buff[1] != -1:
                r[post_alu_buff[1]] = post_alu_buff[0]
                post_alu_buff[0] = -1
                post_alu_buff[1] = -1
            if post_mem_buff[1] != -1:
                r[post_mem_buff[1]] = post_mem_buff[0]
                post_mem_buff[0] = -1
                post_mem_buff[1] = -1

    def __init__(self, instrs, opcodes, mem, addrs, 
    arg1, arg2, arg3, num_instrs, dest, src1, src2, cycle):
        self.instrs = instrs
        self.opcodes = opcodes
        self.mem = mem
        self.addrs = addrs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.num_instrs = num_instrs
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.cycle = cycle
    
    def print_state(self, output_file):
        output_file.write("Cycle: " + str(cycle) + "\n")
        output_file.write("Pre-Issue Buffer:" + "\n")
        for i in range(len(pre_issue_buff)):
            output_file.write("Entry " + str(i) + ":" + str(pre_issue_buff[i]) + "\n")
        output_file.write("Pre_ALU Queue:" + "\n")
        for i in range(len(pre_alu_buff)):
            output_file.write("Entry " + str(i) + ":" + str(pre_alu_buff[i]) + "\n")
        output_file.write("Post_ALU Queue:" + "\n")
        for i in range(len(post_alu_buff)):
            output_file.write("Entry " + str(i) + ":" + str(post_alu_buff[i]) + "\n")
        output_file.write("Pre_MEM Queue:" + "\n")
        for i in range(len(pre_mem_buff)):
            output_file.write("Entry " + str(i) + ":" + str(pre_mem_buff[i]) + "\n")
        output_file.write("Post_MEM Queue:" + "\n")
        for i in range(len(post_mem_buff)):
            output_file.write("Entry " + str(i) + ":" + str(post_mem_buff[i]) + "\n")
        output_file.write("Registers:" + "\n")
        output_file.write("R00:" + "\t")
        for i in range(len(r)):
            if i == 8 or i == 16 or i == 24:
                output_file.write("\n")
                if i == 8:
                    output_file.write("R0" + str(i) + "\t")
                else:
                    output_file.write("R" + str(i) + "\t")
            output_file.write(str(r[i]) + "\t")

    def run(self):

        for i in range(len(sys.argv)):
            if sys.argv[i] == '-i' and i < (len(sys.argv) - 1):
                input_file = sys.argv[i + i]
            elif sys.argv[i] == '-o' and i < (len(sys.argv) - 1):
                output_file = sys.argv[i + 1]
        
        output_file = open(output_file + "_sim.txt", 'w')

        booyakasha = True
        while booyakasha:
            self.WB.run()
            self.print_state(output_file)
            self.cycle += 1
            

    class MEM:

        def __init__(self):
            pass
        
        @staticmethod
        def run():
            print("Do the damn thing")

if __name__ == "__main__":
    d = disassembler.Disassembler()
    d.run()
    s = Simulator(disassembler.instructions, disassembler.opcodeStr, disassembler.mem, disassembler.addrs, disassembler.arg1,
                  disassembler.arg2, disassembler.arg3, disassembler.num_instrs, disassembler.dest, disassembler.src1, 
                  disassembler.src2, 0)
    s.run()    
        
    



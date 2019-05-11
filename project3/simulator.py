import disassembler
import sys

cycle = 0
pre_issue_buff = [-1, -1, -1, -1]
pre_alu_buff = [-1, -1]
pre_mem_buff = [-1, -1]
post_mem_buff = [-1, -1]
post_alu_buff = [-1, -1]
r = [0] * 32

class Simulator:


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
    
    def get_mem_idx(self, address, is_instr):
        if is_instr is False:
            return (address - (96 + (self.num_instrs * 4))) / 4
        else:
            return (address - 96) / 4

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
            

    class MEM:

        def __init__(self):
            pass
        
        @staticmethod
        def run():
            print("Do the damn thing")

    class Cache:

        sets = [[[0,0,0,0,0],[0,0,0,0,0]], [[0,0,0,0,0],[0,0,0,0,0]],
                [[0,0,0,0,0],[0,0,0,0,0]], [[0,0,0,0,0],[0,0,0,0,0]]]
        
        lru = [0,0,0,0]
        tag_msk = 4294967264
        set_msk = 24

        missed_list = []
        
        def __init__(self):
            pass
        @staticmethod
        def flush():
            print("Flush, bitch")

        @staticmethod
        def access_mem(mem_idx, inst_idx, is_write, data_to_write):
            # check if mem or instruction and calculate address
            if mem_idx == -1:
                address_local = 96 + (4 * inst_idx)
            else:
                address_local = 96 + (4 * num_instrs) + (4 * mem_idx)
            
            # figure out which word in the block
            if address_local % 8 == 0:
                data_word = 0
                addr1 = address_local
                addr2 = address_local + 4
            elif address_local % 8 != 0:
                data_word = 1
                addr1 = address_local
                addr2 = address_local + 4

            # if addr1 is instr, get instruction
            # else, get data
            if addr1 < 96 + (4 * num_instrs):
                data1 = instrs[get_mem_idx(addr1, True)]
            else:
                data1 = mem[get_mem_idx(addr1, False)]

            # same thing for addr2
            if addr2 < 96 + (4 * num_instrs):
                data2 = instrs[get_mem_idx(addr2, True)]
            else:
                data2 = mem[get_mem_idx(addr2, False)]
            
            if is_write and data_word == 0:
                data1 = data_to_write
            elif is_write and data_word == 1:
                data2 = data_to_write
            
            # get set and tag for addr1
            set_num = (addr1 & set_msk) >> 3
            tag = (addr1 & tag_msk) >> 5

            if sets[set_num][0][0] == 1 and sets[set_num][0][2] == tag:
                hit = True
                assoc_block = 0
            elif sets[set_num][1][0] == 1 and sets[set_num][1][2] == tag:
                hit = True
                assoc_block = 1

            # if hit, update LRU and dirty bit if is_write = True
            if hit:
                if hit and is_write:
                    sets[set_num][assoc_block][1] = 1
                    lru[set_num] = (assoc_block + 1) % 2
                    sets[set_num][assoc_block][data_word + 3] = data_to_write
                lru[set_num] = (assoc_block + 1) % 2
                return [True, sets[set_num][assoc_block][data_word + 3]]
            else:  # miss
                # if we missed last time, take it out of the list and do the write
                if addr1 in missed_list:
                    while missed_list.count(addr1) > 0:
                        missed_list.remove(addr1)
                    # if dirty bit is 1 do write back    
                    if sets[set_num][lru[set_num]][2] == 1:
                        wb_addr = sets[set_num][lru[set_num]][2]
                        wb_addr = (wb_addr << 5) + (set_num << 3)
                        if wb_addr >= (num_instrs * 4) + 96:
                            mem[get_mem_idx(wb_addr, False)] = sets[set_num][lru[set_num]][3]
                        if wb_addr + 4 >= (num_instrs * 4) + 96:
                            mem[get_mem_idx(wb_addr, False)] = sets[set_num][lru[set_num]][4]

                    # write cache

                    # valid = 1
                    sets[set_num][lru[set_num]][0] = 1
                    # dirty bit = 0 or 1 depending on is_write
                    sets[set_num][lru[set_num]][1] = 0
                    if is_write:
                        sets[set_num][lru[set_num]][1] = 1
                    # write tag, data1 and data2
                    sets[set_num][lru[set_num]][2] = tag
                    sets[set_num][lru[set_num]][3] = data1
                    sets[set_num][lru[set_num]][4] = data2
                    # change lru bit
                    lru[set_num] = (lru[set_num] + 1) % 2

                    return [True, sets[set_num][(lru[set_num] + 1) % 2]][data_word + 3]
                else:
                    if missed_list.count(addr1) == 0:
                        missed_list.append(addr1)
                    return [False, 0]




            


if __name__ == "__main__":
    d = disassembler.Disassembler()
    d.run()
    s = Simulator(disassembler.instructions, disassembler.opcodeStr, disassembler.mem, disassembler.addrs, disassembler.arg1,
                  disassembler.arg2, disassembler.arg3, disassembler.num_instrs, disassembler.dest, disassembler.src1, 
                  disassembler.src2, 0)
    s.run()    
        
    



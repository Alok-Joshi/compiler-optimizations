import json
import sys

class block:
    def __init__(self, block_name, block_list):
        self.block_name = block_name
        self.block_list = block_list

class control_flow_graph:

    def __init__(self, program):

        self.cfg = dict()
        self._program = json.load(program)

        self.blocks = self._get_blocks(self._program[0])
        self.block_lookup = dict()
        #for now, only one function has been supported
        pass

    def _get_blocks(self, function):

        blocks = list()
        block_list = list()
        block_counter = 0;
        current_label = "section"+str(block_counter)

        instructions = function["instrs"]

        for itr in instructions:

            if("op" in itr):
                block_list.append(itr)

            elif ("label" in itr) or (itr["op"] == "jmp") or ( itr["op"] == "br"):

                
                if len(block_list) > 0: 
                    new_block = block(current_label,block_list)
                    self.block_lookup[current_label] = new_block
                    blocks.append(new_block)

                    block_counter += 1
                    block_list = list()

                if("label" in itr):
                    current_label = itr["label"]
                else:
                    current_label = "section" + str(block_counter)

        return blocks;



    def _generate_cfg(self):

        for i in range(len(self.blocks)):

            block_obj = self.blocks[i]
            last_instruction = block_obj.block_list[-1]

            if(last_instruction["op"] == "jmp" or last_instruction["op"] == "br"): #checking for terminator instructions

                self.cfg[self.block_lookup[block_obj.block_name]] = list()

                for label in last_instruction["labels"]:
                    self.cfg[self.block_lookup[block_obj.block_name]].append(label)

            elif i != len(self.blocks) -1:
                #just link it to the next block

                self.cfg[self.block_lookup[block_obj.block_name]] = self.blocks[i+1]








if(__name__ == "__main__"):

    cfg = control_flow_graph(sys.stdin)


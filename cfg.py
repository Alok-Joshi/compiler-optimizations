import json
import sys

class block:
    def __init__(self, block_name, block_list):
        self.block_name = block_name
        self.block_list = block_list

    def __str__(self):

        rep = ""
        rep += self.block_name + '\n'
        rep += str(self.block_list) + '\n'

        return rep

class control_flow_graph:

    def __init__(self, function):

        self.cfg: dict[str,str] = dict()
        self._function = function
        self.block_lookup: dict[str,block] = dict()

        self.blocks = self._get_blocks(self._function)
        self._generate_cfg()
        pass

    def _get_blocks(self, function):

        blocks = list()
        block_list = list()
        block_counter = 0;
        current_label = "section"+str(block_counter)

        instructions = function["instrs"]
        control_instructions = ["jmp","br","ret"]
        #call is not a terminator, as we return back to the basic block after the call is done


        for itr in instructions:

            if("op" in itr):
                block_list.append(itr)

            if ("label" in itr) or (itr["op"] in control_instructions):

                
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

        if len(block_list) > 0: #the last block, as the last block may or may not have a jmp/br instruction

            new_block = block(current_label,block_list)
            self.block_lookup[current_label] = new_block
            blocks.append(new_block)

        return blocks;





    def export(self):
        print('digraph {} {{'.format(self._function["name"]))

        for block in self.blocks:
            print('  {};'.format(block.block_name))

        for label in self.blocks:

            children = self.cfg[label.block_name]

            for node in children:
                print('  {} -> {};'.format(label.block_name,node))
        
            
        print('}')


    def _generate_cfg(self):

        for i in range(len(self.blocks)):

            block_obj = self.blocks[i]
            last_instruction = block_obj.block_list[-1]
            self.cfg[block_obj.block_name] = list()

            if(last_instruction["op"] == "jmp" or last_instruction["op"] == "br"): #checking for terminator instructions

                    self.cfg[block_obj.block_name] = last_instruction["labels"]

            
            elif(last_instruction["op"] == "ret"):
                    self.cfg[block_obj.block_name] = []    


            elif i != len(self.blocks) -1:
                #just link it to the next block

                self.cfg[block_obj.block_name] = [self.blocks[i+1].block_name,]








if(__name__ == "__main__"):



    program = json.load(sys.stdin)
    for function in program["functions"]:
        
        cfg = control_flow_graph(function)
        cfg.export()


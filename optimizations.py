import json
from cfg import block, control_flow_graph
import json
import sys



def dead_code_remover(block_list: list[dict]):


    deletion_candidates: dict[str,int] = dict() #variable name and its corresponding instruction line number
    repeated_candidates = set()
    block_list = list(block_list)


    for i  in range(len(block_list)):

        itr = block_list[i]
        if "args" in itr:

            for arg in itr["args"]:
                
                if arg in deletion_candidates:
                    del deletion_candidates[arg]

        if "dest" in itr:
            if itr["dest"] in deletion_candidates:
                repeated_candidates.add(deletion_candidates[itr["dest"]])

            deletion_candidates[itr["dest"]] = i;




    new_block_list = []
    for line_number in range(len(block_list)):

        itr = block_list[line_number]

        if (line_number in deletion_candidates.values() or line_number in repeated_candidates):
            continue;

        else:
            new_block_list.append(itr)



            





    block_list = new_block_list
    return block_list






if(__name__ == "__main__"):

    program = json.load(sys.stdin)

    for function in program["functions"]:

        cfg = control_flow_graph(function)
        for block in cfg.blocks:

            old_block = block
            while True:

                new_block_list= dead_code_remover(old_block.block_list)
                if(old_block.block_list == new_block_list):
                    break;
                else:
                    old_block.block_list = new_block_list

            print(old_block)

        



        








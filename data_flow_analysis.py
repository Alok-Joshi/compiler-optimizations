import json
import sys
from cfg import control_flow_graph



in_value = dict()
out_value = dict()




def merge(preds: list[str] ):
    
    new_in_value = set()

    for pred in preds:
        
        new_in_value = new_in_value.union(out_value[pred])

    return new_in_value



def transfer(in_value,block):
    """ generates out value """

    out_value = set(in_value)
    for itr in block.block_list:

        if "dest" in itr:
            if(itr["dest"] in out_value):
                out_value.remove(itr["dest"]) #implies this is a kill, its a redefinition
            else:
                out_value.add(itr["dest"]) #implies this is a new definition

    return out_value



def reaching_definitions(cfg:control_flow_graph):
    
    worklist = cfg.blocks


    while len(worklist) > 0:
        block = worklist.pop(0)

        in_value[block.block_name] = merge(block.pred) if(len(block.pred)> 0) else in_value[block.block_name]
        new_out_value = transfer(in_value[block.block_name],block)



        if(new_out_value != out_value[block.block_name]):

            out_value[block.block_name] = new_out_value
            worklist.extend((cfg.block_lookup[successor] for successor in block.succ))

        

    

if __name__ == "__main__":


    program = json.load(sys.stdin)

    for function in program["functions"]:

        cfg = control_flow_graph(function)
        for block in cfg.blocks:
            #print(block.succ)
            #print(block.pred)
            in_value[block.block_name] = set()
            out_value[block.block_name] = set()


        if "args" in function:
            for arg in function["args"]: #generating the seed value in_value for the entry block

                for block in cfg.blocks:
                    if(len(block.pred)  == 0):
                        in_value[block.block_name].add(arg["name"])

        reaching_definitions(cfg)


        for block_name in in_value:

            print(f"{block_name}: ")

            print("In: ",end = '')
            for value in in_value[block_name]:
                print(f"{value} ", end = '')

            print()

            print("Out: ",end = '')
            for value in out_value[block_name]:
                print(f"{value} ", end = '')

            print()
            print()



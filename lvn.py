import json



def get_value(instruction,environment):
        #its either a value or const operation
    
        if(instruction["op"] == "const"):

            value  = ("const",instruction["args"][0])
            return value

        else:

            value = list()
            value.append(instruction["op"])
            args = [arg for arg in instruction["args"]]

            value.extend(args)
            value_tuple = tuple(value)
            return value_tuple


        
        
def find_index(table,value):

    for i in range(len(table)):
        if table[i][0] == value:
            return i;

    return -1;

def local_value_numbering(block):

    environment: dict[str,int] = dict()
    table = list() #table's ith index is a tuple of type [value,canonical_home_variable]


    for itr in block:

        if "dest" in itr:
            #its a value or const operation

            value = get_value(itr,environment)
            value_number = find_index(table,value)
            value_in_table = (value_number > 0)

            if(value_in_table):

                    environment[itr["dest"]] = value_number;
                    #Reconstruction of instruction: id in this case
                    itr["op"] = "id"
                    itr["args"] = [ table[value_number][1] ] 


            else:

                new_value = [value,itr["dest"]]
                table.append(new_value)

                environment[itr["dest"]] = len(table)-1 # pointing the variable to the latest entry, the new value

                #instruction reconstruction
                itr["args"] = [table[environment[arg]][1] for arg in itr["args"]]
                #replacing the variables with their canonical homes



                #TODO: need to consider the case of a variable name being reassigned
                    
                    
                

                






#ifndef CFG_H
#define CFG_H

#include <nlohmann/json.hpp>
#include <string>
#include <vector>
#include <unordered_map>



typedef nlohmann:: json block;

class control_flow_graph {

    
    std:: unordered_map<std:: string, std:: vector<block>> graph;
    //string is the label name, vector<block> are its successor nodes

    std:: vector<block> get_block(nlohmann:: json function); 
    public:
    control_flow_graph(nlohmann::json bril_program);
    

};




#endif

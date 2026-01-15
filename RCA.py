import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from StateSchema import RCAState
from ExtractLog import extractlog
from ExtractSourceCode import extractsourcecode
from GenerateRca import generate_rca

import logging

# Configure the root logger to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize the state graph for the RCA process
graph = StateGraph(RCAState)
graph.add_node('extractlog', extractlog)
graph.add_node('extractsourcecode', extractsourcecode)
graph.add_node('generate_rca', generate_rca)

graph.add_edge(START, 'extractlog')
graph.add_edge('extractlog', 'extractsourcecode')
graph.add_edge('extractsourcecode', 'generate_rca')
graph.add_edge('generate_rca', END)

workflow = graph.compile()

if __name__ == "__main__":
    # specify the log name to start the workflow
    logname = "log3.json"
    initial_state = RCAState(logfile=logname)
    state = workflow.invoke(initial_state)

    # save the response to a file
    # check if RCAoutput folder exists, if not create it
    folder_name = state['logfile'].split(".")[0]
    if not os.path.exists(os.path.join("RCAoutput", folder_name)):
        os.makedirs(os.path.join("RCAoutput", folder_name))
    
    filename = folder_name + '_' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    with open(os.path.join("RCAoutput", folder_name, f"{filename}.txt"), "w") as f:
        f.write(state['rca'])
    
    # dump the entire state to a json file for debugging
    with open(os.path.join("RCAoutput", folder_name, f"{filename}_state.json"), "w") as f:
        json.dump(state, f, indent=4)

    logger.info("Process Completed")
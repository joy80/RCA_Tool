import os
import json
from StateSchema import RCAState
import logging

# Configure the root logger to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extractsourcecode(state: RCAState) -> RCAState:
    try:
    # take sourceclass from state and search the file in ingestion\src folder as {sourceclass}.groovy
        source_class = state.sourceclass
        file_path = os.path.join("ingestion", "src", f"{source_class}.groovy")
        with open(file_path, "r") as file:
            source_code = file.read()
            state.sourcecontext = source_code
            logger.info(f"Extracted source code for class {source_class}")
        return state
    except Exception as e:
        logger.error(f"Error in extractsourcecode: {e}")
        raise e


# initial_state = RCAState(logfile="log1.json", sourceclass="GetUserInfo")
# extractsourcecode(initial_state)
import os
import json
from StateSchema import RCAState
import logging

# Configure the root logger to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extractlog(state: RCAState) -> RCAState:
    try:
        logfile = state.logfile
        with open(os.path.join("ingestion\log", logfile), "r") as file:
            log_data = json.load(file)
        state.timestamp = log_data.get("timestamp", "")
        state.level = log_data.get("level", "")
        state.messege = log_data.get("messege", "")
        state.index = log_data.get("index", "")
        state.sourceclass = log_data.get("class", "")
        state.service = log_data.get("service", "")
        state.stacktrace = log_data.get("stacktrace", "")
        return state
    except Exception as e:
        logger.error(f"Error in extractlog: {e}")
        raise e

# initial_state = RCAState(logfile="log1.json")
# extractlog(initial_state)
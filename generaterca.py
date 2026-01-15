# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import os
from StateSchema import RCAState

import logging

# Configure the root logger to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def generate_rca(state: RCAState) -> RCAState:
    try:
        prompt_str = """Act as a software engineer and Give a detailed root cause analysis (RCA) for the following log entry and 
            Provide Recommended Code fix (if applicable). Output should be concise and to the point for consistent parsing.
            1. Root Cause Analysis:
            2. Recommended Code Fix:
            
            Log Message:{state.messege}
            Log Analysis:{state.stacktrace}
            Source Code Analysis:{state.sourcecontext}
        """
        prompt_str = prompt_str.format(state=state)
        # Initialize Google GenAI client
        logger.info("Calling Google Generative AI model for RCA generation...")
        llm = GoogleGenerativeAI(model="gemini-3-flash-preview", 
                                google_api_key=os.getenv("GOOGLE_API_KEY"),
                                temperature=0.1
                        )
        response = llm.invoke(
                input=prompt_str
        )
        state.rca = response
        return state
    except Exception as e:
        logger.error(f"Error in generate_rca: {e}")
        raise e
    

# initial_state = RCAState(logfile="log1.json")
# generate_rca(initial_state)
    


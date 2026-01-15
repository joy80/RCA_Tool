from typing import TypedDict, Literal
from pydantic import BaseModel, Field


# Define the model for structured output
class RCAState(BaseModel):
    logfile: str = Field(description="The log file name") # make it mandatory
    timestamp: str = Field(default="", description="The timestamp of the log entry")
    level: str = Field(default="", description="The severity level of the log entry")
    messege: str = Field(default="", description="The message content of the log entry")
    index: str = Field(default="", description="The index of the log entry")
    sourceclass: str = Field(default="", description="The class from which the log was generated")
    service: str = Field(default="", description="The service that generated the log")
    stacktrace: str = Field(default="", description="The stack trace of the error")
    sourcecontext: str = Field(default="", description="The source code from which the log was generated")
    rca: str = Field(default="", description="The root cause analysis of the log entry from the LLM")

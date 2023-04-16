
import boto3
from langchain.llms import OpenAI
from typing import Tuple
from uuid import uuid4

import tempfile
import config
import pandas as pd  
from langchain.agents import create_pandas_dataframe_agent

#file_name = f"cost_report.csv" 
s3 = boto3.client('s3')


def get_costs_csv_from_s3():
    response = s3.get_object(Bucket=config.config.BUCKET_NAME, Key=config.config.KEY)
    return response['Body'].read()


PREFIX = '''
You are working with a pandas dataframe in Python that contains AWS Cost Explorer data. The name of the dataframe is `df`.

The data includes various AWS services and their usage costs on different dates. You are an expert in AWS and know all service names

Keep in mind that columns names maybe different from input i.e Column name is "Amazon SageMaker" but input could be "Sagemaker" or "Amazon SageMaker" etc. 

You should use the tools below to answer the question posed of you:

python_repl_ast: A Python shell. Use this to execute python commands. Input should be a valid python command. When using this tool, sometimes output is abbreviated - make sure it does not look abbreviated before using it in your answer.
'''

SUFFIX = '''
Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do
Action: the action to take, should be one of [python_repl_ast]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

This is the result of `print(df.head())`:
{df}

Begin!

Question: {input}
{agent_scratchpad}
'''


def run(api_key: str, session_id: str, prompt: str) -> Tuple[str, str]:
    if not session_id:
        session_id = str(uuid4())

    
    # Step 1: Import the file from S3
    csv_content = get_costs_csv_from_s3()
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp_csv_file:  # Keep the mode as "wb"
        temp_csv_file.write(csv_content)  # Write the content directly as bytes
        temp_csv_file_path = temp_csv_file.name
    df = pd.read_csv(temp_csv_file_path)
    # Step 2: Create a CSV agent and run it with the user's prompt
    #agent = create_csv_agent(OpenAI(temperature=0, openai_api_key=api_key, model_name=config.config.MODEL_NAME), temp_csv_file_path, verbose=True)
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0,openai_api_key=api_key, model_name=config.config.MODEL_NAME), df, verbose=True, prefix=PREFIX, suffix=SUFFIX)

    response = agent.run(prompt)
    print(response)

    return response, session_id

import boto3
from botocore.config import Config
from langchain_aws import ChatBedrock
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM

from typing import List
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_community.utils.math import cosine_similarity
import numpy as np
from src.kevin_function import * 


# import logging
class AWSBedrock(DeepEvalBaseLLM):
    def __init__(
        self,
        model
    ):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "llama-3-1-8b"
    

retry_config = Config(
    retries = {
        'max_attempts': 10,  # Customize the number of retry attempts
        'mode': 'adaptive'   # Or 'adaptive' for dynamically adjusting retries
    }
)

# Initialize the Bedrock client with retry configuration
bedrock_client = boto3.client('bedrock-runtime', config=retry_config)

# Use the ChatBedrock model in LangChain with the client that has retries
llm = ChatBedrock(
    client=bedrock_client,
    model_id="meta.llama3-1-8b-instruct-v1:0",  # Or "meta.llama3-1-70b-instruct-v1:0"
    temperature=0.4,
    max_tokens=None)


def call_function(info: dict):
    query = info["query"]
    answer = info["answer"]
    func_to_call = eval(answer["function"])
    arguments = answer["arguments"]
    return {"query": query, "output": func_to_call(**arguments)}

def generate_response(query_output, llm):
    messages = [
    ("system", f"You are a bot and you should reply to the user based on the function calling return. The return is {query_output["output"]}"),
    ("user", query_output["query"])]
    response = llm.invoke(messages)
    query_output["response"] = response.content
    return query_output




# model for deepeval
aws_bedrock = AWSBedrock(model=llm)

# get metric
def get_relevancy(generated_data):
    try:
        query_output = call_function(generated_data)
        query_response = generate_response(query_output, llm)
        metric = AnswerRelevancyMetric(
            threshold=0.3,
            model=aws_bedrock,
            include_reason=False # can be changed to false later
            )
        
        test_case = LLMTestCase(
            input=query_response["query"],
            actual_output= query_response["response"])
        
        metric.measure(test_case)
        
        return metric.score
    
    except Exception:
        return None
    

class Query(BaseModel):
    """reverse prompt engineering output"""
    query: List[str] = Field(description="list of queries according to the user repsonse")

parser = JsonOutputParser(pydantic_object=Query)
model_id = "amazon.titan-embed-text-v2:0"
embedding = BedrockEmbeddings(model_id=model_id)

def get_reverse_prompt(n, query_response, llm):
    prompt = PromptTemplate(
        template="Guess " + str(n) + "most possible queries based on a user's response.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    query_response["response"]
    prompt_and_model = prompt | llm
    output = prompt_and_model.invoke({"query": query_response["response"]})

    return parser.invoke(output)

def calculate_mean_similiarity(generated_data):
    query_output = call_function(generated_data)
    query_response = generate_response(query_output, llm)
    reverse_queries = get_reverse_prompt(3, query_response, llm)    
    original_embedded = embedding.embed_query(query_response["query"])
    guess_embeded = embedding.embed_documents(reverse_queries["query"])
    
    return np.array([cosine_similarity([original_embedded], [item])[0] for item in guess_embeded]).mean()
    
    
    
    

from langchain.chains import RetrievalQA
from dotenv import load_dotenv, find_dotenv
from src.reranker import get_reranked_docs
from langchain_core.prompts import PromptTemplate
from src.query_enhancement import get_enhanced_query
from openai import OpenAI
from src.prompt_templates import GENERATE_ANSWER_PROMPT_TEMPLATE
import os
# Load the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv('OPENAI_API_KEY')


client = OpenAI(api_key=api_key)

def generate_answer(query):
    enhanced_query = get_enhanced_query(query)
    retrieve_and_rerank = get_reranked_docs(enhanced_query)    
    context = "\n\n".join(retrieve_and_rerank)  # Combine excerpts into a single string
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": GENERATE_ANSWER_PROMPT_TEMPLATE.format(context=context, enhanced_query = enhanced_query)},
            {"role": "user", "content": enhanced_query}
        ]
    )
    return completion.choices[0].message.content

# print(generate_answer("what is indian panel code?"))
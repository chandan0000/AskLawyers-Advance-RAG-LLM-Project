from langchain.chains import RetrievalQA
from dotenv import load_dotenv, find_dotenv
from reranker import get_reranked_docs
from langchain_core.prompts import PromptTemplate
from query_enhancement import get_enhanced_query
from openai import OpenAI
from prompt_templates import GENERATE_ANSWER_PROMPT_TEMPLATE

client = OpenAI()

custom_template = """
You are an helpful assistent of law. Answer query in detail

{context}

{question}
"""

prompt = PromptTemplate(template=custom_template, input_variables=["context", "question"])


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
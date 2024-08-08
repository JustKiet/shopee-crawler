import langchain
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
import json
from Secret.secret import OpenAIKey

from shopee_crawler.json_structure import ProductInfo, DetailedProductInfo

OUTPUT_PATH = "outputs"

# Define model & API key
MODEL = ChatOpenAI(model="gpt-4o-mini",
                   api_key=OpenAIKey())

# LLM Chain
def llm_jsonify(data_path, to_file=False):
    """Description: Extracts product information from a raw content file and converts it into a JSON file."""

    model = MODEL
    
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        data = data_path

    parser = JsonOutputParser(pydantic_object=ProductInfo)

    prompt = PromptTemplate(
        template="You are a data scientist working for a company that sells products online. You have been given the task to extract data from a raw content file and convert it into a JSON file. NOTE: Only follow the instructions, do not say anything more. If the conditions are not met, do not say anything either. Must process ALL the given content, do not mention doing something similar.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    output = chain.invoke({"query": data})

    if to_file:
        with open(os.path.join(OUTPUT_PATH, "llm_output.json"), "w", encoding="utf-8") as file:
            json.dump(output, file, ensure_ascii=False, indent=4)

    return output

def llm_distributor_identifier(data_path):
    """Description: Identifies the distributor of a product from the crawled product information."""

    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        data = data_path
    
    model = MODEL

    parser = StrOutputParser()

    prompt = PromptTemplate(
        template="You are a data scientist working for a company that sells products online. You have been given the task to identify the official distributor of a product based on the product information. NOTE: Only follow the instructions and give ONLY THE OFFICIAL DISTRIBUTOR NAME, do not say anything more. If the conditions are not met, do not say anything either. Must process ALL the given content, do not mention doing something similar.\n{query}\n",
        input_variables=["query"],
    )

    chain = prompt | model | parser

    distributor = chain.invoke({"query": data})

    return distributor

def llm_get_product_detail(data_path, to_file=False):
    """Description: Get product details (manufacturerName, manufacturerLink, additionalInfo, intendedUse) from the crawled product information."""

    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as file:
            data = file.read()
    else:
        data = data_path

    model = MODEL

    parser = JsonOutputParser(pydantic_object=DetailedProductInfo)

    prompt = PromptTemplate(
        template="You are a data scientist working for a company that sells products online. You have been given the task to extract detailed product information from a raw content file. NOTE: Only follow the instructions, do not say anything more. If the conditions are not met, do not say anything either. Must process ALL the given content, do not mention doing something similar.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    output = chain.invoke({"query": data})
    
    if to_file:
        with open('detailed_info.json', 'w', encoding='utf-8') as file:
            json.dump(output, file, ensure_ascii=False, indent=4)

    return output
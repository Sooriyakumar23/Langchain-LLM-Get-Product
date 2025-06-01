import os
import sys
from dotenv import load_dotenv

from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Price in USD")
    detail: str = Field(description="Product detail")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(f"Query: {query}")
    else:
        raise Exception("Please Enter a Query.....")

    parser = JsonOutputParser(pydantic_object=Product)

    prompt = ChatPromptTemplate([
        ("system", "You are a helpful assistant in getting product data."),
        ("user", "Give me the product detail of {query} in {instruction}")
    ])

    llm = ChatGroq(model="qwen-qwq-32b")

    chain = prompt | llm | parser

    result = chain.invoke({"query": query, "instruction": parser.get_format_instructions()})

    print (f"{result['name']} costs around {result['price']} USD. It is {result['detail']}")
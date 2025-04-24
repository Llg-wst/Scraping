import asyncio
from crawl4ai import *
from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI()
load_dotenv()

url = input("Enter your url:")

# implement crawler using crawl4ai
async def crawl( url: str ):
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(
            url = url)
        print(results.markdown)
        return results.markdown


#implememt openai to extract required details from crawled content.
async def extract_ai( content: str ):
    system_prompt= """
            You are a data‐extraction assistant. When given any unstructured text describing
            a business, extract the following fields and return them as a single valid JSON object:

              • business_name      (string or null)
              • address            (string or null)
              • email              (string or null)
              • phone              (string or null)
              • services           (array of strings; empty array if none)
              • opening_hours      (object mapping days to hours; empty object if none)
              • faqs               (array of { "question": string, "answer": string }; empty array if none)

            Rules:
              1. Output only the JSON—no extra commentary.
              2. Use null for missing scalars; empty arrays/objects for missing lists/maps.
              3. Preserve original capitalization and punctuation.
        """

    response = client.responses.create(
        model="gpt-4.1",
        input= [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    print(response.output_text)
    return response.output_text
    
    

# create a function to call both the crawl and extract ai
async def scrape(url: str):
    crawled_content =  await crawl(url)

    structured_data = await extract_ai(crawled_content)

    print(structured_data)
    return structured_data


if __name__ == "__main__":
    asyncio.run(scrape(url))
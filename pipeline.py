import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv(override=True)

open_ai_api_key = os.getenv("OPENAI_API_KEY")
open_ai_base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=open_ai_api_key, base_url=open_ai_base_url)

base_model = os.getenv("BASE_MODEL")


def completion(s_prompt, u_prompt, temperature=0.8):
    completion = client.chat.completions.create(
        model=base_model,
        messages=[
            {"role": "system", "content": s_prompt},
            {"role": "user", "content": u_prompt},
        ],
        temperature=temperature,
    )
    return completion.choices[0].message.content


def get_generate_prompt(city):
    return f"""
    Write a comprehensive article about {city}, one of the most popular cities in the world.
    Cover its history, culture, cuisine, architecture, famous landmarks, neighborhoods, daily life, and what makes it unique.
    Include specific districts, street names, restaurants, and insider details.
    Each part must be at least 3 sentences.
    Write as flowing narrative prose — no headers, no bullet points, no markdown formatting.
    Begin the article immediately without any preamble
    """


def generate():
    article = ""
    system_prompt = "You are a helpful travelling assistant. Output must be returned in UTF-8 chars only.  Use only ASCII punctuation, no curly quotes"
    cities = ["Tokyo", "New York", "London", "Paris", "Dubai"]
    print(f"Start generating article about {len(cities)} cities, please wait...")
    i = 1
    article = f"# {len(cities)} Popular Cities In The World\n\n"
    for city in cities:
        print(f"> generating about {city} ({i}/{len(cities)})")
        article += (
            f"## {city}\n\n"
            + completion(system_prompt, get_generate_prompt(city))
            + f"\n\n"
        )
        print(f"- finished generate about {city}.")
        i += 1

    print(f"finished generating article about {len(cities)} cities.\n\n")

    return article


def summarize(article, max_sentences=15):
    system_prompt = "You are an expert editor. Summarize accurately. Output must be returned in UTF-8 chars only.  Use only ASCII punctuation, no curly quotes"
    user_prompt = f"""Group this article about 5 most popular cities in the world per city, then summarize into {max_sentences} sentences per city.

    Strict rule:
    1. Take most important points including: city uniqueness, 1 iconic landmark, 1 iconic food, 1 iconic culture fact.
    2. Do not include or generate any information not in the article.
    3. Write as flowing paragraphs — no headers, no bullet points, no markdown formatting.
    4. Begin the article immediately without any preamble

    Article:
    ---
    {article}
    ---
    """

    print("Start summarizing article, please wait...")
    sum = completion(system_prompt, user_prompt, temperature=0.3)
    print("finished summarizing article.\n\n")

    return sum


class City(BaseModel):
    name: str
    country: str
    history: str
    culture: str
    uniqueness: str
    iconic_foods: list[str]
    landmarks: list[str]


class CityCollection(BaseModel):
    cities: list[City]


def structurize(article):
    system_prompt = "You are an expert editor. Extract the information based on user message. Output must be returned in UTF-8 chars only.  Use only ASCII punctuation, no curly quotes"

    print("Start structurizing article, please wait...")
    completion = client.chat.completions.parse(
        model=base_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": article,
            },
        ],
        response_format=CityCollection,
    )

    parsed = completion.choices[0].message.parsed
    print("finished structurizing article.\n\n")
    return parsed

article = generate()
summarized = summarize(article, 10)
structurized = structurize(summarized).model_dump_json(indent=2)
print(structurized)

with open("output.txt", "w", encoding="utf-8-sig") as f:
    f.write(structurized)


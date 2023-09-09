#! /bin/python3

import http.client
import json
import argparse
import asyncio
from typing import Union
from os import getenv
from sys import stderr, stdout

API_KEY = getenv("WEATHER_API_KEY")

async def query_api(query: str) -> str:
    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
    }


    conn.request("GET", f"/current.json?q={query}", headers=headers)

    res = conn.getresponse()

    data = json.loads(res.read())

    return data

def process_response( response:dict ) -> str:
    output = ""


    if response.get("error"):
        code, message = response.get( "error" ).values()
        print(f"ERROR {code}: {message}", file=stderr)
        return

    name = response.get( "location" ).get( "name" ).capitalize()
    text = response.get( "current" ).get( "condition" ).get( "text" ).lower()

    output = f"In { name } it is { text }"

    return output



async def process_input(query:Union[ str, list[str] ]) -> list[str]:
    output = []


    queries = [query_api(q) for q in query]
    responses = await asyncio.gather(*queries)

    for response in responses:
        data = process_response(response)

        if data:
            output.append(data)

    return output




async def main():

    parser = argparse.ArgumentParser(
            description="Check the weather in the given city",
            )
    parser.add_argument("city", nargs="+")
    parser.add_argument("-o", "--output", action="store")

    args = parser.parse_args()

    city_name = args.city


    output = await process_input(city_name)


    if args.output:
        with open(args.output, "w") as file:
            file.writelines(output)
    else:
        for line in output:
            print(line, file=stdout)


if __name__ == "__main__":
    asyncio.run( main() )

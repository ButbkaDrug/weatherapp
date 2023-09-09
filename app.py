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

def process_response( response:dict ) -> Union[str, None]:
    output = ""


    if response.get("error"):
        code, message = response.get( "error" ).values()
        print(f"ERROR {code}: {message}", file=stderr)
        return

    current = response.get( "current" )

    name = response.get( "location" ).get( "name" ).capitalize()
    text = current.get("condition").get( "text" ).lower()
    temp = current.get("temp_c")
    feels_like = current.get("feelslike_c")
    speed = current.get("wind_kph")
    humidity = current.get("humidity")

    output = f"In { name } it is { text }. Temperature is {temp} C, feels like {feels_like}. Wind speed is {speed} km/h. Humidity is {humidity}%"

    return output

def sort_results(results:list[dict], key:str) -> None:

    def sort_by_key(entry:Union[dict, None]) -> int:
        if entry.get("error"):
            return 0
        return entry.get("current").get(key)

    return results.sort( key=sort_by_key)




async def process_input(query: list[str], sort_by:str=None ) -> list[str]:
    output = []


    queries = [query_api(q) for q in query]
    responses = await asyncio.gather(*queries)

    if sort_by:
        sort_results(responses, sort_by)


    for response in responses:
        data = process_response(response)

        if data:
            output.append(data)

    return output




async def main():

    parser = argparse.ArgumentParser(
            description="Check the weather in the given city",
    )
    sort_keys = parser.add_mutually_exclusive_group()

    parser.add_argument("city", nargs="+")
    parser.add_argument("-o", "--output", action="store")
    sort_keys.add_argument("-t", "--sort-by-temperature", action="store_const", const="temp_c")
    sort_keys.add_argument("-w", "--sort-by-wind-speed", action="store_const", const="wind_kph")
    sort_keys.add_argument("-u", "--sort-by-humidity", action="store_const", const="humidity")

    args = parser.parse_args()

    city_name = args.city


    sort_group = [
            args.sort_by_temperature,
            args.sort_by_wind_speed,
            args.sort_by_humidity
    ]

    key: str = None

    if any(sort_group):
        key = [x for x in sort_group if x].pop()




    output = await process_input(city_name, key)


    if args.output:
        with open(args.output, "w") as file:
            file.writelines(output)
    else:
        for line in output:
            print(line, file=stdout)


if __name__ == "__main__":
    asyncio.run( main() )

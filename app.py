#! /bin/python3

import http.client
import json
import argparse
from os import getenv

API_KEY = getenv("WEATHER_API_KEY")

def main():

    parser = argparse.ArgumentParser(
            description="Check the weather in the given city",
            )
    parser.add_argument("city")

    args = parser.parse_args()

    if not args.city:
        city_name = input("Please, provide the name of the city: ")
    else:
        city_name = args.city

    conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
    }


    conn.request("GET", f"/search.json?q={city_name}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    if len(data.decode("utf-8")) < 3:
        print(f"I'm sorry. No city called {city_name} were found!")
        exit()



    conn.request("GET", f"/current.json?q={city_name}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(json.loads(data))

if __name__ == "__main__":
    main()

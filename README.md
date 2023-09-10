# WeatherApp

WeatherApp is a simple python script to fetch the weather data from **weatherapi** via **rapidapi** service. To use the script, you need to register with rapidapi(free) and sign up for weatherapi(free). Then provide your API key. Only standard python modules are used, so that you don't have to install any additional packages. 

You can fetch data by city name, airport code, and more. Multiple locations can be fetched at once. The app uses asyncio to speed up the process.

I wrote it mostly for personal use, but anyone who finds it useful is welcomed to use it. 

Usage example:

```bash

$ python3 weatherapp.py London "San Francisco" Dubai

```

output would be like:
```bash
It is partly cloudy in London. Temperature is 17.0 C, feels like 17.0. Wind speed is 4.0 km/h. Humidity is 88%
It is partly cloudy in San francisco. Temperature is 15.0 C, feels like 14.5. Wind speed is 19.1 km/h. Humidity is 93%
It is sunny in Dubai. Temperature is 34.0 C, feels like 44.5. Wind speed is 11.2 km/h. Humidity is 67%
```
You can also sort output using -t to sort by temperature, -w will sort by wind speed and -u will sort by humidity. 

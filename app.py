import http.client

conn = http.client.HTTPSConnection("weatherapi-com.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "2087f67ac9msh21efbd395e4dc40p1e3dd6jsn1dfac09a3a5d",
    'X-RapidAPI-Host': "weatherapi-com.p.rapidapi.com"
}

conn.request("GET", "/current.json?q=53.1%2C-0.13", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

def advanced_weather(location = "cincinnati"):
    """""""""""""""
    Soup stuff
    """""""""""""""

    try:
        from bs4 import BeautifulSoup
    except:
        import os
        os.system("python3 -m pip install beautifulsoup4")
        from bs4 import BeautifulSoup
        
    import requests

    if "cincinnati" in location.lower():
        url = ("https://weather.com/weather/hourbyhour/l/229496fea2153559a056b812ded2a50721c9ae6c4a60ff800179cca93ec56caa")
    else:
        #resort to cincinnati if there is no other locaton
        url = ("https://weather.com/weather/hourbyhour/l/229496fea2153559a056b812ded2a50721c9ae6c4a60ff800179cca93ec56caa")
    
    r  = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data)
    #print(soup)

    """""""""""""""
    Get table
    """""""""""""""

    table = soup.find_all('table')[0]
    info = table.find_all('td')

    """""""""""""""
    Get individual data
    """""""""""""""

    time = str(info[1].find_all("span")[0])[23:]#time for aproximate

    description = str(info[2].find_all("span")[0])[6:]#what the wether is outside
    rain_chance = str(info[5].find_all("span")[2])[6:]#%chance for rain
    wind = str(info[7].find_all("span")[0])[15:]# wind (direction speed mph)

    temp_F = str(info[3].find_all("span"))[16:]#temp in F
    temp_F_feals = str(info[4].find_all("span"))[16:]#feels like in F
    humidity = str(info[6].find_all("span")[0])[21:]# % humidity

    """""""""""""""
    Cleanup
    """""""""""""""

    time = time[:time.index('<')]

    description = description[:description.index('<')]
    rain_chance = rain_chance[:rain_chance.index('<')]
    wind = wind[:wind.index('<')]

    temp_F = temp_F[:temp_F.index('<')]
    temp_F_feals = temp_F_feals[:temp_F_feals.index('<')]
    humidity = humidity[:humidity.index('<')]

    """""""""""""""
    Show
    """""""""""""""

    print("Time for estamate:",time)
    print("Weather outside:",description,"   Rain chance:",rain_chance,"   Wind: ",wind)
    print("Tempeture:",temp_F,"   Feels like:",temp_F_feals,"   Humidity:",humidity)
    data = {"Time":time,"Description": description, "Rain": rain_chance, "Wind": wind, "Temp": temp_F, "Feels": temp_F_feals, "Humidity": humidity}

    return(data)


if __name__ == "__main__":
    advanced_weather()
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_num_from_string(s):
    match = re.search(r"[-+]?\d*\.\d+|\d+", s)
    return float(match.group()) 


def fetch_data( StationID, Prov, Month, Year):
    base_url = "https://climate.weather.gc.ca/climate_data/daily_data_e.html?"
    params = {
        "StationID": StationID,
        "Prov": Prov,
        "searchType": "stnName",
        "optLimit": "yearRange",
        "Month": Month,
        "Year": Year
    }
    query_string = urlencode(params)
    url = f"{base_url}{query_string}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"error accessing info from {StationID}, {Prov}, {Month}, {Year}")    
    return response.text

def get_nums_from(data):
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find("table")
    rows = table.find_all("tr")
    # each Item is the amount of snow on the ground (cm) in a day that had snow on ground
    snow_measures = []
    isCredible = True

    for row in rows:
        tds = row.find_all("td")
        if len(tds) != 11:
            continue
        cell_data = tds[8].text.strip()
        if cell_data.isnumeric():
            num = int(cell_data)
            if num > 0:
                snow_measures.append(num)
        relevant_tds = [b.text.strip() for b in rows[-4].find_all("td")]
        try:
            total_rain, total_snow, total_precip = map(get_num_from_string, relevant_tds[5:8])
        except: 
            total_rain, total_snow, total_precip, isCredible = 0,0,0, False
        
   
    return snow_measures, total_rain, total_snow, total_precip, isCredible



def get_annual_data(StationID, Prov, Year, verbose):
    
    annual_snowy_days = 0
    annual_total_rain = 0
    annual_total_snowfall = 0
    annual_total_percip = 0
    isYearCredible = "True"

    
    for Month in range(1, 13):
        if verbose==True:
            if (isYearCredible == "True"):
                sentence = "we got full data so far"
            else:
                sentence = "some data is missing"
            print((f"Getting Data for {Month}/{Year}, {sentence}"))

           
        data = fetch_data(StationID, Prov, Month, Year)
        try:
            snow_measures, total_rain, total_snow, total_precip, isCredible = get_nums_from(data)
        except:
            verbose and print(f"Too much data is missing for {Year}")
            return None

        if isCredible == "True":
            isYearCredible = "False"
        
        annual_snowy_days += len(snow_measures)
        annual_total_rain += total_rain
        annual_total_snowfall += total_snow
        annual_total_percip += total_precip
    
    if verbose == "little":
        if (isYearCredible):
            sentence = "we got full data so far"
        else:
            sentence = "we are not sure about the numbers though"
            print((f"Getting Data for {Year}, {sentence}"))
    
  
    return annual_snowy_days, round(annual_total_rain), round(annual_total_snowfall), round(annual_total_percip), isYearCredible


def main(StationID, Province, fromYear, toYear, verbose=False):
    rows = []
    yearsRange = list(range(fromYear, toYear + 1))
    years_to_present = []
    for Year in yearsRange:
        row = get_annual_data(StationID, Province, Year, verbose)
        if row != None:
            years_to_present.append(Year)
            rows.append(row)
       
  
    
    columns = 'snowy days', 'tot rain (mm)', 'tot snowfall (cm)', 'tot percip', 'full data?'
    df = pd.DataFrame(data=rows, index=years_to_present, columns=columns)
    df.loc['average'] = df.mean(numeric_only=True)

    return df

###############################################################

#### Enter years station and province
## Verbose could be True, False or "little"
# Results notes:
# snowy days (how many days had snow on the ground), 
# full data - sometimes days are missing in which case we assume 0 percipitation -
# and the year would have full data False.

###############################################################

result = main(50089, "NL", 2014, 2021, "little")
print(result)
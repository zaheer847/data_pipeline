import requests
import pandas as pd

def fetch_user_data():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    user_data = response.json()
    # print('\nStart\n',user_data,'\nEnd\n')
    user_data = pd.DataFrame(user_data)
    user_data = user_data[['id','name','username','email','address']].rename(columns={'id': 'customer_id'})
    return user_data


def merge_data_with_users():
    sales_data = pd.read_csv('sales_data.csv')
    merged_data = pd.merge(sales_data, fetch_user_data(), on='customer_id')
    return merged_data

def fetch_weather_data():
    merged_data = merge_data_with_users()
    merged_data = merged_data.assign(weather_description='Weather_description_None')
    api_key = "8a07d17a778413731d4440c41812b402"
    for index, row in merged_data.iterrows():
        lat = row['address']['geo']['lat']
        lon = row['address']['geo']['lng']
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]
        merged_data.at[index, 'temperature'] = temperature
        print(merged_data)
        merged_data.at[index,'weather_description'] = description
    return merged_data



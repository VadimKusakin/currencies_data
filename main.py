import pandas as pd
from datetime import datetime
import os
from sqlalchemy import create_engine

start_date = "30/12/2023" # С 31.12.2023 по 10.01.2024 нет данных, поэтому для дальнейшего заполнения используем более раннюю дату
# start_date = "01/01/2024"
end_date = datetime.today().strftime("%d/%m/%Y")

url = 'https://cbr.ru/scripts/XML_val.asp?d=0' 
currency_ids = pd.read_xml(url, encoding='cp1251') # Получаем данные с id для всех валют

# Получение данных валюты за период
def get_data(currency, start_date, end_date):
    currency_id = currency_ids.loc[currency_ids['Name'] == currency, 'ID'].values[0]
    currency_url = f'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={end_date}&VAL_NM_RQ={currency_id}'
    currency_data = pd.read_xml(currency_url, encoding='cp1251')
    return currency_data

date_range = pd.date_range(start=start_date, end=end_date, freq='D') # Создаем столбец с каждым числом
df = pd.DataFrame({'Date': date_range.strftime('%d.%m.%Y')})

currencies = ["Вон Республики Корея", "Евро", "Доллар США"]

for currency in currencies:
    currency_data = get_data(currency, start_date, end_date) 
    df = df.merge(currency_data[['Date', 'VunitRate']], on='Date', how='left') # Соединяем с каждым числом
    df = df.rename(columns={'VunitRate': currency})

df.ffill(inplace=True) # Заполняем пропуски предыдущими значениями
df = df.iloc[2:].reset_index(drop=True) # Удаляем строки 30.12.2023 и 31.12.2023
print(df)

# Параметры подключения к MySQL
db_user = os.environ.get("MYSQL_USER")
db_password = os.environ.get("MYSQL_PASSWORD")
db_host = os.environ.get("MYSQL_HOST")
db_name = os.environ.get("MYSQL_DATABASE")

# Подключение
connection_string = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(connection_string)

# Загрузка данных
df.to_sql("currency_data", engine, if_exists="replace", index=False)
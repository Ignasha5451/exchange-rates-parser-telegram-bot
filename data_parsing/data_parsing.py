import json
import datetime

import requests
from bs4 import BeautifulSoup

from database.CRUD import create_instance


async def parsing() -> None:
    url = "https://www.google.com/finance/quote/USD-UAH"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", string=lambda text: text and "AF_initDataCallback({key: 'ds:10'" in text)
    script_content = script_tag.string

    data_list = json.loads(
        script_content[script_content.index("["):script_content.rindex("]") + 1]
    )[0][0][3][0][1]

    for exchange_rate in data_list:
        year, month, day, hour, minute = map(lambda elem: elem if elem else 0, exchange_rate[0][:5])
        date_time = datetime.datetime(year, month, day, hour, minute)

        await create_instance(date_time=date_time, exchange_rate=exchange_rate[1][0])

from datetime import datetime

import pandas as pd

from database.CRUD import read_instances


async def xlsx_creating() -> None:
    query = await read_instances()
    hour = 0
    index = 0
    data = []
    while index < len(query):
        model_instance = query[index][0]
        if hour < model_instance.datetime.hour:
            date_time = datetime(
                model_instance.datetime.year,
                model_instance.datetime.month,
                model_instance.datetime.day,
                hour,
                0,
                0
            )
            data.append({"datetime": f"{date_time}", "exchange_rate": model_instance.exchange_rate})
            hour += 1
        elif hour == model_instance.datetime.hour:
            data.append({"datetime": f"{model_instance.datetime}", "exchange_rate": model_instance.exchange_rate})
            hour += 1
        else:
            index += 1
    while hour <= datetime.now().hour:
        date_time = datetime(
            query[-1][0].datetime.year,
            query[-1][0].datetime.month,
            query[-1][0].datetime.day,
            hour,
            0,
            0
        )
        data.append({"datetime": f"{date_time}", "exchange_rate": query[-1][0].exchange_rate})
        hour += 1
    df = pd.DataFrame(data)

    df.to_excel("data_parsing/exchange_rates/exchange_rates.xlsx", index=False)

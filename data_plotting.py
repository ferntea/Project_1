import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pytz

def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создаёт график, отображающий цены закрытия и скользящие средние, и сохраняет его в файл.

    Параметры:
    data (DataFrame): Данные об акциях, включая цены закрытия и скользящие средние.
    ticker (str): Тикер акции, который будет отображён на графике.
    period (str): Период времени, который будет отображён на графике.
    filename (str, опционально): Имя файла для сохранения графика. Если не указано,
                                  имя файла генерируется автоматически.

    Возвращает:
    None
    """
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Цена закрытия')
            plt.plot(dates, data['Moving_Average'].values, label='Скользящее среднее')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Цена закрытия')
        plt.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')

    # Get current time in Moscow timezone
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz).strftime("%Y%m%d_%H%M%S")

    if filename is None:
        filename = f"results/{ticker}_{period}_stock_price_chart_{current_time}.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")

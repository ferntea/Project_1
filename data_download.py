import os
import pandas as pd
import yfinance as yf

def fetch_stock_data(ticker, period='1mo'):
    """
    Получает исторические данные об акциях для указанного тикера и временного периода.

    Параметры:
    ticker (str): Тикер акции, например 'AAPL'.
    period (str): Период времени для получения данных, по умолчанию '1mo'.

    Возвращает:
    DataFrame: Данные об акциях в формате DataFrame.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def add_moving_average(data, window_size=5):
    """
    Добавляет колонку со скользящим средним к данным о ценах закрытия.

    Параметры:
    data (DataFrame): Данные об акциях, включая цены закрытия.
    window_size (int): Размер окна для расчёта скользящего среднего, по умолчанию 5.

    Возвращает:
    DataFrame: Данные об акциях с добавленной колонкой скользящего среднего.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    """
    Рассчитывает и отображает среднюю цену закрытия акций за заданный период.

    Параметры:
    data (DataFrame): Данные об акциях, включая цены закрытия.
    """
    average_price = data['Close'].mean()
    print(f"\nСредняя цена закрытия акций за заданный период: {average_price:.2f}\n")

def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.

    Параметры:
    data (DataFrame): Данные об акциях, включая цены закрытия.
    threshold (float): Порог колебаний в процентах.
    """
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    fluctuation = ((max_price - min_price) / min_price) * 100  # Calculate percentage fluctuation

    if fluctuation > threshold:
        print(f"Уведомление: Цена акций колебалась более чем на {threshold}% за период. "
              f"Максимальная цена: {max_price:.2f}, Минимальная цена: {min_price:.2f}, "
              f"Общее колебание: {fluctuation:.2f}%")

def export_data_to_csv(data, filename):
    """
    Сохраняет данные об акциях в CSV файл в директории /results.

    Параметры:
    data (DataFrame): Данные об акциях, которые нужно сохранить.
    filename (str): Имя файла для сохранения данных.
    """
    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')

    # Create the full path for the CSV file
    full_path = os.path.join('results', filename)

    # Save DataFrame to CSV, including the index
    data.to_csv(full_path, index=True)
    print(f"Данные сохранены в файл: {full_path}")

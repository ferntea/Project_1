import os
import pandas as pd
import yfinance as yf  # Assuming you're using yfinance to fetch stock data

import pandas as pd
import yfinance as yf


def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    """
    Получает данные о акциях для заданного тикера.

    :param ticker: Тикер акции (например, 'AAPL')
    :param period: Предустановленный период для данных (например, '1mo', '1y')
    :param start_date: Дата начала для пользовательского диапазона дат (формат: 'YYYY-MM-DD')
    :param end_date: Дата окончания для пользовательского диапазона дат (формат: 'YYYY-MM-DD')
    :return: DataFrame, содержащий данные о акциях
    """
    if period:
        # Fetch data using predefined period
        stock_data = yf.download(ticker, period=period)
    elif start_date and end_date:
        # Fetch data using custom date range
        stock_data = yf.download(ticker, start=start_date, end=end_date)
    else:
        raise ValueError("Either period or both start_date and end_date must be provided.")

    return stock_data

def export_data_to_csv(data, filename):
    """
    Экспортирует данные об акциях в CSV файл

    Параметры:
    data (DataFrame): Данные о акциях для экспорта.
    filename (str): Имя файла для сохранения данных.
    """
    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')

    # Save the data to the specified CSV file in the results directory
    filepath = os.path.join('results', filename)
    data.to_csv(filepath)
    print(f"Данные сохранены в файл: {filepath}")

def calculate_and_display_average_price(data, ticker):
    """
    Рассчитывает и отображает среднюю цену закрытия

    Параметры:
    data (DataFrame): Данные о акциях.
    ticker (str): Символ тикера акции для доступа к правильному столбцу.
    """
    print("Структура DataFrame:")
    print(data.head())  # Показать первые несколько строк DataFrame
    print("Столбцы DataFrame:", data.columns)  # Показать столбцы в DataFrame

    # Access the 'Close' column using the MultiIndex
    close_column = ('Close', ticker)
    if close_column not in data.columns:
        raise ValueError(f"DataFrame должен содержать столбец '{close_column}'.")

    # Убедитесь, что столбец 'Close' является числовым
    data[close_column] = pd.to_numeric(data[close_column], errors='coerce')

    average_price = data[close_column].mean()  # Это должно вернуть скалярное значение
    if pd.isna(average_price):
        print("Не удалось рассчитать среднюю цену закрытия. Проверьте данные.")
    else:
        print(f"Средняя цена закрытия: {average_price:.2f}")

def add_moving_average(data, ticker, window=20):
    """
    Добавляет скользящее среднее к данным о акциях.

    Параметры:
    data (DataFrame): Данные о акциях.
    ticker (str): Символ тикера акции для доступа к правильному столбцу.
    window (int): Размер окна для скользящего среднего.

    Возвращает:
    DataFrame: Данные о акциях с добавленным столбцом скользящего среднего.
    """
    close_column = ('Close', ticker)
    data['Moving_Average'] = data[close_column].rolling(window=window).mean()
    return data

def calculate_rsi(data, ticker, window=14):
    """
    Рассчитывает индекс относительной силы (RSI) для данных о ценах закрытия.

    Параметры:
    data (DataFrame): Данные о акциях, включая цены закрытия.
    ticker (str): Символ тикера акции для доступа к правильному столбцу.
    window (int): Период для расчета RSI, по умолчанию 14.

    Возвращает:
    DataFrame: Данные о акциях с добавленным столбцом RSI.
    """
    close_column = ('Close', ticker)
    delta = data[close_column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def calculate_macd(data, ticker):
    """
    Рассчитывает MACD для данных о ценах закрытия.

    Параметры:
    data (DataFrame): Данные о акциях, включая цены закрытия.
    ticker (str): Символ тикера акции для доступа к правильному столбцу.

    Возвращает:
    DataFrame: Данные о акциях с добавленным столбцом MACD и сигнальной линией.
    """
    close_column = ('Close', ticker)
    exp1 = data[close_column].ewm(span=12, adjust=False).mean()
    exp2 = data[close_column].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data

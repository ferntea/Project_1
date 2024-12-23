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

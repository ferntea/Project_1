import os
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import pytz

def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создаёт график, отображающий цены закрытия, скользящие средние, RSI и MACD, и сохраняет его в файл.

    Параметры:
    data (DataFrame): Данные о акциях, включая цены закрытия и индикаторы.
    ticker (str): Тикер акции, который будет отображён на графике.
    period (str): Период времени, который будет отображён на графике.
    filename (str, опционально): Имя файла для сохранения графика. Если не указано,
                                  имя файла генерируется автоматически.

    Возвращает:
    None
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # График цены закрытия и скользящего среднего
    ax1.plot(data.index, data['Close'], label='Цена закрытия', color='blue')
    ax1.plot(data.index, data['Moving_Average'], label='Скользящее среднее', color='orange')
    ax1.set_title(f"{ticker} Цена акций с течением времени")
    ax1.set_ylabel("Цена")
    ax1.legend()

    # График RSI
    ax2.plot(data.index, data['RSI'], label='RSI', color='orange')
    ax2.axhline(70, linestyle='--', alpha=0.5, color='red', label='Перепроданность')
    ax2.axhline(30, linestyle='--', alpha=0.5, color='green', label='Перекупленность')
    ax2.set_title('Индекс относительной силы (RSI)')
    ax2.set_ylabel("RSI")
    ax2.legend()

    # График MACD
    ax3.plot(data.index, data['MACD'], label='MACD', color='blue')
    ax3.plot(data.index, data['Signal_Line'], label='Сигнальная линия', color='red')
    ax3.set_title('MACD')
    ax3.set_ylabel("MACD")
    ax3.legend()

    plt.xlabel("Дата")

    # Убедитесь, что директория для результатов существует
    if not os.path.exists('results'):
        os.makedirs('results')

    # Получите текущее время в московском часовом поясе
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz).strftime("%Y%m%d_%H%M%S")

    if filename is None:
        filename = f"results/{ticker}_{period}_stock_price_chart_{current_time}.png"

    plt.tight_layout()  # Настройка макета для предотвращения наложения
    plt.savefig(filename)
    plt.close()  # Закрыть фигуру, чтобы освободить память
    print(f"График сохранен как {filename}")

import data_download as dd
import data_plotting as dplt
from datetime import datetime


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: "
          "AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), "
          "AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: "
          "1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")
    print("Вы также можете ввести конкретные даты начала и окончания для анализа.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    # Ask user if they want to use a custom date range
    use_custom_dates = input("Хотите ли вы указать конкретные даты начала и окончания? (да/нет): ").strip().lower()

    if use_custom_dates == 'да':
        start_date = input("Введите дату начала (в формате YYYY-MM-DD): ")
        end_date = input("Введите дату окончания (в формате YYYY-MM-DD): ")
        period = None  # No predefined period since we are using custom dates
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        start_date = None
        end_date = None

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)

    # Check if stock_data is None or empty
    if stock_data is None or stock_data.empty:
        print("Не удалось получить данные о акциях. Проверьте тикер и период.")
        return

    # Generate filename with current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
    filename = f"{ticker}_{'custom_dates' if use_custom_dates == 'да' else period}_stock_data_{current_time}.csv"  # Create the filename

    # Export stock data to CSV file
    dd.export_data_to_csv(stock_data, filename)

    # Calculate and display average closing price
    dd.calculate_and_display_average_price(stock_data, ticker)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data, ticker)  # Pass ticker here

    # Calculate RSI and MACD
    stock_data = dd.calculate_rsi(stock_data, ticker)  # Pass ticker here
    stock_data = dd.calculate_macd(stock_data, ticker)  # Pass ticker here

    # Check if stock_data is still valid after calculations
    if stock_data is None or stock_data.empty:
        print("Ошибка при расчете индикаторов. Проверьте данные.")
        return

    # Ask user for plot style
    plot_style = input(
        "Введите стиль графика (например, 'ggplot', 'classic', 'bmh', 'dark_background'): ").strip()

    # Plot the data
    print("Сохранение графика...")
    dplt.create_and_save_plot(stock_data, ticker, period, plot_style)


if __name__ == "__main__":
    main()

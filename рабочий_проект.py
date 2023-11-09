import streamlit as st
import yfinance as yf
import plotly.express as px
from datetime import date, timedelta, datetime
import pandas as pd

file_path = 'SMLNK.xlsx'
df = pd.read_excel(file_path)
st.title("Относительное изменение активов во времени")
currencies = ["USD", "RUB", "BTC", "GOLD", "CHF", "SMLNK", "CTWK"]
strategies = ['Лучший результат', 'Худший результат', 'Бездействие', 'Самостоятельные решения']
st.sidebar.title('Меню настроек')
asset_on_hands = st.sidebar.number_input("Введите количество у.е. Вашего актива:")
selected_currency = st.sidebar.selectbox("Условные единицы в:", currencies, index=0)
other_currencies = st.sidebar.multiselect("Активы:", currencies, default=currencies[1:])
start_date = st.sidebar.date_input("Начало периода:", date(2023, 1, 1), format='DD-MM-YYYY')
end_date = st.sidebar.date_input("Конец периода:", date(2023, 8, 8), format='DD-MM-YYYY')
available_dates = [str(start_date + timedelta(days=i)) for i in range((end_date - start_date).days + 1)]
date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in available_dates]
formatted_dates = [date.strftime("%d-%m-%Y") for date in date_objects]
selected_dates = st.sidebar.multiselect("Выберите даты для отметки на графике:", formatted_dates)
selected_strategy = st.sidebar.selectbox("Выберите стратегию инвестирования:", strategies, index=0)
i=0

if st.button("Обновить данные и построить график"):
    fig = px.line()

    if "USD" in selected_currency:
        st.title('USD')
        max_relative_change_USD = []
        min_relative_change_USD = []
        if "RUB" in other_currencies:
            data_rub_USD = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_rub_USD = round((data_rub_USD['Open'] / data_rub_USD['Open'].iloc[0] - 1) * 100,2)
            fig.add_scatter(x=data_rub_USD.index, y=relative_change_rub_USD, name="RUB")
            max_relative_change_USD.append(relative_change_rub_USD.iloc[-1])
            min_relative_change_USD.append(relative_change_rub_USD.iloc[-1])
        if "BTC" in other_currencies:
            data_btc_USD = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
            relative_change_btc_USD = round((data_btc_USD['Open'] / data_btc_USD['Open'].iloc[0] - 1) * 100,2)
            fig.add_scatter(x=data_btc_USD.index, y=relative_change_btc_USD, name="BTC")
            max_relative_change_USD.append(relative_change_btc_USD.iloc[-1])
            min_relative_change_USD.append(relative_change_btc_USD.iloc[-1])
        if "GOLD" in other_currencies:
            data_gold_USD = yf.download("GC=F", start=start_date, end=end_date, progress=False)
            relative_change_gold_USD = round((data_gold_USD['Open'] / data_gold_USD['Open'].iloc[0] - 1) * 100,2)
            fig.add_scatter(x=data_gold_USD.index, y=relative_change_gold_USD, name="GOLD")
            max_relative_change_USD.append(relative_change_gold_USD.iloc[-1])
            min_relative_change_USD.append(relative_change_gold_USD.iloc[-1])
        if "CHF" in other_currencies:
            data_chf_USD = yf.download("CHFUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_chf_USD = round((data_chf_USD['Open']/ data_chf_USD['Open'].iloc[0] - 1) * 100, 2)
            fig.add_scatter(x=data_chf_USD.index, y=relative_change_chf_USD, name="CHF")
            max_relative_change_USD.append(relative_change_chf_USD.iloc[-1])
            min_relative_change_USD.append(relative_change_chf_USD.iloc[-1])
        if "SMLNK" in other_currencies:
            first_element = df['USD'].iloc[0]
            relative_change_smlnk_USD = round(((df['USD'] - first_element) / first_element) * 100,2)
            fig.add_scatter(x=df["Дата"], y=relative_change_smlnk_USD, name="SMLNK")
            max_relative_change_USD.append(relative_change_smlnk_USD.iloc[-1])
            min_relative_change_USD.append(relative_change_smlnk_USD.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(max_relative_change_USD)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(f'Лучший результат: {round((income * asset_on_hands/100) + asset_on_hands,2)} {selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(max_relative_change_USD)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)} {selected_currency}')
        if selected_strategy in 'Бездействие':
            data_usd_USD = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_usd_USD = round((data_usd_USD['Open'] / data_usd_USD['Open']), 2)
            fig.add_scatter(x=data_usd_USD.index, y=relative_change_usd_USD, name="USD")

    if "RUB" in selected_currency:
        st.title('RUB')
        max_relative_change_RUB = []
        min_relative_change_RUB = []
        if "BTC" in other_currencies:
            data_btc_RUB = yf.download("BTC-RUB", start=start_date, end=end_date, progress=False)
            relative_change_btc_RUB = round((data_btc_RUB['Open'] / data_btc_RUB['Open'].iloc[0] - 1) * 100,2)
            fig.add_scatter(x=data_btc_RUB.index, y=relative_change_btc_RUB, name="BTC")
            max_relative_change_RUB.append(relative_change_btc_RUB.iloc[-1])
            min_relative_change_RUB.append(relative_change_btc_RUB.iloc[-1])
        if "USD" in other_currencies:
            data_usd_RUB = yf.download("USDRUB=X", start=start_date, end=end_date, progress=False)
            relative_change_usd_RUB = round((data_usd_RUB['Open'] / data_usd_RUB['Open'].iloc[0] - 1) * 100,2)
            fig.add_scatter(x=data_usd_RUB.index, y=relative_change_usd_RUB, name="USD")
            max_relative_change_RUB.append(relative_change_usd_RUB.iloc[-1])
            min_relative_change_RUB.append(relative_change_usd_RUB.iloc[-1])
        if "GOLD" in other_currencies:
            data_usd_RUB = yf.download("USDRUB=X", start=start_date, end=end_date, progress=False)
            data_gold_RUB = yf.download("GC=F", start=start_date, end=end_date, progress=False)
            relative_change_gold_RUB = (round(((data_gold_RUB['Open']*data_usd_RUB['Open']) / (data_gold_RUB['Open'].iloc[0]*data_usd_RUB['Open'].iloc[0]) - 1) * 100, 2))
            fig.add_scatter(x=data_gold_RUB.index, y=relative_change_gold_RUB, name="GOLD")
            max_relative_change_RUB.append(relative_change_gold_RUB.iloc[-1])
            min_relative_change_RUB.append(relative_change_gold_RUB.iloc[-1])
        if "CHF" in other_currencies:
            data_chf_RUB = yf.download("CHFUSD=X", start=start_date, end=end_date, progress=False)
            data_usd_RUB = yf.download("USDRUB=X", start=start_date, end=end_date, progress=False)
            relative_change_chf_RUB = round(((data_chf_RUB['Open'] * data_usd_RUB['Open']) / (data_chf_RUB['Open'].iloc[0] * data_usd_RUB['Open'].iloc[0]) - 1) * 100, 2)
            fig.add_scatter(x=data_chf_RUB.index, y=relative_change_chf_RUB, name="CHF")
            max_relative_change_RUB.append(relative_change_chf_RUB.iloc[-1])
            min_relative_change_RUB.append(relative_change_chf_RUB.iloc[-1])
        if "SMLNK" in other_currencies:
            first_element = df['RUB'].iloc[0]
            relative_change_smlnk_RUB = round(((df['RUB'] - first_element) / first_element) * 100,2)
            fig.add_scatter(x=df["Дата"], y=relative_change_smlnk_RUB, name="SMLNK")
            max_relative_change_RUB.append(relative_change_smlnk_RUB.iloc[-1])
            min_relative_change_RUB.append(relative_change_smlnk_RUB.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(max_relative_change_RUB)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(f'Лучший результат: {round((income * asset_on_hands/100) + asset_on_hands,2)} {selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(max_relative_change_RUB)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)} {selected_currency}')
        if selected_strategy in 'Бездействие':
            data_rub_RUB = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_rub_RUB = round((data_rub_RUB['Open'] / data_rub_RUB['Open']), 2)
            fig.add_scatter(x=data_rub_RUB.index, y=relative_change_rub_RUB, name="RUB")

    if "BTC" in selected_currency:
        st.title('BTC')
        max_relative_change_BTC = []
        min_relative_change_BTC = []
        if "RUB" in other_currencies:
            data_rub_BTC = yf.download("BTC-RUB", start=start_date, end=end_date, progress=False)
            relative_change_rub_BTC = round((data_rub_BTC['Open'].iloc[0] / data_rub_BTC['Open'] - 1) * 100,2)
            fig.add_scatter(x=data_rub_BTC.index, y=relative_change_rub_BTC, name="RUB")
            max_relative_change_BTC.append(relative_change_rub_BTC.iloc[-1])
            min_relative_change_BTC.append(relative_change_rub_BTC.iloc[-1])
        if "USD" in other_currencies:
            data_btc_USD = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
            relative_change_usd_BTC = round((data_btc_USD['Open'].iloc[0] / data_btc_USD['Open'] - 1) * 100,2)
            fig.add_scatter(x=data_btc_USD.index, y=relative_change_usd_BTC, name="USD")
            max_relative_change_BTC.append(relative_change_usd_BTC.iloc[-1])
            min_relative_change_BTC.append(relative_change_usd_BTC.iloc[-1])
        if "GOLD" in other_currencies:
            data_btc_USD = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
            data_gold_BTC = yf.download("GC=F", start=start_date, end=end_date, progress=False)
            relative_change_gold_BTC = round((data_gold_BTC['Close'] /
                    data_gold_BTC['Close'].iloc[0] - 1) * (data_btc_USD['Open'].iloc[0] / data_btc_USD['Open'] - 1) * 100, 2)
            fig.add_scatter(x=data_gold_BTC.index, y=relative_change_gold_BTC, name="GOLD")
            max_relative_change_BTC.append(relative_change_gold_BTC.iloc[-1])
            min_relative_change_BTC.append(relative_change_gold_BTC.iloc[-1])
        if "CHF" in other_currencies:
            data_chf_BTC = yf.download("CHFUSD=X", start=start_date, end=end_date, progress=False)
            data_usd_BTC = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
            relative_change_chf_BTC = round(((data_chf_BTC['Open'] * data_usd_BTC['Open'].Iloc[0]) / (
                        data_chf_BTC['Open'].iloc[0] * data_usd_BTC['Open']) - 1) * 100, 2)
            fig.add_scatter(x=data_chf_BTC.index, y=relative_change_chf_BTC, name="CHF")
            max_relative_change_BTC.append(relative_change_chf_BTC.iloc[-1])
            min_relative_change_BTC.append(relative_change_chf_BTC.iloc[-1])
        if "SMLNK" in other_currencies:
            first_element = df['BTC'].iloc[0]
            relative_change_smlnk_BTC = round(((df['BTC'] - first_element) / first_element) * 100,2)
            fig.add_scatter(x=df["Дата"], y=relative_change_smlnk_BTC, name="SMLNK")
            max_relative_change_BTC.append(relative_change_smlnk_BTC.iloc[-1])
            min_relative_change_BTC.append(relative_change_smlnk_BTC.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(max_relative_change_BTC)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(f'Лучший результат: {round((income * asset_on_hands/100) + asset_on_hands,2)} {selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(max_relative_change_BTC)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)} {selected_currency}')
        if selected_strategy in 'Бездействие':
            data_btc_BTC = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_btc_BTC = round((data_btc_BTC['Open'] / data_btc_BTC['Open']), 2)
            fig.add_scatter(x=data_btc_BTC.index, y=relative_change_btc_BTC, name="USD")
    for date_to_mark in selected_dates:
        i+=1
        date_to_mark_object = datetime.strptime(date_to_mark, "%d-%m-%Y")
        fig.add_scatter(x=[date_to_mark_object], y=[0], mode='markers', name=f'B{i}', marker=dict(size=10))

    for trace in fig.data:
        trace.update(text=trace.y)

    fig.update_layout(
        xaxis_title="Дата",
        yaxis_title="Относительное изменение, %"
    )

    st.plotly_chart(fig)

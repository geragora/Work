import streamlit as st
import yfinance as yf
import plotly.express as px
from datetime import date, timedelta, datetime
import pandas as pd

file_path = 'SMLNK.xlsx'
df1 = pd.read_excel(file_path, sheet_name=0)
df2 = pd.read_excel(file_path, sheet_name=1)
df1['Дата'] = df1['Дата'].dt.strftime('%Y-%m-%d')
df2['Дата'] = df2['Дата'].dt.strftime('%Y-%m-%d')
df1.set_index("Дата", inplace=True)
df2.set_index("Дата", inplace=True)
lst1 = df1.index.values.tolist()
lst2 = df2.index.values.tolist()
st.title("Относительное изменение активов во времени")
currencies = ["USD", "RUB", "BTC", "SMLNK", "CTWK"]
strategies = ['Лучший результат', 'Худший результат', 'Бездействие', 'Самостоятельные решения']
st.sidebar.title('Меню настроек')
asset_on_hands = st.sidebar.number_input("Введите количество у.е. Вашего актива:")
selected_currency = st.sidebar.selectbox("Условные единицы в:", currencies, index=0)
other_currencies = st.sidebar.multiselect("Активы:", currencies, default=currencies[1:])
start_date = st.sidebar.date_input("Начало периода:", date(2023, 1, 1), format='YYYY-MM-DD')
end_date = st.sidebar.date_input("Конец периода:", date(2023, 8, 1), format='YYYY-MM-DD')
available_dates = [str(start_date + timedelta(days=i)) for i in range((end_date - start_date).days + 1)]
date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in available_dates]
formatted_dates = [date.strftime("%Y-%m-%d") for date in date_objects]
selected_dates = st.sidebar.multiselect("Выберите даты для отметки на графике:", formatted_dates)
selected_strategy = st.sidebar.selectbox("Выберите стратегию инвестирования:", strategies, index=0)
i = 0

if st.button("Обновить данные и построить график"):
    fig = px.line()


    if "RUB" in selected_currency:
        st.title('RUB')
        relative_change_RUB = []
        if "BTC" in other_currencies:
            data_btc_RUB = yf.download("BTC-RUB", start=start_date, end=end_date, progress=False)
            relative_change_btc_RUB = round((data_btc_RUB['Open'] / data_btc_RUB['Open'].iloc[0] - 1) * 100, 2)
            fig.add_scatter(x=data_btc_RUB.index, y=relative_change_btc_RUB, name="BTC")
            relative_change_RUB.append(relative_change_btc_RUB.iloc[-1])
        if "USD" in other_currencies:
            data_usd_RUB = yf.download("USDRUB=X", start=start_date, end=end_date, progress=False)
            relative_change_usd_RUB = round((data_usd_RUB['Open'] / data_usd_RUB['Open'].iloc[0] - 1) * 100, 2)
            fig.add_scatter(x=data_usd_RUB.index, y=relative_change_usd_RUB, name="USD")
            relative_change_RUB.append(relative_change_usd_RUB.iloc[-1])
        if "SMLNK" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                first_element = df1['RUB'].iloc[0]
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_smlnk_RUB = round(((df1["RUB"].iloc[aidd1:] - df1['RUB'].iloc[aidd1])
                                                   / df1['RUB'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2+1], y=relative_change_smlnk_RUB, name="SMLNK")
                relative_change_RUB.append(relative_change_smlnk_RUB.iloc[-1])
        if "CTWK" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                first_element = df2['RUB'].iloc[0]
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_ctwk_RUB = round(((df2["RUB"].iloc[aidd1:] - df2['RUB'].iloc[aidd1])
                                                  / df2['RUB'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2+1], y=relative_change_ctwk_RUB, name="CTWK")
                relative_change_RUB.append(relative_change_ctwk_RUB.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(relative_change_RUB)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(f'Лучший результат: {round((income * asset_on_hands/100) + asset_on_hands,2)}'
                         f' {selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(relative_change_RUB)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)}'
                         f'{selected_currency}')
        if selected_strategy in 'Бездействие':
            data_rub_RUB = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_rub_RUB = round((data_rub_RUB['Open'] / data_rub_RUB['Open']), 2)
            fig.add_scatter(x=data_rub_RUB.index, y=relative_change_rub_RUB, name="RUB")

    if "USD" in selected_currency:
        st.title('USD')
        relative_change_USD = []
        if "RUB" in other_currencies:
            data_rub_USD = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_rub_USD = round((data_rub_USD['Open'] / data_rub_USD['Open'].iloc[0] - 1) * 100, 2)
            fig.add_scatter(x=data_rub_USD.index, y=relative_change_rub_USD, name="RUB")
            relative_change_USD.append(relative_change_rub_USD.iloc[-1])
        if "BTC" in other_currencies:
            data_btc_USD = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
            relative_change_btc_USD = round((data_btc_USD['Open'] / data_btc_USD['Open'].iloc[0] - 1) * 100, 2)
            fig.add_scatter(x=data_btc_USD.index, y=relative_change_btc_USD, name="BTC")
            relative_change_USD.append(relative_change_btc_USD.iloc[-1])
        if "SMLNK" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                first_element = df1['RUB'].iloc[0]
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_smlnk_USD = round(((df1["USD"].iloc[aidd1:] - df1['USD'].iloc[aidd1])
                                                   / df1['USD'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2 + 1], y=relative_change_smlnk_USD, name="SMLNK")
                relative_change_USD.append(relative_change_smlnk_USD.iloc[-1])
        if "CTWK" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                first_element = df2['USD'].iloc[0]
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_ctwk_USD = round(((df2['USD'].iloc[aidd1:] - df2['USD'].iloc[aidd1])
                                                  / df2['USD'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2+1], y=relative_change_ctwk_USD, name="CTWK")
                relative_change_USD.append(relative_change_ctwk_USD.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(relative_change_USD)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(f'Лучший результат: {round((income * asset_on_hands/100) + asset_on_hands,2)} '
                         f'{selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(relative_change_USD)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)}'
                         f' {selected_currency}')
        if selected_strategy in 'Бездействие':
            data_usd_USD = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_usd_USD = round((data_usd_USD['Open'] / data_usd_USD['Open']), 2)
            fig.add_scatter(x=data_usd_USD.index, y=relative_change_usd_USD, name="USD")
        for date_to_mark in selected_dates:
            i += 1
            fig.add_scatter(x=[date_to_mark], y=[0], mode='markers', name=f'B{i}', marker=dict(size=10, color='red'))

    if "BTC" in selected_currency:
        st.title('BTC')
        relative_change_BTC = []
        if "RUB" in other_currencies:
            data_rub_BTC = yf.download("BTC-RUB", start=start_date, end=end_date, progress=False)
            relative_change_rub_BTC = round((data_rub_BTC['Open'].iloc[0] / data_rub_BTC['Open'] - 1) * 100, 2)
            fig.add_scatter(x=data_rub_BTC.index, y=relative_change_rub_BTC, name="RUB")
            relative_change_BTC.append(relative_change_rub_BTC.iloc[-1])
        if "USD" in other_currencies:
            data_btc_USD = yf.download("BTC-USD", start=start_date, end=end_date, progress=False)
            relative_change_usd_BTC = round((data_btc_USD['Open'].iloc[0] / data_btc_USD['Open'] - 1) * 100, 2)
            fig.add_scatter(x=data_btc_USD.index, y=relative_change_usd_BTC, name="USD")
            relative_change_BTC.append(relative_change_usd_BTC.iloc[-1])
        if "SMLNK" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_smlnk_BTC = round(((df1["BTC"].iloc[aidd1:] - df1['BTC'].iloc[aidd1])
                                                   / df1['BTC'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2 + 1], y=relative_change_smlnk_BTC, name="SMLNK")
                relative_change_BTC.append(relative_change_smlnk_BTC.iloc[-1])
        if "CTWK" in other_currencies:
            if str(start_date) or str(end_date) in df2.index:
                first_element = df2['CTWK'].iloc[0]
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_ctwk_BTC = round(((df2['CTWK'].iloc[aidd1:] - df2['CTWK'].iloc[aidd1])
                                                  / df2['CTWK'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2+1], y=relative_change_ctwk_BTC, name="CTWK")
                relative_change_BTC.append(relative_change_ctwk_BTC.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(relative_change_BTC)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(f'Лучший результат: {round((income * asset_on_hands/100) + asset_on_hands,2)} '
                         f'{selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(relative_change_BTC)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)} '
                         f'{selected_currency}')
        if selected_strategy in 'Бездействие':
            data_btc_BTC = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_btc_BTC = round((data_btc_BTC['Open'] / data_btc_BTC['Open']), 2)
            fig.add_scatter(x=data_btc_BTC.index, y=relative_change_btc_BTC, name="USD")
        for date_to_mark in selected_dates:
            i += 1
            date_to_mark_object = datetime.strptime(date_to_mark, "%d-%m-%Y")
            fig.add_scatter(x=[date_to_mark_object], y=[0], mode='markers', name=f'B{i}', marker=dict(size=10))

    if "SMLNK" in selected_currency:
        st.title('SMLNK')
        relative_change_SMLNK = []
        if "RUB" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_smlnk_BTC = round(
                    ((df1['RUB'].iloc[aidd1]) / df1["RUB"].iloc[aidd1:] - 1) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2 + 1], y=relative_change_smlnk_BTC, name="RUB")
                relative_change_SMLNK.append(relative_change_smlnk_BTC.iloc[-1])
        if "USD" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_usd_SMLNK = round(
                    ((df1['USD'].iloc[aidd1]) / df1['USD'].iloc[aidd1:] - 1) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2 + 1], y=relative_change_usd_SMLNK, name="USD")
                relative_change_SMLNK.append(relative_change_usd_SMLNK.iloc[-1])
        if "BTC" in other_currencies:
            if str(start_date) or str(end_date) in df1.index:
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_btc_SMLNK = round(
                    ((df1['BTC'].iloc[aidd1]) / df1['BTC'].iloc[aidd1:] - 1) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2 + 1], y=relative_change_btc_SMLNK, name="BTC")
                relative_change_SMLNK.append(relative_change_btc_SMLNK.iloc[-1])
        if "CTWK" in other_currencies:
            if str(start_date) or str(end_date) in df2.index:
                first_element = df1['CTWK'].iloc[0]
                aidd1 = lst1.index(str(start_date))
                aidd2 = lst1.index(str(end_date))
                relative_change_ctwk_SMLNK = round(((df1['CTWK'].iloc[aidd1:] - df1['CTWK'].iloc[aidd1])
                                                    / df1['CTWK'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df1.index[aidd1:aidd2+1], y=relative_change_ctwk_SMLNK, name="CTWK")
                relative_change_SMLNK.append(relative_change_ctwk_SMLNK.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(relative_change_SMLNK)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(
                    f'Лучший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)} '
                    f'{selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(relative_change_SMLNK)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(
                    f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)}'
                    f' {selected_currency}')
        if selected_strategy in 'Бездействие':
            data_btc_BTC = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_btc_BTC = round((data_btc_BTC['Open'] / data_btc_BTC['Open']), 2)
            fig.add_scatter(x=data_btc_BTC.index, y=relative_change_btc_BTC, name="USD")

    if "CTWK" in selected_currency:
        st.title('CTWK')
        relative_change_CTWK = []
        if "RUB" in other_currencies:
            if str(start_date) or str(end_date) in df2.index:
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_rub_CTWK = round(
                    ((df2['RUB'].iloc[aidd1]) / df2["RUB"].iloc[aidd1:] - 1) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2 + 1], y=relative_change_rub_CTWK, name="RUB")
                relative_change_CTWK.append(relative_change_rub_CTWK.iloc[-1])
        if "USD" in other_currencies:
            if str(start_date) or str(end_date) in df2.index:
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_usd_CTWK = round(
                    ((df2['USD'].iloc[aidd1]) / df2['USD'].iloc[aidd1:] - 1) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2 + 1], y=relative_change_usd_CTWK, name="USD")
                relative_change_CTWK.append(relative_change_usd_CTWK.iloc[-1])
        if "BTC" in other_currencies:
            if str(start_date) or str(end_date) in df2.index:
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_btc_CTWK = round(
                    ((df2['BTC'].iloc[aidd1]) / df2['BTC'].iloc[aidd1:] - 1) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2 + 1], y=relative_change_btc_CTWK, name="BTC")
                relative_change_CTWK.append(relative_change_btc_CTWK.iloc[-1])
        if "SMLNK" in other_currencies:
            if str(start_date) or str(end_date) in df2.index:
                first_element = df2['CTWK'].iloc[0]
                aidd1 = lst2.index(str(start_date))
                aidd2 = lst2.index(str(end_date))
                relative_change_ctwk_BTC = round(((df2['SMLNK'].iloc[aidd1:] - df2['SMLNK'].iloc[aidd1])
                                                  / df2['SMLNK'].iloc[aidd1]) * 100, 2)
                fig.add_scatter(x=df2.index[aidd1:aidd2+1], y=relative_change_ctwk_BTC, name="SMLNK")
                relative_change_CTWK.append(relative_change_ctwk_BTC.iloc[-1])
        if selected_strategy in "Лучший результат":
            income = max(relative_change_CTWK)
            if income < 0:
                st.write(f'Лучший результат: не приобретать других активов')
            else:
                st.write(
                    f'Лучший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)} '
                    f'{selected_currency}')
        if selected_strategy in "Худший результат":
            income = min(relative_change_CTWK)
            if income > 0:
                st.write(f'Худший результат: остаться в этом активе')
            else:
                st.write(
                    f'Худший результат: {round((income * asset_on_hands / 100) + asset_on_hands, 2)}'
                    f' {selected_currency}')
        if selected_strategy in 'Бездействие':
            data_btc_BTC = yf.download("RUBUSD=X", start=start_date, end=end_date, progress=False)
            relative_change_btc_BTC = round((data_btc_BTC['Open'] / data_btc_BTC['Open']), 2)
            fig.add_scatter(x=data_btc_BTC.index, y=relative_change_btc_BTC, name="USD")


    for trace in fig.data:
        trace.update(text=trace.y)

    fig.update_layout(
        xaxis_title="Дата",
        yaxis_title="Относительное изменение, %"
    )

    st.plotly_chart(fig)

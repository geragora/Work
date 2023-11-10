import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import yfinance as yf

data_btc_usd = yf.download("BTC-USD", start="2020-04-01", end="2023-04-30", progress=False).High
data_rub_USD = yf.download("USDRUB=X", start="2020-04-01", end="2023-04-30", progress=False).High
rub_usd_btc = {}
count = 0
for i in data_rub_USD.index:
    count += 1
    try:
        if count%20 == 0:
            rub_usd_btc[i] =  [1, data_rub_USD[i], data_btc_usd.loc[i]*data_rub_USD[i]]
    except:
        continue


x = list(rub_usd_btc.values())
date = list(rub_usd_btc.keys())
d = [1000 for i in range(len(x[0]))]

def dataframe(dfs):
    data_dfs = []
    for index in range(len(dfs)):
        
        data = { 'KRUR': d,'KUSD': d, 'BTC': d}#, 'SMLNK': d, 'CTWK': d}
        df = pd.DataFrame(data)
        df = df.set_index(df.columns)
        df = df.rename_axis(date[index])
        df.iloc[0,:] = dfs[index]
        for j in range(len(df.columns)):
            for i in range(j,len(df.columns)):
                if i==j:
                    df.iloc[i,j] = 1
                    continue
                if j<i:
                    df.iloc[j,i] = df.iloc[0,i]/df.iloc[0,j]
                df.iloc[i,j] = df.iloc[j,j]/df.iloc[j,i]
        data_dfs.append(df)
    return data_dfs
    

dfs = dataframe(x)

currency = 'BTC'

active_data = []
max_values = []
capital = [0.07]
for i in range(1, len(dfs)):
    list_f = pd.DataFrame(dfs[i - 1])
    list_s = pd.DataFrame(dfs[i])
    max_values.append((list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :])
    max = ((list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :]).max()
    data1 = list_f.index.name
    data2 = list_s.index.name
    max_index = max_values[i-1].max().idxmax()
    rub_value = max_values[i-1][max_index][0]
    usd_value = max_values[i-1][max_index][1]
    btc_value = max_values[i-1][max_index][2]
    capital.append(capital[-1]*(1+max_values[i-1][max_index][currency]))
    x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
            'Прирост в рублях': round(rub_value, 2), 'Прирост в долларах': round(usd_value, 2),
            'Прирост в биткойнах': round(btc_value, 2)}
    
    active_data.append(x)

active = pd.DataFrame(active_data)


fig = go.Figure()
data = pd.DataFrame({'KRUR': [0]*(len(max_values)+1),'KUSD': [0]*(len(max_values)+1), 'BTC': [0]*(len(max_values)+1)})#, 'SMLNK': [0]*5, 'CTWK': [0]*5})


for i in range(len(max_values)):
    dataset = pd.DataFrame(max_values[i])
    # for col in range(len(data.columns)):
    data.iloc[i+1] = dataset.loc[currency,:]


for j in range(len(data.columns)):
    for i in range(len(date)-1):
        if data.columns[j] == active.iloc[i,1]:
                    fig.add_trace(go.Scatter(x=date[i:i+2],
                                                y=data.iloc[i:i+2,j],
                                                mode='lines',
                                                line=dict(color='red')
                                                ))

                    continue
        fig.add_trace(go.Scatter(x=date[i:i+2],
                                    y=data.iloc[i:i+2,j],
                                    mode='lines',
                                    line=dict(color='gray')
                                    ))



fig.add_trace(go.Scatter(x=date,
                            y=capital,
                            mode='lines',
                            line=dict(color='green')
                            ))

st.plotly_chart(fig)
st.dataframe(active)














active_data = []
max_values = []
capital = [1]
for i in range(1, len(dfs)):
    list_f = pd.DataFrame(dfs[i - 1])
    list_s = pd.DataFrame(dfs[i])
    max_values.append((list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :])
    max = ((list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :]).min()
    data1 = list_f.index.name
    data2 = list_s.index.name
    max_index = max_values[i-1].max().idxmin()
    rub_value = max_values[i-1][max_index][0]
    usd_value = max_values[i-1][max_index][1]
    btc_value = max_values[i-1][max_index][2]
    capital.append(capital[-1]*(1+max_values[i-1][max_index][currency]))
    x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
            'Прирост в рублях': round(rub_value, 2), 'Прирост в долларах': round(usd_value, 2),
            'Прирост в биткойнах': round(btc_value, 2)}
    
    active_data.append(x)

active = pd.DataFrame(active_data)


fig = go.Figure()
data = pd.DataFrame({'KRUR': [0]*(len(max_values)+1),'KUSD': [0]*(len(max_values)+1), 'BTC': [0]*(len(max_values)+1)})#, 'SMLNK': [0]*5, 'CTWK': [0]*5})


for i in range(len(max_values)):
    dataset = pd.DataFrame(max_values[i])
    # for col in range(len(data.columns)):
    data.iloc[i+1] = dataset.loc[currency,:]


for j in range(len(data.columns)):
    for i in range(len(date)-1):
        if data.columns[j] == active.iloc[i,1]:
                    fig.add_trace(go.Scatter(x=date[i:i+2],
                                                y=data.iloc[i:i+2,j],
                                                mode='lines',
                                                line=dict(color='green')
                                                ))

                    continue
        fig.add_trace(go.Scatter(x=date[i:i+2],
                                    y=data.iloc[i:i+2,j],
                                    mode='lines',
                                    line=dict(color='gray')
                                    ))



fig.add_trace(go.Scatter(x=date,
                            y=capital,
                            mode='lines',
                            line=dict(color='red')
                            ))

st.plotly_chart(fig)

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px



x = [
    [ 1, 70,	1157800,78000000,	57188000],
    [1,96,2788360,161253000,101949216],  
    [1, 100, 2760036, 170000000, 90000000],
    [1, 60, 1350000, 130000000, 60000000],
    [1, 100, 3000000, 180000000, 120000000]
]

date = [0,1,2,3,4]

def dataframe(dfs):
    data_dfs = []
    for index in range(len(dfs)):
        
        d = [1000 for i in range(len(dfs[0]))]
        data = { 'KRUR': d,'KUSD': d, 'BTC': d, 'SMLNK': d, 'CTWK': d}
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


active_data = []
max_values = []
capital = [1]
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
    capital.append(capital[-1]*(1+np.max(max)))
   
    x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
            'Прирост в рублях': round(rub_value, 2), 'Прирост в долларах': round(usd_value, 2),
            'Прирост в биткойнах': round(btc_value, 2)}
    
    active_data.append(x)

active = pd.DataFrame(active_data)


fig = go.Figure()
data = pd.DataFrame({ 'KRUR': [0]*5,'KUSD': [0]*5, 'BTC': [0]*5, 'SMLNK': [0]*5, 'CTWK': [0]*5})

for i in range(len(max_values)):
    dataset = pd.DataFrame(max_values[i])
    for col in range(len(data.columns)):
         data.iloc[ i+1, :] = dataset.iloc[0,:] 



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



fig.add_trace(go.Scatter( x = date,
                            y=capital,
                            mode='lines',
                            line=dict(color='green')
                            ))

st.plotly_chart(fig)












active_data = []
max_values = []
capital = [1]
for i in range(1, len(dfs)):
    list_f = pd.DataFrame(dfs[i - 1])
    list_s = pd.DataFrame(dfs[i])
    max_values.append((list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :])
    data1 = list_f.index.name
    data2 = list_s.index.name
    max_index = max_values[i-1].min().idxmin()
    rub_value = max_values[i-1][max_index][0]
    usd_value = max_values[i-1][max_index][1]
    btc_value = max_values[i-1][max_index][2]
    capital.append(capital[-1]*(1+rub_value))
    x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
            'Прирост в рублях': round(rub_value, 2), 'Прирост в долларах': round(usd_value, 2),
            'Прирост в биткойнах': round(btc_value, 2)}
    
    active_data.append(x)

active = pd.DataFrame(active_data)

fig = go.Figure()
data = pd.DataFrame({ 'KRUR': [0]*5,'KUSD': [0]*5, 'BTC': [0]*5, 'SMLNK': [0]*5, 'CTWK': [0]*5})

for i in range(len(max_values)):
    dataset = pd.DataFrame(max_values[i])
    for col in range(len(data.columns)):
         data.iloc[ i+1, :] = dataset.iloc[0,:] 



for j in range(len(data.columns)):
    for i in range(len(date)-1):
        if data.columns[j] == active.iloc[i,1]:
                    fig.add_trace(go.Scatter(x=date[i:i+2],
                                                y=data.iloc[i:i+2,j],
                                                mode='lines',
                                                line=dict(color='blue')
                                                ))

                    continue
        fig.add_trace(go.Scatter(x=date[i:i+2],
                                    y=data.iloc[i:i+2,j],
                                    mode='lines',
                                    line=dict(color='gray')
                                    ))



fig.add_trace(go.Scatter( x = date,
                            y=capital,
                            mode='lines',
                            line=dict(color='green')
                            ))

st.plotly_chart(fig)
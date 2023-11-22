import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import yfinance as yf
#загрузить в файл курсы валют чтобы их не загружат и каждый раз, это сэкономит время!

# Инициализация состояния сессии
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {'KRUR': 0, 'KUSD': 0, 'BTC': 0}
# Боковая панель для ввода
# st.sidebar.title("Выберите валюту, в которой у вас имеются накопления")
options = st.sidebar.selectbox('Выберите валюту, в которой у вас имеются накопления', ('KRUR', 'KUSD', 'BTC'))
some_value = st.sidebar.number_input(f'Введите количество {options}', value=0)#[4900000,70000, 1]

# options_frequency = st.sidebar.selectbox('Выберите валюту, в которой у вас имеются накопления', ('KRUR', 'KUSD', 'BTC'))

frequency = st.sidebar.number_input(f'Как часто редко перекладывать активы', value=5)

# Обновление портфеля
st.session_state.portfolio[options] = some_value

# Отображение портфеля в боковой панели
st.sidebar.write('## Портфель')
if not (st.session_state.portfolio['KRUR'] or st.session_state.portfolio['KUSD'] or st.session_state.portfolio['BTC']):
    st.sidebar.text('Портфель пуст')
else:
    for asset, quantity in st.session_state.portfolio.items():
        if quantity!= 0.0:
            st.sidebar.text(f'{asset} : {quantity}')


option = st.sidebar.selectbox(
    'Выберите валюту, в которой будет изображена динамика активов',
    ('KRUR', 'KUSD', 'BTC')
)


start_date = st.sidebar.date_input('Выберите начальную дату', pd.to_datetime("2022-04-01"))
end_date = st.sidebar.date_input('Выберите конечную дату', pd.to_datetime("2023-11-09"))

##################################################################################################################################
def download(frequency):
            data_btc_usd = yf.download("BTC-USD", start=start_date, end=end_date).High
            data_rub_USD = yf.download("USDRUB=X", start=start_date, end=end_date).High
            rub_usd_btc = {}
            count = 0
            for i in data_rub_USD.index:
                count += 1
                try:
                    if count%frequency == 0:
                        rub_usd_btc[i] =  [1, data_rub_USD[i], data_btc_usd.loc[i]*data_rub_USD[i]]
                except:
                    continue


            x = list(rub_usd_btc.values())
            date = list(rub_usd_btc.keys())

            def dataframe(dfs):
                data_dfs = []
                for index in range(len(dfs)):
                    d = [1000 for i in range(len(dfs[0]))]
                    
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
            return dfs,date
##################################################################################################################################



def MAX_MIN(currency, func,funcx, dfs, date):
            active_data = []
            max_values = []
            if func == pd.DataFrame.max:
                title = 'Наилучшая стратегия'
            else:
                title = 'Наихудшая стратегия'
            capital = [1]
            for i in range(1, len(dfs)):
                list_f = pd.DataFrame(dfs[i - 1])
                list_s = pd.DataFrame(dfs[i])
                max_values.append(1+(list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :])
                max = func((list_s.iloc[:, :] - list_f.iloc[:,:]) / list_f.iloc[:, :])
                data1 = list_f.index.name
                data2 = list_s.index.name
                max_index = func(max_values[i-1])
                max_index = funcx(max_index)
                rub_value = max_values[i-1][max_index][0]
                usd_value = max_values[i-1][max_index][1]
                btc_value = max_values[i-1][max_index][2]
                capital.append(capital[-1]*(max_values[i-1][max_index][currency]))
                x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
                        'KRUR': round(rub_value, 2), 'KUSD': round(usd_value, 2),
                        'BTC': round(btc_value, 2)}
                
                active_data.append(x)

            active = pd.DataFrame(active_data)


            fig = go.Figure()
            data = pd.DataFrame({'KRUR': [st.session_state.portfolio['KRUR']*dfs[0].loc[currency,'KRUR']]*(len(max_values)+1),
                                 'KUSD': [st.session_state.portfolio['KUSD']*dfs[0].loc[currency, 'KUSD']]*(len(max_values)+1),
                                 'BTC': [st.session_state.portfolio['BTC']*dfs[0].loc[currency, 'BTC']]*(len(max_values)+1)
                                 })
  

            redata = data.iloc[0]

            for i in range(1,len(max_values)):
                for col in dfs[0].columns:
                    data.loc[i,col] = redata[col]*(active.loc[i-1,col])
                redata = data.iloc[i]

            yozero = [0]

            for j in range(len(data.columns)):
                for i in range(len(date)-2):
                    if data.columns[j] == active.iloc[i,1]:
                        if data.columns[j] == 'KRUR':
                            color = 'red'
                        elif data.columns[j] == 'KUSD':
                            color = 'blue'
                        else:
                            color = 'orange'
                        fig.add_trace(go.Scatter(x=date[i:i+2],
                                                            y=data.iloc[i:i+2,j],
                                                            mode='lines',
                                                            line=dict(color=color),
                                                            name = data.columns[j],
                                                            text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(data.iloc[i,j]*dfs[i].loc[ data.columns[0],currency],
                                                                                                                                  data.iloc[i,j]*dfs[i].loc[ data.columns[1],currency], 
                                                                                                                                  data.iloc[i,j]*dfs[i].loc[data.columns[2],currency]),

                                                            # hoverinfo='skip'
                                                            #hovertemplate='%{x}: <br>%{name}'
                                                            ))
                        
                        
                        continue
                    fig.add_trace(go.Scatter(x=date[i:i+2],
                                                y=data.iloc[i:i+2,j],
                                                mode='lines',
                                                line=dict(color='gray'),
                                                name = data.columns[j],
                                                text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(data.iloc[i,j]*dfs[i].loc[ data.columns[0],currency],
                                                                                                                                  data.iloc[i,j]*dfs[i].loc[ data.columns[1],currency], 
                                                                                                                                  data.iloc[i,j]*dfs[i].loc[data.columns[2],currency]),
                                                ))

            fig.update_layout(showlegend=False,title=title)
            # fig.update_yaxes(type="log", showticklabels=False)
            fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')

            # fig.update_yaxes(type="log", dtick=1,showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')
            fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')


            return st.plotly_chart(fig)



def inaction(currency,dfs, date):
            fig = go.Figure()
            for j in range(len(dfs)-1):
                for col in dfs[j].columns:
                        if col == 'KRUR':
                            color = 'red'
                        elif col == 'KUSD':
                            color = 'blue'
                        else:
                            color = 'orange'
                        fig.add_trace(go.Scatter(x=date[j:j+2],
                                                            y=[df.loc[currency, col] * st.session_state.portfolio[col] for df in dfs[j:j+2]],
                                                            mode='lines',
                                                            line=dict(color=color),
                                                            name = col,
                                                            text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(st.session_state.portfolio[col]/dfs[j].loc[col, "KRUR"],
                                                                                                                                  st.session_state.portfolio[col]/dfs[j].loc[col, "KUSD"], 
                                                                                                                                  st.session_state.portfolio[col]/dfs[j].loc[col, "BTC"],
                                                                                                                    
                                                                                                                                  ),

                                                            # hoverinfo='skip'
                                                            # hovertemplate='%{x}: <br>%{name}'
                                                            ))
         

            fig.update_layout(showlegend=False,title="Бездействие")
            # fig.update_yaxes(type="log", showticklabels=False)
            fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')

            fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='rgba(128,128,128,0.2)')


            return st.plotly_chart(fig)




# def experience(currency, dfs):
        # fig = go.Figure()
        # for j in range(len(dfs)-1):
        #         for col in dfs[j].columns:
        #                 if col == 'KRUR':
        #                     color = 'red'
        #                 elif col == 'KUSD':
        #                     color = 'blue'
        #                 else:
        #                     color = 'orange'
        #                 fig.add_trace(go.Scatter(x=date[j:j+2],
        #                                                     y=[dfs[j].loc[currency, col], dfs[j+1].loc[currency, col]],
        #                                                     mode='lines',
        #                                                     line=dict(color=color),
        #                                                     name = col, 
        #                                                     text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(st.session_state.portfolio[col]/dfs[j].loc[col, "KRUR"],
        #                                                                                                                           st.session_state.portfolio[col]/dfs[j].loc[col, "KUSD"], 
        #                                                                                                                           st.session_state.portfolio[col]/dfs[j].loc[col, "BTC"]),
                                                                                                                    
        #                                                                                                                           ))
                                     
        # fig.update_layout(showlegend=False,title="История")
        # fig.update_yaxes(type="log", showticklabels=False)

        # return st.plotly_chart(fig)                                                                                            
            # fig = go.Figure()
            # data = pd.DataFrame({'KRUR': [st.session_state.portfolio['KRUR']*dfs[0].loc[currency,'KRUR']]*(len(max_values)+1),
            #                      'KUSD': [st.session_state.portfolio['KUSD']*dfs[0].loc[currency, 'KUSD']]*(len(max_values)+1),
            #                      'BTC': [st.session_state.portfolio['BTC']*dfs[0].loc[currency, 'BTC']]*(len(max_values)+1)
            #                      })
  

            # redata = data.iloc[0]

            # for i in range(1,len(max_values)):
            #     for col in dfs[0].columns:
            #         data.loc[i,col] = redata[col]*(active.loc[i-1,col])
            #     redata = data.iloc[i]

            # yozero = [0]

            # for j in range(len(data.columns)):
            #     for i in range(len(date)-2):
            #         if data.columns[j] == active.iloc[i,1]:
            #             if data.columns[j] == 'KRUR':
            #                 color = 'red'
            #             elif data.columns[j] == 'KUSD':
            #                 color = 'blue'
            #             else:
            #                 color = 'orange'
            #             fig.add_trace(go.Scatter(x=date[i:i+2],
            #                                                 y=data.iloc[i:i+2,j],
            #                                                 mode='lines',
            #                                                 line=dict(color=color),
            #                                                 name = data.columns[j],
            #                                                 text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(data.iloc[i,j]*dfs[i].loc[ data.columns[0],currency],
            #                                                                                                                       data.iloc[i,j]*dfs[i].loc[ data.columns[1],currency], 
            #                                                                                                                       data.iloc[i,j]*dfs[i].loc[data.columns[2],currency]),

            #                                                 # hoverinfo='skip'
            #                                                 #hovertemplate='%{x}: <br>%{name}'
            #                                                 ))
                        
                        
            #             continue
            #         fig.add_trace(go.Scatter(x=date[i:i+2],
            #                                     y=data.iloc[i:i+2,j],
            #                                     mode='lines',
            #                                     line=dict(color='gray'),
            #                                     name = data.columns[j],
            #                                     text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(data.iloc[i,j]*dfs[i].loc[ data.columns[0],currency],
            #                                                                                                                       data.iloc[i,j]*dfs[i].loc[ data.columns[1],currency], 
            #                                                                                                                       data.iloc[i,j]*dfs[i].loc[data.columns[2],currency]),
            #                                     ))

            # fig.update_layout(showlegend=False,title=title)
            # fig.update_yaxes(type="log", showticklabels=False)

            # return st.plotly_chart(fig)

     
     
# activs = [i for i,j in st.session_state.portfolio.items() if j!=0]

# experience(option, history)
dfs,date = download(frequency)[0],download(frequency)[1]
dfs1, date1 = download(1)
MAX_MIN(option, pd.DataFrame.max, pd.Series.idxmax, dfs,date )
MAX_MIN(option, pd.DataFrame.min, pd.Series.idxmin, dfs,date )
inaction(option, dfs1, date1)

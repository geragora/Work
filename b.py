import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from plotly.subplots import make_subplots
import psycopg2
# from datetime import datetime




if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {'KRUR': 0, 'KUSD': 0, 'BTC': 0}

options = st.sidebar.selectbox('Выберите валюту, в которой у вас имеются накопления', ('KRUR', 'KUSD', 'BTC'))
some_value = st.sidebar.number_input(f'Введите количество {options}', value=0.0, step=0.01)#[4900000,70000, 1]


frequency = st.sidebar.number_input(f'Как  редко перекладывать активы', value=5)


st.session_state.portfolio[options] = some_value

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


start_date = str(st.sidebar.date_input('Выберите начальную дату', pd.to_datetime("2023-01-01")))
end_date = str(st.sidebar.date_input('Выберите конечную дату', pd.to_datetime("2023-11-09")))
##################################################################################################################################
def download(frequency = 1):
            data  = pd.DataFrame(pd.read_csv('combined_data_full_history.csv')).set_index('Date')
            data_btc_usd = data.loc[start_date:end_date, 'High_BTC']
            data_rub_USD = data.loc[start_date:end_date, 'High_USDRUB']
            rub_usd_btc = {}
            count = 0
            for i in data_rub_USD.index:
                count += 1
                try:
                    if count%frequency == 0:
                        rub_usd_btc[i] =   [1, data_rub_USD[i], data_btc_usd.loc[i]*data_rub_USD[i]]
                except:
                    continue


            x = list(rub_usd_btc.values())
            date = list(rub_usd_btc.keys())

            def dataframe(dfs):
                data_dfs = []
                for index in range(len(dfs)):
                    d = [1000 for i in range(len(dfs[0]))]
                    
                    data = { 'KRUR': d,'KUSD': d, 'BTC': d}
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



def MAX_MIN(currency, func,funcx, dfs, date,sum, portfel, fig):
    
            active_data = []
            max_values = []
            if func == pd.DataFrame.max:
                title = 'График роста капитала, при правильном перераспределении активов' 
            else:
                title = 'График падения капитала, при неправильном перераспределении активов'
            capital = [1]
            # c = 0
            cap=[]
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
                capital.append(capital[-1]* (max_values[i-1][max_index][currency]))
                cap.append(max_values[i-1][max_index][currency]-1)
                x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
                        'KRUR': rub_value, 'KUSD': usd_value,
                        'BTC': btc_value}
                x = {'Промежуток времени': '{} -- {}'.format(data1, data2), 'Лучший актив': max_index,
                        'KRUR': round(rub_value, 5), 'KUSD': round(usd_value, 5),
                        'BTC': round(btc_value,5)}
                active_data.append(x)
            active = pd.DataFrame(active_data)

            # fig = go.Figure()
            # fig = make_subplots(rows=1, cols=2, subplot_titles=[title, 'Изменение активов, при их правильном перераспределении'])


            data = pd.DataFrame({'KRUR': [st.session_state.portfolio['KRUR']*dfs[0].loc[currency,'KRUR']]*(len(max_values)),
                                'KUSD': [st.session_state.portfolio['KUSD']*dfs[0].loc[currency, 'KUSD']]*(len(max_values)),
                                 'BTC': [st.session_state.portfolio['BTC']*dfs[0].loc[currency, 'BTC']]*(len(max_values))
                                 })
  
            data_portf ={'KRUR': st.session_state.portfolio['KRUR'],
                                 'KUSD': st.session_state.portfolio['KUSD'],
                                 'BTC': st.session_state.portfolio['BTC']
                                 }
            redata = data.iloc[0]

            for i in range(1,len(max_values)):
                for col in dfs[0].columns:
                    data.loc[i,col] = redata[col]*active.loc[i-1,col]
                redata = data.iloc[i]
            data /= data.iloc[0]
            color = {'KRUR': 'red',  'KUSD':'blue' , 'BTC':'orange'}
            color_light = {'KRUR': 'rgba(255, 150, 150, 0.2)',  'KUSD':'rgba(150, 200, 255, 0.2)' , 'BTC':'rgba(255, 200, 150, 0.2)'}
            legend = {'KRUR': True,  'KUSD': True , 'BTC': True}
            for i in range(len(date)-1):
                for j in range(len(data.columns)):
                    if data.columns[j] == active.iloc[i,1]:
                        fig.add_trace(go.Scatter(x=date[i:i+2],
                                                y=capital[i:i+2],
                                                mode='lines',
                                                line=dict(color=color[data.columns[j]]),
                                                name = data.columns[j],
                                                text='''RUB: {:,.2f} <span style="color:green; font-style:italic; font-size:smaller; border: 1px solid #fff; padding: 4px;">+{:,.2f}</span><br>USD:{:,.2f} <span style="color:green; font-style:italic;font-size:smaller">+{:,.4f}</span><br>BTC: {:,.5f}  <span style="color:green; font-style:italic;font-size:smaller">+{:,.5f}'''.format(
                                                                                                                                round(sum*capital[i]*dfs[i].loc[ data.columns[0],currency],2),  round(sum*capital[i]*dfs[i].loc[data.columns[1],currency]  / sum*dfs[0].loc[ data.columns[0],currency],2) ,
                                                                                                                                round(sum*capital[i]*dfs[i].loc[ data.columns[1],currency],2), round(sum*capital[i]*dfs[i].loc[data.columns[1],currency]  / sum*dfs[0].loc[ data.columns[1],currency],5) ,
                                                                                                                                round(sum*capital[i]*dfs[i].loc[ data.columns[2],currency],8), round(sum*capital[i]*dfs[i].loc[data.columns[2],currency]  / sum*dfs[0].loc[ data.columns[2],currency],5) ).replace(',', ' '),
                                                                                                                                
                                                                                                                                showlegend =any(list(legend.values())),
                                                                                                                                ),
                                                                                                                              
                                                # row=1,
                                                # col=1  
                                                )
                        legend[data.columns[j]] = False
                        


                        # fig.add_trace(go.Scatter(x=date[i:i+2],
                                                            # y=[i for i in data.iloc[i:i+2,j]],
                                                            # mode='lines',
                                                            # line=dict(color=color[data.columns[j]]),
                                                            # name = data.columns[j],
                                                            # text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(round(data_portf[data.columns[j]]*data.loc[i,data.columns[j]]*dfs[i].loc[data.columns[0],data.columns[j]],2),
                                                            #                                                                       round(data_portf[data.columns[j]]*data.loc[i,data.columns[j]]*dfs[i].loc[data.columns[1],data.columns[j]],2), 
                                                            #                                                                       round(data_portf[data.columns[j]]*data.loc[i,data.columns[j]]*dfs[i].loc[data.columns[2],data.columns[j]],5),

                                                            #                                                                       ),
                                                            # showlegend = False,),
                                                            # row=1,  
                                                            # col=2
                                                        
                                                            # )

                        continue
                    
                    # fig.add_trace(go.Scatter(x=date[i:i+2],
                    #                             y=[i for i in data.iloc[i:i+2,j]],


                    #                             mode='lines',
                    #                             line=dict(color=color[data.columns[j]]),
                    #                             name = data.columns[j],
                    #                             text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}'''.format(
                    #                                                                                                             round(data_portf[data.columns[j]]*data.loc[i,data.columns[j]]*dfs[i].loc[data.columns[0],data.columns[j]],2),
                    #                                                                                                               round(data_portf[data.columns[j]]*data.loc[i,data.columns[j]]*dfs[i].loc[data.columns[1],data.columns[j]],2), 
                    #                                                                                                               round(data_portf[data.columns[j]]*data.loc[i,data.columns[j]]*dfs[i].loc[data.columns[2],data.columns[j]],4),
                    #                                                                                                               ),
                    #                                                                                                               showlegend= False,),
                    #                             row=1, 
                    #                             col=2 
                    #                             )
            fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor=color_light[currency])

            fig.update_yaxes(showgrid= True, gridwidth=0.5, gridcolor=color_light[currency])
                                                                                                                        
            
            # fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor=color_light[currency], row = 1, col=2)

            # fig.update_yaxes(showgrid= True, gridwidth=0.5, gridcolor=color_light[currency], row = 1, col=2)

            return fig


def inaction(currency,dfs, date, fig = go.Figure()):
            hystory = down_bd()
            sum = []
            k = 0 
            cur_port = {}
            for k in list(hystory.keys()):
                cur_port[k] = [0]
            all = []
            for i in range(len(date)):
                date[i] = date[i]  + ' 00:00:00'
            start = 0
            sum, pre_sum = 1,1
            for i in range(len(date)-1):
                al = 0

                for k in list(hystory.keys()):
                    if  date[i] in hystory[k].keys():
                        cur_port[k].append(cur_port[k][-1] + hystory[k][date[i]]['add']*dfs[i].loc[option, k])
                        al += cur_port[k][-1] + hystory[k][date[i]]['add']*dfs[i].loc[option, k]
                all.append(al)


            for j in range(len(date)):              
                if j != 0 :
                    k += 1
                    fig.add_trace(go.Scatter(x=date[j-1:j+1],
                                                                y=all[j-1:j+1],

                                                                mode='lines',
                                                                line=dict(color='purple'),
                                                                # name = col,
                                                                # text='''в рублях:{},<br> в долларах:{},<br> в биткойнах: {}, {}'''.format(sumall *dfs[j].loc[col, "KRUR"],
                                                                #                                                                     sumall *dfs[j].loc[col, "KUSD"], 
                                                                #                                                                     sumall *dfs[j].loc[col, "BTC"],
                                                                                                                                  
                                                                                                                        
                                                                                                                                ))

                                                            
                         
            # return fig
            return st.plotly_chart(fig)

def down_bd():
         # Замените значения переменных на свои
    dbname = "app_invest"
    user = "postgres"
    password = "invest"
    host = "localhost"
    port = "5432"

    # Создание подключения
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Создание курсора
    cursor = conn.cursor()

    cursor.execute("SELECT name_operations, active, value, date FROM operations")
    rows = cursor.fetchall()
    history = {'rub': {}, 'usd': {}, 'btc': {}}

    for row in rows:
        active = row[1]
        datetime_str = row[3].strftime('%Y-%m-%d %H:%M:%S')  # предполагается, что date - это объект datetime

        if active not in history:
            history[active] = {}

        if datetime_str not in history[active]:
            history[active][datetime_str] = {}

        operation_type = row[0]
        value = row[2]

        if operation_type not in history[active][datetime_str]:
            history[active][datetime_str][operation_type] = value
        else:
            history[active][datetime_str][operation_type] += value
        cursor.close()
        conn.close()
    return history
def experience(dfs, date, currency, fig):

    color_light = {'KRUR': 'rgba(255, 150, 150, 0.2)',  'KUSD':'rgba(150, 200, 255, 0.2)' , 'BTC':'rgba(255, 200, 150, 0.2)'}

    # portfel = {
    #     'KRUR': 10000,
    #     'KUSD': 100,
    #     'BTC' : 0.02
    # }
    hystory = {
            'KRUR':
                    {
                         date[5]:{'KUSD':1000},#'BTC':100
                         date[2]:{'+': 3000},
                        
                         date[6]:{'-': 1000, '+':300},
                         date[8]:{'-': 1000},


                    },

            'KUSD':
                    {
                         date[3]:{'+': 120},
                         date[4]:{'-': 50},

                         date[9]:{'+': 30},
                         date[13]:{'+': 30},
                         date[15]:{'+': 30},


                    },
            'BTC':
                    {
 
                        date[15]:{'+':0.04}                     
                    },

    }
    hystory = down_bd()
    port = {

        # 'KRUR': 10000,
        # 'KUSD': 100,
        # 'BTC' : 0.02
    }   


    color = {'KRUR': 'red',  'KUSD':'blue' , 'BTC':'orange'}
    cur_port = {
        # 'KRUR': [10000],
        # 'KUSD': [100],
        # 'BTC' : [0.02]
    }
    fig = make_subplots(rows=1, cols=2, subplot_titles = [ 'История изменения активов', 'Изменение капитала'])

    for i in range(len(date)):
        date[i] = date[i]  + ' 00:00:00'
    start = 0
    sum, pre_sum = 1,1
    for i in range(len(date)-1):
        for k in list(hystory.keys()):


            # time = datetime.strptime(list(hystory[k].keys()), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            # time = time.strftime("%Y-%m-%d")
            

            # st.write(hystory[k].keys())
            # st.write(date[i])
            # st.write(list(hystory[k].keys())[0] ==date[i])

            if k not in port.keys() and date[i] in hystory[k].keys():
                cur_port[k] = []
                cur_port[k].append(hystory[k][date[i]]['add'])#проблема
                # st.write(cur_port, ' cur_port')

                port[k] =  hystory[k][date[i]]['add']
                # st.write(cur_port[k][0]['add'])

                start += cur_port[k][0] * dfs[0].loc[option, k]


        # if date[i] in hystory.keys():
        #     if 'add' in hystory[date[i]].keys():
        #           port[hystory[date[i]]['add']]
        #     if 'withdraw' in hystory[date[i]].keys():
        #         del  port[hystory[date[i]]['withdraw']]
        for j in list(cur_port.keys()):
            
            try:

                if  list(hystory[j][date[i]].keys())[0] == 'add':

                    fig.add_trace(go.Scatter(x=[date[i],date[i]],
                                            
                                         y = [port[j] * dfs[i].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1, (port[j]* dfs[i].loc[option, j] + hystory[j][date[i]]['add']* dfs[i].loc[option, j])/cur_port[j][0]/dfs[0].loc[option, j] - 1],
                                                            
                                                            mode='lines',
                                                            line=dict(color=color[j], dash='dash'),
                                                            name = j,
                                                            text=''' + {} '''.format(hystory[j][date[i]]['add']
                                                                                                                    
                                                                                                                                  )
                                                            ),
                                                            row=1,
                                                            col=1) 
                    port[j] =  (port[j] + hystory[j][date[i]]['add'])
                    cur_port[j].append(cur_port[j][-1] + hystory[j][date[i]]['add'])
                elif list(hystory[j][date[i]].keys())[0] == 'withdraw':
                    fig.add_trace(go.Scatter(x=[date[i],date[i]],
                                            
                                         y = [port[j]* dfs[i].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1, (port[j]* dfs[i].loc[option, j] - hystory[j][date[i]]['withdraw']* dfs[i].loc[option, j])/cur_port[j][0]/dfs[0].loc[option, j] - 1],
                                             
                                                            
                                                            mode='lines',
                                                            line=dict(color=color[j], dash='dash'),
                                                            name = j,
                                                            text=''' - {} '''.format(hystory[j][date[i]]['withdraw']
                                                                                                                    
                                                                                                                                  )
                                                            ),
                                                            row=1,
                                                            col=1)
                    port[j] = (port[j] - hystory[j][date[i]]['withdraw'])
                    cur_port[j].append(cur_port[j][-1] - hystory[j][date[i]]['withdraw'])
                for k in cur_port.keys():
                    
                    if date[i] in hystory[j].keys()  and k in list(hystory[j][date[i]].keys()):

                        fig.add_trace(go.Scatter(x=[date[i],date[i]],
                    
                                    y = [port[j] * dfs[i].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1, (port[j]* dfs[i].loc[option, j] - hystory[j][date[i]][k]* dfs[i].loc[option, j])/cur_port[j][0]/dfs[0].loc[option, j] - 1],

                                    mode='lines',
                                    line=dict(color= color[j], dash='dash'),
                                    name = j,
                                    text=''' - {} '''.format(hystory[j][date[i]][k]
                                                                                            
                                                                                                            )
                                    ),
                                    row=1,
                                    col=1)

                        port[j] = (port[j] - hystory[j][date[i]][k])
                        # cur_port[j].append(cur_port[j][-1] - hystory[j][date[i]][k])
                        cur_port[j][-1] += hystory[j][date[i]][k]

                        fig.add_trace(go.Scatter(x=[date[i],date[i]],
                    
                                    y = [port[k] * dfs[i].loc[option, k]/cur_port[k][0]/dfs[0].loc[option, k] - 1, (port[k]* dfs[i].loc[option, k] + hystory[j][date[i]][k] * dfs[i].loc[option, j])/cur_port[k][0]/dfs[0].loc[option, k] - 1],

                                    
                                    mode='lines',
                                    line=dict(color=color[j] , dash='dash'),
                                    name = j,
                                    text=''' + {} '''.format(hystory[j][date[i]][k]
                                                                                            
                                                                                                            )
                                    ),
                                    row=1,
                                    col=1) 
                        port[k] = (port[k] + hystory[j][date[i]][k] * dfs[i].loc[k, j])
                        # cur_port[k].append(cur_port[k][-1] + hystory[j][date[i]][k]* dfs[i].loc[k, j])
                        cur_port[k][-1] += hystory[j][date[i]][k]* dfs[i].loc[k, j]
                                       
                if i!=len(date)-1:
                    cur_port[j].append(cur_port[j][-1])
                    
                    fig.add_trace(go.Scatter(x=[date[i],date[i+1]],
                                            
                                         y = [port[j]* dfs[i].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1, port[j]* dfs[i+1].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1],

                                                            mode='lines',
                                                            line=dict(color=color[j]),
                                                            name = j,

                                                            text='''RUB:{},<br>USD:{},<br>BTC:{}'''.format(
                                                            cur_port[j][-1] * dfs[i].loc['KRUR',j],
                                                            cur_port[j][-1] * dfs[i].loc['KUSD',j],
                                                            cur_port[j][-1] * dfs[i].loc['BTC', j])
                                                                                                                    
                                                                                                                                  )
                                                            ,
                                                            row=1,
                                                            col=1 )
            except:
                if i!=len(date)-1:
                    fig.add_trace(go.Scatter(x=[date[i],date[i+1]],
                                            
                                         y = [port[j] * dfs[i].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1, port[j]* dfs[i+1].loc[option, j]/cur_port[j][0]/dfs[0].loc[option, j] - 1],
                                                            
                                                            mode='lines',
                                                            line=dict(color= color[j]),
                                                            name = j,

                                                            text='''RUB:{},<br>USD:{},<br>BTC:{}'''.format(
                                                            cur_port[j][-1] * dfs[i].loc['KRUR',j],
                                                            cur_port[j][-1] * dfs[i].loc['KUSD',j],
                                                            cur_port[j][-1] * dfs[i].loc['BTC', j])
                                                                                                                    
                                                                                                                                  )
                                                            ,
                                                            row=1,
                                                            col=1 )
                cur_port[j].append(cur_port[j][-1])

                    
        sum_change = 0
        for k in list(cur_port.keys()):
            sum += cur_port[k][-1] * dfs[i].loc[option, k]
            sum_change += (cur_port[k][-1] - cur_port[k][-2]) * dfs[i].loc[option, k]

        c = 0
        for j in list(port.keys()):
                try:
                    if list(hystory[j][date[i]].keys())[0] == 'add' or list(hystory[j][date[i]].keys())[0] == 'withdraw':
                        c += 1
                except:
                    pass
        if c>0:
            fig.add_trace(go.Scatter(x=date[i-1:i+1],
                                                    
                                                                    y = [pre_sum, pre_sum* dfs[i].loc[option, k]/ dfs[i-1].loc[option, k]],
                                                                    mode='lines',
                                                                    line=dict(color='white'),
                                                                    name = 'Капитал',
                                                                    text='''RUB:{},<br>USD:{},<br>BTC:{}'''.format(
                                                                        sum * dfs[i-1].loc['KRUR',option],
                                                                        sum * dfs[i-1].loc['KUSD',option],
                                                                        sum * dfs[i-1].loc['BTC', option]                  
                                                                                                                                            )
                                                                    ),
                                                            row=1,
                                                            col=2 
                                                            )
            fig.add_trace(go.Scatter(x=[date[i],date[i]],
                                                y = [pre_sum* dfs[i].loc[option, k]/ dfs[i-1].loc[option, k], sum/start],
                                                mode='lines',
                                                line=dict(color='white', dash = 'dash'),
                                                name = 'Капитал',
                                                        text='''RUB:{},<br>USD:{},<br>BTC:{}'''.format(
                                                            sum * dfs[i].loc['KRUR',option],
                                                            sum * dfs[i].loc['KUSD',option],
                                                            sum * dfs[i].loc['BTC', option]
                                                                                                    
                                                                                                                        )
                                                ),
                                                            row=1,
                                                            col=2 
                                                            )


                    
        else:
                fig.add_trace(go.Scatter(x=date[i-1:i+1],
                                        
                                                        y = [pre_sum, sum/start],
                                                        mode='lines',
                                                        line=dict(color='white'),
                                                        name = 'Капитал',
                                                        text='''RUB:{},<br>USD:{},<br>BTC:{}'''.format(
                                                            sum * dfs[i-1].loc['KRUR',option],
                                                            sum * dfs[i-1].loc['KUSD',option],
                                                            sum * dfs[i-1].loc['BTC', option]

                                                                                                            
                                                                                                                                )
                                                        ),
                                                            row=1,
                                                            col=2 
                                                            )
                                                            
        pre_sum = sum/start
        sum = 0

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor=color_light[currency])

    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor=color_light[currency])

    # return fig
    return st.plotly_chart(fig)






def uno(dfs, date, currency, fig):

    coin = 10000
    # fig = go.Figure()
    for i in range(len(dfs)-1):
                for col in dfs[i].columns:
                        if col == 'KRUR':
                            color = 'red'
                        elif col == 'KUSD':
                            color = 'blue'
                        else:
                            color = 'orange'
                        fig.add_trace(go.Scatter(x=date[i:i+2],
                                                            y=[coin*dfs[i].loc[col,option]/dfs[0].loc[col,option],coin*dfs[i+1].loc[col, option]/dfs[0].loc[col,option] ],

                                                            mode='lines',
                                                            line=dict(color=color),
                                                            name = col,
                                                            ))  
    return st.plotly_chart(fig)

    
     
def exp():
    
    # Список элементов для выпадающего списка
    options = ['Max', 'Min', 'inaction', 'Users']

    # Виджет выпадающего списка
    selected_option = st.multiselect("Выберите вариант:", options)
    # st.write(selected_option)
    fig = go.Figure()
    if 'Max' in selected_option:
        MAX_MIN(option, pd.DataFrame.max, pd.Series.idxmax, dfs,date, sum,st.session_state.portfolio, fig)
    if 'Min' in selected_option:
        MAX_MIN(option, pd.DataFrame.min, pd.Series.idxmin, dfs,date, sum, st.session_state.portfolio, fig)
    if 'inaction' in selected_option:
        inaction(option, dfs1, date1, fig, sum)
    if 'Users' in selected_option:
         experience(dfs, date, option, fig)
    # fig.update_layout(yaxis_type="log")
    # st.write(sum)
    return st.plotly_chart(fig)
     

dfs,date = download(frequency)
sum = 0
for i in st.session_state.portfolio.keys():
        sum += st.session_state.portfolio[i] * dfs[0].loc[option, i]

dfs1, date1 = download(1)
# MAX_MIN(option, pd.DataFrame.max, pd.Series.idxmax, dfs,date, sum,st.session_state.portfolio)
# MAX_MIN(option, pd.DataFrame.min, pd.Series.idxmin, dfs,date, sum, st.session_state.portfolio)
# inaction(option, dfs1, date1)
# uno(dfs, date, option)
# fig = go.Figure()
# exp()
fig = go.Figure()
# inaction(option, dfs1, date1, fig)
# st.plotly_chart(inaction(option, dfs1, date1, fig))
experience(dfs, date[:30], option, fig)



# Закрытие курсора и соединения


# @st.cache(allow_output_mutation=True, hash_funcs={type: lambda x: None})
# def exp_wrapper(portfolio_keys):
#     sum = 0
#     for i in portfolio_keys:
#         sum += st.session_state.portfolio[i] * dfs[0].loc[option, i]
#     exp(sum, portfolio_keys)

# # Преобразуйте dict_keys в список
# portfolio_keys_list = list(st.session_state.portfolio.keys())

# # Используйте exp_wrapper с передачей списка вместо dict_keys
# exp_wrapper(portfolio_keys_list)

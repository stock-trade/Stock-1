#-*-coding=utf-8-*-
import datetime
import os

from setting import get_engine
import pandas as pd
import tushare as ts
import numpy as np
from plot_line import plot_stock_line
'''
昨日涨停的今日的实时情况
'''

def monitor():
    engine = get_engine('db_zdt')
    table='20180409zdt'
    api=ts.get_apis()
    df = pd.read_sql(table,engine,index_col='index')
    # print df
    price_list=[]
    percent_list=[]
    amplitude_list=[]
    start=datetime.datetime.now()
    for i in df[u'代码'].values:
        try:
            curr= ts.quotes(i,conn=api)
            last_close =curr['last_close'].values[0]
            curr_price =curr['price'].values[0]
            amplitude=round(((curr['high'].values[0]-curr['low'].values[0])*1.00/last_close)*100,2)
            # if last_close>=curr_price:
            # print i,
            # print df[df[u'代码']==i][u'名称'].values[0],
            # print  percent
        except Exception,e:
            print e
            curr_price=0
        if last_close==0:
            percent= np.nan
        percent = round((curr_price - last_close) * 100.00 / last_close, 2)
        percent_list.append(percent)
        price_list.append(curr_price)
        amplitude_list.append(amplitude)

    df[u'今日价格']=price_list
    df[u'今日涨幅']=percent_list
    df[u'今日振幅']=amplitude_list
    df[u'更新时间']=datetime.datetime.now().strftime('%Y %m %d %H:%M%S')

    # print df
    # df[df['today_price']==0]
    end=datetime.datetime.now()
    print 'time use {}'.format(end-start)

    df.to_sql(table+'monitor',engine,if_exists='replace')
    ts.close_apis(api)

'''
绘制k线图，今日暂停的k线图
'''
def plot_yesterday_zt():
    engine = get_engine('db_zdt')
    table='20180413zrzt'
    df = pd.read_sql(table,engine)
    for i in range(len(df)):
        code = df.iloc[i][u'代码']
        name = df.iloc[i][u'名称']
        plot_stock_line(code,name,save=True)

if __name__ == '__main__':
    os.chdir('data')
    plot_yesterday_zt()
import pandas as pd
import numpy as np
from matplotlib import dates
import matplotlib.pyplot as plt


def preprocess(df):
    df = df[['Date', 'Heure / Time', 'Vélos depuis le 1er janvier / Grand total', "Vélos ce jour / Today's total"]]
    df.rename(columns = {'Heure / Time': 'Time', 'Vélos depuis le 1er janvier / Grand total' : 'Total', "Vélos ce jour / Today's total" : "TodayTotal"}, inplace = True)
    df.drop(0,0,inplace=True)
    df.drop(1,0,inplace=True)
    df.sort_values('Date',ascending= True)
    
    # Remove missing hours cases by np.nan

    df['Time']=df['Time'].replace('', np.nan)
    df.dropna(subset=['Time'], inplace=True)
    
    dfdatetime = df['Date'].astype(str) +' '+ df['Time'].astype(str) 
    time_improved = pd.to_datetime(dfdatetime, format = '%d/%m/%Y %H:%M:%S')
    df['Time'] = time_improved
    
    
    
    # Remove useless columns
    del df['Date']
    del df['Total']

    index_with_nan = df.index[df.isnull().any(axis=1)]
    df.drop(index_with_nan,0, inplace=True)

    df['DayofWeek'] = df['Time'].dt.dayofweek
    df['Day'] = df['Time'].dt.day
    df['Month'] = df['Time'].dt.month
    df['Year'] = df['Time'].dt.year
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute

    df.set_index('Time',inplace=True)
    
    return df






def timeseries_plot(y, color, y_label):
    # y is Series with index of datetime
    days = dates.DayLocator()
    dfmt_minor = dates.DateFormatter('%m-%d')
    weekday = dates.WeekdayLocator(byweekday=(), interval=1)

    fig, ax = plt.subplots()
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_minor_formatter(dfmt_minor)

    ax.xaxis.set_major_locator(weekday)
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%a'))

    ax.set_ylabel(y_label)
    ax.plot(y.index, y, color)
    fig.set_size_inches(12, 8)
    plt.tight_layout()
    plt.savefig(y_label + '.png', dpi=300)
    plt.show()

# average time series


def bucket_avg(ts, bucket):
    # ts is Sereis with index
    # bucket =["30T","60T","M".....]
    y = ts.resample(bucket).mean()
    return y


def config_plot():
    plt.style.use('seaborn-paper')
#    plt.rcParams.update({'axes.prop_cycle': cycler(color='jet')})
    plt.rcParams.update({'axes.titlesize': 20})
    plt.rcParams['legend.loc'] = 'best'
    plt.rcParams.update({'axes.labelsize': 22})
    plt.rcParams.update({'xtick.labelsize': 16})
    plt.rcParams.update({'ytick.labelsize': 16})
    plt.rcParams.update({'figure.figsize': (10, 6)})
    plt.rcParams.update({'legend.fontsize': 20})
    return 1




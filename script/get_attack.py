import numpy as np
import pandas as pd
import re


def get_attack(start_time, end_time):
    '''
    Args:
        - start_time: <np.datetime64>
        - end_time: <np.datetime64>
    Returns:
        - feature_list: <list>[<list>], e.g. [['LIT101'], ['AIT101', 'LIT201']]
        - anomaly_start_time_list: <list>[<np.datetime64>], e.g. [array('2015-12-28T10:44:53', dtype='datetime64[s]'), array('2015-12-28T10:58:30', dtype='datetime64[s]')]
        - anomaly_end_time_list: <list>[<np.datetime64>], e.g. [array('2015-12-28T10:44:53', dtype='datetime64[s]'), array('2015-12-28T10:58:30', dtype='datetime64[s]')]
    Reminder: 
        - Return lists have the same length.
    '''

    df = pd.read_excel('data/swat-2015-attack.xlsx') ##read data
    df = df[['Start Time', 'End Time', 'Attack Point']] 
    df1 = df.iloc[:41].dropna()
    df1 = df1.reset_index(drop=True)
    df1['Start Time'] = pd.to_datetime(df1.loc[:,'Start Time']) # Series



    ### regulate End Time
    Start_time = df1['Start Time'].to_string()  #Series to string
    date = re.findall("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", Start_time) #extract all times
    End_time = df1['End Time']

    End_Time = []
    for i in range(len(date)):
        End_Time.append(date[i]+' '+str(End_time[i]))
    df1['End Time'] = End_Time
    df1['End Time'] = pd.to_datetime(df1['End Time'])


    ### regulate Attack Point
    Attack_point = df1['Attack Point']
    b =[]
    for i in range(len(Attack_point)):
        b.append(str(Attack_point[i]).split(', '))
    df1['Attack Point'] = b
        

    ### get the require row index
    start = df1[df1['Start Time'] == start_time].index.tolist()[0]
    end = df1[df1['End Time'] == end_time].index.tolist()[0]
    feature_list = df1['Attack Point'][start:end].tolist()
    anomaly_start_time_list = df1['Start Time'][start:end].to_numpy(dtype='datetime64[s]')
    anomaly_end_time_list = df1['End Time'][start:end].to_numpy(dtype='datetime64[s]')

    return feature_list, anomaly_start_time_list, anomaly_end_time_list

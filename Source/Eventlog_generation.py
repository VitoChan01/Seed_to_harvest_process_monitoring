import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pm4py
import pickle
import itertools
import seed_to_harvest as sth

#Dir path
sites_pth = 'Source/Data/sites'
cdl_pth = 'Source/Data/cdl'
season_pth = 'Source/Data/season'

loglist=[]
warningslist=[]
faillist=[]
#load location list
location=np.load('Source/masklayers/wgscenterlist.npy')
for i in np.arange(0,148,1):
    #loading data
    sid=i
    ts=pd.read_hdf(sites_pth+f'/Site{sid:03}_NBARint.h5')
    cdl=pd.read_hdf(cdl_pth+f'/Site{sid:03}_cdl.h5')
    season=pd.read_hdf(season_pth+f'/Site{sid:03}_season_day.h5')
    loc=location[i]

    try:
        timelog, warnings = sth.eventtime_MACD(ts, season, cdl, sid, loc, 2007)
        loglist.append(timelog)
        warningslist.append(warnings)
    except Exception as e:
        print(f"Error encountered for site {sid}: {e}")
        faillist.append(sid)
timelog=pd.concat(loglist, axis=0, join='inner', ignore_index=True)

#cleaning according to CDL
def warn_mark(i,n):
    return f"{i:04}_{n+2007}"
def warn_site_years(Lst):
    threshold=np.nonzero(np.array(Lst[1])<0.75)[0]
    return list(map(lambda x: warn_mark(Lst[0], x), threshold))

with open(cdl_pth+"/ConsistencyPerc", "rb") as fp:   # Unpickling
    site_consistencyL = pickle.load(fp)

CaseID_anom=list(map(warn_site_years, enumerate(site_consistencyL)))

flat_CaseID_anom = list(itertools.chain.from_iterable(CaseID_anom))

timelog['Multiple_crop'] = 0

timelog.loc[timelog['CaseID'].isin(flat_CaseID_anom), 'Multiple_crop'] = 1

#report results
print('number of all detected rotation: ',timelog.shape[0]/4)
print('number of rotation failed: ',16*148-timelog.shape[0]/4)
print('number of rotation with multiple crops on field: ',timelog[timelog['Multiple_crop'] != 0].shape[0]/4)
print('number of rotation with single crop on field: ',timelog[timelog['Multiple_crop'] == 0].shape[0]/4)
print('number of cases with multiple crops on field: ',len(flat_CaseID_anom))

#save the event log
timelog.to_hdf(f'Event_log/log_148sites_240129_df.h5', key='df', mode='w') 
if __name__ == "__main__":
    dataframe = pm4py.format_dataframe(timelog, case_id='CaseID', activity_key='Activity', timestamp_key='Timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    pm4py.write_xes(event_log, 'Event_log/148sites_240129.xes')


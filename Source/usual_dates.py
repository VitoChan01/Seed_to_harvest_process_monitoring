import matplotlib.pyplot as plt
import pandas as pd

#load log
timelog=pd.read_hdf('Event_log/log_148sites_240129_df.h5')

#source usda field crops usual planting and harvesting --idaho
#https://downloads.usda.library.cornell.edu/usda-esmis/files/vm40xr56k/dv13zw65p/w9505297d/planting-10-29-2010.pdf
potato_usual=[[pd.Timestamp(2009, 4, 6).dayofyear,pd.Timestamp(2009, 6, 9).dayofyear]
              ,[pd.Timestamp(2009, 8, 15).dayofyear,pd.Timestamp(2009, 10, 27).dayofyear]]

alfalfa_usual=[[0,0]
               ,[pd.Timestamp(2009, 5, 22).dayofyear,pd.Timestamp(2009, 10, 20).dayofyear]]

sugarbeets_usual=[[pd.Timestamp(2009, 3, 24).dayofyear,pd.Timestamp(2009, 5, 5).dayofyear]
                  ,[pd.Timestamp(2009, 9, 15).dayofyear,pd.Timestamp(2009, 11, 10).dayofyear]]

springwheat_usual=[[pd.Timestamp(2009, 3, 21).dayofyear,pd.Timestamp(2009, 5, 26).dayofyear]
                   ,[pd.Timestamp(2009, 8, 4).dayofyear,pd.Timestamp(2009, 9, 29).dayofyear]]

winterwheat_usual=[[pd.Timestamp(2008, 9, 8).dayofyear,pd.Timestamp(2008, 11, 3).dayofyear]
                   ,[pd.Timestamp(2009, 7, 23).dayofyear,pd.Timestamp(2009, 9, 14).dayofyear]]

timelog['Day_of_Year'] = timelog['Timestamp'].dt.dayofyear

crops = ['Potatoes', 'Spring Wheat', 'Sugarbeets']
usual = [potato_usual, springwheat_usual, sugarbeets_usual]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12,5))
axes=axes.flatten()

for i, crop in enumerate(crops):
    crop_df = timelog[timelog['Multiple_crop']==0][timelog[timelog['Multiple_crop']==0]['Crop'] == crop]
    axes[i].boxplot([crop_df[crop_df['Activity'] == activity]['Day_of_Year'] for activity in ['Emergence', 'Maturity', 'Senescence', 'Dormancy']], labels=['Emergence', 'Maturity', 'Senescence', 'Dormancy'])
    axes[i].hlines(usual[i][0], 0.5, 1.5, ls='--', lw=1.5, color='g', label='usual planting')
    axes[i].hlines(usual[i][1], 3.5, 4.5, ls='--', lw=1.5, color='r', label='usual harvesting')
    axes[i].set_ylabel('Day of Year')
    axes[i].set_title(f'{crop}')
    axes[i].set_xlabel('Activity')
    axes[i].legend()


plt.suptitle('Result distribution with usual planting and harvesting dates')
plt.tight_layout()
plt.savefig('Result/boxplot_3crop.pdf', format='pdf')
plt.show()

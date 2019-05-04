import arcpy
from datetime import datetime, timedelta
import pandas as pd
from geopy.distance import great_circle

#arcpy.env.workspace = r'C:\Users\User\Desktop\WAZE\TN'
'''
def distance(p1,p2):
    x1, y1 = p1[0]), p1[1]
    x2, y2 = p2[0]), p2[1]
    distance = math.hypot(x1-x2, y1-y2)
    return distance
'''
def time_diff(time1, time2):
    datetimeFormat = '%m/%d/%Y %H:%M'
    time_diff = datetime.strptime(time1, datetimeFormat) - datetime.strptime(time2, datetimeFormat)
    mins = timedelta.total_seconds(time_diff)/60
    return abs(mins)
   
#shp1 = 'offical_acc'
#shp2 = 'waze_acc_region1'

#spatial_ref = arcpy.Describe(shp1).spatialReference
waze_df = pd.read_csv(r'C:\Users\User\Desktop\WAZE\Presentation-10132017\waze_acc_route.csv')
report_df = pd.read_csv(r'C:\Users\User\Desktop\WAZE\Presentation-10132017\acc_report_coor_real.csv')

report_df['match'] = 0
waze_df['match'] = 0

report_out = []
waze_out = []
for i, row in report_df.iterrows():
    dur = row['blkDuration']
    time1 = row['inc_start']
    p1 = str(row['coordinate']).split(',')
    for j, each in waze_df.iterrows():
        try:
            time2 = each['pubDate']
            p2 = str(each['ns2_point']).split(' ')
            d = great_circle((float(p1[0]), float(p1[1])), (float(p2[0]), float(p2[1]))).miles
            time = time_diff(time1, time2)
            if d < 0.5 and time < max(1, dur):
                print(d)
                report_out.append(row)
                waze_out.append(each)
        except:
            continue


pd.DataFrame(report_out).to_csv(r'C:\Users\User\Desktop\report_matched.csv')
pd.DataFrame(waze_out).to_csv(r'C:\Users\User\Desktop\waze_matched.csv')

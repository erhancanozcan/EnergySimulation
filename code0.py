#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:18:52 2021

@author: can
"""
import sys
import os
script_location="/Users/can/Desktop/energy/code"
os.chdir(script_location)
import numpy as np
import pandas as pd
#import datetime
from datetime import datetime
%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import random
#%%
from single_house import Home
outside_temp=np.array([4,4,4,4,3,3,3,3,2,2,2,2,
                       4,4,4,4,4,4,4,4,4,4,4,4,
                       4,4,4,4,5,5,5,5,6,7,7,7,
                       7,7,7,7,7,7,7,7,7,8,10,11,
                       11,12,12,12,12,12,12,12,12,12,12,12,
                       10,10,8,8,7,7,5,5,5,5,5,5,
                       4,4,4,4,4,4,4,4,4,4,4,4,
                       4,4,4,4,4,4,4,4,4,4,4,4])

# gamma1 large ==>low_insulation level
# gamma2 large ==>low size
ins_type="low"
house_size="large"

house_type={"insulation":ins_type,"size":house_size}
#%%
num_houses=2
village=[]

for i in range(num_houses):
    #generate_home
    home1=Home(outside_temp+5*i,house_type)
    village.append(home1)
    
    #generate orders
    start_time="00:00"
    water_usage=random.uniform(0,home1.ewh.capacity/2)
    des_temp=42
    order_ewh={"starting_time":start_time,
               "water_amount":water_usage,
               "desired_temp": des_temp,
               "order_status": 1}




    amp=np.random.randint(5,9)
    start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
    order_ev={"starting_time":start_time,
              "amps": amp,
               "battery_level":0.95,
               "desired_level": 1.0,
               "order_status": 1}

    start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
    order_wm={"starting_time":start_time,
               "order_status": 1}

    start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
    order_dryer={"starting_time":start_time,
               "order_status": 1}

    start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
    order_oven={"starting_time":start_time,
               "order_status": 1}

    time_r=15
    n_row=int(24*60/time_r)#the length of outside temperature list and set list.
    set_temp=np.repeat(25.0-2*i,n_row)
    order_HVAC={"set_temperature":set_temp}
    ###orders are generated.
    
    village[i].get_orders(order_ewh,order_ev,order_wm,order_dryer,order_oven,order_HVAC)
    
#%%
change_in_orders=False
order_ewh["order_status"]=0
order_ev["order_status"]=0
order_wm["order_status"]=0
order_dryer["order_status"]=0
order_oven["order_status"]=0
#repeat below for each house
i=0
if change_in_orders==True:
    print("orders are updated")
    
outside_temp=np.roll(village[i].outside_temp, -1)
outside_temp[n_row-1]=outside_temp[n_row-1]+np.random.normal(1,0.1,1)
village[i].get_orders(order_ewh,order_ev,order_wm,order_dryer,order_oven,order_HVAC)
village[i].check_activity_status()
village[i].plot_load("HVAC")
village[i].shift(outside_temp)

#%%

#in a for loop
###generate orders
###uptade outside temperature
###shift time for home
start_time="00:00"
water_usage=random.uniform(0,home1.ewh.capacity/2)
des_temp=42
order_ewh={"starting_time":start_time,
           "water_amount":water_usage,
           "desired_temp": des_temp,
           "order_status": 1}





start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
order_ev={"starting_time":start_time,
           "battery_level":0.95,
           "desired_level": 1.0,
           "order_status": 1}

start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
order_wm={"starting_time":start_time,
           "order_status": 1}

start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
order_dryer={"starting_time":start_time,
           "order_status": 1}

start_time=str(random.randint(0, 24)).zfill(2)+":"+str(random.randint(0, 59)).zfill(2)
order_oven={"starting_time":start_time,
           "order_status": 1}

time_r=15
n_row=int(24*60/time_r)#the length of outside temperature list and set list.
set_temp=np.repeat(25.0,n_row)
order_HVAC={"set_temperature":set_temp}


#%%
home1=Home(outside_temp)
home1.get_orders(order_ewh,order_ev,order_wm,order_dryer,order_oven,order_HVAC)

home1.plot_load("ewh")
home1.plot_load("ev")
home1.plot_load("wm")
home1.plot_load("refrigerator")
home1.plot_load("dryer")
home1.plot_load("oven")
home1.plot_load("HVAC")
home1.plot_load("pv")



#%%

from ewh import SimpleWaterHeater
ewh=SimpleWaterHeater(1,15)

start_time="00:00"
ewh.heat_water(start_time, water_amount=10,tap_water_temp=4,desired_temp=42)
#requiredQ=10*1*(42-4) ====> Q=(m)(c)(/delta T)
start_time="12:00"
ewh.heat_water(start_time, water_amount=30,tap_water_temp=4,desired_temp=42)
start_time="20:00"
ewh.heat_water(start_time, water_amount=60,tap_water_temp=4,desired_temp=42)
start_time="23:55"
ewh.heat_water(start_time, water_amount=80,tap_water_temp=4,desired_temp=42)
#%%
ax_ev=ewh.load_int.plot(ylim=(0,3))
ax_ev.set(xlabel='Time', ylabel='KWatt')
ax_ev.set_title("Load Curve")
ax_ev.legend(["EWH"])
plt.show()
ewh.shift_time()
#%%

from ev import ev
ev1=ev(1,15)

start_time="00:00"
ev1.charge_battery(start_time, 0.95, 1.0)
start_time="12:00"
ev1.charge_battery(start_time, 0.1, 0.5)
start_time="20:00"
ev1.charge_battery(start_time, 0.5, 0.6)
start_time="23:55"
ev1.charge_battery(start_time, 0.5, 0.7)
#ev1.report_load_curve()
#ev1.load_int
#%%
ax_ev=ev1.load_int.plot(ylim=(0,3))
ax_ev.set(xlabel='Time', ylabel='KWatt')
ax_ev.set_title("Load Curve")
ax_ev.legend(["EV"])
plt.show()
ev1.shift_time()
#%%
from other_appliances import refrigerator
refrigerator1=refrigerator(15)
#%%
refrigerator1.load_int.plot()
refrigerator1.shift_time_ref()
#%%
from other_appliances import washing_machine,dryer,oven
washing_machine1=washing_machine(15)

start_time="00:00"
washing_machine1.schedule(start_time)
start_time="12:00"
washing_machine1.schedule(start_time)
start_time="23:30"
washing_machine1.schedule(start_time)

#%%
washing_machine1.load_int.plot()
washing_machine1.shift_time()

#%%

# gamma1 large ==>low_insulation level
# gamma2 large ==>low size

ins_type="low"
house_size="small"

house_type={"insulation":ins_type,"size":house_size}

if house_type["insulation"] =="low":
    gamma1=np.random.normal(0.15,0.001)
elif house_type["insulation"] =="high":
    gamma1=np.random.normal(0.10,0.001)
if house_type["size"] =="small":
    gamma1=np.random.normal(0.0000035,0.0000001)
elif house_type["size"] =="large":
    gamma1=np.random.normal(0.0000020,0.0000001)




#gamma1 low mean 0.05
#gamma1 high mean 0.10
from HVAC import Heating
#HVAC1=Heating(0.10,0.0000020,3,28.0,15,heater_type=1) #high insulation large house
#HVAC1=Heating(0.15,0.0000020,3,28.0,15,heater_type=1) #low insulation large house
#HVAC1=Heating(0.10,0.0000035,3,28.0,15,heater_type=1)  #high insulation small house
HVAC1=Heating(0.15,0.0000035,3,28.0,15,heater_type=1) ##low insulation small house

n_row=int(24*60/HVAC1.time_r)#the length of outside temperature list and set list.
outside_temp=np.array([4,4,4,4,3,3,3,3,2,2,2,2,
                       4,4,4,4,4,4,4,4,4,4,4,4,
                       4,4,4,4,5,5,5,5,6,7,7,7,
                       7,7,7,7,7,7,7,7,7,8,10,11,
                       11,12,12,12,12,12,12,12,12,12,12,12,
                       10,10,8,8,7,7,5,5,5,5,5,5,
                       4,4,4,4,4,4,4,4,4,4,4,4,
                       4,4,4,4,4,4,4,4,4,4,4,4])

set_temp=np.repeat(24.0,n_row)


#outside_temp=outside_temp+10

#%%

HVAC1.simulate_temperature(outside_temp, set_temp)
HVAC1.load_int.plot()
ax1=HVAC1.temp_pred.plot()
ax1.plot(HVAC1.temp_pred.index,outside_temp[1:96])
ax1.set(xlabel='Time', ylabel='°C')
ax1.set_title("Temperature Curve")
ax1.legend(["Inside","Outside"])

outside_temp=np.roll(outside_temp, -1)
outside_temp[n_row-1]=outside_temp[n_row-1]+np.random.normal(1,0.1,1)
HVAC1.shift_time()
print(HVAC1.inside_temp)







#%%
from pv import PV



os.chdir('/Users/can/Desktop/energy/code/solar_data/boston')
solar_irradiation_data=pd.read_csv('2784951_42.38_-71.13_2018.csv') 

PV1=PV(1,15,solar_irradiation_data,eff=0.2)


#%%
ax_pv=PV1.report.plot()
ax_pv.set(xlabel='Time', ylabel='Generated KW')
ax_pv.set_title("Load Curve")
ax_pv.legend(["PV"])
PV1.shift_time()

#%%
#used pvlib library to generate solar panel pv laod curve.
"""
https://pvlib-python.readthedocs.io/en/stable/package_overview.html
"""
#estimate pv for an apartment in NY
m2_covered=1.0
#from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
# specify location (Tucson, AZ)
latitude, longitude, tz = 40.7, -74.0, 'America/New_York'
#latitude, longitude, tz = 37.8, -122.4, 'America/Los_Angeles'
#start = pd.Timestamp(datetime.date.today(), tz=tz)
start = pd.Timestamp(datetime.now(), tz=tz)
#start=pd.Timestamp('2018-1-01 00:00', tz='America/New_York')
end = start + pd.Timedelta(hours=24)
#end = start + pd.Timedelta(days=15)
irrad_vars = ['ghi', 'dni', 'dhi']


from pvlib.pvsystem import PVSystem, retrieve_sam
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.tracking import SingleAxisTracker
from pvlib.modelchain import ModelChain

sandia_modules = retrieve_sam('sandiamod')

cec_inverters = retrieve_sam('cecinverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']

inverter = cec_inverters['SMA_America__SC630CP_US__with_ABB_EcoDry_Ultra_transformer_']

temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# model a big tracker for more fun
system = SingleAxisTracker(module_parameters=module, inverter_parameters=inverter, temperature_model_parameters=temperature_model_parameters, modules_per_string=15, strings_per_inverter=300)

from pvlib.forecast import GFS
# fx is a common abbreviation for forecast
fx_model = GFS()

fx_data = fx_model.get_processed_data(latitude, longitude, start, end)



#data is given 5 mins intervals. We consider only first 5days.
how_many_steps=int((60/5)*24*30)

os.chdir('/Users/can/Desktop/energy/code/solar_data/boston')
#sys.path.insert(0, '/Users/can/Desktop/energy/code/solar_data/boston/')
new_fx_data=pd.read_csv('2784951_42.38_-71.13_2018.csv')  
new_fx_data=new_fx_data.iloc[:,[5,6,7]]

new_fx_data.columns=np.char.lower(new_fx_data.iloc[1,:].values.astype('<U5'))
new_fx_data=new_fx_data.drop([0,1])
new_fx_data['ghi'] = new_fx_data['ghi'].astype(float)
new_fx_data['dhi'] = new_fx_data['dhi'].astype(float)
new_fx_data['dni'] = new_fx_data['dni'].astype(float)
new_fx_data=new_fx_data.iloc[:8640,]

#update_time_periods=pd.date_range("2018-01-01", "2018-01-31", freq="5min").strftime('%H:%M')
update_time_periods=pd.date_range("2018-01-01", "2018-01-31", freq="5min")
update_time_periods=update_time_periods[:8640]
new_fx_data.index=update_time_periods
# use a ModelChain object to calculate modeling intermediates
mc = ModelChain(system, fx_model.location)


#fx_data['temp_air']=20.0


#ghi,dni,dhi is enough to make prediction.
#fx_data=fx_data.iloc[:,[2,3,4]]
# extract relevant data for model chain
mc.run_model(new_fx_data)
#mc.results.total_irrad.plot();

irradiation_per_msq=mc.results.total_irrad['poa_global']*m2_covered
irradiation_per_msq.index=irradiation_per_msq.index.strftime('%H:%M')

time_tmp=np.arange(0,8640,3)

irradiation_per_msq.iloc[time_tmp,]

#%%
#code below performs interpolation.
tmp=irradiation_per_msq.index.strftime('%H:%M')
irradiation_per_msq=pd.DataFrame(irradiation_per_msq)
irradiation_per_msq=irradiation_per_msq.set_index(tmp)


time_periods=pd.date_range("00:00", "23:45", freq="15min").strftime('%H:%M')

start = pd.Timestamp(datetime.now(), tz=tz).strftime('%H:%M')

tmp=np.where(start>=time_periods)[0]
s_index=tmp[len(tmp)-1]
adjusted_start_time=time_periods[s_index]

end = start + pd.Timedelta(hours=24)


pd.date_range("00:00", last, freq=f).strftime('%H:%M')

generated_energy=pd.DataFrame(index=ev1.load_int.index)
generated_energy=generated_energy.join(irradiation_per_msq)
generated_energy.iloc[0,0]=0.0
generated_energy=generated_energy['poa_global'].interpolate()
#interpolation is completed.



ax_pv=generated_energy.plot()
ax_pv.set(xlabel='Time', ylabel='AC Power (W)')
ax_pv.set_title("Generated Energy from PV")
ax_pv.legend(["PV"])
plt.show()

#%%
"""
plt.legend(loc='best');
mc.results.ac.fillna(0).plot();
plt.ylim(0, None);
plt.ylabel('AC Power (W)');
"""

#%%
#read parquet data
deneme=pd.read_parquet("100137-0.parquet")

a=deneme.columns
#%%

#b=deneme[['timestamp','out.electricity.water_systems.energy_consumption']]
b=deneme[['timestamp','out.electricity.heating.energy_consumption']]
b.iloc[:,1]=b.iloc[:,1]*3600*1000

filtered_b = b.loc[(b['timestamp'] >= '2018-01-03')
                     & (b['timestamp'] <= '2018-01-04')]

filtered_b.index=filtered_b.timestamp

filtered_b=filtered_b.drop(columns=['timestamp'])

filtered_b.plot()




"""
df = pd.DataFrame({'num_posts': [4, 6, 3, 9, 1, 14, 2, 5, 7, 2],
                   'date': ['2020-08-09', '2020-08-25', 
                            '2020-09-05', '2020-09-12', 
                            '2020-09-29', '2020-10-15',
                            '2020-11-21', '2020-12-02', 
                            '2020-12-10', '2020-12-18']})

type(df.date)
df.date.values[0]

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df.date.values[0]

type(b.timestamp)
b.timestamp.values[0]
"""

#%%

#%%




import pytz
import inspect
import pvlib
pytz.country_timezones('US')[0]

pd.Timestamp('2021-12-18 00:00', tz='America/New_York')

pvlib_abspath = os.path.dirname(os.path.abspath(inspect.getfile(pvlib)))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 20:38:51 2021

@author: can
"""
import numpy as np
import pandas as pd
import datetime
import math

class Heating:
    
    #by one watt energy 3.4BTU per hour
    #1/3.4  BTU per hour can be achieved by 1 watt energy.
    #1 BTU = 1055.056 watt-seconds.
    #1 BTU/h=0.00029 kW or BTU/EER = watts
    #1sq feet requires 20BTU ===> multiple sq feet by 20
    def __init__(self, gamma1,gamma2,gamma3,inside_temp,time_resolution,heater_type=1,heating_season=1):
        self.inside_temp=inside_temp
        self.heater_type=heater_type
        self.heating_season=heating_season
        self.time_r=time_resolution
        self.gamma1=gamma1
        self.gamma2=gamma2
        self.gamma3=gamma3
        self.solar_irradiation=0#we may need to  adjust this part.
        
        if self.heater_type==1:
            #nominal power indicates the instanteneous electric consumption
            #during charging.
            #battery capacity indicates the max_charge capacity.
            self.heater_efficiency=0.9
            self.power_heater=3000*(60*self.time_r) #1000 is the instanteneous power. (60*time is the second)
        if time_resolution>=60:
            raise Exception("Time resolution cannot be greater than or equal to 60.")
        last="23:"+str(60-time_resolution)
        f=str(time_resolution)+"min"
        time_periods=pd.date_range("00:00", last, freq=f).strftime('%H:%M')
        
        self.load_int=pd.DataFrame(index=np.arange(len(time_periods)))
        self.nrow=len(time_periods)
        
        self.load_int=self.load_int.set_index(time_periods)
        self.load_int['HVAC-in watts']=0
        
        #self.temperature=pd.DataFrame(index=np.arange(len(time_periods)))
        
        #self.temperature=self.temperature.set_index(time_periods)
        #self.temperature['°C']=0
        
    def simulate_temperature(self,outside_temp,set_temp,deadband):
        #deadbandwidth adjustment!!!!
        pred=[None]*(self.nrow-1)
        tmp=self.inside_temp
        for i in range(len(pred)):
            
            term1=self.gamma1*(outside_temp[i]-tmp)
            
            #coef=0 no hvac coef 1 heating coef=-1 cooling
            coef=0
            if set_temp[i]==None:
                coef=0
            #elif set_temp[i]>=outside_temp[i] and tmp < set_temp[i] :
            #    coef=1
            #elif set_temp[i]<outside_temp[i] and tmp > set_temp[i] :
            #    coef=-1  
            elif self.heating_season==1 and tmp < set_temp[i] - deadband :
                coef=1
            elif self.heating_season==-1 and tmp > set_temp[i] + deadband :
                coef=-1
                self.power_heater=2000*(60*self.time_r)  
            term2=coef*self.gamma2*(self.heater_efficiency*self.power_heater)
            self.load_int.iloc[i,0]=abs(coef)*((self.power_heater)/(60*self.time_r)/1000.0+0*abs(set_temp[i]-tmp)*100)
            
            term3=self.gamma3*self.solar_irradiation
            
            pred[i]=tmp+term1+term2+term3
            
            tmp=pred[i]
        
        
        tmp_index=self.load_int.index[1:self.nrow]
        self.temp_pred=pd.DataFrame(pred)
        self.temp_pred=self.temp_pred.set_index(tmp_index)
        

    def shift_time(self):
        new_index=np.roll(self.load_int.index,-1)
        self.load_int=self.load_int.set_index(new_index)
        self.load_int['HVAC-in watts']=0
        self.inside_temp=self.temp_pred.iloc[0,0]+np.random.normal(0,0.1,1)
        
        
        
        
#her shift yaptigiginda outside temperature prediction i degistir.
#inside temperature i guncelle.
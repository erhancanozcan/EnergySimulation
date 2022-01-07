#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 10:25:14 2021

@author: can
"""

import numpy as np
import pandas as pd
import datetime
import math

"""
class abc():
    def __init__(self):
        print(self.a)
        
    @property
    def a(self):
        return 1
"""
class ev:
    
    def __init__(self, car_type,time_resolution):
        self.car_type=car_type
        self.time_r=time_resolution
        self.period_from_next_day=0
        
        if self.car_type==1:
            #nominal power indicates the instanteneous electric consumption
            #during charging.
            #battery capacity indicates the max_charge capacity.
            self.nominal_power=1.5
            self.battery_capacity=19
        if time_resolution>=60:
            raise Exception("Time resolution cannot be greater than or equal to 60.")
        last="23:"+str(60-time_resolution)
        f=str(time_resolution)+"min"
        time_periods=pd.date_range("00:00", last, freq=f).strftime('%H:%M')
        
        self.load_int=pd.DataFrame(index=np.arange(len(time_periods)))
        self.nrow=len(time_periods)
        
        self.load_int=self.load_int.set_index(time_periods)
        self.load_int['EV']=0
        
        #self.time_periods=pd.date_range("00:00", last, freq=f).strftime('%H:%M')
        
        #self.load_int=np.zeros(len(self.time_periods))
        
        #self.load_int=pd.DataFrame(self.load_int)
        
        #self.load_int=self.load_int.set_index(self.time_periods)
        
    def charge_battery(self,start_time,charged_level,desired_level,amp=None):
        
        if amp==None:
            self.nominal_power=1.5
        elif amp!=None:
            self.nominal_power=amp*0.24
        if desired_level>1.0:
            raise Exception("Desired charge level cannot be larger than 1.0")
        if charged_level>desired_level:
            raise Exception("Current Charged Level cannot be larger than desired charge level")
        
        time_periods=self.load_int.index
        tmp=np.where(start_time>=time_periods)[0]
        s_index=tmp[len(tmp)-1]
        adjusted_start_time=time_periods[s_index]
        #print(adjusted_start_time)
        
        
        required_power=(desired_level-charged_level)*self.battery_capacity
        required_minutes_to_charge=(required_power*60)/self.nominal_power
        how_many_step=int(math.ceil(required_minutes_to_charge/self.time_r))
        
        f_index=s_index+how_many_step
        
        if f_index>self.nrow:
            if(self.period_from_next_day>0):
                print("There already exists a task which is planned to be completed in next day.")
            self.period_from_next_day=f_index-self.nrow
            print("We reached the end of the day. It will be charged until new day.")
            f_index=self.nrow
        
        #print(self.load_int.iloc[s_index:f_index,0])
        tmp_cntrl=np.array(self.load_int.iloc[s_index:f_index,0])
        #if self.load_int[s_index:f_index].any()!=0:
        if tmp_cntrl.any()!=0:
            print("EV is already scheduled to charge in this period. Possible error in scheduling the charge.")
        self.load_int.iloc[s_index:f_index,0]=np.random.normal(0,0.05,f_index-s_index)+self.nominal_power
    
        
    def shift_time(self):
        tmp_ind=np.arange(1, self.nrow)
        tmp_ind=np. append(tmp_ind, 0)
        self.load_int = self.load_int.iloc[tmp_ind]
        self.load_int.iloc[self.nrow-1,0]=0
        if self.period_from_next_day>0:
            print("Remaining {} jobs from previos day ".format(self.period_from_next_day))
            self.load_int.iloc[self.nrow-1,0]=np.random.normal(0,0.05,1)+self.nominal_power
            self.period_from_next_day=self.period_from_next_day-1
            
    
    #def report_load_curve(self):
     #   self.load_int=pd.DataFrame(self.load_int)
      #  self.load_int=self.load_int.set_index(self.time_periods)
        
        
            
            
            
        
        
        
        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 18:11:02 2021

@author: can
"""

import numpy as np
import pandas as pd
import datetime
import math

class other_appliances:
    def __init__(self,time_resolution):
        self.time_r=time_resolution
        self.period_from_next_day=0
        
        if time_resolution>=60:
            raise Exception("Time resolution cannot be greater than or equal to 60.")
            
            
        last="23:"+str(60-time_resolution)
        f=str(time_resolution)+"min"
        time_periods=pd.date_range("00:00", last, freq=f).strftime('%H:%M')
        
        self.load_int=pd.DataFrame(index=np.arange(len(time_periods)))
        self.nrow=len(time_periods)
        
        self.load_int=self.load_int.set_index(time_periods)
        self.load_int['Energy']=0
        

    def schedule(self,start_time):
        time_periods=self.load_int.index
        tmp=np.where(start_time>=time_periods)[0]
        s_index=tmp[len(tmp)-1]
        adjusted_start_time=time_periods[s_index]
        #print(adjusted_start_time)
        
        how_many_step=int(math.ceil(self.duration/self.time_r))
        
        f_index=s_index+how_many_step
        if f_index>self.nrow:
            if(self.period_from_next_day>0):
                print("There already exists a task which is planned to be completed in next day.")
            self.period_from_next_day=f_index-self.nrow
            print("We reached the end of the day. It will be used until new day.")
            f_index=self.nrow
            
        #print(self.load_int.iloc[s_index:f_index,0])
        tmp_cntrl=np.array(self.load_int.iloc[s_index:f_index,0])
        #if self.load_int[s_index:f_index].any()!=0:
        if tmp_cntrl.any()!=0:
            print("Appliance is already scheduled to charge in this period. Possible error in scheduling.")
        #self.load_int.iloc[s_index:f_index,0]=np.random.normal(0,0.05,f_index-s_index)+self.nominal_power
        self.load_int.iloc[s_index:f_index,0]=self.nominal_power
        
    def shift_time(self):
        tmp_ind=np.arange(1, self.nrow)
        tmp_ind=np. append(tmp_ind, 0)
        self.load_int = self.load_int.iloc[tmp_ind]
        self.load_int.iloc[self.nrow-1,0]=0
        if self.period_from_next_day>0:
            print("Remaining {} jobs from previos day ".format(self.period_from_next_day))
            self.load_int.iloc[self.nrow-1,0]=self.nominal_power
            self.period_from_next_day=self.period_from_next_day-1
 
class washing_machine(other_appliances):
    def __init__(self, time_resolution):
        #A normal 7 kg washing machine requires maximum power of 2000 watt – 2500 watt
        self.nominal_power = 2
        self.duration=90
        other_appliances.__init__(self, time_resolution)
        
class dryer(other_appliances):
    def __init__(self, time_resolution):
        #Dryers are typically somewhere in the range of 2,000 to 6,000 watts
        self.nominal_power = 4
        self.duration=120
        other_appliances.__init__(self, time_resolution)
        
class oven(other_appliances):
    def __init__(self, time_resolution):
        #Most electric ovens draw between 2,000 and 5,000 watts
        self.nominal_power = 3.5
        self.duration=60
        other_appliances.__init__(self, time_resolution)
        
class refrigerator(other_appliances):
    def __init__(self, time_resolution):
        #Domestic fridge power consumption is typically between 100 and 250 watts
        self.nominal_power = 0.2
        other_appliances.__init__(self, time_resolution)
        self.load_int['Energy']=self.nominal_power
        
        
    def shift_time_ref(self):
        tmp_ind=np.arange(1, self.nrow)
        tmp_ind=np. append(tmp_ind, 0)
        self.load_int = self.load_int.iloc[tmp_ind]
        self.load_int.iloc[self.nrow-1,0]=self.nominal_power
        
        

        
        

    


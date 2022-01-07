#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 17:52:17 2021

@author: can
"""

from pvlib.pvsystem import PVSystem, retrieve_sam
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.tracking import SingleAxisTracker
from pvlib.modelchain import ModelChain
from pvlib.forecast import GFS

import numpy as np
import pandas as pd
from datetime import datetime
import math
import os

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


class PV:
    #we assume no heat loss from the tank.
    """https://www.quora.com/How-many-kWh-will-1-sq-meter-of-solar-panel-produce-in-1-year"""
    def __init__(self, m_square,time_resolution,new_fx_data,eff):
        #size of one typical pv is 1.6m2.
        self.s_ind=0
        self.eff=eff
        self.m_square=m_square
        self.time_r=time_resolution
        ##data is given 5 mins intervals. We consider only first 30days.
        #if you change this variable, you need to adjust update_time_periods variable.
        self.how_many_days=30
        self.how_many_steps=int((60/5)*24*self.how_many_days)


        if time_resolution>=60 or time_resolution%5!=0:
            raise Exception("Either time resolutionis greater than 60 or time res is not multiple of 5.")

        
        latitude, longitude, tz = 40.7, -74.0, 'America/New_York'
        
        start = pd.Timestamp(datetime.now(), tz=tz)
        
        end = start + pd.Timedelta(hours=24)
        
        irrad_vars = ['ghi', 'dni', 'dhi']
        
        
        sandia_modules = retrieve_sam('sandiamod')

        cec_inverters = retrieve_sam('cecinverter')

        module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']

        inverter = cec_inverters['SMA_America__SC630CP_US__with_ABB_EcoDry_Ultra_transformer_']

        temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

        # model a big tracker for more fun
        system = SingleAxisTracker(module_parameters=module, inverter_parameters=inverter, temperature_model_parameters=temperature_model_parameters, modules_per_string=15, strings_per_inverter=300)



        fx_model = GFS()

        fx_data = fx_model.get_processed_data(latitude, longitude, start, end)
        
        
        #os.chdir('/Users/can/Desktop/energy/code/solar_data/boston')
        #sys.path.insert(0, '/Users/can/Desktop/energy/code/solar_data/boston/')
        #new_fx_data=pd.read_csv('2784951_42.38_-71.13_2018.csv')  
        #new_fx_data=new_fx_data.iloc[:,[5,6,7]]

        #new_fx_data.columns=np.char.lower(new_fx_data.iloc[1,:].values.astype('<U5'))
        #new_fx_data=new_fx_data.drop([0,1])
        #new_fx_data['ghi'] = new_fx_data['ghi'].astype(float)
        #new_fx_data['dhi'] = new_fx_data['dhi'].astype(float)
        #new_fx_data['dni'] = new_fx_data['dni'].astype(float)
        new_fx_data=new_fx_data.iloc[:self.how_many_steps,]


        #update_time_periods=pd.date_range("2018-01-01", "2018-01-31", freq="5min")
        #update_time_periods=update_time_periods[:self.how_many_steps]
        #new_fx_data.index=update_time_periods
        # use a ModelChain object to calculate modeling intermediates
        mc = ModelChain(system, fx_model.location)
        
        mc.run_model(new_fx_data)
        
        adjust_time_resolution=int(self.time_r/5)
        #print(adjust_time_resolution)
        time_tmp=np.arange(0,self.how_many_steps,adjust_time_resolution)
        
        self.irradiation_per_msq=mc.results.total_irrad['poa_global']*self.m_square*self.eff
        self.irradiation_per_msq.index=self.irradiation_per_msq.index.strftime('%H:%M')
        self.irradiation_per_msq=self.irradiation_per_msq.iloc[time_tmp,]
        
        self.nrow=int(24*60/self.time_r)
        self.report=self.irradiation_per_msq.iloc[self.s_ind:(self.s_ind+self.nrow),]/1000
        print(round(sum(self.report*self.time_r*60)/3600/1000,5), "KWh energy will be produced in total in next 24 hours")
        
    def shift_time(self):
        self.s_ind+=1
        self.report=self.irradiation_per_msq.iloc[self.s_ind:(self.s_ind+self.nrow),]/1000
        print(round(sum(self.report*self.time_r*60)/3600/1000,5), "KWh energy will be produced in total in next 24 hours")
        

        


        
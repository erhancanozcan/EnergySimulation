#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 21:11:39 2022

@author: can
"""
import numpy as np
import pandas as pd
from EnergySimulation.ewh import SimpleWaterHeater
from EnergySimulation.ev import ev
from EnergySimulation.other_appliances import refrigerator
from EnergySimulation.other_appliances import washing_machine,dryer,oven
from EnergySimulation.HVAC import Heating
from EnergySimulation.pv import PV
import matplotlib.pyplot as plt
from datetime import datetime

class Home:
    def __init__(self,outside_temp,house_type,heating_season,dt_obj,wh_type=1,ev_type=1,heater_type=1,solar_panel_area=10,inside_tmp=22.0,tap_water_temp=4,time_resolution=15):
        
        np.random.seed(abs(int(outside_temp[0])))
        self.outside_temp=outside_temp
        self.house_type=house_type
        self.dt_obj=dt_obj
        
        if house_type["insulation"] =="low":
            gamma1=np.random.normal(0.15,0.001)
        elif house_type["insulation"] =="high":
            gamma1=np.random.normal(0.10,0.001)
        if house_type["size"] =="small":
            gamma2=np.random.normal(0.0000020,0.0000001)
        elif house_type["size"] =="large":
            gamma2=np.random.normal(0.0000020,0.0000001)
        
        
        
        self.wh_type=wh_type
        self.ev_type=ev_type
        self.heater_type=heater_type
        self.solar_panel_area=solar_panel_area
        self.time_resolution=time_resolution
        self.inside_tmp=inside_tmp
        self.tap_water_temp=tap_water_temp

        
        
        
        
        self.ewh=SimpleWaterHeater(wh_type,time_resolution)
        self.ev=ev(ev_type,time_resolution)
        self.refrigerator=refrigerator(time_resolution)
        self.washing_machine=washing_machine(time_resolution)
        self.dryer=dryer(time_resolution)
        self.oven=oven(time_resolution)
        
        
        
        
        self.HVAC=Heating(gamma1,gamma2,3,inside_tmp,time_resolution,heater_type,heating_season)
        #self.HVAC=Heating(0.10,0.0000022,3,inside_tmp,time_resolution,heater_type)
        
        
        solar_irradiation_data=pd.read_csv('EnergySimulation/data/2784951_42.38_-71.13_2018.csv')
        
        solar_irradiation_data=solar_irradiation_data.iloc[:,[5,6,7]]

        solar_irradiation_data.columns=np.char.lower(solar_irradiation_data.iloc[1,:].values.astype('<U5'))
        solar_irradiation_data=solar_irradiation_data.drop([0,1])
        solar_irradiation_data['ghi'] = solar_irradiation_data['ghi'].astype(float)
        solar_irradiation_data['dhi'] = solar_irradiation_data['dhi'].astype(float)
        solar_irradiation_data['dni'] = solar_irradiation_data['dni'].astype(float)
        
        
        update_time_periods=pd.date_range("2018-01-01", "2019-01-01", freq="5min")
        update_time_periods=update_time_periods[:len(update_time_periods)-1]
        solar_irradiation_data.index=update_time_periods
        
        #dt_obj = "07/15/2018"
        dt_obj=datetime.strptime(dt_obj, '%m/%d/%Y')
        start_index=np.where(dt_obj.date()==solar_irradiation_data.index.date)[0][0]
        #solar_irradiation_data=solar_irradiation_data.iloc[start_index:,:].values
        solar_irradiation_data=solar_irradiation_data.iloc[start_index:,:]


        #this part create randomness for each house in solar data
        zeros=(solar_irradiation_data==0)
        tmp=np.random.normal(0,20,solar_irradiation_data.shape)
        tmp[zeros]=0
        solar_irradiation_data=solar_irradiation_data+tmp
        solar_irradiation_data=abs(solar_irradiation_data)
        #solar_irradiation_data[solar_irradiation_data<0]=0
        ###end of randomdness in solar.
        
        self.PV=PV(solar_panel_area,15,solar_irradiation_data,eff=0.2)
        
        self.current_time=self.ewh.load_int.index[0]
        
    def get_orders(self,order_ewh,order_ev,order_wm,order_dryer,order_oven,order_HVAC):
        self.order_ewh=order_ewh
        self.order_ev=order_ev
        self.order_wm=order_wm
        self.order_dryer=order_dryer
        self.order_oven=order_oven
        self.order_HVAC=order_HVAC
        
        #you must get HVAC order at every iteration!!!
        self.HVAC.simulate_temperature(self.outside_temp, order_HVAC["set_temperature"])
        
        
        if order_ewh['order_status'] == 1:
            self.ewh.heat_water(order_ewh['starting_time'], order_ewh['water_amount'],self.tap_water_temp,order_ewh['desired_temp'])
        if order_ev['order_status'] == 1:
            self.ev.charge_battery(order_ev['starting_time'], order_ev['battery_level'], order_ev['desired_level'],amp=order_ev['amps'])
        if order_wm['order_status'] == 1:    
            self.washing_machine.schedule(order_wm['starting_time'])
        if order_dryer['order_status'] == 1:    
            self.dryer.schedule(order_dryer['starting_time'])
        if order_oven['order_status'] == 1:    
            self.oven.schedule(order_oven['starting_time'])
            

    
    def shift(self,outside_temp):
        self.outside_temp=outside_temp
        
        
        self.ewh.shift_time()
        self.ev.shift_time()
        self.refrigerator.shift_time_ref()
        self.washing_machine.shift_time()
        self.dryer.shift_time()
        self.oven.shift_time()
        self.HVAC.shift_time()
        self.PV.shift_time()
        
        self.current_time=self.ewh.load_int.index[0]
            
    
    def plot_load(self,appliance):
        
        if appliance == "ewh":
            ax_ev=self.ewh.load_int.plot(ylim=(0,3))
            ax_ev.set(xlabel='Time', ylabel='KWatt')
            ax_ev.set_title("Load Curve")
            ax_ev.legend(["EWH"],fontsize=20)
            plt.show()
        elif appliance=="ev":
            ax_ev=self.ev.load_int.plot(ylim=(0,3))
            ax_ev.set(xlabel='Time', ylabel='KWatt')
            ax_ev.set_title("Load Curve")
            ax_ev.legend(["EV"],fontsize=20)
            plt.show()
        elif appliance=="wm":
            ax_ev=self.washing_machine.load_int.plot()
            ax_ev.set(xlabel='Time', ylabel='KWatt')
            ax_ev.set_title("Load Curve")
            ax_ev.legend(["WM"],fontsize=20)
            plt.show()
        elif appliance=="refrigerator":
            ax_ev=self.refrigerator.load_int.plot()
            ax_ev.set(xlabel='Time', ylabel='KWatt')
            ax_ev.set_title("Load Curve")
            ax_ev.legend(["Refrigerator"],fontsize=20)
            plt.show()
        elif appliance=="dryer":
            ax_ev=self.dryer.load_int.plot()
            ax_ev.set(xlabel='Time', ylabel='KWatt')
            ax_ev.set_title("Load Curve")
            ax_ev.legend(["Dryer"],fontsize=20)
            plt.show()
        elif appliance=="oven":
            ax_ev=self.oven.load_int.plot()
            ax_ev.set(xlabel='Time', ylabel='KWatt')
            ax_ev.set_title("Load Curve")
            ax_ev.legend(["Oven"],fontsize=20)
            plt.show()
        elif appliance == "HVAC":
            ax_load=(self.HVAC.load_int).plot()
            ax_load.set(xlabel='Time', ylabel='KWatt')
            ax_load.set_title("Load Curve")
            ax_load.legend(["HVAC"],fontsize=20)
            plt.show()
            
            
            ax_temperature=self.HVAC.temp_pred.plot()
            ax_temperature.plot(self.HVAC.temp_pred.index,self.outside_temp[1:96])
            ax_temperature.plot(self.HVAC.temp_pred.index,self.order_HVAC["set_temperature"][1:96])
            ax_temperature.set(xlabel='Time', ylabel='°C')
            ax_temperature.set_title("Temperature Curve")
            ax_temperature.legend(["Inside","Outside","Thermostat Set"],fontsize=15)
            plt.show()
        elif appliance == "pv":
            ax_pv=self.PV.report.plot()
            ax_pv.set(xlabel='Time', ylabel='Generated KW')
            ax_pv.set_title("Load Curve")
            ax_pv.legend(["PV"],fontsize=20)
        elif appliance == "all":
            energy=self.ewh.load_int['EV']+\
            self.ev.load_int['EV']+\
            self.refrigerator.load_int['Energy']+\
            self.washing_machine.load_int['Energy']+\
            self.dryer.load_int['Energy']+\
            self.oven.load_int['Energy']+\
            self.HVAC.load_int['HVAC-in watts']
            energy.index=self.HVAC.load_int.index
            
            ax_pv=energy.plot()
            ax_pv.set(xlabel='Time', ylabel='KW')
            ax_pv.set_title("Daily Load Curve")
            ax_pv.legend(["Load"])    
        else:
            raise Exception(appliance, "not implemented")
            
    def check_activity_status(self):
        ewh_activity=-1
        ev_activity=-1
        wm_activity=-1
        dryer_activity=-1
        oven_activity=-1
        HVAC_activity=-1
        ref_activity=-1
        
        if self.ewh.load_int.iloc[0,0]>0:
            ewh_activity=1
        else:
            ewh_activity=0
        if self.ev.load_int.iloc[0,0]>0:
            ev_activity=1
        else:
            ev_activity=0
        if self.washing_machine.load_int.iloc[0,0]>0:
            wm_activity=1
        else:
            wm_activity=0
        if self.dryer.load_int.iloc[0,0]>0:
            dryer_activity=1
        else:
            dryer_activity=0            
        if self.oven.load_int.iloc[0,0]>0:
            oven_activity=1
        else:
            oven_activity=0
        if self.HVAC.load_int.iloc[0,0]>0:
            HVAC_activity=1
        else:
            HVAC_activity=0
        if self.refrigerator.load_int.iloc[0,0]>0:
            ref_activity=1
        else:
            ref_activity=0
            
        status={"EWH":ewh_activity,"EV":ev_activity,"WM":wm_activity,
                "Dryer":dryer_activity,"Oven":oven_activity,"HVAC":HVAC_activity,
                "Refrigerator":ref_activity}
        print(status)
        
        
        
            
        
        
            
            
            
            
            
            
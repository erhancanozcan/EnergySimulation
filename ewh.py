import numpy as np
import pandas as pd
import datetime
import math

class SimpleWaterHeater:
    #we assume no heat loss from the tank.
    def __init__(self, ewh_type,time_resolution):
        self.ewh_type=ewh_type
        self.time_r=time_resolution
        self.period_from_next_day=0
        self.water_heat_capacity=4186#J/(KG*°C)
        
        if self.ewh_type==1:
            #nominal power indicates the instanteneous electric consumption
            #during charging.
            #battery capacity indicates the max_charge capacity.
            self.nominal_power=1000#watt= Volt(250)*Current(4)*pure_resistance_coef(1)
            self.capacity=300#kg
        if time_resolution>=60:
            raise Exception("Time resolution cannot be greater than or equal to 60.")
        last="23:"+str(60-time_resolution)
        f=str(time_resolution)+"min"
        time_periods=pd.date_range("00:00", last, freq=f).strftime('%H:%M')
        
        self.load_int=pd.DataFrame(index=np.arange(len(time_periods)))
        self.nrow=len(time_periods)
        
        self.load_int=self.load_int.set_index(time_periods)
        self.load_int['EV']=0
        

    def heat_water(self,start_time,water_amount,tap_water_temp,desired_temp):
        if water_amount>self.capacity:
            print("Consumed water amount is greater than capacity. Variable water amount is set back to capacity")
            water_amount=self.capacity
        if tap_water_temp>desired_temp:
            raise Exception("Tap water Temperature cannot be larger than desired temperature")
        
        time_periods=self.load_int.index
        tmp=np.where(start_time>=time_periods)[0]
        s_index=tmp[len(tmp)-1]
        adjusted_start_time=time_periods[s_index]
        #print(adjusted_start_time)
        
        
        #Note that temperatures are in terms of Celcius
        #required energy is calculated in terms of joule.
        required_energy=water_amount*self.water_heat_capacity*(desired_temp-tap_water_temp)
        required_minutes_to_charge=required_energy/(self.nominal_power*60)
        how_many_step=int(math.ceil(required_minutes_to_charge/self.time_r))
        
        f_index=s_index+how_many_step
        
        if f_index>self.nrow:
            if(self.period_from_next_day>0):
                print("There already exists a task which is planned to be completed in next day.")
            self.period_from_next_day=f_index-self.nrow
            print("We reached the end of the day. It will be heated until new day.")
            f_index=self.nrow
        
        #print(self.load_int.iloc[s_index:f_index,0])
        tmp_cntrl=np.array(self.load_int.iloc[s_index:f_index,0])
        #if self.load_int[s_index:f_index].any()!=0:
        if tmp_cntrl.any()!=0:
            print("EWH is already scheduled in this period. Possible error in scheduling the charge.")
        self.load_int.iloc[s_index:f_index,0]=np.random.normal(0,0.05,f_index-s_index)+(self.nominal_power/1000)
        #nominal power is divided by 1000 to convert it into kw
    def shift_time(self):
        tmp_ind=np.arange(1, self.nrow)
        tmp_ind=np. append(tmp_ind, 0)
        self.load_int = self.load_int.iloc[tmp_ind]
        self.load_int.iloc[self.nrow-1,0]=0
        if self.period_from_next_day>0:
            print("Remaining {} jobs from previos day ".format(self.period_from_next_day))
            self.load_int.iloc[self.nrow-1,0]=np.random.normal(0,0.05,1)+(self.nominal_power/1000)
            self.period_from_next_day=self.period_from_next_day-1
            #nominal power is divided by 1000 to convert it into kw
         



"""https://github.com/jmaguire1/WaterHeaterPythonModel/blob/master/basic_water_heater.py"""

import math

class BasicWaterHeater(object):
    """ An instance of a simple water heater from gridlabd"""
    RHOWATER = 62.4
    GALPCF = 7.4805195
    BTUPHPKW = 1e3 * 3.4120

    def __init__(self, tank_setpoint=132,
                       thermostat_deadband=10,
                       heating_element_capacity=4.5,
                       tank_volume=50,
                       tank_ua=3.7,
                       current_temperature=128,
                       nominal_voltage=240,
                       inlet_temp=60):

        self.heat_needed = 0
        self.heating_element_capacity = heating_element_capacity
        self.tank_setpoint = tank_setpoint
        self.thermostat_deadband = thermostat_deadband
        self.tank_ua = tank_ua#heat loss coefficienct
        self.tank_volume = tank_volume
        self.inlet_temp = inlet_temp
        self.cp = 1
        self.cw = tank_volume/BasicWaterHeater.GALPCF * BasicWaterHeater.RHOWATER * self.cp;
        self.current_temperature = current_temperature
        self.nominal_voltage = nominal_voltage


    def execute(self, delta_t=None,
                      actual_voltage=None,
                      water_demand=None,
                      ambient_temp=None,
                      tank_setpoint=None,
                      ):

        """ Calculate next temperature and load"""
        self.tank_setpoint = tank_setpoint

        # print(self.tank_setpoint)

        mdot_Cp = self.cp * water_demand * 60 * BasicWaterHeater.RHOWATER / BasicWaterHeater.GALPCF

        c1 = (self.tank_ua + mdot_Cp) / self.cw

        actual_kW = (self.heat_needed*self.heating_element_capacity *
                     (actual_voltage*actual_voltage) /
                     (self.nominal_voltage*self.nominal_voltage))

        c2 = (actual_kW*BasicWaterHeater.BTUPHPKW +
              mdot_Cp*self.inlet_temp +
              self.tank_ua*ambient_temp)/(self.tank_ua + mdot_Cp)

        new_temp = c2 - (c2 - self.current_temperature) * math.exp(-c1 * delta_t )

        #internal_gain = self.tank_ua * (new_temp - ambient_temp);

        Tlower  = self.tank_setpoint - self.thermostat_deadband/2.0;
        Tupper = self.tank_setpoint + self.thermostat_deadband/2.0;

        if( new_temp <= Tlower + 0.02):
            self.heat_needed = 1
        elif( new_temp >= Tupper - 0.02):
            self.heat_needed = 0

        self.current_temperature = new_temp
        return {'temperature': new_temp,
                'load': actual_kW}
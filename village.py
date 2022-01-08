#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 22:02:51 2022

@author: can
"""



import numpy as np
import pandas as pd
from datetime import datetime
import math
import os
import matplotlib.pyplot as plt


def village_plot(village,app_type,num_houses):

    if app_type=="ewh":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].ewh.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].ewh.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["EWH"],fontsize=20)
        plt.show()
        
    elif app_type=="ev":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].ev.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].ev.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["EV"],fontsize=20)
        plt.show()
    elif app_type=="wm":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].washing_machine.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].washing_machine.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["WM"],fontsize=20)
        plt.show()
    elif app_type=="refrigerator":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].refrigerator.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].refrigerator.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["WM"],fontsize=20)
        plt.show()
    elif app_type=="dryer":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].dryer.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].dryer.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["WM"],fontsize=20)
        plt.show()
    elif app_type=="oven":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].oven.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].oven.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["WM"],fontsize=20)
        plt.show()
        
    elif app_type=="HVAC":
        
        tmp=np.zeros(96)
        #tmp=village[0].ewh.load_int
        #tmp.iloc[:,0]=0
        i=0
        
        for i in range(num_houses):
            tmp=tmp+village[i].HVAC.load_int.values[:,0]
        
        tmp=pd.DataFrame(tmp)
        tmp.index=village[0].HVAC.load_int.index
        ax_ev=tmp.plot()
        ax_ev.set(xlabel='Time', ylabel='KWatt')
        ax_ev.set_title("Load Curve")
        ax_ev.legend(["EWH"],fontsize=20)
        plt.show()

 
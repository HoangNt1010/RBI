import os,sys
import sys
from cloud import models
import time
import math
from builtins import property
from datetime import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
from pathlib import _Selector

from cloud.process.RBI import Postgresql as DAL_CAL

class corrosion_with_internalcladding:
    def __init__(self,InternalCladding,NomalThick,CladdingThickness,CladdingCorrosionRate,CurrentThick,
                 ComponentNumber = "",APIComponentType="",AssesmentDate = datetime.now(),Commissiondate = datetime.now()):
        self.InternalCladding = InternalCladding
        self.NomalThick = NomalThick
        self.CladdingThickness = CladdingThickness
        self.CladdingCorrosionRate = CladdingCorrosionRate
        self.CurrentThick = CurrentThick
        self.ComponentNumber = ComponentNumber
        self.APIComponentType = APIComponentType
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate

    def GET_AGE(self):
        try:
            age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber,"Internal Lining Degradation",self.Commissiondate, self.AssesmentDate)
            print("1",self.Commissiondate)
            print("2",self.AssesmentDate)
            print("age",age)
            return age
        except Exception as e:
            print("error in getage")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    def trdi(self):
        return self.CurrentThick

    def agerc(self, age):
        try:
            print(self.InternalCladding)
            a = age - self.GET_AGE()
            if self.InternalCladding:
                print(a)
                # print("cuong",((self.trdi() - (self.NomalThick - self.CladdingThickness)) / self.CladdingCorrosionRate - a))
                return max(((self.trdi() - (self.NomalThick - self.CladdingThickness)) / self.CladdingCorrosionRate - a), 0)
            else:
                return max(((self.trdi() - self.NomalThick) / self.CladdingCorrosionRate - a), 0)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return 0

# class corrosion_rate_for_tank:

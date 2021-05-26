import time
import time
import math
import traceback#dung cho tinh toan noi suy
import sys#dung cho tinh toan noi suy
from builtins import property
from datetime import datetime
import  numpy as np
from dateutil.relativedelta import relativedelta
from pathlib import _Selector
#from rbi import MYSQL_CAL as DAL_CAL
# from pyglet.input.carbon_hid import Self

from cloud.process.RBI import Postgresql as DAL_CAL
from django.core.mail import EmailMessage
from cloud import models

class Df_Thin:
    def __init__(self,Diametter ,NomalThick ,CurrentThick,MinThickReq,CorrosionRate,CA,ProtectedBarrier,CladdingThickness,CladdingCorrosionRate,InternalCladding,
                 NoINSP_THINNING,EFF_THIN,OnlineMonitoring,HighlyEffectDeadleg,ContainsDeadlegs,TankMaintain653,AdjustmentSettle,ComponentIsWeld,
                 WeldJointEffciency,AllowableStress,TensileStrengthDesignTemp,YieldStrengthDesignTemp,StructuralThickness,MINIUM_STRUCTURAL_THICKNESS_GOVERS,
                 Pressure,ShapeFactor,CR_Confidents_Level,EquipmentType,AssesmentDate = datetime.now(),Commissiondate = datetime.now(),ComponentNumber = "",APIComponentType=""):
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
        self.APIComponentType = APIComponentType

        self.Diametter = Diametter
        self.NomalThick = NomalThick
        self.CurrentThick = CurrentThick
        self.MinThickReq = MinThickReq
        self.CorrosionRate = CorrosionRate
        self.CA = CA
        self.ProtectedBarrier = ProtectedBarrier
        self.CladdingThickness = CladdingThickness
        self.CladdingCorrosionRate = CladdingCorrosionRate
        self.InternalCladding = InternalCladding
        self.NoINSP_THINNING = NoINSP_THINNING
        self.EFF_THIN = EFF_THIN
        self.OnlineMonitoring = OnlineMonitoring
        self.HighlyEffectDeadleg = HighlyEffectDeadleg
        self.ContainsDeadlegs = ContainsDeadlegs
        self.TankMaintain653 = TankMaintain653
        self.AdjustmentSettle = AdjustmentSettle
        self.ComponentIsWeld = ComponentIsWeld
        self.WeldJointEffciency = WeldJointEffciency
        self.AllowableStress = AllowableStress
        self.TensileStrengthDesignTemp = TensileStrengthDesignTemp
        self.YieldStrengthDesignTemp = YieldStrengthDesignTemp
        self.StructuralThickness = StructuralThickness
        self.MINIUM_STRUCTURAL_THICKNESS_GOVERS = MINIUM_STRUCTURAL_THICKNESS_GOVERS
        self.Pressure = Pressure
        self.ShapeFactor = ShapeFactor
        self.CR_Confidents_Level = CR_Confidents_Level
        self.EquipmentType = EquipmentType
    def getTmin(self):
        if self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType =="TANKROOFFLOAT0":
            if (self.ProtectedBarrier):
                #t = 2.54
                t=0.05
            else:
                #t = 1.27
                t=0.1
        else:
            t = self.MinThickReq
        return t

    DM_Name = ["Internal Thinning", "Internal Lining Degradation", "Caustic Stress Corrosion Cracking",
               "Amine Stress Corrosion Cracking", "Sulphide Stress Corrosion Cracking (H2S)", "HIC/SOHIC-H2S",
               "Carbonate Stress Corrosion Cracking", "Polythionic Acid Stress Corrosion Cracking",
               "Chloride Stress Corrosion Cracking", "Hydrogen Stress Cracking (HF)", "HF Produced HIC/SOHIC",
               "External Corrosion", "Corrosion Under Insulation", "External Chloride Stress Corrosion Cracking",
               "Chloride Stress Corrosion Cracking Under Insulation", "High Temperature Hydrogen Attack",
               "Brittle Fracture", "Temper Embrittlement", "885F Embrittlement", "Sigma Phase Embrittlement",
               "Vibration-Induced Mechanical Fatigue"]
    def agetk(self,age):
        return age
    def trdi(self):
        return self.CurrentThick

    def agerc(self, age):
        try:
            a = age - self.GET_AGE()
            if self.InternalCladding:
                return max(((self.trdi() - (self.NomalThick - self.CladdingThickness)) / self.CladdingCorrosionRate - a), 0)
            else:
                return max(((self.trdi() - self.NomalThick) / self.CladdingCorrosionRate - a), 0)
        except Exception as e:
            print(e)
            return 0
    def ArtWithoutCladdingMaterial(self,age):
        return (self.CorrosionRate * self.agetk(age) / self.trdi())
    def ArtWithCladdingMaterial1(self,age):
        return (self.CladdingCorrosionRate * self.agetk(age) / self.trdi())
    def ArtWithCladdingMaterial2(self, age):
        a = (self.CladdingCorrosionRate * self.agerc(age) + self.CorrosionRate * (self.agetk(age) - self.agerc(age))) / self.trdi()
        return (self.CladdingCorrosionRate * self.agerc(age) + self.CorrosionRate * ( self.agetk(age) - self.agerc(age))) / self.trdi()
    def Art(self,age):
        try:
            if self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType == "TANKROOFFLOAT0":
                # print("Art")
                # print(max((1-(self.trdi() - self.CorrosionRate * self.agetk(age)) / (self.getTmin() + self.CA)), 0.0))
                return max((1-(self.trdi() - self.CorrosionRate * self.agetk(age)) / (self.getTmin() + self.CA)), 0.0)
            elif (self.InternalCladding):
                if (self.agetk(age) < self.agerc(age)):
                    print(self.agerc(age))
                    return (self.CladdingCorrosionRate * self.agetk(age)/ self.trdi())
                else:
                    a =(self.CladdingCorrosionRate * self.agerc(age) + self.CorrosionRate * (self.agetk(age) - self.agerc(age))) / self.trdi()
                    return (self.CladdingCorrosionRate * self.agerc(age) + self.CorrosionRate * (self.agetk(age) - self.agerc(age))) / self.trdi()
            else:
                if self.trdi()==0:
                    return 1;
                else:
                    return (self.CorrosionRate * self.agetk(age) / self.trdi())
        except Exception as e:
            print(e)
            return 1
    def FS_Thin(self):


            return ((self.YieldStrengthDesignTemp + self.TensileStrengthDesignTemp)/2) * self.WeldJointEffciency * 1.1

    def getalpha(self):
        return self.ShapeFactor
    def strengthRationMin(self):
        try:
            if self.MINIUM_STRUCTURAL_THICKNESS_GOVERS==False:
                return (self.Pressure * self.Diametter) / (self.getalpha() * self.FS_Thin() * self.trdi())
            else:
                return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(),
                                                                             self.StructuralThickness)) / (
                       self.FS_Thin() * self.trdi())
        except Exception as e:
            return 'null'
    def strengthRatioInter(self):
        return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(), self.StructuralThickness)) / (self.FS_Thin() * self.trdi())
    def SRp_Thin(self):
        if self.MINIUM_STRUCTURAL_THICKNESS_GOVERS == False:
            return (self.Pressure * self.Diametter)/(self.getalpha() * self.FS_Thin() * self.trdi())
        else:
            # return (self.WeldJointEffciency * self.TensileStrengthDesignTemp * max(self.getTmin(),self.StructuralThickness))/(self.FS_Thin() * self.trdi())
            #return (self.WeldJointEffciency * self.TensileStrengthDesignTemp * max(self.getTmin(),self.StructuralThickness))/(self.FS_Thin() * self.YieldStrengthDesignTemp)
            return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(),self.StructuralThickness)) / (self.FS_Thin() * self.trdi())
    def Pr_P1_Thin(self):
        if self.CR_Confidents_Level == "Low":
            return 0.5
        elif self.CR_Confidents_Level == "Medium":
            return 0.7
        else:
            return 0.8
    def Pr_P2_Thin(self):
        if self.CR_Confidents_Level == "Low":
            return 0.3
        elif self.CR_Confidents_Level == "Medium":
            return 0.2
        else:
            return 0.15
    def Pr_P3_Thin(self):
        if self.CR_Confidents_Level == "Low":
            return 0.2
        elif self.CR_Confidents_Level == "Medium":
            return 0.1
        else:
            return  0.05

    def NA_Thin(self):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(self.ComponentNumber, self.DM_Name[0])
        return a
    def NB_Thin(self):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(self.ComponentNumber, self.DM_Name[0])
        return b
    def NC_Thin(self):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(self.ComponentNumber, self.DM_Name[0])
        return c
    def ND_Thin(self):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(self.ComponentNumber, self.DM_Name[0])
        return d

    def I1_Thin(self):
        a=self.Pr_P1_Thin() * pow(0.9,self.NA_Thin()) * pow(0.7,self.NB_Thin()) * pow(0.5,self.NC_Thin()) * pow(0.4,self.ND_Thin())
        return self.Pr_P1_Thin() * pow(0.9,self.NA_Thin()) * pow(0.7,self.NB_Thin()) * pow(0.5,self.NC_Thin()) * pow(0.4,self.ND_Thin())
    def I2_Thin(self):
        a=self.Pr_P2_Thin() * pow(0.09,self.NA_Thin()) * pow(0.2,self.NB_Thin()) * pow(0.3,self.NC_Thin()) * pow(0.33,self.ND_Thin())
        return self.Pr_P2_Thin() * pow(0.09,self.NA_Thin()) * pow(0.2,self.NB_Thin()) * pow(0.3,self.NC_Thin()) * pow(0.33,self.ND_Thin())
    def I3_Thin(self):
        a=self.Pr_P3_Thin() * pow(0.01,self.NA_Thin()) * pow(0.1,self.NB_Thin()) * pow(0.2,self.NC_Thin()) * pow(0.27,self.ND_Thin())
        return self.Pr_P3_Thin() * pow(0.01,self.NA_Thin()) * pow(0.1,self.NB_Thin()) * pow(0.2,self.NC_Thin()) * pow(0.27,self.ND_Thin())
    def Po_P1_Thin(self):
        a=self.I1_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
        return self.I1_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
    def Po_P2_Thin(self):
        a = self.I2_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
        return self.I2_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
    def Po_P3_Thin(self):
        return self.I3_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
    def B1_Thin(self,age):
        # print("check age",age,self.Art(age))
        return (1 - self.Art(age)- self.SRp_Thin())/math.sqrt(pow(self.Art(age), 2) * 0.04 + pow((1 - self.Art(age)), 2) * 0.04 + pow(self.SRp_Thin(), 2) * pow(0.05, 2))
    def B2_Thin(self,age):
        return (1- 2*self.Art(age)-self.SRp_Thin())/math.sqrt(pow(self.Art(age),2)*4*0.04 + pow(1-2*self.Art(age),2)*0.04+pow(self.SRp_Thin(),2)*pow(0.05,2))
    def B3_Thin(self,age):
        return (1- 4*self.Art(age)-self.SRp_Thin())/math.sqrt(pow(self.Art(age),2)*16*0.04 + pow(1-4*self.Art(age),2)*0.04+pow(self.SRp_Thin(),2)*pow(0.05,2))

    def API_ART(self, a):
        if self.APIComponentType == 'TANKBOTTOM0' or self.APIComponentType == 'TANKROOFFLOAT0':
            data = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
                    0.95, 1]
            if a < (data[0] + data[1]) / 2:
            #if 0.025 < a < (data[0] + data[1]) / 2:
                return data[0]
            elif (a < (data[1] + data[2]) / 2):
                return data[1]
            elif (a < (data[2] + data[3]) / 2):
                return data[2]
            elif (a < (data[3] + data[4]) / 2):
                return data[3]
            elif (a < (data[4] + data[5]) / 2):
                return data[4]
            elif (a < (data[5] + data[6]) / 2):
                return data[5]
            elif (a < (data[6] + data[7]) / 2):
                return data[6]
            elif (a < (data[7] + data[8]) / 2):
                return data[7]
            elif (a < (data[8] + data[9]) / 2):
                return data[8]
            elif (a < (data[9] + data[10]) / 2):
                return data[9]
            elif (a < (data[10] + data[11]) / 2):
                return data[10]
            elif (a < (data[11] + data[12]) / 2):
                return data[11]
            elif (a < (data[12] + data[13]) / 2):
                return data[12]
            elif (a < (data[13] + data[14]) / 2):
                return data[13]
            elif (a < (data[14] + data[15]) / 2):
                return data[14]
            elif (a < (data[15] + data[16]) / 2):
                return data[15]
            elif (a < (data[16] + data[17]) / 2):
                return data[16]
            elif (a < (data[17] + data[18]) / 2):
                return data[17]
            elif (a < (data[18] + data[19]) / 2):
                return data[18]
            else:
                return data[19]
        else:
            return a

    def erfcc(self,x):
        z = abs(x)
        t = 1. / (1. + 0.5 * z)
        r = t * math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (.37409196 +
                                                                      t * (.09678418 + t * (-.18628806 + t * (.27886807 +
                                                                                                         t * (
                                                                                                         -1.13520398 + t * (
                                                                                                         1.48851587 + t * (
                                                                                                         -.82215223 +
                                                                                                         t * .17087277)))))))))
        if (x >= 0.):
            return r
        else:
            return 2. - r

    def ncdf(self,x):
        return 1. - 0.5 * math.erfc(x / (2 ** 0.5))
    def DFB_THIN(self, age):
        self.EFF_THIN = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[0])
        self.NoINSP_THINNING = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,self.DM_Name[0])
        if (self.APIComponentType == 'TANKBOTTOM0' or self.APIComponentType == 'TANKROOFFLOAT0'):
            if (self.NomalThick == 0 or self.CurrentThick == 0):
                return 1390
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_512(self.API_ART(self.Art(age)), self.NoINSP_THINNING, self.EFF_THIN)
                #return DAL_CAL.POSTGRESQL.GET_TBL_512(self.API_ART(self.Art(age)), self.EFF_THIN)
        else:
            try:
                if (self.NomalThick == 0 or self.CurrentThick == 0 or self.WeldJointEffciency == 0 or (self.YieldStrengthDesignTemp == 0 and self.TensileStrengthDesignTemp == 0)):
                    return 6500;
                else:
                    a = self.Po_P1_Thin() * self.ncdf(- self.B1_Thin(age))
                    b = self.Po_P2_Thin() * self.ncdf(- self.B2_Thin(age))
                    c = self.Po_P3_Thin() * self.ncdf(- self.B3_Thin(age))
                    return (a + b + c) / (1.56 * pow(10, -4))
            except Exception as e:
                print(e)
                return 0
    def adjustmentInjection(self):
        if (self.HighlyEffectDeadleg):
            return 3
        else:
            return 1
    def adjustmentOnline(self):
        if (
                                                                self.OnlineMonitoring == "Amine high velocity corrosion - Electrical resistance probes" or self.OnlineMonitoring == "Amine high velocity corrosion - Key process variable" or self.OnlineMonitoring == "Amine low velocity corrosion - Electrical resistance probes" or self.OnlineMonitoring == "HCL corrosion - Electrical resistance probes" or
                                                    self.OnlineMonitoring == "HCL corrosion - Key process variable" or self.OnlineMonitoring == "HF corrosion - Key process variable" or self.OnlineMonitoring == "High temperature H2S/H2 corrosion - Electrical resistance probes" or self.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Electrical resistance probes" or
                                    self.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Key process variable" or self.OnlineMonitoring == "Sour water high velocity corrosion - Key process variable" or self.OnlineMonitoring == "Sour water low velocity corrosion - Electrical resistance probes" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Electrical resistance probes" or
                    self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Key process parameters" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion low velocity - Electrical resistance probes"):
            return 10
        elif (
                                    self.OnlineMonitoring == "Amine low velocity corrosion - Corrosion coupons" or self.OnlineMonitoring == "HCL corrosion - Corrosion coupons" or self.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Corrosion coupons" or self.OnlineMonitoring == "Sour water high velocity corrosion - Corrosion coupons" or self.OnlineMonitoring == "Sour water high velocity corrosion - Electrical resistance probes" or
                    self.OnlineMonitoring == "Sour water low velocity corrosion - Corrosion coupons" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion low velocity - Corrosion coupons"):
            return 2
        elif (
                            self.OnlineMonitoring == "Amine low velocity corrosion - Key process variable" or self.OnlineMonitoring == "HCL corrosion - Key process variable & Electrical resistance probes" or self.OnlineMonitoring == "Sour water low velocity corrosion - Key process variable" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Key process parameters & electrical resistance probes" or self.OnlineMonitoring == "Sulfuric acid(H2S / H2) corrosion low velocity - Key process parameters"):
            return 20
        else:
            return 1
    def adjustmentDeadLegs(self):
        if (self.ContainsDeadlegs):
            return 3
        else:
            return 1
    def adjustmentSettlement(self):
        if (self.AdjustmentSettle == "Recorded settlement exceeds API 653 criteria"):
            Fsm = 2
        elif (self.AdjustmentSettle == "Recorded settlement meets API 653 criteria"):
            Fsm = 1
        elif (self.AdjustmentSettle == "Settlement never evaluated"):
            Fsm = 1.5
        else:
            Fsm = 0
        return Fsm
    def adjustmentMaintenance(self):
        if (self.TankMaintain653):
                Fam = 1
        else:
                Fam = 5
        return Fam
    def adjustmentWeldedContruction(self):
        if (self.ComponentIsWeld):
                Fwd = 1
        else:
                Fwd = 10
        return Fwd
    def DF_THIN(self, age):
        Fwd = 1
        Fam = 1
        Fsm = 1
        if (self.HighlyEffectDeadleg):
            Fip = 3
        else:
            Fip = 1
        if (self.ContainsDeadlegs):
            Fdl = 3
        else:
            Fdl = 1

        if self.EquipmentType == "Tank":
            if (self.ComponentIsWeld):
                Fwd = 1
            else:
                Fwd = 10
            if (self.TankMaintain653):
                Fam = 1
            else:
                Fam = 5

            if (self.AdjustmentSettle == "Recorded settlement exceeds API 653 criteria"):
                Fsm = 2
            elif (self.AdjustmentSettle == "Recorded settlement meets API 653 criteria"):
                Fsm = 1
            elif (self.AdjustmentSettle == "Settlement never evaluated"):
                Fsm = 1.5
            else:
                Fsm = 1
        if (
                                                                self.OnlineMonitoring == "Amine high velocity corrosion - Electrical resistance probes" or self.OnlineMonitoring == "Amine high velocity corrosion - Key process variable" or self.OnlineMonitoring == "Amine low velocity corrosion - Electrical resistance probes" or self.OnlineMonitoring == "HCL corrosion - Electrical resistance probes" or
                                                    self.OnlineMonitoring == "HCL corrosion - Key process variable" or self.OnlineMonitoring == "HF corrosion - Key process variable" or self.OnlineMonitoring == "High temperature H2S/H2 corrosion - Electrical resistance probes" or self.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Electrical resistance probes" or
                                    self.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Key process variable" or self.OnlineMonitoring == "Sour water high velocity corrosion - Key process variable" or self.OnlineMonitoring == "Sour water low velocity corrosion - Electrical resistance probes" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Electrical resistance probes" or
                    self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Key process parameters" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion low velocity - Electrical resistance probes"):
            Fom = 10
        elif (
                                    self.OnlineMonitoring == "Amine low velocity corrosion - Corrosion coupons" or self.OnlineMonitoring == "HCL corrosion - Corrosion coupons" or self.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Corrosion coupons" or self.OnlineMonitoring == "Sour water high velocity corrosion - Corrosion coupons" or self.OnlineMonitoring == "Sour water high velocity corrosion - Electrical resistance probes" or
                    self.OnlineMonitoring == "Sour water low velocity corrosion - Corrosion coupons" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion low velocity - Corrosion coupons"):
            Fom = 2
        elif (
                            self.OnlineMonitoring == "Amine low velocity corrosion - Key process variable" or self.OnlineMonitoring == "HCL corrosion - Key process variable & Electrical resistance probes" or self.OnlineMonitoring == "Sour water low velocity corrosion - Key process variable" or self.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Key process parameters & electrical resistance probes" or self.OnlineMonitoring == "Sulfuric acid(H2S / H2) corrosion low velocity - Key process parameters"):
            Fom = 20
        else:
            Fom = 1
        a =  (self.DFB_THIN(age) * Fip * Fdl * Fwd * Fam * Fsm)/Fom
        return max(a,0.1)

    def GET_AGE(self):
        try:
            age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber,"Internal Lining Degradation",self.Commissiondate, self.AssesmentDate)
            # print("1",self.Commissiondate)
            # print("2",self.AssesmentDate)
            # print("age",round(age,2),age)
            return age
        except Exception as e:
            print(e, "error in getage")
###########
    def DF_THINNING_API(self, i):
        # print("thin",self.DF_THIN(self.GET_AGE() + i))
        return self.DF_THIN(self.GET_AGE() + i)
    def DFB_THIN_API(self, i):
        return self.DFB_THIN(self.GET_AGE() + i)
class Df_Lining:
    def __init__(self,INTERNAL_LINNING,LinningType,LINNER_CONDITION,LINNER_ONLINE,AssesmentDate,Commissiondate,ComponentNumber):
        self.INTERNAL_LINNING=INTERNAL_LINNING
        self.LinningType=LinningType
        self.LINNER_CONDITION=LINNER_CONDITION
        self.LINNER_ONLINE=LINNER_ONLINE
        self.ComponentNumber=ComponentNumber
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def DFB_LINNING(self, age):
        if (self.INTERNAL_LINNING):
            if (self.LinningType == "Organic - Low Quality"):
                SUSCEP_LINNING ="MoreThan6Years"
                return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            elif(self.LinningType == "Organic - Medium Quality"):
                SUSCEP_LINNING ="WithinLast6Years"
                return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            elif(self.LinningType == "Organic - High Quality"):
                SUSCEP_LINNING ="WithinLast3Years"
                return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_64(math.ceil(age), self.LinningType)
    def Fdl(self):
        if (self.LINNER_CONDITION == "Poor"):
            Fdl = 10
        elif (self.LINNER_CONDITION == "Average"):
            Fdl = 2
        else:
            Fdl = 1
        return Fdl
    def Fom(self):
        if (self.LINNER_ONLINE):
            Fom = 0.1
        else:
            Fom = 1
        return Fom
    def DF_LINNING(self, age):
        if (self.INTERNAL_LINNING):
            if (self.LINNER_CONDITION == "Poor"):
                Fdl = 10
            elif (self.LINNER_CONDITION == "Average"):
                Fdl = 2
            else:
                Fdl = 1

            if (self.LINNER_ONLINE):
                Fom = 0.1
            else:
                Fom = 1
            return self.DFB_LINNING(age) * Fdl * Fom
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Internal Lining Degradation", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DF_LINING_API(self, i):
        return self.DF_LINNING(self.GET_AGE() + i)

    def DFB_LINNING_API(self, i):
        return self.DFB_LINNING(self.GET_AGE() + i)
class Df_Caustic:
    def __init__(self,CRACK_PRESENT,HEAT_TREATMENT,NaOHConcentration,HEAT_TRACE,STEAM_OUT,MAX_OP_TEMP,CARBON_ALLOY,CAUSTIC_INSP_EFF,CACBONATE_INSP_NUM,CAUSTIC_INSP_NUM,PWHT,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.HEAT_TREATMENT=HEAT_TREATMENT
        self.NaOHConcentration=NaOHConcentration
        self.HEAT_TRACE=HEAT_TRACE
        self.STEAM_OUT=STEAM_OUT
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.CARBON_ALLOY=CARBON_ALLOY
        self.CAUSTIC_INSP_EFF=CAUSTIC_INSP_EFF
        self.CACBONATE_INSP_NUM=CACBONATE_INSP_NUM
        self.CAUSTIC_INSP_NUM=CAUSTIC_INSP_NUM
        # chua thay su dung PWHT
        self.PWHT=PWHT
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def getSusceptibility_Caustic(self):
        if (self.CRACK_PRESENT):
            sus = "High"
            # if self.CRACK_PRESENT == "Cracks Removed":
            #     sus = "None"
        elif (self.HEAT_TREATMENT == "Stress Relieved"):
            sus = "None"
        else:
            if (self.plotinArea() == 'A'):
                if (self.NaOHConcentration < 5):
                    if (self.HEAT_TRACE):
                        sus = "Medium"
                    elif (self.STEAM_OUT):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.HEAT_TRACE):
                    sus = "High"
                elif (self.STEAM_OUT):
                    sus = "Medium"
                else:
                    sus = "None"
            else:
                if (self.NaOHConcentration < 5):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def plotinArea(self):
        TempBase = self.interpolation(self.NaOHConcentration)
        if (self.MAX_OP_TEMP < TempBase):
            k = 'A'
        else:
            k = 'B'
        return k

    def interpolation(self, t):
        X = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        Y = [81.25, 80, 78.125, 74.219, 69.375, 65.625, 58.75, 55, 51.25, 48.75, 48.125]
        n = len(X)
        try:
            c = [0 for _ in range(n)]
            w = [0 for _ in range(n)]
            for i in range(0, n):
                # print(i)
                w[i] = Y[i]
                for j in reversed(range(i)):
                    # print(j)
                    w[j] = (w[j + 1] - w[j]) / (X[i] - X[j])
                c[i] = w[0]
            s = c[n - 1]
            for i in reversed(range(n - 1)):
                # print(X[i])
                s = s * (t - X[i]) + c[i]
            # print(c)
            return s
        except Exception as e:
            print(e)
            raise

    def SVI_CAUSTIC(self):
        if (self.getSusceptibility_Caustic() == "High"):
            sev = 5000
        elif (self.getSusceptibility_Caustic() == "Medium"):
            sev = 500
        elif (self.getSusceptibility_Caustic() == "Low"):
            sev = 50
        else:
            sev = 0
        return sev
    def DFB_CAUSTIC(self, age):
        if (self.CARBON_ALLOY and self.NaOHConcentration != 0):
            self.CAUSTIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Caustic Stress Corrosion Cracking")
            self.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Caustic Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_CAUSTIC()
            elif (self.CAUSTIC_INSP_EFF == "E" or self.CAUSTIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CAUSTIC_INSP_NUM) + self.CAUSTIC_INSP_EFF
            DFB_CAUSTIC = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CAUSTIC(), FIELD)
            return DFB_CAUSTIC
        else:
            return 0
    def DF_CAUSTIC(self, age):
        if (self.CARBON_ALLOY and self.NaOHConcentration != 0):
            self.CAUSTIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Caustic Stress Corrosion Cracking")
            self.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Caustic Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_CAUSTIC()
            elif (self.CAUSTIC_INSP_EFF == "E" or self.CAUSTIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CAUSTIC_INSP_NUM) + self.CAUSTIC_INSP_EFF
            DFB_CAUSTIC = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CAUSTIC(), FIELD)
            return DFB_CAUSTIC * pow(max(age, 1.0), 1.1)
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Caustic Stress Corrosion Cracking", self.Commissiondate,
                                              self.AssesmentDate)
        return age

    def DFB_CAUSTIC_API(self, i):
        return self.DFB_CAUSTIC(self.GET_AGE() + i)
    def DF_CAUSTIC_API(self, i):
        return self.DF_CAUSTIC(self.GET_AGE() + i)
class Df_Amine:
    def __init__(self,AMINE_EXPOSED,CARBON_ALLOY,CRACK_PRESENT,AMINE_SOLUTION,MAX_OP_TEMP,HEAT_TRACE,STEAM_OUT,AMINE_INSP_EFF,AMINE_INSP_NUM,PWHT,AssesmentDate,Commissiondate,ComponentNumber):
        # chua thay su dung PWHT
        self.AMINE_EXPOSED=AMINE_EXPOSED
        self.CARBON_ALLOY=CARBON_ALLOY
        self.CRACK_PRESENT=CRACK_PRESENT
        self.AMINE_SOLUTION=AMINE_SOLUTION
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.HEAT_TRACE=HEAT_TRACE
        self.STEAM_OUT=STEAM_OUT
        self.AMINE_INSP_EFF=AMINE_INSP_EFF
        self.AMINE_INSP_NUM=AMINE_INSP_NUM
        self.PWHT=PWHT
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def getSusceptibility_Amine(self):
        if (self.AMINE_EXPOSED and self.CARBON_ALLOY):
            if (self.CRACK_PRESENT):
                sus = "High"
                # if self.CRACK_PRESENT == "Cracks Removed":
                #     sus = "None"
            # elif (self.HEAT_TREATMENT == "Stress Relieved"):
            #     sus = "None"
            else:
                if (
                                self.AMINE_SOLUTION == "Methyldiethanolamine MDEA" or self.AMINE_SOLUTION == "Disopropanolamine DIPA"):
                    if (self.MAX_OP_TEMP > 82.22):
                        sus = "High"
                    elif ((
                                  self.MAX_OP_TEMP > 37.78 and self.MAX_OP_TEMP < 82.22) or self.HEAT_TRACE or self.STEAM_OUT):
                        sus = "Medium"
                    else:
                        sus = "Low"
                elif (self.AMINE_SOLUTION == "Diethanolamine DEA"):
                    if (self.MAX_OP_TEMP > 82.22):
                        sus = "Medium"
                    elif ((
                                  self.MAX_OP_TEMP > 60 and self.MAX_OP_TEMP < 82.22) or self.HEAT_TRACE or self.STEAM_OUT):
                        sus = "Low"
                    else:
                        sus = "None"
                else:
                    if (self.MAX_OP_TEMP > 82.22 or self.HEAT_TRACE or self.STEAM_OUT):
                        sus = "Low"
                    else:
                        sus = "None"
            return sus

    def SVI_AMINE(self):
        if (self.getSusceptibility_Amine() == "High"):
            return 1000
        elif (self.getSusceptibility_Amine() == "Medium"):
            return 100
        elif (self.getSusceptibility_Amine() == "Low"):
            return 10
        else:
            return 0
    def DFB_AMINE(self,age):
        self.AMINE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Amine Stress Corrosion Cracking")
        self.AMINE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,
                                                                 "Amine Stress Corrosion Cracking")
        if (self.AMINE_INSP_EFF == "E" or self.AMINE_INSP_NUM == 0):
            FIELD = "E"
        elif (age > 1):
            return self.SVI_AMINE()
        else:
            FIELD = str(self.AMINE_INSP_NUM) + self.AMINE_INSP_EFF
        return DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_AMINE(), FIELD)
    def DF_AMINE(self, age):
        if (self.CARBON_ALLOY):
            self.AMINE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Amine Stress Corrosion Cracking")
            self.AMINE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Amine Stress Corrosion Cracking")
            if (self.AMINE_INSP_EFF == "E" or self.AMINE_INSP_NUM == 0):
                FIELD = "E"
            elif (age > 1):
                return self.SVI_AMINE()
            else:
                FIELD = str(self.AMINE_INSP_NUM) + self.AMINE_INSP_EFF
            DFB_AMIN = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_AMINE(), FIELD)

            return DFB_AMIN * pow(max(age, 1.0), 1.1)
        else:
            return 0

    def GET_AGE(self):
        try:
            age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Amine Stress Corrosion Cracking", self.Commissiondate,
                                              self.AssesmentDate)
            return age
        except Exception as e:

            print(e)
        ###########
    def DFB_AMINE_API(self,i):
        return self.DFB_AMINE(self.GET_AGE() + i)
    def DF_AMINE_API(self, i):
        return self.DF_AMINE(self.GET_AGE() + i)
class Df_Sulphide:
    def __init__(self,PH,H2SContent,PRESENT_CYANIDE,CRACK_PRESENT,PWHT,BRINNEL_HARDNESS,CARBON_ALLOY,AQUEOUS_OPERATOR,ENVIRONMENT_H2S_CONTENT,SULPHIDE_INSP_EFF,SULPHIDE_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.PH=PH
        self.H2SContent=H2SContent
        self.PRESENT_CYANIDE=PRESENT_CYANIDE
        self.CRACK_PRESENT=CRACK_PRESENT
        self.PWHT=PWHT
        self.BRINNEL_HARDNESS=BRINNEL_HARDNESS
        self.CARBON_ALLOY=CARBON_ALLOY
        self.AQUEOUS_OPERATOR=AQUEOUS_OPERATOR
        self.ENVIRONMENT_H2S_CONTENT=ENVIRONMENT_H2S_CONTENT
        self.SULPHIDE_INSP_EFF=SULPHIDE_INSP_EFF
        self.SULPHIDE_INSP_NUM=SULPHIDE_INSP_NUM
        self.AssesmentDate=AssesmentDate
        self.Commissiondate=Commissiondate
        self.ComponentNumber=ComponentNumber
    def GET_ENVIRONMENTAL_SEVERITY(self):
        if (self.PH < 5.5):
            if (self.H2SContent < 50):
                env = "Low"
            elif (self.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        elif (self.PH <= 7.5 and self.PH >= 5.5):
            if (self.H2SContent > 10000):
                env = "Moderate"
            else:
                env = "Low"
        elif (self.PH >= 7.6 and self.PH <= 8.3):
            if (self.H2SContent < 50):
                env = "Low"
            else:
                env = "Moderate"
        elif (self.PH >= 8.4 and self.PH <= 8.9):
            if (self.H2SContent < 50):
                env = "Low"
            elif (self.H2SContent <= 10000 and self.PRESENT_CYANIDE):
                env = "High"
            elif (self.H2SContent <= 10000):
                env = "Moderate"
            else:
                env = "High"
        else:
            if (self.H2SContent < 50):
                env = "Low"
            elif (self.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        return env

    def GET_SUSCEPTIBILITY_SULPHIDE(self):
        env = self.GET_ENVIRONMENTAL_SEVERITY()
        if (self.CRACK_PRESENT):
            sus = "High"
            # if self.CRACK_PRESENT == "Cracks Removed":
            #     sus = "None"
        elif (self.PWHT):
            if (self.BRINNEL_HARDNESS == "Below 200"):
                sus = "None"
            elif (self.BRINNEL_HARDNESS == "Between 200 and 237"):
                if (env == "High"):
                    sus = "Low"
                else:
                    sus = "None"
            else:
                if (env == "High"):
                    sus = "Medium"
                elif (env == "Moderate"):
                    sus = "Low"
                else:
                    sus = "None"
        else:
            if (self.BRINNEL_HARDNESS == "Below 200"):
                sus = "Low"
            elif (self.BRINNEL_HARDNESS == "Between 200 and 237"):
                if (env == "Low"):
                    sus = "Low"
                else:
                    sus = "Medium"
            else:
                if (env == "Low"):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_SULPHIDE(self):
        if (self.GET_SUSCEPTIBILITY_SULPHIDE() == "High"):
            return 100
        elif (self.GET_SUSCEPTIBILITY_SULPHIDE() == "Medium"):
            return 10
        elif (self.GET_SUSCEPTIBILITY_SULPHIDE() == "Low"):
            return 1
        else:
            return 0
    def DFB_SULPHIDE(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.ENVIRONMENT_H2S_CONTENT):
            self.SULPHIDE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Sulphide Stress Corrosion Cracking (H2S)")
            self.SULPHIDE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Sulphide Stress Corrosion Cracking (H2S)")
            if (age < 1):
                return self.SVI_SULPHIDE()
            elif (self.SULPHIDE_INSP_EFF == "E" or self.SULPHIDE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.SULPHIDE_INSP_NUM) + self.SULPHIDE_INSP_EFF
            DFB_SULPHIDE = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_SULPHIDE(), FIELD)
            return DFB_SULPHIDE
        else:
            return 0
    def DF_SULPHIDE(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.ENVIRONMENT_H2S_CONTENT):
            self.SULPHIDE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Sulphide Stress Corrosion Cracking (H2S)")
            self.SULPHIDE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Sulphide Stress Corrosion Cracking (H2S)")
            if (age < 1):
                return self.SVI_SULPHIDE()
            elif (self.SULPHIDE_INSP_EFF == "E" or self.SULPHIDE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.SULPHIDE_INSP_NUM) + self.SULPHIDE_INSP_EFF
            DFB_SULPHIDE = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_SULPHIDE(), FIELD)
            return DFB_SULPHIDE * pow(max(age, 1.0), 1.1)
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Sulphide Stress Corrosion Cracking (H2S)", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_SULPHIDE_API(self, i):
        return self.DFB_SULPHIDE(self.GET_AGE() + i)
    def DF_SULPHIDE_API(self, i):
        return self.DF_SULPHIDE(self.GET_AGE() + i)
class Df_Hicsohic_H2s:
    def __init__(self,PH,H2SContent,PRESENT_CYANIDE,CRACK_PRESENT,PWHT,SULFUR_CONTENT,OnlineMonitoring,CARBON_ALLOY,AQUEOUS_OPERATOR,ENVIRONMENT_H2S_CONTENT,SULFUR_INSP_EFF,SULFUR_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.PH=PH
        self.H2SContent=H2SContent
        self.PRESENT_CYANIDE=PRESENT_CYANIDE
        self.CRACK_PRESENT=CRACK_PRESENT
        self.PWHT=PWHT
        self.SULFUR_CONTENT=SULFUR_CONTENT
        self.OnlineMonitoring=OnlineMonitoring
        self.CARBON_ALLOY=CARBON_ALLOY
        self.AQUEOUS_OPERATOR=AQUEOUS_OPERATOR
        self.ENVIRONMENT_H2S_CONTENT=ENVIRONMENT_H2S_CONTENT
        self.SULFUR_INSP_EFF=SULFUR_INSP_EFF
        self.SULFUR_INSP_NUM=SULFUR_INSP_NUM
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def GET_ENVIROMENTAL_HICSOHIC_H2S(self):
        if (self.PH < 5.5):
            if (self.H2SContent < 50):
                env = "Low"
            elif (self.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        elif (self.PH >= 5.5 and self.PH <= 7.5):
            if (self.H2SContent > 10000):
                env = "Moderate"
            else:
                env = "Low"
        elif (self.PH >= 7.6 and self.PH <= 8.3):
            if (self.H2SContent < 50):
                env = "Low"
            else:
                env = "Moderate"
        elif (self.PH >= 8.4 and self.PH <= 8.9):
            if (self.H2SContent < 50):
                env = "Low"
            elif (self.H2SContent <= 10000 and self.PRESENT_CYANIDE):
                env = "High"
            elif (self.H2SContent <= 10000):
                env = "Moderate"
            else:
                env = "High"
        else:
            if (self.H2SContent < 50):
                env = "Low"
            elif (self.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        return env

    def GET_SUSCEPTIBILITY_HICSOHIC_H2S(self):
        env = self.GET_ENVIROMENTAL_HICSOHIC_H2S()
        if (self.CRACK_PRESENT):
            sus = "High"
        elif (self.PWHT):
            if (self.SULFUR_CONTENT == "High > 0.01%"):
                if (env == "High"):
                    sus = "High"
                elif (env == "Moderate"):
                    sus = "Medium"
                else:
                    sus = "Low"
            elif self.SULFUR_CONTENT == "Low <= 0.01%":
                if (env == "High"):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                sus = "Low"
        else:
            if (self.SULFUR_CONTENT == "High > 0.01%"):
                if (env == "Low"):
                    sus = "Medium"
                else:
                    sus = "High"
            elif (self.SULFUR_CONTENT == "Low <=0.01%"):
                if (env == "High"):
                    sus = "High"
                elif (env == "Moderate"):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                if (env == "High"):
                    sus = "Medium"
                else:
                    sus = "Low"
        return sus

    def SVI_HICSOHIC_H2S(self):
        if (self.GET_SUSCEPTIBILITY_HICSOHIC_H2S() == "High"):
            return 100
        elif (self.GET_SUSCEPTIBILITY_HICSOHIC_H2S() == "Medium"):
            return 10
        elif (self.GET_ENVIROMENTAL_HICSOHIC_H2S() == "Low"):
            return 1
        else:
            return 0

    def FOM_HIC(self):
        if self.OnlineMonitoring == "Other corrosion - Key process variable and Hydrogen probes":
            return 4
        elif (
                self.OnlineMonitoring == "Other corrosion - Key process variable" or self.OnlineMonitoring == "Other corrosion - Hydrogen probes"):
            return 2
        else:
            return 1
    def DFB_HICSOHIC_H2S(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.ENVIRONMENT_H2S_CONTENT):
            self.SULFUR_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "HIC/SOHIC-H2S")
            self.SULFUR_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "HIC/SOHIC-H2S")
            if (age < 1):
                return self.SVI_HICSOHIC_H2S() / self.FOM_HIC()
            elif (self.SULFUR_INSP_EFF == "E" or self.SULFUR_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.SULPHIDE_INSP_NUM) + self.SULFUR_INSP_NUM
            DFB_SULFUR = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HICSOHIC_H2S(), FIELD)
            return DFB_SULFUR
        else:
            return 0
    def DF_HICSOHIC_H2S(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.ENVIRONMENT_H2S_CONTENT):
            self.SULFUR_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "HIC/SOHIC-H2S")
            self.SULFUR_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "HIC/SOHIC-H2S")
            if (age < 1):
                return self.SVI_HICSOHIC_H2S() / self.FOM_HIC()
            elif (self.SULFUR_INSP_EFF == "E" or self.SULFUR_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.SULPHIDE_INSP_NUM) + self.SULFUR_INSP_NUM
            DFB_SULFUR = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HICSOHIC_H2S(), FIELD)
            return (DFB_SULFUR * pow(max(age, 1.0), 1.1)) / self.FOM_HIC()
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "HIC/SOHIC-H2S", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_HICSOHIC_H2S_API(self, i):
        return self.DFB_HICSOHIC_H2S(self.GET_AGE() + i)
    def DF_HICSOHIC_H2S_API(self, i):
        return self.DF_HICSOHIC_H2S(self.GET_AGE() + i)
class Df_Cacbonate:
    def __init__(self,CRACK_PRESENT,PWHT,CO3_CONTENT,PH,CARBON_ALLOY,AQUEOUS_OPERATOR,CACBONATE_INSP_EFF,CACBONATE_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.PWHT=PWHT
        self.CO3_CONTENT=CO3_CONTENT
        self.PH=PH
        self.CARBON_ALLOY=CARBON_ALLOY
        self.AQUEOUS_OPERATOR=AQUEOUS_OPERATOR
        self.CACBONATE_INSP_EFF=CACBONATE_INSP_EFF
        self.CACBONATE_INSP_NUM=CACBONATE_INSP_NUM
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def GET_SUSCEPTIBILITY_CARBONATE(self):
        if (self.CRACK_PRESENT):
            sus = "High"
        elif (self.PWHT):
            sus = "None"
        else:
            if (self.CO3_CONTENT < 100):
                if (self.PH < 7.5):
                    sus = "None"
                elif (self.PH >= 9.0):
                    sus = "High"
                else:
                    sus = "Low"
            else:
                if (self.PH < 7.5):
                    sus = "None"
                elif (7.5 <= self.PH < 8):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_CARBONATE(self):
        if (self.GET_SUSCEPTIBILITY_CARBONATE() == "High"):
            return 1000
        elif (self.GET_SUSCEPTIBILITY_CARBONATE() == "Medium"):
            return 100
        elif (self.GET_SUSCEPTIBILITY_CARBONATE() == "Low"):
            return 10
        else:
            return 0
    def DFB_CACBONATE(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.PH >= 7.5):
            self.CACBONATE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Carbonate Stress Corrosion Cracking")
            self.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Carbonate Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_CARBONATE()
            elif (self.CACBONATE_INSP_EFF == "E" or self.CACBONATE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CACBONATE_INSP_NUM) + self.CACBONATE_INSP_EFF
            return(DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CARBONATE(), FIELD))
        else:
            return 0
    def DF_CACBONATE(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.PH >= 7.5):
            self.CACBONATE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Carbonate Stress Corrosion Cracking")
            self.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Carbonate Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_CARBONATE()
            elif (self.CACBONATE_INSP_EFF == "E" or self.CACBONATE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CACBONATE_INSP_NUM) + self.CACBONATE_INSP_EFF
            DFB_CACBONATE = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CARBONATE(), FIELD)

            return DFB_CACBONATE * pow(max(age, 1.0), 1.1)
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Carbonate Stress Corrosion Cracking", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_CACBONATE_API(self, i):
        return self.DFB_CACBONATE(self.GET_AGE() + i)
    def DF_CACBONATE_API(self, i):
        return self.DF_CACBONATE(self.GET_AGE() + i)
class Df_PTA:
    def __init__(self,CRACK_PRESENT,ExposedSH2OOperation,ExposedSH2OShutdown,MAX_OP_TEMP,ThermalHistory,PTAMaterial,DOWNTIME_PROTECTED,PTA_SUSCEP,CARBON_ALLOY,NICKEL_ALLOY,EXPOSED_SULFUR,PTA_INSP_EFF,PTA_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.ExposedSH2OOperation=ExposedSH2OOperation
        self.ExposedSH2OShutdown=ExposedSH2OShutdown
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.ThermalHistory=ThermalHistory
        self.PTAMaterial=PTAMaterial
        self.DOWNTIME_PROTECTED=DOWNTIME_PROTECTED
        self.PTA_SUSCEP=PTA_SUSCEP
        self.CARBON_ALLOY=CARBON_ALLOY
        self.NICKEL_ALLOY=NICKEL_ALLOY
        self.EXPOSED_SULFUR=EXPOSED_SULFUR
        self.PTA_INSP_EFF=PTA_INSP_EFF
        self.PTA_INSP_NUM=PTA_INSP_NUM
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber

    def GET_SUSCEPTIBILITY_PTA(self):
        if (self.CRACK_PRESENT):
            sus = "High"
            return sus
        if (not self.ExposedSH2OOperation and not self.ExposedSH2OShutdown):
            sus = "None"
        else:
            if (self.MAX_OP_TEMP < 427):
                if (self.ThermalHistory == "Solution Annealed"):
                    if (self.PTAMaterial == "Regular 300 series Stainless Steels and Alloys 600 and 800"):
                        sus = "Medium"
                    elif (self.PTAMaterial == "H Grade 300 series Stainless Steels"):
                        sus = "High"
                    elif (self.PTAMaterial == "L Grade 300 series Stainless Steels"):
                        sus = "Low"
                    elif (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Medium"
                    elif (
                        self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised Before Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Medium"
                    elif (
                        self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised After Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Low"
                    elif (
                        self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                else:
                    sus = "None"
            else:
                if (self.ThermalHistory == "Solution Annealed"):
                    if (self.PTAMaterial == "Regular 300 series Stainless Steels and Alloys 600 and 800"):
                        sus = "High"
                    elif (self.PTAMaterial == "H Grade 300 series Stainless Steels"):
                        sus = "High"
                    elif (self.PTAMaterial == "L Grade 300 series Stainless Steels"):
                        sus = "Medium"
                    elif (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "High"
                    elif (
                        self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Medium"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised Before Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "High"
                    elif (
                        self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised After Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Low"
                    elif (
                        self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                else:
                    sus = "None"
        if (self.DOWNTIME_PROTECTED):
            if (sus == "High"):
                sus = "Medium"
            elif (sus == "Medium"):
                sus = "Low"
            else:
                sus = "None"
        return sus

    def SVI_PTA(self):
        if (self.GET_SUSCEPTIBILITY_PTA() == "High"):
            return 5000
        elif (self.GET_SUSCEPTIBILITY_PTA() == "Medium"):
            return 500
        elif (self.GET_SUSCEPTIBILITY_PTA() == "Low"):
            return 50
        else:
            return 1

    def DFB_PTA(self, age):
        if (self.PTA_SUSCEP or ((self.CARBON_ALLOY or self.NICKEL_ALLOY) and self.EXPOSED_SULFUR)):
            self.PTA_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber,
                                                                "Polythionic Acid Stress Corrosion Cracking")
            self.PTA_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,
                                                                   "Polythionic Acid Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_PTA()
            elif (self.PTA_INSP_EFF == "E" or self.PTA_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.PTA_INSP_NUM) + self.PTA_INSP_EFF
            DFB_PTA = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_PTA(), FIELD)
            return DFB_PTA
        else:
            return 0
    def DF_PTA(self, age):
        if (self.PTA_SUSCEP or ((self.CARBON_ALLOY or self.NICKEL_ALLOY) and self.EXPOSED_SULFUR)):
            self.PTA_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Polythionic Acid Stress Corrosion Cracking")
            self.PTA_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Polythionic Acid Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_PTA()
            elif (self.PTA_INSP_EFF == "E" or self.PTA_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.PTA_INSP_NUM) + self.PTA_INSP_EFF
            DFB_PTA = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_PTA(), FIELD)
            return DFB_PTA * pow(age, 1.1)
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Polythionic Acid Stress Corrosion Cracking", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_PTA_API(self, i):
        return self.DFB_PTA(self.GET_AGE() + i)
    def DF_PTA_API(self, i):
        return self.DF_PTA(self.GET_AGE() + i)
class Df_CLSCC:
    def __init__(self,CRACK_PRESENT,PH,MAX_OP_TEMP,MIN_OP_TEMP,CHLORIDE_ION_CONTENT,INTERNAL_EXPOSED_FLUID_MIST,AUSTENITIC_STEEL,CLSCC_INSP_EFF,CLSCC_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.PH=PH
        self.MAX_OP_TEMP=MAX_OP_TEMP
        # chua thay su dung MIN_OP_TEMP
        self.MIN_OP_TEMP=MIN_OP_TEMP
        self.CHLORIDE_ION_CONTENT=CHLORIDE_ION_CONTENT
        self.INTERNAL_EXPOSED_FLUID_MIST=INTERNAL_EXPOSED_FLUID_MIST
        self.AUSTENITIC_STEEL=AUSTENITIC_STEEL
        self.CLSCC_INSP_EFF=CLSCC_INSP_EFF
        self.CLSCC_INSP_NUM=CLSCC_INSP_NUM
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def GET_SUSCEPTIBILITY_CLSCC(self):
        if (self.CRACK_PRESENT):
            sus = "High"
            return sus
        if (self.PH <= 10):
            if (self.MAX_OP_TEMP <= 38):
                if (self.CHLORIDE_ION_CONTENT > 1000):
                    sus = "Medium"
                else:
                    sus = "High"
            elif (self.MAX_OP_TEMP > 38 and self.MAX_OP_TEMP <= 66):
                if (self.CHLORIDE_ION_CONTENT >= 1 and self.CHLORIDE_ION_CONTENT <= 10):
                    sus = "Low"
                elif (self.CHLORIDE_ION_CONTENT > 1000):
                    sus = "High"
                else:
                    sus = "Medium"
            elif (self.MAX_OP_TEMP > 66 and self.MAX_OP_TEMP <= 93):
                if (self.CHLORIDE_ION_CONTENT >= 1 and self.CHLORIDE_ION_CONTENT <= 100):
                    sus = "Medium"
                else:
                    sus = "High"
            elif (self.MAX_OP_TEMP > 93 and self.MAX_OP_TEMP <= 149):
                if (self.CHLORIDE_ION_CONTENT >= 11 and self.CHLORIDE_ION_CONTENT <= 1000):
                    sus = "High"
                else:
                    sus = "Medium"
            else:
                sus = "High"
        else:
            if (self.MAX_OP_TEMP <= 38):
                sus = "None"
            elif (self.MAX_OP_TEMP > 38 and self.MAX_OP_TEMP <= 93):
                sus = "Low"
            elif (self.MAX_OP_TEMP > 93 and self.MAX_OP_TEMP <= 149):
                if (self.CHLORIDE_ION_CONTENT > 1000):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                if (self.CHLORIDE_ION_CONTENT >= 1 and self.CHLORIDE_ION_CONTENT <= 100):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_CLSCC(self):
        if (self.GET_SUSCEPTIBILITY_CLSCC() == "High"):
            return 5000
        elif (self.GET_SUSCEPTIBILITY_CLSCC() == "Medium"):
            return 500
        elif (self.GET_SUSCEPTIBILITY_CLSCC() == "Low"):
            return 50
        else:
            return 0
    def DFB_CLSCC(self, age):
        if (self.INTERNAL_EXPOSED_FLUID_MIST and self.AUSTENITIC_STEEL and self.MAX_OP_TEMP > 38):
            self.CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Chloride Stress Corrosion Cracking")
            self.CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,"Chloride Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_CLSCC()
            if (self.CLSCC_INSP_EFF == "E" or self.CLSCC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CLSCC_INSP_NUM) + self.CLSCC_INSP_EFF
            DFB_CLSCC = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CLSCC(), FIELD)
            return DFB_CLSCC
        else:
            return 0
    def DF_CLSCC(self, age):
        if (self.INTERNAL_EXPOSED_FLUID_MIST and self.AUSTENITIC_STEEL and self.MAX_OP_TEMP > 38):
            self.CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Chloride Stress Corrosion Cracking")
            self.CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,"Chloride Stress Corrosion Cracking")
            if (age < 1):
                return self.SVI_CLSCC()
            if (self.CLSCC_INSP_EFF == "E" or self.CLSCC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CLSCC_INSP_NUM) + self.CLSCC_INSP_EFF
            DFB_CLSCC = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CLSCC(), FIELD)
            return DFB_CLSCC * pow(age, 1.1)
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Chloride Stress Corrosion Cracking", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_CLSCC_API(self, i):
        return self.DFB_CLSCC(self.GET_AGE() + i)
    def DF_CLSCC_API(self, i):
        return self.DF_CLSCC(self.GET_AGE() + i)
class Df_HSCHF:
    def __init__(self,CRACK_PRESENT,HF_PRESENT,CARBON_ALLOY,PWHT,BRINNEL_HARDNESS,HSC_HF_INSP_EFF,HSC_HF_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.HF_PRESENT=HF_PRESENT
        self.CARBON_ALLOY=CARBON_ALLOY
        self.PWHT=PWHT
        self.BRINNEL_HARDNESS=BRINNEL_HARDNESS
        self.HSC_HF_INSP_EFF=HSC_HF_INSP_EFF
        self.HSC_HF_INSP_NUM=HSC_HF_INSP_NUM
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def GET_SUSCEPTIBILITY_HSCHF(self):
        if (self.CRACK_PRESENT):
            sus = "High"
            return sus
        if (not self.HF_PRESENT or not self.CARBON_ALLOY):
            sus = "None"
        else:
            if (self.PWHT):
                if (self.BRINNEL_HARDNESS == "Below 200"):
                    sus = "None"
                elif (self.BRINNEL_HARDNESS == "Between 200 and 237"):
                    sus = "Low"
                else:
                    sus = "High"
            else:
                if (self.BRINNEL_HARDNESS == "Below 200"):
                    sus = "Low"
                elif (self.BRINNEL_HARDNESS == "Between 200 and 237"):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_HSCHF(self):
        if (self.GET_SUSCEPTIBILITY_HSCHF() == "High"):
            return 100
        elif (self.GET_SUSCEPTIBILITY_HSCHF() == "Medium"):
            return 10
        else:
            return 0

    def DFB_HSCHF(self, age):
        if (self.CARBON_ALLOY and self.HF_PRESENT):
            self.HSC_HF_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber,
                                                                   "Hydrogen Stress Cracking (HF)")
            self.HSC_HF_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,
                                                                      "Hydrogen Stress Cracking (HF)")
            if (age < 1):
                return self.SVI_HSCHF()
            if (self.HSC_HF_INSP_EFF == "E" or self.HSC_HF_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.HSC_HF_INSP_NUM) + self.HSC_HF_INSP_EFF
            DFB_HSCHF = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HSCHF(), FIELD)
            return DFB_HSCHF
        else:
            return 0

    def DF_HSCHF(self, age):
        if (self.CARBON_ALLOY and self.HF_PRESENT):
            self.HSC_HF_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Hydrogen Stress Cracking (HF)")
            self.HSC_HF_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Hydrogen Stress Cracking (HF)")
            if (age < 1):
                return self.SVI_HSCHF()
            if (self.HSC_HF_INSP_EFF == "E" or self.HSC_HF_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.HSC_HF_INSP_NUM) + self.HSC_HF_INSP_EFF
            DFB_HSCHF = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HSCHF(), FIELD)
            return DFB_HSCHF * pow(age, 1.1)
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Hydrogen Stress Cracking (HF)",
                                              self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_HSCHF_API(self, i):
        return self.DFB_HSCHF(self.GET_AGE() + i)

    def DF_HSCHF_API(self, i):
        return self.DF_HSCHF(self.GET_AGE() + i)

class Df_HIC_SOHIC_HF:
    def __init__(self,CRACK_PRESENT,HF_PRESENT,CARBON_ALLOY,PWHT,SULFUR_CONTENT,OnlineMonitoring,HICSOHIC_INSP_EFF,HICSOHIC_INSP_NUM,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.HF_PRESENT=HF_PRESENT
        self.CARBON_ALLOY=CARBON_ALLOY
        self.PWHT=PWHT
        self.SULFUR_CONTENT=SULFUR_CONTENT
        self.HICSOHIC_INSP_EFF=HICSOHIC_INSP_EFF
        self.HICSOHIC_INSP_NUM=HICSOHIC_INSP_NUM
        # chua thay su dung OnlineMonitoring
        self.OnlineMonitoring=OnlineMonitoring
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def GET_SUSCEPTIBILITY_HICSOHIC_HF(self):
        if (self.CRACK_PRESENT):
            return "High"
        if (not self.HF_PRESENT or not self.CARBON_ALLOY):
            return "None"
        if (self.PWHT):
            if (self.SULFUR_CONTENT == "High > 0.01%"):
                sus = "High"
            elif (self.SULFUR_CONTENT == "Low 0.002 - 0.01%"):
                sus = "Medium"
            else:
                sus = "Low"
        else:
            if (self.SULFUR_CONTENT == "High > 0.01%" or self.SULFUR_CONTENT == "Low 0.002 - 0.01%"):
                sus = "High"
            else:
                sus = "Medium"
        return sus

    def FOM_HIC(self):
        if self.OnlineMonitoring == "Other corrosion - Key process variable and Hydrogen probes":
            return 4
        elif (
                self.OnlineMonitoring == "Other corrosion - Key process variable" or self.OnlineMonitoring == "Other corrosion - Hydrogen probes"):
            return 2
        else:
            return 1
    def SVI_HICSOHIC_HF(self):
        if (self.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "High"):
            return 100
        elif (self.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "Medium"):
            return 10
        elif (self.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "Low"):
            return 1
        else:
            return 0
    def DFB_HIC_SOHIC_HF(self, age):
        if (self.CARBON_ALLOY and self.HF_PRESENT):
            self.HICSOHIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "HF Produced HIC/SOHIC")
            self.HICSOHIC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "HF Produced HIC/SOHIC")
            if (age < 1):
                return self.SVI_HICSOHIC_HF() / self.FOM_HIC()
            if (self.HICSOHIC_INSP_EFF == "E" or self.HICSOHIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.HICSOHIC_INSP_NUM) + self.HICSOHIC_INSP_EFF
            DFB_HICSOHIC_HF = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HICSOHIC_HF(), FIELD)
            return DFB_HICSOHIC_HF
        else:
            return 0
    def DF_HIC_SOHIC_HF(self, age):
        if (self.CARBON_ALLOY and self.HF_PRESENT):
            self.HICSOHIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "HF Produced HIC/SOHIC")
            self.HICSOHIC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "HF Produced HIC/SOHIC")
            if (age < 1):
                return self.SVI_HICSOHIC_HF() / self.FOM_HIC()
            if (self.HICSOHIC_INSP_EFF == "E" or self.HICSOHIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.HICSOHIC_INSP_NUM) + self.HICSOHIC_INSP_EFF
            DFB_HICSOHIC_HF = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HICSOHIC_HF(), FIELD)
            return DFB_HICSOHIC_HF * pow(age, 1.1) / self.FOM_HIC()
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "HF Produced HIC/SOHIC", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_HIC_SOHIC_HF_API(self, i):
        return self.DFB_HIC_SOHIC_HF(self.GET_AGE() + i)
    def DF_HIC_SOHIC_HF_API(self, i):
        return self.DF_HIC_SOHIC_HF(self.GET_AGE() + i)
# Calculate EXTERNAL CORROSION
class Df_EXTERNAL_CORROSION:
    def __init__(self,COMPONENT_INSTALL_DATE,EXTERN_COAT_QUALITY,EXTERNAL_EVIRONMENT,CUI_PERCENT_2,CUI_PERCENT_3,CUI_PERCENT_4,CUI_PERCENT_5,CUI_PERCENT_6,SUPPORT_COATING,INTERFACE_SOIL_WATER,EXTERNAL_EXPOSED_FLUID_MIST,CARBON_ALLOY,
                 MAX_OP_TEMP,MIN_OP_TEMP,EXTERNAL_INSP_EFF,EXTERNAL_INSP_NUM,NoINSP_EXTERNAL,APIComponentType,NomalThick,CurrentThick,WeldJointEffciency,YieldStrengthDesignTemp,TensileStrengthDesignTemp,ShapeFactor,
                 MINIUM_STRUCTURAL_THICKNESS_GOVERS,CR_Confidents_Level,AllowableStress,MinThickReq,StructuralThickness,Pressure,Diametter,AssesmentDate,Commissiondate,ComponentNumber):

        self.COMPONENT_INSTALL_DATE=COMPONENT_INSTALL_DATE
        self.EXTERN_COAT_QUALITY=EXTERN_COAT_QUALITY
        self.EXTERNAL_EVIRONMENT=EXTERNAL_EVIRONMENT
        self.CUI_PERCENT_3=CUI_PERCENT_3
        self.CUI_PERCENT_2=CUI_PERCENT_2
        self.CUI_PERCENT_4=CUI_PERCENT_4
        self.CUI_PERCENT_5=CUI_PERCENT_5
        self.CUI_PERCENT_6=CUI_PERCENT_6
        self.SUPPORT_COATING=SUPPORT_COATING
        self.INTERFACE_SOIL_WATER=INTERFACE_SOIL_WATER
        self.EXTERNAL_EXPOSED_FLUID_MIST=EXTERNAL_EXPOSED_FLUID_MIST
        self.CARBON_ALLOY=CARBON_ALLOY
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.MIN_OP_TEMP=MIN_OP_TEMP
        self.EXTERNAL_INSP_EFF=EXTERNAL_INSP_EFF
        self.EXTERNAL_INSP_NUM=EXTERNAL_INSP_NUM
        self.NoINSP_EXTERNAL=NoINSP_EXTERNAL
        self.APIComponentType=APIComponentType
        self.NomalThick=NomalThick
        self.CurrentThick=CurrentThick
        self.WeldJointEffciency=WeldJointEffciency
        self.YieldStrengthDesignTemp=YieldStrengthDesignTemp
        self.TensileStrengthDesignTemp=TensileStrengthDesignTemp
        self.ShapeFactor=ShapeFactor
        self.MINIUM_STRUCTURAL_THICKNESS_GOVERS=MINIUM_STRUCTURAL_THICKNESS_GOVERS
        self.CR_Confidents_Level=CR_Confidents_Level
        self.AllowableStress=AllowableStress
        self.MinThickReq=MinThickReq
        self.StructuralThickness=StructuralThickness
        # chua thay su dung Pressure
        self.Pressure = Pressure
        self.Diametter = Diametter
        self.AssesmentDate = AssesmentDate
        self.Commissiondate=Commissiondate
        self.ComponentNumber=ComponentNumber
    def AGE_CLSCC(self):
        try:
            print(self.AssesmentDate)
            print(self.COMPONENT_INSTALL_DATE)
            TICK_SPAN = abs((self.AssesmentDate.date() - self.COMPONENT_INSTALL_DATE.date()).days)
            print(TICK_SPAN)/365
            return TICK_SPAN / 365
        except Exception as e:
            print(e)
            return 0
        # if (self.EXTERN_COAT_QUALITY == "High coating quality"):
        #     AGE_COAT = self.COMPONENT_INSTALL_DATE + relativedelta(years=+15)  # Age + 15
        # elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
        #     AGE_COAT = self.COMPONENT_INSTALL_DATE + relativedelta(years=+5)  # Age + 5
        # else:
        #     AGE_COAT = self.COMPONENT_INSTALL_DATE
        # TICK_SPAN = abs((self.AssesmentDate.date() - AGE_COAT.date()).days)
        #TICK_SPAN = abs((self.AssesmentDate.date()-self.COMPONENT_INSTALL_DATE.date()).days)
        #return TICK_SPAN / 365

    def agetk(self, age):
        return age
    def AGE_CUI(self, age):#section 15.6.3: Step 5-6-7
        try:
            a=float(self.AGE_CLSCC())
            if (self.agetk(age) >= a):
                if (self.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a)
                elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a)
                else:
                    COAT = 0
            else:
                if (self.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a) - min(15, a - self.agetk(age))
                elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a) - min(5, a - self.agetk(age))
                else:
                    COAT = 0
            a=self.agetk(age) - COAT
            return a
        except Exception as e:
            print(e)

    def API_EXTERNAL_CORROSION_RATE(self):
        if (self.EXTERNAL_EVIRONMENT == "Arid/dry"):
            CR_EXTERN = (self.CUI_PERCENT_3+self.CUI_PERCENT_4+self.CUI_PERCENT_5)*0.025/100
        elif(self.EXTERNAL_EVIRONMENT=="Marine"):
            CR_EXTERN =(self.CUI_PERCENT_2*0.025+self.CUI_PERCENT_3*0.127+self.CUI_PERCENT_4*0.127+self.CUI_PERCENT_5*0.127+self.CUI_PERCENT_6*0.025)/100
        elif (self.EXTERNAL_EVIRONMENT == "Severe"):
            CR_EXTERN = (self.CUI_PERCENT_3*0.254+self.CUI_PERCENT_4*0.254+self.CUI_PERCENT_5*0.254+self.CUI_PERCENT_6*0.051)/100
        else:
            CR_EXTERN = (self.CUI_PERCENT_3*0.076+self.CUI_PERCENT_4*0.076+self.CUI_PERCENT_5*0.051)/100

        return CR_EXTERN

    def getalpha(self):
        return self.ShapeFactor
    def strengthRationMin(self):
        if self.MINIUM_STRUCTURAL_THICKNESS_GOVERS == False:
            return (self.Pressure * self.Diametter) / (self.getalpha() * self.FS_Thin() * self.trdi())
        else:
            return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(),
                                                                         self.StructuralThickness)) / (
                       self.FS_Thin() * self.trdi())

    def strengthRatioInter(self):
        return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(), self.StructuralThickness)) / (
        self.FS_Thin() * self.trdi())
    def FPS(self):
        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1
        return FPS
    def FIP(self):
        if (self.INTERFACE_SOIL_WATER):
            FIP = 1 #can xem lai, hien tai trong riskwise luon bang 1
        else:
            FIP = 1
        return FIP
    def CR(self):
        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1
        if (self.INTERFACE_SOIL_WATER):
            FIP = 1
        else:
            FIP = 1
        CR = self.API_EXTERNAL_CORROSION_RATE() * max(FPS, FIP)
        return CR

    def API_ART_EXTERNAL(self, age):
        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1
        if (self.INTERFACE_SOIL_WATER):
            FIP = 1
        else:
            FIP = 1
        CR = self.API_EXTERNAL_CORROSION_RATE() * max(FPS, FIP)

        try:
            ART_EXT = (CR*self.AGE_CUI(age))/self.trdi()
        except Exception as e:
            print(e)
            ART_EXT = 1
        return ART_EXT

    def ncdf(self,x):
        return 1. - 0.5 * math.erfc(x / (2 ** 0.5))

    def DF_EXTERNAL_CORROSION(self, age):
        if (self.EXTERNAL_EXPOSED_FLUID_MIST or (
        self.CARBON_ALLOY and not (self.MAX_OP_TEMP < -23 or self.MIN_OP_TEMP > 121))):
            self.EXTERNAL_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "External Corrosion")
            self.EXTERNAL_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "External Corrosion")
            self.NoINSP_EXTERNAL = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "External Corrosion")
        if (self.EXTERNAL_INSP_EFF == "" or self.EXTERNAL_INSP_NUM == 0):
            self.EXTERNAL_INSP_EFF = "E"
        if (self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType == "TANKROOFFLOAT0"):
            if (self.NomalThick == 0 or self.CurrentThick == 0 or self.WeldJointEffciency == 0 or(
             self.YieldStrengthDesignTemp == 0 and self.TensileStrengthDesignTemp == 0) or self.EXTERN_COAT_QUALITY == "" or (bool(self.COMPONENT_INSTALL_DATE) == False)):
                return 6500;
                # return 1390
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_512(self.API_ART(self.API_ART_EXTERNAL(age)), self.EXTERNAL_INSP_NUM,
                                                     self.EXTERNAL_INSP_EFF)
        else:
            if (self.NomalThick == 0 or self.CurrentThick == 0 or self.WeldJointEffciency== 0 or
            (self.YieldStrengthDesignTemp == 0 and self.TensileStrengthDesignTemp == 0) or self.EXTERN_COAT_QUALITY == "" or (bool(self.COMPONENT_INSTALL_DATE) == False)):
                return 6500;
            elif(self.APIComponentType =="TANKBOTTOM" and self.ShapeFactor==0.0 and self.MINIUM_STRUCTURAL_THICKNESS_GOVERS==False):#bổ sung trường hợp
                return 6500
            else:
                try:
                    a = self.Po_P1_EXTERNAL() * self.ncdf(- self.B1_EXTERNAL(age))
                    b = self.Po_P2_EXTERNAL() * self.ncdf(- self.B2_EXTERNAL(age))
                    c = self.Pr_P3_EXTERNAL() * self.ncdf(- self.B3_EXTERNAL(age))
                    return (a + b + c) / (1.56 * pow(10, -4))
                except Exception as e:
                    print(e)
                    return 0
        # else:
        #     return 0
    def Pr_P1_EXTERNAL(self):
        if self.CR_Confidents_Level == "Low":
            return 0.5
        elif self.CR_Confidents_Level == "Medium":
            return 0.7
        else:
            return 0.8
    def Pr_P2_EXTERNAL(self):
        if self.CR_Confidents_Level == "Low":
            return 0.3
        elif self.CR_Confidents_Level == "Medium":
            return 0.2
        else:
            return 0.15
    def Pr_P3_EXTERNAL(self):
        if self.CR_Confidents_Level == "Low":
            return 0.2
        elif self.CR_Confidents_Level == "Medium":
            return 0.1
        else:
            return  0.05

    def NA_EXTERNAL(self):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(self.ComponentNumber, 'External Corrosion')

        return a
    def NB_EXTERNAL(self):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(self.ComponentNumber, 'External Corrosion')

        return b
    def NC_EXTERNAL(self):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(self.ComponentNumber, 'External Corrosion')
        return c
    def ND_EXTERNAL(self):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(self.ComponentNumber, 'External Corrosion')
        return d
    def I1_EXTERNAL(self):
        a=self.Pr_P1_EXTERNAL() * pow(0.9,self.NA_EXTERNAL()) * pow(0.7,self.NB_EXTERNAL()) * pow(0.5,self.NC_EXTERNAL()) * pow(0.4,self.ND_EXTERNAL())
        return self.Pr_P1_EXTERNAL() * pow(0.9,self.NA_EXTERNAL()) * pow(0.7,self.NB_EXTERNAL()) * pow(0.5,self.NC_EXTERNAL()) * pow(0.4,self.ND_EXTERNAL())
    def I2_EXTERNAL(self):
        a=self.Pr_P2_EXTERNAL() * pow(0.09,self.NA_EXTERNAL()) * pow(0.2,self.NB_EXTERNAL()) * pow(0.3,self.NC_EXTERNAL()) * pow(0.33,self.ND_EXTERNAL())
        return self.Pr_P2_EXTERNAL() * pow(0.09,self.NA_EXTERNAL()) * pow(0.2,self.NB_EXTERNAL()) * pow(0.3,self.NC_EXTERNAL()) * pow(0.33,self.ND_EXTERNAL())
    def I3_EXTERNAL(self):
        a=self.Pr_P3_EXTERNAL() * pow(0.01,self.NA_EXTERNAL()) * pow(0.1,self.NB_EXTERNAL()) * pow(0.2,self.NC_EXTERNAL()) * pow(0.27,self.ND_EXTERNAL())
        return self.Pr_P3_EXTERNAL() * pow(0.01,self.NA_EXTERNAL()) * pow(0.1,self.NB_EXTERNAL()) * pow(0.2,self.NC_EXTERNAL()) * pow(0.27,self.ND_EXTERNAL())
    def Po_P1_EXTERNAL(self):
        a=self.I1_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
        return self.I1_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
    def Po_P2_EXTERNAL(self):
        a = self.I2_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
        return self.I2_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
    def Po_P3_EXTERNAL(self):
        a=self.I3_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
        return self.I3_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
    def getTmin(self):
        if self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType =="TANKROOFFLOAT0":
            if (self.ProtectedBarrier):
                #t = 2.54
                t=0.05
            else:
                #t = 1.27
                t=0.1
        else:
            t = self.MinThickReq
        return t
    def FS_Thin(self):
        return ((self.YieldStrengthDesignTemp + self.TensileStrengthDesignTemp)/2) * self.WeldJointEffciency * 1.1
    def trdi(self):
        return self.CurrentThick
    def SRp_Thin(self):
        if self.MINIUM_STRUCTURAL_THICKNESS_GOVERS == False:
            return (self.Pressure * self.Diametter) / (self.getalpha() * self.FS_Thin() * self.trdi())
        else:
            # return (self.WeldJointEffciency * self.TensileStrengthDesignTemp * max(self.getTmin(),self.StructuralThickness))/(self.FS_Thin() * self.trdi())
            # return (self.WeldJointEffciency * self.TensileStrengthDesignTemp * max(self.getTmin(),self.StructuralThickness))/(self.FS_Thin() * self.YieldStrengthDesignTemp)
            return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(), self.StructuralThickness)) / (
            self.FS_Thin() * self.trdi())
    def B1_EXTERNAL(self,age):
        return (1 - self.API_ART_EXTERNAL(age)- self.SRp_Thin())/math.sqrt(pow(self.API_ART_EXTERNAL(age), 2) * 0.04 + pow((1 - self.API_ART_EXTERNAL(age)), 2) * 0.04 + pow(self.SRp_Thin(), 2) * pow(0.05, 2))
    def B2_EXTERNAL(self,age):
        return (1- 2*self.API_ART_EXTERNAL(age)-self.SRp_Thin())/math.sqrt(pow(self.API_ART_EXTERNAL(age),2)*4*0.04 + pow(1-2*self.API_ART_EXTERNAL(age),2)*0.04+pow(self.SRp_Thin(),2)*pow(0.05,2))
    def B3_EXTERNAL(self,age):
        return (1- 4*self.API_ART_EXTERNAL(age)-self.SRp_Thin())/math.sqrt(pow(self.API_ART_EXTERNAL(age),2)*16*0.04 + pow(1-4*self.API_ART_EXTERNAL(age),2)*0.04+pow(self.SRp_Thin(),2)*pow(0.05,2))

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "External Corrosion", self.Commissiondate,
                                              self.AssesmentDate)
        return age
    def DF_EXTERNAL_CORROSION_API(self, i):
        return self.DF_EXTERNAL_CORROSION(self.GET_AGE() + i)
# Calculate CUI
class Df_CUI:
    def __init__(self,EXTERNAL_EVIRONMENT,CUI_PERCENT_2,CUI_PERCENT_3,CUI_PERCENT_4,CUI_PERCENT_5,CUI_PERCENT_6,CUI_PERCENT_7,CUI_PERCENT_8,CUI_PERCENT_9,INSULATION_TYPE,PIPING_COMPLEXITY,INSULATION_CONDITION,SUPPORT_COATING,INTERFACE_SOIL_WATER,EXTERNAL_EXPOSED_FLUID_MIST,CARBON_ALLOY,MAX_OP_TEMP,MIN_OP_TEMP,CUI_INSP_EFF,CUI_INSP_NUM,APIComponentType,NomalThick,CurrentThick,CR_Confidents_Level,MINIUM_STRUCTURAL_THICKNESS_GOVERS,WeldJointEffciency,YieldStrengthDesignTemp,TensileStrengthDesignTemp,AllowableStress,MinThickReq,StructuralThickness,Pressure,Diametter,ShapeFactor,COMPONENT_INSTALL_DATE,EXTERN_COAT_QUALITY,AssesmentDate,Commissiondate,ComponentNumber):
        self.EXTERNAL_EVIRONMENT=EXTERNAL_EVIRONMENT
        self.CUI_PERCENT_2=CUI_PERCENT_2
        self.CUI_PERCENT_3=CUI_PERCENT_3
        self.CUI_PERCENT_4=CUI_PERCENT_4
        self.CUI_PERCENT_5=CUI_PERCENT_5
        self.CUI_PERCENT_6=CUI_PERCENT_6
        self.CUI_PERCENT_7=CUI_PERCENT_7
        self.CUI_PERCENT_8=CUI_PERCENT_8
        self.CUI_PERCENT_9=CUI_PERCENT_9
        self.INSULATION_TYPE=INSULATION_TYPE
        self.PIPING_COMPLEXITY=PIPING_COMPLEXITY
        self.INSULATION_CONDITION=INSULATION_CONDITION
        self.SUPPORT_COATING=SUPPORT_COATING
        self.INTERFACE_SOIL_WATER=INTERFACE_SOIL_WATER
        self.EXTERNAL_EXPOSED_FLUID_MIST=EXTERNAL_EXPOSED_FLUID_MIST
        self.CARBON_ALLOY=CARBON_ALLOY
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.MIN_OP_TEMP=MIN_OP_TEMP
        self.CUI_INSP_EFF=CUI_INSP_EFF
        self.CUI_INSP_NUM=CUI_INSP_NUM
        self.APIComponentType=APIComponentType
        self.NomalThick=NomalThick
        self.CurrentThick=CurrentThick
        self.CR_Confidents_Level=CR_Confidents_Level
        self.MINIUM_STRUCTURAL_THICKNESS_GOVERS=MINIUM_STRUCTURAL_THICKNESS_GOVERS
        self.WeldJointEffciency=WeldJointEffciency
        self.YieldStrengthDesignTemp=YieldStrengthDesignTemp
        self.TensileStrengthDesignTemp=TensileStrengthDesignTemp
        self.AllowableStress=AllowableStress
        self.MinThickReq=MinThickReq
        self.StructuralThickness=StructuralThickness
        self.Pressure=Pressure
        self.Diametter=Diametter
        self.ShapeFactor=ShapeFactor
        self.COMPONENT_INSTALL_DATE=COMPONENT_INSTALL_DATE
        self.EXTERN_COAT_QUALITY=EXTERN_COAT_QUALITY
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def ncdf(self,x):
        return 1. - 0.5 * math.erfc(x / (2 ** 0.5))
    def API_CORROSION_RATE(self):
        if (self.EXTERNAL_EVIRONMENT == "Arid/dry"):
            CR_CUI = (
                     self.CUI_PERCENT_3 * 0.025 + self.CUI_PERCENT_4 * 0.025 + self.CUI_PERCENT_5 * 0.051 + self.CUI_PERCENT_6 * 0.025) / 100
        elif (self.EXTERNAL_EVIRONMENT == "Marine"):
            CR_CUI = (
                     self.CUI_PERCENT_2 * 0.025 + self.CUI_PERCENT_3 * 0.127 + self.CUI_PERCENT_4 * 0.127 + self.CUI_PERCENT_5 * 0.254 + self.CUI_PERCENT_6 * 0.127 + self.CUI_PERCENT_7 * 0.051 + self.CUI_PERCENT_8 * 0.051 + self.CUI_PERCENT_9 * 0.025) / 100
        elif (self.EXTERNAL_EVIRONMENT == "Severe"):
            CR_CUI = (
                     self.CUI_PERCENT_2 * 0.076 + self.CUI_PERCENT_3 * 0.254 + self.CUI_PERCENT_4 * 0.254 + self.CUI_PERCENT_5 * 0.508 + self.CUI_PERCENT_6 * 0.254 + self.CUI_PERCENT_7 * 0.254 + self.CUI_PERCENT_8 * 0.254 + self.CUI_PERCENT_9 * 0.127) / 100
        else:
            CR_CUI = (
                     self.CUI_PERCENT_3 * 0.076 + self.CUI_PERCENT_4 * 0.076 + self.CUI_PERCENT_5 * 0.127 + self.CUI_PERCENT_6 * 0.025 + self.CUI_PERCENT_7 * 0.025) / 100
        return CR_CUI
    def API_ART(self, a):
        if self.APIComponentType == 'TANKBOTTOM0' or self.APIComponentType == 'TANKROOFFLOAT0':
            data = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9,
                    0.95, 1]
            if a < (data[0] + data[1]) / 2:
            #if 0.025 < a < (data[0] + data[1]) / 2:
                return data[0]
            elif (a < (data[1] + data[2]) / 2):
                return data[1]
            elif (a < (data[2] + data[3]) / 2):
                return data[2]
            elif (a < (data[3] + data[4]) / 2):
                return data[3]
            elif (a < (data[4] + data[5]) / 2):
                return data[4]
            elif (a < (data[5] + data[6]) / 2):
                return data[5]
            elif (a < (data[6] + data[7]) / 2):
                return data[6]
            elif (a < (data[7] + data[8]) / 2):
                return data[7]
            elif (a < (data[8] + data[9]) / 2):
                return data[8]
            elif (a < (data[9] + data[10]) / 2):
                return data[9]
            elif (a < (data[10] + data[11]) / 2):
                return data[10]
            elif (a < (data[11] + data[12]) / 2):
                return data[11]
            elif (a < (data[12] + data[13]) / 2):
                return data[12]
            elif (a < (data[13] + data[14]) / 2):
                return data[13]
            elif (a < (data[14] + data[15]) / 2):
                return data[14]
            elif (a < (data[15] + data[16]) / 2):
                return data[15]
            elif (a < (data[16] + data[17]) / 2):
                return data[16]
            elif (a < (data[17] + data[18]) / 2):
                return data[17]
            elif (a < (data[18] + data[19]) / 2):
                return data[18]
            else:
                return data[19]
        else:
            return a
    def getTmin(self):
        if self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType =="TANKROOFFLOAT0":
            if (self.ProtectedBarrier):
                #t = 2.54
                t=0.05
            else:
                #t = 1.27
                t=0.1
        else:
            t = self.MinThickReq
        return t
    def getalpha(self):
        return self.ShapeFactor
    def FS_Thin(self):
        return ((self.YieldStrengthDesignTemp + self.TensileStrengthDesignTemp)/2) * self.WeldJointEffciency * 1.1
    def trdi(self):
        return self.CurrentThick
    def SRp_Thin(self):
        if self.MINIUM_STRUCTURAL_THICKNESS_GOVERS == False:
            return (self.Pressure * self.Diametter) / (self.getalpha() * self.FS_Thin() * self.trdi())
        else:
            # return (self.WeldJointEffciency * self.TensileStrengthDesignTemp * max(self.getTmin(),self.StructuralThickness))/(self.FS_Thin() * self.trdi())
            # return (self.WeldJointEffciency * self.TensileStrengthDesignTemp * max(self.getTmin(),self.StructuralThickness))/(self.FS_Thin() * self.YieldStrengthDesignTemp)
            return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(), self.StructuralThickness)) / (
            self.FS_Thin() * self.trdi())
    def strengthRationMin(self):
        return (self.Pressure * self.Diametter) / (self.getalpha() * self.FS_Thin() * self.trdi())
    def strengthRatioInter(self):
        return (self.WeldJointEffciency * self.AllowableStress * max(self.getTmin(), self.StructuralThickness)) / (self.FS_Thin() * self.trdi())
    def INS(self):
        if (
                            self.INSULATION_TYPE == "Asbestos" or self.INSULATION_TYPE == "Calcium Silicate" or self.INSULATION_TYPE == "Mineral Wool" or self.INSULATION_TYPE == "Fibreglass" or self.INSULATION_TYPE == "Unknown/Unspecified"):
            FIN = 1.25
        elif (self.INSULATION_TYPE == "Foam Glass"):
            FIN = 0.75
        else:
            FIN = 1
        return  FIN
    def FIC(self):
        if (self.INSULATION_CONDITION == "Below average"):
            FIC = 1.25
        elif (self.INSULATION_CONDITION == "Above average"):
            FIC = 0.75
        else:
            FIC = 1
        return FIC
    def FCM(self):
        if (self.PIPING_COMPLEXITY == "Below average"):
            FCM = 0.75
        elif (self.PIPING_COMPLEXITY == "Above average"):
            FCM = 1.75
        else:
            FCM = 1
        return FCM
    def FPS(self):
        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1
        return FPS
    def FIP(self):
        if (self.INTERFACE_SOIL_WATER):
            FIP = 2
        else:
            FIP = 1
        return FIP
    def CR(self):
        if (
                            self.INSULATION_TYPE == "Asbestos" or self.INSULATION_TYPE == "Calcium Silicate" or self.INSULATION_TYPE == "Mineral Wool" or self.INSULATION_TYPE == "Fibreglass" or self.INSULATION_TYPE == "Unknown/Unspecified"):
            FIN = 1.25
        elif (self.INSULATION_TYPE == "Foam Glass"):
            FIN = 0.75
        else:
            FIN = 1

        if (self.PIPING_COMPLEXITY == "Below average"):
            FCM = 0.75
        elif (self.PIPING_COMPLEXITY == "Above average"):
            FCM = 1.75
        else:
            FCM = 1

        if (self.INSULATION_CONDITION == "Below average"):
            FIC = 1.25
        elif (self.INSULATION_CONDITION == "Above average"):
            FIC = 0.75
        else:
            FIC = 1

        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1

        if (self.INTERFACE_SOIL_WATER):
            FIP = 2
        else:
            FIP = 1

        CR = self.API_CORROSION_RATE() * FIN * FCM * FIC * max(FPS, FIP)
        return CR
    def API_ART_CUI(self, age):
        if (
                            self.INSULATION_TYPE == "Asbestos" or self.INSULATION_TYPE == "Calcium Silicate" or self.INSULATION_TYPE == "Mineral Wool" or self.INSULATION_TYPE == "Fibreglass" or self.INSULATION_TYPE == "Unknown/Unspecified"):
            FIN = 1.25
        elif (self.INSULATION_TYPE == "Foam Glass"):
            FIN = 0.75
        else:
            FIN = 1

        if (self.PIPING_COMPLEXITY == "Below average"):
            FCM = 0.75
        elif (self.PIPING_COMPLEXITY == "Above average"):
            FCM = 1.75
        else:
            FCM = 1

        if (self.INSULATION_CONDITION == "Below average"):
            FIC = 1.25
        elif (self.INSULATION_CONDITION == "Above average"):
            FIC = 0.75
        else:
            FIC = 1

        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1

        if (self.INTERFACE_SOIL_WATER):
            FIP = 2
        else:
            FIP = 1

        CR = self.API_CORROSION_RATE() * FIN * FCM * FIC * max(FPS, FIP)
        try:
            # ART_CUI = max(1 - (self.CurrentThick - CR * self.AGE_CUI(age)) / (self.getTmin() + self.CA), 0)
            ART_CUI = (CR * self.AGE_CUI(age)) / self.trdi()
        except:
            ART_CUI = 1
        return self.API_ART(ART_CUI)

    def agetk(self, age):
        return age
    def AGE_CLSCC(self):
        try:
            TICK_SPAN = abs((self.AssesmentDate.date() - self.COMPONENT_INSTALL_DATE.date()).days)
            return TICK_SPAN / 365
        except Exception as e:
            print(e)
    def AGE_CUI(self, age):#section 15.6.3: Step 5-6-7
        try:
            a=float(self.AGE_CLSCC())
            if (self.agetk(age) >= a):
                if (self.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a)
                elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a)
                else:
                    COAT = 0
            else:
                if (self.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a) - min(15, a - self.agetk(age))
                elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a) - min(5, a - self.agetk(age))
                else:
                    COAT = 0
            a=self.agetk(age) - COAT
            return a
        except Exception as e:
            print(e)

    def NA_FERRITIC(self):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(self.ComponentNumber, "Corrosion Under Insulation")
        return a

    def NB_FERRITIC(self):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(self.ComponentNumber, "Corrosion Under Insulation")
        return b

    def NC_FERRITIC(self):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(self.ComponentNumber, "Corrosion Under Insulation")
        return c

    def ND_FERRITIC(self):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(self.ComponentNumber, "Corrosion Under Insulation")
        return d
    def Pr_P1_EXTERNAL(self):
        if self.CR_Confidents_Level == "Low":
            return 0.5
        elif self.CR_Confidents_Level == "Medium":
            return 0.7
        else:
            return 0.8
    def Pr_P2_EXTERNAL(self):
        if self.CR_Confidents_Level == "Low":
            return 0.3
        elif self.CR_Confidents_Level == "Medium":
            return 0.2
        else:
            return 0.15
    def Pr_P3_EXTERNAL(self):
        if self.CR_Confidents_Level == "Low":
            return 0.2
        elif self.CR_Confidents_Level == "Medium":
            return 0.1
        else:
            return  0.05
    def I1_FERRITIC(self):
        a = self.Pr_P1_EXTERNAL() * pow(0.9, self.NA_FERRITIC()) * pow(0.7, self.NB_FERRITIC()) * pow(0.5,
                                                                                                      self.NC_FERRITIC()) * pow(
            0.4, self.ND_FERRITIC())
        return self.Pr_P1_EXTERNAL() * pow(0.9, self.NA_FERRITIC()) * pow(0.7, self.NB_FERRITIC()) * pow(0.5,
                                                                                                         self.NC_FERRITIC()) * pow(
            0.4, self.ND_FERRITIC())

    def I2_FERRITIC(self):
        a = self.Pr_P2_EXTERNAL() * pow(0.09, self.NA_FERRITIC()) * pow(0.2, self.NB_FERRITIC()) * pow(0.3,
                                                                                                       self.NC_FERRITIC()) * pow(
            0.33, self.ND_FERRITIC())
        return self.Pr_P2_EXTERNAL() * pow(0.09, self.NA_FERRITIC()) * pow(0.2, self.NB_FERRITIC()) * pow(0.3,
                                                                                                          self.NC_FERRITIC()) * pow(
            0.33, self.ND_FERRITIC())

    def I3_FERRITIC(self):
        a = self.Pr_P3_EXTERNAL() * pow(0.01, self.NA_FERRITIC()) * pow(0.1, self.NB_FERRITIC()) * pow(0.2,
                                                                                                       self.NC_FERRITIC()) * pow(
            0.27, self.ND_FERRITIC())
        return self.Pr_P3_EXTERNAL() * pow(0.01, self.NA_FERRITIC()) * pow(0.1, self.NB_FERRITIC()) * pow(0.2,
                                                                                                          self.NC_FERRITIC()) * pow(
            0.27, self.ND_FERRITIC())

    def Po_P1_FERRITIC(self):
        return self.I1_FERRITIC() / (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())
        # return (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())

    def Po_P2_FERRITIC(self):
        return self.I2_FERRITIC() / (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())

    def Po_P3_FERRITIC(self):
        return self.I3_FERRITIC() / (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())

    def B1_FERRITIC(self, age):
        a = (1 - self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 0.04 + pow((1 - self.API_ART_CUI(age)), 2) * 0.04 + pow(self.SRp_Thin(),
                                                                                                    2) * pow(0.05,
                                                                                                             2))
        return (1 - self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 0.04 + pow((1 - self.API_ART_CUI(age)), 2) * 0.04 + pow(self.SRp_Thin(),
                                                                                                    2) * pow(0.05,
                                                                                                             2))

    def B2_FERRITIC(self, age):
        b = (1 - 2 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 4 * 0.04 + pow(1 - 2 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))
        return (1 - 2 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 4 * 0.04 + pow(1 - 2 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))

    def B3_FERRITIC(self, age):
        c = (1 - 4 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 16 * 0.04 + pow(1 - 4 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))
        return (1 - 4 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 16 * 0.04 + pow(1 - 4 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))

    def DF_CUI(self, age):
        if (self.EXTERNAL_EXPOSED_FLUID_MIST or (
                    self.CARBON_ALLOY and not (self.MAX_OP_TEMP < -12 or self.MIN_OP_TEMP > 177))):
            self.CUI_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Corrosion Under Insulation")
            self.CUI_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "Corrosion Under Insulation")
            if (self.CUI_INSP_EFF == "" or self.CUI_INSP_NUM == 0):
                self.CUI_INSP_EFF = "E"
            if (self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType == "TANKROOFFLOAT0"):
                if (self.NomalThick == 0 or self.CurrentThick == 0):
                    return 1390
                else:
                    return DAL_CAL.POSTGRESQL.GET_TBL_512(self.API_ART(self.API_ART_CUI(age)), self.CUI_INSP_NUM,
                                                          self.CUI_INSP_EFF)
            else:
                if (self.NomalThick == 0 or self.CurrentThick == 0):
                    return 1900
                else:
                    try:
                        a = self.Po_P1_FERRITIC() * self.ncdf(- self.B1_FERRITIC(age))
                        b = self.Po_P2_FERRITIC() * self.ncdf(- self.B2_FERRITIC(age))
                        c = self.Po_P3_FERRITIC() * self.ncdf(- self.B3_FERRITIC(age))
                        s = (a + b + c) / (1.56 * pow(10, -4))
                        return (a + b + c) / (1.56 * pow(10, -4))
                    except Exception as e:
                        print(e)
                        return 0
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Corrosion Under Insulation", self.Commissiondate,
                                              self.AssesmentDate)
        return age
    def DF_CUI_API(self, i):
        return self.DF_CUI(self.GET_AGE() + i)

 # cal EXTERNAL CLSCC
class Df_EXTERN_CLSCC:
    def __init__(self,CRACK_PRESENT,EXTERNAL_EVIRONMENT,MAX_OP_TEMP,EXTERN_CLSCC_INSP_EFF,EXTERN_CLSCC_INSP_NUM,AUSTENITIC_STEEL,EXTERNAL_EXPOSED_FLUID_MIST,MIN_DESIGN_TEMP,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT=CRACK_PRESENT
        self.EXTERNAL_EVIRONMENT=EXTERNAL_EVIRONMENT
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.EXTERN_CLSCC_INSP_EFF=EXTERN_CLSCC_INSP_EFF
        self.EXTERN_CLSCC_INSP_NUM=EXTERN_CLSCC_INSP_NUM
        self.AUSTENITIC_STEEL=AUSTENITIC_STEEL
        self.EXTERNAL_EXPOSED_FLUID_MIST=EXTERNAL_EXPOSED_FLUID_MIST
        self.MIN_DESIGN_TEMP=MIN_DESIGN_TEMP
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def CLSCC_SUSCEP(self):
        if (self.CRACK_PRESENT):
            sus = "High"
        else:
            if (self.EXTERNAL_EVIRONMENT == "Arid/dry"):
                sus = "Not"
            elif (self.EXTERNAL_EVIRONMENT == "Marine"):
                if (self.MAX_OP_TEMP < 49 or self.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (self.MAX_OP_TEMP >= 49 and self.MAX_OP_TEMP < 93):
                    sus = "Medium"
                else:
                    sus = "Low"
            elif (self.EXTERNAL_EVIRONMENT == "Severe"):
                if (self.MAX_OP_TEMP < 49 or self.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (self.MAX_OP_TEMP >= 49 and self.MAX_OP_TEMP < 93):
                    sus = "High"
                else:
                    sus = "Medium"
            elif (self.EXTERNAL_EVIRONMENT == "Temperate"):
                if (self.MAX_OP_TEMP < 49 or self.MAX_OP_TEMP > 149):
                    sus = "Not"
                else:
                    sus = "Low"
            else:
                sus = "Not"
        return sus
    def SVI(self):
        sus = self.CLSCC_SUSCEP()
        if (sus == "High"):
            SVI = 50
        elif (sus == "Medium"):
            SVI = 10
        elif (sus == "Low"):
            SVI = 1
        else:
            SVI = 0
        return SVI
    def DFB_EXTERN_CLSCC(self):
        sus = self.CLSCC_SUSCEP()
        if (sus == "High"):
            SVI = 50
        elif (sus == "Medium"):
            SVI = 10
        elif(sus == "Low"):
            SVI = 1
        else:
            SVI=0
        self.EXTERN_CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber,"External Chloride Stress Corrosion Cracking")
        self.EXTERN_CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, "External Chloride Stress Corrosion Cracking")
        if (self.EXTERN_CLSCC_INSP_EFF == "E" or self.EXTERN_CLSCC_INSP_NUM == 0):
            FIELD = "E"
        else:
            FIELD = str(self.EXTERN_CLSCC_INSP_NUM) + self.EXTERN_CLSCC_INSP_EFF
        return DAL_CAL.POSTGRESQL.GET_TBL_74(SVI, FIELD)
    def DFB_EXTERN_CLSCC(self, age):
        if (self.AUSTENITIC_STEEL and self.EXTERNAL_EXPOSED_FLUID_MIST and not (
                self.MAX_OP_TEMP < 49 or self.MIN_DESIGN_TEMP > 149)):
            if(age<1):
                return self.DFB_EXTERN_CLSCC(age)
            else:
                return self.DFB_EXTERN_CLSCC(age)
        else:
            return 0
    def DF_EXTERN_CLSCC(self, age):
        if (self.AUSTENITIC_STEEL and self.EXTERNAL_EXPOSED_FLUID_MIST and not (
                self.MAX_OP_TEMP < 49 or self.MIN_DESIGN_TEMP > 149)):
            if(age<1):
                return self.DFB_EXTERN_CLSCC(age)
            else:
                return self.DFB_EXTERN_CLSCC(age) * pow(self.AGE_CUI(age), 1.1)
        else:
            return 0
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "External Chloride Stress Corrosion Cracking", self.Commissiondate,
                                              self.AssesmentDate)
        return age
    def DBF_EXTERN_CLSCC_API(self, i):
        return self.DFB_EXTERN_CLSCC(self.GET_AGE() + i)
    def DF_EXTERN_CLSCC_API(self, i):
        return self.DF_EXTERN_CLSCC(self.GET_AGE() + i)
# Calculate EXTERN CUI CLSCC
class Df_CUI_CLSCC:
    def __init__(self,CRACK_PRESENT,EXTERNAL_EVIRONMENT,MAX_OP_TEMP,PIPING_COMPLEXITY,INSULATION_CONDITION,INSULATION_CHLORIDE,EXTERN_CLSCC_CUI_INSP_EFF,EXTERN_CLSCC_CUI_INSP_NUM,AUSTENITIC_STEEL,EXTERNAL_INSULATION,EXTERNAL_EXPOSED_FLUID_MIST,MIN_OP_TEMP,EXTERN_COAT_QUALITY,AssesmentDate,Commissiondate,ComponentNumber):
        self.CRACK_PRESENT = CRACK_PRESENT
        self.EXTERNAL_EVIRONMENT = EXTERNAL_EVIRONMENT
        self.MAX_OP_TEMP = MAX_OP_TEMP
        self.PIPING_COMPLEXITY = PIPING_COMPLEXITY
        self.INSULATION_CONDITION = INSULATION_CONDITION
        self.INSULATION_CHLORIDE = INSULATION_CHLORIDE
        self.EXTERN_CLSCC_CUI_INSP_EFF = EXTERN_CLSCC_CUI_INSP_EFF
        self.EXTERN_CLSCC_CUI_INSP_NUM = EXTERN_CLSCC_CUI_INSP_NUM
        self.AUSTENITIC_STEEL = AUSTENITIC_STEEL
        self.EXTERNAL_INSULATION = EXTERNAL_INSULATION
        self.EXTERNAL_EXPOSED_FLUID_MIST = EXTERNAL_EXPOSED_FLUID_MIST
        self.MIN_OP_TEMP = MIN_OP_TEMP
        # chua thay su dung EXTERN_COAT_QUALITY
        self.EXTERN_COAT_QUALITY = EXTERN_COAT_QUALITY
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def CUI_CLSCC_SUSCEP(self):
        if (self.CRACK_PRESENT):
            sus = "High"
        else:
            if (self.EXTERNAL_EVIRONMENT == "Arid/dry"):
                if (self.MAX_OP_TEMP >= 49 and self.MAX_OP_TEMP < 93):
                    sus = "Low"
                else:
                    sus = "Not"
            elif (self.EXTERNAL_EVIRONMENT == "Marine"):
                if (self.MAX_OP_TEMP < 49 or self.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (self.MAX_OP_TEMP >= 49 and self.MAX_OP_TEMP < 93):
                    sus = "High"
                else:
                    sus = "Medium"
            elif (self.EXTERNAL_EVIRONMENT == "Severe"):
                if (self.MAX_OP_TEMP < 49 or self.MAX_OP_TEMP > 149):
                    sus = "Not"
                else:
                    sus = "High"
            elif (self.EXTERNAL_EVIRONMENT == "Temperate"):
                if (self.MAX_OP_TEMP < 49 or self.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (self.MAX_OP_TEMP >= 49 and self.MAX_OP_TEMP < 93):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                sus = "Not"
        return sus

    def ADJUST_COMPLEXITY(self):
        SCP = self.CUI_CLSCC_SUSCEP()
        if (SCP == "High"):
            if (self.PIPING_COMPLEXITY == "Below average"):
                SCP = "Medium"
            else:
                SCP = "High"
        elif (SCP == "Medium"):
            if (self.PIPING_COMPLEXITY == "Below average"):
                SCP = "Low"
            elif (self.PIPING_COMPLEXITY == "Above average"):
                SCP = "High"
            else:
                SCP = "Medium"
        else:
            if (self.PIPING_COMPLEXITY == "Above average"):
                SCP = "Medium"
            else:
                SCP = "Low"
        return SCP

    def ADJUST_ISULATION(self):
        SCP = self.ADJUST_COMPLEXITY()
        if (SCP == "High"):
            if (self.INSULATION_CONDITION == "Above average"):
                SCP = "Medium"
            else:
                SCP = "High"
        elif (SCP == "Medium"):
            if (self.INSULATION_CONDITION == "Above average"):
                SCP = "Low"
            elif (self.INSULATION_CONDITION == "Below average"):
                SCP = "High"
            else:
                SCP = "Medium"
        else:
            if (self.INSULATION_CONDITION == "Below average"):
                SCP = "Medium"
            else:
                SCP = "Low"
        return SCP

    def ADJUST_CHLORIDE_INSULATION(self):
        SCP = self.ADJUST_ISULATION()
        if (self.INSULATION_CHLORIDE):
            if (SCP == "High"):
                SCP = "Medium"
            elif (SCP == "Medium"):
                SCP = "Low"
            else:
                SCP = "Low"
        else:
            SCP = self.ADJUST_ISULATION()
        return SCP

    def agetk(self, age):
        return age
    def AGE_CLSCC(self):
        try:
            TICK_SPAN = abs((self.AssesmentDate.date() - self.COMPONENT_INSTALL_DATE.date()).days)
            return TICK_SPAN / 365
        except Exception as e:
            print(e)
    def AGE_CUI(self, age):#section 15.6.3: Step 5-6-7
        try:
            a=float(self.AGE_CLSCC())
            if (self.agetk(age) >= a):
                if (self.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a)
                elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a)
                else:
                    COAT = 0
            else:
                if (self.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a) - min(15, a - self.agetk(age))
                elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a) - min(5, a - self.agetk(age))
                else:
                    COAT = 0
            a=self.agetk(age) - COAT
            return a
        except Exception as e:
            print(e)
    def SVI(self):
        SCP = self.ADJUST_CHLORIDE_INSULATION()
        if (SCP == "High"):
            SVI = 50
        elif (SCP == "Medium"):
            SVI = 10
        elif (SCP == "Low"):
            SVI = 1
        else:
            SVI = 0
        return SVI
    def DFB_CUI_CLSCC(self,age):
        SCP = self.ADJUST_CHLORIDE_INSULATION()
        if (SCP == "High"):
            SVI = 50
        elif (SCP == "Medium"):
            SVI = 10
        elif(SCP == "Low"):
            SVI = 1
        else:
            SVI = 0
        try:
            self.EXTERN_CLSCC_CUI_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, "Chloride Stress Corrosion Cracking Under Insulation")
            self.EXTERN_CLSCC_CUI_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,"Chloride Stress Corrosion Cracking Under Insulation")

            if (self.EXTERN_CLSCC_CUI_INSP_EFF == "E" or self.EXTERN_CLSCC_CUI_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.EXTERN_CLSCC_CUI_INSP_NUM) + self.EXTERN_CLSCC_CUI_INSP_EFF
            return DAL_CAL.POSTGRESQL.GET_TBL_74(SVI, FIELD)
        except Exception as e:
            print(e)
            return 0

    def DF_CUI_CLSCC(self,age):
        # if not self.EXTERN_COATING:
        #     return 0
        if (self.AUSTENITIC_STEEL and self.EXTERNAL_INSULATION and self.EXTERNAL_EXPOSED_FLUID_MIST and not (
                self.MIN_OP_TEMP > 150 or self.MAX_OP_TEMP < 50)):
            if(age<1):
                return self.DFB_CUI_CLSCC()
            else:
                return self.DFB_CUI_CLSCC() * pow(self.AGE_CUI(age), 1.1)
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Chloride Stress Corrosion Cracking Under Insulation", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DFB_CUI_CLSCC_API(self, i):
        return self.DFB_CUI_CLSCC(self.GET_AGE() + i)
    def DF_CUI_CLSCC_API(self, i):
        return self.DF_CUI_CLSCC(self.GET_AGE() + i)
# Calculate HTHA
class DF_HTHA:
    def __init__(self,HTHA_PRESSURE,CRITICAL_TEMP,HTHADamageObserved,MAX_OP_TEMP,MATERIAL_SUSCEP_HTHA,HTHA_MATERIAL,Hydrogen,AssesmentDate,Commissiondate,ComponentNumber):
        self.HTHA_PRESSURE = HTHA_PRESSURE
        self.CRITICAL_TEMP = CRITICAL_TEMP
        self.HTHADamageObserved = HTHADamageObserved
        self.MAX_OP_TEMP = MAX_OP_TEMP
        self.MATERIAL_SUSCEP_HTHA = MATERIAL_SUSCEP_HTHA
        self.HTHA_MATERIAL = HTHA_MATERIAL
        self.Hydrogen = Hydrogen
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def HTHA_PV(self, age):
        try:
            HTHA_AGE = age * 24 * 365
            log1 = math.log10(self.HTHA_PRESSURE / 0.0979)
            log2 = 3.09 * pow(10, -4) * (self.CRITICAL_TEMP + 273) * (math.log10(HTHA_AGE) + 14)
            return log1 + log2
        except:
            return 0
    def delta(self):
        HTHA_PRESSURE_psia = self.HTHA_PRESSURE * 145;
        dataT = self.MAX_OP_TEMP * 9 / 5 + 32;
        TemperatureAdjusted = dataT +20
        deltaT = 0;
        if (self.MATERIAL_SUSCEP_HTHA == True):
            if (
                        self.HTHA_MATERIAL == "Carbon Steel" or self.HTHA_MATERIAL == "C-0.5Mo (Annealed)" or self.HTHA_MATERIAL == "C-0.5Mo (Normalised)"):
                if (self.MAX_OP_TEMP > 177 and self.HTHA_PRESSURE >= 0.345):
                    SUSCEP = "High"
                else:
                    SUSCEP = "No"
            if (self.HTHA_MATERIAL == "1Cr-0.5Mo"):
                if (HTHA_PRESSURE_psia >= 50.0 and HTHA_PRESSURE_psia < 700.0):
                    deltaT = TemperatureAdjusted - ((-0.2992 * HTHA_PRESSURE_psia) + 1100.0)
                elif ((HTHA_PRESSURE_psia >= 700.0) and (HTHA_PRESSURE_psia < 1250.0)):
                    deltaT = (TemperatureAdjusted - 905.0)
                elif ((HTHA_PRESSURE_psia >= 1250.0) and (HTHA_PRESSURE_psia < 1800.0)):
                    deltaT = (TemperatureAdjusted - (1171.11 * pow(HTHA_PRESSURE_psia - 1215.03, -0.092)))
                elif ((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 2600.0)):
                    deltaT = (TemperatureAdjusted - (
                    ((4E-05 * pow(HTHA_PRESSURE_psia, 2.0)) - (0.2042 * HTHA_PRESSURE_psia)) + 903.69));
                elif ((HTHA_PRESSURE_psia >= 2600.0) and (HTHA_PRESSURE_psia < 13000.0)):
                    deltaT = (TemperatureAdjusted - 625.0);
            if (self.HTHA_MATERIAL == "1.25Cr-0.5Mo"):
                if ((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1250.0)):
                    deltaT = (TemperatureAdjusted - ((-0.1668 * HTHA_PRESSURE_psia) + 1150.0))
                elif ((HTHA_PRESSURE_psia >= 1250.0) and (HTHA_PRESSURE_psia < 1800.0)):
                    deltaT = (TemperatureAdjusted - (1171.11 * pow(HTHA_PRESSURE_psia - 1215.03, -0.092)))
                elif ((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 2600.0)):
                    deltaT = (TemperatureAdjusted - (
                    ((4E-05 * pow(HTHA_PRESSURE_psia, 2.0)) - (0.2042 * HTHA_PRESSURE_psia)) + 903.69))
                elif ((HTHA_PRESSURE_psia >= 2600.0) and (HTHA_PRESSURE_psia < 13000.0)):
                    deltaT = (TemperatureAdjusted - 625.0)
            if (self.HTHA_MATERIAL == "2.25Cr-1Mo"):
                if ((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 2000.0)):
                    deltaT = (TemperatureAdjusted - ((-0.1701 * HTHA_PRESSURE_psia) + 1200.0))
                elif ((HTHA_PRESSURE_psia >= 2000.0) and (HTHA_PRESSURE_psia < 6000.0)):
                    deltaT = (TemperatureAdjusted - 855.0)
                elif (self.HTHA_MATERIAL == "3Cr-1Mo"):
                    if ((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1800.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1659 * HTHA_PRESSURE_psia) + 1250.0))
                    elif ((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 6000.0)):
                        deltaT = (TemperatureAdjusted - 950.0)
            if (self.HTHA_MATERIAL == "6Cr-0.5Mo"):
                if ((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1100.0)):
                    deltaT = (TemperatureAdjusted - ((-0.1254 * HTHA_PRESSURE_psia) + 1300.0))
                elif ((HTHA_PRESSURE_psia >= 1100.0) and (HTHA_PRESSURE_psia < 6000.0)):
                    deltaT = (TemperatureAdjusted - 1120.0)
        return deltaT
    def HTHA_SUSCEP(self, age):
        SUSCEP = ""
        if (self.HTHADamageObserved == 1):
            if (self.MAX_OP_TEMP > 177 and self.HTHA_PRESSURE >= 0.345):
                SUSCEP = "High"
            else:
                SUSCEP = "No"
        else:
            HTHA_PRESSURE_psia = self.HTHA_PRESSURE * 145;
            TemperatureAdjusted = self.MAX_OP_TEMP * 9 / 5 + 32;
            deltaT = 0;
            if (self.MATERIAL_SUSCEP_HTHA== True):
                if(self.HTHA_MATERIAL == "Carbon Steel" or self.HTHA_MATERIAL=="C-0.5Mo (Annealed)" or self.HTHA_MATERIAL=="C-0.5Mo (Normalised)"):
                    if (self.MAX_OP_TEMP > 177 and self.HTHA_PRESSURE >= 0.345):
                        SUSCEP = "High"
                    else:
                        SUSCEP = "No"
                if(self.HTHA_MATERIAL=="1Cr-0.5Mo"):
                    if (HTHA_PRESSURE_psia >= 50.0 and HTHA_PRESSURE_psia < 700.0):
                        deltaT = TemperatureAdjusted - ((-0.2992 * HTHA_PRESSURE_psia) + 1100.0)
                    elif((HTHA_PRESSURE_psia >= 700.0) and (HTHA_PRESSURE_psia < 1250.0)):
                        deltaT = (TemperatureAdjusted - 905.0)
                    elif ((HTHA_PRESSURE_psia >= 1250.0) and (HTHA_PRESSURE_psia < 1800.0)):
                        deltaT = (TemperatureAdjusted - (1171.11 * pow(HTHA_PRESSURE_psia - 1215.03, -0.092)))
                    elif ((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 2600.0)):
                        deltaT = (TemperatureAdjusted - (((4E-05 * pow(HTHA_PRESSURE_psia, 2.0)) - (0.2042 * HTHA_PRESSURE_psia)) + 903.69));
                    elif ((HTHA_PRESSURE_psia >= 2600.0) and (HTHA_PRESSURE_psia < 13000.0)):
                        deltaT = (TemperatureAdjusted - 625.0);
                if(self.HTHA_MATERIAL=="1.25Cr-0.5Mo"):
                    if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1250.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1668 * HTHA_PRESSURE_psia) + 1150.0))
                    elif((HTHA_PRESSURE_psia >= 1250.0) and (HTHA_PRESSURE_psia < 1800.0)):
                        deltaT = (TemperatureAdjusted - (1171.11 * pow(HTHA_PRESSURE_psia - 1215.03, -0.092)))
                    elif((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 2600.0)):
                        deltaT = (TemperatureAdjusted - (((4E-05 * pow(HTHA_PRESSURE_psia,2.0)) - (0.2042 * HTHA_PRESSURE_psia)) + 903.69))
                    elif((HTHA_PRESSURE_psia >= 2600.0) and (HTHA_PRESSURE_psia < 13000.0)):
                        deltaT = (TemperatureAdjusted - 625.0)
                if(self.HTHA_MATERIAL=="2.25Cr-1Mo"):
                    if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 2000.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1701 * HTHA_PRESSURE_psia) + 1200.0))
                    elif((HTHA_PRESSURE_psia >= 2000.0) and (HTHA_PRESSURE_psia < 6000.0)):
                        deltaT = (TemperatureAdjusted - 855.0)
                    elif(self.HTHA_MATERIAL=="3Cr-1Mo"):
                        if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1800.0)):
                            deltaT = (TemperatureAdjusted - ((-0.1659 * HTHA_PRESSURE_psia) + 1250.0))
                        elif((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 6000.0)):
                            deltaT = (TemperatureAdjusted - 950.0)
                if(self.HTHA_MATERIAL=="6Cr-0.5Mo"):
                    if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1100.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1254 * HTHA_PRESSURE_psia) + 1300.0))
                    elif((HTHA_PRESSURE_psia >= 1100.0) and (HTHA_PRESSURE_psia < 6000.0)):
                        deltaT = (TemperatureAdjusted - 1120.0)
                if(self.HTHA_MATERIAL=="Not Applicable"):
                    SUSCEP = "None"
            if(SUSCEP == ""):
                if(deltaT >= 0):
                    SUSCEP = "High"
                elif(deltaT < 0 and deltaT >= -50):
                    SUSCEP = "Medium"
                elif(deltaT < -50 and deltaT >= -100):
                    SUSCEP = "Low"
                else:
                    SUSCEP = "None"
        return SUSCEP

    def DF_HTHA(self, age):
        if(self.Hydrogen == 0 or self.MAX_OP_TEMP == 0):
            return 0 # sua thanh -1 khi dung inspection plan
        if(self.HTHA_SUSCEP(age) == "No"):
            return 0 # sua thanh -1 khi dung inspection plan
        elif(self.HTHA_SUSCEP(age) == "Observed" or self.HTHA_SUSCEP(age) == "High"):
            kq = 5000
        elif(self.HTHA_SUSCEP(age) == "Medium"):
            kq = 2000
        elif(self.HTHA_SUSCEP(age) == "Low"):
            kq = 100
        else:
            kq = 0
        return kq
    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "High Temperature Hydrogen Attack", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DF_HTHA_API(self, i):
        return self.DF_HTHA(self.GET_AGE() + i)
 # Calculate BRITTLE
class DF_BRITTLE:
    def __init__(self,PRESSSURE_CONTROL,MIN_TEMP_PRESSURE,CRITICAL_TEMP,PWHT,REF_TEMP,BRITTLE_THICK,FABRICATED_STEEL,EQUIPMENT_SATISFIED,NOMINAL_OPERATING_CONDITIONS,CET_THE_MAWP,CYCLIC_SERVICE,
                 EQUIPMENT_CIRCUIT_SHOCK,NomalThick, CARBON_ALLOY, MIN_DESIGN_TEMP, MAX_OP_TEMP,AssesmentDate,Commissiondate,ComponentNumber):
        self.PRESSSURE_CONTROL=PRESSSURE_CONTROL
        self.MIN_TEMP_PRESSURE=MIN_TEMP_PRESSURE
        self.CRITICAL_TEMP=CRITICAL_TEMP
        self.PWHT=PWHT
        self.REF_TEMP=REF_TEMP
        self.BRITTLE_THICK=BRITTLE_THICK

        self.FABRICATED_STEEL=FABRICATED_STEEL
        self.EQUIPMENT_SATISFIED=EQUIPMENT_SATISFIED
        self.NOMINAL_OPERATING_CONDITIONS=NOMINAL_OPERATING_CONDITIONS
        self.CET_THE_MAWP=CET_THE_MAWP
        self.CYCLIC_SERVICE=CYCLIC_SERVICE
        self.EQUIPMENT_CIRCUIT_SHOCK=EQUIPMENT_CIRCUIT_SHOCK
        self.NomalThick=NomalThick
        self.CARBON_ALLOY=CARBON_ALLOY
        self.MIN_DESIGN_TEMP=MIN_DESIGN_TEMP
        self.MAX_OP_TEMP=MAX_OP_TEMP
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def Tmin(self):
        TEMP_BRITTLE = 0
        if (self.PRESSSURE_CONTROL):
            TEMP_BRITTLE = self.MIN_TEMP_PRESSURE
        else:
            TEMP_BRITTLE = self.CRITICAL_TEMP
        return TEMP_BRITTLE
    def Tmin_Tref(self):
        return (self.Tmin()-self.REF_TEMP)
    def DFB_BRITTLE(self,age):
        TEMP_BRITTLE = 0
        if (self.PRESSSURE_CONTROL):
            TEMP_BRITTLE = self.MIN_TEMP_PRESSURE
        else:
            TEMP_BRITTLE = self.CRITICAL_TEMP
        if (self.PWHT):
            return DAL_CAL.POSTGRESQL.GET_TBL_215(self.API_TEMP(TEMP_BRITTLE - self.REF_TEMP),
                                                  self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
        else:
            return DAL_CAL.POSTGRESQL.GET_TBL_214(self.API_TEMP(TEMP_BRITTLE - self.REF_TEMP),
                                                  self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
    def API_TEMP(self, TEMP):
        data = [-56, -44, -33, -22, -11, 0, 11, 22, 33, 44, 56]
        if (TEMP < data[0]):
            return data[0]
        elif (TEMP < data[1]):
            return data[0]
        elif (TEMP < data[2]):
            return data[1]
        elif (TEMP < data[3]):
            return data[2]
        elif (TEMP < data[4]):
            return data[3]
        elif (TEMP < data[5]):
            return data[4]
        elif (TEMP < data[6]):
            return data[5]
        elif (TEMP < data[7]):
            return data[6]
        elif (TEMP < data[8]):
            return data[7]
        elif (TEMP < data[9]):
            return data[8]
        elif (TEMP < data[10]):
            return data[9]
        else:
            return data[10]

    def API_SIZE_BRITTLE(self, SIZE):
        data = [6.4, 12.7, 25.4, 38.1, 50.8, 63.5, 76.2, 88.9, 101.6]
        if (SIZE < data[0]):
            return data[0]
        elif (SIZE < data[1]):
            return data[1]
        elif (SIZE < data[2]):
            return data[2]
        elif (SIZE < data[3]):
            return data[3]
        elif (SIZE < data[4]):
            return data[4]
        elif (SIZE < data[5]):
            return data[5]
        elif (SIZE < data[6]):
            return data[6]
        elif (SIZE < data[7]):
            return data[7]
        else:
            return data[8]
    def FSE(self):
        Fse = 1
        if (self.BRITTLE_THICK <= 12.7 or (
                                        self.FABRICATED_STEEL and self.EQUIPMENT_SATISFIED and self.NOMINAL_OPERATING_CONDITIONS
                            and self.CET_THE_MAWP and self.CYCLIC_SERVICE and self.EQUIPMENT_CIRCUIT_SHOCK and (
                            self.NomalThick <= 50.8))):
            Fse = 0.01
        return Fse
    def DF_BRITTLE(self, i):
        try:
            Fse = 1
            if (self.BRITTLE_THICK <= 12.7 or (
                                    self.FABRICATED_STEEL and self.EQUIPMENT_SATISFIED and self.NOMINAL_OPERATING_CONDITIONS
                        and self.CET_THE_MAWP and self.CYCLIC_SERVICE and self.EQUIPMENT_CIRCUIT_SHOCK and (
                self.NomalThick <= 50.8))):
                Fse = 0.01
            if (self.CARBON_ALLOY and (
                    self.CRITICAL_TEMP < self.MIN_DESIGN_TEMP or self.MAX_OP_TEMP < self.MIN_DESIGN_TEMP)):
                # if (self.LOWEST_TEMP):
                return self.DFB_BRITTLE(i) * Fse
                # else:
                #     return self.DFB_BRIITLE()
            else:
                return 0
        except Exception as e:
            print(e)

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Brittle Fracture", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########
    def DFB_BRITTLE_API(self, i):
        return self.DFB_BRITTLE(self.GET_AGE() + i)
    def DF_BRITTLE_API(self, i):
        return self.DF_BRITTLE(self.GET_AGE() + i)

    # Calculate TEMP EMBRITTLE
class Df_TEMP_EMBRITTLE:
    def __init__(self,TEMPER_SUSCEP,CARBON_ALLOY,MAX_OP_TEMP,MIN_OP_TEMP,PRESSSURE_CONTROL,MIN_TEMP_PRESSURE,REF_TEMP,DELTA_FATT,CRITICAL_TEMP,PWHT,BRITTLE_THICK,MIN_DESIGN_TEMP,AssesmentDate,Commissiondate,ComponentNumber):
        self.TEMPER_SUSCEP = TEMPER_SUSCEP
        self.CARBON_ALLOY = CARBON_ALLOY
        self.MAX_OP_TEMP = MAX_OP_TEMP
        self.MIN_OP_TEMP = MIN_OP_TEMP
        self.PRESSSURE_CONTROL = PRESSSURE_CONTROL
        self.MIN_TEMP_PRESSURE = MIN_TEMP_PRESSURE
        self.REF_TEMP = REF_TEMP
        self.DELTA_FATT = DELTA_FATT
        self.CRITICAL_TEMP = CRITICAL_TEMP
        self.PWHT = PWHT
        self.BRITTLE_THICK = BRITTLE_THICK
        self.MIN_DESIGN_TEMP = MIN_DESIGN_TEMP
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def API_SIZE_BRITTLE(self, SIZE):
        data = [6.4, 12.7, 25.4, 38.1, 50.8, 63.5, 76.2, 88.9, 101.6]
        if (SIZE < data[0]):
            return data[0]
        elif (SIZE < data[1]):
            return data[1]
        elif (SIZE < data[2]):
            return data[2]
        elif (SIZE < data[3]):
            return data[3]
        elif (SIZE < data[4]):
            return data[4]
        elif (SIZE < data[5]):
            return data[5]
        elif (SIZE < data[6]):
            return data[6]
        elif (SIZE < data[7]):
            return data[7]
        else:
            return data[8]

    def API_TEMP(self, TEMP):
        data = [-56, -44, -33, -22, -11, 0, 11, 22, 33, 44, 56]
        if (TEMP < data[0]):
            return data[0]
        elif (TEMP < data[1]):
            return data[0]
        elif (TEMP < data[2]):
            return data[1]
        elif (TEMP < data[3]):
            return data[2]
        elif (TEMP < data[4]):
            return data[3]
        elif (TEMP < data[5]):
            return data[4]
        elif (TEMP < data[6]):
            return data[5]
        elif (TEMP < data[7]):
            return data[6]
        elif (TEMP < data[8]):
            return data[7]
        elif (TEMP < data[9]):
            return data[8]
        elif (TEMP < data[10]):
            return data[9]
        else:
            return data[10]
    def REF_TEMPaddDELTA_FATT(self):
        return (self.REF_TEMP + self.DELTA_FATT)
    def TEMP_EMBRITTLE(self):
        TEMP_EMBRITTLE = 0
        if (self.PRESSSURE_CONTROL):
            TEMP_EMBRITTLE = self.MIN_TEMP_PRESSURE - (self.REF_TEMP + self.DELTA_FATT)
        else:
            TEMP_EMBRITTLE = min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP) - (self.REF_TEMP + self.DELTA_FATT)
        return TEMP_EMBRITTLE
    def TMPT(self):
        if (self.PRESSSURE_CONTROL):
            return self.MIN_TEMP_PRESSURE
        else:
            min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP)
    def DF_TEMP_EMBRITTLE(self,i):
        if (self.TEMPER_SUSCEP or (self.CARBON_ALLOY and not (self.MAX_OP_TEMP < 343 or self.MIN_OP_TEMP > 577))):
            TEMP_EMBRITTLE = 0
            if (self.PRESSSURE_CONTROL):
                TEMP_EMBRITTLE = self.MIN_TEMP_PRESSURE - (self.REF_TEMP + self.DELTA_FATT)
            else:
                TEMP_EMBRITTLE = min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP) - (self.REF_TEMP + self.DELTA_FATT)
            if (self.PWHT):
                return DAL_CAL.POSTGRESQL.GET_TBL_215(self.API_TEMP(TEMP_EMBRITTLE),
                                                     self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_214(self.API_TEMP(TEMP_EMBRITTLE),
                                                     self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Temper Embrittlement", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DF_TEMP_EMBRITTLE_API(self, i):
        return self.DF_TEMP_EMBRITTLE(self.GET_AGE() + i)
# Calculate 885w
class Df_885:
    def __init__(self,CHROMIUM_12,MIN_OP_TEMP,MAX_OP_TEMP,PRESSSURE_CONTROL,MIN_TEMP_PRESSURE,REF_TEMP,CRITICAL_TEMP,MIN_DESIGN_TEMP,AssesmentDate,Commissiondate,ComponentNumber):

        self.CHROMIUM_12 = CHROMIUM_12
        self.MIN_OP_TEMP = MIN_OP_TEMP
        self.MAX_OP_TEMP = MAX_OP_TEMP
        self.PRESSSURE_CONTROL = PRESSSURE_CONTROL
        self.MIN_TEMP_PRESSURE = MIN_TEMP_PRESSURE
        self.REF_TEMP = REF_TEMP
        self.CRITICAL_TEMP = CRITICAL_TEMP
        self.MIN_DESIGN_TEMP = MIN_DESIGN_TEMP
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def Tmin_Tref(self):
        TEMP_885 = 0
        if (self.PRESSSURE_CONTROL):
            TEMP_885 = self.MIN_TEMP_PRESSURE - self.REF_TEMP
        else:
            TEMP_885 = min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP) - self.REF_TEMP
        return TEMP_885
    def Tmin(self):
        if (self.PRESSSURE_CONTROL):
            return(self.MIN_TEMP_PRESSURE)
        else:
            return(min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP))
    def DF_885(self, i):
        if (self.CHROMIUM_12 and not (self.MIN_OP_TEMP > 566 or self.MAX_OP_TEMP < 371)):
            TEMP_885 = 0
            if (self.PRESSSURE_CONTROL):
                TEMP_885 = self.MIN_TEMP_PRESSURE - self.REF_TEMP
            else:
                TEMP_885 = min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP) - self.REF_TEMP
            data = [-56, -44, -33, -22, -11, 0, 11, 22, 33, 44, 56]
            if (TEMP_885 < data[0]):
                return 1381
            elif (TEMP_885 < data[1]):
                return 1381
            elif (TEMP_885 < data[2]):
                return 1216
            elif (TEMP_885 < data[3]):
                return 1022
            elif (TEMP_885 < data[4]):
                return 806
            elif (TEMP_885 < data[5]):
                return 581
            elif (TEMP_885 < data[6]):
                return 371
            elif (TEMP_885 < data[7]):
                return 200
            elif (TEMP_885 < data[8]):
                return 87
            elif (TEMP_885 < data[9]):
                return 30
            elif (TEMP_885 < data[10]):
                return 8
            elif (TEMP_885 == data[10]):
                return 371
            else:
                return 0
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "885F Embrittlement", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DF_885_API(self, i):
        return self.DF_885(self.GET_AGE() + i)
# Calculate SIGMA
class Df_SIGMA:
    def __init__(self,MIN_TEM,AUSTENITIC_STEEL,MIN_OP_TEMP,MAX_OP_TEMP,PRESSSURE_CONTROL,MIN_TEMP_PRESSURE,CRITICAL_TEMP,PERCENT_SIGMA,AssesmentDate,Commissiondate,ComponentNumber):

        self.MIN_TEM = MIN_TEM
        self.AUSTENITIC_STEEL = AUSTENITIC_STEEL
        self.MIN_OP_TEMP = MIN_OP_TEMP
        self.MAX_OP_TEMP = MAX_OP_TEMP
        self.PRESSSURE_CONTROL = PRESSSURE_CONTROL
        self.MIN_TEMP_PRESSURE = MIN_TEMP_PRESSURE
        self.CRITICAL_TEMP = CRITICAL_TEMP
        self.PERCENT_SIGMA = PERCENT_SIGMA
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def API_TEMP_SIGMA(self,MIN_TEM):
        DATA = [-46, -18, 10, 38, 66, 93, 204, 316, 427, 538, 649]
        if (MIN_TEM < DATA[0]):
            TEMP = DATA[0]
        elif (MIN_TEM < DATA[1]):
            TEMP = DATA[0]
        elif (MIN_TEM < DATA[2]):
            TEMP = DATA[1]
        elif (MIN_TEM < DATA[3]):
            TEMP = DATA[2]
        elif (MIN_TEM < DATA[4]):
            TEMP = DATA[3]
        elif (MIN_TEM < DATA[5]):
            TEMP = DATA[4]
        elif (MIN_TEM < DATA[6]):
            TEMP = DATA[5]
        elif (MIN_TEM < DATA[7]):
            TEMP = DATA[6]
        elif (MIN_TEM < DATA[8]):
            TEMP = DATA[7]
        elif (MIN_TEM < DATA[9]):
            TEMP = DATA[8]
        elif (MIN_TEM < DATA[10]):
            TEMP = DATA[9]
        else:
            TEMP = DATA[10]
        return TEMP
    def sigmaContent(self):
        if (self.PERCENT_SIGMA < 5):
            return 'Low Sigma'
        elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
            return 'Medium Sigma'
        else:
            return 'High Sigma'
    def DF_SIGMA(self,i):
        if (self.AUSTENITIC_STEEL and not (self.MIN_OP_TEMP > 927 or self.MAX_OP_TEMP < 593)):
            TEMP_SIGMA  = 0
            if (self.PRESSSURE_CONTROL):
                TEMP_SIGMA  = self.MIN_TEMP_PRESSURE
            else:
                TEMP_SIGMA  = min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP)
            TEMP = self.API_TEMP_SIGMA(TEMP_SIGMA)
            DFB_SIGMA = 0
            if (TEMP == 649):
                if (self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0
                else:
                    DFB_SIGMA = 18
            elif (TEMP == 538):
                if (self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0
                else:
                    DFB_SIGMA = 53
            elif (TEMP == 427):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0.2
                else:
                    DFB_SIGMA = 160
            elif (TEMP == 316):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0.9
                else:
                    DFB_SIGMA = 481
            elif (TEMP == 204):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 1.3
                else:
                    DFB_SIGMA = 1333
            elif (TEMP == 93):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.1
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 3
                else:
                    DFB_SIGMA = 3202
            elif (TEMP == 66):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.3
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 5
                else:
                    DFB_SIGMA = 3871
            elif (TEMP == 38):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.6
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 7
                else:
                    DFB_SIGMA = 4196
            elif (TEMP == 10):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.9
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 11
                else:
                    DFB_SIGMA = 4196
            elif (TEMP == -18):
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 1
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 20
                else:
                    DFB_SIGMA = 4196
            else:
                if (self.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 1.1
                elif (self.PERCENT_SIGMA >= 5 and self.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 34
                else:
                    DFB_SIGMA = 4196
            return DFB_SIGMA
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Sigma Phase Embrittlement", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DF_SIGMA_API(self, i):
        return self.DF_SIGMA(self.GET_AGE() + i)

        # Calculate Pipping
class Df_PIPE:
    def __init__(self,PREVIOUS_FAIL,AMOUNT_SHAKING,TIME_SHAKING,CYLIC_LOAD,APIComponentType,CORRECT_ACTION,NUM_PIPE,PIPE_CONDITION,JOINT_TYPE,BRANCH_DIAMETER,AssesmentDate,Commissiondate,ComponentNumber):
        self.PREVIOUS_FAIL = PREVIOUS_FAIL
        self.AMOUNT_SHAKING = AMOUNT_SHAKING
        self.TIME_SHAKING = TIME_SHAKING
        self.CYLIC_LOAD = CYLIC_LOAD
        self.APIComponentType = APIComponentType
        self.CORRECT_ACTION = CORRECT_ACTION
        self.NUM_PIPE = NUM_PIPE
        self.PIPE_CONDITION = PIPE_CONDITION
        self.JOINT_TYPE = JOINT_TYPE
        self.BRANCH_DIAMETER = BRANCH_DIAMETER
        self.AssesmentDate = AssesmentDate
        self.Commissiondate = Commissiondate
        self.ComponentNumber = ComponentNumber
    def DFB_PIPE(self):
        if (self.PREVIOUS_FAIL == "Greater than one"):
            DFB_PF = 500
        elif (self.PREVIOUS_FAIL == "One"):
            DFB_PF = 50
        else:
            DFB_PF = 1

        if (self.AMOUNT_SHAKING == "Severe"):
            DFB_AS = 500
        elif (self.AMOUNT_SHAKING == "Moderate"):
            DFB_AS = 50
        else:
            DFB_AS = 1

        if (self.TIME_SHAKING == "13 to 52 weeks"):
            FFB_AS = 0.02
        elif (self.TIME_SHAKING == "2 to 13 weeks"):
            FFB_AS = 0.2
        else:
            FFB_AS = 1

        if (self.CYLIC_LOAD == "Reciprocating machinery"):
            DFB_CF = 50
        elif (self.CYLIC_LOAD == "PRV chatter"):
            DFB_CF = 25
        elif (self.CYLIC_LOAD == "Valve with high pressure drop"):
            DFB_CF = 10
        else:
            DFB_CF = 1

        return max(DFB_PF, max(DFB_AS * FFB_AS, DFB_CF))

    def checkPiping(self):
        pip = ["PIPE-1", "PIPE-2", "PIPE-4", "PIPE-6", "PIPE-8", "PIPE-10", "PIPE-12", "PIPE-16", "PIPEGT16"]
        check = False
        for a in pip:
            if self.APIComponentType == a:
                check = True
                break
        return check

    def DF_PIPE(self, i):
        if (self.checkPiping()):
            if (self.CORRECT_ACTION == "Engineering Analysis"):
                FCA = 0.002
            elif (self.CORRECT_ACTION == "Experience"):
                FCA = 0.2
            else:
                FCA = 2

            if (self.NUM_PIPE == "Up to 5"):
                FPC = 0.5
            elif (self.NUM_PIPE == "6 to 10"):
                FPC = 1
            else:
                FPC = 2

            if (
                            self.PIPE_CONDITION == "Broken gussets or gussets welded directly to pipe" or self.PIPE_CONDITION == "Missing or damage supports, improper support"):
                FCP = 2
            else:
                FCP = 1

            if (self.JOINT_TYPE == "Sweepolets"):
                FJB = 0.02
            elif (self.JOINT_TYPE == "Piping tee weldolets"):
                FJB = 0.2
            elif (self.JOINT_TYPE == "Threaded, socket welded, or saddle on"):
                FJB = 2
            else:
                FJB = 1

            if (self.BRANCH_DIAMETER == "All branches greater than 2\" Nominal OD"):
                FBD = 0.02
            else:
                FBD = 1
            return self.DFB_PIPE() * FCA * FPC * FCP * FJB * FBD
        else:
            return 0

    def GET_AGE(self):
        age = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber, "Vibration-Induced Mechanical Fatigue", self.Commissiondate,
                                              self.AssesmentDate)
        return age
        ###########

    def DF_PIPE_API(self, i):
        return self.DF_LINNING(self.GET_AGE() + i)


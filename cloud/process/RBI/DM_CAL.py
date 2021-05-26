from concurrent.futures import ThreadPoolExecutor
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

from cloud.process.RBI.Object.table import Table65 as TBL65
from cloud.process.RBI.Object.table import Table64 as TBL64
from cloud.process.RBI.Object.table import Table7_4 as TBL74

# nhung gia tri Num_inspec, EFF khong can truyen khi su dung ham
class DM_CAL:
    # ham khoi tao
    def __init__(self,ComponentNumber = "", Commissiondate = datetime.now(), AssessmentDate = datetime.now(), APIComponentType="",
                 Diametter=0, NomalThick=0, CurrentThick=0, MinThickReq=0, CorrosionRate=0, CA=0,
                 ProtectedBarrier=False, CladdingCorrosionRate=0, InternalCladding=False, NoINSP_THINNING=0,
                 EFF_THIN="E", OnlineMonitoring="", HighlyEffectDeadleg=False, ContainsDeadlegs=False,
                 TankMaintain653=False, AdjustmentSettle="", ComponentIsWeld=False,
                 LinningType="", LINNER_ONLINE=False, LINNER_CONDITION="", INTERNAL_LINNING=False,
                 CAUSTIC_INSP_EFF="E", CAUSTIC_INSP_NUM=0, HEAT_TREATMENT="", NaOHConcentration=0, HEAT_TRACE=False,
                 STEAM_OUT=False,
                 AMINE_INSP_EFF="E", AMINE_INSP_NUM=0, AMINE_EXPOSED=False, AMINE_SOLUTION="",
                 ENVIRONMENT_H2S_CONTENT=False, AQUEOUS_OPERATOR=False, AQUEOUS_SHUTDOWN=False, SULPHIDE_INSP_EFF="E",
                 SULPHIDE_INSP_NUM=0, H2SContent=0, PH=0, PRESENT_CYANIDE=False, BRINNEL_HARDNESS="",
                 SULFUR_INSP_EFF="E", SULFUR_INSP_NUM=0, SULFUR_CONTENT="",StructuralThickness =0,
                 CACBONATE_INSP_EFF="E", CACBONATE_INSP_NUM=0, CO3_CONTENT=0,
                 PTA_SUSCEP=False, NICKEL_ALLOY=False, EXPOSED_SULFUR=False, PTA_INSP_EFF="E", PTA_INSP_NUM=0,
                 ExposedSH2OOperation=False, ExposedSH2OShutdown=False, ThermalHistory="", PTAMaterial="",
                 DOWNTIME_PROTECTED=False, MINIUM_STRUCTURAL_THICKNESS_GOVERS=False,
                 INTERNAL_EXPOSED_FLUID_MIST =False, EXTERNAL_EXPOSED_FLUID_MIST=False, CHLORIDE_ION_CONTENT=0,
                 CLSCC_INSP_EFF="E", CLSCC_INSP_NUM=0,WeldJonintEfficiency=0, AllowableStress=0,
                 HSC_HF_INSP_EFF="E", HSC_HF_INSP_NUM=0,YeildStrengthDesignTemp =0,
                 HICSOHIC_INSP_EFF="E", HICSOHIC_INSP_NUM=0, HF_PRESENT=False,
                 EXTERNAL_INSP_NUM=0, EXTERNAL_INSP_EFF="E",Pressure=0,
                 INTERFACE_SOIL_WATER=False, SUPPORT_COATING=False, INSULATION_TYPE="", CUI_INSP_NUM=0,
                 CUI_INSP_EFF="E", CUI_PERCENT_1=0, CUI_PERCENT_2=0,
                 CUI_PERCENT_3=0, CUI_PERCENT_4=0, CUI_PERCENT_5=0, CUI_PERCENT_6=0, CUI_PERCENT_7=0, CUI_PERCENT_8=0,
                 CUI_PERCENT_9=0, CUI_PERCENT_10=0,
                 EXTERN_CLSCC_INSP_NUM=0, EXTERN_CLSCC_INSP_EFF="E",
                 EXTERNAL_INSULATION=False, COMPONENT_INSTALL_DATE=datetime.now().date(), CRACK_PRESENT=False,
                 EXTERNAL_EVIRONMENT="", EXTERN_COATING = False, EXTERN_COAT_QUALITY="", EXTERN_CLSCC_CUI_INSP_NUM=0,
                 EXTERN_CLSCC_CUI_INSP_EFF="E", PIPING_COMPLEXITY="", INSULATION_CONDITION="",
                 INSULATION_CHLORIDE=False, ShapeFactor="",
                 MATERIAL_SUSCEP_HTHA=False, HTHA_MATERIAL="", HTHA_NUM_INSP=0, HTHA_EFFECT="E", HTHA_PRESSURE=0,
                 CRITICAL_TEMP=0, DAMAGE_FOUND=False,CR_Confidents_Level="",
                 LOWEST_TEMP=False,TensileStrengthDesignTemp=0,
                 TEMPER_SUSCEP=False, PWHT=False, BRITTLE_THICK=0, CARBON_ALLOY=False, DELTA_FATT=0,
                 MAX_OP_TEMP=0, CHROMIUM_12=False, MIN_OP_TEMP=0, MIN_DESIGN_TEMP=0, REF_TEMP=0,
                 AUSTENITIC_STEEL=False, PERCENT_SIGMA=0,
                 EquipmentType="", PREVIOUS_FAIL="", AMOUNT_SHAKING="", TIME_SHAKING="", CYLIC_LOAD="",
                 CORRECT_ACTION="", NUM_PIPE="", PIPE_CONDITION="", JOINT_TYPE="", BRANCH_DIAMETER="",PRESSSURE_CONTROL=False,
                 FABRICATED_STEEL=False, EQUIPMENT_SATISFIED=False, NOMINAL_OPERATING_CONDITIONS=False,CET_THE_MAWP=False,
                 CYCLIC_SERVICE = False, EQUIPMENT_CIRCUIT_SHOCK=False,MIN_TEMP_PRESSURE=0,
                 Hydrogen = 0,HTHADamageObserved=0,CladdingThickness=0
                 # PRIMARY_SOIL_TYPE="", PARTICAL_SIZE_UNIFORMITY="",
                 # MOSTURE_LEVEL="",EquipmentTemperature=0, CATHODIC_PROTECTION_EFF="", SoilResistivity_ConsideredforbaseCR=False,
                 # AST_PAD_TYPE_FACTOR="",AST_DRAINAGE_TYPE="",AST_PAD_TYPE_BOTTOM="",SoilSideTemperature=0,
                 # COATING_TYPE="",BASE_COATING_TYPE=False,AGE_COATING=0,WATER_DRAW_OFF=False,
                 # MAX_RATED_TEMP_EXCEEDED=False,COATING_MANTENANCE_RAREORNONE=False,CR_SB = 0,CR_PB=0,STRAM_COIL=False,ProductSideBottomCR=""
                 # ,LEVEL_CHEMICALS_CONTAMINANTS="",CATHODIC_PROTECTION_TYPE="",SoilResistivity = 0,PRODUCT_SIDE_CONDITION="",
                 # ProductSideTemp=0
                 ):

        self.ComponentNumber = ComponentNumber
        self.CommissionDate = Commissiondate
        self.AssesmentDate = AssessmentDate
        self.APIComponentType = APIComponentType
        # Thinning input
        self.CladdingThickness = CladdingThickness
        self.Diametter = Diametter
        self.NomalThick = NomalThick
        self.CurrentThick = CurrentThick
        self.MinThickReq = MinThickReq
        self.CorrosionRate = CorrosionRate
        self.CA = CA
        self.ProtectedBarrier = ProtectedBarrier
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
        self.WeldJointEffciency = WeldJonintEfficiency
        self.AllowableStress = AllowableStress
        self.TensileStrengthDesignTemp = TensileStrengthDesignTemp
        self.YieldStrengthDesignTemp = YeildStrengthDesignTemp
        self.StructuralThickness = StructuralThickness
        self.MINIUM_STRUCTURAL_THICKNESS_GOVERS = MINIUM_STRUCTURAL_THICKNESS_GOVERS
        self.Pressure = Pressure
        self.ShapeFactor = ShapeFactor
        self.CR_Confidents_Level= CR_Confidents_Level


        # Linning input
        self.LinningType = LinningType
        self.LINNER_ONLINE = LINNER_ONLINE
        self.LINNER_CONDITION = LINNER_CONDITION
        self.INTERNAL_LINNING = INTERNAL_LINNING


        # SCC Caustic input
        self.CAUSTIC_INSP_EFF = CAUSTIC_INSP_EFF
        self.CAUSTIC_INSP_NUM = CAUSTIC_INSP_NUM
        self.HEAT_TREATMENT = HEAT_TREATMENT
        self.NaOHConcentration = NaOHConcentration
        self.HEAT_TRACE = HEAT_TRACE
        self.STEAM_OUT = STEAM_OUT

        # SCC Amine input
        self.AMINE_INSP_EFF = AMINE_INSP_EFF
        self.AMINE_INSP_NUM = AMINE_INSP_NUM
        self.AMINE_EXPOSED = AMINE_EXPOSED
        self.AMINE_SOLUTION = AMINE_SOLUTION

        # Sulphide Stress Cracking input
        self.ENVIRONMENT_H2S_CONTENT = ENVIRONMENT_H2S_CONTENT
        self.AQUEOUS_OPERATOR = AQUEOUS_OPERATOR
        self.AQUEOUS_SHUTDOWN = AQUEOUS_SHUTDOWN
        self.SULPHIDE_INSP_EFF = SULPHIDE_INSP_EFF
        self.SULPHIDE_INSP_NUM = SULPHIDE_INSP_NUM
        self.H2SContent = H2SContent
        self.PH = PH
        self.PRESENT_CYANIDE = PRESENT_CYANIDE
        self.BRINNEL_HARDNESS = BRINNEL_HARDNESS

        # HIC/SOHIC H2S input
        self.SULFUR_INSP_EFF = SULFUR_INSP_EFF
        self.SULFUR_INSP_NUM = SULFUR_INSP_NUM
        self.SULFUR_CONTENT = SULFUR_CONTENT

        # Carboonate Cracking input
        self.CACBONATE_INSP_EFF = CACBONATE_INSP_EFF
        self.CACBONATE_INSP_NUM = CACBONATE_INSP_NUM
        self.CO3_CONTENT = CO3_CONTENT

        # PTA Cracking input
        self.PTA_SUSCEP = PTA_SUSCEP
        self.NICKEL_ALLOY = NICKEL_ALLOY
        self.EXPOSED_SULFUR = EXPOSED_SULFUR
        self.PTA_INSP_EFF = PTA_INSP_EFF
        self.PTA_INSP_NUM = PTA_INSP_NUM
        self.ExposedSH2OOperation = ExposedSH2OOperation
        self.ExposedSH2OShutdown = ExposedSH2OShutdown
        self.ThermalHistory = ThermalHistory
        self.PTAMaterial = PTAMaterial
        self.DOWNTIME_PROTECTED = DOWNTIME_PROTECTED

        # CLSCC input
        self.INTERNAL_EXPOSED_FLUID_MIST = INTERNAL_EXPOSED_FLUID_MIST
        self.EXTERNAL_EXPOSED_FLUID_MIST = EXTERNAL_EXPOSED_FLUID_MIST
        self.CHLORIDE_ION_CONTENT = CHLORIDE_ION_CONTENT
        self.CLSCC_INSP_EFF = CLSCC_INSP_EFF
        self.CLSCC_INSP_NUM = CLSCC_INSP_NUM

        # HFC-HS input
        self.HSC_HF_INSP_EFF = HSC_HF_INSP_EFF
        self.HSC_HF_INSP_NUM = HSC_HF_INSP_NUM

        # HICSOHIC-HF input
        self.HICSOHIC_INSP_EFF = HICSOHIC_INSP_EFF
        self.HICSOHIC_INSP_NUM = HICSOHIC_INSP_NUM
        self.HF_PRESENT = HF_PRESENT

        # EXTERNAL CORROSION input
        self.EXTERNAL_INSP_NUM = EXTERNAL_INSP_NUM
        self.EXTERNAL_INSP_EFF = EXTERNAL_INSP_EFF
        #self.NoINSP_EXTERNAL= NoINSP_EXTERNAL

        # CUI input
        self.INTERFACE_SOIL_WATER = INTERFACE_SOIL_WATER
        self.SUPPORT_COATING = SUPPORT_COATING
        self.INSULATION_TYPE = INSULATION_TYPE
        self.CUI_INSP_NUM = CUI_INSP_NUM
        self.CUI_INSP_EFF = CUI_INSP_EFF
        self.CUI_PERCENT_1 = CUI_PERCENT_1
        self.CUI_PERCENT_2 = CUI_PERCENT_2
        self.CUI_PERCENT_3 = CUI_PERCENT_3
        self.CUI_PERCENT_4 = CUI_PERCENT_4
        self.CUI_PERCENT_5 = CUI_PERCENT_5
        self.CUI_PERCENT_6 = CUI_PERCENT_6
        self.CUI_PERCENT_7 = CUI_PERCENT_7
        self.CUI_PERCENT_8 = CUI_PERCENT_8
        self.CUI_PERCENT_9 = CUI_PERCENT_9
        self.CUI_PERCENT_10 = CUI_PERCENT_10

        # EXTERNAL CLSCC input
        self.EXTERN_CLSCC_INSP_NUM = EXTERN_CLSCC_INSP_NUM
        self.EXTERN_CLSCC_INSP_EFF = EXTERN_CLSCC_INSP_EFF

        # EXTERN CUI CLSCC input
        self.EXTERNAL_INSULATION = EXTERNAL_INSULATION
        self.COMPONENT_INSTALL_DATE = COMPONENT_INSTALL_DATE
        self.CRACK_PRESENT = CRACK_PRESENT
        self.EXTERNAL_EVIRONMENT = EXTERNAL_EVIRONMENT
        self.EXTERN_COAT_QUALITY = EXTERN_COAT_QUALITY
        self.EXTERN_CLSCC_CUI_INSP_NUM = EXTERN_CLSCC_CUI_INSP_NUM
        self.EXTERN_CLSCC_CUI_INSP_EFF = EXTERN_CLSCC_CUI_INSP_EFF
        self.PIPING_COMPLEXITY = PIPING_COMPLEXITY
        self.INSULATION_CONDITION = INSULATION_CONDITION
        self.INSULATION_CHLORIDE = INSULATION_CHLORIDE
        self.EXTERN_COATING = EXTERN_COATING

        # HTHA input
        self.MATERIAL_SUSCEP_HTHA = MATERIAL_SUSCEP_HTHA
        self.HTHA_MATERIAL = HTHA_MATERIAL
        self.HTHA_NUM_INSP = HTHA_NUM_INSP
        self.HTHA_EFFECT = HTHA_EFFECT
        self.HTHA_PRESSURE = HTHA_PRESSURE
        self.CRITICAL_TEMP = CRITICAL_TEMP
        self.DAMAGE_FOUND = DAMAGE_FOUND
        self.Hydrogen = Hydrogen
        self.HTHADamageObserved = HTHADamageObserved

        # BRITTLE input
        self.LOWEST_TEMP = LOWEST_TEMP
        self.PRESSSURE_CONTROL = PRESSSURE_CONTROL
        self.FABRICATED_STEEL = FABRICATED_STEEL
        self.EQUIPMENT_SATISFIED = EQUIPMENT_SATISFIED
        self.NOMINAL_OPERATING_CONDITIONS = NOMINAL_OPERATING_CONDITIONS
        self.CET_THE_MAWP = CET_THE_MAWP
        self.CYCLIC_SERVICE = CYCLIC_SERVICE
        self.EQUIPMENT_CIRCUIT_SHOCK = EQUIPMENT_CIRCUIT_SHOCK
        self.MIN_TEMP_PRESSURE = MIN_TEMP_PRESSURE

        # TEMPER EMBRITTLE input
        self.TEMPER_SUSCEP = TEMPER_SUSCEP
        self.PWHT = PWHT
        self.BRITTLE_THICK = BRITTLE_THICK
        self.CARBON_ALLOY = CARBON_ALLOY
        self.DELTA_FATT = DELTA_FATT

        # 885 input
        self.MAX_OP_TEMP = MAX_OP_TEMP
        self.CHROMIUM_12 = CHROMIUM_12
        self.MIN_OP_TEMP = MIN_OP_TEMP
        self.MIN_DESIGN_TEMP = MIN_DESIGN_TEMP
        self.REF_TEMP = REF_TEMP

        # SIGMA input
        self.AUSTENITIC_STEEL = AUSTENITIC_STEEL
        self.PERCENT_SIGMA = PERCENT_SIGMA

        # PIPING MECHANICAL input
        self.EquipmentType = EquipmentType
        self.PREVIOUS_FAIL = PREVIOUS_FAIL
        self.AMOUNT_SHAKING = AMOUNT_SHAKING
        self.TIME_SHAKING = TIME_SHAKING
        self.CYLIC_LOAD = CYLIC_LOAD
        self.CORRECT_ACTION = CORRECT_ACTION
        self.NUM_PIPE = NUM_PIPE
        self.PIPE_CONDITION = PIPE_CONDITION
        self.JOINT_TYPE = JOINT_TYPE
        self.BRANCH_DIAMETER = BRANCH_DIAMETER

    ### caculate corrosion rate input ###

        # soil side corrosion input
        # self.PRIMARY_SOIL_TYPE = PRIMARY_SOIL_TYPE
        # self.LEVER_CHEMICCALS_CONTAMINANTS = LEVEL_CHEMICALS_CONTAMINANTS
        # self.PARTICAL_SIZE_UNIFORMITY = PARTICAL_SIZE_UNIFORMITY
        # self.MOSTURE_LEVEL = MOSTURE_LEVEL
        # self.EquipmentTemperature = EquipmentTemperature
        # self.CATHODIC_PROTECTION_EFF = CATHODIC_PROTECTION_EFF
        # self.COATING_TYPE = COATING_TYPE
        # self.BASE_COATING_TYPE = BASE_COATING_TYPE
        # self.AGE_COATING = AGE_COATING
        # self.MAX_RATED_TEMP_EXCEEDED = MAX_RATED_TEMP_EXCEEDED
        # self.COATING_MANTENANCE_RAREORNONE = COATING_MANTENANCE_RAREORNONE
        # self.SoilResistivity_Considered_forbaseCR = SoilResistivity_ConsideredforbaseCR


        # Tank bottom corrosion input
           #soil side corrosion rate for tank input
        # self.SoilResistivity = SoilResistivity
        # self.AST_PAD_TYPE_FACTOR = AST_PAD_TYPE_FACTOR
        # self.AST_DRAINAGE_TYPE = AST_DRAINAGE_TYPE
        # self.CATHODIC_PROTECTION_TYPE = CATHODIC_PROTECTION_TYPE
        # self.AST_PAD_TYPE_BOTTOM = AST_PAD_TYPE_BOTTOM
        # self.SoilSideTemperature = SoilSideTemperature
        # self.CR_SB = CR_SB
            # product side corrosion rate for tank input
        # self.CR_PB = CR_PB
        # self.PRODUCT_SIDE_CONDITION = PRODUCT_SIDE_CONDITION
        # self.ProductSideTemp = ProductSideTemp
        # self.STRAM_COIL = STRAM_COIL
        # self.WATER_DRAW_OFF = WATER_DRAW_OFF
        # self.ProductSideBottomCR = ProductSideBottomCR


    # PoF convert cataloge
    def PoFCategory(self, DF_total):
        if round(DF_total, 0) <= 2:
            return "1"
        elif round(DF_total, 0) > 2 and round(DF_total, 0) <= 20:
            return "2"
        elif round(DF_total, 0) > 20 and round(DF_total, 0) <= 150:
            return "3"
        elif round(DF_total, 0) > 150 and round(DF_total, 0) <= 1000:
            return "4"
        else:
            return "5"
        # if DF_total <= 2:
        #     return "1"
        # elif DF_total <= 20:
        #     return "2"
        # elif DF_total <= 100:
        #     return "3"
        # elif DF_total <= 1000:
        #     return "4"
        # else:
        #     return "5"

    # DF LIST
    DM_Name = ["Internal Thinning", "Internal Lining Degradation", "Caustic Stress Corrosion Cracking",
               "Amine Stress Corrosion Cracking", "Sulphide Stress Corrosion Cracking (H2S)", "HIC/SOHIC-H2S",
               "Carbonate Stress Corrosion Cracking", "Polythionic Acid Stress Corrosion Cracking",
               "Chloride Stress Corrosion Cracking", "Hydrogen Stress Cracking (HF)", "HF Produced HIC/SOHIC",
               "External Corrosion", "Corrosion Under Insulation", "External Chloride Stress Corrosion Cracking",
               "Chloride Stress Corrosion Cracking Under Insulation", "High Temperature Hydrogen Attack",
               "Brittle Fracture", "Temper Embrittlement", "885F Embrittlement", "Sigma Phase Embrittlement",
               "Vibration-Induced Mechanical Fatigue"]
    # calculate Thinning Damage Factor
    #step 1

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

    def agetk(self,age):
        return age
    def trdi(self):
        return self.CurrentThick

    def agerc(self, age):
        try:
            a = age - self.GET_AGE()[0]
            if self.InternalCladding:
                return max(((self.trdi() - (self.NomalThick - self.CladdingThickness)) / self.CladdingCorrosionRate - a), 0)
            else:
                return max(((self.trdi() - self.NomalThick) / self.CladdingCorrosionRate - a), 0)
        except:
            return 0
    def Art(self,age):
        try:
            if self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType == "TANKROOFFLOAT0":
                # print("Art")
                # print(max((1-(self.trdi() - self.CorrosionRate * self.agetk(age)) / (self.getTmin() + self.CA)), 0.0))
                return max((1-(self.trdi() - self.CorrosionRate * self.agetk(age)) / (self.getTmin() + self.CA)), 0.0)
            elif (self.InternalCladding):
                if (self.agetk(age) < self.agerc(age)):
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
        try:
            a=self.I1_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
        except Exception as e:
            print(e,"Po_P1_Thin")
        return self.I1_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
    def Po_P2_Thin(self):
        a = self.I2_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
        return self.I2_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
    def Po_P3_Thin(self):
        return self.I3_Thin()/(self.I1_Thin() + self.I2_Thin() + self.I3_Thin())
    def B1_Thin(self,age):
        # print("test b1_Thin")
        # print((1 - self.Art(age)- self.SRp_Thin())/math.sqrt(pow(self.Art(age), 2) * 0.04 + pow((1 - self.Art(age)), 2) * 0.04 + pow(self.SRp_Thin(), 2) * pow(0.05, 2)))
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
        # print(self.EquipmentType)
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
                Fsm = 0
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
        # print("thing",a)
        # print("DFB_THIN",self.DFB_THIN(age))
        # print("FIP",Fip)
        # print("Fdl",Fdl)
        # print("Fwd",Fwd)
        # print("Fam",Fam)
        # print("Fsm",Fsm)
        # print("self.AdjustmentSettle",self.AdjustmentSettle)
        return max(a,0.1)

    #Calculate Linning:
    def DFB_LINNING(self, age):
        # if (self.INTERNAL_LINNING):
            # if (self.LinningType == "Organic - Low Quality"):
            #     SUSCEP_LINNING ="MoreThan6Years"
            #     return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            # elif(self.LinningType == "Organic - Medium Quality"):
            #     SUSCEP_LINNING ="WithinLast6Years"
            #     return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            # elif(self.LinningType == "Organic - High Quality"):
            #     SUSCEP_LINNING ="WithinLast3Years"
            #     return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            # else:
            #     return DAL_CAL.POSTGRESQL.GET_TBL_64(math.ceil(age), self.LinningType)
        newAge = math.ceil(age)
        if (newAge < 1):
            newAge = 1
        elif (newAge >= 25):
            newAge = 25
        else:
            newAge = newAge
        if (self.INTERNAL_LINNING):
            if (self.LinningType == "Organic - Low Quality"):
                return TBL65.Table_Year_In_Service.get(newAge)[0]
            elif(self.LinningType == "Organic - Medium Quality"):
                return TBL65.Table_Year_In_Service.get(newAge)[1]
            elif(self.LinningType == "Organic - High Quality"):
                return TBL65.Table_Year_In_Service.get(newAge)[2]
            else:
                if self.LinningType == "Strip lined alloy":
                    index = 0
                elif self.LinningType == "Castable refractory":
                    index = 1
                elif self.LinningType == "Castable refractory severe condition":
                    index = 2
                elif self.LinningType == "Glass lined":
                    index = 3
                elif self.LinningType == "Acid Brick":
                    index = 4
                else:
                    index = 5
                    return TBL64.Table_Years_Since_Last_Inspection.get(newAge)[index]
        else:
            return 0
       

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

    # Calculate Caustic:
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
        Y = [81.25,80, 78.125, 74.219, 69.375, 65.625, 58.75, 55, 51.25, 48.75, 48.125]
        n = len(X)
        try:
            c = [0 for _ in range(n)]
            w = [0 for _ in range(n)]
            for i in range (0, n):
                #print(i)
                w[i]=Y[i]
                for j in reversed(range(i)):
                    #print(j)
                    w[j] = (w[j + 1] - w[j]) / (X[i] - X[j])
                c[i]=w[0]
            s = c[n-1]
            for i in reversed(range(n-1)):
                #print(X[i])
                s = s * (t -X[i])+c[i]
            #print(c)
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

    def DF_CAUSTIC(self, age):
        if (self.CARBON_ALLOY and self.NaOHConcentration != 0):
            self.CAUSTIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[2])
            self.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[2])
            if(age<1):
                return self.SVI_CAUSTIC()
            elif(self.CAUSTIC_INSP_EFF == "E" or self.CAUSTIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CAUSTIC_INSP_NUM) + self.CAUSTIC_INSP_EFF
            DFB_CAUSTIC = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CAUSTIC(), FIELD)
            return DFB_CAUSTIC * pow( max(age,1.0), 1.1)
        else:
            return 0

    # Calculate SCC AMINE:
    #co van de ve thuat toan. Can xem lai
    def getSusceptibility_Amine(self):
        if(self.AMINE_EXPOSED and self.CARBON_ALLOY):
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
                    elif ((self.MAX_OP_TEMP > 37.78 and self.MAX_OP_TEMP < 82.22) or self.HEAT_TRACE or self.STEAM_OUT):
                        sus = "Medium"
                    else:
                        sus = "Low"
                elif (self.AMINE_SOLUTION == "Diethanolamine DEA"):
                    if (self.MAX_OP_TEMP > 82.22):
                        sus = "Medium"
                    elif ((self.MAX_OP_TEMP > 60 and self.MAX_OP_TEMP < 82.22) or self.HEAT_TRACE or self.STEAM_OUT):
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

    def DF_AMINE(self, age):
        if (self.CARBON_ALLOY):
            self.AMINE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[3])
            self.AMINE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[3])
            if (self.AMINE_INSP_EFF == "E" or self.AMINE_INSP_NUM == 0):
                FIELD = "E"
            elif(age>1):
                return self.SVI_AMINE()
            else:
                FIELD = str(self.AMINE_INSP_NUM) + self.AMINE_INSP_EFF
            DFB_AMIN = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_AMINE(), FIELD)
            print(DFB_AMIN * pow(max(age,1.0),1.1))
            return DFB_AMIN * pow(max(age,1.0),1.1)
        else:
            return 0

    # Calculate Sulphide Stress Cracking
    def GET_ENVIRONMENTAL_SEVERITY(self):
        if (self.PH < 5.5):
            if  (self.H2SContent < 50):
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

    def DF_SULPHIDE(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.ENVIRONMENT_H2S_CONTENT):
            self.SULPHIDE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[4])
            self.SULPHIDE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber,self.DM_Name[4])
            if(age<1):
                return self.SVI_SULPHIDE()
            elif(self.SULPHIDE_INSP_EFF == "E" or self.SULPHIDE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.SULPHIDE_INSP_NUM) + self.SULPHIDE_INSP_EFF
            DFB_SULPHIDE = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_SULPHIDE(), FIELD)
            return DFB_SULPHIDE * pow(max(age,1.0),1.1)
        else:
            return 0

    # Calculate HIC/SOHIC-H2S
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
        elif (self.OnlineMonitoring == "Other corrosion - Key process variable" or self.OnlineMonitoring=="Other corrosion - Hydrogen probes"):
            return 2
        else:
            return 1

    def DF_HICSOHIC_H2S(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.ENVIRONMENT_H2S_CONTENT):
            self.SULFUR_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[5])
            self.SULFUR_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[5])
            if(age<1):
                return self.SVI_HICSOHIC_H2S()/self.FOM_HIC()
            elif (self.SULFUR_INSP_EFF == "E" or self.SULFUR_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.SULPHIDE_INSP_NUM) + self.SULFUR_INSP_NUM
            DFB_SULFUR = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HICSOHIC_H2S(), FIELD)
            return (DFB_SULFUR * pow(max(age,1.0), 1.1))/self.FOM_HIC()
        else:
            return 0

    # Calculate Cacbonate Cracking
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
                elif (7.5<= self.PH < 8):
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

    def DF_CACBONATE(self, age):
        if (self.CARBON_ALLOY and self.AQUEOUS_OPERATOR and self.PH >= 7.5):
            self.CACBONATE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[6])
            self.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[6])
            if(age<1):
                return self.SVI_CARBONATE()
            elif (self.CACBONATE_INSP_EFF == "E" or self.CACBONATE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CACBONATE_INSP_NUM) + self.CACBONATE_INSP_EFF
            DFB_CACBONATE = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CARBONATE(), FIELD)
            return DFB_CACBONATE * pow(max(age, 1.0), 1.1)
        else:
            return 0
    # Calculate PTA Cracking
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
                    elif (self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised Before Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Medium"
                    elif (self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised After Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Low"
                    elif (self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
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
                    elif (self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Medium"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised Before Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "High"
                    elif (self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (self.ThermalHistory == "Stabilised After Welding"):
                    if (self.PTAMaterial == "321 Stainless Steel"):
                        sus = "Low"
                    elif (self.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
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

    def DF_PTA(self, age):
        if (self.PTA_SUSCEP or ((self.CARBON_ALLOY or self.NICKEL_ALLOY) and self.EXPOSED_SULFUR)):
            self.PTA_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[7])
            self.PTA_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[7])
            if(age<1):
                return self.SVI_PTA()
            elif (self.PTA_INSP_EFF == "E" or self.PTA_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.PTA_INSP_NUM) + self.PTA_INSP_EFF
            DFB_PTA = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_PTA(), FIELD)
            return DFB_PTA * pow(age, 1.1)
        else:
            return 0

    # Calculate CLSCC
    def GET_SUSCEPTIBILITY_CLSCC(self):
        if (self.CRACK_PRESENT):
            sus = "High"
            return sus
        if (self.PH <= 10):
            if (self.MAX_OP_TEMP <=38):
                if(self.CHLORIDE_ION_CONTENT > 1000):
                    sus = "Medium"
                else:
                    sus = "High"
            elif(self.MAX_OP_TEMP > 38 and self.MAX_OP_TEMP <= 66):
                if(self.CHLORIDE_ION_CONTENT>=1 and self.CHLORIDE_ION_CONTENT<=10):
                    sus = "Low"
                elif(self.CHLORIDE_ION_CONTENT>1000):
                    sus = "High"
                else:
                    sus = "Medium"
            elif(self.MAX_OP_TEMP > 66 and self.MAX_OP_TEMP <= 93):
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
            if (self.MAX_OP_TEMP <=38):
                sus = "None"
            elif(self.MAX_OP_TEMP > 38 and self.MAX_OP_TEMP <= 93):
                sus = "Low"
            elif(self.MAX_OP_TEMP > 93 and self.MAX_OP_TEMP <= 149):
                if (self.CHLORIDE_ION_CONTENT >1000):
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

    def DF_CLSCC(self, age):
        if (self.INTERNAL_EXPOSED_FLUID_MIST and self.AUSTENITIC_STEEL and self.MAX_OP_TEMP > 38):
            self.CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[8])
            self.CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[8])
            if(age<1):
                return self.SVI_CLSCC()
            if (self.CLSCC_INSP_EFF == "E" or self.CLSCC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.CLSCC_INSP_NUM) + self.CLSCC_INSP_EFF
            DFB_CLSCC = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_CLSCC(), FIELD)
            return DFB_CLSCC * pow(age, 1.1)
        else:
            return 0

    # Calculate HSC-HF
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

    def DF_HSCHF(self, age):
        if (self.CARBON_ALLOY and self.HF_PRESENT):
            self.HSC_HF_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[9])
            self.HSC_HF_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[9])
            if(age<1):
                return self.SVI_HSCHF()
            if (self.HSC_HF_INSP_EFF == "E" or self.HSC_HF_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.HSC_HF_INSP_NUM) + self.HSC_HF_INSP_EFF
            DFB_HSCHF = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HSCHF(), FIELD)
            return DFB_HSCHF * pow(age, 1.1)
        else:
            return 0

    # Calculate HICSOHIC-HF
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

    def SVI_HICSOHIC_HF(self):
        if (self.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "High"):
            return 100
        elif (self.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "Medium"):
            return 10
        elif (self.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "Low"):
            return 1
        else:
            return 0

    def DF_HIC_SOHIC_HF(self, age):
        if (self.CARBON_ALLOY and self.HF_PRESENT):
            self.HICSOHIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[10])
            self.HICSOHIC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[10])
            if(age<1):
                return self.SVI_HICSOHIC_HF()/self.FOM_HIC()
            if (self.HICSOHIC_INSP_EFF == "E" or self.HICSOHIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(self.HICSOHIC_INSP_NUM) + self.HICSOHIC_INSP_EFF
            DFB_HICSOHIC_HF = DAL_CAL.POSTGRESQL.GET_TBL_74(self.SVI_HICSOHIC_HF(), FIELD)
            return DFB_HICSOHIC_HF * pow(age, 1.1)/self.FOM_HIC()
        else:
            return 0


    # Calculate EXTERNAL CORROSION
    def AGE_CLSCC(self):
        try:
            TICK_SPAN = abs((self.AssesmentDate.date() - self.COMPONENT_INSTALL_DATE.date()).days)
            return TICK_SPAN / 365
        except Exception as e:
            print(e)
        # if (self.EXTERN_COAT_QUALITY == "High coating quality"):
        #     AGE_COAT = self.COMPONENT_INSTALL_DATE + relativedelta(years=+15)  # Age + 15
        # elif (self.EXTERN_COAT_QUALITY == "Medium coating quality"):
        #     AGE_COAT = self.COMPONENT_INSTALL_DATE + relativedelta(years=+5)  # Age + 5
        # else:
        #     AGE_COAT = self.COMPONENT_INSTALL_DATE
        # TICK_SPAN = abs((self.AssesmentDate.date() - AGE_COAT.date()).days)
        #TICK_SPAN = abs((self.AssesmentDate.date()-self.COMPONENT_INSTALL_DATE.date()).days)
        #return TICK_SPAN / 365

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

    def API_ART_EXTERNAL(self, age):
        if (self.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1
        if (self.INTERFACE_SOIL_WATER): # cần kiểm tra lại điều kiện, hiện tại trong tinh toán FIP luôn =1
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

    def DF_EXTERNAL_CORROSION(self, age):
        if (self.EXTERNAL_EXPOSED_FLUID_MIST or (
        self.CARBON_ALLOY and not (self.MAX_OP_TEMP < -23 or self.MIN_OP_TEMP > 121))):
            self.EXTERNAL_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[11])
            self.EXTERNAL_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[11])
            self.NoINSP_EXTERNAL = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[11])
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
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(self.ComponentNumber, self.DM_Name[11])

        return a
    def NB_EXTERNAL(self):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(self.ComponentNumber, self.DM_Name[11])

        return b
    def NC_EXTERNAL(self):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(self.ComponentNumber, self.DM_Name[11])
        return c
    def ND_EXTERNAL(self):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(self.ComponentNumber, self.DM_Name[11])
        return d
    def I1_EXTERNAL(self):
        a=self.Pr_P1_EXTERNAL() * pow(0.9,self.NA_EXTERNAL()) * pow(0.7,self.NB_EXTERNAL()) * pow(0.5,self.NC_EXTERNAL()) * pow(0.4,self.ND_EXTERNAL())
        return self.Pr_P1_EXTERNAL() * pow(0.9,self.NA_EXTERNAL()) * pow(0.7,self.NB_EXTERNAL()) * pow(0.5,self.NC_EXTERNAL()) * pow(0.4,self.ND_EXTERNAL())
    def I2_EXTERNAL(self):
        a=self.Pr_P2_EXTERNAL() * pow(0.09,self.NA_EXTERNAL()) * pow(0.2,self.NB_EXTERNAL()) * pow(0.3,self.NC_EXTERNAL()) * pow(0.33,self.ND_EXTERNAL())
        return self.Pr_P2_EXTERNAL() * pow(0.09,self.NA_EXTERNAL()) * pow(0.2,self.NB_EXTERNAL()) * pow(0.3,self.NC_EXTERNAL()) * pow(0.33,self.ND_EXTERNAL())

    def I3_EXTERNAL(self):
        a = self.Pr_P3_EXTERNAL() * pow(0.01, self.NA_EXTERNAL()) * pow(0.1, self.NB_EXTERNAL()) * pow(0.2,
                                                                                                       self.NC_EXTERNAL()) * pow(
            0.27, self.ND_EXTERNAL())
        return self.Pr_P3_EXTERNAL() * pow(0.01, self.NA_EXTERNAL()) * pow(0.1, self.NB_EXTERNAL()) * pow(0.2,
                                                                                                          self.NC_EXTERNAL()) * pow(
            0.27, self.ND_EXTERNAL())
    def Po_P1_EXTERNAL(self):
        a=self.I1_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
        return self.I1_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
    def Po_P2_EXTERNAL(self):
        a = self.I2_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
        return self.I2_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
    def Po_P3_EXTERNAL(self):
        a=self.I3_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
        return self.I3_EXTERNAL()/(self.I1_EXTERNAL() + self.I2_EXTERNAL() + self.I3_EXTERNAL())
    def B1_EXTERNAL(self,age):
        return (1 - self.API_ART_EXTERNAL(age)- self.SRp_Thin())/math.sqrt(pow(self.API_ART_EXTERNAL(age), 2) * 0.04 + pow((1 - self.API_ART_EXTERNAL(age)), 2) * 0.04 + pow(self.SRp_Thin(), 2) * pow(0.05, 2))
    def B2_EXTERNAL(self,age):
        return (1- 2*self.API_ART_EXTERNAL(age)-self.SRp_Thin())/math.sqrt(pow(self.API_ART_EXTERNAL(age),2)*4*0.04 + pow(1-2*self.API_ART_EXTERNAL(age),2)*0.04+pow(self.SRp_Thin(),2)*pow(0.05,2))
    def B3_EXTERNAL(self,age):
        return (1- 4*self.API_ART_EXTERNAL(age)-self.SRp_Thin())/math.sqrt(pow(self.API_ART_EXTERNAL(age),2)*16*0.04 + pow(1-4*self.API_ART_EXTERNAL(age),2)*0.04+pow(self.SRp_Thin(),2)*pow(0.05,2))



    # Calculate CUI
    # def API_CUI_TEMP(self):
    #     if (self.EXTERNAL_EVIRONMENT == "Arid/dry"):
    #         CR_CUI = (self.CUI_PERCENT_3*0.025+self.CUI_PERCENT_4*0.025+self.CUI_PERCENT_5*0.051+self.CUI_PERCENT_6*0.025)/100
    #     elif(self.EXTERNAL_EVIRONMENT=="Marine"):
    #         CR_CUI = (self.CUI_PERCENT_2 * 0.025 + self.CUI_PERCENT_3 * 0.127 + self.CUI_PERCENT_4 * 0.127 + self.CUI_PERCENT_5 * 0.254 + self.CUI_PERCENT_6 * 0.127 + self.CUI_PERCENT_7 * 0.051 + self.CUI_PERCENT_8 * 0.025) / 100
    #     elif (self.EXTERNAL_EVIRONMENT == "Severe"):
    #         CR_CUI =(self.CUI_PERCENT_2*0.076+self.CUI_PERCENT_3*0.254+self.CUI_PERCENT_4*0.254+self.CUI_PERCENT_5*0.508+self.CUI_PERCENT_6*0.254+self.CUI_PERCENT_7*0.254+self.CUI_PERCENT_8*0.127)/100
    #     else:
    #         CR_CUI = (self.CUI_PERCENT_3*0.076+self.CUI_PERCENT_4*0.076+self.CUI_PERCENT_5*0.127+self.CUI_PERCENT_6*0.025+self.CUI_PERCENT_7*0.025)/100
    #     return CR_CUI
        # data = [-12, -8, 6, 32, 71, 107, 107, 135, 162, 176]
        # list = [self.CUI_PERCENT_1, self.CUI_PERCENT_2, self.CUI_PERCENT_3, self.CUI_PERCENT_4, self.CUI_PERCENT_5,
        #         self.CUI_PERCENT_6, self.CUI_PERCENT_7, self.CUI_PERCENT_8, self.CUI_PERCENT_9, self.CUI_PERCENT_10]
        # return data[list.index(max(list))]

    def API_CORROSION_RATE(self):
        if (self.EXTERNAL_EVIRONMENT == "Arid/dry"):
            CR_CUI = (self.CUI_PERCENT_3*0.025+self.CUI_PERCENT_4*0.025+self.CUI_PERCENT_5*0.051+self.CUI_PERCENT_6*0.025)/100
        elif(self.EXTERNAL_EVIRONMENT=="Marine"):
            CR_CUI = (self.CUI_PERCENT_2 * 0.025 + self.CUI_PERCENT_3 * 0.127 + self.CUI_PERCENT_4 * 0.127 + self.CUI_PERCENT_5 * 0.254 + self.CUI_PERCENT_6 * 0.127 + self.CUI_PERCENT_7 * 0.051 + self.CUI_PERCENT_8 * 0.051+self.CUI_PERCENT_9 * 0.025) / 100
        elif (self.EXTERNAL_EVIRONMENT == "Severe"):
            CR_CUI =(self.CUI_PERCENT_2*0.076+self.CUI_PERCENT_3*0.254+self.CUI_PERCENT_4*0.254+self.CUI_PERCENT_5*0.508+self.CUI_PERCENT_6*0.254+self.CUI_PERCENT_7*0.254+self.CUI_PERCENT_8*0.254+self.CUI_PERCENT_9 * 0.127)/100
        else:
            CR_CUI = (self.CUI_PERCENT_3*0.076+self.CUI_PERCENT_4*0.076+self.CUI_PERCENT_5*0.127+self.CUI_PERCENT_6*0.025+self.CUI_PERCENT_7*0.025)/100
        return CR_CUI

    def API_ART_CUI(self, age):
        if (self.INSULATION_TYPE == "Asbestos" or self.INSULATION_TYPE == "Calcium Silicate" or self.INSULATION_TYPE == "Mineral Wool" or self.INSULATION_TYPE == "Fibreglass"or self.INSULATION_TYPE == "Unknown/Unspecified"):
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
            #ART_CUI = max(1 - (self.CurrentThick - CR * self.AGE_CUI(age)) / (self.getTmin() + self.CA), 0)
            ART_CUI = (CR * self.AGE_CUI(age)) / self.trdi()
        except:
            ART_CUI = 1
        return self.API_ART(ART_CUI)

    def NA_FERRITIC(self):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(self.ComponentNumber, self.DM_Name[12])
        return a

    def NB_FERRITIC(self):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(self.ComponentNumber, self.DM_Name[12])
        return b

    def NC_FERRITIC(self):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(self.ComponentNumber, self.DM_Name[12])
        return c

    def ND_FERRITIC(self):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(self.ComponentNumber, self.DM_Name[12])
        return d

    def I1_FERRITIC(self):
        a = self.Pr_P1_EXTERNAL() * pow(0.9, self.NA_FERRITIC()) * pow(0.7, self.NB_FERRITIC()) * pow(0.5,self.NC_FERRITIC()) * pow(0.4, self.ND_FERRITIC())
        return self.Pr_P1_EXTERNAL() * pow(0.9, self.NA_FERRITIC()) * pow(0.7, self.NB_FERRITIC()) * pow(0.5,self.NC_FERRITIC()) * pow(0.4, self.ND_FERRITIC())

    def I2_FERRITIC(self):
        a = self.Pr_P2_EXTERNAL() * pow(0.09, self.NA_FERRITIC()) * pow(0.2, self.NB_FERRITIC()) * pow(0.3,self.NC_FERRITIC()) * pow(0.33, self.ND_FERRITIC())
        return self.Pr_P2_EXTERNAL() * pow(0.09, self.NA_FERRITIC()) * pow(0.2, self.NB_FERRITIC()) * pow(0.3,self.NC_FERRITIC()) * pow(0.33, self.ND_FERRITIC())

    def I3_FERRITIC(self):
        a = self.Pr_P3_EXTERNAL() * pow(0.01, self.NA_FERRITIC()) * pow(0.1, self.NB_FERRITIC()) * pow(0.2,self.NC_FERRITIC()) * pow(0.27, self.ND_FERRITIC())
        return self.Pr_P3_EXTERNAL() * pow(0.01, self.NA_FERRITIC()) * pow(0.1, self.NB_FERRITIC()) * pow(0.2,self.NC_FERRITIC()) * pow(0.27, self.ND_FERRITIC())

    def Po_P1_FERRITIC(self):
        return self.I1_FERRITIC() / (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())

    def Po_P2_FERRITIC(self):
        return self.I2_FERRITIC() / (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())

    def Po_P3_FERRITIC(self):
        return self.I3_FERRITIC() / (self.I1_FERRITIC() + self.I2_FERRITIC() + self.I3_FERRITIC())

    def B1_FERRITIC(self, age):
        a=(1 - self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 0.04 + pow((1 - self.API_ART_CUI(age)), 2) * 0.04 + pow(self.SRp_Thin(),
                                                                                                    2) * pow(0.05, 2))
        return (1 - self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 0.04 + pow((1 - self.API_ART_CUI(age)), 2) * 0.04 + pow(self.SRp_Thin(),
                                                                                                    2) * pow(0.05, 2))

    def B2_FERRITIC(self, age):
        b=(1 - 2 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 4 * 0.04 + pow(1 - 2 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))
        return (1 - 2 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 4 * 0.04 + pow(1 - 2 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))

    def B3_FERRITIC(self, age):
        c=(1 - 4 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 16 * 0.04 + pow(1 - 4 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))
        return (1 - 4 * self.API_ART_CUI(age) - self.SRp_Thin()) / math.sqrt(
            pow(self.API_ART_CUI(age), 2) * 16 * 0.04 + pow(1 - 4 * self.API_ART_CUI(age), 2) * 0.04 + pow(
                self.SRp_Thin(), 2) * pow(0.05, 2))

    def DF_CUI(self, age):
        if (self.EXTERNAL_EXPOSED_FLUID_MIST or (
                    self.CARBON_ALLOY and not (self.MAX_OP_TEMP < -12 or self.MIN_OP_TEMP > 177))):
            self.CUI_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[12])
            self.CUI_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[12])
            if (self.CUI_INSP_EFF == "" or self.CUI_INSP_NUM == 0):
                self.CUI_INSP_EFF = "E"
            if (self.APIComponentType == "TANKBOTTOM0" or self.APIComponentType == "TANKROOFFLOAT0"):
                if (self.NomalThick == 0 or self.CurrentThick == 0):
                    return 1390
                else:
                    return DAL_CAL.POSTGRESQL.GET_TBL_512(self.API_ART(self.API_ART_CUI(age)),self.CUI_INSP_NUM,self.CUI_INSP_EFF)
            else:
                if (self.NomalThick == 0 or self.CurrentThick == 0):
                    return 1900
                else:
                    try:
                        a = self.Po_P1_FERRITIC() * self.ncdf(- self.B1_FERRITIC(age))
                        b = self.Po_P2_FERRITIC() * self.ncdf(- self.B2_FERRITIC(age))
                        c = self.Po_P3_FERRITIC() * self.ncdf(- self.B3_FERRITIC(age))
                        s=(a + b + c) / (1.56 * pow(10, -4))
                        return (a + b + c) / (1.56 * pow(10, -4))
                    except Exception as e:
                        print(e)
                        return 0
        else:
            return 0

    # cal EXTERNAL CLSCC
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
        self.EXTERN_CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[13])
        self.EXTERN_CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[13])
        if (self.EXTERN_CLSCC_INSP_EFF == "E" or self.EXTERN_CLSCC_INSP_NUM == 0):
            FIELD = "E"
        else:
            FIELD = str(self.EXTERN_CLSCC_INSP_NUM) + self.EXTERN_CLSCC_INSP_EFF
        return DAL_CAL.POSTGRESQL.GET_TBL_74(SVI, FIELD)

    def DF_EXTERN_CLSCC(self, age):
        if (self.AUSTENITIC_STEEL and self.EXTERNAL_EXPOSED_FLUID_MIST and not (
                self.MAX_OP_TEMP < 49 or self.MIN_DESIGN_TEMP > 149)):
            if(age<1):
                return self.DFB_EXTERN_CLSCC()
            else:
                return self.DFB_EXTERN_CLSCC() * pow(self.AGE_CUI(age), 1.1)
        else:
            return 0

    # Calculate EXTERN CUI CLSCC
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

    def DFB_CUI_CLSCC(self):
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
            self.EXTERN_CLSCC_CUI_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[14])
            self.EXTERN_CLSCC_CUI_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[14])

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

    # Calculate HTHA
    def HTHA_PV(self, age):
        try:
            HTHA_AGE = age * 24 * 365
            log1 = math.log10(self.HTHA_PRESSURE / 0.0979)
            log2 = 3.09 * pow(10, -4) * (self.CRITICAL_TEMP + 273) * (math.log10(HTHA_AGE) + 14)
            return log1 + log2
        except:
            return 0

    def HTHA_SUSCEP(self, age):
        SUSCEP = ""
        if (self.HTHADamageObserved == 1):
            if (self.MAX_OP_TEMP > 177 and self.HTHA_PRESSURE >= 0.345):
                SUSCEP = "High"
            else:
                SUSCEP = "No"
        else:
            HTHA_PRESSURE_psia = self.HTHA_PRESSURE * 145;
            dataT = self.MAX_OP_TEMP * 9 / 5 + 32;
            TemperatureAdjusted = dataT + 20
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

    # def API_DF_HTHA(self, age):
    #     API_HTHA = DAL_CAL.POSTGRESQL.GET_TBL_204(self.HTHA_SUSCEP(age))
    #     self.HTHA_EFFECT = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[15])
    #     self.HTHA_NUM_INSP = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[15])
    #     if self.HTHA_NUM_INSP > 2:
    #         self.HTHA_NUM_INSP = 2
    #
    #     if (self.DAMAGE_FOUND):
    #         return 2000
    #     else:
    #         if (self.HTHA_NUM_INSP == 0):
    #             return API_HTHA[0]
    #         elif (self.HTHA_NUM_INSP == 1 and self.HTHA_EFFECT == "D"):
    #             return API_HTHA[1]
    #         elif (self.HTHA_NUM_INSP == 1 and self.HTHA_EFFECT == "C"):
    #             return API_HTHA[2]
    #         elif (self.HTHA_NUM_INSP == 1 and self.HTHA_EFFECT == "B"):
    #             return API_HTHA[3]
    #         elif (self.HTHA_NUM_INSP == 2 and self.HTHA_EFFECT == "D"):
    #             return API_HTHA[4]
    #         elif (self.HTHA_NUM_INSP == 2 and self.HTHA_EFFECT == "C"):
    #             return API_HTHA[5]
    #         else:
    #             return API_HTHA[6]

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

    # Calculate BRITTLE
    def DFB_BRIITLE(self):
        TEMP_BRITTLE = 0
        if(self.PRESSSURE_CONTROL):
            TEMP_BRITTLE=self.MIN_TEMP_PRESSURE
        else:
            TEMP_BRITTLE=self.CRITICAL_TEMP
        if (self.PWHT):
            return DAL_CAL.POSTGRESQL.GET_TBL_215(self.API_TEMP(TEMP_BRITTLE - self.REF_TEMP),
                                                 self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
        else:
            return DAL_CAL.POSTGRESQL.GET_TBL_214(self.API_TEMP(TEMP_BRITTLE - self.REF_TEMP),
                                                 self.API_SIZE_BRITTLE(self.BRITTLE_THICK))

    def DF_BRITTLE(self,i):
        try:
            Fse = 1
            if(self.BRITTLE_THICK<=12.7 or (self.FABRICATED_STEEL and self.EQUIPMENT_SATISFIED and self.NOMINAL_OPERATING_CONDITIONS
            and self.CET_THE_MAWP and self.CYCLIC_SERVICE and self.EQUIPMENT_CIRCUIT_SHOCK and (self.NomalThick <=50.8))):
                Fse = 0.01
            if (self.CARBON_ALLOY and (self.CRITICAL_TEMP < self.MIN_DESIGN_TEMP or self.MAX_OP_TEMP < self.MIN_DESIGN_TEMP)):
                # if (self.LOWEST_TEMP):
                print("Tempbrit",self.DFB_BRIITLE())
                return self.DFB_BRIITLE() * Fse
                # else:
                #     return self.DFB_BRIITLE()
            else:
                return 0
        except Exception as e:
            print(e)

    # Calculate TEMP EMBRITTLE
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

    def DF_TEMP_EMBRITTLE(self,i):
        if (self.TEMPER_SUSCEP and (self.CARBON_ALLOY and not (self.MAX_OP_TEMP < 343 or self.MIN_OP_TEMP > 577))):
            TEMP_EMBRITTLE = 0
            print("go temp")
            if (self.PRESSSURE_CONTROL):
                TEMP_EMBRITTLE = self.MIN_TEMP_PRESSURE - (self.REF_TEMP + self.DELTA_FATT)
            else:
                TEMP_EMBRITTLE = min(self.MIN_DESIGN_TEMP, self.CRITICAL_TEMP) - (self.REF_TEMP + self.DELTA_FATT)
            if (self.PWHT):
                return DAL_CAL.POSTGRESQL.GET_TBL_215(self.API_TEMP(TEMP_EMBRITTLE),
                                                     self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
            else:
                print(TEMP_EMBRITTLE, self.BRITTLE_THICK)
                return DAL_CAL.POSTGRESQL.GET_TBL_214(self.API_TEMP(TEMP_EMBRITTLE),
                                                     self.API_SIZE_BRITTLE(self.BRITTLE_THICK))
        else:
            return 0

    # Calculate 885w
    def DF_885(self,i):
        if (self.CHROMIUM_12 and not (self.MIN_OP_TEMP > 566 or self.MAX_OP_TEMP < 371)):
            TEMP_885 = 0
            if(self.PRESSSURE_CONTROL):
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

    # Calculate SIGMA
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

    # Calculate Pipping
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
        pip = ["PIPE-1", "PIPE-2", "PIPE-4", "PIPE-6", "PIPE-8", "PIPE-10", "PIPE-12","PIPE-16", "PIPEGT16"]
        check = False
        for a in pip:
            if self.APIComponentType == a:
                check = True
                break
        return check

    def DF_PIPE(self,i):
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
                # FJB = 1
                FJB = 0

            if (self.BRANCH_DIAMETER == "All branches greater than 2\" Nominal OD"):
                FBD = 0.02
            else:
                FBD = 1
            return self.DFB_PIPE() * FCA * FPC * FCP * FJB * FBD
        else:
            return 0


    ##################################################################################
    def GET_AGE_INSERVICE(self):
        return float((self.AssesmentDate.date() - self.CommissionDate.date()).days/365)

    def GET_AGE(self):
        age = np.zeros(21)#(0,14)
        for a in range(0,21):#(0,14)
            age[a] = DAL_CAL.POSTGRESQL.GET_AGE_INSP(self.ComponentNumber,self.DM_Name[a],self.CommissionDate, self.AssesmentDate)
        return age

    def DF_THINNING_API(self, i):
        # print("test THIN 1233-------")
        # print(self.GET_AGE()[0])
        # print(self.DF_THIN(self.GET_AGE()[0] + i))
        return self.DF_THIN(self.GET_AGE()[0] + i)

    def DF_LINNING_API(self, i):
        # print(self.DF_LINNING(self.GET_AGE()[1] + i))
        return self.DF_LINNING(self.GET_AGE()[1] + i)

    def DF_CAUTISC_API(self, i):
        return self.DF_CAUSTIC(self.GET_AGE()[2] + i)

    def DF_AMINE_API(self, i):
        return self.DF_AMINE(self.GET_AGE()[3] + i)

    def DF_SULPHIDE_API(self, i):
        return self.DF_SULPHIDE(self.GET_AGE()[4] + i)

    def DF_HICSOHIC_H2S_API(self, i):
        return self.DF_HICSOHIC_H2S(self.GET_AGE()[5] + i)

    def DF_CACBONATE_API(self,i):
        return self.DF_CACBONATE(self.GET_AGE()[6] + i)

    def DF_PTA_API(self,i):
        return self.DF_PTA(self.GET_AGE()[7] + i)

    def DF_CLSCC_API(self,i):
        return self.DF_CLSCC(self.GET_AGE()[8] + i)

    def DF_HSCHF_API(self, i):
        return self.DF_HSCHF(self.GET_AGE()[9] + i)

    def DF_HIC_SOHIC_HF_API(self, i):
        return self.DF_HIC_SOHIC_HF(self.GET_AGE()[10] + i)

    def DF_EXTERNAL_CORROSION_API(self, i):
        # print(self.DF_EXTERNAL_CORROSION(self.GET_AGE()[11] + i))
        return self.DF_EXTERNAL_CORROSION(self.GET_AGE()[11] + i)

    def DF_CUI_API(self, i):
        return self.DF_CUI(self.GET_AGE()[12] + i)

    def DF_EXTERN_CLSCC_API(self, i):
        return self.DF_EXTERN_CLSCC(self.GET_AGE()[13] + i)

    def DF_CUI_CLSCC_API(self,i):
        return self.DF_CUI_CLSCC(self.GET_AGE()[14] + i)

    def DF_HTHA_API(self, i):#chua test dc
        return self.DF_HTHA(self.GET_AGE()[15] + i)

    def DF_BRITTLE_API(self, i):
        return self.DF_BRITTLE(self.GET_AGE()[16] + i)

    def DF_TEMP_EMBRITTLE_API(self,i):
        return self.DF_TEMP_EMBRITTLE(self.GET_AGE()[17] + i)

    def DF_885_API(self,i):
        return self.DF_885(self.GET_AGE()[18] + i)

    def DF_SIGMA_API(self,i):
        return self.DF_SIGMA(self.GET_AGE()[19] + i)

    def DF_PIPE_API(self,i):
        return self.DF_PIPE(self.GET_AGE()[20] + i)

    # TOTAL ---------------------
    def DF_SSC_TOTAL_API(self, i):#done - con anie)
        DF_SCC = max(self.DF_CAUTISC_API(i), self.DF_AMINE_API(i), self.DF_SULPHIDE_API(i), self.DF_HIC_SOHIC_HF_API(i), self.DF_HICSOHIC_H2S_API(i),
                     self.DF_CACBONATE_API(i), self.DF_PTA_API(i), self.DF_CLSCC_API(i), self.DF_HSCHF(i))
        # print(self.DF_CAUTISC_API(i))
        # print(self.DF_AMINE_API(i))
        # print(self.DF_SULPHIDE_API(i))
        # print(self.DF_HIC_SOHIC_HF_API(i))
        # print(self.DF_HICSOHIC_H2S_API(i))
        # print(self.DF_CACBONATE_API(i))
        # print(self.DF_PTA_API(i))
        # print(self.DF_CLSCC_API(i))
        # print(self.DF_HSCHF(i))
        return DF_SCC

    def DF_EXT_TOTAL_API(self, i):#done
        DF_EXT = max(self.DF_EXTERNAL_CORROSION_API(i), self.DF_CUI_API(i),self.DF_EXTERN_CLSCC_API(i), self.DF_CUI_CLSCC_API(i))
        return DF_EXT
        #return 0.07

    def DF_BRIT_TOTAL_API(self,i):#done
        DF_BRIT = max(self.DF_BRITTLE_API(i) + self.DF_TEMP_EMBRITTLE_API(i), self.DF_SIGMA_API(i), self.DF_885_API(i))
        return DF_BRIT

    def DF_THINNING_TOTAL_API(self, i):#done
        try:
            if self.INTERNAL_LINNING and (self.DF_LINNING_API(i) != 0):
                DF_THINNING_TOTAL = min(self.DF_THINNING_API(i), self.DF_LINNING_API(i))
            else:
                DF_THINNING_TOTAL = self.DF_THINNING_API(i)
            return DF_THINNING_TOTAL
        except Exception as e:
            print(e, "erorr thin")

    def DF_RISK_CHART_THINNING(self):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = self.DF_THINNING_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_EXT(self):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = self.DF_EXT_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_SSC(self):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = self.DF_SSC_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_HTHA(self):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = self.DF_HTHA_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_BRIT(self):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = self.DF_BRIT_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_PIPE(self):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = self.DF_PIPE_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_TOTAL_API(self,i):#testing df_htha
        try:
            executor = ThreadPoolExecutor()
            DF_THINNING_TOTAL_API_Thread = executor.submit(self.DF_THINNING_TOTAL_API, i)
            DF_EXT_TOTAL_API_Thread = executor.submit(self.DF_EXT_TOTAL_API, i)
            DF_SSC_TOTAL_API_Thread = executor.submit(self.DF_SSC_TOTAL_API, i)
            DF_HTHA_API_Thread = executor.submit(self.DF_HTHA_API, i)
            DF_BRIT_TOTAL_API_Thread = executor.submit(self.DF_BRIT_TOTAL_API, i)
            DF_PIPE_API_Thread = executor.submit(self.DF_PIPE_API, i)

            DF_THINNING_TOTAL_API = DF_THINNING_TOTAL_API_Thread.result()
            DF_EXT_TOTAL_API = DF_EXT_TOTAL_API_Thread.result()
            DF_SSC_TOTAL_API = DF_SSC_TOTAL_API_Thread.result()
            DF_HTHA_API = DF_HTHA_API_Thread.result()
            DF_BRIT_TOTAL_API = DF_BRIT_TOTAL_API_Thread.result()
            DF_PIPE_API = DF_PIPE_API_Thread.result()

            TOTAL_DF_API = max(DF_THINNING_TOTAL_API, DF_EXT_TOTAL_API) + DF_SSC_TOTAL_API + DF_HTHA_API + DF_BRIT_TOTAL_API + DF_PIPE_API
            # TOTAL_DF_API = max(self.DF_THINNING_TOTAL_API(i), self.DF_EXT_TOTAL_API(i)) + self.DF_SSC_TOTAL_API(
            #     i) + self.DF_HTHA_API(i) + self.DF_BRIT_TOTAL_API(i) + self.DF_PIPE_API(i)
        except Exception as e:
            print(e)
        return TOTAL_DF_API

    def DF_TOTAL_GENERAL(self, i):#testing df_htha
        executor = ThreadPoolExecutor()
        DF_THINNING_TOTAL_API_Thread = executor.submit(self.DF_THINNING_TOTAL_API, i)
        DF_EXT_TOTAL_API_Thread = executor.submit(self.DF_EXT_TOTAL_API, i)
        DF_SSC_TOTAL_API_Thread = executor.submit(self.DF_SSC_TOTAL_API, i)
        DF_HTHA_API_Thread = executor.submit(self.DF_HTHA_API, i)
        DF_BRIT_TOTAL_API_Thread = executor.submit(self.DF_BRIT_TOTAL_API, i)
        DF_PIPE_API_Thread = executor.submit(self.DF_PIPE_API, i)

        DF_THINNING_TOTAL_API = DF_THINNING_TOTAL_API_Thread.result()
        DF_EXT_TOTAL_API = DF_EXT_TOTAL_API_Thread.result()
        DF_SSC_TOTAL_API = DF_SSC_TOTAL_API_Thread.result()
        DF_HTHA_API = DF_HTHA_API_Thread.result()
        DF_BRIT_TOTAL_API = DF_BRIT_TOTAL_API_Thread.result()
        DF_PIPE_API = DF_PIPE_API_Thread.result() 

        TOTAL_DF_API = DF_THINNING_TOTAL_API + DF_EXT_TOTAL_API + DF_SSC_TOTAL_API + DF_HTHA_API + DF_BRIT_TOTAL_API + DF_PIPE_API
        # TOTAL_DF_API = self.DF_THINNING_TOTAL_API(i) + self.DF_EXT_TOTAL_API(i) + self.DF_SSC_TOTAL_API(
        #     i) + self.DF_HTHA_API(i) + self.DF_BRIT_TOTAL_API(i) + self.DF_PIPE_API(i)
        # print( "DF_total",TOTAL_DF_API,i)
        return TOTAL_DF_API

    def convertRisk(self,risk):
        if risk >= 1:
            return 1
        else:
            return risk

    def DF_LIST_16_old(self, FC_Total, GFF, FSM, Risk_Target):
        # data = []
        # # data.append(Risk_Target)
        # a = 1
        # temp = 0
        # #for a in range(1, 16):
        # while (a < 16.0):
        #     risk=self.convertRisk( self.DF_TOTAL_API(a) * GFF * FSM) * FC_Total
        #     if temp==0:
        #         if risk >Risk_Target:
        #             temp=1
        #             minia=a-1+0.1
        #             # danh dau vi tri de tim risktarget data[1]
        #             data.insert(0, minia-0.1001)
        #             while minia<a:
        #                 data.append(self.convertRisk( self.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total)
        #             data.append(risk)
        #         else:
        #             if data[1]==Risk_Target:
        #                 data.append(risk)
        #                 temp = 1
        #                 minia = a + 0.1001
        #                 # danh dau vi tri de tim risktarget
        #                 data.insert(0, minia-0.1)
        #
        #                 while minia < a+1:
        #                     data.append(self.convertRisk(self.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total)
        #                     minia += 0.1
        #     else:
        #         data.append(risk)
        #     a += 1
        #
        data = []
        # data.append(Risk_Target)
        # for a in range(0.1,3.2,0.1):
        a = 1
        temp = 0
        # poin la diem giao voi risktarget gan nhat
        poin=-1
        while (a < 17.0):
            obj = {}
            obj['df_factor'] = self.DF_TOTAL_API(a)
            obj['pof'] = self.convertRisk(obj['df_factor'] * GFF * FSM)
            obj['risk'] = obj['pof'] * FC_Total

            if temp == 0 and obj['risk'] > Risk_Target:
                temp = 1
                minia = a - 1 + 1/12
                # danh dau vi tri de tim risktarget
                objTarget = {}
                objTarget['df_factor'] = -1
                objTarget['pof'] = -1
                objTarget['risk'] = minia - 1 / 12
                data.insert(0, objTarget)
                while minia < a-0.0001:
                    objNew = {}
                    objNew['df_factor'] = self.DF_TOTAL_API(minia)
                    objNew['pof'] = self.convertRisk(objNew['df_factor'] * GFF * FSM)
                    objNew['risk'] = objNew['pof'] * FC_Total
                    # risknew=self.convertRisk(self.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total
                    data.append(objNew)
                    # tim diem giao voi risktarget
                    if poin==-1:
                        if objNew['risk']>Risk_Target:
                            if minia-1/12>=0:
                                poin=minia-1/12
                            else:
                                poin = minia
                    #             xong
                    # print('minia' + str(minia))
                    minia += 1/12
                if poin == -1:
                    poin=minia - 1/12
                data.append(obj)

            else:
                data.append(obj)
            a += 1
            # print('a=' + str(a))
            # print('lengthdata')
            # print(len(data))
        if temp==0:
            temp = 1
            minia = 16+1/12
            # danh dau vi tri de tim risktarget
            objTarget = {}
            objTarget['df_factor'] = -1
            objTarget['pof'] = -1
            objTarget['risk'] = minia - 1 / 12
            data.insert(0, objTarget)

            while minia < a-0.0001:
                objNew = {}
                objNew['df_factor'] = self.DF_TOTAL_API(minia)
                objNew['pof'] = self.convertRisk(objNew['df_factor'] * GFF * FSM)
                objNew['risk'] = objNew['pof'] * FC_Total
                # risknew = self.convertRisk(self.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total
                data.append(objNew)
                # tim diem giao voi risktarget
                if poin == -1:
                    poin=16
                # xong
                # print('minia' + str(minia))
                minia += 1 / 12


        # luu poin vao truong cuoi cung cua database
        objPoin = {}
        objPoin['df_factor'] = -1
        objPoin['pof'] = -1
        objPoin['risk'] = poin
        data.append(objPoin)
        return data

    def DF_LIST_16_GENERAL_old(self, FC_Total, GFF, FSM, Risk_Target):
        data = []
        # data.append(Risk_Target)
        # for a in range(0.1,3.2,0.1):
        a=1
        temp=0
        # poin la diem giao voi risktarget gan nhat
        poin = -1
        while (a<17.0):
            obj={}
            obj['df_factor']=self.DF_TOTAL_GENERAL(a)
            obj['pof']=self.convertRisk(obj['df_factor'] * GFF * FSM)
            # print(obj['pof'])
            obj['risk']=obj['pof']*FC_Total
            # risk = self.convertRisk(self.DF_TOTAL_GENERAL(a) * GFF * FSM) * FC_Total
            # print('so sanh')
            # print(str(risk)+' '+str(Risk_Target)+' '+str(temp))
            if temp==0 and obj['risk'] >Risk_Target :
                temp=1
                minia=a-1+1/12
                # danh dau vi tri de tim risktarget
                objTarget = {}
                objTarget['df_factor'] = -1
                objTarget['pof'] = -1
                objTarget['risk'] = minia-1/12
                data.insert(0,objTarget)
                while minia<a-0.0001:
                    objNew = {}
                    objNew['df_factor'] = self.DF_TOTAL_GENERAL(minia)
                    objNew['pof'] = self.convertRisk(objNew['df_factor'] * GFF * FSM)
                    # print(GFF,FSM,obj['df_factor'],objNew['pof'],minia)
                    objNew['risk'] = objNew['pof'] * FC_Total

                    data.append(objNew)
                    # tim diem giao voi risktarget
                    if poin == -1:
                        if objNew['risk'] > Risk_Target:
                            if minia - 1/12 >= 0:
                                poin = minia - 1/12
                            else:
                                poin = minia
                                #             xong
                    # print('minia'+str(minia))
                    # print(objNew['risk'])
                    minia += 1/12
                if poin == -1:
                    poin=minia - 1/12
                data.append(obj)

            else:
                data.append(obj)
            a+=1

            # print('a='+str(a))
            # print('lengthdata')
            # print(len(data))
        if temp == 0:
            temp = 1
            minia = 16+1/12
            # danh dau vi tri de tim risktarget
            objTarget = {}
            objTarget['df_factor'] = -1
            objTarget['pof'] = -1
            objTarget['risk'] = minia - 1 / 12
            data.insert(0, objTarget)
            while minia < a-0.0001:
                objNew = {}
                objNew['df_factor'] = self.DF_TOTAL_GENERAL(minia)
                objNew['pof'] = self.convertRisk(objNew['df_factor'] * GFF * FSM)
                objNew['risk'] = objNew['pof'] * FC_Total
                # risknew = self.convertRisk(self.DF_TOTAL_GENERAL(minia) * GFF * FSM) * FC_Total
                data.append(objNew)
                # tim diem giao voi risktarget
                if poin == -1:
                    poin=16
                            #             xong
                # print('minia' + str(minia))
                # print(risknew)
                minia += 1 / 12

        # luu poin vao truong cuoi cung cua database
        objPoin = {}
        objPoin['df_factor'] = -1
        objPoin['pof'] = -1
        objPoin['risk'] = poin
        # print(poin)
        data.append(objPoin)
        # print('lengthdata')
        # print(len(data))
        return data

    def INSP_DUE_DATE(self, FC_Total, GFF, FSM, Risk_Target):
        DF_TARGET = Risk_Target/(FC_Total * GFF * FSM)
        # for a in range(1,16):
        for a in range(0,16):
            if self.DF_TOTAL_API(a) >= DF_TARGET:
                break
        if(a==15):
            return self.AssesmentDate + relativedelta(years=a+1)
        else:
            return self.AssesmentDate + relativedelta(years=a-1)

    def INSP_DUE_DATE_General(self, FC_total, GFF, FSM, Risk_Target):
        DF_TARGET = Risk_Target/(FC_total*GFF*FSM)
        # for a in range(1,16):
        for a in range(0,16):
            if self.DF_TOTAL_GENERAL(a) >= DF_TARGET:
                break
        if(a==15):
            return self.AssesmentDate + relativedelta(year=a+1)
        else:
            return self.AssesmentDate + relativedelta(year=a)

    def SEND_EMAIL(self, FC_Total, GFF, FSM, Risk_Target,ErrDammage,facilityname,request):
        try:
            DF_TARGET = Risk_Target/(FC_Total * GFF * FSM)
            if self.DF_TOTAL_API(0) >= DF_TARGET or self.DF_TOTAL_API(1) >= DF_TARGET:
                print("Send Email to Manage !!!!")
                email_subject = "Warning notice from " + str(facilityname) + " Facility .......!"
                message = "The following damage factors are very high and they need maintenance:\n"
                for da in ErrDammage:
                    DFm =models.DMItems.objects.get(dmitemid=da)
                    message += "  + "+str(DFm.dmdescription) + ".\n"
                message += "\n Email from Facility"
                #to_email = "doanhtuan14111997@gmail.com"
                if request.session['kind'] == 'factory':
                    UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
                    # print("check site")
                    # print(UserID)
                    to_email = models.ZUser.objects.get(id=UserID).email_service
                else:
                    to_email = "luongvancuongkmhd1998@cortekrbi.com"
                Email = EmailMessage(email_subject, message, to=[to_email])
                Email.send()
        except Exception as e:
            print(e)

    def ISDF(self):
        DM_ID = [8, 9, 61, 57, 73, 69, 60, 72, 62, 70, 67, 34, 32, 66, 63, 68, 2, 18, 1, 14, 10]
        data_mechanism = []
        DF_ITEM = np.zeros(21)
        DF_ITEM[0] = self.DF_THINNING_API(0)
        DF_ITEM[1] = self.DF_LINNING_API(0)
        DF_ITEM[2] = self.DF_CAUTISC_API(0)
        DF_ITEM[3] = self.DF_AMINE_API(0)
        DF_ITEM[4] = self.DF_SULPHIDE_API(0)
        DF_ITEM[5] = self.DF_HICSOHIC_H2S_API(0)
        DF_ITEM[6] = self.DF_CACBONATE_API(0)
        DF_ITEM[7] = self.DF_PTA_API(0)
        DF_ITEM[8] = self.DF_CLSCC_API(0)
        DF_ITEM[9] = self.DF_HSCHF_API(0)
        DF_ITEM[10] = self.DF_HIC_SOHIC_HF_API(0)
        DF_ITEM[11] = self.DF_EXTERNAL_CORROSION_API(0)
        DF_ITEM[12] = self.DF_CUI_API(0)
        DF_ITEM[13] = self.DF_EXTERN_CLSCC_API(0)
        DF_ITEM[14] = self.DF_CUI_CLSCC_API(0)
        DF_ITEM[15] = self.DF_HTHA_API(0)
        DF_ITEM[16] = self.DF_BRITTLE_API(0)
        DF_ITEM[17] = self.DF_TEMP_EMBRITTLE_API(0)
        DF_ITEM[18] = self.DF_885_API(0)
        DF_ITEM[19] = self.DF_SIGMA_API(0)
        DF_ITEM[20] = self.DF_PIPE_API(0)
        for i in range(0,21):
            if DF_ITEM[i] > 0:
                data_return = {}
                data_return['DF1'] = DF_ITEM[i]
                data_return['DM_ITEM_ID'] = DM_ID[i]
                data_return['isActive'] = 1
                data_return['i'] = i
                data_return['highestEFF'] = DAL_CAL.POSTGRESQL.GET_MAX_INSP(self.ComponentNumber, self.DM_Name[i])
                data_return['secondEFF'] = data_return['highestEFF']
                data_return['numberINSP'] = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(self.ComponentNumber, self.DM_Name[i])
                data_return['lastINSP'] = DAL_CAL.POSTGRESQL.GET_LAST_INSP(self.ComponentNumber, self.DM_Name[i], self.AssesmentDate)
                if i == 0:
                    data_return['DF2'] = self.DF_THINNING_API(3)
                    data_return['DF3'] = self.DF_THINNING_API(6)
                elif i == 1:
                    data_return['DF2'] = self.DF_LINNING_API(3)
                    data_return['DF3'] = self.DF_LINNING_API(6)
                elif i == 2:
                    data_return['DF2'] = self.DF_CAUTISC_API(3)
                    data_return['DF3'] = self.DF_CAUTISC_API(6)
                elif i == 3:
                    data_return['DF2'] = self.DF_AMINE_API(3)
                    data_return['DF3'] = self.DF_AMINE_API(6)
                elif i == 4:
                    data_return['DF2'] = self.DF_SULPHIDE_API(3)
                    data_return['DF3'] = self.DF_SULPHIDE_API(6)
                elif i == 5:
                    data_return['DF2'] = self.DF_HICSOHIC_H2S_API(3)
                    data_return['DF3'] = self.DF_HICSOHIC_H2S_API(6)
                elif i == 6:
                    data_return['DF2'] = self.DF_CACBONATE_API(3)
                    data_return['DF3'] = self.DF_CACBONATE_API(6)
                elif i == 7:
                    data_return['DF2'] = self.DF_PTA_API(3)
                    data_return['DF3'] = self.DF_PTA_API(6)
                elif i == 8:
                    data_return['DF2'] = self.DF_CLSCC_API(3)
                    data_return['DF3'] = self.DF_CLSCC_API(6)
                elif i == 9:
                    data_return['DF2'] = self.DF_HSCHF_API(3)
                    data_return['DF3'] = self.DF_HSCHF_API(6)
                elif i == 10:
                    data_return['DF2'] = self.DF_HIC_SOHIC_HF_API(3)
                    data_return['DF3'] = self.DF_HIC_SOHIC_HF_API(6)
                elif i == 11:
                    data_return['DF2'] = self.DF_EXTERNAL_CORROSION_API(3)
                    data_return['DF3'] = self.DF_EXTERNAL_CORROSION_API(6)
                elif i == 12:
                    data_return['DF2'] = self.DF_CUI_API(3)
                    data_return['DF3'] = self.DF_CUI_API(6)
                elif i == 15:
                    data_return['DF2'] = self.DF_HTHA_API(3)
                    data_return['DF3'] = self.DF_HTHA_API(6)
                else:
                    data_return['DF2'] = DF_ITEM[i]
                    data_return['DF3'] = DF_ITEM[i]
                data_mechanism.append(data_return)
        return data_mechanism

    def DF_LIST_16_GENERAL(self, FC_Total, GFF, FSM, Risk_Target):
        data = []
        a = 1
        temp = 0
        # poin la diem giao voi risktarget gan nhat
        poin = -1 
        def calRisk(a, FC_Total, GFF, FSM):
            obj = {}
            obj['df_factor'] = self.DF_TOTAL_GENERAL(a)
            obj['pof'] = self.convertRisk(obj['df_factor'] * GFF * FSM)
            obj['risk'] = obj['pof'] * FC_Total
            return a, obj
        def cal16Year():
            result16year ={}
            values = [*range(1, 17, 1)]
            with ThreadPoolExecutor(max_workers = 5) as executor:
                results = executor.map(calRisk, values, [FC_Total]*16 , [GFF]*16, [FSM]*16)
            for result in results:
                result16year[result[0]] = result[1]
            return result16year
        result16year = cal16Year() 
        while (a < 17.0):
            # obj = {}
            # obj['df_factor'] = self.DF_TOTAL_GENERAL(a)
            # obj['pof'] = self.convertRisk(obj['df_factor'] * GFF * FSM)
            # obj['risk'] = obj['pof']*FC_Total
            obj = {}
            obj['df_factor'] = result16year.get(a)['df_factor']
            obj['pof'] = result16year.get(a)['pof']
            obj['risk'] = result16year.get(a)['risk']
            if temp == 0 and obj['risk'] > Risk_Target:
                temp = 1
                minia = a-1+1/12
                # danh dau vi tri de tim risktarget
                objTarget = {}
                objTarget['df_factor'] = -1
                objTarget['pof'] = -1
                objTarget['risk'] = minia-1/12
                data.insert(0, objTarget)
                while minia < a-0.0001:
                    objNew = {}
                    objNew['df_factor'] = self.DF_TOTAL_GENERAL(minia)
                    objNew['pof'] = self.convertRisk(
                        objNew['df_factor'] * GFF * FSM)
                    # print(GFF,FSM,obj['df_factor'],objNew['pof'],minia)
                    objNew['risk'] = objNew['pof'] * FC_Total

                    data.append(objNew)
                    # tim diem giao voi risktarget
                    if poin == -1:
                        if objNew['risk'] > Risk_Target:
                            if minia - 1/12 >= 0:
                                poin = minia - 1/12
                            else:
                                poin = minia
                    minia += 1/12
                if poin == -1:
                    poin = minia - 1/12
                data.append(obj)

            else:
                data.append(obj)
            a += 1

        if temp == 0:
            temp = 1
            minia = 16+1/12
            # danh dau vi tri de tim risktarget
            objTarget = {}
            objTarget['df_factor'] = -1
            objTarget['pof'] = -1
            objTarget['risk'] = minia - 1 / 12
            data.insert(0, objTarget)
            while minia < a-0.0001:
                objNew = {}
                objNew['df_factor'] = self.DF_TOTAL_GENERAL(minia)
                objNew['pof'] = self.convertRisk(
                    objNew['df_factor'] * GFF * FSM)
                objNew['risk'] = objNew['pof'] * FC_Total
                # risknew = self.convertRisk(self.DF_TOTAL_GENERAL(minia) * GFF * FSM) * FC_Total
                data.append(objNew)
                # tim diem giao voi risktarget
                if poin == -1:
                    poin = 16
                    #             xong
                # print('minia' + str(minia))
                # print(risknew)
                minia += 1 / 12

        # luu poin vao truong cuoi cung cua database
        objPoin = {}
        objPoin['df_factor'] = -1
        objPoin['pof'] = -1
        objPoin['risk'] = poin
        data.append(objPoin)
        return data


    def DF_LIST_16(self, FC_Total, GFF, FSM, Risk_Target):
        data = []
        a = 1
        temp = 0
        # poin la diem giao voi risktarget gan nhat
        poin = -1
        def calRisk(a, FC_Total, GFF, FSM):
            obj = {}
            obj['df_factor'] = self.DF_TOTAL_API(a)
            obj['pof'] = self.convertRisk(obj['df_factor'] * GFF * FSM)
            obj['risk'] = obj['pof'] * FC_Total
            return a, obj
        def cal16Year():
            result16year ={}
            values = [*range(1, 17, 1)]
            with ThreadPoolExecutor(max_workers = 5) as executor:
                results = executor.map(calRisk, values, [FC_Total]*16 , [GFF]*16, [FSM]*16)
            for result in results:
                result16year[result[0]] = result[1]
            return result16year
        result16year = cal16Year() 
        while (a < 17.0):
            obj = {}
            obj['df_factor'] = result16year.get(a)['df_factor']
            obj['pof'] = result16year.get(a)['pof']
            obj['risk'] = result16year.get(a)['risk'] 
            if temp == 0 and obj['risk'] > Risk_Target:
                temp = 1
                minia = a - 1 + 1/12
                # danh dau vi tri de tim risktarget
                objTarget = {}
                objTarget['df_factor'] = -1
                objTarget['pof'] = -1
                objTarget['risk'] = minia - 1 / 12
                data.insert(0, objTarget)
                while minia < a-0.0001:
                    objNew = {}
                    objNew['df_factor'] = self.DF_TOTAL_API(minia)
                    objNew['pof'] = self.convertRisk(
                        objNew['df_factor'] * GFF * FSM)
                    objNew['risk'] = objNew['pof'] * FC_Total
                    # risknew=self.convertRisk(self.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total
                    data.append(objNew)
                    # tim diem giao voi risktarget
                    if poin == -1:
                        if objNew['risk'] > Risk_Target:
                            if minia-1/12 >= 0:
                                poin = minia-1/12
                            else:
                                poin = minia
                    #             xong
                    # print('minia' + str(minia))
                    minia += 1/12
                if poin == -1:
                    poin = minia - 1/12
                data.append(obj)

            else:
                data.append(obj)
            a += 1
        if temp == 0:
            temp = 1
            minia = 16+1/12
            # danh dau vi tri de tim risktarget
            objTarget = {}
            objTarget['df_factor'] = -1
            objTarget['pof'] = -1
            objTarget['risk'] = minia - 1 / 12
            data.insert(0, objTarget)

            while minia < a-0.0001:
                objNew = {}
                objNew['df_factor'] = self.DF_TOTAL_API(minia)
                objNew['pof'] = self.convertRisk(
                    objNew['df_factor'] * GFF * FSM)
                objNew['risk'] = objNew['pof'] * FC_Total
                # risknew = self.convertRisk(self.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total
                data.append(objNew)
                # tim diem giao voi risktarget
                if poin == -1:
                    poin = 16
                # xong
                # print('minia' + str(minia))
                minia += 1 / 12

        # luu poin vao truong cuoi cung cua database
        objPoin = {}
        objPoin['df_factor'] = -1
        objPoin['pof'] = -1
        objPoin['risk'] = poin
        data.append(objPoin)
        return data
    

#################   Caculate corrosion rate - CR    ################################

#####---- caculate soil side corrosion ----#####
    # caculate base corrosion rate
    # row1 = ["Sand", "Low Chlorides", "Homogeneous, finesilt or sand", "Dry, desert-like"]
    # row2 = ["Silt", "Moderate", "Mixed", "Variable moisture"]
    # row3 = ["Clay", "High Chlorides", "> 50% Gravel", "Normally saturated"]
    # def COUNTROW1(self):
    #     count = 0
    #     if (self.PRIMARY_SOIL_TYPE == self.row1[0]):
    #         count = 1
    #     else:
    #         count = 0
    #     if (self.LEVER_CHEMICCALS_CONTAMINANTS == self.row1[1]):
    #         count = count + 1
    #     else:
    #         count = count
    #     if (self.PARTICAL_SIZE_UNIFORMITY == self.row1[2]):
    #         count = count + 1
    #     else:
    #         count = count
    #     if (self.MOSTURE_LEVEL == self.row1[3]):
    #         count = count + 1
    #     else:
    #         count = count
    #     return count
    #
    # def COUNTROW2(self):
    #     count = 0
    #     if (self.PRIMARY_SOIL_TYPE == self.row2[0]):
    #         count = 1
    #     else:
    #         count = 0
    #     if (self.LEVER_CHEMICCALS_CONTAMINANTS == self.row2[1]):
    #         count = count + 1
    #     else:
    #         count = count
    #     if (self.PARTICAL_SIZE_UNIFORMITY == self.row2[2]):
    #         count = count + 1
    #     else:
    #         count = count
    #     if (self.MOSTURE_LEVEL == self.row3[3]):
    #         count = count + 1
    #     else:
    #         count = count
    #     return count
    #
    # def COUNTROW3(self):
    #     count = 0
    #     if (self.PRIMARY_SOIL_TYPE == self.row3[0]):
    #         count = 1
    #     else:
    #         count = 0
    #     if (self.LEVER_CHEMICCALS_CONTAMINANTS == self.row3[1]):
    #         count = count + 1
    #     else:
    #         count = count
    #     if (self.PARTICAL_SIZE_UNIFORMITY == self.row3[2]):
    #         count = count + 1
    #     else:
    #         count = count
    #     if (self.MOSTURE_LEVEL == self.row3[3]):
    #         count = count + 1
    #     else:
    #         count = count
    #     return count
    #
    # def BASE_CR(self):
    #     if (self.COUNTROW3()== 3 or self.COUNTROW3() == 4 or ( self.COUNTROW3() == 2 and self.COUNTROW1() == 1)):
    #         return 0.25
    #     elif (self.COUNTROW2() == 3 or self.COUNTROW2() == 4 or ( self.COUNTROW2() == 2 and self.COUNTROW1() == 1 )):
    #         return 0.13
    #     elif (self.COUNTROW1() == 3 or self.COUNTROW1() ==4 or (self.COUNTROW1() == 2 and self.COUNTROW2() == 1)):
    #         return 0.03
    #     elif (self.COUNTROW2() == 2 and self.COUNTROW3() == 2):
    #         return 0.178
    #     else:
    #         return 0.07
    #
    # def FSR_BASE_CR(self):
    #     if (self.SoilResistivity < 500):
    #         return 1.50
    #     elif ( 500 <= self.SoilResistivity <= 1000):
    #         return 1.25
    #     elif (1000 <= self.SoilResistivity <= 2000):
    #         return 1.00
    #     elif (2000 <= self.SoilResistivity <= 10000):
    #         return 0.83
    #     else:
    #         return 0.6
    #
    # def FT(self):
    #     if (49 < self.EquipmentTemperature < 104):
    #         return 2
    #     else:
    #         return 1
    #
    # def FCP(self):
    #     if (self.CATHODIC_PROTECTION_EFF == "No CP on structure (or CP exists but is not regularly tested per NACE RP0169  and  CP on an adjacent structure could cause stray current corrosion "):
    #         return 10.0
    #     elif (self.CATHODIC_PROTECTION_EFF == "No cathodic protection"):
    #         return 1.0
    #     elif (self.CATHODIC_PROTECTION_EFF  == "Cathodic protection exists, but is not tested each year or part of the structure is not inaccordance with any NACE RP0169 criteria"):
    #         return 0.8
    #     elif (self.CATHODIC_PROTECTION_EFF == "Cathodic protection is tested annually and is in accordance with NACE RP0169 “on” pontial criteria over entire structure"):
    #         return 0.4
    #     else:
    #         return 0.05
    # fce = he so coating effectiveness
    # def FCE(self):
    #     ce = 1.0
    #     if (self.COATING_TYPE == "Fusion Bonded Epoxy" or self.COATING_TYPE == "Liquid Epoxy"
    #           or self.COATING_TYPE == "Asphalt Enamel" or self.COATING_TYPE == "Asphalt Mastic"):
    #         if (self.BASE_COATING_TYPE):
    #             ce =  1.0
    #         if (self.AGE_COATING > 20):
    #             ce = ce * 1.1
    #         if (self.MAX_RATED_TEMP_EXCEEDED):
    #             ce = ce * 1.5
    #         if (self.COATING_MANTENANCE_RAREORNONE):
    #             ce = ce * 1.1
    #         return ce
    #     elif (self.COATING_TYPE == "Coal Tar Enamel"):
    #         if (self.BASE_COATING_TYPE):
    #             ce = 1.0
    #         if (self.AGE_COATING > 20):
    #             ce = ce * 1.2
    #         if (self.MAX_RATED_TEMP_EXCEEDED):
    #             ce = ce * 2.0
    #         if (self.COATING_MANTENANCE_RAREORNONE):
    #             ce = ce * 1.5
    #         return ce
    #     elif (self.COATING_TYPE == "Extruded Polyethylene with mastic or rubber"):
    #         if (self.BASE_COATING_TYPE):
    #             ce = 1.0
    #         if (self.AGE_COATING > 20):
    #             ce = ce * 1.2
    #         if (self.MAX_RATED_TEMP_EXCEEDED):
    #             ce = ce * 3.0
    #         if (self.COATING_MANTENANCE_RAREORNONE):
    #             ce = ce * 1.5
    #         return ce
    #     elif (self.COATING_TYPE == "Mill Applied PE Tape with mastic"):
    #         if (self.BASE_COATING_TYPE):
    #             ce = 1.5
    #         if (self.AGE_COATING > 20):
    #             ce = ce * 1.2
    #         if (self.MAX_RATED_TEMP_EXCEEDED):
    #             ce = ce * 3.0
    #         if (self.COATING_MANTENANCE_RAREORNONE):
    #             ce = ce * 1.5
    #         return ce
    #     elif (self.COATING_TYPE == "Field Applied PE Tape with mastic"):
    #         if (self.BASE_COATING_TYPE):
    #             ce = 2.0
    #         if (self.AGE_COATING > 20):
    #             ce = ce * 2.0
    #         if (self.MAX_RATED_TEMP_EXCEEDED):
    #             ce = ce * 3.0
    #         if (self.COATING_MANTENANCE_RAREORNONE):
    #             ce = ce * 1.5
    #         return ce
    #     elif (self.COATING_TYPE == "Three-Layer PE or PP"):
    #         if (self.BASE_COATING_TYPE):
    #             ce = 1.0
    #         if (self.AGE_COATING > 20):
    #             ce = ce * 1.2
    #         if (self.MAX_RATED_TEMP_EXCEEDED):
    #             ce = ce * 2.0
    #         if (self.COATING_MANTENANCE_RAREORNONE):
    #             ce = ce * 1.2
    #         return  ce
    #     else:
    #         return ce
    # caculate soil side corrosion rate
    # def SOIL_SIDE_CR(self):
    #     if (self.SoilResistivity_Considered_forbaseCR):
    #         return self.BASE_CR() * self.FSR_BASE_CR() * self.FT() * self.FCP()
    #     else:
    #         return self.BASE_CR() * self.FSR_BASE_CR() * self.FT() * self.FCP() * self.FCE()
    #






#####---- caculate tank bottom corrosion rate ----#####
    # soil side corrosion rate for tank bottom
    # def FSR(self):
    #     if (self.SoilResistivity < 500):
    #         return 1.5
    #     elif (500 < self.SoilResistivity < 1000 ):
    #         return 1.25
    #     elif (1000 < self.SoilResistivity < 2000):
    #         return 1.0
    #     elif (2000 < self.SoilResistivity < 10000):
    #         return 0.83
    #     elif ( self.SoilResistivity > 10000):
    #         return 0.66
    #     else:
    #         return 1.0
    #
    # def FPA(self):
    #     if (self.ASTPADTYPE == "Soil With High Salt" ):
    #         return 1.5
    #     elif (self.AST_PAD_TYPE == "Crushed Limestone"):
    #         return 1.4
    #     elif (self.AST_PAD_TYPE == "Native Soil"):
    #         return 1.3
    #     elif (self.AST_PAD_TYPE == "Construction Grade Sand"):
    #         return 1.15
    #     elif (self.AST_PAD_TYPE == "Continuous Asphalt"):
    #         return 1.0
    #     elif (self.AST_PAD_TYPE == " Continuous Concrete"):
    #         return 1.0
    #     else:
    #         return 0.7

    # def FTD(self):
    #     if (self.AST_DRAINAGE_TYPE == "One Third Frequently Underwater"):
    #         return 3
    #     elif (self.AST_DRAINAGE_TYPE == "Storm Water Collects At AST Base"):
    #         return 2
    #     else:
    #         return 1

    # def FCP(self):
    #     if (self.CATHODIC_PROTECTION_TYPE == "None"):
    #         return 1.0
    #     elif (self.CATHODIC_PROTECTION_TYPE == "Yes Not Per API 651"):
    #         return 0.66
    #     else:
    #         return 0.33

    # def FTB(self):
    #     if (self.AST_PAD_TYPE_BOTTOM == "RPB Not Per API 650"):
    #         return 1.4
    #     else:
    #         return 1.0

    # def FST(self):
    #     if (self.SoilSideTemperature <= 24):
    #         return 1.0
    #     elif (24 < self.SoilSideTemperature <= 66):
    #         return 1.1
    #     elif (66 < self.SoilSideTemperature <=93):
    #         return 1.3
    #     elif (93 < self.SoilSideTemperature <= 121):
    #         return 1.4
    #     else:
    #         return 1.0
    # def CR_S(self):
    #     if self.CR_SB == 0:
    #         return 0.13 * self.FSR() * self.FPA() * self.FTD() * self.FCP() * self.FTB() * self.FST()
    #     else:
    #         return self.CR_SB * self.FSR() * self.FPA() * self.FTD() * self.FCP() * self.FTB() * self.FST()

    ### product side corrosion rate for tank bottom

    # def FPC(self):
    #     if self.PRODUCT_SIDE_CONDITION== "Wet":
    #         return 2.5
    #     else:
    #         return 1.0
    # def FPT(self):
    #     if self.ProductSideTemp <= 24 :
    #         return 1.0
    #     elif 24<self.ProductSideTemp <= 66 :
    #         return 1.1
    #     elif 66<self.ProductSideTemp<=93 :
    #         return 1.3
    #     elif 93<self.ProductSideTemp<=121 :
    #         return 1.4
    #     else:
    #         return 1.0
    # def FSC(self):
    #     if self.STRAM_COIL :
    #         return 1.15
    #     else:
    #         return 1.0
    # def FWD(self):
    #     if self.WATER_DRAW_OFF:
    #         return 0.7
    #     else:
    #         return 1.0
        # product side corrosion rate
    # def CR_P(self):
    #     if self.CR_PB == 0:
    #         return 0.05 * self.FPC() * self.FPT() * self.FSC() * self.FWD()
    # def FinalEstimated_CR(self):
    #     if self.ProductSideBottomCR == "Widespread":
    #         return max(self.CR_S(),self.CR_P())
    #     else:
    #         return self.CR_S()+self.CR_P()









import time
import time
import math
from builtins import property
from datetime import datetime
import  numpy as np
from dateutil.relativedelta import relativedelta
from pathlib import _Selector
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL


#file tinh toan toc do an mon

class CO_CAL:
    # ham khoi tao
    def __init__(self,SoilResistivity="", ASTPADTYPE="", AST_DRAINAGE_TYPE="", CATHODIC_PROTECTION_TYPE="",
                 AST_PAD_TYPE_BOTTOM="",SoilSideTemperature="",crsb=0,PRODUCT_SIDE_CONDITION="",ProductSideTemp="",STRAM_COIL="",
                 WATER_DRAW_OFF = "", crpb=0, ProductSideBottomCR=""):

        self.SoilResistivity = SoilResistivity
        self.ASTPADTYPE = ASTPADTYPE
        self.AST_DRAINAGE_TYPE = AST_DRAINAGE_TYPE
        self.CATHODIC_PROTECTION_TYPE =CATHODIC_PROTECTION_TYPE
        self.AST_PAD_TYPE_BOTTOM = AST_PAD_TYPE_BOTTOM
        self.SoilSideTemperature = SoilSideTemperature
        self.crsb =crsb

        self.PRODUCT_SIDE_CONDITION = PRODUCT_SIDE_CONDITION
        self.ProductSideTemp = ProductSideTemp
        self.STRAM_COIL = STRAM_COIL
        self.WATER_DRAW_OFF = WATER_DRAW_OFF
        self.crpb = crpb
        self.ProductSideBottomCR = ProductSideBottomCR



    def FSR(self):
        if (self.SoilResistivity == "Very Corrosive (<500 Ω-centimeter)"):
            return 1.50
        elif (self.SoilResistivity == "Corrosive (500-1000 Ω-cm)"):
            return 1.25
        elif (self.SoilResistivity == "Moderetly Corrosive (1000-2000 Ω-cm)"):
            return 1.00
        elif (self.SoilResistivity == "Mildly Corrosive (2000-10000 Ω-cm)"):
            return 0.83
        else:
            return 0.66

    def FPA(self):
        if (self.ASTPADTYPE == "Soil With High Salt"):
            return 1.5
        elif (self.ASTPADTYPE == "Crushed Limestone"):
            return 1.4
        elif (self.ASTPADTYPE == "Native Soil"):
            return 1.3
        elif (self.ASTPADTYPE == "Construction Grade Sand"):
            return 1.15
        elif (self.ASTPADTYPE == "Continuous Asphalt"):
            return 1.0
        elif (self.ASTPADTYPE == " Continuous Concrete"):
            return 1.0
        else:
            return 0.7

    def FTD(self):
        if (self.AST_DRAINAGE_TYPE == "One Third Frequently UnderWater"):
            return 3
        elif (self.AST_DRAINAGE_TYPE == "Storm Water Collects At AST Base"):
            return 2
        else:
            return 1

    def FCP(self):
        if (self.CATHODIC_PROTECTION_TYPE == "None"):
            return 1.0
        elif (self.CATHODIC_PROTECTION_TYPE == "Yes Not Per API 651"):
            return 0.66
        else:
            return 0.33

    def FTB(self):
        if (self.AST_PAD_TYPE_BOTTOM == "RPB Not Per API 650"):
            return 1.4
        else:
            return 1.0

    def FST(self):
        if (self.SoilSideTemperature =="Temp ≤ 24"):
            return 1.0
        elif (self.SoilSideTemperature =="24 < Temp ≤ 66"):
            return 1.1
        elif (self.SoilSideTemperature =="66 < Temp ≤ 93"):
            return 1.3
        elif (self.SoilSideTemperature == "92 < Temp ≤ 121"):
            return 1.4
        else:
            return 1.0

    def CR_SB(self,crsb):
        if crsb == 0:
            return 0.13
        else:
            return crsb

    def CR_S(self):
        if self.CR_SB(crsb=self.crsb) == 0:
            return 0.13 * self.FSR() * self.FPA() * self.FTD() * self.FCP() * self.FTB() * self.FST()
        else:
            return self.CR_SB(crsb=self.crsb) * self.FSR() * self.FPA() * self.FTD() * self.FCP() * self.FTB() * self.FST()

    ### product side corrosion rate for tank bottom

    def FPC(self):
        if self.PRODUCT_SIDE_CONDITION == "Wet":
            return 2.5
        else:
            return 1.0

    def FPT(self):
        if (self.ProductSideTemp =="Temp ≤ 24"):
            return 1.0
        elif (self.ProductSideTemp =="24 < Temp ≤ 66"):
            return 1.1
        elif (self.ProductSideTemp =="66 < Temp &le; 93"):
            return 1.3
        elif (self.ProductSideTemp =="92 < Temp ≤ 121"):
            return 1.4
        else:
            return 1.0

    def FSC(self):
        if (self.STRAM_COIL == "Yes"):
            return 1.15
        else:
            return 1.0

    def FWD(self):
        if (self.WATER_DRAW_OFF =="Yes"):
            return 0.7
        else:
            return 1.0

        # product side corrosion rate
    def CR_PB(self,crpb):
        if crpb == 0:
            return 0.5
        else:
            return crpb

    def CR_P(self):
        if (self.CR_PB(crpb=self.crpb) == 0):
            return 0.05 * self.FPC() * self.FPT() * self.FSC() * self.FWD()
        else:
            return self.CR_PB(crpb=self.crpb)*self.FPC() * self.FPT() * self.FSC() * self.FWD()

    def FinalEstimated_CR(self):
        if (self.ProductSideBottomCR == "Localised"):
            return max(self.CR_S(), self.CR_P())
        else:
            return self.CR_S() + self.CR_P()
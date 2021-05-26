import math
import numpy as np
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL
from cloud import models

class CA_Toxic: #LEVEL 1
    def __init__(self,proposalID,TOXIC_FLUID,ReleasePhase,toxic_percent,API_COMPONENT_TYPE_NAME,model_fluid,store_pressure):
        self.proposalID = proposalID
        self.TOXIC_FLUID = TOXIC_FLUID
        self.ReleasePhase =ReleasePhase
        self.toxic_percent = toxic_percent
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.model_fluid = model_fluid
        self.store_pressure=store_pressure

    def ld_n_max(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i==1:
            return rwcofholesize.ld_max_n_small
        elif i==2:
            return rwcofholesize.ld_max_n_medium
        elif i==3:
            return rwcofholesize.ld_max_n_large
        else:
            return rwcofholesize.ld_max_n_rupture

    def mass_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.mass_n_small
        elif i == 2:
            return rwcofholesize.mass_n_medium
        elif i == 3:
            return rwcofholesize.mass_n_large
        else:
            return rwcofholesize.mass_n_rupture

    def W_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.wn_small
        elif i == 2:
            return rwcofholesize.wn_medium
        elif i == 3:
            return rwcofholesize.wn_large
        else:
            return rwcofholesize.wn_rupture

    def ReleasetType(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.releasetype_small
        elif i == 2:
            return rwcofholesize.releasetype_medium
        elif i == 3:
            return rwcofholesize.releasetype_large
        else:
            return rwcofholesize.releasetype_rupture
    def ld_tox_n(self,i):
        try:
            return min(3600,(self.mass_n(i)/self.W_n(i)),(60*self.ld_n_max(i)))
        except:
            return 0

    def ContantC(self,i):
        if self.model_fluid == "HF Acid":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i)/60)<5:
                    return 1.1401
                elif (self.ld_tox_n(i)/60)<10:
                    return 1.1031
                elif (self.ld_tox_n(i)/60)<20:
                    return 1.0816
                elif (self.ld_tox_n(i)/60)<40:
                    return 1.0942
                elif (self.ld_tox_n(i)/60)<60:
                    return 1.103
            else:
                return 1.4056
        elif self.model_fluid == "H2S":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i)/60)<5:
                    return 1.2411
                elif (self.ld_tox_n(i)/60)<10:
                    return 1.241
                elif (self.ld_tox_n(i)/60)<20:
                    return 1.237
                elif (self.ld_tox_n(i)/60)<40:
                    return 1.2297
                elif (self.ld_tox_n(i)/60)<60:
                    return 1.2266
            else:
                return 0.974
        else:
            return 0

    def ContantD(self,i):
        if self.model_fluid == "HF Acid":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 3.5683
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3.8431
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4.104
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 4.3295
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 4.4576
            else:
                return 3.306
        elif self.model_fluid == "H2S":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 3.9686
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 4.0948
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4.238
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 4.3626
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 4.4365
            else:
                return 2.784
        else:
            return 0

    def ContantE(self,i):
        if self.model_fluid == "Ammonia":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 636.7
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 846.3
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 1053
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1256
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 1455
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 1650
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 1842
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 2029
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 2213
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 2389
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 2558
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 2714
            else:
                return 2684
        elif self.model_fluid == "Chlorine":
            if self.ReleasetType(i) == "Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 3350
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3518
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 3798
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4191
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 4694
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 5312
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 6032
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 6860
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 7788
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 8798
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 9890
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 10994
            else:
                return 3528
        elif self.model_fluid == "AlCl3" :
            if self.ReleasePhase=="Gas" :
                if (self.ld_tox_n(i)/60)<1.5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 3.4531
            else:
                if (self.ld_tox_n(i)/60)<1.5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 3.4531
        elif self.model_fluid == "CO" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 9.55
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 60.09
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 189.42
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 651.49
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1252.67
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1521.89
            else:
                return 0
        elif self.model_fluid == "HCl" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 47.39
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 123.67
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 531.45
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 224.55
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 950.92
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 2118.87
            else:
                return 0
        elif self.model_fluid == "Nitric Acid" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 13230.9
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 17146
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 23851.3
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 31185
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 35813.7
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 38105.8
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1114.96
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 2006.1
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 2674.47
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4112.65
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 6688.99
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 9458.29
        elif self.model_fluid == "NO2" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1071.74
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1466.57
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1902.9
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 2338.76
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 3621.1
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 4070.48
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 430
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 649.49
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1340.93
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3020.54
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 6110.67
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 9455.68
        elif self.model_fluid == "Phosgene" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 3095.33
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 5918.49
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 12129.3
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 27459.6
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 63526.4
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 96274.2
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 733.39
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1520.02
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 4777.72
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 14727.5
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 42905
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 77287.7
        elif self.model_fluid == "TDI" :
            if self.ReleasePhase=="Liquid":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 793.04
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 846.54
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1011.9
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1026.06
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1063.8
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1063.8
            else:
                return 0
        elif self.model_fluid == "EE" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0.8954
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.7578
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 4.0002
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 7.54
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 24.56
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 31.22
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 59.67
            else:
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.6857
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3.6389
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 9.8422
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 23.513
        elif self.model_fluid == "EO" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0.5085
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 2.972
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 7.9931
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 47.69
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 237.57
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1088.4
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1767.5
            else:
                return 0
        elif self.model_fluid == "PO" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0.0008
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0.0008
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.0864
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.1768
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.4172
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.9537
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.2289
            else:
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 2.4084
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 9.0397
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 17.425
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 34.255
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 367.06
        else:
            return 0

    def ContantF(self,i):
        if self.model_fluid == "Ammonia":
            if self.ReleasePhase=="Gas" and self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 1.183
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.181
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 1.18
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.178
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 1.176
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 1.174
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 1.172
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.169
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 1.166
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 1.161
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 1.155
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.145
            else:
                return 0.9011
        elif self.model_fluid == "Chlorine":
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 1.097
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.095
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 1.092
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.089
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 1.085
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 1.082
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 1.077
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.072
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 1.066
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 1.057
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 1.046
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.026
            else:
                return 1.177
        elif self.model_fluid == "AlCl3":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.9411
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.9411
        elif self.model_fluid == "CO":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.15
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.13
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.11
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.17
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.21
            else:
                return 0
        elif self.model_fluid == "HCl":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.09
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.15
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.1
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.18
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.2
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.23
            else:
                return 0
        elif self.model_fluid == "Nitric Acid":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.25
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.25
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.24
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.23
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.22
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.22
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.08
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.02
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.12
        elif self.model_fluid == "NO2":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 0.7
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.68
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.68
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.72
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.7
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.71
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 0.98
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.04
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.07
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.08
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.12
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.13
        elif self.model_fluid == "Phosgene":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.2
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.29
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.24
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.27
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.3
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.31
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.1
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.12
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.16
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.2
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.23
        elif self.model_fluid == "TDI":
            if self.ReleasePhase=="Liquid":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.09
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.1
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.03
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 793.04
                else:
                    return 0
        elif self.model_fluid == "EE":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 1.171
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.181
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.122
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.111
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.971
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.995
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.899
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.105
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.065
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.132
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.104
        elif self.model_fluid == "EO":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 1.222
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.207
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.271
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.2909
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.2849
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.1927
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.203
            else:
                return 0
        elif self.model_fluid == "PO":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 1.913
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.913
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.127
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.2203
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.2164
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.2097
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.2522
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.198
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.111
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.114
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.118
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.9855
        else:
            return 0

    def ContantC_toxic2(self,i):
        if self.TOXIC_FLUID == "HF Acid":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i)/60)<5:
                    return 1.1401
                elif (self.ld_tox_n(i)/60)<10:
                    return 1.1031
                elif (self.ld_tox_n(i)/60)<20:
                    return 1.0816
                elif (self.ld_tox_n(i)/60)<40:
                    return 1.0942
                elif (self.ld_tox_n(i)/60)<60:
                    return 1.103
            else:
                return 1.4056
        elif self.TOXIC_FLUID == "H2S":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i)/60)<5:
                    return 1.2411
                elif (self.ld_tox_n(i)/60)<10:
                    return 1.241
                elif (self.ld_tox_n(i)/60)<20:
                    return 1.237
                elif (self.ld_tox_n(i)/60)<40:
                    return 1.2297
                elif (self.ld_tox_n(i)/60)<60:
                    return 1.2266
            else:
                return 0.974
        else:
            return 0

    def ContantD_toxic2(self,i):
        if self.TOXIC_FLUID == "HF Acid":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 3.5683
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3.8431
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4.104
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 4.3295
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 4.4576
            else:
                return 3.306
        elif self.TOXIC_FLUID == "H2S":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 3.9686
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 4.0948
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4.238
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 4.3626
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 4.4365
            else:
                return 2.784
        else:
            return 0

    def ContantE_toxic2(self,i):
        if self.TOXIC_FLUID == "Ammonia":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 636.7
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 846.3
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 1053
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1256
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 1455
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 1650
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 1842
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 2029
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 2213
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 2389
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 2558
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 2714
            else:
                return 2684
        elif self.TOXIC_FLUID == "Chlorine":
            if self.ReleasetType(i) == "Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 3350
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3359
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 3798
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4191
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 4694
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 5312
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 6032
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 6860
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 7788
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 8798
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 9890
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 10994
            else:
                return 3528
        elif self.TOXIC_FLUID == "AlCl3" :
            if self.ReleasePhase=="Gas" :
                if (self.ld_tox_n(i)/60)<1.5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 3.4531
            else:
                if (self.ld_tox_n(i)/60)<1.5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 3.4531
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 3.4531
        elif self.TOXIC_FLUID == "CO" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 9.55
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 60.09
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 189.42
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 651.49
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1252.67
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1521.89
            else:
                return 0
        elif self.TOXIC_FLUID == "HCl" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 47.39
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 123.67
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 531.45
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 224.55
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 950.92
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 2118.87
            else:
                return 0
        elif self.TOXIC_FLUID == "Nitric Acid" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 13230.9
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 17146
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 23851.3
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 31185
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 35813.7
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 38105.8
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1114.96
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 2041.91
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 2674.47
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 4112.65
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 6688.99
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 9458.29
        elif self.TOXIC_FLUID == "NO2" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1071.74
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1466.57
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1902.9
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 2338.76
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 3621.1
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 4070.48
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 430
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 610.31
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1340.93
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3020.54
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 6110.67
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 9455.68
        elif self.TOXIC_FLUID == "Phosgene" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 3095.33
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 5918.49
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 12129.3
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 27459.6
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 63526.4
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 96274.2
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 733.39
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1520.02
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 4777.72
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 14727.5
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 42905
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 77287.7
        elif self.TOXIC_FLUID == "TDI" :
            if self.ReleasePhase=="Liquid":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 793.04
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 846.54
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1011.9
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1026.06
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1063.8
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1063.8
            else:
                if (self.ld_tox_n(i)/60)<1.5:
                    return 793.04
                else:
                    return 0
        elif self.TOXIC_FLUID == "EE" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0.8954
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.7578
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 4.0002
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 7.54
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 24.56
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 31.22
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 59.67
            else:
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.6857
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 3.6389
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 9.8422
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 23.513
        elif self.TOXIC_FLUID == "EO" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0.5085
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 2.972
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 7.9931
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 47.69
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 237.57
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1088.4
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1767.5
            else:
                return 0
        elif self.TOXIC_FLUID == "PO" :
            if self.ReleasePhase=="Gas":
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0.0008
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0.0008
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.0864
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.1768
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.4172
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.9537
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.2289
            else:
                if (self.ld_tox_n(i) / 60)<1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 2.4084
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 9.0397
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 17.425
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 34.255
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 367.06
        else:
            return 0

    def ContantF_toxic2(self,i):
        if self.TOXIC_FLUID == "Ammonia":
            if self.ReleasetType(i) == "Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 1.183
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.181
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 1.18
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.178
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 1.176
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 1.174
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 1.172
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.169
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 1.166
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 1.161
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 1.155
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.145
            else:
                return 0.9011
        elif self.TOXIC_FLUID == "Chlorine":
            if self.ReleasetType(i)=="Continuous":
                if (self.ld_tox_n(i) / 60) < 5:
                    return 1.097
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.095
                elif (self.ld_tox_n(i) / 60) < 15:
                    return 1.092
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.089
                elif (self.ld_tox_n(i) / 60) < 25:
                    return 1.085
                elif (self.ld_tox_n(i) / 60) < 30:
                    return 1.082
                elif (self.ld_tox_n(i) / 60) < 35:
                    return 1.077
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.072
                elif (self.ld_tox_n(i) / 60) < 45:
                    return 1.066
                elif (self.ld_tox_n(i) / 60) < 50:
                    return 1.057
                elif (self.ld_tox_n(i) / 60) < 55:
                    return 1.046
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.026
            else:
                return 1.177
        elif self.TOXIC_FLUID == "AlCl3":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.9411
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.9411
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.9411
        elif self.TOXIC_FLUID == "CO":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.15
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.13
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.11
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.17
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.21
            else:
                return 0
        elif self.TOXIC_FLUID == "HCl":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.09
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.15
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.1
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.18
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.2
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.23
            else:
                return 0
        elif self.TOXIC_FLUID == "Nitric Acid":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.25
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.25
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.24
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.23
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.22
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.22
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.08
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.02
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.12
        elif self.TOXIC_FLUID == "NO2":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 0.7
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0.68
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 0.68
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.72
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.7
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.71
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 0.98
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.04
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.07
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.08
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.12
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.13
        elif self.TOXIC_FLUID == "Phosgene":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.2
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.29
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.24
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.27
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.3
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.31
            else:
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.1
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.12
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.16
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.2
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.23
        elif self.TOXIC_FLUID == "TDI":
            if self.ReleasePhase=="Liquid":
                if (self.ld_tox_n(i) / 60) < 3:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.09
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.1
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.06
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.03
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 793.04
                else:
                    return 0
        elif self.TOXIC_FLUID == "EE":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 1.171
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.181
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.122
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.111
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 0.971
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 0.995
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.899
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.105
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.065
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.132
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.104
        elif self.TOXIC_FLUID == "EO":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 1.222
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.207
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.271
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.2909
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.2849
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.1927
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.203
            else:
                return 0
        elif self.TOXIC_FLUID == "PO":
            if self.ReleasePhase == "Gas":
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 1.913
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 1.913
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.127
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.2203
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.2164
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.2097
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 1.2522
            else:
                if (self.ld_tox_n(i) / 60) < 1.5:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 3:
                    return 0
                elif (self.ld_tox_n(i) / 60) < 5:
                    return 1.198
                elif (self.ld_tox_n(i) / 60) < 10:
                    return 1.111
                elif (self.ld_tox_n(i) / 60) < 20:
                    return 1.114
                elif (self.ld_tox_n(i) / 60) < 40:
                    return 1.118
                elif (self.ld_tox_n(i) / 60) < 60:
                    return 0.9855
        else:
            return 0
    def mfrac_tox(self):
        return self.toxic_percent

    def Rate_tox_n(self,i):
        return (1-self.mfrac_tox()/100) * self.W_n(i)
    def Mass_tox_n(self,i):
        return self.mass_n(i) * (1-self.mfrac_tox()/100)
    def Rate_tox_n_toxic(self,i):
        return (self.mfrac_tox() * self.W_n(i))/100
    def Mass_tox_n_toxic(self,i):
        return (self.mass_n(i) * self.mfrac_tox())/100

    def CA_injn_tox2(self,i):
        try:
            C8 = 0.0929
            C4 = 2.205
            if self.toxic_percent==0:
                return 0
            else:
                if self.TOXIC_FLUID == "HF Acid" or self.TOXIC_FLUID == "H2S":
                    if self.ReleasetType(i)=="Continuous":
                        return C8*math.pow(10,self.ContantC_toxic2(i)*math.log10(C4*self.Rate_tox_n_toxic(i))+self.ContantD_toxic2(i))
                    else:
                        return C8*math.pow(10,self.ContantC_toxic2(i)*math.log10(C4*self.Mass_tox_n_toxic(i))+self.ContantD_toxic2(i))
                elif self.TOXIC_FLUID=="Ammonia" or self.TOXIC_FLUID=="Chlorine":
                    if self.ReleasetType(i)=="Continuous":
                        return self.ContantE_toxic2(i)*math.pow(self.Rate_tox_n_toxic(i),self.ContantF_toxic2(i))
                    else:
                        return self.ContantE_toxic2(i)*math.pow(self.Mass_tox_n_toxic(i),self.ContantF_toxic2(i))
                elif self.TOXIC_FLUID=="AlCl3" or self.TOXIC_FLUID=="CO" or self.TOXIC_FLUID=="HCl" or self.TOXIC_FLUID=="Nitric Acid" or self.TOXIC_FLUID=="NO2" or self.TOXIC_FLUID=="Phosgene" or self.TOXIC_FLUID=="TDI" or self.TOXIC_FLUID=="EE" or self.TOXIC_FLUID=="EO" or self.TOXIC_FLUID=="PO":
                    if self.ReleasetType(i)=="Continuous":
                        return self.ContantE_toxic2(i)*math.pow(self.Rate_tox_n_toxic(i),self.ContantF_toxic2(i))
                    else:
                        return self.ContantE_toxic2(i)*math.pow(self.Rate_tox_n_toxic(i),self.ContantF_toxic2(i))
                else:
                    return 0
        except Exception as e:
            print(e)


    def CA_toxic_inj2(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            # print(obj)
            #print('ca_injn',(obj[0] * self.CA_injn_tox2(1) + obj[1] * self.CA_injn_tox2(2) + obj[2] * self.CA_injn_tox2(3) + obj[3] * self.CA_injn_tox2(4)) / obj[4])
            return (obj[0] * self.CA_injn_tox2(1) + obj[1] * self.CA_injn_tox2(2) + obj[2] * self.CA_injn_tox2(3) + obj[3] * self.CA_injn_tox2(4)) / obj[4]
        except Exception as e:
            print("CA_toxic_inj2",e)

    def CA_injn_tox(self,i):
        try:
            C8 = 0.0929
            C4 = 2.205
            if self.model_fluid == "HF Acid" or self.model_fluid == "H2S":
                if self.ReleasetType(i)=="Continuous":
                    return C8*math.pow(10,self.ContantC(i)*math.log10(C4*self.Rate_tox_n(i))+self.ContantD(i))
                else:
                    return C8*math.pow(10,self.ContantC(i)*math.log10(C4*self.Mass_tox_n(i))+self.ContantD(i))
            elif self.model_fluid=="Ammonia" or self.model_fluid=="Chlorine":
                if self.ReleasetType(i)=="Continuous":
                    return self.ContantE(i)*math.pow(self.Rate_tox_n(i),self.ContantF(i))*1000
                else:
                    return self.ContantE(i)*math.pow(self.Mass_tox_n(i),self.ContantF(i))*1000
            elif self.model_fluid=="AlCl3" or self.model_fluid=="CO" or self.model_fluid=="HCl" or self.model_fluid=="Nitric Acid" or self.model_fluid=="NO2" or self.model_fluid=="Phosgene" or self.model_fluid=="TDI" or self.model_fluid=="EE" or self.model_fluid=="EO" or self.model_fluid=="PO":
                if self.ReleasetType(i)=="Continuous":
                    return self.ContantE(i)*math.pow(self.Rate_tox_n(i),self.ContantF(i))
                else:
                    return self.ContantE(i)*math.pow(self.Rate_tox_n(i),self.ContantF(i))
            else:
                return 0
        except Exception as e:
            print(e)


    def CA_toxic_inj(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0] * self.CA_injn_tox(1) + obj[1] * self.CA_injn_tox(2) + obj[2] * self.CA_injn_tox(3) + obj[3] * self.CA_injn_tox(4)) / obj[4]
        except Exception as e:
            return 0
            print("CA_toxic_inj",e)

    #None FLA and Non Toxic

    def Rate_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i == 1:
            return rwcofholesize.rate_n_small
        elif i == 2:
            return rwcofholesize.rate_n_medium
        elif i == 3:
            return rwcofholesize.rate_n_large
        else:
            return rwcofholesize.rate_n_rupture

    def NoneCA_cont_Inj_n(self,i):
        C9 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(9)
        if self.store_pressure<163:
            num=163
        else:
            if self.store_pressure>590:
                num=590
            else:
                num=self.store_pressure
        g=(2696-(3.1754999999999995*(num-101.325)))+(1.474*math.pow((0.145*(num-101.325)),2))
        h=0.31-(0.00032*math.pow(0.145*(num-101.325)-40,2))
        if self.model_fluid=="Steam":
            return 0.123*self.Rate_n(i)
        elif self.model_fluid=="Acid" or self.model_fluid=="Caustic":
            return (0.01858*g)*math.pow(2.205*self.Rate_n(i),h)
        else :
            return 0


    def NoneCA_Inst_Inj_n(self,i):
        C10 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(10)
        if self.model_fluid=="Steam":
            return 9.774 * math.pow(self.mass_n(i),0.6384)
        else:
            return 0

    def Fact_IC(self,i):
        if self.model_fluid=="Steam":
            return min(self.Rate_n(i)/25.2,1)
        else:
            return 0

    def NoneCA_leck_Inj_n(self,i):
        try:
            return self.NoneCA_Inst_Inj_n(i)*self.Fact_IC(i)+self.NoneCA_cont_Inj_n(i)*(1-self.Fact_IC(i))
        except:
            return 0

    def NoneCA_leck(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0] * self.NoneCA_leck_Inj_n(1) + obj[1] * self.NoneCA_leck_Inj_n(2) + obj[2] * self.NoneCA_leck_Inj_n(3) + obj[3] * self.NoneCA_leck_Inj_n(4)) / obj[4]
        except:
            return 0

    def CA_total(self, flammable_cmd,flammable_inj):
        cainj = max(flammable_inj,self.CA_toxic_inj(),self.NoneCA_leck())
        cacmd = max(self.CA_toxic_inj2(),cainj)
        return max(flammable_cmd,cacmd)

    def CA_Category(self,flammable_cmd,flammable_inj):
        if (self.CA_total(flammable_cmd,flammable_inj) <= 9.29):
            return "A"
        elif (self.CA_total(flammable_cmd,flammable_inj) <= 92.9):
            return "B"
        elif (self.CA_total(flammable_cmd,flammable_inj) <= 279):
            return "C"
        elif (self.CA_total(flammable_cmd,flammable_inj) <= 929):
            return "D"
        else:
            return "E"
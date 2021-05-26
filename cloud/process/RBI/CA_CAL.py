import math
import numpy as np
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL

class CA_NORMAL: #LEVEL 1
    def __init__(self, NominalDiametter = 0, MATERIAL_COST = 0, FLUID = "", FLUID_PHASE = "", API_COMPONENT_TYPE_NAME ="", DETECTION_TYPE = "",
                 ISOLATION_TYPE = "", STORED_PRESSURE = 0, ATMOSPHERIC_PRESSURE = 0, STORED_TEMP = 0, MASS_INVERT = 0,
                 MASS_COMPONENT = 0, MITIGATION_SYSTEM = "", TOXIC_PERCENT = 0, RELEASE_DURATION = "", PRODUCTION_COST = 0,
                 INJURE_COST = 0, ENVIRON_COST = 0, PERSON_DENSITY = 0, EQUIPMENT_COST = 0, TOXIC_PHASE = "",
                 MAX_OPERATING_TEMP = 0, TOXIC_FLUID = ""):
        self.NominalDiametter = NominalDiametter
        self.MATERIAL_COST = MATERIAL_COST
        self.FLUID = FLUID
        self.FLUID_PHASE = FLUID_PHASE
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.DETECTION_TYPE = DETECTION_TYPE
        self.ISOLATION_TYPE = ISOLATION_TYPE
        self.STORED_PRESSURE = STORED_PRESSURE
        self.ATMOSPHERIC_PRESSURE = ATMOSPHERIC_PRESSURE
        self.STORED_TEMP = STORED_TEMP
        self.MASS_INVERT = MASS_INVERT
        self.MASS_COMPONENT = MASS_COMPONENT
        self.MITIGATION_SYSTEM = MITIGATION_SYSTEM
        self.TOXIC_PERCENT = TOXIC_PERCENT
        self.RELEASE_DURATION = RELEASE_DURATION
        self.PRODUCTION_COST = PRODUCTION_COST
        self.INJURE_COST = INJURE_COST
        self.ENVIRON_COST = ENVIRON_COST
        self.PERSON_DENSITY = PERSON_DENSITY
        self.EQUIPMENT_COST = EQUIPMENT_COST
        self.TOXIC_PHASE = TOXIC_PHASE
        self.MAX_OPERATING_TEMP = MAX_OPERATING_TEMP #moi them vao
        self.TOXIC_FLUID = TOXIC_FLUID #moi them vAO

    # C1 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(1)
    # C2 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(2)
    # C3 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(3)
    def FC_Category(self, fc):
        if (fc <= 10000):
            return "A"
        elif (fc <= 100000):
            return "B"
        elif (fc <= 1000000):
            return "C"
        elif (fc <= 10000000):
            return "D"
        else:
            return "E"

    def CA_Category(self, ca):
        if (ca <= 9.29):
            return "A"
        elif (ca <= 92.9):
            return "B"
        elif (ca <= 279):
            return "C"
        elif (ca <= 929):
            return "D"
        else:
            return "E"
    #### ham lay cac gia tri consequence analysis properties

    def auto_ignition_temp(self):
        try:
            tbl52 = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            return tbl52[9]  # doi tu do K sang do C
        except Exception as e:
            print(e)
            return 0

    def liquid_density(self):
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        return data[1] * 16.02
        # return data[1]

    def ideal_gas_ratio(self):
        if self.FLUID == "HCl":
            return 1.41
        elif self.FLUID == "Nitric Acid" or self.FLUID == "NO2" or self.FLUID == "Phosgene" or self.FLUID == "TDI":
            return 1.5
        else:
            return max(self.C_P() / (self.C_P() - 8.314), 1.01)

    def ambient(self):
        return DAL_CAL.POSTGRESQL.GET_RELEASE_PHASE(self.FLUID)

    def moleculer_weight(self):
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        return data[0]

    def gff(self, i):
        try:
            if not (self.FLUID is None):
                obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
                if (i == 1):
                    return obj[0]
                elif (i == 2):
                    return obj[1]
                elif (i == 3):
                    return obj[2]
                else:
                    return obj[3]
            else:
                return 0
        except Exception as e:
            print(e)
    def model_fluid_type(self):
        fluidtype  = DAL_CAL.POSTGRESQL.GET_MODEL_FLUID_TYPE(self.FLUID)
        return fluidtype
    def model_toxic_type(self):
        toxictype = DAL_CAL.POSTGRESQL.GET_TOXIC_FLUID_TYPE(self.TOXIC_FLUID)
        return  toxictype

    def NBP(self):
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        nbp  = ((data[2] -32)/1.8)
        return nbp

    def TYPE_FLUID(self): #done
        try:
            API_TYPE = "TYPE 0"
            if (self.FLUID is None):
                API_TYPE = "TYPE 0"
            else:
                if(self.FLUID == "C1-C2" or self.FLUID == "C13-C16" or self.FLUID == "C17-C25" or self.FLUID =="C25+" or
                   self.FLUID == "C3-C4" or self.FLUID == "C5" or self.FLUID == "C6-C8" or self.FLUID == "C9-C12" or
                   self.FLUID == "Acid" or self.FLUID == "AlCl3" or self.FLUID == "H2" or self.FLUID == "H2S" or self.FLUID == "HCl" or
                   self.FLUID == "HF" or self.FLUID == "Nitric Acid" or self.FLUID == "NO2" or self.FLUID == "Phosgene" or
                   self.FLUID == "Pyrophoric" or self.FLUID == "Steam" or self.FLUID == "TDI" or self.FLUID == "Water" or self.FLUID =="Ammonia"
                   or self.FLUID == "Chorine"):
                    API_TYPE = "TYPE 0"
                elif(self.FLUID == "CO" or self.FLUID == "DEE" or self.FLUID == "EE" or self.FLUID == "EEA" or self.FLUID == "EG" or
                     self.FLUID == "EO" or self.FLUID == "Methanol" or self.FLUID == "PO" or self.FLUID == "Styrene" or self.FLUID == "Aromatics"):
                    API_TYPE = "TYPE 1"
                else:
                    API_TYPE = "TYPE 0"
            return API_TYPE
        except Exception as e:
            print(e)
            print('exception at type fluid')

    def GET_DATA_API_COM(self):  #done
        try:
            return DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        except Exception as e:
            print(e)
            print('exception at get_data_api_com')

    def GET_RELEASE_PHASE(self): #done
        try:
            return self.FLUID_PHASE
        except Exception as e:
            print(e)
            print('exception at GET_RELEASE_PHASE')

    def d_n(self, i): #checked
        try:
            if(i == 1):
                return 6.4
            elif(i == 2):
                return 25
            elif(i == 3):
                return 102
            else:
                return min(self.NominalDiametter , 406)
        except Exception as e:
            print(e)
            print('exception at d_n')

    def a_n(self, i): #checked #dung
        if not (self.FLUID is None):
            return math.pi * pow(self.d_n(i),2) / 4
        else:
            return 0

    def C_P(self): #checked #ideal gas specific heat capacity
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            t = self.MAX_OPERATING_TEMP + 273.15
            if (t != 0):
                CP_C2 = round((data[6] / t) / ( math.sinh(data[6] / t)),5)
                CP_E2 = round((data[8] / t) / ( math.cosh(data[8] / t)),5)
                if (data[3] == 1):
                    return data[4] + data[5] * t + data[6] * pow(t, 2) + data[7] * pow(t, 3)
                elif(data[3] == 2):
                    return data[4] + data[5] * CP_C2 * CP_C2 + data[6] * CP_E2 * CP_E2
                elif(data[3] == 3):
                    return data[4] + data[5] * t + data[6] * pow(t, 2) + data[7] * pow(t, 3) + data[8] * pow(t, 4)
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            print(e)
            print('exception at C_p')

    def ReleasePhase(self):

        if (self.ambient()=="Liquid") and (self.FLUID_PHASE=="Liquid"):
            return "Liquid"
        elif self.FLUID=="C1-C2" or self.FLUID=="C3-C4" or self.FLUID=="HCl" or self.FLUID=="H2" or self.FLUID=="H2S" or self.FLUID=="HF" or self.FLUID == "CO" or self.FLUID=="EO" or self.FLUID=="Ammonia" or self.FLUID=="Chlorine":
            print('self.FLUID',self.FLUID)
            return "Gas"
        elif self.FLUID_PHASE == "Gas":
            return "Gas"
        elif self.NBP()<=300:
            return "Liquid"
        else:
            return "Gas"

    def W_n(self, i):   #checking
        try:
            C1 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(1)
            # C2 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(2)
            if (self.ReleasePhase() != "Liquid"):
                print('vao')
                R = 8.314
                k = self.ideal_gas_ratio()
                p_trans = 101.325 * pow((k + 1) / 2, k / (k - 1))
                if (self.STORED_PRESSURE > p_trans):
                    x = ((k * self.moleculer_weight() / (R * (self.MAX_OPERATING_TEMP+273.15))) * pow(2 / (k + 1), (k + 1) / (k - 1)))
                    return round(0.0009 * self.a_n(i) * self.STORED_PRESSURE * math.sqrt(x),5)
                else:
                    x = (self.moleculer_weight() / (R * (self.MAX_OPERATING_TEMP+273.15))) * ((2 * k) / (k - 1)) * pow(
                        101.325 / self.STORED_PRESSURE, 2 / k) * (
                        1 - pow(self.ATMOSPHERIC_PRESSURE / self.STORED_PRESSURE, (k - 1) / k))
                    return round(0.0009 * self.a_n(i) * self.STORED_PRESSURE * math.sqrt(x),5)
            else:
                return round(0.61 * self.liquid_density() * (self.a_n(i) / C1) * math.pow((2 * (self.STORED_PRESSURE - 101.325)) / self.liquid_density(), 1 / 2),5)

        except Exception as e :
            return 0
            print(e)
            print('exception at def w_n')


    def W_max8(self,i): #done
        try:
            C1 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(1)
            # C2 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(2)
            if (i == 4 ):
                if (self.ReleasePhase() != "Liquid"):
                    R = 8.314
                    k = self.ideal_gas_ratio()
                    p_trans = 101.325 * pow((k + 1) / 2, k / (k - 1))
                    if (self.STORED_PRESSURE > p_trans):
                        x = (
                            (k * self.moleculer_weight() / (R * (self.MAX_OPERATING_TEMP + 273.15))) * pow(2 / (k + 1),(k + 1) / (k - 1)))
                        return 0.0009 * 32450 * self.STORED_PRESSURE * math.sqrt(x)
                    else:
                        x = (self.moleculer_weight() / (R * (self.MAX_OPERATING_TEMP + 273.15))) * (
                        (2 * k) / (k - 1)) * pow(
                            101.325 / self.STORED_PRESSURE, 2 / k) * (
                                1 - pow(self.ATMOSPHERIC_PRESSURE / self.STORED_PRESSURE, (k - 1) / k))
                        return 0.0009 * 32450 * self.STORED_PRESSURE * math.sqrt(x)
                else:
                    return 0.61 * self.liquid_density() * (32450 / C1) * math.pow((2 * (self.STORED_PRESSURE - 101.325)) / self.liquid_density(), 1 / 2)
            else:
                if (self.ReleasePhase() != "Liquid"):
                    R = 8.314
                    k = self.ideal_gas_ratio()
                    p_trans = 101.325 * pow((k + 1) / 2, k / (k - 1))
                    if (self.STORED_PRESSURE > p_trans):
                        x = (
                        (k * self.moleculer_weight() / (R * (self.MAX_OPERATING_TEMP+273.15))) * pow(2 / (k + 1), (k + 1) / (k - 1)))
                        return 0.0009 * self.a_n(i) * self.STORED_PRESSURE * math.sqrt(x)
                    else:
                        x = (self.moleculer_weight() / (R * (self.MAX_OPERATING_TEMP+273.15))) * ((2 * k) / (k - 1)) * pow(
                            101.325 / self.STORED_PRESSURE, 2 / k) * (
                            1 - pow(self.ATMOSPHERIC_PRESSURE / self.STORED_PRESSURE, (k - 1) / k))
                        return 0.0009 * self.a_n(i) * self.STORED_PRESSURE * math.sqrt(x)
                else:
                    return 0.61 * self.liquid_density() * (self.a_n(i) / C1) * math.pow((2 * (self.STORED_PRESSURE - 101.325)) / self.liquid_density(), 1 / 2)

        except Exception as e :
            # return 0
            print(e)
            print('exception at def w_n')

    def mass_addn(self, i): #checked
        try:
            if (self.a_n(i) == 0):
                return 0
            else:
                return 180 * min(self.W_n(i),self.W_max8(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at mass_addn')

    def mass_avail_n(self, i): #checked
        try:
            return self.MASS_INVERT
        except Exception as e:
            print(e)
            return 0

    def t_n(self, i): #checked
        try:
            wn = self.W_n(i)
            if(wn == 0):
                return 0
            else:
                return (DAL_CAL.POSTGRESQL.GET_TBL_3B21(3)) / wn
        except Exception as e:
            print(e)
            print('exception at def t_n')

    def releaseType(self, i):#done
        if not (self.FLUID is None):
            try:
                tn = self.t_n(i)
                obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME) #lay gff
                mass_n = self.mass_n(i)
                c3 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(3)
                if (obj[i] == obj[1]):
                    return "Continuous"
                if (((tn > 180) and (mass_n <= c3 )) and ((tn > 180) and (mass_n < c3))):
                    return "Continuous"
                return  "Instantaneous"
            except Exception as e:
                print(e)
                print('exception at releasetype')
        else:
            return 'NotApplicable'

    def fact_di(self):#checked
        try:
            if (self.DETECTION_TYPE == "A" and self.ISOLATION_TYPE == "A"):
                return 0.25
            elif(self.DETECTION_TYPE == "A" and self.ISOLATION_TYPE == "B"):
                return 0.2
            elif((self.DETECTION_TYPE == "A" or self.DETECTION_TYPE == "B") and self.ISOLATION_TYPE == "C"):
                return 0.1
            elif((self.ISOLATION_TYPE == "A" or  self.ISOLATION_TYPE == "B") and self.DETECTION_TYPE == "B"):
                return 0.15
            else:
                return 0
        except Exception as e:
            print(e)
            print('exception at fact_di')

    def ld_n_max(self, i):#checked
        try:
            if not(self.FLUID is None):
                massavail=self.mass_avail_n(i)
                rate=self.rate_n(i)
                dn = self.d_n(i)
                if (self.DETECTION_TYPE == "A" and self.ISOLATION_TYPE == "A"):
                    if (dn == 6.4):
                        ld_max = 20
                    elif (dn == 25):
                        ld_max = 10
                    elif (dn == 102):
                        ld_max = 5
                    else:
                        ld_max = round((massavail/rate)/60,5)
                elif(self.DETECTION_TYPE == "A" and self.ISOLATION_TYPE == "B"):
                    if (dn == 6.4):
                        ld_max = 30
                    elif (dn == 25):
                        ld_max = 20
                    elif (dn == 102):
                        ld_max = 10
                    else:
                        ld_max = 1
                elif(self.DETECTION_TYPE == "A" and self.ISOLATION_TYPE == "C"):
                    if (dn == 6.4):
                        ld_max = 40
                    elif (dn == 25):
                        ld_max = 30
                    elif (dn == 102):
                        ld_max = 20
                    else:
                        ld_max = round((massavail/rate)/60,5)
                elif((self.ISOLATION_TYPE == "A" or self.ISOLATION_TYPE == "B") and self.DETECTION_TYPE == "B"):
                    if (dn == 6.4):
                        ld_max = 40
                    elif (dn == 25):
                        ld_max = 30
                    elif (dn == 102):
                        ld_max = 20
                    else:
                        ld_max = round((massavail/rate)/60,5)
                elif(self.DETECTION_TYPE == "B" and self.ISOLATION_TYPE == "C"):
                    if (dn == 6.4):
                        ld_max = 60
                    elif (dn == 25):
                        ld_max = 30
                    elif (dn == 102):
                        ld_max = 20
                    else:
                        ld_max = round((massavail/rate)/60,5)
                elif(self.DETECTION_TYPE == "C" and (self.ISOLATION_TYPE == "A" or self.ISOLATION_TYPE == "B" or self.ISOLATION_TYPE == "C")):
                    if (dn == 6.4):
                        ld_max = 60
                    elif (dn == 25):
                        ld_max = 40
                    elif (dn == 102):
                        ld_max = 20
                    else:
                        ld_max = round((massavail/rate)/60,5)
                else:
                    ld_max = 0
                return ld_max
            else:
                return 0
        except:
            return 0


    def rate_n(self, i): #checked
        try:
            if not (self.FLUID is None):
                wn = self.W_n(i)
                factdi = self.fact_di()
                rate = wn * (1 - factdi)
                if(rate==0):
                    return 1
                else:
                    return rate
            else:
                return 0
        except Exception as e:
            return 0
            print(e)
            print('exception at rate_n')

    def ld_n(self, i):#checked
        try:
            ldmax = self.ld_n_max(i)
            if(self.rate_n(i) == 0):
                return 0
            else:
                if (ldmax != 0):
                    return min(self.mass_avail_n(i) / self.rate_n(i), 60 * ldmax)
                else:
                    return self.mass_avail_n(i) / self.rate_n(i)
        except Exception as e:
            return 0
            print(e)
            print('exception at ld_n')

    def mass_n(self, i):#checked
        try:
            if(i==4):
                return self.mass_avail_n(4)
            else:
                return min(self.rate_n(i) * self.ld_n(i), self.mass_avail_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at mass_n')

    def fact_mit(self):  # checked
        try:
            if (
                    self.MITIGATION_SYSTEM == "Inventory blowdown, coupled with isolation system activated remotely or automatically"):
                return 0.25
            elif (self.MITIGATION_SYSTEM == "Fire water deluge system and monitors"):
                return 0.2
            elif (self.MITIGATION_SYSTEM == "Fire water monitors only"):
                return 0.05
            else:
                return 0.15
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_mit')

    def eneff_n(self, i): #checked
        try:
            if(self.mass_n(i) == 0):
                return 1.0
            else:
                calenff = (4 * math.log10(DAL_CAL.POSTGRESQL.GET_TBL_3B21(4) * self.mass_n(i)) - 15)
                if (calenff < 1):
                    return 1.0
                else:
                    return calenff
        except Exception as e:
            return 0
            print(e)
            print('exception at eneff_n')

    def a_cmd(self, select): #done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_58(self.FLUID)
            a_cmd = [0,0,0,0]
            if(self.ReleasePhase() == "Gas"):
                a_cmd[0] = data[0]
                a_cmd[1] = data[4]
                a_cmd[2] = data[8]
                a_cmd[3] = data[12]
            else:
                a_cmd[0] = data[2]
                a_cmd[1] = data[6]
                a_cmd[2] = data[10]
                a_cmd[3] = data[14]
            if(a_cmd[select - 1] == 0):
                return 1
            else:
                return a_cmd[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at a_cmd')

    def b_cmd(self, select):
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_58(self.FLUID)
            b_cmd = [0, 0, 0, 0]
            if(self.ReleasePhase() == "Gas"):
                b_cmd[0] = data[1]
                b_cmd[1] = data[5]
                b_cmd[2] = data[9]
                b_cmd[3] = data[13]
            else:
                b_cmd[0] = data[3]
                b_cmd[1] = data[7]
                b_cmd[2] = data[11]
                b_cmd[3] = data[15]
            return b_cmd[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at b_cmd')

    def a_inj(self, select): #done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_59(self.FLUID)
            a_inj = [0, 0, 0, 0]
            if(self.GET_RELEASE_PHASE() == "Gas"):
                a_inj[0] = data[0]
                a_inj[1] = data[4]
                a_inj[2] = data[8]
                a_inj[3] = data[12]
            else:
                a_inj[0] = data[2]
                a_inj[1] = data[6]
                a_inj[2] = data[10]
                a_inj[3] = data[14]
            return a_inj[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at a_inj')

    def b_inj(self, select): #done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_59(self.FLUID)
            b_inj = [0, 0, 0, 0]
            if (self.GET_RELEASE_PHASE() == "Gas"):
                b_inj[0] = data[1]
                b_inj[1] = data[5]
                b_inj[2] = data[9]
                b_inj[3] = data[13]
            else:
                b_inj[0] = data[3]
                b_inj[1] = data[7]
                b_inj[2] = data[11]
                b_inj[3] = data[15]
            return b_inj[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at b_inj')

    def ca_cmdn_cont(self, select , i): #done
        try:
            return self.a_cmd(select) * pow(self.rate_n(i), self.b_cmd(select)) * (1 - self.fact_mit())
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmdn_cont')

    def effrate_n(self, select, i):
        try:
            API_FLUID_TYPE = self.TYPE_FLUID()
            try:
                if((self.GET_RELEASE_PHASE() == "Liquid") and (API_FLUID_TYPE == "TYPE 0")):
                    return (1 / (DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)) * math.exp(math.log10(self.ca_cmdn_cont(select, i) / (self.a_cmd(select) * (DAL_CAL.POSTGRESQL.GET_TBL_3B21(8)))) * pow(self.b_cmd(select), -1)))
                else:
                    return self.rate_n(i)
            except:
                return self.rate_n(i)
        except Exception as e:
            return 0
            print(e)
            print('exception at effrate_n')

    def ca_cmdn_inst(self, select , i): #done
        try:
            if(self.eneff_n(i) == 0):
                return 0
            else:
                return self.a_cmd(select) * pow(self.mass_n(i), self.b_cmd(select)) * (1 - self.fact_mit()) * (1/self.eneff_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmdn_inst')

    def ca_injn_cont(self, select, i):#done
        try:
            return self.a_inj(select) * pow(self.rate_n(i), self.b_inj(select)) * (1 - self.fact_mit())
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_cont')
    def ca_injn_inst(self, select, i):#done
        try:
            if(self.eneff_n(i) == 0):
                return 0
            else:
                return self.a_inj(select) * pow(self.mass_n(i), self.b_inj(select)) * ((1 - self.fact_mit()) / self.eneff_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_inst')
    def fact_n_ic(self, i): #checked
        try:
            releasetype = self.releaseType(i)
            if (releasetype == "Continuous"):
                return min(self.rate_n(i) / (DAL_CAL.POSTGRESQL.GET_TBL_3B21(5)), 1.0)
            else:
                return 1
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_n_ic')

    def fact_ait(self): #checked
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            ait = 273 + (data[9] - 32) / 1.8 #doi do f sang do C roi doi sang do K
            if ((self.STORED_TEMP + (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6))) <= ait):
                return 0
            elif((self.STORED_TEMP - (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6))) >= ait):
                return 1
            else:
                return (self.STORED_TEMP - ait + (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6))) / (2 * (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6)))
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_ait')

    def ca_cmdn_flame(self, i): #done
        try:
            caailcmdn = self.ca_cmdn_cont(2, i) * self.fact_n_ic(i) + self.ca_cmdn_inst(4, i) * (1 - self.fact_n_ic(i))
            caainlcmdn = self.ca_cmdn_cont(1, i) * self.fact_n_ic(i) + self.ca_cmdn_inst(3, i) * (1 - self.fact_n_ic(i))
            return caailcmdn * self.fact_ait() + caainlcmdn * (1 - self.fact_ait())
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmd_flame')
    def ca_injn_flame(self, i): #test
        try:
            caailinjn = abs(self.ca_injn_cont(2, i)) * self.fact_n_ic(i) + abs(self.ca_injn_inst(4, i)) * (1 - self.fact_n_ic(i))
            caainlinjn = abs(self.ca_injn_cont(1, i)) * self.fact_n_ic(i) + abs(self.ca_injn_inst(3, i)) * (1 - self.fact_n_ic(i))
            return caailinjn * self.fact_ait() + caainlinjn * (1 - self.fact_ait())
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_flam')
    def checkFlame(self): #test
        try:
            check = False
            itemsFrammable = ["C1-C2", "C3-C4", "C5", "C6-C8", "C9-C12", "C13-C16", "C17-C25", "C25+", "H2", "H2S", "HF", "CO", "DEE", "Methanol", "PO", "Styrene", "Aromatics", "EEA", "EE", "EG", "EO" ]
            for x in itemsFrammable:
                if(self.FLUID == x):
                    check = True
                    break
            return  check
        except Exception as e:
            return 0
            print(e)
            print('exception at checkflame')
    def ca_cmd_flame(self): #test
        try:
            if(not self.checkFlame()):
                return 0
            else:
                obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
                t = obj[0] * self.ca_cmdn_flame(1) + obj[1] * self.ca_cmdn_flame(2) + obj[2] * self.ca_cmdn_flame(3) + obj[3] * self.ca_cmdn_flame(4)
                ca_cmd_flame = t / obj[4] # t / gff_Total
                return math.fabs(ca_cmd_flame)
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmd_flame')
    def ca_inj_flame(self): #test
        try:
            if(not self.checkFlame()):
                return 0
            else:
                obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
                t = obj[0] * self.ca_injn_flame(1) + obj[1] * self.ca_injn_flame(2) + obj[2] * self.ca_injn_flame(3) + obj[3] * self.ca_injn_flame(4)
                ca_inj = t / obj[4]
                return math.fabs(ca_inj)
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_flame')

    def rate_tox_n(self, i): #done
        try:
            return self.TOXIC_PERCENT * self.W_n(i) / 100
        except Exception as e:
            return 0
            print(e)
            print('exception at rate_tox_n')

    def mass_tox_n(self, i): #done
        try:
            return self.TOXIC_PERCENT * self.mass_n(i) / 100
        except Exception as e:
            return 0
            print(e)
            print('exception at mass_tox_n')

    def GET_TOXIC(self): #done
        try:
            TOXIC_PHASE = "Liquid"
            if(self.FLUID_PHASE == "Vapor" or self.FLUID_PHASE == "Two-phase"):
                TOXIC_PHASE = "Gas"
            if(self.FLUID == "HF"):
                if(self.RELEASE_DURATION == 5):
                    a = [1.1401, 3.5683]
                elif(self.RELEASE_DURATION == 10):
                    a = [1.1031, 3.8431]
                elif (self.RELEASE_DURATION == 20):
                    a = [1.0816, 4.1040]
                elif (self.RELEASE_DURATION == 40):
                    a = [1.0942, 4.3295]
                elif (self.RELEASE_DURATION == 60):
                    a = [1.1031, 4.4576]
                else:
                    a = [1.4056, 33606]
            elif(self.FLUID == "H2S"):
                if (self.RELEASE_DURATION == 5):
                    a = [1.2411, 3.9686]
                elif (self.RELEASE_DURATION == 10):
                    a = [1.2410, 4.0948]
                elif (self.RELEASE_DURATION == 20):
                    a = [1.2370, 4.238]
                elif (self.RELEASE_DURATION == 40):
                    a = [1.2297, 4.3626]
                elif (self.RELEASE_DURATION == 60):
                    a = [1.2266, 4.4365]
                else:
                    a = [0.9674, 2.7840]
            elif(self.FLUID == "Ammonia"):
                if (self.RELEASE_DURATION == 5):
                    a = [636.7, 1.183]
                elif (self.RELEASE_DURATION == 10):
                    a = [846.3, 1.181]
                elif (self.RELEASE_DURATION == 15):
                    a = [1053, 1.180]
                elif (self.RELEASE_DURATION == 20):
                    a = [1256, 1.178]
                elif (self.RELEASE_DURATION == 25):
                    a = [1455, 1.176]
                elif (self.RELEASE_DURATION == 30):
                    a = [1650, 1.174]
                elif (self.RELEASE_DURATION == 35):
                    a = [1842, 1.172]
                elif (self.RELEASE_DURATION == 40):
                    a = [2029, 1.169]
                elif (self.RELEASE_DURATION == 45):
                    a = [2213, 1.166]
                elif (self.RELEASE_DURATION == 50):
                    a = [2389, 1.161]
                elif (self.RELEASE_DURATION == 55):
                    a = [2558, 1.155]
                elif (self.RELEASE_DURATION == 60):
                    a = [2714, 1.145]
                else:
                    a = [2.684, 0.9011]
            elif(self.FLUID == "Chlorine"):
                if (self.RELEASE_DURATION == 5):
                    a = [3350, 1.097]
                elif (self.RELEASE_DURATION == 10):
                    a = [3518, 1.095]
                elif (self.RELEASE_DURATION == 15):
                    a = [3798, 1.092]
                elif (self.RELEASE_DURATION == 20):
                    a = [4191, 1.089]
                elif (self.RELEASE_DURATION == 25):
                    a = [4694, 1.085]
                elif (self.RELEASE_DURATION == 30):
                    a = [5312, 1.082]
                elif (self.RELEASE_DURATION == 35):
                    a = [6032, 1.077]
                elif (self.RELEASE_DURATION == 40):
                    a = [6860, 1.072]
                elif (self.RELEASE_DURATION == 45):
                    a = [7788, 1.066]
                elif (self.RELEASE_DURATION == 50):
                    a = [8798, 1.057]
                elif (self.RELEASE_DURATION == 55):
                    a = [9890, 1.046]
                elif (self.RELEASE_DURATION == 60):
                    a = [10994, 1.026]
                else:
                    a = [3.528, 1.177]
            elif(self.FLUID == "AlCl3" and TOXIC_PHASE == "Gas"):
                a = [3.4531, 0.9411]
            elif(self.FLUID == "CO" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 3):
                    a = [9.55, 1.15]
                elif (self.RELEASE_DURATION == 5):
                    a = [60.09, 1.06]
                elif (self.RELEASE_DURATION == 10):
                    a = [189.42, 1.13]
                elif (self.RELEASE_DURATION == 20):
                    a = [651.49, 1.11]
                elif (self.RELEASE_DURATION == 40):
                    a = [1252.67, 1.17]
                else:
                    a = [1521.89, 1.21]
            elif(self.FLUID == "HCl" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 3):
                    a = [47.39, 1.09]
                elif (self.RELEASE_DURATION == 5):
                    a = [123.67, 1.15]
                elif (self.RELEASE_DURATION == 10):
                    a = [531.45, 1.10]
                elif (self.RELEASE_DURATION == 20):
                    a = [224.55, 1.18]
                elif (self.RELEASE_DURATION == 40):
                    a = [950.92, 1.20]
                else:
                    a = [2118.87, 1.23]
            elif(self.FLUID == "Nitric Acid" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 3):
                    a = [13230.9, 1.25]
                elif (self.RELEASE_DURATION == 5):
                    a = [17146, 1.25]
                elif (self.RELEASE_DURATION == 10):
                    a = [23851.3, 1.24]
                elif (self.RELEASE_DURATION == 20):
                    a = [31185, 1.23]
                elif (self.RELEASE_DURATION == 40):
                    a = [35813.7, 1.22]
                else:
                    a = [38105.8, 1.22]
            elif(self.FLUID == "Nitric Acid" and TOXIC_PHASE == "Liquid"):
                if (self.RELEASE_DURATION == 3):
                    a = [1114.96, 1.08]
                elif (self.RELEASE_DURATION == 5):
                    a = [2006.1, 1.02]
                elif (self.RELEASE_DURATION == 10):
                    a = [2674.47, 1.06]
                elif (self.RELEASE_DURATION == 20):
                    a = [4112.65, 1.06]
                elif (self.RELEASE_DURATION == 40):
                    a = [6688.99, 1.06]
                else:
                    a = [9458.29, 1.12]
            elif(self.FLUID == "NO2" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 3):
                    a = [1071.74, 0.70]
                elif (self.RELEASE_DURATION == 5):
                    a = [1466.57, 0.68]
                elif (self.RELEASE_DURATION == 10):
                    a = [1902.9, 0.68]
                elif (self.RELEASE_DURATION == 20):
                    a = [2338.76, 0.72]
                elif (self.RELEASE_DURATION == 40):
                    a = [3621.1, 0.7]
                else:
                    a = [4070.48, 0.71]
            elif (self.FLUID == "NO2" and TOXIC_PHASE == "Liquid"):
                if (self.RELEASE_DURATION == 3):
                    a = [430, 0.98]
                elif (self.RELEASE_DURATION == 5):
                    a = [610.31, 1.04]
                elif (self.RELEASE_DURATION == 10):
                    a = [1340.93, 1.07]
                elif (self.RELEASE_DURATION == 20):
                    a = [3020.54, 1.08]
                elif (self.RELEASE_DURATION == 40):
                    a = [6110.67, 1.12]
                else:
                    a = [9455.68, 1.13]
            elif(self.FLUID == "Phosgene" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 3):
                    a = [3095.33, 1.20]
                elif (self.RELEASE_DURATION == 5):
                    a = [5918.49, 1.29]
                elif (self.RELEASE_DURATION == 10):
                    a = [12129.3, 1.24]
                elif (self.RELEASE_DURATION == 20):
                    a = [27459.6, 1.27]
                elif (self.RELEASE_DURATION == 40):
                    a = [63526.4, 1.30]
                else:
                    a = [96274.2, 1.31]
            elif(self.FLUID == "Phosgene" and TOXIC_PHASE == "Liquid"):
                if (self.RELEASE_DURATION == 3):
                    a = [733.39, 1.06]
                elif (self.RELEASE_DURATION == 5):
                    a = [1520.02, 1.10]
                elif (self.RELEASE_DURATION == 10):
                    a = [4777.72, 1.12]
                elif (self.RELEASE_DURATION == 20):
                    a = [14727.5, 1.16]
                elif (self.RELEASE_DURATION == 40):
                    a = [42905, 1.20]
                else:
                    a = [77287.7, 1.23]
            elif(self.FLUID == "TDI" and TOXIC_PHASE == "Liquid"):
                if (self.RELEASE_DURATION == 3):
                    a = [793.04, 1.06]
                elif (self.RELEASE_DURATION == 5):
                    a = [846.54, 1.09]
                elif (self.RELEASE_DURATION == 10):
                    a = [1011.9, 1.10]
                elif (self.RELEASE_DURATION == 20):
                    a = [1026.06, 1.06]
                elif (self.RELEASE_DURATION == 40):
                    a = [1063.8, 1.06]
                else:
                    a = [1252.57, 1.03]
            elif (self.FLUID == "EE" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 1.5):
                    a = [0.8954, 1.171]
                elif (self.RELEASE_DURATION == 3):
                    a = [1.7578, 1.181]
                elif (self.RELEASE_DURATION == 5):
                    a = [4.0002, 1.122]
                elif (self.RELEASE_DURATION == 10):
                    a = [7.5400, 1.111]
                elif (self.RELEASE_DURATION == 20):
                    a = [24.56, 0.971]
                elif (self.RELEASE_DURATION == 40):
                    a = [31.22, 0.995]
                else:
                    a = [59.67, 0.899]
            elif (self.FLUID == "EE" and TOXIC_PHASE == "Liquid"):
                if (self.RELEASE_DURATION == 10):
                    a = [0.6857, 1.105]
                elif (self.RELEASE_DURATION == 20):
                    a = [3.6389, 1.065]
                elif (self.RELEASE_DURATION == 40):
                    a = [9.8422, 1.132]
                else:
                    a = [23.513, 1.104]
            elif(self.FLUID == "EO" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 1.5):
                    a = [0.5085, 1.222]
                elif (self.RELEASE_DURATION == 3):
                    a = [2.9720, 1.207]
                elif (self.RELEASE_DURATION == 5):
                    a = [7.9931, 1.271]
                elif (self.RELEASE_DURATION == 10):
                    a = [47.69, 1.2909]
                elif (self.RELEASE_DURATION == 20):
                    a = [237.57, 1.2849]
                elif (self.RELEASE_DURATION == 40):
                    a = [1088.4, 1.1927]
                else:
                    a = [1767.5, 1.203]
            elif(self.FLUID == "PO" and TOXIC_PHASE == "Gas"):
                if (self.RELEASE_DURATION == 3):
                    a = [0.0008, 1.913]
                elif (self.RELEASE_DURATION == 5):
                    a = [0.0864, 1.217]
                elif (self.RELEASE_DURATION == 10):
                    a = [0.1768, 1.2203]
                elif (self.RELEASE_DURATION == 20):
                    a = [0.4172, 1.2164]
                elif (self.RELEASE_DURATION == 40):
                    a = [0.9537, 1.2097]
                else:
                    a = [1.2289, 1.2522]
            elif(self.FLUID == "PO" and TOXIC_PHASE == "Liquid"):
                if (self.RELEASE_DURATION == 5):
                    a = [2.4084, 1.198]
                elif (self.RELEASE_DURATION == 10):
                    a = [9.0397, 1.111]
                elif (self.RELEASE_DURATION == 20):
                    a = [17.425, 1.114]
                elif (self.RELEASE_DURATION == 40):
                    a = [34.255, 1.118]
                else:
                    a = [367.06, 0.9855]
            else:
                a = [0, 0]
            return a
        except Exception as e:
            return 0
            print(e)
            print('Exception at get_toxic')

    def ca_injn_tox(self, i):#done
        try:
            C8 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(8)
            C4 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)
            releasetype = self.releaseType(i)
            if(releasetype == "Instantaneous"):
                self.RELEASE_DURATION == "Instantaneous Releases"
            a = self.GET_TOXIC()
            if(self.FLUID == "HF" or self.FLUID == "H2S"):
                if(releasetype == "Continuous"):
                    log = a[0] + math.log10(C4 * self.rate_tox_n(i)) + a[1] #done
                else:
                    log = a[0] + math.log10(C4 * self.mass_tox_n(i)) + a[1] #done
                return C8 * pow(10, log)
            elif(self.FLUID == "Ammonia" or self.FLUID == "Chlorine"):
                if(releasetype == "Continuous"):
                    return a[0] * pow(self.rate_tox_n(i), a[1])     #done
                else:
                    return a[0] * pow(self.mass_tox_n(i), a[1])     #done
            elif(self.FLUID == "AlCl3" or self.FLUID == "CO" or self.FLUID == "HCl" or self.FLUID == "Nitric Acid" or self.FLUID == "NO2" or
                         self.FLUID == "Phosgene" or self.FLUID == "TDI" or self.FLUID == "EE" or self.FLUID == "EO" or self.FLUID == "PO"):
                if(releasetype == "Continuous"):
                    return a[0] * pow(self.rate_tox_n(i), a[1]) #done
                else:
                    return a[0] * pow(self.mass_tox_n(i), a[1])  #done
            else:
                return 0
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_tox')
    def checkToxic(self): #done
        try:
            check = False
            itemsToxic = ["Nitric Acid", "AlCl3", "TDI", "EE","Pyrophoric"]
            if (self.FLUID == "H2S" and self.TOXIC_PERCENT > (100 * pow(10, -4))):
                check = True
            elif (self.FLUID == "HF" and self.TOXIC_PERCENT > (30 * pow(10, -4))):
                check = True
            elif (self.FLUID == "CO" and self.TOXIC_PERCENT > (1200 * pow(10, -4))):
                check = True
            elif (self.FLUID == "HCl" and self.TOXIC_PERCENT > (50 * pow(10, -4))):
                check = True
            elif (self.FLUID == "NO2" and self.TOXIC_PERCENT > (20 * pow(10, -4))):
                check = True
            elif (self.FLUID == "Phosgene" and self.TOXIC_PERCENT > (2 * pow(10, -4))):
                check = True
            elif (self.FLUID == "PO" and self.TOXIC_PERCENT > (400 * pow(10, -4))):
                check = True
            elif (self.FLUID == "EO" and self.TOXIC_PERCENT > (800 * pow(10, -4))):
                check = True
            elif (self.FLUID == "Ammonia" and self.TOXIC_PERCENT > (10 * pow(10, -4))):
                 check = True
            elif (self.FLUID == "Chlorine" and self.TOXIC_PERCENT > (10 * pow(10, -4))):
                check = True
            else:
                for x in itemsToxic:
                    if(self.FLUID == x):
                        check = True
                        break
            return check
        except Exception as e:
            return 0
            print(e)
            print('exception at check toxic')

    def ca_inj_tox(self): #done
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            if(not self.checkToxic()):
                return 0
            else:
                t = obj[0]*self.ca_injn_tox(1) + obj[1]*self.ca_injn_tox(2) + obj[2]*self.ca_injn_tox(3) + obj[3]*self.ca_injn_tox(4)
                ca_inj_tox = t / obj[4]
                return abs(ca_inj_tox)
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_tox')

    #Step 10 non flammable non toxic consequence (hau qua doc hai khong de chay)

    def ca_injn_contnfnt(self, i):  #done
        try:
            C11 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(11)
            C9 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(9)
            C8 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(8)
            C4 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)
            g = 2696 - 21.9 * C11 * (self.STORED_PRESSURE - self.ATMOSPHERIC_PRESSURE) + 1.474 * pow((C11 * (self.STORED_PRESSURE - self.ATMOSPHERIC_PRESSURE)), 2)
            h = 0.31 - 0.00032 * pow((C11 * (self.STORED_PRESSURE - self.ATMOSPHERIC_PRESSURE) - 40), 2)
            if(self.FLUID == "Steam"):
                return C9 * self.rate_n(i)
            else:
                return 0.2 * (C8 * g * pow(C4 * self.rate_n(i), h))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_contnfnt')

    def ca_injn_instnfnt(self, i): #done
        try:
            C10 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(10)
            if(self.FLUID == "Steam"):
                return C10 * pow(self.mass_n(i), 0.6384)
            else:
                return 0
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_instnfnt')

    def fact_n_icnfnt(self, i): #done
        try:
            C5 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(5)
            if (self.FLUID == "Steam"):
                return min(self.rate_n(i) / C5, 1)
            else:
                return 0
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_n_icnfnt')

    def ca_injn_leaknfnt(self, i): #done
        try:
            return self.ca_injn_instnfnt(i) * self.fact_n_icnfnt(i) + self.ca_injn_contnfnt(i) * (1 - self.fact_n_icnfnt(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_leaknfnt')
    def checkNone(self): #
        try:
            check = False
            itemsNoneTF = ["Steam", "Acid", "Caustic"]
            for x in itemsNoneTF:
                if(self.FLUID == x):
                    check = True
                    break
            return check
        except Exception as e:
            print(e)
            print('exception at checknone')

    def ca_inj_nfnt(self): #done
     try:
         if(not self.checkNone()):
             return 0
         else:
             obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
             t = obj[0] * self.ca_injn_leaknfnt(1) + obj[1] * self.ca_injn_leaknfnt(2) + obj[2] * self.ca_injn_leaknfnt(3) + obj[3] * self.ca_injn_leaknfnt(4)
             ca_inj_nfnt = t / obj[4]
             return math.fabs(ca_inj_nfnt)
     except Exception as e:
        print(e)
        print('exception at ca_inj_nfnt')

    def ca_cmd(self): #done
        try:
            return self.ca_cmd_flame()
        except Exception as e:
            print(e)
            print('exception at ca_cmd')

    def ca_inj(self): #done
        try:
            cainjflame = self.ca_inj_flame()
            cainjtox = self.ca_inj_tox()
            cainjnfnt = self.ca_inj_nfnt()
            return max(max(cainjflame, cainjtox), cainjnfnt)
        except Exception as e:
            print(e)
            print('exception at ca_inj')
    def ca_final(self): #final consequence area
        try:
            return max(self.ca_inj(), self.ca_cmd())
        except Exception as e:
            print(e)
            print('exception at ca_final')


    def fc_cmd(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        t = obj[0] * obj[5] + obj[1] * obj[6] + obj[2] * obj[7] + obj[3] * obj[8]
        fc_cmd = t * self.MATERIAL_COST / obj[4]
        return fc_cmd

    def fc_affa(self):
        cacmd = self.ca_cmd()
        fc_affa = cacmd * self.EQUIPMENT_COST
        return fc_affa

    def outage_cmd(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        t = obj[0] * obj[9] + obj[1] * obj[10] + obj[2] * obj[11] + obj[3] * obj[12]
        return t / obj[4]

    def outage_affa(self):
        fcaffa = abs(self.fc_affa())
        if fcaffa != 0:
            b = 1.242 + 0.585 * math.log10(fcaffa * pow(10, -6))
        else:
            b = 0
        return pow(10, b)

    def fc_prod(self):
        return (self.outage_cmd() + self.outage_affa()) * self.PRODUCTION_COST

    def fc_inj(self):
        return self.ca_inj() * self.PERSON_DENSITY * self.INJURE_COST

    def vol_n_env(self, i):
        massn = self.mass_n(i)
        C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        C12 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(12)
        fevap= -7.1408 + 8.5827*pow(10,-3)*C12*data[2] - 3.5594*pow(10,-6)*pow(C12*data[2],2) + 2331.1/(C12*data[2]) - 203545/(pow(C12*data[2],2))
        if(self.FLUID == "C6-C8" or self.FLUID == "Acid"):
            frac_evap = 0.9
        elif(self.FLUID == "C9-C12"):
            frac_evap = 0.5
        elif(self.FLUID == "C13-C16"):
            frac_evap = 0.1
        elif(self.FLUID == "C17-C25"):
            frac_evap = 0.05
        elif(self.FLUID == "C25+"):
            frac_evap = 0.02
        elif(self.FLUID == "Nitric Acid"):
            frac_evap = 0.8
        elif(self.FLUID == "NO2" or self.FLUID == "EE"):
            frac_evap = 0.75
        elif(self.FLUID == "TDI"):
            frac_evap = 0.15
        elif(self.FLUID == "Styrene"):
            frac_evap = 0.6
        elif(self.FLUID == "EEA"):
            frac_evap = 0.65
        elif(self.FLUID == "EG"):
            frac_evap = 0.45
        else:
            frac_evap = round(fevap, 2)

        return C13 * massn * (1 - frac_evap) / (data[1] * 16.02)

    def fc_environ(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        t = obj[0] * self.vol_n_env(1) + obj[1] * self.vol_n_env(2) + obj[2] * self.vol_n_env(3) + obj[3] * self.vol_n_env(4)
        return t * self.ENVIRON_COST / obj[4]

    def fc(self):
        fccmd = self.fc_cmd()
        fcaffa = self.fc_affa()
        fcprod = self.fc_prod()
        fcinj = self.fc_inj()
        fcenviron = self.fc_environ()
        return fccmd + fcaffa + fcprod + fcinj + fcenviron

# // Storage tank.
class CA_SHELL: #datsua
    def __init__(self, FLUID, FLUID_HEIGHT, SHELL_COURSE_HEIGHT, TANK_DIAMETER, EnvironSensitivity,
                 P_lvdike, P_onsite, P_offsite, MATERIAL_COST, API_COMPONENT_TYPE_NAME, PRODUCTION_COST,Soil_type,
                 TANK_FLUID,CHT,PROD_COST,EQUIP_OUTAGE_MULTIPLIER,EQUIP_COST,POP_DENS,INJ_COST,release_Fluid_Percent_Toxic,FLUID_PHASE,proposalID):
        self.FLUID = FLUID
        self.FLUID_HEIGHT = FLUID_HEIGHT
        self.SHELL_COURSE_HEIGHT = SHELL_COURSE_HEIGHT
        self.TANK_DIAMETER = TANK_DIAMETER
        self.EnvironSensitivity = EnvironSensitivity
        self.P_lvdike = P_lvdike
        self.P_onsite = P_onsite
        self.P_offsite = P_offsite
        self.MATERIAL_COST = MATERIAL_COST
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.PRODUCTION_COST = PRODUCTION_COST
        self.Soil_type = Soil_type
        self.TANK_FLUID=TANK_FLUID
        self.CHT=CHT
        # self.EQUIPMENT_COST = EQUIPMENT_COST
        #bổ sung 5 tham số đầu vào cho TankShell
        self.PROD_COST = PROD_COST
        self.EQUIP_OUTAGE_MULTIPLIER = EQUIP_OUTAGE_MULTIPLIER
        self.EQUIP_COST = EQUIP_COST
        self.POP_DENS = POP_DENS
        self.INJ_COST = INJ_COST
        self.release_Fluid_Percent_Toxic = release_Fluid_Percent_Toxic/1000000
        self.FLUID_PHASE = FLUID_PHASE
        self.proposalID = proposalID

    def NBP(self):
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        nbp  = ((data[2] -32)/1.8)
        return nbp

    def ambient(self):
        return DAL_CAL.POSTGRESQL.GET_RELEASE_PHASE(self.FLUID)

    def ReleasePhase(self):
        try:
            if (self.FLUID_PHASE=="Gas"):
                return "Gas"
            elif (self.ambient()=="Liquid") and (self.FLUID_PHASE=="Liquid"):
                return "Liquid"
            elif self.NBP()<=300:
                return "Liquid"
            else:
                return "Gas"
        except Exception as e:
            print(e)
            return 0


    def FC_Category(self, fc):
        if (fc <= 10000):
            return "A"
        elif (fc <= 100000):
            return "B"
        elif (fc <= 1000000):
            return "C"
        elif (fc <= 10000000):
            return "D"
        else:
            return "E"

    def k_h_bottom(self):
        k_h = [0, 0, 0]
        if (self.Soil_type == "Coarse Sand"):
            k_h[0] = 0.1
            k_h[1] = 0.01
            k_h[2] = 0.33
        elif(self.Soil_type == "Fine Sand"):
            k_h[0] = 0.01
            k_h[1] = 0.001
            k_h[2] = 0.33
        elif(self.Soil_type == "Very Fine Sand"):
            k_h[0] = pow(10, -3)
            k_h[1] = pow(10, -5)
            k_h[2] = 0.33
        elif(self.Soil_type == "Silt"):
            k_h[0] = pow(10, -5)
            k_h[1] = pow(10, -6)
            k_h[2] = 0.41
        elif(self.Soil_type == "Sandy Clay"):
            k_h[0] = pow(10, -6)
            k_h[1] = pow(10, -7)
            k_h[2] = 0.45
        elif(self.Soil_type == "Clay"):
            k_h[0] = pow(10, -7)
            k_h[1] = pow(10, -8)
            k_h[2] = 0.5
        elif(self.Soil_type == "Concrete-Asphalt"):
            k_h[0] = pow(10, -10)
            k_h[1] = pow(10, -11)
            k_h[2] = 0.3
        else:
            k_h[0] = 1
            k_h[1] = 0.1
            k_h[2] = 0.4
        return k_h

    def k_h_water(self):
        C31 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(31)
        k_h = self.k_h_bottom()
        return C31 * (k_h[0] + k_h[1]) / 2

    def GET_PL_UL_SHELL(self,select):
        data = [0,0]
        if (self.TANK_FLUID == "Gasoline"):
            data[0] = 684.018
            data[1] = 4.01 * pow(10, -3)
        elif(self.TANK_FLUID == "Light Diesel Oil"):
            data[0] = 734.011
            data[1] = 1.04 * pow(10, -3)
        elif(self.TANK_FLUID == "Heavy Diesel Oil"):
            data[0] = 764.527
            data[1] = 2.46 * pow(10, -3)
        elif(self.TANK_FLUID == "Fuel Oil"):
            data[0] = 775.019
            data[1] = 3.69 * pow(10, -2)
        elif(self.TANK_FLUID == "Crude Oil"):
            data[0] = 775.019
            data[1] = 3.69 * pow(10, -2)
        elif (self.TANK_FLUID == "Heavy Crude Oil"):
            data[0] = 900.026
            data[1] = 4.6 * pow(10, -2)
        elif (self.TANK_FLUID == "Heavy Fuel Oil"):
            data[0] = 900.026
            data[1] = 4.6 * pow(10, -2)
        else:
            data[0] = 1000
            data[1] = 1
        return data[select]

    def k_h_prod(self):
        return self.k_h_water() * (self.GET_PL_UL_SHELL(0) / 1000) * (1 / self.GET_PL_UL_SHELL(1))

    def vel_s_prod(self):
        kh = self.k_h_bottom()
        return self.k_h_prod() / kh[2]

    def d_n_shell(self, i):
        if (i == 1):
            dn = 3.175
        elif (i == 2):
            dn = 6.35
        elif (i == 3):
            dn = 50.8
        else:
            dn = 250*self.TANK_DIAMETER
        return dn

    def a_n_shell(self, i):
        return math.pi * pow(self.d_n_shell(i),2) / 4

    def LHT_above(self):
        try:
            LHTab = self.FLUID_HEIGHT-(self.get_Course()-1)*self.CHT
            if LHTab>=0:
                return LHTab
            else:
                return 0
        except Exception as e:
            print(e)
            return 0

    def get_Course(self):
        if self.API_COMPONENT_TYPE_NAME=="COURSE-1":
            return 1
        if self.API_COMPONENT_TYPE_NAME=="COURSE-2":
            return 2
        if self.API_COMPONENT_TYPE_NAME=="COURSE-3":
            return 3
        if self.API_COMPONENT_TYPE_NAME=="COURSE-4":
            return 4
        if self.API_COMPONENT_TYPE_NAME=="COURSE-5":
            return 5
        if self.API_COMPONENT_TYPE_NAME=="COURSE-6":
            return 6
        if self.API_COMPONENT_TYPE_NAME=="COURSE-7":
            return 7
        if self.API_COMPONENT_TYPE_NAME=="COURSE-8":
            return 8
        if self.API_COMPONENT_TYPE_NAME=="COURSE-9":
            return 9
        if self.API_COMPONENT_TYPE_NAME=="COURSE-10":
            return 10

    def Lvol_abouve(self):
        return math.pi * pow(self.TANK_DIAMETER,2) * self.LHT_above() / 4

    def W_n_Tank(self, i):
        try:
            C32 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(32)
            if(self.MATERIAL_COST==1):
                return C32 * 0.61 * self.a_n_shell(i) * math.sqrt(2 * 9.8196 * self.FLUID_HEIGHT)
            else:
                return C32 * 0.61 * self.a_n_shell(i) * math.sqrt(2 * 9.8196 * self.FLUID_HEIGHT)
        except Exception as e:
            print(e)
            return 0

    def Bbl_total_shell(self):
        try:
            return math.pi * pow(self.TANK_DIAMETER,2) * self.FLUID_HEIGHT / (4* DAL_CAL.POSTGRESQL.GET_TBL_3B21(13))
        except Exception as e:
            print(e)
            return 0

    def Bbl_avail(self, i):
        try:
            C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
            return self.Lvol_abouve()*C13
            # return math.pi * pow(self.TANK_DIAMETER, 2) * (self.FLUID_HEIGHT - (i - 1) * self.SHELL_COURSE_HEIGHT) / (4 * C13)
        except Exception as e:
            print(e)
            return 0

    def ld_tank(self, i):
        try:
            if(self.d_n_shell(i) <= 3.175):
                return min(self.Bbl_avail(i) / self.W_n_Tank(i), 7)
            else:
                # return 1
                return min(self.Bbl_avail(i) / self.W_n_Tank(i), 1)
        except:
            return 1

    def Bbl_leak_n(self, i):
        return min(self.W_n_Tank(i) * self.ld_tank(i), self.Bbl_avail(i))

    def getCost(self):
        try:
            costTANK = [0, 0, 0, 0, 0, 0]
            if (self.EnvironSensitivity == "High"):
                costTANK[0] = 10
                costTANK[1] = 50
                costTANK[2] = 500
                costTANK[3] = 3000
                costTANK[4] = 10000
                costTANK[5] = 5000
            elif(self.EnvironSensitivity == "Medium"):
                costTANK[0] = 10
                costTANK[1] = 50
                costTANK[2] = 250
                costTANK[3] = 1500
                costTANK[4] = 5000
                costTANK[5] = 1500
            elif(self.EnvironSensitivity == "Low"):
                costTANK[0] = 10
                costTANK[1] = 50
                costTANK[2] = 100
                costTANK[3] = 500
                costTANK[4] = 1000
                costTANK[5] = 500
            else:
                costTANK[0] = 0
                costTANK[1] = 0
                costTANK[2] = 0
                costTANK[3] = 0
                costTANK[4] = 0
                costTANK[5] = 0
            return costTANK
        except Exception as e:
            print(e)
            return 0

    def Bbl_leak_release(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            summ = self.Bbl_leak_n(1) * obj[0] + self.Bbl_leak_n(2) * obj[1] + self.Bbl_leak_n(3) * obj[2]
            return summ / obj[4]
        except Exception as e:
            print(e)
            return 0

    def Bbl_leak_indike(self):
        try:
            return self.Bbl_leak_release() * (1 - self.P_lvdike / 100)
        except Exception as e:
            print(e)
            return 0

    def Bbl_leak_ssonsite(self):
        try:
            return self.P_onsite * (self.Bbl_leak_release() - self.Bbl_leak_indike()) / 100
        except Exception as e:
            print(e)
            return 0

    def Bbl_leak_ssoffsite(self):
        try:
            return self.P_offsite * (self.Bbl_leak_release() - self.Bbl_leak_indike() - self.Bbl_leak_ssonsite()) / 100
        except Exception as e:
            print(e)
            return 0

    def Bbl_leak_water(self):
        try:
            return self.Bbl_leak_release() - (self.Bbl_leak_indike() + self.Bbl_leak_ssonsite() + self.Bbl_leak_ssoffsite())
        except Exception as e:
            print(e)
            return 0

    def FC_leak_environ(self):
        try:
            cost = self.getCost()
            return self.Bbl_leak_indike() * cost[0] + self.Bbl_leak_ssonsite() * cost[1] + self.Bbl_leak_ssoffsite() * cost[2] + self.Bbl_leak_water() * cost[5]
        except Exception as e:
            print(e)
            return 0

    def Bbl_rupture_n(self):
        try:
            return self.Bbl_avail(4)
        except Exception as e:
            print(e)
            return 0

    def Bbl_rupture_release(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return self.Bbl_rupture_n() * obj[3] / obj[4]
        except Exception as e:
            print(e)
            return 0

    def Bbl_rupture_indike(self):
        try:
            return self.Bbl_rupture_release() * (1 - self.P_lvdike / 100)
        except Exception as e:
            print(e)
            return 0

    def Bbl_rupture_ssonsite(self):
        try:
            return self.P_onsite * (self.Bbl_rupture_release() - self.Bbl_rupture_indike()) / 100
        except Exception as e:
            print(e)
            return 0

    def Bbl_rupture_ssoffsite(self):
        try:
            return self.P_offsite * (self.Bbl_rupture_release() - self.Bbl_rupture_indike() - self.Bbl_rupture_ssonsite()) / 100
        except Exception as e:
            print(e)
            return 0

    def Bbl_rupture_water(self):
        try:
            return self.Bbl_rupture_release() - (self.Bbl_rupture_indike() + self.Bbl_rupture_ssonsite() + self.Bbl_rupture_ssoffsite())
        except Exception as e:
            print(e)
            return 0

    def FC_rupture_environ(self):
        try:
            cost = self.getCost()
            return self.Bbl_rupture_indike() * cost[0] + self.Bbl_rupture_ssonsite() * cost[1] + self.Bbl_rupture_ssoffsite() * cost[2] + self.Bbl_rupture_water() * cost[5]
        except Exception as e:
            print(e)
            return 0

    def FC_environ_shell(self):
        try:
            return self.FC_leak_environ() + self.FC_rupture_environ()
        except Exception as e:
            print(e)
            return 0

    def FC_PROD_SHELL(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t = obj[0] * obj[9] + obj[1] * obj[10] + obj[2] * obj[11] + obj[3] * obj[12]
            return t * self.PRODUCTION_COST / obj[4]
        except:
            return 0

    def fc_cmd(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t = obj[0] * obj[5] + obj[1] * obj[6] + obj[2] * obj[7] + obj[3] * obj[8]
            fc_cmd = t * self.MATERIAL_COST / obj[4]
            return fc_cmd
        except Exception as e:
            print(e)
            return 0
#bổ sung tính 3 tham số đầu ra cho tankshell
    def fc_affa_tank(self): #dat
        if self.release_Fluid_Percent_Toxic<=0:
            return 0
        else:
            cacmd =self.CA_Flam_Cmd_shell()
            fc_affa = cacmd * self.EQUIP_COST
            return fc_affa
    def  outage_affa_tank(self):
        fcaffa = abs(self.fc_affa_tank())
        if fcaffa != 0:
            b = 1.242 + 0.585 * math.log10(fcaffa * pow(10.0, -6.0))
        else:
            b = 0
        return pow(10.0, b)
    def ca_cmd_flame_shell(self):
        t=7*pow(10,-5)*self.AINL_Cmd(1)+2.5*pow(10,-5)*self.AINL_Cmd(2)+5*pow(10,-6)*self.AINL_Cmd(3)+ pow(10,-7)*self.AINL_Cmd(4)
        ca_cmd_flame = t/0.0001001
        return abs(ca_cmd_flame)

    def AINL_Cmd(self,i):
        AINL_Cmd =self.getEquationConstants(0)*pow(self.rate_Flammable(i),self.getEquationConstants(1))
        if (AINL_Cmd >0):
            return AINL_Cmd
        else:
            return 0

    def rate_Flammable(self,i):
        # rate_Flammable = (self.W_n_Tank(i)*1.84*pow(10,-6))*pl_ul[0]
        rate_Flammable = (self.W_n_Tank(i) * 1.84 * pow(10, -6)) * self.GET_PL_UL_SHELL(0)
        if(rate_Flammable>0):
            return rate_Flammable
        else:
            return 0

    def getEquationConstants(self, select):
        try:
            data1 = DAL_CAL.POSTGRESQL.GET_TBL_58(self.FLUID)
            data2 = DAL_CAL.POSTGRESQL.GET_TBL_59(self.FLUID)
            input = [0, 0, 0, 0, 0, 0, 0, 0]
            if (self.TANK_FLUID == "Water"):
                return 0
            else:
                input[0] = data1[2]
                input[1] = data1[3]
                input[2] = data1[6]
                input[3] = data1[7]
                input[4] = data2[2]
                input[5] = data2[3]
                input[6] = data2[6]
                input[7] = data2[7]
            return input[select]
        except Exception as e:
            return 0
            print(e)
            print('exception at getEquationConstants')

    def fc_prod_tank(self):
        return (CA_NORMAL.outage_cmd(self)*self.EQUIP_OUTAGE_MULTIPLIER +self.outage_affa_tank())*self.PROD_COST
    def fc_inj_tank(self):
        if self.release_Fluid_Percent_Toxic<=0:
            return 0
        else:
            return self.max_total_inj()*self.POP_DENS*self.INJ_COST
    def leakDurationToxic(self,i):
        if self.release_Fluid_Percent_Toxic==0:
            return 0
        else:
            volume_Fluid_Shell= self.Lvol_abouve()
            mass_Available=volume_Fluid_Shell*self.GET_PL_UL_SHELL(0)
            return min(mass_Available/self.rate_Flammable(i),3600.0)
    def ldToxicMinutes(self,i):
        if self.release_Fluid_Percent_Toxic==0:
            return 0
        else:
            a=max(self.leakDurationToxic(i)/60.0,5.0)
            b=min(a,60.0)
            return b
    def a_cmd(self, select): #done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_58(self.FLUID)
            a_cmd = [0,0,0,0]
            if(self.ReleasePhase() == "Gas"):
                a_cmd[0] = data[0]
                a_cmd[1] = data[4]
                a_cmd[2] = data[8]
                a_cmd[3] = data[12]
            else:
                a_cmd[0] = data[2]
                a_cmd[1] = data[6]
                a_cmd[2] = data[10]
                a_cmd[3] = data[14]
            if(a_cmd[select - 1] == 1):
                return 0
            else:
                return a_cmd[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at a_cmd')

    def b_cmd(self, select):
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_58(self.FLUID)
            b_cmd = [0, 0, 0, 0]
            if (self.ReleasePhase() == "Gas"):
                b_cmd[0] = data[1]
                b_cmd[1] = data[5]
                b_cmd[2] = data[9]
                b_cmd[3] = data[13]
            else:
                b_cmd[0] = data[3]
                b_cmd[1] = data[7]
                b_cmd[2] = data[11]
                b_cmd[3] = data[15]
            return b_cmd[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at b_cmd')
    def a_inj(self, select): #done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_59(self.FLUID)
            a_inj = [0, 0, 0, 0]
            if(self.ReleasePhase() == "Gas"):
                a_inj[0] = data[0]
                a_inj[1] = data[4]
                a_inj[2] = data[8]
                a_inj[3] = data[12]
            else:
                a_inj[0] = data[2]
                a_inj[1] = data[6]
                a_inj[2] = data[10]
                a_inj[3] = data[14]
            return a_inj[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at a_inj')

    def b_inj(self, select): #done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_59(self.FLUID)
            b_inj = [0, 0, 0, 0]
            if (self.ReleasePhase() == "Gas"):
                b_inj[0] = data[1]
                b_inj[1] = data[5]
                b_inj[2] = data[9]
                b_inj[3] = data[13]
            else:
                b_inj[0] = data[3]
                b_inj[1] = data[7]
                b_inj[2] = data[11]
                b_inj[3] = data[15]
            return b_inj[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at b_inj')
    def fact_mit(self): #checked
        try:
            if (self.MITIGATION_SYSTEM == "Inventory blowdown, coupled with isolation system activated remotely or automatically"):
                return 0.25
            elif (self.MITIGATION_SYSTEM == "Fire water deluge system and monitors"):
                return 0.2
            elif (self.MITIGATION_SYSTEM == "Fire water monitors only"):
                return 0.05
            else:
                return 0.15
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_mit')

    def TYPE_FLUID(self): #done
        try:
            API_TYPE = "TYPE 0"
            if (self.FLUID == ""):
                API_TYPE = "TYPE 0"
            else:
                if(self.FLUID == "C1-C2" or self.FLUID == "C13-C16" or self.FLUID == "C17-C25" or self.FLUID =="C25+" or
                   self.FLUID == "C3-C4" or self.FLUID == "C5" or self.FLUID == "C6-C8" or self.FLUID == "C9-C12" or
                   self.FLUID == "Acid" or self.FLUID == "AlCl3" or self.FLUID == "H2" or self.FLUID == "H2S" or self.FLUID == "HCl" or
                   self.FLUID == "HF" or self.FLUID == "Nitric Acid" or self.FLUID == "NO2" or self.FLUID == "Phosgene" or
                   self.FLUID == "Pyrophoric" or self.FLUID == "Steam" or self.FLUID == "TDI" or self.FLUID == "Water" or self.FLUID =="Ammonia"
                   or self.FLUID == "Chorine"):
                    API_TYPE = "TYPE 0"
                elif(self.FLUID == "CO" or self.FLUID == "DEE" or self.FLUID == "EE" or self.FLUID == "EEA" or self.FLUID == "EG" or
                     self.FLUID == "EO" or self.FLUID == "Methanol" or self.FLUID == "PO" or self.FLUID == "Styrene" or self.FLUID == "Aromatics"):
                    API_TYPE = "TYPE 1"
                else:
                    API_TYPE = "TYPE 0"
            return API_TYPE
        except Exception as e:
            return 0
            print(e)
            print('exception at type fluid')


    def ca_cmdn_ainl_cont(self, select , i): #done
        try:
            x = self.rate_Flammable(i)
            return (self.a_cmd(select) * pow(x, self.b_cmd(select)))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmdn_ainl_cont')


    def ca_cmdn_ail_cont(self, select , i): #done
        try:
            x = self.rate_Flammable(i)
            return (self.a_cmd(select) * pow(x, self.b_cmd(select)))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmdn_ail_cont')

    def ca_inj_ainl_cont(self, select , i): #done
        try:
            x = self.rate_Flammable(i)
            return (self.a_inj(select) * pow(x, self.b_inj(select)))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_ainl_cont')


    def ca_inj_ail_cont(self, select , i): #done
        try:
            x = self.rate_Flammable(i)
            return (self.a_inj(select) * pow(x, self.b_inj(select)))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_ail_cont')


    def fact_ait(self): #checked
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            ait = data[9]
            if ((self.STORED_TEMP + 55.6) <= ait):
                return 0
            elif((self.STORED_TEMP - 55.6) >= ait):
                return 1
            else:
                return (self.STORED_TEMP - ait + 55.6) / (2 * 55.6)
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_ait')

    def CA_Flam_Cmd_shell(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return (obj[0]*self.ca_cmdn_ail_cont(2,1)+obj[1]*self.ca_cmdn_ail_cont(2,2)+obj[2]*self.ca_cmdn_ail_cont(2,3)+obj[3]*self.ca_cmdn_ail_cont(2,4))/obj[4]

    def CA_Flam_inj_shell(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0]*self.ca_inj_ail_cont(2,1)+obj[1]*self.ca_inj_ail_cont(2,2)+obj[2]*self.ca_inj_ail_cont(2,3)+obj[3]*self.ca_inj_ail_cont(2,4))/obj[4]
        except Exception as e:
            print(e)
            return 0

    def ConstC(self,i):
        input = self.ldToxicMinutes(i)
        if (input >= 60):
            return 1.2266
        elif(input >= 40):
            return 1.2297
        elif(input >= 20):
            return 1.2370
        elif(input >= 10):
            return 1.2410
        elif(input >= 5):
            return 1.2411
        elif(input == 0):
            return 0
        else:
            return 0.9674
    def ConstD(self,i):
        input = self.ldToxicMinutes(i)
        if (input >= 60):
            return 4.4365
        elif(input >= 40):
            return 4.3626
        elif(input >= 20):
            return 4.238
        elif(input >= 10):
            return 4.0948
        elif(input >= 5):
            return 3.9686
        elif (input == 0):
            return 0
        else:
            return 2.7840

    def releaseRateMass(self,i):
        if (self.release_Fluid_Percent_Toxic*self.rate_Flammable(i))<=0:
            return 1
        else:
            return self.release_Fluid_Percent_Toxic*self.rate_Flammable(i)
    def toxic_Inj(self,i):
        if self.release_Fluid_Percent_Toxic==0:
            return 0
        else:
            t=0.0929 * pow(10.0,(self.ConstC(i)*math.log10(2.205*self.releaseRateMass(i))+self.ConstD(i)))
            return t
    def total_toxic_Inj(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        t = obj[0] * self.toxic_Inj(1) + obj[1] * self.toxic_Inj(2) + obj[2] * self.toxic_Inj(3) + obj[3] * self.toxic_Inj(4)
        total_toxic_Inj = t / obj[4]
        return abs(total_toxic_Inj)
    def max_total_inj(self):
        total_toxic_Inj=self.total_toxic_Inj()
        CA_Flam_inj_shell=self.CA_Flam_inj_shell()
        return max(total_toxic_Inj,CA_Flam_inj_shell)
    def ca_cmd_shell(self):
        CA_Flam_Cmd_shell = self.CA_Flam_Cmd_shell()
        CA_Flam_inj_shell = self.CA_Flam_inj_shell()
        return max(CA_Flam_Cmd_shell,CA_Flam_inj_shell)
    def FC_total_shell(self):
        ca_cmd_shell=self.ca_cmd_shell()
        total_toxic_Inj=self.total_toxic_Inj()
        return max(ca_cmd_shell,total_toxic_Inj)
    def CA_total_shell(self):
        return self.fc_prod_tank()+self.fc_affa_tank()+self.fc_inj_tank()+self.fc_cmd()+self.FC_environ_shell()
class CA_TANK_BOTTOM:
    def __init__(self, Soil_type, TANK_FLUID, Swg, TANK_DIAMETER, FLUID_HEIGHT, API_COMPONENT_TYPE_NAME, PREVENTION_BARRIER, EnvironSensitivity, MATERIAL_COST, PRODUCTION_COST, P_lvdike,P_onsite,P_offsite,Concrete_Asphalt):
        self.Soil_type = Soil_type
        self.TANK_FLUID = TANK_FLUID
        self.Swg = Swg
        self.TANK_DIAMETER = TANK_DIAMETER
        self.FLUID_HEIGHT = FLUID_HEIGHT
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.PREVENTION_BARRIER = PREVENTION_BARRIER
        self.EnvironSensitivity =EnvironSensitivity
        self.MATERIAL_COST = MATERIAL_COST
        self.PRODUCTION_COST = PRODUCTION_COST
        self.P_lvdike = P_lvdike
        self.P_onsite = P_onsite
        self.P_offsite = P_offsite
        self.Concrete_Asphalt = Concrete_Asphalt

    def FC_Category(self, fc):
        if (fc <= 10000):
            return "A"
        elif (fc <= 100000):
            return "B"
        elif (fc <= 1000000):
            return "C"
        elif (fc <= 10000000):
            return "D"
        else:
            return "E"

    def n_rh(self, i):
        if (i==4):
            return 1
        else:
            C36 =DAL_CAL.POSTGRESQL.GET_TBL_3B21(36)
            return max(pow(self.TANK_DIAMETER / C36, 2), 1)

    def k_h_bottom(self):
        k_h = [0, 0, 0]
        if (self.Soil_type == "Coarse Sand"):
            k_h[0] = 0.1
            k_h[1] = 0.01
            k_h[2] = 0.33
        elif(self.Soil_type == "Fine Sand"):
            k_h[0] = 0.01
            k_h[1] = 0.001
            k_h[2] = 0.33
        elif(self.Soil_type == "Very Fine Sand"):
            k_h[0] = pow(10, -3)
            k_h[1] = pow(10, -5)
            k_h[2] = 0.33
        elif(self.Soil_type == "Silt"):
            k_h[0] = pow(10, -5)
            k_h[1] = pow(10, -6)
            k_h[2] = 0.41
        elif(self.Soil_type == "Sandy Clay"):
            k_h[0] = pow(10, -6)
            k_h[1] = pow(10, -7)
            k_h[2] = 0.45
        elif(self.Soil_type == "Clay"):
            k_h[0] = pow(10, -7)
            k_h[1] = pow(10, -8)
            k_h[2] = 0.5
        elif(self.Soil_type == "Concrete-Asphalt"):
            k_h[0] = pow(10, -10)
            k_h[1] = pow(10, -11)
            k_h[2] = 0.3
        else:
            k_h[0] = 1
            k_h[1] = 0.1
            k_h[2] = 0.4
        return k_h

    def k_h_water(self):
        C31 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(31)
        k_h = self.k_h_bottom()
        return C31 * (k_h[0] + k_h[1]) / 2

    def dn_bottom(self, i):
        if (i == 1):
            if (self.PREVENTION_BARRIER):
                dn = 3.175
            else:
                dn = 12.7
        elif (i == 4):
            dn = 250 * self.TANK_DIAMETER
        else:
            dn = 0
        return dn

    def rate_n_tank_bottom(self, i):
        try:
            C33 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(33)
            C34 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(34)
            C35 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(35)
            C37 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(37)
            C38 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(38)
            C39 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(39)
            C40 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(40)
            if (self.PREVENTION_BARRIER):
                ps= pow(self.dn_bottom(i),1.8)/(0.21*pow(0.0762,0.4))
                if (self.k_h_prod() > C34 * pow(self.dn_bottom(i), 2)):
                    return C33 * math.pi * self.dn_bottom(i) * math.sqrt(2 * 1 * 0.0762) * self.n_rh(i)
                elif (self.k_h_prod() <= C37 * pow(ps,(1 / 0.74))):
                    return C35 * 0.21 * pow(self.dn_bottom(i), 0.2) * pow(0.0762, 0.9) * pow(self.k_h_prod(),0.74) * self.n_rh(i)
                else:
                    m = C40 - 0.4324 * math.log10(self.dn_bottom(i)) + 0.5405 * math.log10(0.0762)
                    return C38 * pow(10,2 * math.log10(self.dn_bottom(i)) + 0.5 * math.log10(0.0762) - 0.74 * pow((C39 * 2 * math.log10(self.dn_bottom(i)) - math.log10(self.k_h_prod())) / m, m))
            else:
                ps = pow(self.dn_bottom(i), 1.8) / (0.21 * pow(self.FLUID_HEIGHT, 0.4))
                if (self.k_h_prod() > C34 * pow(self.dn_bottom(i), 2)):
                    return C33 * math.pi * self.dn_bottom(i) * math.sqrt(2 * 1 * self.FLUID_HEIGHT) * self.n_rh(i)
                elif (self.k_h_prod() <= C37*pow(ps,(1/0.74))):
                    return C35 * 0.21 * pow(self.dn_bottom(i), 0.2) * pow(self.FLUID_HEIGHT, 0.9) * pow(self.k_h_prod(), 0.74) * self.n_rh(i)
                else:
                    m = C40-0.4324*math.log10(self.dn_bottom(i)) + 0.5405*math.log10(self.FLUID_HEIGHT)
                    return C38*pow(10,2*math.log10(self.dn_bottom(i))+0.5*math.log10(self.FLUID_HEIGHT)-0.74*pow((C39 * 2*math.log10(self.dn_bottom(i))-math.log10(self.k_h_prod()))/m,m))
        except Exception as e:
            print("Error rate_n_tank_bottom:", e)
            return 0

    def t_ld_tank_bottom(self):
        if (self.Concrete_Asphalt):
            return 7
        elif (self.PREVENTION_BARRIER):
            return 30
        else:
            return 360

    def BBL_TOTAL_TANKBOTTOM(self):
        C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
        return math.pi * pow(self.TANK_DIAMETER, 2) * self.FLUID_HEIGHT / (4 * C13)

    def ld_n_tank_bottom(self, i):
        try:
            C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
            Bbl_total_tank_bottom = (math.pi * pow(self.TANK_DIAMETER, 2) * self.FLUID_HEIGHT * C13) / 4
            if self.rate_n_tank_bottom(i) == 0:
                return self.t_ld_tank_bottom()
            else:
                return min(float(Bbl_total_tank_bottom) / self.rate_n_tank_bottom(i), self.t_ld_tank_bottom())
        except Exception as e:
            print("Error ld_n_tank_bottom:",e)
            return 0

    def Bbl_leak_n_bottom(self, i):
        C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
        Bbl_total_tank_bottom = (math.pi * pow(self.TANK_DIAMETER, 2) * self.FLUID_HEIGHT * C13) / (4)
        return min(self.rate_n_tank_bottom(i) * self.ld_n_tank_bottom(i), Bbl_total_tank_bottom)

    def Bbl_rupture_bottom(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
        Bbl_total_tank_bottom = (math.pi * pow(self.TANK_DIAMETER, 2) * self.FLUID_HEIGHT* C13) / (4)
        return Bbl_total_tank_bottom

    def GET_PL_UL(self):
        data = [0, 0]
        if (self.TANK_FLUID == "Gasoline"):
            data[0] = 684.018
            data[1] = 4.01 * pow(10, -3)
        elif(self.TANK_FLUID == "Light Diesel Oil"):
            data[0] = 734.011
            data[1] = 1.04 * pow(10, -3)
        elif(self.TANK_FLUID == "Heavy Diesel Oil"):
            data[0] = 764.527
            data[1] = 2.46 * pow(10, -3)
        elif(self.TANK_FLUID == "Fuel Oil"):
            data[0] = 775.019
            data[1] = 3.69 * pow(10, -2)
        elif (self.TANK_FLUID == "Crude Oil"):
            data[0] = 775.019
            data[1] = 3.69 * pow(10, -2)
        elif (self.TANK_FLUID == "Heavy Crude Oil"):
            data[0] = 900.026
            data[1] = 4.6 * pow(10, -2)
        elif (self.TANK_FLUID == "Heavy Fuel Oil"):
            data[0] = 900.026
            data[1] = 4.6 * pow(10, -2)
        else:
            data[0] = 1000
            data[1] = 1
        return data

    def k_h_prod(self):
        pl_ul = self.GET_PL_UL()
        return self.k_h_water() * (pl_ul[0] / 1000) * (1 / pl_ul[1])

    def vel_s_prod(self):
        kh = self.k_h_bottom()
        return self.k_h_prod() / kh[2]

    def t_gl_bottom(self):
        try:
            return self.Swg / self.vel_s_prod()
        except:
            return 1

    def Bbl_leak_groundwater(self, i):
        try:
            if (self.t_gl_bottom() < self.t_ld_tank_bottom()):
                return self.Bbl_leak_n_bottom(i) * ((self.t_ld_tank_bottom() - self.t_gl_bottom()) / self.t_ld_tank_bottom())
            else:
                return 0
        except:
            return 0

    def Bbl_leak_subsoil(self, i):
        return self.Bbl_leak_n_bottom(i) - self.Bbl_leak_groundwater(i)

    def getCost(self):
        costTANK = [0, 0, 0, 0, 0, 0]
        if (self.EnvironSensitivity == "High"):
            costTANK[0] = 10
            costTANK[1] = 50
            costTANK[2] = 500
            costTANK[3] = 3000
            costTANK[4] = 10000
            costTANK[5] = 5000
        elif (self.EnvironSensitivity == "Medium"):
            costTANK[0] = 10
            costTANK[1] = 50
            costTANK[2] = 250
            costTANK[3] = 1500
            costTANK[4] = 5000
            costTANK[5] = 1500
        elif (self.EnvironSensitivity == "Low"):
            costTANK[0] = 10
            costTANK[1] = 50
            costTANK[2] = 100
            costTANK[3] = 500
            costTANK[4] = 1000
            costTANK[5] = 500
        else:
            costTANK[0] = 0
            costTANK[1] = 0
            costTANK[2] = 0
            costTANK[3] = 0
            costTANK[4] = 0
            costTANK[5] = 0
        return costTANK

    def FC_leak_environ_bottom(self):
        cost = self.getCost()
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        summa = 0
        for i in range(1,4):
            summa = summa +(self.Bbl_leak_groundwater(i) * cost[4] + self.Bbl_leak_subsoil(i) * cost[3])*obj[i-1]
        if(self.TANK_FLUID == "Water"):
            return 0
        else:
            return summa/obj[4]

    def Bbl_rupture_release_bottom(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
        Bbl_total_tank_bottom = (math.pi * pow(self.TANK_DIAMETER, 2) * self.FLUID_HEIGHT* C13) / (4)
        return (Bbl_total_tank_bottom * obj[3]) / obj[4]

    def Bbl_rupture_indike_bottom(self):
        indike = self.Bbl_rupture_release_bottom() * (1 - self.P_lvdike / 100)
        if(indike > 0):
            return indike
        else:
            return 0

    def Bbl_rupture_ssonsite_bottom(self):
        onsite = self.P_onsite * (self.Bbl_rupture_release_bottom() - self.Bbl_rupture_indike_bottom()) / 100
        if(onsite > 0):
            return onsite
        else:
            return 0

    def Bbl_rupture_ssoffsite_bottom(self):
        offsite = self.P_offsite * (self.Bbl_rupture_release_bottom() - self.Bbl_rupture_indike_bottom() - self.Bbl_rupture_ssonsite_bottom()) / 100
        if(offsite > 0):
            return offsite
        else:
            return 0

    def Bbl_rupture_water_bottom(self):
        water = self.Bbl_rupture_release_bottom() - (self.Bbl_rupture_indike_bottom() + self.Bbl_rupture_ssonsite_bottom() + self.Bbl_rupture_ssoffsite_bottom())
        if(water > 0):
            return water
        else:
            return 0

    def FC_rupture_environ_bottom(self):
        cost = self.getCost()
        if (self.TANK_FLUID == "Water"):
            return 0
        else:
            return self.Bbl_rupture_indike_bottom() * cost[0] + self.Bbl_rupture_ssonsite_bottom() * cost[1] + self.Bbl_rupture_ssoffsite_bottom() * cost[2] + self.Bbl_rupture_water_bottom() * cost[5]

    def FC_environ_bottom(self):
        return self.FC_leak_environ_bottom() + self.FC_rupture_environ_bottom()

    def FC_cmd_bottom(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        C36 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(36)
        summ = obj[0] * obj[5] + obj[1] * obj[6] + obj[2] * obj[7] + obj[3] * obj[8] * pow(self.TANK_DIAMETER / C36, 2)
        return summ * self.MATERIAL_COST / obj[4]

    def FC_PROD_BOTTOM(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        t = obj[0] * obj[9] + obj[1] * obj[10] + obj[2] * obj[11] + obj[3] * obj[12]
        return t * self.PRODUCTION_COST / obj[4]

    def FC_total_bottom(self):
        FC_TOTAL_BOTTOM = self.FC_cmd_bottom() + self.FC_environ_bottom() + self.FC_PROD_BOTTOM()
        if FC_TOTAL_BOTTOM == 0:
            return 100000000
        else:
            return self.FC_cmd_bottom() + self.FC_environ_bottom() + self.FC_PROD_BOTTOM()

class CA_LEVEL_2:
    def __init__(self, FLUID = "", MATERIAL_COST=0, FLUID_PHASE = "Vapor", API_COMPONENT_TYPE_NAME ="" , POOL_FIRE_TYPE ="",
                 EQUIPMENT_COST = 0, FRAC_LIQUID = 0, FRAC_FLASH = 0, STORED_PRESSURE = 0, ATM_PRESSURE = 101, SATURATION_PRESSURE = 0,
                 STORED_TEMP = 0, BUBBLE_TEMP = 0, DEWPOINT_TEMP = 0, ATM_TEMP = 0, SPECIFIC_HEAT_POOL = 0, RENOY_NUMBER = 0,
                 MASS_INVERT = 0, MASS_COMP = 0, MASS_VCE = 0, DETECTION_TYPE = '', ISOLATION_TYPE = '',FLAMMABLE_PERCENT = 0,
                 VOLUME_FIRE_POOL = 0, BUBBLE_GROUND_PRESSURE = 0, WIND_SPEED = 0, SURFACE_TYPE = '', GROUND_TEMP = 0, AMBIENT_CONDITION = '',
                 HUMIDITY = 0, MOLE_FRAC_TOXIC = 0, ):
        return self

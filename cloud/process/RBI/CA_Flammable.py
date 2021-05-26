import math
import numpy as np
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL
from cloud import models

class CA_Flammable: #LEVEL 1
    def __init__(self,FLUID,FLUID_PHASE,MITIGATION_SYSTEM,proposalID,STORED_TEMP,API_COMPONENT_TYPE_NAME,toxic_percent,toxic_fluid):
        self.FLUID = FLUID
        self.FLUID_PHASE = FLUID_PHASE
        self.MITIGATION_SYSTEM = MITIGATION_SYSTEM
        self.proposalID = proposalID
        self.STORED_TEMP = STORED_TEMP
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.toxic_percent = toxic_percent
        self.toxic_fluid = toxic_fluid

    def NBP(self):
        if not (self.FLUID is None):
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            nbp  = ((data[2] -32)/1.8)
        else:
            nbp = 0
        return nbp

    def ambient(self):
        if (self.FLUID is None):
            return 0
        else:
            return DAL_CAL.POSTGRESQL.GET_RELEASE_PHASE(self.FLUID)

    def ReleasePhase(self):
        if not (self.FLUID is None):
            try:
                if (self.FLUID_PHASE=="Gas"):
                    return "Gas"
                elif self.FLUID == "C1-C2" or self.FLUID == "C3-C4" or self.FLUID == "HCl" or self.FLUID == "H2" or self.FLUID == "H2S" or self.FLUID == "HF" or self.FLUID == "CO" or self.FLUID == "EO" or self.FLUID == "Ammonia" or self.FLUID == "Chlorine":
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
        else:
            return None

    def a_cmd(self, select): #done
        if not (self.FLUID is None):
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
        else:
            return 0

    def b_cmd(self, select):
        if not (self.FLUID is None):
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
        else:
            return 0

    def a_inj(self, select): #done
        if not (self.FLUID is None):
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
        else:
            return 0

    def b_inj(self, select): #done
        if not(self.FLUID is None):
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
        else:
            return 0

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
            return 0
            print(e)
            print('exception at type fluid')

    def RATE_N(self,i):
        if not (self.ReleasePhase() is None):
            try:
                if(self.TYPE_FLUID()=="TYPE 0" and self.ReleasePhase()=="Liquid123"):
                    return 0
                else:
                    rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
                    if i==1:
                        return rwcofholesize.rate_n_small
                    elif i==2:
                        return rwcofholesize.rate_n_medium
                    elif i==3:
                        return rwcofholesize.rate_n_large
                    else:
                        return rwcofholesize.rate_n_rupture
            except Exception as e:
                return 0
                print(e)
        else:
            return 0

    def ca_cmdn_cont(self, select , i): #done
        try:
            return (self.a_cmd(select) * pow(self.RATE_N(i), self.b_cmd(select)) * (1 - self.fact_mit()))
        except Exception as e:
            print('exception at ca_cmdn_cont',e)
            return 0

    def eneff_n(self,i):
        try:
            rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
            if i==1:
                return rwcofholesize.eneff_n_small
            elif i==2:
                return rwcofholesize.eneff_n_medium
            elif i==3:
                return rwcofholesize.eneff_n_large
            else:
                return rwcofholesize.eneff_n_rupture
        except Exception as e:
            print('error at eneff_n',e)
            return 0

    def mass_n(self,i):
        try:
            rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
            if i==1:
                return rwcofholesize.mass_n_small
            elif i==2:
                return rwcofholesize.mass_n_medium
            elif i==3:
                return rwcofholesize.mass_n_large
            else:
                return rwcofholesize.mass_n_rupture
        except Exception as e:
            print(e)
            return 0

    def ca_cmdn_inst(self, select , i): #done
        try:
            x = self.mass_n(i)
            if(self.eneff_n(i) == 0):
                return 0
            else:
                return self.a_cmd(select) * pow(x, self.b_cmd(select)) * (1 - self.fact_mit()/self.eneff_n(i))
        except Exception as e:
            print('exception at ca_cmdn_inst',e)
            return 0

    def ca_injn_cont(self, select, i):#done
        x = self.RATE_N(i)
        try:
            return self.a_inj(select) * pow(x, self.b_inj(select)) * (1 - self.fact_mit())
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_inj_cont')

    def ca_injn_inst(self, select, i):#done
        x = self.mass_n(i)
        try:
            if(self.eneff_n(i) == 0):
                return 0
            else:
                return self.a_inj(select) * pow(x, self.b_inj(select)) * ((1 - self.fact_mit()) / self.eneff_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_inst')

    def fact_n_ic(self,i):
        try:
            rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
            if i == 1:
                return rwcofholesize.factIC_n_small
            elif i == 2:
                return rwcofholesize.factIC_n_medium
            elif i == 3:
                return rwcofholesize.factIC_n_large
            else:
                return rwcofholesize.factIC_n_rupture
        except Exception as e:
            print("fact_n_ic",e)
            return 0

    def CA_AINL_CMD_n(self,i):
        try:
            return self.ca_cmdn_inst(3,i)*self.fact_n_ic(i) + self.ca_cmdn_cont(1,i)*(1-self.fact_n_ic(i))
        except Exception as e:
            print("CA_AINL_CMD_n",e)
            return 0

    def CA_AIL_CMD_n(self,i):
        try:
            return self.ca_cmdn_inst(4,i)*self.fact_n_ic(i) + self.ca_cmdn_cont(2,i)*(1-self.fact_n_ic(i))
        except Exception as e:
            print("error at CA_AIL_CMD_n",e)
            return 0

    def CA_AINL_INJ_n(self,i):
        try:
            return self.ca_injn_inst(3,i)*self.fact_n_ic(i) + self.ca_injn_cont(1,i)*(1-self.fact_n_ic(i))
        except:
            return 0

    def CA_AIL_INJ_n(self,i):
        try:
            return self.ca_injn_inst(4,i)*self.fact_n_ic(i) + self.ca_injn_cont(2,i)*(1-self.fact_n_ic(i))
        except:
            return 0

    def auto_ignition_temp(self):
        try:
            tbl52 = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            return (tbl52[9] - 32) / 1.8  # doi tu do K sang do C
        except Exception as e:
            print(e)
            return 0

    def fact_ait(self): #checked
        try:
            # print('STORED_TEMP',self.STORED_TEMP)
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            ait = data[9]
            if ((self.STORED_TEMP + 55.6) <= ait):
                return 0
            elif((self.STORED_TEMP - 55.6) >= ait):
                return 1
            else:
                return (self.STORED_TEMP - ait + 55.6) / (2 * 55.6)
        except Exception as e:
            print('exception at fact_ait', e)
            return 0


    def CA_Flam_Cmd_n(self,i):
        try:
            a=self.CA_AIL_CMD_n(i) * self.fact_ait() + self.CA_AINL_CMD_n(i)*(1-self.fact_ait())
            return self.CA_AIL_CMD_n(i) * self.fact_ait() + self.CA_AINL_CMD_n(i)*(1-self.fact_ait())
        except Exception as e:
            print("error CA_Flam_Cmd_n:",e)
            return 0

    def CA_Flam_inj_n(self,i):
        try:
            return self.CA_AIL_INJ_n(i) * self.fact_ait() + self.CA_AINL_INJ_n(i)*(1-self.fact_ait())
        except:
            return 0

    def CA_Flam_Cmd(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0]*self.CA_Flam_Cmd_n(1)+obj[1]*self.CA_Flam_Cmd_n(2)+obj[2]*self.CA_Flam_Cmd_n(3)+obj[3]*self.CA_Flam_Cmd_n(4))/obj[4]
        except Exception as e:
            print("error at CA_Flam_Cmd",e)

    def CA_Flam_inj(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0]*self.CA_Flam_inj_n(1)+obj[1]*self.CA_Flam_inj_n(2)+obj[2]*self.CA_Flam_inj_n(3)+obj[3]*self.CA_Flam_inj_n(4))/obj[4]
        except Exception as e:
            print(e)
            return 0

    def a_cmd_toxic(self, select):  # done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_58(self.toxic_fluid)
            a_cmd_toxic = [0, 0, 0, 0]
            if (self.ReleasePhase() == "Gas"):
                a_cmd_toxic[0] = data[0]
                a_cmd_toxic[1] = data[4]
                a_cmd_toxic[2] = data[8]
                a_cmd_toxic[3] = data[12]
            else:
                a_cmd_toxic[0] = data[2]
                a_cmd_toxic[1] = data[6]
                a_cmd_toxic[2] = data[10]
                a_cmd_toxic[3] = data[14]
            if (a_cmd_toxic[select - 1] == 1):
                return 0
            else:
                return a_cmd_toxic[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at a_cmd_toxic')

    def b_cmd_toxic(self, select):
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_58(self.toxic_fluid)
            b_cmd_toxic = [0, 0, 0, 0]
            if (self.ReleasePhase() == "Gas"):
                b_cmd_toxic[0] = data[1]
                b_cmd_toxic[1] = data[5]
                b_cmd_toxic[2] = data[9]
                b_cmd_toxic[3] = data[13]
            else:
                b_cmd_toxic[0] = data[3]
                b_cmd_toxic[1] = data[7]
                b_cmd_toxic[2] = data[11]
                b_cmd_toxic[3] = data[15]
            return b_cmd_toxic[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at b_cmd_toxic')

    def a_inj_toxic(self, select):  # done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_59(self.toxic_fluid)
            a_inj_toxic = [0, 0, 0, 0]
            if (self.ReleasePhase() == "Gas"):
                a_inj_toxic[0] = data[0]
                a_inj_toxic[1] = data[4]
                a_inj_toxic[2] = data[8]
                a_inj_toxic[3] = data[12]
            else:
                a_inj_toxic[0] = data[2]
                a_inj_toxic[1] = data[6]
                a_inj_toxic[2] = data[10]
                a_inj_toxic[3] = data[14]
            return a_inj_toxic[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at a_inj_toxic')

    def b_inj_toxic(self, select):  # done
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_59(self.toxic_fluid)
            b_inj_toxic = [0, 0, 0, 0]
            if (self.ReleasePhase() == "Gas"):
                b_inj_toxic[0] = data[1]
                b_inj_toxic[1] = data[5]
                b_inj_toxic[2] = data[9]
                b_inj_toxic[3] = data[13]
            else:
                b_inj_toxic[0] = data[3]
                b_inj_toxic[1] = data[7]
                b_inj_toxic[2] = data[11]
                b_inj_toxic[3] = data[15]
            return b_inj_toxic[select - 1]
        except Exception as e:
            return 0
            print(e)
            print('exception at b_inj_toxic')

    def fact_mit_toxic(self):  # checked
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
            print('exception at fact_mit_toxic')

    def TYPE_FLUID(self):  # done
        try:
            API_TYPE = "TYPE 0"
            if (self.FLUID == ""):
                API_TYPE = "TYPE 0"
            else:
                if (self.FLUID == "C1-C2" or self.FLUID == "C13-C16" or self.FLUID == "C17-C25" or self.FLUID == "C25+" or
                    self.FLUID == "C3-C4" or self.FLUID == "C5" or self.FLUID == "C6-C8" or self.FLUID == "C9-C12" or
                    self.FLUID == "Acid" or self.FLUID == "AlCl3" or self.FLUID == "H2" or self.FLUID == "H2S" or self.FLUID == "HCl" or
                    self.FLUID == "HF" or self.FLUID == "Nitric Acid" or self.FLUID == "NO2" or self.FLUID == "Phosgene" or
                    self.FLUID == "Pyrophoric" or self.FLUID == "Steam" or self.FLUID == "TDI" or self.FLUID == "Water" or self.FLUID == "Ammonia"
                    or self.FLUID == "Chorine"):
                        API_TYPE = "TYPE 0"
                elif (self.FLUID == "CO" or self.FLUID == "DEE" or self.FLUID == "EE" or self.FLUID == "EEA" or self.FLUID == "EG" or
                    self.FLUID == "EO" or self.FLUID == "Methanol" or self.FLUID == "PO" or self.FLUID == "Styrene" or self.FLUID == "Aromatics"):
                        API_TYPE = "TYPE 1"
                else:
                    API_TYPE = "TYPE 0"
            return API_TYPE
        except Exception as e:
            return 0
            print(e)
            print('exception at type fluid')

    def RATE_N_toxic(self, i):
        try:
            if (self.TYPE_FLUID() == "TYPE 0" and self.ReleasePhase() == "Liquid"):
                return 0
            else:
                rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
                if i == 1:
                    return rwcofholesize.rate_n_small
                elif i == 2:
                    return rwcofholesize.rate_n_medium
                elif i == 3:
                    return rwcofholesize.rate_n_large
                else:
                    return rwcofholesize.rate_n_rupture
        except Exception as e:
            print(e)
            return 0

    def ca_cmdn_cont_toxic(self, select, i):  # done
        try:
            x = self.RATE_N(i) * self.toxic_percent / 100
            return (self.a_cmd_toxic(select) * pow(x, self.b_cmd_toxic(select)) * (1 - self.fact_mit()))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmdn_cont_toxic')

    def eneff_n_toxic(self, i):
        try:
            rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
            if i == 1:
                return rwcofholesize.eneff_n_small
            elif i == 2:
                return rwcofholesize.eneff_n_medium
            elif i == 3:
                return rwcofholesize.eneff_n_large
            else:
                return rwcofholesize.eneff_n_rupture
        except Exception as e:
            print(e)
            return 0

    def mass_n_toxic(self, i):
        try:
            rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
            if i == 1:
                return rwcofholesize.mass_n_small
            elif i == 2:
                return rwcofholesize.mass_n_medium
            elif i == 3:
                return rwcofholesize.mass_n_large
            else:
                return rwcofholesize.mass_n_rupture
        except Exception as e:
            print(e)
            return 0

    def ca_cmdn_inst_toxic(self, select, i):  # done
        try:
            x = self.mass_n_toxic(i) * self.toxic_percent / 100
            if (self.eneff_n_toxic(i) == 0):
                return 0
            else:
                return self.a_cmd_toxic(select) * pow(x, self.b_cmd_toxic(select)) * (1 - self.fact_mit()) * (1 / self.eneff_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_cmdn_inst_toxic')

    def ca_injn_cont_toxic(self, select, i):  # done
        x = self.RATE_N(i) * self.toxic_percent / 100
        try:
            return self.a_inj_toxic(select) * pow(x, self.b_inj_toxic(select)) * (1 - self.fact_mit())
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_cont_toxic')

    def ca_injn_inst_toxic(self, select, i):  # done
        x = self.mass_n_toxic(i) * self.toxic_percent / 100
        try:
            if (self.eneff_n(i) == 0):
                return 0
            else:
                return self.a_inj_toxic(select) * pow(x, self.b_inj_toxic(select)) * ((1 - self.fact_mit()) / self.eneff_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at ca_injn_inst_toxic')

    def fact_n_ic(self, i):
        try:
            rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
            if i == 1:
                return rwcofholesize.factIC_n_small
            elif i == 2:
                return rwcofholesize.factIC_n_medium
            elif i == 3:
                return rwcofholesize.factIC_n_large
            else:
                return rwcofholesize.factIC_n_rupture
        except Exception as e:
            print(e)
            return 0

    def CA_AINL_CMD_n_toxic(self, i):
        try:
            return self.ca_cmdn_inst_toxic(3, i) * self.fact_n_ic(i) + self.ca_cmdn_cont_toxic(1, i) * (1 - self.fact_n_ic(i))
        except Exception as e:
            print(e)
            return 0

    def CA_AIL_CMD_n_toxic(self, i):
        try:
            return self.ca_cmdn_inst_toxic(4, i) * self.fact_n_ic(i) + self.ca_cmdn_cont_toxic(2, i) * (1 - self.fact_n_ic(i))
        except:
            return 0

    def CA_AINL_INJ_n_toxic(self, i):
        try:
            return self.ca_injn_inst_toxic(3, i) * self.fact_n_ic(i) + self.ca_injn_cont_toxic(1, i) * (1 - self.fact_n_ic(i))
        except:
            return 0

    def CA_AIL_INJ_n_toxic(self, i):
        try:
            return self.ca_injn_inst_toxic(4, i) * self.fact_n_ic(i) + self.ca_injn_cont_toxic(2, i) * (1 - self.fact_n_ic(i))
        except:
            return 0

    def auto_ignition_temp_toxic(self):
        try:
            tbl52 = DAL_CAL.POSTGRESQL.GET_TBL_52(self.toxic_fluid)
            return (tbl52[9] - 32) / 1.8  # doi tu do K sang do C
        except Exception as e:
            print(e)
            return 0

    def fact_ait_toxic(self):  # checked
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.toxic_fluid)
            ait = data[9]
            if ((self.STORED_TEMP + (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6))) <= ait):
                return 0
            elif ((self.STORED_TEMP - (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6))) >= ait):
                return 1
            else:
                return (self.STORED_TEMP - ait + (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6))) / (2 * (DAL_CAL.POSTGRESQL.GET_TBL_3B21(6)))
        except Exception as e:
            return 0
            print(e)
            print('exception at fact_ait_toxic')

    def CA_Flam_Cmd_n_toxic(self, i):
        try:
            return self.CA_AIL_CMD_n_toxic(i) * self.fact_ait_toxic() + self.CA_AINL_CMD_n_toxic(i) * (1 - self.fact_ait_toxic())
        except:
            return 0

    def CA_Flam_inj_n_toxic(self, i):
        try:
            return self.CA_AIL_INJ_n_toxic(i) * self.fact_ait_toxic() + self.CA_AINL_INJ_n_toxic(i) * (1 - self.fact_ait_toxic())
        except:
            return 0

    def CA_Flam_Cmd_toxic(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return (obj[0] * self.CA_Flam_Cmd_n_toxic(1) + obj[1] * self.CA_Flam_Cmd_n_toxic(2) + obj[2] * self.CA_Flam_Cmd_n_toxic(3) +obj[3] * self.CA_Flam_Cmd_n_toxic(4)) / obj[4]

    def CA_Flam_inj_toxic(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            return (obj[0] * self.CA_Flam_inj_n_toxic(1) + obj[1] * self.CA_Flam_inj_n_toxic(2) + obj[2] * self.CA_Flam_inj_n_toxic(3) + obj[3] * self.CA_Flam_inj_n_toxic(4)) / obj[4]
        except Exception as e:
            print(e)
            return 0
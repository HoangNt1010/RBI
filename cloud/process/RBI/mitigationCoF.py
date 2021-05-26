import math
import numpy as np
#from rbi import MYSQL_CAL as DAL_CAL
from cloud.process.RBI import Postgresql as DAL_CAL
from cloud import models
from cloud.process.RBI import CA_CAL
class FinancialNomalCOF: #LEVEL 1
    def __init__(self,proposalID,FLUID,TOXIC_FLUID,toxic_percent,API_COMPONENT_TYPE_NAME,MATERIAL_COST,CA_cmd,CA_inj,FLUID_PHASE,MITIGATION_SYSTEM,STORED_TEMP,store_pressure,process_unit,outage_multiplier,production_cost,personal_density,injure_cost,evironment_cost):
        self.proposalID = proposalID
        self.FLUID = FLUID
        self.TOXIC_FLUID = TOXIC_FLUID
        self.toxic_percent = toxic_percent
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.MATERIAL_COST =MATERIAL_COST
        self.CA_cmd = CA_cmd
        self.CA_inj = CA_inj
        self.FLUID_PHASE = FLUID_PHASE
        self.MITIGATION_SYSTEM = MITIGATION_SYSTEM
        self.STORED_TEMP = STORED_TEMP
        self.store_pressure=store_pressure
        # hai them
        self.process_unit=process_unit
        self.outage_multiplier=outage_multiplier
        self.production_cost=production_cost
        self.personal_density=personal_density
        self.injure_cost=injure_cost
        self.evironment_cost=evironment_cost

    def outage_cmd_n(self,i):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        try:
            if i==1: return obj[9]
            if i==2: return obj[10]
            if i==3: return obj[11]
            if i==4: return obj[12]
        except Exception as e:
            return 0

    def HoleCost(self,i):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        try:
            if i == 1: return obj[5]
            if i == 2: return obj[6]
            if i == 3: return obj[7]
            if i == 4: return obj[8]
        except Exception as e:
            return 0

    def FC_cmd(self):
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return ((obj[0]*self.HoleCost(1)+obj[1]*self.HoleCost(2)+obj[2]*self.HoleCost(3)+obj[3]*self.HoleCost(4))/obj[4])*self.MATERIAL_COST

    def FC_affa(self):
        try:
            rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
            equipcost = self.process_unit
            # print('equipcost', equipcost)
            return self.CA_cmd *equipcost
        except:
            return 0

    def Outage_affa(self):
        try:
            # print('self.FC_affa()',self.FC_affa())
            if self.FC_affa()==0:
                return 0
            else:
                return pow(10,(1.242+0.585*math.log10(self.FC_affa()*pow(10,-6))))
        except Exception as e:
            print(e)
            return 0

    def outage_cmd(self):
        rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
        outage_multiplier = self.outage_multiplier
        obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
        return ((obj[0]*obj[9]+obj[1]*obj[10]+obj[2]*obj[11]+obj[3]*obj[12])/obj[4])*outage_multiplier

    def FC_prod(self):
        try:
            rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
            return (self.outage_cmd() + self.Outage_affa()) * self.production_cost
        except Exception as e:
            print(e)
            return 0

    def FC_inj(self):
        rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
        popdens = self.personal_density
        injcost = self.injure_cost
        return self.CA_inj * popdens * injcost

    def NBP(self):
        data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
        nbp  = ((data[2] -32)/1.8)
        return nbp

    def frac_evap(self):
        try:
            if (self.FLUID == "C6-C8"):
                return 0.9
            elif (self.FLUID == "C1-C2"):
                return 1
            elif (self.FLUID == "C3-C5" or self.FLUID == "H2" or self.FLUID == "H2S" or self.FLUID == "HF" or self.FLUID == "CO" or self.FLUID == "DEE" or self.FLUID == "HCl" or self.FLUID == "Phosgene" or self.FLUID =="Methanol" or self.FLUID == "PO" or self.FLUID == "EO"):
                return 1
            elif (self.FLUID == "C9-C12"):
                return 0.5
            elif (self.FLUID == "C13-C16"):
                return 0.1
            elif (self.FLUID == "C17-C25"):
                return 0.05
            elif (self.FLUID == "C25+"):
                return 0.02
            elif (self.FLUID == "Acid"):
                return 0.9
            elif (self.FLUID == "Nitric Acid"):
                return 0.8
            elif (self.FLUID == "NO2"):
                return 0.75
            elif (self.FLUID == "TDI"):
                return 0.15
            elif (self.FLUID == "Styrene"):
                return 0.6
            elif (self.FLUID == "EEA"):
                return 0.65
            elif (self.FLUID == "EE"):
                return 0.75
            elif (self.FLUID == "EG"):
                return 0.45
            elif (self.FLUID == "AlCl3"):
                return 0
            else:
                C12=DAL_CAL.POSTGRESQL.GET_TBL_3B21(12)
                NBP=self.NBP()
                x=(((-7.1408 + ((0.0085827 * C12) * (NBP+32))) - ((3.5594 * math.pow(10, -6)) * math.pow(C12 * (NBP+32), 2.0))) + (2331.1 / (C12 * (NBP+32)))) - (203545.0 / math.pow(C12 * (NBP+32), 2.0))
                return x
        except:
            return 1

    def mass_n(self,i):
        rwcofholesize = models.RwFullCoFHoleSize.objects.get(id=self.proposalID)
        if i==1:
            return rwcofholesize.mass_n_small
        elif i==2:
            return rwcofholesize.mass_n_medium
        elif i==3:
            return rwcofholesize.mass_n_large
        else:
            return rwcofholesize.mass_n_rupture

    def liquid_density(self):
        try:
            data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            return data[1] * 16.02
        except:
            return 0

    def Vol_env_n(self,i):
        try:
            C13 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(13)
            return (1.8*self.mass_n(i)*(1-self.frac_evap()))/self.liquid_density()
        except:
            return 0

    def FC_environ(self):
        try:
            rwInputCa = models.RwInputCaLevel1.objects.get(id=self.proposalID)
            evironment_cost = self.evironment_cost
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            x = obj[0]*self.Vol_env_n(1) + obj[1]*self.Vol_env_n(2) + obj[2]*self.Vol_env_n(3) + obj[3]*self.Vol_env_n(4)
            return x*evironment_cost/obj[4]
        except:
            return 0

    def FC_total(self):
        try:
            return self.FC_cmd()+self.FC_affa()+self.FC_prod()+self.FC_inj()+self.FC_environ()
        except:
            return 0

    def FC_Category(self):
        if (self.FC_total() <= 10000):
            return "A"
        elif (self.FC_total() <= 100000):
            return "B"
        elif (self.FC_total() <= 1000000):
            return "C"
        elif (self.FC_total() <= 10000000):
            return "D"
        else:
            return "E"
def FinancialTankBottomCoF(proposalID,productioncost,nominaldiameter):
    rwAss = models.RwAssessment.objects.get(id=proposalID)
    comp = models.ComponentMaster.objects.get(componentid=rwAss.componentid_id)
    # isshell = False
    # if comp.componenttypeid_id == 9 or comp.componenttypeid_id == 13:
    # if comp.componenttypeid_id == 13:
    #     isshell = True
    rwinputca = models.RwInputCaTank.objects.get(id=proposalID)
    rwstream = models.RwStream.objects.get(id=proposalID)
    rwcomponent = models.RwComponent.objects.get(id=proposalID)
    rwequipment = models.RwEquipment.objects.get(id=proposalID)
    rwmaterial = models.RwMaterial.objects.get(id=proposalID)
    rwequipment = models.RwEquipment.objects.get(id=proposalID)
    cacal = CA_CAL.CA_TANK_BOTTOM(Soil_type=rwequipment.typeofsoil, TANK_FLUID=rwstream.tankfluidname,
                                  Swg=rwequipment.distancetogroundwater,
                                  TANK_DIAMETER=nominaldiameter,
                                  FLUID_HEIGHT=rwstream.fluidheight,
                                  API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(
                                      apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                  PREVENTION_BARRIER=bool(rwcomponent.releasepreventionbarrier),
                                  EnvironSensitivity=rwequipment.environmentsensitivity,
                                  MATERIAL_COST=rwmaterial.costfactor,
                                  PRODUCTION_COST=productioncost,
                                  P_lvdike=rwstream.fluidleavedikepercent,
                                  P_onsite=rwstream.fluidleavedikeremainonsitepercent,
                                  P_offsite=rwstream.fluidgooffsitepercent,
                                  Concrete_Asphalt=rwcomponent.concretefoundation)
    FC_TOTAL = cacal.FC_total_bottom()
    return FC_TOTAL
def FinancialShellCOF(proposalID,equip_cost,equip_outage_multiplier,prod_cost,pop_dens,inj_cost):
    rwAss = models.RwAssessment.objects.get(id=proposalID)
    comp = models.ComponentMaster.objects.get(componentid=rwAss.componentid_id)
    # isshell = False
    # if comp.componenttypeid_id == 9 or comp.componenttypeid_id == 13:
    # if comp.componenttypeid_id == 13:
    #     isshell = True
    rwinputca = models.RwInputCaTank.objects.get(id=proposalID)
    rwstream = models.RwStream.objects.get(id=proposalID)
    rwcomponent = models.RwComponent.objects.get(id=proposalID)
    rwequipment = models.RwEquipment.objects.get(id=proposalID)
    rwmaterial = models.RwMaterial.objects.get(id=proposalID)
    rwequipment = models.RwEquipment.objects.get(id=proposalID)



    phase_fluid_storage = rwstream.storagephase
    cacal = CA_CAL.CA_SHELL(FLUID=rwinputca.api_fluid, FLUID_HEIGHT=rwstream.fluidheight,
                            SHELL_COURSE_HEIGHT=rwinputca.shell_course_height,
                            TANK_DIAMETER=rwcomponent.nominaldiameter,
                            EnvironSensitivity=rwequipment.environmentsensitivity,
                            P_lvdike=rwstream.fluidleavedikepercent,
                            P_onsite=rwstream.fluidleavedikeremainonsitepercent,
                            P_offsite=rwstream.fluidgooffsitepercent,
                            MATERIAL_COST=rwmaterial.costfactor,
                            API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(
                                apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                            PRODUCTION_COST=rwinputca.productioncost,
                            Soil_type=rwequipment.typeofsoil,
                            TANK_FLUID=rwstream.tankfluidname,
                            CHT=rwcomponent.shellheight, PROD_COST=prod_cost,
                            EQUIP_OUTAGE_MULTIPLIER=equip_outage_multiplier,
                            EQUIP_COST=equip_cost, POP_DENS=pop_dens,
                            INJ_COST=inj_cost,
                            release_Fluid_Percent_Toxic=rwstream.releasefluidpercenttoxic,
                            FLUID_PHASE=phase_fluid_storage, proposalID=proposalID)
    FC_TOTAL = cacal.CA_total_shell()
    return FC_TOTAL




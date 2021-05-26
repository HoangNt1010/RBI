import math
import numpy as np
from cloud.process.RBI import Postgresql as DAL_CAL
from cloud.process.RBI import CA_CAL
from cloud import models

class CA_CAL_LV2:
    def __init__(self, Psat=0, FRACT_Liquid=0,FRACT_Vapor=0,LOWER_FLAMABILITY=0,UPPER_FLAMABILITY=0,HEAT_COMBUSTION=0,TEMP_FLASH=0,FRACT_FLASH=0,HEAT_COMBUSTION_Liquid=0,HEAT_COMBUSTION_Vapor=0,TEMP_BUBBLE=0,TEMP_DEW=0,
                 deltaHv=0, STORED_PRESSURE=0,ATMOSPHERIC_PRESSURE=101.325,NominalDiametter=0, STORED_TEMP=0,MASS_INVERT=0,DETECTION_TYPE="",ISOLATION_TYPE="", SURFACE="",TEMP_GROUND=0, BUBBLE_POINT_PRESSURE=0,
                 WIND_SPEED_MEASURED=0, MFRAC_FLAM=0,TEMP_FLASH_POINT=0, FLUID="", ATMOSPHERIC_TEMP=0, ATMOSPHERIC_AIR_DENSITY=1.225, ATMOSPHERIC_RELATIVE_HUMIDITY=0, ATMOSPHERIC_WATER_PARTIAL_PRESSURE=0,
                 BRUST_PRESSURE=0,XS_FBALL=0, YIELD_FACTOR={0.03:0.19}, API_COMPONENT_TYPE_NAME="", TOX_LIM=0, MOL_FRAC_TOX=0, EQUIPMENT_STORED_VAPOR=0, N_V=0):
        self.Psat=Psat
        self.FRACT_Liquid=FRACT_Liquid
        self.FRACT_Vapor=FRACT_Vapor
        self.LOWER_FLAMABILITY=LOWER_FLAMABILITY
        self.UPPER_FLAMABILITY=UPPER_FLAMABILITY
        self.HEAT_COMBUSTION=HEAT_COMBUSTION
        self.TEMP_FLASH=TEMP_FLASH
        self.FRACT_FLASH=FRACT_FLASH
        self.HEAT_COMBUSTION_Liquid=HEAT_COMBUSTION_Liquid
        self.HEAT_COMBUSTION_Vapor=HEAT_COMBUSTION_Vapor
        self.TEMP_BUBBLE=TEMP_BUBBLE
        self.TEMP_DEW=TEMP_DEW
        self.deltaHv=deltaHv
        self.STORED_PRESSURE=STORED_PRESSURE*1000
        self.ATMOSPHERIC_PRESSURE=ATMOSPHERIC_PRESSURE #=101.325
        self.NominalDiametter=NominalDiametter
        self.STORED_TEMP=STORED_TEMP
        self.MASS_INVERT=MASS_INVERT
        self.DETECTION_TYPE=DETECTION_TYPE #available
        self.ISOLATION_TYPE=ISOLATION_TYPE #availbale
        self.SURFACE=SURFACE
        self.TEMP_GROUND=TEMP_GROUND
        self.BUBBLE_POINT_PRESSURE=BUBBLE_POINT_PRESSURE
        self.WIND_SPEED_MEASURED=WIND_SPEED_MEASURED
        self.MFRAC_FLAM=MFRAC_FLAM
        self.TEMP_FLASH_POINT=TEMP_FLASH_POINT
        self.FLUID=FLUID #available
        self.ATMOSPHERIC_TEMP=ATMOSPHERIC_TEMP
        self.ATMOSPHERIC_AIR_DENSITY=ATMOSPHERIC_AIR_DENSITY #=1.225
        self.ATMOSPHERIC_RELATIVE_HUMIDITY=ATMOSPHERIC_RELATIVE_HUMIDITY #k ro bang bao nhieu
        self.ATMOSPHERIC_WATER_PARTIAL_PRESSURE=ATMOSPHERIC_WATER_PARTIAL_PRESSURE
        self.BRUST_PRESSURE=BRUST_PRESSURE
        self.XS_FBALL=XS_FBALL
        self.YIELD_FACTOR=YIELD_FACTOR
        self.API_COMPONENT_TYPE_NAME=API_COMPONENT_TYPE_NAME
        self.TOX_LIM=TOX_LIM
        self.MOL_FRAC_TOX=MOL_FRAC_TOX
        self.EQUIPMENT_STORED_VAPOR=EQUIPMENT_STORED_VAPOR
        self.N_V=N_V

    def moleculer_weight(self):
        # print('self.FLUID= ',self.FLUID)
        try:
            if not(self.FLUID is None):
                data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            else:
                return 0
            return data[0]
        except:
            return 0
    def ait(self):
        try:
            if not(self.FLUID is None):
                data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            else:
                return 0
            return data[9]
        except:
            return 0

    def vapour_density(self):
        try:
            return (self.moleculer_weight()*self.STORED_PRESSURE)/(18.314*self.STORED_TEMP)
        except:
            return 0
    def liquid_density(self):
        try:
            if not(self.FLUID is None):
                data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
            else:
                return 0
            return data[1]*16.02
        except:
            return 0

    #Release Hole Size
    def d_n(self, i): #checked
        try:
            if not(self.FLUID is None):
                print("hjx hjx", self.FLUID)
                if(i == 1):
                    return 6.4
                elif(i == 2):
                    return 25
                elif(i == 3):
                    return 102
                else:
                    return min(self.NominalDiametter , 406)
            else:
                return 0
        except Exception as e:
            print(e)
            print('exception at d_n')

    def a_n(self, i): #checked #dung
        return math.pi * pow(self.d_n(i),2) / 4

    def C_P(self): #checked #ideal gas specific heat capacity
        try:
            if not (self.FLUID is None):
                data = DAL_CAL.POSTGRESQL.GET_TBL_52(self.FLUID)
                t = self.STORED_TEMP + 273.15
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
            else:
                return 0
        except Exception as e:
            print(e)
            print('exception at C_p')
    def ReleasePhase(self):
        if (self.STORED_PRESSURE >= self.ATMOSPHERIC_PRESSURE and self.STORED_PRESSURE <= self.Psat):
            return "Gas"
        elif(self.ATMOSPHERIC_PRESSURE >= self.Psat and self.ATMOSPHERIC_PRESSURE <= self.STORED_PRESSURE):
            return "Liquid"
        else:
            return "Two-phase"

    def ideal_gas_ratio(self):
        if self.FLUID == "HCl":
            return 1.41
        elif self.FLUID == "Nitric Acid" or self.FLUID == "NO2" or self.FLUID == "Phosgene" or self.FLUID == "TDI":
            return 1.5
        else:
            return max(self.C_P() / (self.C_P() - 8.314), 1.01)
#Release Rate
    def W_n(self, i):
        try:
            C1 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(1)
            C2 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(2)
            if (self.ReleasePhase() == "Gas" ):
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
    #Fluid Inventory Avaiable
    def t_n(self, i): #checked
        try:
            wn = self.W_n(i)
            print("met vc", (DAL_CAL.POSTGRESQL.GET_TBL_3B21(3)) / wn)
            if(wn == 0):
                return 0
            else:
                return (DAL_CAL.POSTGRESQL.GET_TBL_3B21(3)) / wn
        except Exception as e:
            print(e)
            print('exception at def t_n')
    def releaseType(self, i): #done
        try:
            tn = self.t_n(i)
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME) #lay gff
            mass_n = self.MASS_INVERT
            c3 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(3)
            if (obj[i] == obj[1]):
                return "Continuous"
            if (((tn > 180) and (mass_n <= c3 )) and ((tn > 180) and (mass_n < c3))):
                return "Continuous"
            return  "Instantaneous"
        except Exception as e:
            print(e)
            print('exception at releasetype')

    def mass_avail_n(self, i):  # checked
        try:
            return self.MASS_INVERT
        except Exception as e:
            print(e)
            return 0
    def ld_n_max(self, i):#checked
        try:
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
        except:
            return 0
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
    def mass_n(self, i):  # checked
        try:
            return min(self.rate_n(i) * self.ld_n(i), self.mass_avail_n(i))
        except Exception as e:
            return 0
            print(e)
            print('exception at mass_n')
    #estimat the Impact of dectection and isolation Systems
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
    #Releases Rate and Mass
    def frac_ro(self):
        if (self.ReleasePhase() == "Two-phase"):
            if(self.FRACT_FLASH < 0.5):
                return 1-2*self.FRACT_FLASH
            else:
                return 0
        else:
            return 1
    def rate_n(self, i): #checked
        try:
            wn = self.W_n(i)
            factdi = self.fact_di()
            rate = wn * (1 - factdi)
            if(rate == 0):
                return 1
            else:
                return rate
        except Exception as e:
            return 0
            print(e)
            print('exception at rate_n')
    def W_n_pool(self, i):
        try:
            return self.rate_n(i)*self.frac_ro()
        except Exception as e:
            return 0
            print(e)
    def W_n_jet(self, i):
        try:
            return self.rate_n(i)*(1-self.frac_ro())
        except Exception as e:
            return 0
            print(e)
    def frac_entl(self):
        try:
            frac_l=self.FRACT_Liquid
            frac_fsh=self.FRACT_FLASH
            a=(frac_l*frac_fsh)/(1-self.frac_ro())
            return a
        except Exception as e:
            return 0
            print(e)
    #boiling Liquid Pools and non-boiling liquid pools
    def tp_n(self, i): #chua ro cong thuc, viet bua
        try:
            return self.t_n(i)
        except:
            return 0
    def vp_n(self, i): #chua ro cong thuc, viet bua
        try:
            return self.d_n(i)
        except:
            return 0
    def rp_n(self, i):
        try:
            x=math.pow(8*self.vp_n(i)/math.pi,0.25)*math.pow(self.tp_n(i),0.75)
            return math.sqrt(2/3)*x
        except:
            return 0
    def erate_n(self,i):
        try:
            if(self.TEMP_BUBBLE < self.TEMP_GROUND):
                print("zo",self.SURFACE)
                if(self.SURFACE == "Moist/8% water/sandy"):
                    # print('hihihihihihi')
                    Xsurf = 3
                    Ksurf = 0.59
                    Asurf = 3.36e-7
                elif(self.SURFACE == "Average"):
                    Xsurf = 3
                    Ksurf = 0.96
                    Asurf = 4.59e-7
                elif(self.SURFACE == "Sandy/dry"):
                    Xsurf = 3
                    Ksurf = 0.26
                    Asurf = 1.98e-7
                else: #Concrete
                    # print('co can ok k ')
                    Xsurf = 1
                    Ksurf = 0.92
                    Asurf = 4.16e-7
                x=Xsurf*Ksurf*(self.TEMP_GROUND-self.TEMP_BUBBLE)
                y=DAL_CAL.POSTGRESQL.GET_TBL_3B21(14)*self.deltaHv*math.sqrt(math.pi*Asurf)
                z=math.pow(2*1*self.vp_n(i),0.5)*self.t_n(i)
                return math.pow(math.pi,1.5)*(x/y)*z
            else:
                C15=DAL_CAL.POSTGRESQL.GET_TBL_3B21(15)
                x=(self.BUBBLE_POINT_PRESSURE*self.moleculer_weight())/8.314*self.STORED_TEMP
                return C15*x*math.pow(self.WIND_SPEED_MEASURED,0.78)*math.pow(self.rp_n(i),1.89)
        except Exception as e:
            return 0
            print(e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    #probability of ignition given a releases
    def rate_flam_n(self, i):
        try:
            return self.rate_n(i)*self.MFRAC_FLAM
        except:
            return 0
    def rate_flam(self, i):
        try:
            # print('rate_flam= ', self.rate_flam_n(i))
            # print('fract_flash= ', self.FRACT_FLASH)
            if(self.ReleasePhase()=="Liquid"):
                return self.rate_flam_n(i)*(1-self.FRACT_FLASH)
            else:
                return self.rate_flam_n(i)*self.FRACT_FLASH
        except Exception as e:
            return 0
            print(e)
    def poi_amb_n(self, i):
        try:
            if(self.ReleasePhase()=="Liquid"):
                a=-1.368924e-01
                b=-7.598764e-03
                c=8.282163e-06
                d=-6.124231e-02
                e=6.876128e-02
                f=1.193736e-04
                g=2.081034e-07
                h=-4.057289e-11
                # print('a= ',a)
                C12=DAL_CAL.POSTGRESQL.GET_TBL_3B21(12)
                C4=DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)
                t=C12*self.TEMP_FLASH_POINT
                obj1=(a + b*t + c*math.pow(t,2) + d*math.pow(t,3))
                obj2=(e + f*t + g*math.pow(t,2) + h*math.pow(t,3))
                obj3=np.log(C4*self.rate_flam(i))
                # print('obj1= ',obj1)
                # print('obj2= ',obj2)
                # print('obj3= ',obj3)
                return math.exp(obj1+obj2*obj3)
            else:
                a=-6.053124e-02
                b=-9.958413e-03
                c=1.518603e-05
                d=-1.386705e-08
                e=4.564953e-02
                f=7.912392e-04
                g=-6.489153e-07
                h=7.159409e-10
                C12 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(12)
                C4 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(4)
                t = C12 * self.TEMP_FLASH_POINT
                obj1 = (a + b * t + c * math.pow(t, 2) + d * math.pow(t, 3))
                obj2 = (e + f * t + g * math.pow(t, 2) + h * math.pow(t, 3))
                obj3 = np.log(C4 * self.rate_flam(i))
                # print('obj11= ', obj1)
                # print('obj22= ', obj2)
                # print('obj33= ', obj3)
                # print('res= ', obj1+obj2*obj3)
                return math.exp(obj1+obj2*obj3)
        except:
            return 0
    def poi_ait_liquid(self):
        return 1
    def poi_ait_vapor(self):
        try:
            x=0.7+0.2*((170-self.moleculer_weight())/168)
            return max(0.7,x)
        except:
            return 0
    def poi_liquid(self, i):
        try:
            C16=DAL_CAL.POSTGRESQL.GET_TBL_3B21(16)
            poi_l_n=self.poi_amb_n(i)+(self.poi_ait_liquid()-self.poi_amb_n(i))*((self.STORED_TEMP-C16)/(self.ait()-C16))
            return poi_l_n
        except:
            return 0
    def poi_vapor(self, i):
        try:
            C16 = DAL_CAL.POSTGRESQL.GET_TBL_3B21(16)
            poi_v_n = self.poi_amb_n(i) + (self.poi_ait_vapor() - self.poi_amb_n(i)) * ((self.STORED_TEMP - C16) / (self.ait() - C16))
            return poi_v_n
        except:
            return 0
    def poi_two_phase(self, i):
        try:
            if(self.ReleasePhase()=="Liquid"):
                return self.poi_liquid(i)
            elif(self.ReleasePhase()=="Gas"):
                return self.poi_vapor(i)
            else:
                return self.poi_liquid(i)*self.FRACT_FLASH+self.poi_vapor(i)*(1-self.FRACT_FLASH)
        except:
            return 0
    #Probability of immediate Versus Delayed Ignition Given Ignition
    def poii_liquid(self, i):
        try:
            C16=DAL_CAL.POSTGRESQL.GET_TBL_3B21(16)
            if(self.releaseType(i) == "Continuous"):
                return 0.2+((self.STORED_TEMP-C16)/(self.ait()-C16))*0.8
            else:
                return 0.2+((self.STORED_TEMP-C16)/(self.ait()-C16))*0.8
        except:
            return 0
    def poii_vapor(self, i):
        try:
            C16=DAL_CAL.POSTGRESQL.GET_TBL_3B21(16)
            if(self.releaseType(i) == "Continuous"):
                return 0.5+((self.STORED_TEMP-C16)/(self.ait()-C16))*0.8
            else:
                return 0.1+((self.STORED_TEMP-C16)/(self.ait()-C16))*0.8
        except:
            return 0
    def poii_two_phase(self, i):
        try:
            if(self.ReleasePhase()=="Liquid"):
                return self.poii_liquid(i)
            elif(self.ReleasePhase()=="Gas"):
                return self.poii_vapor(i)
            else:
                return self.FRACT_FLASH*self.poii_liquid(i)+(1-self.FRACT_FLASH)*self.poi_vapor(i)
        except:
            return 0
    #Probability of VCE versus Flash Fire Given Delayed Ignition
    def pvcedi_liquid(self, i):
        try:
            if(self.releaseType(i) == "Continuous"):
                return 0.25
            else:
                return 0.125
        except:
            return 0
    def pvcedi_vapor(self, i):
        if(self.releaseType(i) == "Continuous"):
            return 0.5
        else:
            return 0.25
    def pvcedi_two_phase(self, i):
        try:
            if(self.ReleasePhase()=="Liquid"):
                return self.pvcedi_liquid(i)
            elif(self.ReleasePhase()=="Vapor"):
                return self.pvcedi_vapor(i)
            else:
                if(self.releaseType(i) == "Continuous"):
                    return self.FRACT_FLASH*0.25+(1-self.FRACT_FLASH)*0.5
                else:
                    return self.FRACT_FLASH*0.125+(1-self.FRACT_FLASH)*0.25
        except:
            return 0
    def pffdi_liquid(self, i):
        if(self.releaseType(i) == "Continuous"):
            return 0.75
        else:
            return 0.5
    def pffdi_vapor(self, i):
        if(self.releaseType(i) == "Continuous"):
            return 0.825
        else:
            return 0.75
    def pffdi_two_phase(self, i):
        try:
            if(self.ReleasePhase()=="Liquid"):
                return self.pffdi_liquid(i)
            elif(self.ReleasePhase()=="Gas"):
                return self.pffdi_vapor(i)
            else:
                return self.FRACT_FLASH*self.pffdi_liquid(i)+(1-self.FRACT_FLASH)*self.pffdi_vapor(i)
        except:
            return 0
    #Probability of Fireball Given Immediate Ignition
    def pfbii(self, i):
        if(self.releaseType(i) == "Instantaneous"):
            if(self.ReleasePhase() == "Gas" or self.ReleasePhase() == "Two-Phase"):
                return 1
        else:
            return 0
    #Event Outcome Probabilities
    def pvce_vapor(self, i):
        try:
            return self.poi_vapor(i)*(1-self.poii_vapor(i))*(1-self.pvce_vapor(i))
        except:
            return 0
    def psafe_two(self, i):
        try:
            return 1-self.poi_two_phase(i)
        except:
            return 0
    def ppool_liquid(self, i):
        try:
            return self.poi_liquid(i)*self.poii_liquid(i)
        except:
            return 0
    #Pool Fire Burning Rate
    def m_b(self): #danh cho tank
        try:
            C17=DAL_CAL.POSTGRESQL.GET_TBL_3B21(17)
            if (self.TEMP_BUBBLE < self.TEMP_GROUND): #boiling
                x=C17*self.HEAT_COMBUSTION_Liquid
                y=self.C_P()*math.fabs((self.TEMP_BUBBLE-self.ATMOSPHERIC_TEMP))+self.deltaHv
                return x/y
            else:
                return (C17*self.HEAT_COMBUSTION_Liquid)/self.deltaHv
        except:
            return 0
    #Pool Fire Size
    def aburn_pf_n(self, i):
        try:
            mb=self.m_b()
            print("chua hieu lam", mb)
            return self.W_n_pool(i)/mb
        except:
            return 0
    def amaxpf_n(self, i):
        try:
            C18=DAL_CAL.POSTGRESQL.GET_TBL_3B21(18)
            massavail=self.mass_avail_n(i)
            liquiddensity=self.liquid_density()
            return massavail/(C18*self.frac_ro()*liquiddensity)
        except:
            return 0
    def apf_n(self, i):
        try:
            return min(self.aburn_pf_n(i),self.amaxpf_n(i))
        except:
            return 0
    def rpf_n(self, i):
        try:
            return math.sqrt(self.apf_n(i)/math.pi)
        except:
            return 0
    #Flame Length andn Flame Tilt
    def U_s(self): #chua ro thong so nay
        return 0.5
    def lpf_n(self, i):
        try:
            x=self.rpf_n(i)*math.pow((self.m_b()/self.ATMOSPHERIC_AIR_DENSITY*math.sqrt(2*self.rpf_n(i))),0.67)
            return 110*x*math.pow(self.U_s(),-0.21)
        except:
            return 0
    def Us_n(self, i):
        try:
            x=self.WIND_SPEED_MEASURED*math.pow((self.vapour_density()/2*self.m_b()*self.rpf_n(i)),0.333)
            return max(1,x)
        except:
            return 0
    def cosapf_n(self, i):
        try:
            return 1/math.sqrt(self.Us_n(i))
        except:
            return 0
    #Pool Fire Radiated Energy
    def qrad_pool_n(self, i):
        try:
            C14=DAL_CAL.POSTGRESQL.GET_TBL_3B21(14)
            x=C14*0.35*self.m_b()*self.HEAT_COMBUSTION_Liquid*math.pi*math.pow(self.rpf_n(i),2)
            y=2*math.pi*self.rpf_n(i)*self.lpf_n(i)+math.pi*math.pow(self.rpf_n(i),2)
            return x/y
        except:
            return 0
    def xs_n(self, i): # chua ro cong thuc nay
        return 1
    def P_w(self):
        try:
            C20=DAL_CAL.POSTGRESQL.GET_TBL_3B21(20)
            C21=DAL_CAL.POSTGRESQL.GET_TBL_3B21(21)
            return C20*self.ATMOSPHERIC_RELATIVE_HUMIDITY*math.exp(14.4114-(C21/self.ATMOSPHERIC_TEMP))
        except:
            return 0
    def Tatm(self, i):
        try:
            C19=DAL_CAL.POSTGRESQL.GET_TBL_3B21(19)
            return C19*math.pow(self.P_w()*self.xs_n(i),-0.09)
        except:
            return 0
    def f_v_n(self, i):
        try:
            cos=self.cosapf_n(i)
            sin=math.sqrt(1-math.pow(cos,2))
            # print('cos = ', cos)
            tan=sin/cos
            # print('self.lpf_n(i)=',self.lpf_n(i))
            # print('self.rpf_n(i)=',self.rpf_n(i))
            # print('xs_n(i)=', self.xs_n(i))
            X=self.lpf_n(i)/self.rpf_n(i)
            Y=self.xs_n(i)/self.rpf_n(i)
            Ap=math.pow(X,2)+math.pow(Y+1,2)-2*X*(Y+1)*sin
            Bp=math.pow(X,2)+math.pow(Y+1,2)-2*X*(Y-1)*sin
            Cp=1+(math.pow(Y,2)-1)*math.pow(cos,2)
            # print('Ap= ', Ap)
            # print('Bp= ', Bp)
            # print('Cp= ', Cp)
            Fvn1=((X*cos)/Y-X*sin)*((math.pow(X,2)+math.pow(Y+1,2)-2*Y*(1+sin))/math.pi*math.sqrt(Ap*Bp))*1/(math.tan((Ap*(Y-1))/Bp*(Y+1)))
            # print('okokokokokokokokok')
            Fvn2=(cos/math.pi*math.sqrt(Cp))*1/math.tan((X*Y-(math.pow(Y,2)-1)*sin)/(math.sqrt(math.pow(Y,2))*math.sqrt(Cp)))+1/math.tan((sin*math.sqrt(math.pow(Y,2)))/math.sqrt(Cp))
            # print('concacconcac')
            if(Y-1<0):
                Fvn3 = ((X * cos) / math.pi * (Y - X * sin)) * 1 / math.tan(math.sqrt((1 / (Y + 1))))
            else:
                Fvn3=((X*cos)/math.pi*(Y-X*sin))*1/math.tan(math.sqrt((Y-1)/(Y+1)))
            return Fvn1 + Fvn2 - Fvn3
        except:
            return 0
    def f_h_n(self, i):
        try:
            cos = self.cosapf_n(i)
            sin = math.sqrt(1 - math.pow(cos, 2))
            tan = sin / cos
            X = self.lpf_n(i) / self.rpf_n(i)
            Y = self.xs_n(i) / self.rpf_n(i)
            Ap = math.pow(X, 2) + math.pow(Y + 1, 2) - 2 * X * (Y + 1) * sin
            Bp = math.pow(X, 2) + math.pow(Y + 1, 2) - 2 * X * (Y - 1) * sin
            Cp = 1 + (math.pow(Y, 2) - 1) * math.pow(cos, 2)
            # print('Ap= ', Ap)
            # print('Bp= ', Bp)
            # print('Cp= ', Cp)
            if(Y-1<0):
                Fhn1=(1/math.pi)*(1/math.tan(math.sqrt(1/(Y+1))))
            else:
                Fhn1 = (1 / math.pi) * (1 / math.tan(math.sqrt((Y - 1) / (Y + 1))))
            Fhn2=((math.pow(X,2)+math.pow(Y+1,2)-2*(Y+1+X*Y*sin))/math.pi*math.sqrt(Ap*Bp))*(1/math.tan(math.sqrt(Ap*(Y)/Bp*(Y+1))))
            Fhn3=(sin/math.pi*math.sqrt(Cp))*1/math.tan((X*Y-(math.pow(Y,2)-1)*sin)/(math.sqrt(math.pow(Y,2))*math.sqrt(Cp)))*1/math.tan((sin*math.sqrt(math.pow(Y,2)))/math.sqrt(Cp))
            return Fhn1 - Fhn2 + Fhn3
        except:
            return 0
    def fcyl_n(self, i):
        try:
            # print('self.f_v_n(i)=', self.f_v_n(i))
            # print('self.f_h_n(i)=', self.f_h_n(i))
            return math.sqrt(math.pow(self.f_v_n(i),2)+math.pow(self.f_h_n(i),2))
        except:
            return 0
    def ith_pool_n(self, i):
        try:
            # print('OKOKOK')
            Tatm=self.Tatm(i)
            # print('ok tai day')
            Fcyl_n=self.fcyl_n(i)
            # print('van ok tai day')
            Qrad_pool_n=self.qrad_pool_n(i)
            # print('tiep tuc ok tai day')
            return Tatm*Fcyl_n*Qrad_pool_n
        except:
            return 0
    #Pool Fire Safe Distance and Consequence Area
    def xs_pool_cmd_n(self, i): #chua xac dinh duoc cong thuc
        return 1
    def xs_pool_inj_n(self, i): #ch ua xac dinh duoc cong thuc
        return 1
    def ca_pool_cmd_n(self, i):
        try:
            return math.pi*math.pow(self.xs_pool_cmd_n(i)+self.rpf_n(i),2)
        except:
            return 0
    def ca_pool_inj_n(self, i):
        try:
            return math.pi*math.pow(self.xs_pool_inj_n(i)+self.rpf_n(i),2)
        except:
            return 0
    #Jet Fire Radiated Energy
    def qrad_jet_n(self, i):
        try:
            C14=DAL_CAL.POSTGRESQL.GET_TBL_3B21(14)
            b=0.35
            return C14*b*self.W_n_jet(i)*self.HEAT_COMBUSTION_Vapor
        except:
            return 0
    #Jet Fire Safe Distance and Consequence Area
    def fp_n(self, i):
        try:
            return 1/(4*math.pi*math.pow(self.xs_n(i),2))
        except:
            return 0
    def ith_jet_n(self, i):
        try:
            Tatm=self.Tatm(i)
            qrad_jet=self.qrad_jet_n(i)
            return Tatm*qrad_jet*self.fp_n(i)
        except:
            return 0
    def xs_jet_cmd_n(self, i): #chua ro cong thuc nay
        return 1
    def xs_jet_inj_n(self, i): #chua ro cong thuc nay
        return 1
    def ca_jet_cmd_n(self, i):
        try:
            return math.pi*math.pow(self.xs_jet_cmd_n(i),2)
        except:
            return 0
    def ca_jet_inj_n(self, i):
        try:
            return math.pi*math.pow(self.xs_jet_inj_n(i),2)
        except:
            return 0
    #Fireball
    def mass_fb(self):
        try:
            return self.MFRAC_FLAM*CA_CAL.CA_NORMAL.mass_avail_n(4)
        except:
            return 0
    #Fireball size and duration
    def dmax_fb(self):
        try:
            C22=DAL_CAL.POSTGRESQL.GET_TBL_3B21(22)
            return C22*math.pow(self.mass_fb(),0.333)
        except:
            return 0
    def h_fb(self):
        try:
            return 0.75*self.dmax_fb()
        except:
            return 0
    def t_fb(self):
        try:
            C23=DAL_CAL.POSTGRESQL.GET_TBL_3B21(23)
            C24=DAL_CAL.POSTGRESQL.GET_TBL_3B21(24)
            if(self.mass_fb() <= 29937):
                return C23*math.pow(self.mass_fb(),0.333)
            else:
                return C24*math.pow(self.mass_fb(),0.167)
        except:
            return 0
    #Fireball Radiated Energy
    def b_fb(self):
        try:
            C25=DAL_CAL.POSTGRESQL.GET_TBL_3B21(25)
            return C25*math.pow(self.BRUST_PRESSURE,0.32)
        except:
            return 0
    def qrad_fball(self):
        try:
            C14=DAL_CAL.POSTGRESQL.GET_TBL_3B21(14)
            x=C14*self.b_fb()*self.mass_fb()*self.HEAT_COMBUSTION_Liquid
            y=math.pi*math.pow(self.dmax_fb(),2)*self.t_fb()
            return x/y
        except:
            return 0
    #Fireball Safe Distance and Consequence Area
    def c_fb(self):
        try:
            x=math.pow(self.dmax_fb()/2,2)
            y=math.pow(self.XS_FBALL/2,2)
            return math.sqrt(math.pow(x,2)+math.pow(y,2))
        except:
            return 0
    def fsph(self):
        try:
            return (math.pow(self.dmax_fb(),2))/(4*math.pow(self.c_fb(),2))
        except:
            return 0
    def ith_fball(self):
        try:
            Tatm=self.Tatm()
            qrad_fball=self.qrad_fball()
            fsph=self.fsph()
            return Tatm*qrad_fball*fsph
        except:
            return 0
    def xs_fball_cmd(self): #chua xac duoc cong thuc
        return 1
    def xs_fball_inj(self):
        return 1
    def ca_fball_cmd(self):
        try:
            return math.pi*math.pow(self.xs_fball_cmd(),2)
        except:
            return 0
    def ca_fball_inj(self):
        try:
            return math.pi*math.pow(self.xs_fball_inj(),2)
        except:
            return 0
    #Vapor Cloud Explosions ( VCEs )
    #TNT Equivalency Method
    def mass_vce(self): #chua xac dinh duoc cong thuc
        return 1
    def W_tnt(self):
        try:
            return (self.YIELD_FACTOR*self.mass_vce()*self.HEAT_COMBUSTION)/4648
        except:
            return 0
    def xs_vce_n(self, i): #chua xac dinh duoc cong thuc
        return 1
    def r_hs_n(self, i):
        try:
            C27=DAL_CAL.POSTGRESQL.GET_TBL_3B21(27)
            return C27*(self.xs_vce_n(i)/math.pow(self.W_tnt(),1/3))
        except:
            return 0
    def pso_n(self, i):
        try:
            C26=DAL_CAL.POSTGRESQL.GET_TBL_3B21(26)
            len=np.log(self.r_hs_n(i))
            x=math.fabs(-0.059965896+1.1288697/len-7.9625216/math.pow(len,2)+25.106738/math.pow(len,3)-30.396707/math.pow(len,4)+19.399862/math.pow(len,5)-6.8853477/math.pow(len,6)+1.2825511/math.pow(len,7)-0.097705789/math.pow(len,8))
            return C26*x
        except:
            return 0
    #VCE Safe Distance and Consequence Area
    def Pr_n(self, i):
        try:
            pson=self.pso_n(i)
            C28=DAL_CAL.POSTGRESQL.GET_TBL_3B21(28)
            return -23.8+2.92*np.log(C28*pson)
        except:
            return 0
    def xs_vce_cmd_n(self, i): #chua xac dinh duoc cong thuc
        return 1
    def xs_vce_inj_n(self, i): #chua xac dinh duoc cong thuc
        return 1
    def ca_vce_cmd_n(self, i):
        try:
            xscmd=self.xs_vce_cmd_n(i)
            #xsinj=self.xs_vce_inj_n(i)
            return math.pi*math.pow(xscmd,2)
        except:
            return 0
    def ca_vce_inj_n(self, i):
        try:
            xsinj=self.xs_vce_inj_n(i)
            return math.pi*math.pow(xsinj,2)
        except:
            return 0
    #Flash Fire Consequence Area
    def ca_flash_inj_n(self, i): #chua xac dinh duoc cong thuc nay
        return 1
    def ca_flash_cmd_n(self, i):
        try:
            ca_flash_inj=self.ca_flash_inj_n(i)
            return 0.25*ca_flash_inj
        except:
            return 0
    #Flammable Consequence for Each Release Case
    def ppool_n(self, i): #chua xac dinh duoc cong thuc nay
        return 1
    def pjet_n(self, i): #chua xac dinh duoc cong thuc nay
        return 1
    def pfball_n(self, i): #chua xac dinh duoc cong thuc nay
        return 1
    def pvce_n(self, i): #chua xac dinh duoc cong thuc nay
        return 1
    def pflash_n(self, i): #chua xac dinh duoc cong thuc nay
        return 1
    def ca_flam_cmd_n(self, i):
        try:
            ppool=self.ppool_n(i)
            ca_pool_cmd=self.ca_pool_cmd_n(i)
            pjet=self.pjet_n(i)
            ca_jet_cmd=self.ca_jet_cmd_n(i)
            pfball=self.pfball_n(i)
            pvce=self.pvce_n(i)
            cafball=self.ca_fball_cmd()
            cavce=self.ca_vce_cmd_n(i)
            pflash=self.pflash_n(i)
            caflash=self.ca_flash_cmd_n(i)
            # print('return= ',ppool*ca_pool_cmd+pjet*ca_jet_cmd+pfball*cafball+pvce*cavce+pflash*caflash)
            return ppool*ca_pool_cmd+pjet*ca_jet_cmd+pfball*cafball+pvce*cavce+pflash*caflash
        except:
            return 0
    def ca_flam_inj_n(self, i):
        try:
            ppool = self.ppool_n(i)
            ca_pool_inj = self.ca_pool_inj_n(i)
            pjet = self.pjet_n(i)
            ca_jet_inj = self.ca_jet_inj_n(i)
            pfball = self.pfball_n(i)
            pvce = self.pvce_n(i)
            cafball = self.ca_fball_inj()
            cavce = self.ca_vce_inj_n(i)
            pflash = self.pflash_n(i)
            caflash = self.ca_flash_inj_n(i)
            return ppool * ca_pool_inj + pjet * ca_jet_inj + pfball * cafball + pvce * cavce + pflash * caflash
        except:
            return 0
    #Determination of Final Flammbale Consequence Areas
    def ca_flam_cmd(self):
        try:
            # print(self.API_COMPONENT_TYPE_NAME)
            obj=DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t=obj[0]*self.ca_flam_cmd_n(1)+obj[1]*self.ca_flam_cmd_n(2)+obj[2]*self.ca_flam_cmd_n(3)+obj[3]*self.ca_flam_cmd_n(4)
            # print('obj4= ', obj[4])
            ca_cmd=t / obj[4]
            # print('ca_cmd=', ca_cmd)
            return ca_cmd
        except:
            return 0
    def ca_flam_inj(self):
        try:
            obj = DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t = obj[0] * self.ca_flam_inj_n(1) + obj[1] * self.ca_flam_inj_n(2) + obj[2] * self.ca_flam_inj_n(3) + obj[3] * self.ca_flam_inj_n(4)
            ca_inj = t / obj[4]
            return ca_inj
        except:
            return 0
    #Determine Toxic Consequences
    #Release Duration
    def ld_tox_n(self, i):
        try:
            wn=self.W_n(i)
            obj2 = self.mass_n(i)/wn
            obj3 = 60*self.ld_n_max(i)
            return min(3600, obj2, obj3)
        except:
            return 0
    #Toxic event probabilities
    def ptox_n(self, i):
        try:
            return self.psafe_two(i)
        except:
            return 0
    #Toxic consequence area
    def ca_cloud_n(self, i): #chua xac dinh duoc cong thuc
        return 1
    def ca_tox_inj_n(self, i):
        try:
            ptox=self.ptox_n(i)
            ca_cloud=self.ca_cloud_n(i)
            return ptox*ca_cloud
        except:
            return 0
    def tox_mod_lim(self):
        try:
            tox_lim=self.TOX_LIM
            mol_frac_tox=self.MOL_FRAC_TOX
            return tox_lim/mol_frac_tox
        except:
            return 0
    def ca_tox_inj(self):
        try:
            obj=DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t=obj[0]*self.ca_tox_inj_n(1)+obj[1]*self.ca_tox_inj_n(2)+obj[2]*self.ca_tox_inj_n(3)+obj[3]*self.ca_tox_inj_n(4)
            ca_tox= t / obj[4]
            return ca_tox
        except:
            return 0
    #Non-Flammable Non-Toxic Consequence
    #TNT Equivalency Method
    def w_tnt(self):
        try:
            C29=DAL_CAL.POSTGRESQL.GET_TBL_3B21(29)
            return C29*self.EQUIPMENT_STORED_VAPOR*((self.STORED_PRESSURE-101.325)/(self.ideal_gas_ratio()-1))
        except:
            return 0
    def xs_pexp_cmd(self): #chua ro cong thuc nay
        return 1
    def xs_pexp_inj(self): #chua ro cong thuc nay
        return 1
    def ca_pexp_cmd_n(self, i):
        try:
            if(i==4):
                xs=self.xs_pexp_cmd()
                return math.pi * math.pow(xs, 2)
            else:
                return 1
        except:
            return 0
    def ca_pexp_inj_n(self, i):
        try:
            if(i == 4):
                xs = self.xs_pexp_inj()
                return math.pi * math.pow(xs, 2)
            else:
                return 1
        except:
            return 0
    #TNT Equivalency Method
    def w_tnt_bleve(self):
        try:
            C30=DAL_CAL.POSTGRESQL.GET_TBL_3B21(30)
            nv=self.N_V
            return C30*nv*8.314*self.STORED_TEMP*np.log(self.STORED_PRESSURE/101.325)
        except:
            return 0
    def xs_bleve_cmd(self): #chua xac dinh duoc cong thuc
        return 1
    def xs_bleve_inj(self): #chua xac dinh duoc cong thuc
        return 1
    def ca_bleve_cmd_n(self, i):
        try:
            if(i==4):
                xs=self.xs_bleve_cmd()
                return math.pi*math.pow(xs,2)
            else:
                return 1
        except:
            return 0
    def ca_bleve_inj_n(self, i):
        try:
            if(i==4):
                xs=self.xs_bleve_inj()
                return math.pi*math.pow(xs,2)
            else:
                return 1
        except:
            return 0
    #NFNT Event Tree Probabilities
    def pnfnt_n(self, i):
        try:
            return self.psafe_two(i)
        except:
            return 0
    def ca_nfnt_cmd_n(self, i):
        try:
            pnfnt=self.pnfnt_n(i)
            capexp_cmd=self.ca_pexp_cmd_n(i)
            cableve_cmd=self.ca_bleve_cmd_n(i)
            return pnfnt*max(capexp_cmd,cableve_cmd)
        except:
            return 0
    def ca_nfnt_inj_n(self, i):
        try:
            pnfnt = self.pnfnt_n(i)
            capexp_cmd = self.ca_pexp_inj_n(i)
            cableve_cmd = self.ca_bleve_inj_n(i)
            # caleak=CA_CAL.CA_NORMAL.ca_injn_leaknfnt(i)
            max1=max(capexp_cmd,cableve_cmd)
            max2=max(max1,1)
            return pnfnt*max2
        except:
            return 0
    def ca_nfnt_cmd(self):
        try:
            obj=DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t=obj[0]*self.ca_nfnt_cmd_n(1)+obj[1]*self.ca_nfnt_cmd_n(2)+obj[2]*self.ca_nfnt_cmd_n(3)+obj[3]*self.ca_nfnt_cmd_n(4)
            ca_nfnt=t/obj[4]
            return ca_nfnt
        except:
            return 0
    def ca_nfnt_inj(self):
        try:
            obj=DAL_CAL.POSTGRESQL.GET_API_COM(self.API_COMPONENT_TYPE_NAME)
            t = obj[0] * self.ca_nfnt_inj_n(1) + obj[1] * self.ca_nfnt_inj_n(2) + obj[2] * self.ca_nfnt_inj_n(3) + obj[3] * self.ca_nfnt_inj_n(4)
            ca_nfnt = t / obj[4]
            return ca_nfnt
        except:
            return 0
    #safe
    def ca_safe_cmd(self): #chua xac dinh duoc cong thuc
        return 1
    def ca_safe_inj(self): #chua xac dinh duoc cong thuc
        return 1
    def ca_cmd(self):
        try:
            caflam=self.ca_flam_cmd()
            psafe=self.psafe_two(4)
            casafe=self.ca_safe_cmd()
            canfnt=self.ca_nfnt_cmd()
            return caflam+max(psafe*casafe,canfnt)
        except:
            return 0
    def ca_inj(self):
        try:
            caflam=self.ca_flam_inj()
            psafe=self.psafe_two(4)
            casafe=self.ca_safe_inj()
            catox=self.ca_tox_inj()
            canfnt=self.ca_nfnt_inj()
            return caflam+max(psafe*casafe,catox,canfnt)
        except:
            return 0
    def ca(self):
        try:
            cacmd=self.ca_cmd()
            cainj=self.ca_inj()
            return max(cacmd,cainj)
        except:
            return 0


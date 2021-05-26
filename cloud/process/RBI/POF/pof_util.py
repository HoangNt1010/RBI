import math 
import  numpy as np
from dateutil.relativedelta import relativedelta 
from cloud.process.RBI import Postgresql as DAL_CAL
from django.core.mail import EmailMessage
from cloud import models
from cloud.process.RBI.Object.table import Table65 as TBL65


# nhung gia tri Num_inspec, EFF khong can truyen khi su dung ham
class DM_CAL: 
    # PoF convert cataloge
    def PoFCategory(DF_total):
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
    def getTmin(obj):
        if obj.APIComponentType == "TANKBOTTOM0" or obj.APIComponentType =="TANKROOFFLOAT0":
            if (obj.ProtectedBarrier):
                t=0.05
            else:
                t=0.1
        else:
            t = obj.MinThickReq
        return t 

    def agetk(obj, age):
        return age

    def trdi(obj):
        return obj.CurrentThick

    def agerc(obj, age):
        try:
            a = age - obj.GET_AGE()[0]
            if obj.InternalCladding:
                return max(((obj.CurrentThick - (obj.NomalThick - obj.CladdingThickness)) / obj.CladdingCorrosionRate - a), 0)
            else:
                return max(((obj.CurrentThick - obj.NomalThick) / obj.CladdingCorrosionRate - a), 0)
        except:
            return 0
    def Art(obj,age):
        try:
            if obj.APIComponentType == "TANKBOTTOM0" or obj.APIComponentType == "TANKROOFFLOAT0": 
                return max((1-(obj.trdi() - obj.CorrosionRate * obj.agetk(age)) / (obj.getTmin() + obj.CA)), 0.0)
            elif (obj.InternalCladding):
                if (obj.agetk(age) < obj.agerc(age)):
                    return (obj.CladdingCorrosionRate * obj.agetk(age)/ obj.trdi())
                else:
                    a =(obj.CladdingCorrosionRate * obj.agerc(age) + obj.CorrosionRate * (obj.agetk(age) - obj.agerc(age))) / obj.trdi()
                    return (obj.CladdingCorrosionRate * obj.agerc(age) + obj.CorrosionRate * (obj.agetk(age) - obj.agerc(age))) / obj.trdi()
            else:
                if obj.trdi()==0:
                    return 1
                else:
                    return (obj.CorrosionRate * obj.agetk(age) / obj.trdi())
        except Exception as e:
            print(e)
            return 1
    def FS_Thin(obj):
        return ((obj.YieldStrengthDesignTemp + obj.TensileStrengthDesignTemp)/2) * obj.WeldJointEffciency * 1.1
    def getalpha(obj):
        return obj.ShapeFactor
    def SRp_Thin(obj):
        if obj.MINIUM_STRUCTURAL_THICKNESS_GOVERS == False:
            return (obj.Pressure * obj.Diametter)/(obj.getalpha() * obj.FS_Thin() * obj.trdi())
        else:
            # return (obj.WeldJointEffciency * obj.TensileStrengthDesignTemp * max(obj.getTmin(),obj.StructuralThickness))/(obj.FS_Thin() * obj.trdi())
            #return (obj.WeldJointEffciency * obj.TensileStrengthDesignTemp * max(obj.getTmin(),obj.StructuralThickness))/(obj.FS_Thin() * obj.YieldStrengthDesignTemp)
            return (obj.WeldJointEffciency * obj.AllowableStress * max(obj.getTmin(),obj.StructuralThickness)) / (obj.FS_Thin() * obj.trdi())
    def Pr_P1_Thin(obj):
        if obj.CR_Confidents_Level == "Low":
            return 0.5
        elif obj.CR_Confidents_Level == "Medium":
            return 0.7
        else:
            return 0.8
    def Pr_P2_Thin(obj):
        if obj.CR_Confidents_Level == "Low":
            return 0.3
        elif obj.CR_Confidents_Level == "Medium":
            return 0.2
        else:
            return 0.15
    def Pr_P3_Thin(obj):
        if obj.CR_Confidents_Level == "Low":
            return 0.2
        elif obj.CR_Confidents_Level == "Medium":
            return 0.1
        else:
            return  0.05

    def NA_Thin(obj):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(obj.ComponentNumber, obj.DM_Name[0])
        return a
    def NB_Thin(obj):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(obj.ComponentNumber, obj.DM_Name[0])
        return b
    def NC_Thin(obj):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(obj.ComponentNumber, obj.DM_Name[0])
        return c
    def ND_Thin(obj):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(obj.ComponentNumber, obj.DM_Name[0])
        return d
    def I1_Thin(obj):
        a=obj.Pr_P1_Thin() * pow(0.9,obj.NA_Thin()) * pow(0.7,obj.NB_Thin()) * pow(0.5,obj.NC_Thin()) * pow(0.4,obj.ND_Thin())
        return obj.Pr_P1_Thin() * pow(0.9,obj.NA_Thin()) * pow(0.7,obj.NB_Thin()) * pow(0.5,obj.NC_Thin()) * pow(0.4,obj.ND_Thin())
    def I2_Thin(obj):
        a=obj.Pr_P2_Thin() * pow(0.09,obj.NA_Thin()) * pow(0.2,obj.NB_Thin()) * pow(0.3,obj.NC_Thin()) * pow(0.33,obj.ND_Thin())
        return obj.Pr_P2_Thin() * pow(0.09,obj.NA_Thin()) * pow(0.2,obj.NB_Thin()) * pow(0.3,obj.NC_Thin()) * pow(0.33,obj.ND_Thin())
    def I3_Thin(obj):
        a=obj.Pr_P3_Thin() * pow(0.01,obj.NA_Thin()) * pow(0.1,obj.NB_Thin()) * pow(0.2,obj.NC_Thin()) * pow(0.27,obj.ND_Thin())
        return obj.Pr_P3_Thin() * pow(0.01,obj.NA_Thin()) * pow(0.1,obj.NB_Thin()) * pow(0.2,obj.NC_Thin()) * pow(0.27,obj.ND_Thin())
    def Po_P1_Thin(obj):
        try:
            a=obj.I1_Thin()/(obj.I1_Thin() + obj.I2_Thin() + obj.I3_Thin())
        except Exception as e:
            print(e,"Po_P1_Thin")
        return obj.I1_Thin()/(obj.I1_Thin() + obj.I2_Thin() + obj.I3_Thin())
    def Po_P2_Thin(obj):
        a = obj.I2_Thin()/(obj.I1_Thin() + obj.I2_Thin() + obj.I3_Thin())
        return obj.I2_Thin()/(obj.I1_Thin() + obj.I2_Thin() + obj.I3_Thin())
    def Po_P3_Thin(obj):
        return obj.I3_Thin()/(obj.I1_Thin() + obj.I2_Thin() + obj.I3_Thin())
    def B1_Thin(obj,age):
        # print("test b1_Thin")
        # print((1 - obj.Art(age)- obj.SRp_Thin())/math.sqrt(pow(obj.Art(age), 2) * 0.04 + pow((1 - obj.Art(age)), 2) * 0.04 + pow(obj.SRp_Thin(), 2) * pow(0.05, 2)))
        return (1 - obj.Art(age)- obj.SRp_Thin())/math.sqrt(pow(obj.Art(age), 2) * 0.04 + pow((1 - obj.Art(age)), 2) * 0.04 + pow(obj.SRp_Thin(), 2) * pow(0.05, 2))
    def B2_Thin(obj,age):
        return (1- 2*obj.Art(age)-obj.SRp_Thin())/math.sqrt(pow(obj.Art(age),2)*4*0.04 + pow(1-2*obj.Art(age),2)*0.04+pow(obj.SRp_Thin(),2)*pow(0.05,2))
    def B3_Thin(obj,age):
        return (1- 4*obj.Art(age)-obj.SRp_Thin())/math.sqrt(pow(obj.Art(age),2)*16*0.04 + pow(1-4*obj.Art(age),2)*0.04+pow(obj.SRp_Thin(),2)*pow(0.05,2))

    def API_ART(obj, a):
        if obj.APIComponentType == 'TANKBOTTOM0' or obj.APIComponentType == 'TANKROOFFLOAT0':
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

    def erfcc(obj,x):
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

    def ncdf(obj,x):
        return 1. - 0.5 * math.erfc(x / (2 ** 0.5))
    def DFB_THIN(obj, age):
        obj.EFF_THIN = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[0])
        obj.NoINSP_THINNING = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber,obj.DM_Name[0])
        if (obj.APIComponentType == 'TANKBOTTOM0' or obj.APIComponentType == 'TANKROOFFLOAT0'):
            if (obj.NomalThick == 0 or obj.CurrentThick == 0):
                return 1390
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_512(obj.API_ART(obj.Art(age)), obj.NoINSP_THINNING, obj.EFF_THIN)
                #return DAL_CAL.POSTGRESQL.GET_TBL_512(obj.API_ART(obj.Art(age)), obj.EFF_THIN)
        else:
            try:
                if (obj.NomalThick == 0 or obj.CurrentThick == 0 or obj.WeldJointEffciency == 0 or (obj.YieldStrengthDesignTemp == 0 and obj.TensileStrengthDesignTemp == 0)):
                    return 6500
                else:
                    a = obj.Po_P1_Thin() * obj.ncdf(- obj.B1_Thin(age))
                    b = obj.Po_P2_Thin() * obj.ncdf(- obj.B2_Thin(age))
                    c = obj.Po_P3_Thin() * obj.ncdf(- obj.B3_Thin(age))
                    return (a + b + c) / (1.56 * pow(10, -4))
            except Exception as e:
                print(e)
                return 0

    def DF_THIN(obj, age):
        Fwd = 1
        Fam = 1
        Fsm = 1
        if (obj.HighlyEffectDeadleg):
            Fip = 3
        else:
            Fip = 1
        if (obj.ContainsDeadlegs):
            Fdl = 3
        else:
            Fdl = 1
        # print(obj.EquipmentType)
        if obj.EquipmentType == "Tank":
            if (obj.ComponentIsWeld):
                Fwd = 1
            else:
                Fwd = 10
            if (obj.TankMaintain653):
                Fam = 1
            else:
                Fam = 5

            if (obj.AdjustmentSettle == "Recorded settlement exceeds API 653 criteria"):
                Fsm = 2
            elif (obj.AdjustmentSettle == "Recorded settlement meets API 653 criteria"):
                Fsm = 1
            elif (obj.AdjustmentSettle == "Settlement never evaluated"):
                Fsm = 1.5
            else:
                Fsm = 0
        if (
                                                                obj.OnlineMonitoring == "Amine high velocity corrosion - Electrical resistance probes" or obj.OnlineMonitoring == "Amine high velocity corrosion - Key process variable" or obj.OnlineMonitoring == "Amine low velocity corrosion - Electrical resistance probes" or obj.OnlineMonitoring == "HCL corrosion - Electrical resistance probes" or
                                                    obj.OnlineMonitoring == "HCL corrosion - Key process variable" or obj.OnlineMonitoring == "HF corrosion - Key process variable" or obj.OnlineMonitoring == "High temperature H2S/H2 corrosion - Electrical resistance probes" or obj.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Electrical resistance probes" or
                                    obj.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Key process variable" or obj.OnlineMonitoring == "Sour water high velocity corrosion - Key process variable" or obj.OnlineMonitoring == "Sour water low velocity corrosion - Electrical resistance probes" or obj.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Electrical resistance probes" or
                    obj.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Key process parameters" or obj.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion low velocity - Electrical resistance probes"):
            Fom = 10
        elif (
                                    obj.OnlineMonitoring == "Amine low velocity corrosion - Corrosion coupons" or obj.OnlineMonitoring == "HCL corrosion - Corrosion coupons" or obj.OnlineMonitoring == "High temperature Sulfidic / Naphthenic acid corrosion - Corrosion coupons" or obj.OnlineMonitoring == "Sour water high velocity corrosion - Corrosion coupons" or obj.OnlineMonitoring == "Sour water high velocity corrosion - Electrical resistance probes" or
                    obj.OnlineMonitoring == "Sour water low velocity corrosion - Corrosion coupons" or obj.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion low velocity - Corrosion coupons"):
            Fom = 2
        elif (
                            obj.OnlineMonitoring == "Amine low velocity corrosion - Key process variable" or obj.OnlineMonitoring == "HCL corrosion - Key process variable & Electrical resistance probes" or obj.OnlineMonitoring == "Sour water low velocity corrosion - Key process variable" or obj.OnlineMonitoring == "Sulfuric acid (H2S/H2) corrosion high velocity - Key process parameters & electrical resistance probes" or obj.OnlineMonitoring == "Sulfuric acid(H2S / H2) corrosion low velocity - Key process parameters"):
            Fom = 20
        else:
            Fom = 1
        a =  (obj.DFB_THIN(age) * Fip * Fdl * Fwd * Fam * Fsm)/Fom
        # print("thing",a)
        # print("DFB_THIN",obj.DFB_THIN(age))
        # print("FIP",Fip)
        # print("Fdl",Fdl)
        # print("Fwd",Fwd)
        # print("Fam",Fam)
        # print("Fsm",Fsm)
        # print("obj.AdjustmentSettle",obj.AdjustmentSettle)
        return max(a,0.1)

    #Calculate Linning:
    def DFB_LINNING(obj, age):
        if (obj.INTERNAL_LINNING):
            if (obj.LinningType == "Organic - Low Quality"):
                SUSCEP_LINNING ="MoreThan6Years"
                return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            elif(obj.LinningType == "Organic - Medium Quality"):
                SUSCEP_LINNING ="WithinLast6Years"
                return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            elif(obj.LinningType == "Organic - High Quality"):
                SUSCEP_LINNING ="WithinLast3Years"
                return DAL_CAL.POSTGRESQL.GET_TBL_65(math.ceil(age), SUSCEP_LINNING)
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_64(math.ceil(age), obj.LinningType)
        # if (obj.LinningType == "Organic"):
        #     if (age <= 3):
        #         SUSCEP_LINNING = "WithinLast3Years"
        #     elif (age > 3 and age <= 6):
        #         SUSCEP_LINNING = "WithinLast6Years"
        #     else:
        #         SUSCEP_LINNING = "MoreThan6Years"
        #     #YEAR_IN_SERVICE = obj.GET_AGE_INSERVICE()
        #     return DAL_CAL.POSTGRESQL.GET_TBL_65(int(age), SUSCEP_LINNING)
        # else:
        #     return DAL_CAL.POSTGRESQL.GET_TBL_64(int(round(age)), obj.LinningType)

    def DF_LINNING(obj, age):
        if (obj.INTERNAL_LINNING):
            if (obj.LINNER_CONDITION == "Poor"):
                Fdl = 10
            elif (obj.LINNER_CONDITION == "Average"):
                Fdl = 2
            else:
                Fdl = 1

            if (obj.LINNER_ONLINE):
                Fom = 0.1
            else:
                Fom = 1
            return obj.DFB_LINNING(age) * Fdl * Fom
        else:
            return 0

    # Calculate Caustic:
    def getSusceptibility_Caustic(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
            # if obj.CRACK_PRESENT == "Cracks Removed":
            #     sus = "None"
        elif (obj.HEAT_TREATMENT == "Stress Relieved"):
            sus = "None"
        else:
            if (obj.plotinArea() == 'A'):
                if (obj.NaOHConcentration < 5):
                    if (obj.HEAT_TRACE):
                        sus = "Medium"
                    elif (obj.STEAM_OUT):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (obj.HEAT_TRACE):
                    sus = "High"
                elif (obj.STEAM_OUT):
                    sus = "Medium"
                else:
                    sus = "None"
            else:
                if (obj.NaOHConcentration < 5):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus
    def plotinArea(obj):
        TempBase = obj.interpolation(obj.NaOHConcentration)
        if (obj.MAX_OP_TEMP < TempBase):
            k = 'A'
        else:
            k = 'B'
        return k

    def interpolation(obj, t):
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

    def SVI_CAUSTIC(obj):
        if (obj.getSusceptibility_Caustic() == "High"):
            sev = 5000
        elif (obj.getSusceptibility_Caustic() == "Medium"):
            sev = 500
        elif (obj.getSusceptibility_Caustic() == "Low"):
            sev = 50
        else:
            sev = 0
        return sev

    def DF_CAUSTIC(obj, age):
        if (obj.CARBON_ALLOY and obj.NaOHConcentration != 0):
            obj.CAUSTIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[2])
            obj.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[2])
            if(age<1):
                return obj.SVI_CAUSTIC()
            elif(obj.CAUSTIC_INSP_EFF == "E" or obj.CAUSTIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.CAUSTIC_INSP_NUM) + obj.CAUSTIC_INSP_EFF
            DFB_CAUSTIC = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_CAUSTIC(), FIELD)
            return DFB_CAUSTIC * pow( max(age,1.0), 1.1)
        else:
            return 0

    # Calculate SCC AMINE:
    #co van de ve thuat toan. Can xem lai
    def getSusceptibility_Amine(obj):
        if(obj.AMINE_EXPOSED and obj.CARBON_ALLOY):
            if (obj.CRACK_PRESENT):
                sus = "High"
                # if obj.CRACK_PRESENT == "Cracks Removed":
                #     sus = "None"
            # elif (obj.HEAT_TREATMENT == "Stress Relieved"):
            #     sus = "None"
            else:
                if (
                        obj.AMINE_SOLUTION == "Methyldiethanolamine MDEA" or obj.AMINE_SOLUTION == "Disopropanolamine DIPA"):
                    if (obj.MAX_OP_TEMP > 82.22):
                        sus = "High"
                    elif ((obj.MAX_OP_TEMP > 37.78 and obj.MAX_OP_TEMP < 82.22) or obj.HEAT_TRACE or obj.STEAM_OUT):
                        sus = "Medium"
                    else:
                        sus = "Low"
                elif (obj.AMINE_SOLUTION == "Diethanolamine DEA"):
                    if (obj.MAX_OP_TEMP > 82.22):
                        sus = "Medium"
                    elif ((obj.MAX_OP_TEMP > 60 and obj.MAX_OP_TEMP < 82.22) or obj.HEAT_TRACE or obj.STEAM_OUT):
                        sus = "Low"
                    else:
                        sus = "None"
                else:
                    if (obj.MAX_OP_TEMP > 82.22 or obj.HEAT_TRACE or obj.STEAM_OUT):
                        sus = "Low"
                    else:
                        sus = "None"
            return sus

    def SVI_AMINE(obj):
        if (obj.getSusceptibility_Amine() == "High"):
            return 1000
        elif (obj.getSusceptibility_Amine() == "Medium"):
            return 100
        elif (obj.getSusceptibility_Amine() == "Low"):
            return 10
        else:
            return 0

    def DF_AMINE(obj, age):
        if (obj.CARBON_ALLOY):
            obj.AMINE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[3])
            obj.AMINE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[3])
            if (obj.AMINE_INSP_EFF == "E" or obj.AMINE_INSP_NUM == 0):
                FIELD = "E"
            elif(age>1):
                return obj.SVI_AMINE()
            else:
                FIELD = str(obj.AMINE_INSP_NUM) + obj.AMINE_INSP_EFF
            DFB_AMIN = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_AMINE(), FIELD)
            print(DFB_AMIN * pow(max(age,1.0),1.1))
            return DFB_AMIN * pow(max(age,1.0),1.1)
        else:
            return 0

    # Calculate Sulphide Stress Cracking
    def GET_ENVIRONMENTAL_SEVERITY(obj):
        if (obj.PH < 5.5):
            if  (obj.H2SContent < 50):
                env = "Low"
            elif (obj.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        elif (obj.PH <= 7.5 and obj.PH >= 5.5):
            if (obj.H2SContent > 10000):
                env = "Moderate"
            else:
                env = "Low"
        elif (obj.PH >= 7.6 and obj.PH <= 8.3):
            if (obj.H2SContent < 50):
                env = "Low"
            else:
                env = "Moderate"
        elif (obj.PH >= 8.4 and obj.PH <= 8.9):
            if (obj.H2SContent < 50):
                env = "Low"
            elif (obj.H2SContent <= 10000 and obj.PRESENT_CYANIDE):
                env = "High"
            elif (obj.H2SContent <= 10000):
                env = "Moderate"
            else:
                env = "High"
        else:
            if (obj.H2SContent < 50):
                env = "Low"
            elif (obj.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        return env

    def GET_SUSCEPTIBILITY_SULPHIDE(obj):
        env = obj.GET_ENVIRONMENTAL_SEVERITY()
        if (obj.CRACK_PRESENT):
            sus = "High"
            # if obj.CRACK_PRESENT == "Cracks Removed":
            #     sus = "None"
        elif (obj.PWHT):
            if (obj.BRINNEL_HARDNESS == "Below 200"):
                sus = "None"
            elif (obj.BRINNEL_HARDNESS == "Between 200 and 237"):
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
            if (obj.BRINNEL_HARDNESS == "Below 200"):
                sus = "Low"
            elif (obj.BRINNEL_HARDNESS == "Between 200 and 237"):
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

    def SVI_SULPHIDE(obj):
        if (obj.GET_SUSCEPTIBILITY_SULPHIDE() == "High"):
            return 100
        elif (obj.GET_SUSCEPTIBILITY_SULPHIDE() == "Medium"):
            return 10
        elif (obj.GET_SUSCEPTIBILITY_SULPHIDE() == "Low"):
            return 1
        else:
            return 0

    def DF_SULPHIDE(obj, age):
        if (obj.CARBON_ALLOY and obj.AQUEOUS_OPERATOR and obj.ENVIRONMENT_H2S_CONTENT):
            obj.SULPHIDE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[4])
            obj.SULPHIDE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber,obj.DM_Name[4])
            if(age<1):
                return obj.SVI_SULPHIDE()
            elif(obj.SULPHIDE_INSP_EFF == "E" or obj.SULPHIDE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.SULPHIDE_INSP_NUM) + obj.SULPHIDE_INSP_EFF
            DFB_SULPHIDE = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_SULPHIDE(), FIELD)
            return DFB_SULPHIDE * pow(max(age,1.0),1.1)
        else:
            return 0

    # Calculate HIC/SOHIC-H2S
    def GET_ENVIROMENTAL_HICSOHIC_H2S(obj):
        if (obj.PH < 5.5):
            if (obj.H2SContent < 50):
                env = "Low"
            elif (obj.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        elif (obj.PH >= 5.5 and obj.PH <= 7.5):
            if (obj.H2SContent > 10000):
                env = "Moderate"
            else:
                env = "Low"
        elif (obj.PH >= 7.6 and obj.PH <= 8.3):
            if (obj.H2SContent < 50):
                env = "Low"
            else:
                env = "Moderate"
        elif (obj.PH >= 8.4 and obj.PH <= 8.9):
            if (obj.H2SContent < 50):
                env = "Low"
            elif (obj.H2SContent <= 10000 and obj.PRESENT_CYANIDE):
                env = "High"
            elif (obj.H2SContent <= 10000):
                env = "Moderate"
            else:
                env = "High"
        else:
            if (obj.H2SContent < 50):
                env = "Low"
            elif (obj.H2SContent <= 1000):
                env = "Moderate"
            else:
                env = "High"
        return env

    def GET_SUSCEPTIBILITY_HICSOHIC_H2S(obj):
        env = obj.GET_ENVIROMENTAL_HICSOHIC_H2S()
        if (obj.CRACK_PRESENT):
            sus = "High"
        elif (obj.PWHT):
            if (obj.SULFUR_CONTENT == "High > 0.01%"):
                if (env == "High"):
                    sus = "High"
                elif (env == "Moderate"):
                    sus = "Medium"
                else:
                    sus = "Low"
            elif obj.SULFUR_CONTENT == "Low <= 0.01%":
                if (env == "High"):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                    sus = "Low"
        else:
            if (obj.SULFUR_CONTENT == "High > 0.01%"):
                if (env == "Low"):
                    sus = "Medium"
                else:
                    sus = "High"
            elif (obj.SULFUR_CONTENT == "Low <=0.01%"):
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

    def SVI_HICSOHIC_H2S(obj):
        if (obj.GET_SUSCEPTIBILITY_HICSOHIC_H2S() == "High"):
            return 100
        elif (obj.GET_SUSCEPTIBILITY_HICSOHIC_H2S() == "Medium"):
            return 10
        elif (obj.GET_ENVIROMENTAL_HICSOHIC_H2S() == "Low"):
            return 1
        else:
            return 0
    def FOM_HIC(obj):
        if obj.OnlineMonitoring == "Other corrosion - Key process variable and Hydrogen probes":
            return 4
        elif (obj.OnlineMonitoring == "Other corrosion - Key process variable" or obj.OnlineMonitoring=="Other corrosion - Hydrogen probes"):
            return 2
        else:
            return 1

    def DF_HICSOHIC_H2S(obj, age):
        if (obj.CARBON_ALLOY and obj.AQUEOUS_OPERATOR and obj.ENVIRONMENT_H2S_CONTENT):
            obj.SULFUR_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[5])
            obj.SULFUR_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[5])
            if(age<1):
                return obj.SVI_HICSOHIC_H2S()/obj.FOM_HIC()
            elif (obj.SULFUR_INSP_EFF == "E" or obj.SULFUR_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.SULPHIDE_INSP_NUM) + obj.SULFUR_INSP_NUM
            DFB_SULFUR = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_HICSOHIC_H2S(), FIELD)
            return (DFB_SULFUR * pow(max(age,1.0), 1.1))/obj.FOM_HIC()
        else:
            return 0

    # Calculate Cacbonate Cracking
    def GET_SUSCEPTIBILITY_CARBONATE(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
        elif (obj.PWHT):
            sus = "None"
        else:
            if (obj.CO3_CONTENT < 100):
                if (obj.PH < 7.5):
                    sus = "None"
                elif (obj.PH >= 9.0):
                    sus = "High"
                else:
                    sus = "Low"
            else:
                if (obj.PH < 7.5):
                    sus = "None"
                elif (7.5<= obj.PH < 8):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_CARBONATE(obj):
        if (obj.GET_SUSCEPTIBILITY_CARBONATE() == "High"):
            return 1000
        elif (obj.GET_SUSCEPTIBILITY_CARBONATE() == "Medium"):
            return 100
        elif (obj.GET_SUSCEPTIBILITY_CARBONATE() == "Low"):
            return 10
        else:
            return 0

    def DF_CACBONATE(obj, age):
        if (obj.CARBON_ALLOY and obj.AQUEOUS_OPERATOR and obj.PH >= 7.5):
            obj.CACBONATE_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[6])
            obj.CACBONATE_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[6])
            if(age<1):
                return obj.SVI_CARBONATE()
            elif (obj.CACBONATE_INSP_EFF == "E" or obj.CACBONATE_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.CACBONATE_INSP_NUM) + obj.CACBONATE_INSP_EFF
            DFB_CACBONATE = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_CARBONATE(), FIELD)
            return DFB_CACBONATE * pow(max(age, 1.0), 1.1)
        else:
            return 0
    # Calculate PTA Cracking
    def GET_SUSCEPTIBILITY_PTA(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
            return sus
        if (not obj.ExposedSH2OOperation and not obj.ExposedSH2OShutdown):
            sus = "None"
        else:
            if (obj.MAX_OP_TEMP < 427):
                if (obj.ThermalHistory == "Solution Annealed"):
                    if (obj.PTAMaterial == "Regular 300 series Stainless Steels and Alloys 600 and 800"):
                        sus = "Medium"
                    elif (obj.PTAMaterial == "H Grade 300 series Stainless Steels"):
                        sus = "High"
                    elif (obj.PTAMaterial == "L Grade 300 series Stainless Steels"):
                        sus = "Low"
                    elif (obj.PTAMaterial == "321 Stainless Steel"):
                        sus = "Medium"
                    elif (obj.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (obj.ThermalHistory == "Stabilised Before Welding"):
                    if (obj.PTAMaterial == "321 Stainless Steel"):
                        sus = "Medium"
                    elif (obj.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (obj.ThermalHistory == "Stabilised After Welding"):
                    if (obj.PTAMaterial == "321 Stainless Steel"):
                        sus = "Low"
                    elif (obj.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                else:
                    sus = "None"
            else:
                if (obj.ThermalHistory == "Solution Annealed"):
                    if (obj.PTAMaterial == "Regular 300 series Stainless Steels and Alloys 600 and 800"):
                        sus = "High"
                    elif (obj.PTAMaterial == "H Grade 300 series Stainless Steels"):
                        sus = "High"
                    elif (obj.PTAMaterial == "L Grade 300 series Stainless Steels"):
                        sus = "Medium"
                    elif (obj.PTAMaterial == "321 Stainless Steel"):
                        sus = "High"
                    elif (obj.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Medium"
                    else:
                        sus = "None"
                elif (obj.ThermalHistory == "Stabilised Before Welding"):
                    if (obj.PTAMaterial == "321 Stainless Steel"):
                        sus = "High"
                    elif (obj.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                elif (obj.ThermalHistory == "Stabilised After Welding"):
                    if (obj.PTAMaterial == "321 Stainless Steel"):
                        sus = "Low"
                    elif (obj.PTAMaterial == "347 Stainless Steel, Alloy 20, Alloy 625, All austenitic weld overlay"):
                        sus = "Low"
                    else:
                        sus = "None"
                else:
                    sus = "None"
        if (obj.DOWNTIME_PROTECTED):
            if (sus == "High"):
                sus = "Medium"
            elif (sus == "Medium"):
                sus = "Low"
            else:
                sus = "None"
        return sus

    def SVI_PTA(obj):
        if (obj.GET_SUSCEPTIBILITY_PTA() == "High"):
            return 5000
        elif (obj.GET_SUSCEPTIBILITY_PTA() == "Medium"):
            return 500
        elif (obj.GET_SUSCEPTIBILITY_PTA() == "Low"):
            return 50
        else:
            return 1

    def DF_PTA(obj, age):
        if (obj.PTA_SUSCEP or ((obj.CARBON_ALLOY or obj.NICKEL_ALLOY) and obj.EXPOSED_SULFUR)):
            obj.PTA_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[7])
            obj.PTA_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[7])
            if(age<1):
                return obj.SVI_PTA()
            elif (obj.PTA_INSP_EFF == "E" or obj.PTA_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.PTA_INSP_NUM) + obj.PTA_INSP_EFF
            DFB_PTA = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_PTA(), FIELD)
            return DFB_PTA * pow(age, 1.1)
        else:
            return 0

    # Calculate CLSCC
    def GET_SUSCEPTIBILITY_CLSCC(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
            return sus
        if (obj.PH <= 10):
            if (obj.MAX_OP_TEMP <=38):
                if(obj.CHLORIDE_ION_CONTENT > 1000):
                    sus = "Medium"
                else:
                    sus = "High"
            elif(obj.MAX_OP_TEMP > 38 and obj.MAX_OP_TEMP <= 66):
                if(obj.CHLORIDE_ION_CONTENT>=1 and obj.CHLORIDE_ION_CONTENT<=10):
                    sus = "Low"
                elif(obj.CHLORIDE_ION_CONTENT>1000):
                    sus = "High"
                else:
                    sus = "Medium"
            elif(obj.MAX_OP_TEMP > 66 and obj.MAX_OP_TEMP <= 93):
                if (obj.CHLORIDE_ION_CONTENT >= 1 and obj.CHLORIDE_ION_CONTENT <= 100):
                    sus = "Medium"
                else:
                    sus = "High"
            elif (obj.MAX_OP_TEMP > 93 and obj.MAX_OP_TEMP <= 149):
                if (obj.CHLORIDE_ION_CONTENT >= 11 and obj.CHLORIDE_ION_CONTENT <= 1000):
                    sus = "High"
                else:
                    sus = "Medium"
            else:
                sus = "High"
        else:
            if (obj.MAX_OP_TEMP <=38):
                sus = "None"
            elif(obj.MAX_OP_TEMP > 38 and obj.MAX_OP_TEMP <= 93):
                sus = "Low"
            elif(obj.MAX_OP_TEMP > 93 and obj.MAX_OP_TEMP <= 149):
                if (obj.CHLORIDE_ION_CONTENT >1000):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                if (obj.CHLORIDE_ION_CONTENT >= 1 and obj.CHLORIDE_ION_CONTENT <= 100):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_CLSCC(obj):
        if (obj.GET_SUSCEPTIBILITY_CLSCC() == "High"):
            return 5000
        elif (obj.GET_SUSCEPTIBILITY_CLSCC() == "Medium"):
            return 500
        elif (obj.GET_SUSCEPTIBILITY_CLSCC() == "Low"):
            return 50
        else:
            return 0

    def DF_CLSCC(obj, age):
        if (obj.INTERNAL_EXPOSED_FLUID_MIST and obj.AUSTENITIC_STEEL and obj.MAX_OP_TEMP > 38):
            obj.CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[8])
            obj.CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[8])
            if(age<1):
                return obj.SVI_CLSCC()
            if (obj.CLSCC_INSP_EFF == "E" or obj.CLSCC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.CLSCC_INSP_NUM) + obj.CLSCC_INSP_EFF
            DFB_CLSCC = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_CLSCC(), FIELD)
            return DFB_CLSCC * pow(age, 1.1)
        else:
            return 0

    # Calculate HSC-HF
    def GET_SUSCEPTIBILITY_HSCHF(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
            return sus
        if (not obj.HF_PRESENT or not obj.CARBON_ALLOY):
            sus = "None"
        else:
            if (obj.PWHT):
                if (obj.BRINNEL_HARDNESS == "Below 200"):
                    sus = "None"
                elif (obj.BRINNEL_HARDNESS == "Between 200 and 237"):
                    sus = "Low"
                else:
                    sus = "High"
            else:
                if (obj.BRINNEL_HARDNESS == "Below 200"):
                    sus = "Low"
                elif (obj.BRINNEL_HARDNESS == "Between 200 and 237"):
                    sus = "Medium"
                else:
                    sus = "High"
        return sus

    def SVI_HSCHF(obj):
        if (obj.GET_SUSCEPTIBILITY_HSCHF() == "High"):
            return 100
        elif (obj.GET_SUSCEPTIBILITY_HSCHF() == "Medium"):
            return 10
        else:
            return 0

    def DF_HSCHF(obj, age):
        if (obj.CARBON_ALLOY and obj.HF_PRESENT):
            obj.HSC_HF_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[9])
            obj.HSC_HF_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[9])
            if(age<1):
                return obj.SVI_HSCHF()
            if (obj.HSC_HF_INSP_EFF == "E" or obj.HSC_HF_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.HSC_HF_INSP_NUM) + obj.HSC_HF_INSP_EFF
            DFB_HSCHF = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_HSCHF(), FIELD)
            return DFB_HSCHF * pow(age, 1.1)
        else:
            return 0

    # Calculate HICSOHIC-HF
    def GET_SUSCEPTIBILITY_HICSOHIC_HF(obj):
        if (obj.CRACK_PRESENT):
            return "High"
        if (not obj.HF_PRESENT or not obj.CARBON_ALLOY):
            return "None"
        if (obj.PWHT):
            if (obj.SULFUR_CONTENT == "High > 0.01%"):
                sus = "High"
            elif (obj.SULFUR_CONTENT == "Low 0.002 - 0.01%"):
                sus = "Medium"
            else:
                sus = "Low"
        else:
            if (obj.SULFUR_CONTENT == "High > 0.01%" or obj.SULFUR_CONTENT == "Low 0.002 - 0.01%"):
                sus = "High"
            else:
                sus = "Medium"
        return sus

    def SVI_HICSOHIC_HF(obj):
        if (obj.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "High"):
            return 100
        elif (obj.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "Medium"):
            return 10
        elif (obj.GET_SUSCEPTIBILITY_HICSOHIC_HF() == "Low"):
            return 1
        else:
            return 0

    def DF_HIC_SOHIC_HF(obj, age):
        if (obj.CARBON_ALLOY and obj.HF_PRESENT):
            obj.HICSOHIC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[10])
            obj.HICSOHIC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[10])
            if(age<1):
                return obj.SVI_HICSOHIC_HF()/obj.FOM_HIC()
            if (obj.HICSOHIC_INSP_EFF == "E" or obj.HICSOHIC_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.HICSOHIC_INSP_NUM) + obj.HICSOHIC_INSP_EFF
            DFB_HICSOHIC_HF = DAL_CAL.POSTGRESQL.GET_TBL_74(obj.SVI_HICSOHIC_HF(), FIELD)
            return DFB_HICSOHIC_HF * pow(age, 1.1)/obj.FOM_HIC()
        else:
            return 0


    # Calculate EXTERNAL CORROSION
    def AGE_CLSCC(obj):
        try:
            TICK_SPAN = abs((obj.AssesmentDate.date() - obj.COMPONENT_INSTALL_DATE.date()).days)
            return TICK_SPAN / 365
        except Exception as e:
            print(e)
        # if (obj.EXTERN_COAT_QUALITY == "High coating quality"):
        #     AGE_COAT = obj.COMPONENT_INSTALL_DATE + relativedelta(years=+15)  # Age + 15
        # elif (obj.EXTERN_COAT_QUALITY == "Medium coating quality"):
        #     AGE_COAT = obj.COMPONENT_INSTALL_DATE + relativedelta(years=+5)  # Age + 5
        # else:
        #     AGE_COAT = obj.COMPONENT_INSTALL_DATE
        # TICK_SPAN = abs((obj.AssesmentDate.date() - AGE_COAT.date()).days)
        #TICK_SPAN = abs((obj.AssesmentDate.date()-obj.COMPONENT_INSTALL_DATE.date()).days)
        #return TICK_SPAN / 365

    def AGE_CUI(obj, age):#section 15.6.3: Step 5-6-7
        try:
            a=float(obj.AGE_CLSCC())
            if (obj.agetk(age) >= a):
                if (obj.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a)
                elif (obj.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a)
                else:
                    COAT = 0
            else:
                if (obj.EXTERN_COAT_QUALITY == "High coating quality"):
                    COAT = min(15, a) - min(15, a - obj.agetk(age))
                elif (obj.EXTERN_COAT_QUALITY == "Medium coating quality"):
                    COAT = min(5, a) - min(5, a - obj.agetk(age))
                else:
                    COAT = 0
            a=obj.agetk(age) - COAT
            return a
        except Exception as e:
            print(e)

    def API_EXTERNAL_CORROSION_RATE(obj):
        if (obj.EXTERNAL_EVIRONMENT == "Arid/dry"):
            CR_EXTERN = (obj.CUI_PERCENT_3+obj.CUI_PERCENT_4+obj.CUI_PERCENT_5)*0.025/100
        elif(obj.EXTERNAL_EVIRONMENT=="Marine"):
            CR_EXTERN =(obj.CUI_PERCENT_2*0.025+obj.CUI_PERCENT_3*0.127+obj.CUI_PERCENT_4*0.127+obj.CUI_PERCENT_5*0.127+obj.CUI_PERCENT_6*0.025)/100
        elif (obj.EXTERNAL_EVIRONMENT == "Severe"):
            CR_EXTERN = (obj.CUI_PERCENT_3*0.254+obj.CUI_PERCENT_4*0.254+obj.CUI_PERCENT_5*0.254+obj.CUI_PERCENT_6*0.051)/100
        else:
            CR_EXTERN = (obj.CUI_PERCENT_3*0.076+obj.CUI_PERCENT_4*0.076+obj.CUI_PERCENT_5*0.051)/100

        return CR_EXTERN

    def API_ART_EXTERNAL(obj, age):
        if (obj.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1
        if (obj.INTERFACE_SOIL_WATER): # cần kiểm tra lại điều kiện, hiện tại trong tinh toán FIP luôn =1
            FIP = 1
        else:
            FIP = 1
        CR = obj.API_EXTERNAL_CORROSION_RATE() * max(FPS, FIP)

        try:
            ART_EXT = (CR*obj.AGE_CUI(age))/obj.trdi()
        except Exception as e:
            print(e)
            ART_EXT = 1
        return ART_EXT

    def DF_EXTERNAL_CORROSION(obj, age):
        if (obj.EXTERNAL_EXPOSED_FLUID_MIST or (
        obj.CARBON_ALLOY and not (obj.MAX_OP_TEMP < -23 or obj.MIN_OP_TEMP > 121))):
            obj.EXTERNAL_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[11])
            obj.EXTERNAL_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[11])
            obj.NoINSP_EXTERNAL = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[11])
        if (obj.EXTERNAL_INSP_EFF == "" or obj.EXTERNAL_INSP_NUM == 0):
            obj.EXTERNAL_INSP_EFF = "E"
        if (obj.APIComponentType == "TANKBOTTOM0" or obj.APIComponentType == "TANKROOFFLOAT0"):
            if (obj.NomalThick == 0 or obj.CurrentThick == 0 or obj.WeldJointEffciency == 0 or(
             obj.YieldStrengthDesignTemp == 0 and obj.TensileStrengthDesignTemp == 0) or obj.EXTERN_COAT_QUALITY == "" or (bool(obj.COMPONENT_INSTALL_DATE) == False)):
                return 6500;
                # return 1390
            else:
                return DAL_CAL.POSTGRESQL.GET_TBL_512(obj.API_ART(obj.API_ART_EXTERNAL(age)), obj.EXTERNAL_INSP_NUM,
                                                     obj.EXTERNAL_INSP_EFF)
        else:
            if (obj.NomalThick == 0 or obj.CurrentThick == 0 or obj.WeldJointEffciency== 0 or
            (obj.YieldStrengthDesignTemp == 0 and obj.TensileStrengthDesignTemp == 0) or obj.EXTERN_COAT_QUALITY == "" or (bool(obj.COMPONENT_INSTALL_DATE) == False)):
                return 6500;
            elif(obj.APIComponentType =="TANKBOTTOM" and obj.ShapeFactor==0.0 and obj.MINIUM_STRUCTURAL_THICKNESS_GOVERS==False):#bổ sung trường hợp
                return 6500
            else:
                try:
                    a = obj.Po_P1_EXTERNAL() * obj.ncdf(- obj.B1_EXTERNAL(age))
                    b = obj.Po_P2_EXTERNAL() * obj.ncdf(- obj.B2_EXTERNAL(age))
                    c = obj.Pr_P3_EXTERNAL() * obj.ncdf(- obj.B3_EXTERNAL(age))
                    return (a + b + c) / (1.56 * pow(10, -4))
                except Exception as e:
                    print(e)
                    return 0
        # else:
        #     return 0
    def Pr_P1_EXTERNAL(obj):
        if obj.CR_Confidents_Level == "Low":
            return 0.5
        elif obj.CR_Confidents_Level == "Medium":
            return 0.7
        else:
            return 0.8
    def Pr_P2_EXTERNAL(obj):
        if obj.CR_Confidents_Level == "Low":
            return 0.3
        elif obj.CR_Confidents_Level == "Medium":
            return 0.2
        else:
            return 0.15
    def Pr_P3_EXTERNAL(obj):
        if obj.CR_Confidents_Level == "Low":
            return 0.2
        elif obj.CR_Confidents_Level == "Medium":
            return 0.1
        else:
            return  0.05

    def NA_EXTERNAL(obj):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(obj.ComponentNumber, obj.DM_Name[11])

        return a
    def NB_EXTERNAL(obj):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(obj.ComponentNumber, obj.DM_Name[11])

        return b
    def NC_EXTERNAL(obj):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(obj.ComponentNumber, obj.DM_Name[11])
        return c
    def ND_EXTERNAL(obj):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(obj.ComponentNumber, obj.DM_Name[11])
        return d
    def I1_EXTERNAL(obj):
        a=obj.Pr_P1_EXTERNAL() * pow(0.9,obj.NA_EXTERNAL()) * pow(0.7,obj.NB_EXTERNAL()) * pow(0.5,obj.NC_EXTERNAL()) * pow(0.4,obj.ND_EXTERNAL())
        return obj.Pr_P1_EXTERNAL() * pow(0.9,obj.NA_EXTERNAL()) * pow(0.7,obj.NB_EXTERNAL()) * pow(0.5,obj.NC_EXTERNAL()) * pow(0.4,obj.ND_EXTERNAL())
    def I2_EXTERNAL(obj):
        a=obj.Pr_P2_EXTERNAL() * pow(0.09,obj.NA_EXTERNAL()) * pow(0.2,obj.NB_EXTERNAL()) * pow(0.3,obj.NC_EXTERNAL()) * pow(0.33,obj.ND_EXTERNAL())
        return obj.Pr_P2_EXTERNAL() * pow(0.09,obj.NA_EXTERNAL()) * pow(0.2,obj.NB_EXTERNAL()) * pow(0.3,obj.NC_EXTERNAL()) * pow(0.33,obj.ND_EXTERNAL())

    def I3_EXTERNAL(obj):
        a = obj.Pr_P3_EXTERNAL() * pow(0.01, obj.NA_EXTERNAL()) * pow(0.1, obj.NB_EXTERNAL()) * pow(0.2,
                                                                                                       obj.NC_EXTERNAL()) * pow(
            0.27, obj.ND_EXTERNAL())
        return obj.Pr_P3_EXTERNAL() * pow(0.01, obj.NA_EXTERNAL()) * pow(0.1, obj.NB_EXTERNAL()) * pow(0.2,
                                                                                                          obj.NC_EXTERNAL()) * pow(
            0.27, obj.ND_EXTERNAL())
    def Po_P1_EXTERNAL(obj):
        a=obj.I1_EXTERNAL()/(obj.I1_EXTERNAL() + obj.I2_EXTERNAL() + obj.I3_EXTERNAL())
        return obj.I1_EXTERNAL()/(obj.I1_EXTERNAL() + obj.I2_EXTERNAL() + obj.I3_EXTERNAL())
    def Po_P2_EXTERNAL(obj):
        a = obj.I2_EXTERNAL()/(obj.I1_EXTERNAL() + obj.I2_EXTERNAL() + obj.I3_EXTERNAL())
        return obj.I2_EXTERNAL()/(obj.I1_EXTERNAL() + obj.I2_EXTERNAL() + obj.I3_EXTERNAL())
    def Po_P3_EXTERNAL(obj):
        a=obj.I3_EXTERNAL()/(obj.I1_EXTERNAL() + obj.I2_EXTERNAL() + obj.I3_EXTERNAL())
        return obj.I3_EXTERNAL()/(obj.I1_EXTERNAL() + obj.I2_EXTERNAL() + obj.I3_EXTERNAL())
    def B1_EXTERNAL(obj,age):
        return (1 - obj.API_ART_EXTERNAL(age)- obj.SRp_Thin())/math.sqrt(pow(obj.API_ART_EXTERNAL(age), 2) * 0.04 + pow((1 - obj.API_ART_EXTERNAL(age)), 2) * 0.04 + pow(obj.SRp_Thin(), 2) * pow(0.05, 2))
    def B2_EXTERNAL(obj,age):
        return (1- 2*obj.API_ART_EXTERNAL(age)-obj.SRp_Thin())/math.sqrt(pow(obj.API_ART_EXTERNAL(age),2)*4*0.04 + pow(1-2*obj.API_ART_EXTERNAL(age),2)*0.04+pow(obj.SRp_Thin(),2)*pow(0.05,2))
    def B3_EXTERNAL(obj,age):
        return (1- 4*obj.API_ART_EXTERNAL(age)-obj.SRp_Thin())/math.sqrt(pow(obj.API_ART_EXTERNAL(age),2)*16*0.04 + pow(1-4*obj.API_ART_EXTERNAL(age),2)*0.04+pow(obj.SRp_Thin(),2)*pow(0.05,2)) 

    def API_CORROSION_RATE(obj):
        if (obj.EXTERNAL_EVIRONMENT == "Arid/dry"):
            CR_CUI = (obj.CUI_PERCENT_3*0.025+obj.CUI_PERCENT_4*0.025+obj.CUI_PERCENT_5*0.051+obj.CUI_PERCENT_6*0.025)/100
        elif(obj.EXTERNAL_EVIRONMENT=="Marine"):
            CR_CUI = (obj.CUI_PERCENT_2 * 0.025 + obj.CUI_PERCENT_3 * 0.127 + obj.CUI_PERCENT_4 * 0.127 + obj.CUI_PERCENT_5 * 0.254 + obj.CUI_PERCENT_6 * 0.127 + obj.CUI_PERCENT_7 * 0.051 + obj.CUI_PERCENT_8 * 0.051+obj.CUI_PERCENT_9 * 0.025) / 100
        elif (obj.EXTERNAL_EVIRONMENT == "Severe"):
            CR_CUI =(obj.CUI_PERCENT_2*0.076+obj.CUI_PERCENT_3*0.254+obj.CUI_PERCENT_4*0.254+obj.CUI_PERCENT_5*0.508+obj.CUI_PERCENT_6*0.254+obj.CUI_PERCENT_7*0.254+obj.CUI_PERCENT_8*0.254+obj.CUI_PERCENT_9 * 0.127)/100
        else:
            CR_CUI = (obj.CUI_PERCENT_3*0.076+obj.CUI_PERCENT_4*0.076+obj.CUI_PERCENT_5*0.127+obj.CUI_PERCENT_6*0.025+obj.CUI_PERCENT_7*0.025)/100
        return CR_CUI

    def API_ART_CUI(obj, age):
        if (obj.INSULATION_TYPE == "Asbestos" or obj.INSULATION_TYPE == "Calcium Silicate" or obj.INSULATION_TYPE == "Mineral Wool" or obj.INSULATION_TYPE == "Fibreglass"or obj.INSULATION_TYPE == "Unknown/Unspecified"):
            FIN = 1.25
        elif (obj.INSULATION_TYPE == "Foam Glass"):
            FIN = 0.75
        else:
            FIN = 1

        if (obj.PIPING_COMPLEXITY == "Below average"):
            FCM = 0.75
        elif (obj.PIPING_COMPLEXITY == "Above average"):
            FCM = 1.75
        else:
            FCM = 1

        if (obj.INSULATION_CONDITION == "Below average"):
            FIC = 1.25
        elif (obj.INSULATION_CONDITION == "Above average"):
            FIC = 0.75
        else:
            FIC = 1

        if (obj.SUPPORT_COATING):
            FPS = 2
        else:
            FPS = 1

        if (obj.INTERFACE_SOIL_WATER):
            FIP = 2
        else:
            FIP = 1

        CR = obj.API_CORROSION_RATE() * FIN * FCM * FIC * max(FPS, FIP)
        try:
            #ART_CUI = max(1 - (obj.CurrentThick - CR * obj.AGE_CUI(age)) / (obj.getTmin() + obj.CA), 0)
            ART_CUI = (CR * obj.AGE_CUI(age)) / obj.trdi()
        except:
            ART_CUI = 1
        return obj.API_ART(ART_CUI)

    def NA_FERRITIC(obj):
        a = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EFFA(obj.ComponentNumber, obj.DM_Name[12])
        return a

    def NB_FERRITIC(obj):
        b = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFB(obj.ComponentNumber, obj.DM_Name[12])
        return b

    def NC_FERRITIC(obj):
        c = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFC(obj.ComponentNumber, obj.DM_Name[12])
        return c

    def ND_FERRITIC(obj):
        d = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP_FOR_THIN_EEFD(obj.ComponentNumber, obj.DM_Name[12])
        return d

    def I1_FERRITIC(obj):
        a = obj.Pr_P1_EXTERNAL() * pow(0.9, obj.NA_FERRITIC()) * pow(0.7, obj.NB_FERRITIC()) * pow(0.5,obj.NC_FERRITIC()) * pow(0.4, obj.ND_FERRITIC())
        return obj.Pr_P1_EXTERNAL() * pow(0.9, obj.NA_FERRITIC()) * pow(0.7, obj.NB_FERRITIC()) * pow(0.5,obj.NC_FERRITIC()) * pow(0.4, obj.ND_FERRITIC())

    def I2_FERRITIC(obj):
        a = obj.Pr_P2_EXTERNAL() * pow(0.09, obj.NA_FERRITIC()) * pow(0.2, obj.NB_FERRITIC()) * pow(0.3,obj.NC_FERRITIC()) * pow(0.33, obj.ND_FERRITIC())
        return obj.Pr_P2_EXTERNAL() * pow(0.09, obj.NA_FERRITIC()) * pow(0.2, obj.NB_FERRITIC()) * pow(0.3,obj.NC_FERRITIC()) * pow(0.33, obj.ND_FERRITIC())

    def I3_FERRITIC(obj):
        a = obj.Pr_P3_EXTERNAL() * pow(0.01, obj.NA_FERRITIC()) * pow(0.1, obj.NB_FERRITIC()) * pow(0.2,obj.NC_FERRITIC()) * pow(0.27, obj.ND_FERRITIC())
        return obj.Pr_P3_EXTERNAL() * pow(0.01, obj.NA_FERRITIC()) * pow(0.1, obj.NB_FERRITIC()) * pow(0.2,obj.NC_FERRITIC()) * pow(0.27, obj.ND_FERRITIC())

    def Po_P1_FERRITIC(obj):
        return obj.I1_FERRITIC() / (obj.I1_FERRITIC() + obj.I2_FERRITIC() + obj.I3_FERRITIC())

    def Po_P2_FERRITIC(obj):
        return obj.I2_FERRITIC() / (obj.I1_FERRITIC() + obj.I2_FERRITIC() + obj.I3_FERRITIC())

    def Po_P3_FERRITIC(obj):
        return obj.I3_FERRITIC() / (obj.I1_FERRITIC() + obj.I2_FERRITIC() + obj.I3_FERRITIC())

    def B1_FERRITIC(obj, age):
        a=(1 - obj.API_ART_CUI(age) - obj.SRp_Thin()) / math.sqrt(
            pow(obj.API_ART_CUI(age), 2) * 0.04 + pow((1 - obj.API_ART_CUI(age)), 2) * 0.04 + pow(obj.SRp_Thin(),
                                                                                                    2) * pow(0.05, 2))
        return (1 - obj.API_ART_CUI(age) - obj.SRp_Thin()) / math.sqrt(
            pow(obj.API_ART_CUI(age), 2) * 0.04 + pow((1 - obj.API_ART_CUI(age)), 2) * 0.04 + pow(obj.SRp_Thin(),
                                                                                                    2) * pow(0.05, 2))

    def B2_FERRITIC(obj, age):
        b=(1 - 2 * obj.API_ART_CUI(age) - obj.SRp_Thin()) / math.sqrt(
            pow(obj.API_ART_CUI(age), 2) * 4 * 0.04 + pow(1 - 2 * obj.API_ART_CUI(age), 2) * 0.04 + pow(
                obj.SRp_Thin(), 2) * pow(0.05, 2))
        return (1 - 2 * obj.API_ART_CUI(age) - obj.SRp_Thin()) / math.sqrt(
            pow(obj.API_ART_CUI(age), 2) * 4 * 0.04 + pow(1 - 2 * obj.API_ART_CUI(age), 2) * 0.04 + pow(
                obj.SRp_Thin(), 2) * pow(0.05, 2))

    def B3_FERRITIC(obj, age):
        c=(1 - 4 * obj.API_ART_CUI(age) - obj.SRp_Thin()) / math.sqrt(
            pow(obj.API_ART_CUI(age), 2) * 16 * 0.04 + pow(1 - 4 * obj.API_ART_CUI(age), 2) * 0.04 + pow(
                obj.SRp_Thin(), 2) * pow(0.05, 2))
        return (1 - 4 * obj.API_ART_CUI(age) - obj.SRp_Thin()) / math.sqrt(
            pow(obj.API_ART_CUI(age), 2) * 16 * 0.04 + pow(1 - 4 * obj.API_ART_CUI(age), 2) * 0.04 + pow(
                obj.SRp_Thin(), 2) * pow(0.05, 2))

    def DF_CUI(obj, age):
        if (obj.EXTERNAL_EXPOSED_FLUID_MIST or (
                    obj.CARBON_ALLOY and not (obj.MAX_OP_TEMP < -12 or obj.MIN_OP_TEMP > 177))):
            obj.CUI_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[12])
            obj.CUI_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[12])
            if (obj.CUI_INSP_EFF == "" or obj.CUI_INSP_NUM == 0):
                obj.CUI_INSP_EFF = "E"
            if (obj.APIComponentType == "TANKBOTTOM0" or obj.APIComponentType == "TANKROOFFLOAT0"):
                if (obj.NomalThick == 0 or obj.CurrentThick == 0):
                    return 1390
                else:
                    return DAL_CAL.POSTGRESQL.GET_TBL_512(obj.API_ART(obj.API_ART_CUI(age)),obj.CUI_INSP_NUM,obj.CUI_INSP_EFF)
            else:
                if (obj.NomalThick == 0 or obj.CurrentThick == 0):
                    return 1900
                else:
                    try:
                        a = obj.Po_P1_FERRITIC() * obj.ncdf(- obj.B1_FERRITIC(age))
                        b = obj.Po_P2_FERRITIC() * obj.ncdf(- obj.B2_FERRITIC(age))
                        c = obj.Po_P3_FERRITIC() * obj.ncdf(- obj.B3_FERRITIC(age))
                        s=(a + b + c) / (1.56 * pow(10, -4))
                        return (a + b + c) / (1.56 * pow(10, -4))
                    except Exception as e:
                        print(e)
                        return 0
        else:
            return 0

    # cal EXTERNAL CLSCC
    def CLSCC_SUSCEP(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
        else:
            if (obj.EXTERNAL_EVIRONMENT == "Arid/dry"):
                sus = "Not"
            elif (obj.EXTERNAL_EVIRONMENT == "Marine"):
                if (obj.MAX_OP_TEMP < 49 or obj.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (obj.MAX_OP_TEMP >= 49 and obj.MAX_OP_TEMP < 93):
                    sus = "Medium"
                else:
                    sus = "Low"
            elif (obj.EXTERNAL_EVIRONMENT == "Severe"):
                if (obj.MAX_OP_TEMP < 49 or obj.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (obj.MAX_OP_TEMP >= 49 and obj.MAX_OP_TEMP < 93):
                    sus = "High"
                else:
                    sus = "Medium"
            elif (obj.EXTERNAL_EVIRONMENT == "Temperate"):
                if (obj.MAX_OP_TEMP < 49 or obj.MAX_OP_TEMP > 149):
                    sus = "Not"
                else:
                    sus = "Low"
            else:
                sus = "Not"
        return sus

    def DFB_EXTERN_CLSCC(obj):
        sus = obj.CLSCC_SUSCEP()
        if (sus == "High"):
            SVI = 50
        elif (sus == "Medium"):
            SVI = 10
        elif(sus == "Low"):
            SVI = 1
        else:
            SVI=0
        obj.EXTERN_CLSCC_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[13])
        obj.EXTERN_CLSCC_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[13])
        if (obj.EXTERN_CLSCC_INSP_EFF == "E" or obj.EXTERN_CLSCC_INSP_NUM == 0):
            FIELD = "E"
        else:
            FIELD = str(obj.EXTERN_CLSCC_INSP_NUM) + obj.EXTERN_CLSCC_INSP_EFF
        return DAL_CAL.POSTGRESQL.GET_TBL_74(SVI, FIELD)

    def DF_EXTERN_CLSCC(obj, age):
        if (obj.AUSTENITIC_STEEL and obj.EXTERNAL_EXPOSED_FLUID_MIST and not (
                obj.MAX_OP_TEMP < 49 or obj.MIN_DESIGN_TEMP > 149)):
            if(age<1):
                return obj.DFB_EXTERN_CLSCC()
            else:
                return obj.DFB_EXTERN_CLSCC() * pow(obj.AGE_CUI(age), 1.1)
        else:
            return 0

    # Calculate EXTERN CUI CLSCC
    def CUI_CLSCC_SUSCEP(obj):
        if (obj.CRACK_PRESENT):
            sus = "High"
        else:
            if (obj.EXTERNAL_EVIRONMENT == "Arid/dry"):
                if (obj.MAX_OP_TEMP >= 49 and obj.MAX_OP_TEMP < 93):
                    sus = "Low"
                else:
                    sus = "Not"
            elif (obj.EXTERNAL_EVIRONMENT == "Marine"):
                if (obj.MAX_OP_TEMP < 49 or obj.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (obj.MAX_OP_TEMP >= 49 and obj.MAX_OP_TEMP < 93):
                    sus = "High"
                else:
                    sus = "Medium"
            elif (obj.EXTERNAL_EVIRONMENT == "Severe"):
                if (obj.MAX_OP_TEMP < 49 or obj.MAX_OP_TEMP > 149):
                    sus = "Not"
                else:
                    sus = "High"
            elif (obj.EXTERNAL_EVIRONMENT == "Temperate"):
                if (obj.MAX_OP_TEMP < 49 or obj.MAX_OP_TEMP > 149):
                    sus = "Not"
                elif (obj.MAX_OP_TEMP >= 49 and obj.MAX_OP_TEMP < 93):
                    sus = "Medium"
                else:
                    sus = "Low"
            else:
                sus = "Not"
        return sus

    def ADJUST_COMPLEXITY(obj):
        SCP = obj.CUI_CLSCC_SUSCEP()
        if (SCP == "High"):
            if (obj.PIPING_COMPLEXITY == "Below average"):
                SCP = "Medium"
            else:
                SCP = "High"
        elif (SCP == "Medium"):
            if (obj.PIPING_COMPLEXITY == "Below average"):
                SCP = "Low"
            elif (obj.PIPING_COMPLEXITY == "Above average"):
                SCP = "High"
            else:
                SCP = "Medium"
        else:
            if (obj.PIPING_COMPLEXITY == "Above average"):
                SCP = "Medium"
            else:
                SCP = "Low"
        return SCP

    def ADJUST_ISULATION(obj):
        SCP = obj.ADJUST_COMPLEXITY()
        if (SCP == "High"):
            if (obj.INSULATION_CONDITION == "Above average"):
                SCP = "Medium"
            else:
                SCP = "High"
        elif (SCP == "Medium"):
            if (obj.INSULATION_CONDITION == "Above average"):
                SCP = "Low"
            elif (obj.INSULATION_CONDITION == "Below average"):
                SCP = "High"
            else:
                SCP = "Medium"
        else:
            if (obj.INSULATION_CONDITION == "Below average"):
                SCP = "Medium"
            else:
                SCP = "Low"
        return SCP

    def ADJUST_CHLORIDE_INSULATION(obj):
        SCP = obj.ADJUST_ISULATION()
        if (obj.INSULATION_CHLORIDE):
            if (SCP == "High"):
                SCP = "Medium"
            elif (SCP == "Medium"):
                SCP = "Low"
            else:
                SCP = "Low"
        else:
            SCP = obj.ADJUST_ISULATION()
        return SCP

    def DFB_CUI_CLSCC(obj):
        SCP = obj.ADJUST_CHLORIDE_INSULATION()
        if (SCP == "High"):
            SVI = 50
        elif (SCP == "Medium"):
            SVI = 10
        elif(SCP == "Low"):
            SVI = 1
        else:
            SVI = 0
        try:
            obj.EXTERN_CLSCC_CUI_INSP_EFF = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[14])
            obj.EXTERN_CLSCC_CUI_INSP_NUM = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[14])

            if (obj.EXTERN_CLSCC_CUI_INSP_EFF == "E" or obj.EXTERN_CLSCC_CUI_INSP_NUM == 0):
                FIELD = "E"
            else:
                FIELD = str(obj.EXTERN_CLSCC_CUI_INSP_NUM) + obj.EXTERN_CLSCC_CUI_INSP_EFF
            return DAL_CAL.POSTGRESQL.GET_TBL_74(SVI, FIELD)
        except Exception as e:
            print(e)
            return 0

    def DF_CUI_CLSCC(obj,age):
        # if not obj.EXTERN_COATING:
        #     return 0
        if (obj.AUSTENITIC_STEEL and obj.EXTERNAL_INSULATION and obj.EXTERNAL_EXPOSED_FLUID_MIST and not (
                obj.MIN_OP_TEMP > 150 or obj.MAX_OP_TEMP < 50)):
            if(age<1):
                return obj.DFB_CUI_CLSCC()
            else:
                return obj.DFB_CUI_CLSCC() * pow(obj.AGE_CUI(age), 1.1)
        else:
            return 0

    # Calculate HTHA
    def HTHA_PV(obj, age):
        try:
            HTHA_AGE = age * 24 * 365
            log1 = math.log10(obj.HTHA_PRESSURE / 0.0979)
            log2 = 3.09 * pow(10, -4) * (obj.CRITICAL_TEMP + 273) * (math.log10(HTHA_AGE) + 14)
            return log1 + log2
        except:
            return 0

    def HTHA_SUSCEP(obj, age):
        SUSCEP = ""
        if (obj.HTHADamageObserved == 1):
            if (obj.MAX_OP_TEMP > 177 and obj.HTHA_PRESSURE >= 0.345):
                SUSCEP = "High"
            else:
                SUSCEP = "No"
        else:
            HTHA_PRESSURE_psia = obj.HTHA_PRESSURE * 145;
            dataT = obj.MAX_OP_TEMP * 9 / 5 + 32;
            TemperatureAdjusted = dataT + 20
            deltaT = 0;
            if (obj.MATERIAL_SUSCEP_HTHA== True):
                if(obj.HTHA_MATERIAL == "Carbon Steel" or obj.HTHA_MATERIAL=="C-0.5Mo (Annealed)" or obj.HTHA_MATERIAL=="C-0.5Mo (Normalised)"):
                    if (obj.MAX_OP_TEMP > 177 and obj.HTHA_PRESSURE >= 0.345):
                        SUSCEP = "High"
                    else:
                        SUSCEP = "No"
                if(obj.HTHA_MATERIAL=="1Cr-0.5Mo"):
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
                if(obj.HTHA_MATERIAL=="1.25Cr-0.5Mo"):
                    if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1250.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1668 * HTHA_PRESSURE_psia) + 1150.0))
                    elif((HTHA_PRESSURE_psia >= 1250.0) and (HTHA_PRESSURE_psia < 1800.0)):
                        deltaT = (TemperatureAdjusted - (1171.11 * pow(HTHA_PRESSURE_psia - 1215.03, -0.092)))
                    elif((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 2600.0)):
                        deltaT = (TemperatureAdjusted - (((4E-05 * pow(HTHA_PRESSURE_psia,2.0)) - (0.2042 * HTHA_PRESSURE_psia)) + 903.69))
                    elif((HTHA_PRESSURE_psia >= 2600.0) and (HTHA_PRESSURE_psia < 13000.0)):
                        deltaT = (TemperatureAdjusted - 625.0)
                if(obj.HTHA_MATERIAL=="2.25Cr-1Mo"):
                    if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 2000.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1701 * HTHA_PRESSURE_psia) + 1200.0))
                    elif((HTHA_PRESSURE_psia >= 2000.0) and (HTHA_PRESSURE_psia < 6000.0)):
                        deltaT = (TemperatureAdjusted - 855.0)
                    elif(obj.HTHA_MATERIAL=="3Cr-1Mo"):
                        if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1800.0)):
                            deltaT = (TemperatureAdjusted - ((-0.1659 * HTHA_PRESSURE_psia) + 1250.0))
                        elif((HTHA_PRESSURE_psia >= 1800.0) and (HTHA_PRESSURE_psia < 6000.0)):
                            deltaT = (TemperatureAdjusted - 950.0)
                if(obj.HTHA_MATERIAL=="6Cr-0.5Mo"):
                    if((HTHA_PRESSURE_psia >= 50.0) and (HTHA_PRESSURE_psia < 1100.0)):
                        deltaT = (TemperatureAdjusted - ((-0.1254 * HTHA_PRESSURE_psia) + 1300.0))
                    elif((HTHA_PRESSURE_psia >= 1100.0) and (HTHA_PRESSURE_psia < 6000.0)):
                        deltaT = (TemperatureAdjusted - 1120.0)
                if(obj.HTHA_MATERIAL=="Not Applicable"):
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

    # def API_DF_HTHA(obj, age):
    #     API_HTHA = DAL_CAL.POSTGRESQL.GET_TBL_204(obj.HTHA_SUSCEP(age))
    #     obj.HTHA_EFFECT = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[15])
    #     obj.HTHA_NUM_INSP = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[15])
    #     if obj.HTHA_NUM_INSP > 2:
    #         obj.HTHA_NUM_INSP = 2
    #
    #     if (obj.DAMAGE_FOUND):
    #         return 2000
    #     else:
    #         if (obj.HTHA_NUM_INSP == 0):
    #             return API_HTHA[0]
    #         elif (obj.HTHA_NUM_INSP == 1 and obj.HTHA_EFFECT == "D"):
    #             return API_HTHA[1]
    #         elif (obj.HTHA_NUM_INSP == 1 and obj.HTHA_EFFECT == "C"):
    #             return API_HTHA[2]
    #         elif (obj.HTHA_NUM_INSP == 1 and obj.HTHA_EFFECT == "B"):
    #             return API_HTHA[3]
    #         elif (obj.HTHA_NUM_INSP == 2 and obj.HTHA_EFFECT == "D"):
    #             return API_HTHA[4]
    #         elif (obj.HTHA_NUM_INSP == 2 and obj.HTHA_EFFECT == "C"):
    #             return API_HTHA[5]
    #         else:
    #             return API_HTHA[6]

    def DF_HTHA(obj, age):
        if(obj.Hydrogen == 0 or obj.MAX_OP_TEMP == 0):
            return 0 # sua thanh -1 khi dung inspection plan
        if(obj.HTHA_SUSCEP(age) == "No"):
            return 0 # sua thanh -1 khi dung inspection plan
        elif(obj.HTHA_SUSCEP(age) == "Observed" or obj.HTHA_SUSCEP(age) == "High"):
            kq = 5000
        elif(obj.HTHA_SUSCEP(age) == "Medium"):
            kq = 2000
        elif(obj.HTHA_SUSCEP(age) == "Low"):
            kq = 100
        else:
            kq = 0
        return kq

    # Calculate BRITTLE
    def DFB_BRIITLE(obj):
        TEMP_BRITTLE = 0
        if(obj.PRESSSURE_CONTROL):
            TEMP_BRITTLE=obj.MIN_TEMP_PRESSURE
        else:
            TEMP_BRITTLE=obj.CRITICAL_TEMP
        if (obj.PWHT):
            return DAL_CAL.POSTGRESQL.GET_TBL_215(obj.API_TEMP(TEMP_BRITTLE - obj.REF_TEMP),
                                                 obj.API_SIZE_BRITTLE(obj.BRITTLE_THICK))
        else:
            return DAL_CAL.POSTGRESQL.GET_TBL_214(obj.API_TEMP(TEMP_BRITTLE - obj.REF_TEMP),
                                                 obj.API_SIZE_BRITTLE(obj.BRITTLE_THICK))

    def DF_BRITTLE(obj,i):
        try:
            Fse = 1
            if(obj.BRITTLE_THICK<=12.7 or (obj.FABRICATED_STEEL and obj.EQUIPMENT_SATISFIED and obj.NOMINAL_OPERATING_CONDITIONS
            and obj.CET_THE_MAWP and obj.CYCLIC_SERVICE and obj.EQUIPMENT_CIRCUIT_SHOCK and (obj.NomalThick <=50.8))):
                Fse = 0.01
            if (obj.CARBON_ALLOY and (obj.CRITICAL_TEMP < obj.MIN_DESIGN_TEMP or obj.MAX_OP_TEMP < obj.MIN_DESIGN_TEMP)):
                # if (obj.LOWEST_TEMP):
                print("Tempbrit",obj.DFB_BRIITLE())
                return obj.DFB_BRIITLE() * Fse
                # else:
                #     return obj.DFB_BRIITLE()
            else:
                return 0
        except Exception as e:
            print(e)

    # Calculate TEMP EMBRITTLE
    def API_SIZE_BRITTLE(obj, SIZE):
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

    def API_TEMP(obj, TEMP):
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

    def DF_TEMP_EMBRITTLE(obj,i):
        if (obj.TEMPER_SUSCEP and (obj.CARBON_ALLOY and not (obj.MAX_OP_TEMP < 343 or obj.MIN_OP_TEMP > 577))):
            TEMP_EMBRITTLE = 0
            print("go temp")
            if (obj.PRESSSURE_CONTROL):
                TEMP_EMBRITTLE = obj.MIN_TEMP_PRESSURE - (obj.REF_TEMP + obj.DELTA_FATT)
            else:
                TEMP_EMBRITTLE = min(obj.MIN_DESIGN_TEMP, obj.CRITICAL_TEMP) - (obj.REF_TEMP + obj.DELTA_FATT)
            if (obj.PWHT):
                return DAL_CAL.POSTGRESQL.GET_TBL_215(obj.API_TEMP(TEMP_EMBRITTLE),
                                                     obj.API_SIZE_BRITTLE(obj.BRITTLE_THICK))
            else:
                print(TEMP_EMBRITTLE, obj.BRITTLE_THICK)
                return DAL_CAL.POSTGRESQL.GET_TBL_214(obj.API_TEMP(TEMP_EMBRITTLE),
                                                     obj.API_SIZE_BRITTLE(obj.BRITTLE_THICK))
        else:
            return 0

    # Calculate 885w
    def DF_885(obj,i):
        if (obj.CHROMIUM_12 and not (obj.MIN_OP_TEMP > 566 or obj.MAX_OP_TEMP < 371)):
            TEMP_885 = 0
            if(obj.PRESSSURE_CONTROL):
                TEMP_885 = obj.MIN_TEMP_PRESSURE - obj.REF_TEMP
            else:
                TEMP_885 = min(obj.MIN_DESIGN_TEMP, obj.CRITICAL_TEMP) - obj.REF_TEMP
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
    def API_TEMP_SIGMA(obj,MIN_TEM):
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

    def DF_SIGMA(obj,i):
        if (obj.AUSTENITIC_STEEL and not (obj.MIN_OP_TEMP > 927 or obj.MAX_OP_TEMP < 593)):
            TEMP_SIGMA  = 0
            if (obj.PRESSSURE_CONTROL):
                TEMP_SIGMA  = obj.MIN_TEMP_PRESSURE
            else:
                TEMP_SIGMA  = min(obj.MIN_DESIGN_TEMP, obj.CRITICAL_TEMP)
            TEMP = obj.API_TEMP_SIGMA(TEMP_SIGMA)
            DFB_SIGMA = 0
            if (TEMP == 649):
                if (obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0
                else:
                    DFB_SIGMA = 18
            elif (TEMP == 538):
                if (obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0
                else:
                    DFB_SIGMA = 53
            elif (TEMP == 427):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0.2
                else:
                    DFB_SIGMA = 160
            elif (TEMP == 316):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 0.9
                else:
                    DFB_SIGMA = 481
            elif (TEMP == 204):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 1.3
                else:
                    DFB_SIGMA = 1333
            elif (TEMP == 93):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.1
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 3
                else:
                    DFB_SIGMA = 3202
            elif (TEMP == 66):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.3
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 5
                else:
                    DFB_SIGMA = 3871
            elif (TEMP == 38):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.6
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 7
                else:
                    DFB_SIGMA = 4196
            elif (TEMP == 10):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 0.9
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 11
                else:
                    DFB_SIGMA = 4196
            elif (TEMP == -18):
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 1
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 20
                else:
                    DFB_SIGMA = 4196
            else:
                if (obj.PERCENT_SIGMA < 5):
                    DFB_SIGMA = 1.1
                elif (obj.PERCENT_SIGMA >= 5 and obj.PERCENT_SIGMA < 10):
                    DFB_SIGMA = 34
                else:
                    DFB_SIGMA = 4196
            return DFB_SIGMA
        else:
            return 0

    # Calculate Pipping
    def DFB_PIPE(obj):
        if (obj.PREVIOUS_FAIL == "Greater than one"):
            DFB_PF = 500
        elif (obj.PREVIOUS_FAIL == "One"):
            DFB_PF = 50
        else:
            DFB_PF = 1

        if (obj.AMOUNT_SHAKING == "Severe"):
            DFB_AS = 500
        elif (obj.AMOUNT_SHAKING == "Moderate"):
            DFB_AS = 50
        else:
            DFB_AS = 1

        if (obj.TIME_SHAKING == "13 to 52 weeks"):
            FFB_AS = 0.02
        elif (obj.TIME_SHAKING == "2 to 13 weeks"):
            FFB_AS = 0.2
        else:
            FFB_AS = 1

        if (obj.CYLIC_LOAD == "Reciprocating machinery"):
            DFB_CF = 50
        elif (obj.CYLIC_LOAD == "PRV chatter"):
            DFB_CF = 25
        elif (obj.CYLIC_LOAD == "Valve with high pressure drop"):
            DFB_CF = 10
        else:
            DFB_CF = 1

        return max(DFB_PF, max(DFB_AS * FFB_AS, DFB_CF))

    def checkPiping(obj):
        pip = ["PIPE-1", "PIPE-2", "PIPE-4", "PIPE-6", "PIPE-8", "PIPE-10", "PIPE-12","PIPE-16", "PIPEGT16"]
        check = False
        for a in pip:
            if obj.APIComponentType == a:
                check = True
                break
        return check

    def DF_PIPE(obj,i):
        if (obj.checkPiping()):
            if (obj.CORRECT_ACTION == "Engineering Analysis"):
                FCA = 0.002
            elif (obj.CORRECT_ACTION == "Experience"):
                FCA = 0.2
            else:
                FCA = 2

            if (obj.NUM_PIPE == "Up to 5"):
                FPC = 0.5
            elif (obj.NUM_PIPE == "6 to 10"):
                FPC = 1
            else:
                FPC = 2

            if (
                    obj.PIPE_CONDITION == "Broken gussets or gussets welded directly to pipe" or obj.PIPE_CONDITION == "Missing or damage supports, improper support"):
                FCP = 2
            else:
                FCP = 1

            if (obj.JOINT_TYPE == "Sweepolets"):
                FJB = 0.02
            elif (obj.JOINT_TYPE == "Piping tee weldolets"):
                FJB = 0.2
            elif (obj.JOINT_TYPE == "Threaded, socket welded, or saddle on"):
                FJB = 2
            else:
                # FJB = 1
                FJB = 0

            if (obj.BRANCH_DIAMETER == "All branches greater than 2\" Nominal OD"):
                FBD = 0.02
            else:
                FBD = 1
            return obj.DFB_PIPE() * FCA * FPC * FCP * FJB * FBD
        else:
            return 0


    ##################################################################################
    def GET_AGE_INSERVICE(obj):
        return float((obj.AssesmentDate.date() - obj.CommissionDate.date()).days/365)

    def GET_AGE(obj):
        age = np.zeros(21)#(0,14)
        for a in range(0,21):#(0,14)
            age[a] = DAL_CAL.POSTGRESQL.GET_AGE_INSP(obj.ComponentNumber,obj.DM_Name[a],obj.CommissionDate, obj.AssesmentDate)
        return age

    def DF_THINNING_API(obj, i):
        # print("test THIN 1233-------")
        # print(obj.GET_AGE()[0])
        # print(obj.DF_THIN(obj.GET_AGE()[0] + i))
        return obj.DF_THIN(obj.GET_AGE()[0] + i)

    def DF_LINNING_API(obj, i):
        # print(obj.DF_LINNING(obj.GET_AGE()[1] + i))
        return obj.DF_LINNING(obj.GET_AGE()[1] + i)

    def DF_CAUTISC_API(obj, i):
        return obj.DF_CAUSTIC(obj.GET_AGE()[2] + i)

    def DF_AMINE_API(obj, i):
        return obj.DF_AMINE(obj.GET_AGE()[3] + i)

    def DF_SULPHIDE_API(obj, i):
        return obj.DF_SULPHIDE(obj.GET_AGE()[4] + i)

    def DF_HICSOHIC_H2S_API(obj, i):
        return obj.DF_HICSOHIC_H2S(obj.GET_AGE()[5] + i)

    def DF_CACBONATE_API(obj,i):
        return obj.DF_CACBONATE(obj.GET_AGE()[6] + i)

    def DF_PTA_API(obj,i):
        return obj.DF_PTA(obj.GET_AGE()[7] + i)

    def DF_CLSCC_API(obj,i):
        return obj.DF_CLSCC(obj.GET_AGE()[8] + i)

    def DF_HSCHF_API(obj, i):
        return obj.DF_HSCHF(obj.GET_AGE()[9] + i)

    def DF_HIC_SOHIC_HF_API(obj, i):
        return obj.DF_HIC_SOHIC_HF(obj.GET_AGE()[10] + i)

    def DF_EXTERNAL_CORROSION_API(obj, i):
        # print(obj.DF_EXTERNAL_CORROSION(obj.GET_AGE()[11] + i))
        return obj.DF_EXTERNAL_CORROSION(obj.GET_AGE()[11] + i)

    def DF_CUI_API(obj, i):
        return obj.DF_CUI(obj.GET_AGE()[12] + i)

    def DF_EXTERN_CLSCC_API(obj, i):
        return obj.DF_EXTERN_CLSCC(obj.GET_AGE()[13] + i)

    def DF_CUI_CLSCC_API(obj,i):
        return obj.DF_CUI_CLSCC(obj.GET_AGE()[14] + i)

    def DF_HTHA_API(obj, i):#chua test dc
        return obj.DF_HTHA(obj.GET_AGE()[15] + i)

    def DF_BRITTLE_API(obj, i):
        return obj.DF_BRITTLE(obj.GET_AGE()[16] + i)

    def DF_TEMP_EMBRITTLE_API(obj,i):
        return obj.DF_TEMP_EMBRITTLE(obj.GET_AGE()[17] + i)

    def DF_885_API(obj,i):
        return obj.DF_885(obj.GET_AGE()[18] + i)

    def DF_SIGMA_API(obj,i):
        return obj.DF_SIGMA(obj.GET_AGE()[19] + i)

    def DF_PIPE_API(obj,i):
        return obj.DF_PIPE(obj.GET_AGE()[20] + i)

    # TOTAL ---------------------
    def DF_SSC_TOTAL_API(obj, i):#done - con anie)
        DF_SCC = max(obj.DF_CAUTISC_API(i), obj.DF_AMINE_API(i), obj.DF_SULPHIDE_API(i), obj.DF_HIC_SOHIC_HF_API(i), obj.DF_HICSOHIC_H2S_API(i),
                     obj.DF_CACBONATE_API(i), obj.DF_PTA_API(i), obj.DF_CLSCC_API(i), obj.DF_HSCHF(i))
        # print(obj.DF_CAUTISC_API(i))
        # print(obj.DF_AMINE_API(i))
        # print(obj.DF_SULPHIDE_API(i))
        # print(obj.DF_HIC_SOHIC_HF_API(i))
        # print(obj.DF_HICSOHIC_H2S_API(i))
        # print(obj.DF_CACBONATE_API(i))
        # print(obj.DF_PTA_API(i))
        # print(obj.DF_CLSCC_API(i))
        # print(obj.DF_HSCHF(i))
        return DF_SCC

    def DF_EXT_TOTAL_API(obj, i):#done
        DF_EXT = max(obj.DF_EXTERNAL_CORROSION_API(i), obj.DF_CUI_API(i),obj.DF_EXTERN_CLSCC_API(i), obj.DF_CUI_CLSCC_API(i))
        return DF_EXT
        #return 0.07

    def DF_BRIT_TOTAL_API(obj,i):#done
        DF_BRIT = max(obj.DF_BRITTLE_API(i) + obj.DF_TEMP_EMBRITTLE_API(i), obj.DF_SIGMA_API(i), obj.DF_885_API(i))
        return DF_BRIT

    def DF_THINNING_TOTAL_API(obj, i):#done
        try:
            if obj.INTERNAL_LINNING and (obj.DF_LINNING_API(i) != 0):
                DF_THINNING_TOTAL = min(obj.DF_THINNING_API(i), obj.DF_LINNING_API(i))
            else:
                DF_THINNING_TOTAL = obj.DF_THINNING_API(i)
            return DF_THINNING_TOTAL
        except Exception as e:
            print(e, "erorr thin")

    def DF_RISK_CHART_THINNING(obj):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = obj.DF_THINNING_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_EXT(obj):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = obj.DF_EXT_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_SSC(obj):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = obj.DF_SSC_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_HTHA(obj):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = obj.DF_HTHA_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_BRIT(obj):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = obj.DF_BRIT_TOTAL_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_RISK_CHART_PIPE(obj):
        try:
            data = []
            # for a in range(1, 16):
            for a in range(1, 16):
                risk = obj.DF_PIPE_API(a)
                data.append(risk)
            return data
        except Exception as e:
            print(e)
        return data

    def DF_TOTAL_API(obj,i):#testing df_htha
        try:
            TOTAL_DF_API = max(obj.DF_THINNING_TOTAL_API(i), obj.DF_EXT_TOTAL_API(i)) + obj.DF_SSC_TOTAL_API(
                i) + obj.DF_HTHA_API(i) + obj.DF_BRIT_TOTAL_API(i) + obj.DF_PIPE_API(i)
        except Exception as e:
            print(e)
        return TOTAL_DF_API

    def DF_TOTAL_GENERAL(obj, i):#testing df_htha
        TOTAL_DF_API = obj.DF_THINNING_TOTAL_API(i) + obj.DF_EXT_TOTAL_API(i) + obj.DF_SSC_TOTAL_API(
            i) + obj.DF_HTHA_API(i) + obj.DF_BRIT_TOTAL_API(i) + obj.DF_PIPE_API(i)
        print( "DF_total",TOTAL_DF_API,i)
        return TOTAL_DF_API

    def convertRisk(obj,risk):
        if risk >= 1:
            return 1
        else:
            return risk

    def DF_LIST_16(obj, FC_Total, GFF, FSM, Risk_Target):
        
        data = []
        
        a = 1
        temp = 0
        
        poin=-1
        while (a < 17.0):
            obj = {}
            obj['df_factor'] = obj.DF_TOTAL_API(a)
            obj['pof'] = obj.convertRisk(obj['df_factor'] * GFF * FSM)
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
                    objNew['df_factor'] = obj.DF_TOTAL_API(minia)
                    objNew['pof'] = obj.convertRisk(objNew['df_factor'] * GFF * FSM)
                    objNew['risk'] = objNew['pof'] * FC_Total
                    # risknew=obj.convertRisk(obj.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total
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
                objNew['df_factor'] = obj.DF_TOTAL_API(minia)
                objNew['pof'] = obj.convertRisk(objNew['df_factor'] * GFF * FSM)
                objNew['risk'] = objNew['pof'] * FC_Total
                # risknew = obj.convertRisk(obj.DF_TOTAL_API(minia) * GFF * FSM) * FC_Total
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

    def DF_LIST_16_GENERAL(obj,FC_Total, GFF, FSM, Risk_Target):
        data = []
      
        a=1
        temp=0
       
        poin = -1
        while (a<17.0):
            obj={}
            obj['df_factor']=obj.DF_TOTAL_GENERAL(a)
            obj['pof']=obj.convertRisk(obj['df_factor'] * GFF * FSM)
            # print(obj['pof'])
            obj['risk']=obj['pof']*FC_Total
          
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
                    objNew['df_factor'] = obj.DF_TOTAL_GENERAL(minia)
                    objNew['pof'] = obj.convertRisk(objNew['df_factor'] * GFF * FSM)
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
                objNew['df_factor'] = obj.DF_TOTAL_GENERAL(minia)
                objNew['pof'] = obj.convertRisk(objNew['df_factor'] * GFF * FSM)
                objNew['risk'] = objNew['pof'] * FC_Total
                # risknew = obj.convertRisk(obj.DF_TOTAL_GENERAL(minia) * GFF * FSM) * FC_Total
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

    def INSP_DUE_DATE(obj, FC_Total, GFF, FSM, Risk_Target):
        DF_TARGET = Risk_Target/(FC_Total * GFF * FSM)
        # for a in range(1,16):
        for a in range(0,16):
            if obj.DF_TOTAL_API(a) >= DF_TARGET:
                break
        if(a==15):
            return obj.AssesmentDate + relativedelta(years=a+1)
        else:
            return obj.AssesmentDate + relativedelta(years=a-1)

    def INSP_DUE_DATE_General(obj, FC_total, GFF, FSM, Risk_Target):
        DF_TARGET = Risk_Target/(FC_total*GFF*FSM)
        # for a in range(1,16):
        for a in range(0,16):
            if obj.DF_TOTAL_GENERAL(a) >= DF_TARGET:
                break
        if(a==15):
            return obj.AssesmentDate + relativedelta(year=a+1)
        else:
            return obj.AssesmentDate + relativedelta(year=a)

    def SEND_EMAIL(obj, FC_Total, GFF, FSM, Risk_Target,ErrDammage,facilityname,request):
        try:
            DF_TARGET = Risk_Target/(FC_Total * GFF * FSM)
            if obj.DF_TOTAL_API(0) >= DF_TARGET or obj.DF_TOTAL_API(1) >= DF_TARGET:
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

    def ISDF(obj):
        DM_ID = [8, 9, 61, 57, 73, 69, 60, 72, 62, 70, 67, 34, 32, 66, 63, 68, 2, 18, 1, 14, 10]
        data_mechanism = []
        DF_ITEM = np.zeros(21)
        DF_ITEM[0] = obj.DF_THINNING_API(0)
        DF_ITEM[1] = obj.DF_LINNING_API(0)
        DF_ITEM[2] = obj.DF_CAUTISC_API(0)
        DF_ITEM[3] = obj.DF_AMINE_API(0)
        DF_ITEM[4] = obj.DF_SULPHIDE_API(0)
        DF_ITEM[5] = obj.DF_HICSOHIC_H2S_API(0)
        DF_ITEM[6] = obj.DF_CACBONATE_API(0)
        DF_ITEM[7] = obj.DF_PTA_API(0)
        DF_ITEM[8] = obj.DF_CLSCC_API(0)
        DF_ITEM[9] = obj.DF_HSCHF_API(0)
        DF_ITEM[10] = obj.DF_HIC_SOHIC_HF_API(0)
        DF_ITEM[11] = obj.DF_EXTERNAL_CORROSION_API(0)
        DF_ITEM[12] = obj.DF_CUI_API(0)
        DF_ITEM[13] = obj.DF_EXTERN_CLSCC_API(0)
        DF_ITEM[14] = obj.DF_CUI_CLSCC_API(0)
        DF_ITEM[15] = obj.DF_HTHA_API(0)
        DF_ITEM[16] = obj.DF_BRITTLE_API(0)
        DF_ITEM[17] = obj.DF_TEMP_EMBRITTLE_API(0)
        DF_ITEM[18] = obj.DF_885_API(0)
        DF_ITEM[19] = obj.DF_SIGMA_API(0)
        DF_ITEM[20] = obj.DF_PIPE_API(0)
        for i in range(0,21):
            if DF_ITEM[i] > 0:
                data_return = {}
                data_return['DF1'] = DF_ITEM[i]
                data_return['DM_ITEM_ID'] = DM_ID[i]
                data_return['isActive'] = 1
                data_return['i'] = i
                data_return['highestEFF'] = DAL_CAL.POSTGRESQL.GET_MAX_INSP(obj.ComponentNumber, obj.DM_Name[i])
                data_return['secondEFF'] = data_return['highestEFF']
                data_return['numberINSP'] = DAL_CAL.POSTGRESQL.GET_NUMBER_INSP(obj.ComponentNumber, obj.DM_Name[i])
                data_return['lastINSP'] = DAL_CAL.POSTGRESQL.GET_LAST_INSP(obj.ComponentNumber, obj.DM_Name[i], obj.AssesmentDate)
                if i == 0:
                    data_return['DF2'] = obj.DF_THINNING_API(3)
                    data_return['DF3'] = obj.DF_THINNING_API(6)
                elif i == 1:
                    data_return['DF2'] = obj.DF_LINNING_API(3)
                    data_return['DF3'] = obj.DF_LINNING_API(6)
                elif i == 2:
                    data_return['DF2'] = obj.DF_CAUTISC_API(3)
                    data_return['DF3'] = obj.DF_CAUTISC_API(6)
                elif i == 3:
                    data_return['DF2'] = obj.DF_AMINE_API(3)
                    data_return['DF3'] = obj.DF_AMINE_API(6)
                elif i == 4:
                    data_return['DF2'] = obj.DF_SULPHIDE_API(3)
                    data_return['DF3'] = obj.DF_SULPHIDE_API(6)
                elif i == 5:
                    data_return['DF2'] = obj.DF_HICSOHIC_H2S_API(3)
                    data_return['DF3'] = obj.DF_HICSOHIC_H2S_API(6)
                elif i == 6:
                    data_return['DF2'] = obj.DF_CACBONATE_API(3)
                    data_return['DF3'] = obj.DF_CACBONATE_API(6)
                elif i == 7:
                    data_return['DF2'] = obj.DF_PTA_API(3)
                    data_return['DF3'] = obj.DF_PTA_API(6)
                elif i == 8:
                    data_return['DF2'] = obj.DF_CLSCC_API(3)
                    data_return['DF3'] = obj.DF_CLSCC_API(6)
                elif i == 9:
                    data_return['DF2'] = obj.DF_HSCHF_API(3)
                    data_return['DF3'] = obj.DF_HSCHF_API(6)
                elif i == 10:
                    data_return['DF2'] = obj.DF_HIC_SOHIC_HF_API(3)
                    data_return['DF3'] = obj.DF_HIC_SOHIC_HF_API(6)
                elif i == 11:
                    data_return['DF2'] = obj.DF_EXTERNAL_CORROSION_API(3)
                    data_return['DF3'] = obj.DF_EXTERNAL_CORROSION_API(6)
                elif i == 12:
                    data_return['DF2'] = obj.DF_CUI_API(3)
                    data_return['DF3'] = obj.DF_CUI_API(6)
                elif i == 15:
                    data_return['DF2'] = obj.DF_HTHA_API(3)
                    data_return['DF3'] = obj.DF_HTHA_API(6)
                else:
                    data_return['DF2'] = DF_ITEM[i]
                    data_return['DF3'] = DF_ITEM[i]
                data_mechanism.append(data_return)
        return data_mechanism










from cloud.process.RBI.Object.table import ConversionFactorCOF
from cloud.process.RBI.COF.TankBottom import tank_bottom_object
import math
from cloud.process.RBI import Postgresql as DAL_CAL

# Obj = tank_bottom_object.TankBottomCofObject 

class CaTankBottomUtil:
    def FC_Category(fc):
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

    def n_rh(TANK_DIAMETER):
        hole = {
            "D1": 0,
            "D4": 0
        }
        d4 = 1
        C36 = ConversionFactorCOF._C36
        d1 = max(pow(TANK_DIAMETER / C36, 2), 1)
        hole.update({"D1": d1, "D4": d4})
        return hole

    def k_h_bottom(Soil_type):
        k_h = [0, 0, 0]
        if (Soil_type == "Coarse Sand"):
            k_h[0] = 0.1
            k_h[1] = 0.01
            k_h[2] = 0.33
        elif(Soil_type == "Fine Sand"):
            k_h[0] = 0.01
            k_h[1] = 0.001
            k_h[2] = 0.33
        elif(Soil_type == "Very Fine Sand"):
            k_h[0] = pow(10, -3)
            k_h[1] = pow(10, -5)
            k_h[2] = 0.33
        elif(Soil_type == "Silt"):
            k_h[0] = pow(10, -5)
            k_h[1] = pow(10, -6)
            k_h[2] = 0.41
        elif(Soil_type == "Sandy Clay"):
            k_h[0] = pow(10, -6)
            k_h[1] = pow(10, -7)
            k_h[2] = 0.45
        elif(Soil_type == "Clay"):
            k_h[0] = pow(10, -7)
            k_h[1] = pow(10, -8)
            k_h[2] = 0.5
        elif(Soil_type == "Concrete-Asphalt"):
            k_h[0] = pow(10, -10)
            k_h[1] = pow(10, -11)
            k_h[2] = 0.3
        else:
            k_h[0] = 1
            k_h[1] = 0.1
            k_h[2] = 0.4
        return k_h

    def k_h_water(k_h_bottom):
        C31 = ConversionFactorCOF._C31
        k_h = k_h_bottom
        return C31 * (k_h[0] + k_h[1]) / 2

    def dn_bottom(PREVENTION_BARRIER, TANK_DIAMETER):
        hole = {
            "D1": 0,
            "D4": 0
        }
        if (PREVENTION_BARRIER):
            d1 = 3.175
        else:
            d1 = 12.7
        d4 = 250 * TANK_DIAMETER
        hole.update({"D1": d1, "D4": d4})
        return hole

    def rate_n_tank_bottom(PREVENTION_BARRIER, FLUID_HEIGHT, dn_bottom, k_h_prod, n_rh):
        try:
            hole = {"D1": 0, "D4": 0}
            C33 = ConversionFactorCOF._C33
            C34 = ConversionFactorCOF._C34
            C35 = ConversionFactorCOF._C35
            C37 = ConversionFactorCOF._C37
            C38 = ConversionFactorCOF._C38
            C39 = ConversionFactorCOF._C39
            C40 = ConversionFactorCOF._C40
            _height = FLUID_HEIGHT
            if (PREVENTION_BARRIER):
                _height = 0.0762
            ps = pow(dn_bottom.get("D1"), 1.8) / (0.21 * pow(_height, 0.4))
            if (k_h_prod > C34 * pow(dn_bottom.get("D1"), 2)):
                d1 = C33 * math.pi * \
                    dn_bottom.get("D1") * math.sqrt(2 * 1 *
                                                    _height) * n_rh.get("D1")
            elif (k_h_prod <= C37 * pow(ps, (1 / 0.74))):
                d1 = C35 * 0.21 * pow(dn_bottom.get("D1"), 0.2) * \
                    pow(_height, 0.9) * pow(k_h_prod, 0.74) * n_rh.get("D1")
            else:
                m = C40-0.4324 * \
                    math.log10(dn_bottom.get("D1")) + \
                    0.5405*math.log10(_height)
                d1 = C38 * pow(10, 2*math.log10(dn_bottom.get("D1"))+0.5*math.log10(_height) -
                               0.74*pow((C39 * 2*math.log10(dn_bottom.get("D1"))-math.log10(k_h_prod))/m, m))

            if (k_h_prod > C34 * pow(dn_bottom.get("D4"), 2)):
                d4 = C33 * math.pi * \
                    dn_bottom.get("D4") * math.sqrt(2 * 1 *
                                                    _height) * n_rh.get("D4")
            elif (k_h_prod <= C37 * pow(ps, (1 / 0.74))):
                d4 = C35 * 0.21 * pow(dn_bottom.get("D4"), 0.2) * \
                    pow(_height, 0.9) * pow(k_h_prod, 0.74) * n_rh.get("D4")
            else:
                m = C40-0.4324 * \
                    math.log10(dn_bottom.get("D4")) + \
                    0.5405*math.log10(_height)
                d4 = C38 * pow(10, 2*math.log10(dn_bottom.get("D4"))+0.5*math.log10(_height) -
                               0.74*pow((C39 * 2*math.log10(dn_bottom.get("D4"))-math.log10(k_h_prod))/m, m))

            hole.update({"D1": d1, "D4": d4})
            return hole
        except Exception as e:
            print("Error rate_n_tank_bottom:", e)

    def t_ld_tank_bottom(Concrete_Asphalt, PREVENTION_BARRIER):
        if (Concrete_Asphalt):
            return 7
        elif (PREVENTION_BARRIER):
            return 30
        else:
            return 360

    def BBL_TOTAL_TANKBOTTOM(TANK_DIAMETER, FLUID_HEIGHT):
        C13 = ConversionFactorCOF._C13
        return math.pi * pow(TANK_DIAMETER, 2) * FLUID_HEIGHT / (4 * C13)

    def ld_n_tank_bottom(TANK_DIAMETER, FLUID_HEIGHT, rate_n_tank_bottom, t_ld_tank_bottom):
        try:
            hole = {"D1": 0, "D4": 0}
            C13 = ConversionFactorCOF._C13
            Bbl_total_tank_bottom = (
                math.pi * pow(TANK_DIAMETER, 2) * FLUID_HEIGHT * C13) / 4
            if rate_n_tank_bottom.get("D1") == 0:
                d1 = t_ld_tank_bottom()
            else:
                d1 = min(float(Bbl_total_tank_bottom) /
                         rate_n_tank_bottom.get("D1"), t_ld_tank_bottom)

            if rate_n_tank_bottom.get("D4") == 0:
                d4 = t_ld_tank_bottom()
            else:
                d4 = min(float(Bbl_total_tank_bottom) /
                         rate_n_tank_bottom.get("D4"), t_ld_tank_bottom)
            hole.update({"D1": d1, "D4": d4})
            return hole
        except Exception as e:
            print("Error ld_n_tank_bottom:", e)

    def Bbl_leak_n_bottom(TANK_DIAMETER, FLUID_HEIGHT, rate_n_tank_bottom, ld_n_tank_bottom):
        C13 = ConversionFactorCOF._C13
        hole = {"D1": 0, "D4": 0}
        Bbl_total_tank_bottom = (
            math.pi * pow(TANK_DIAMETER, 2) * FLUID_HEIGHT * C13) / (4)
        d4 = min(rate_n_tank_bottom.get("D4") * ld_n_tank_bottom.get("D4"), Bbl_total_tank_bottom)
        Bbl_total_tank_bottom = (
            math.pi * pow(TANK_DIAMETER, 2) * FLUID_HEIGHT * C13) / (4)
        d1 = min(rate_n_tank_bottom.get("D1") * ld_n_tank_bottom.get("D1"), Bbl_total_tank_bottom)
        hole.update({"D1": d1, "D4": d4})
        return hole

    def Bbl_rupture_bottom(TANK_DIAMETER, FLUID_HEIGHT): 
        C13 = ConversionFactorCOF._C13
        Bbl_total_tank_bottom = (
            math.pi * pow(TANK_DIAMETER, 2) * FLUID_HEIGHT * C13) / (4)
        return Bbl_total_tank_bottom

    def GET_PL_UL(TANK_FLUID):
        data = [0, 0]
        if (TANK_FLUID == "Gasoline"):
            data[0] = 684.018
            data[1] = 4.01 * pow(10, -3)
        elif(TANK_FLUID == "Light Diesel Oil"):
            data[0] = 734.011
            data[1] = 1.04 * pow(10, -3)
        elif(TANK_FLUID == "Heavy Diesel Oil"):
            data[0] = 764.527
            data[1] = 2.46 * pow(10, -3)
        elif(TANK_FLUID == "Fuel Oil"):
            data[0] = 775.019
            data[1] = 3.69 * pow(10, -2)
        elif (TANK_FLUID == "Crude Oil"):
            data[0] = 775.019
            data[1] = 3.69 * pow(10, -2)
        elif (TANK_FLUID == "Heavy Crude Oil"):
            data[0] = 900.026
            data[1] = 4.6 * pow(10, -2)
        elif (TANK_FLUID == "Heavy Fuel Oil"):
            data[0] = 900.026
            data[1] = 4.6 * pow(10, -2)
        else:
            data[0] = 1000
            data[1] = 1
        return data

    def k_h_prod(GET_PL_UL, k_h_water):
        pl_ul = GET_PL_UL
        return k_h_water * (pl_ul[0] / 1000) * (1 / pl_ul[1])

    def vel_s_prod(k_h_bottom, k_h_prod):
        kh = k_h_bottom
        return k_h_prod / kh[2]

    def t_gl_bottom(Swg, vel_s_prod):
        try:
            return Swg / vel_s_prod
        except:
            return 1

    def Bbl_leak_groundwater(t_gl_bottom, t_ld_tank_bottom, Bbl_leak_n_bottom):
        try:
            hole = {"D1": 0, "D4": 0} 
            d1, d4 = 0, 0
            if (t_gl_bottom < t_ld_tank_bottom):
                d1 = Bbl_leak_n_bottom.get("D1") * ((t_ld_tank_bottom - t_gl_bottom) / t_ld_tank_bottom)
            if (t_gl_bottom < t_ld_tank_bottom):
                d4 = Bbl_leak_n_bottom.get("D4") * ((t_ld_tank_bottom - t_gl_bottom) / t_ld_tank_bottom) 
            hole.update({"D1": d1, "D4": d4})
            return hole
        except Exception as e:
            print("Error Bbl_leak_groundwater:", e)

    def Bbl_leak_subsoil(Bbl_leak_n_bottom, Bbl_leak_groundwater):
        hole = {"D1": 0, "D4": 0}
        d1 = Bbl_leak_n_bottom.get("D1") - Bbl_leak_groundwater.get("D1")
        d4 = Bbl_leak_n_bottom.get("D4") - Bbl_leak_groundwater.get("D4")
        hole.update({"D1": d1, "D4": d4})
        return hole

    def getCost(EnvironSensitivity):
        costTANK = [0, 0, 0, 0, 0, 0]
        if (EnvironSensitivity == "High"):
            costTANK[0] = 10
            costTANK[1] = 50
            costTANK[2] = 500
            costTANK[3] = 3000
            costTANK[4] = 10000
            costTANK[5] = 5000
        elif (EnvironSensitivity == "Medium"):
            costTANK[0] = 10
            costTANK[1] = 50
            costTANK[2] = 250
            costTANK[3] = 1500
            costTANK[4] = 5000
            costTANK[5] = 1500
        elif (EnvironSensitivity == "Low"):
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

    def FC_leak_environ_bottom(TANK_FLUID, getCost, Bbl_leak_groundwater, Bbl_leak_subsoil):
        if(TANK_FLUID == "Water"):
            return 0
        cost = getCost
        obj = [0.00072, 0, 0, 0.000002, 0.00072, 5000, 0, 0, 120000, 5, 0, 0, 50]
        summa = 0
        summa = summa + (Bbl_leak_groundwater.get("D1") * cost[4] + Bbl_leak_subsoil.get("D1") * cost[3])*obj[0]
        summa = summa + (Bbl_leak_groundwater.get("D4") * cost[4] + Bbl_leak_subsoil.get("D4") * cost[3])*obj[3] 
        # for i in range(1, 4):
        #     summa = summa + (Bbl_leak_groundwater(i) *
        #                      cost[4] + Bbl_leak_subsoil(i) * cost[3])*obj[i-1] 
        return summa/obj[4]

    def Bbl_rupture_release_bottom(API_COMPONENT_TYPE_NAME, TANK_DIAMETER, FLUID_HEIGHT):
        obj = [0.00072, 0, 0, 0.000002, 0.00072, 5000, 0, 0, 120000, 5, 0, 0, 50]
        C13 = ConversionFactorCOF._C13
        Bbl_total_tank_bottom = (
            math.pi * pow(TANK_DIAMETER, 2) * FLUID_HEIGHT * C13) / (4)
        return (Bbl_total_tank_bottom * obj[3]) / obj[4]

    def Bbl_rupture_indike_bottom(Bbl_rupture_release_bottom, P_lvdike):
        indike = Bbl_rupture_release_bottom * (1 - P_lvdike / 100)
        if(indike > 0):
            return indike
        else:
            return 0

    def Bbl_rupture_ssonsite_bottom(P_onsite, Bbl_rupture_release_bottom, Bbl_rupture_indike_bottom):
        onsite = P_onsite * (Bbl_rupture_release_bottom -
                             Bbl_rupture_indike_bottom / 100)
        if(onsite > 0):
            return onsite
        else:
            return 0

    def Bbl_rupture_ssoffsite_bottom(P_offsite, Bbl_rupture_release_bottom, Bbl_rupture_indike_bottom, Bbl_rupture_ssonsite_bottom):
        offsite = P_offsite * (Bbl_rupture_release_bottom -
                               Bbl_rupture_indike_bottom - Bbl_rupture_ssonsite_bottom) / 100
        if(offsite > 0):
            return offsite
        else:
            return 0

    def Bbl_rupture_water_bottom(Bbl_rupture_release_bottom, Bbl_rupture_indike_bottom, Bbl_rupture_ssonsite_bottom, Bbl_rupture_ssoffsite_bottom):
        water = Bbl_rupture_release_bottom - \
            (Bbl_rupture_indike_bottom + Bbl_rupture_ssonsite_bottom +
             Bbl_rupture_ssoffsite_bottom)
        if(water > 0):
            return water
        else:
            return 0

    def FC_rupture_environ_bottom(getCost, TANK_FLUID, Bbl_rupture_indike_bottom, Bbl_rupture_ssonsite_bottom, Bbl_rupture_water_bottom, Bbl_rupture_ssoffsite_bottom):
        cost = getCost
        if (TANK_FLUID == "Water"):
            return 0
        else:
            return Bbl_rupture_indike_bottom * cost[0] + Bbl_rupture_ssonsite_bottom() * cost[1] + Bbl_rupture_ssoffsite_bottom * cost[2] + Bbl_rupture_water_bottom * cost[5]

    def FC_environ_bottom(FC_leak_environ_bottom, FC_rupture_environ_bottom):
        return FC_leak_environ_bottom + FC_rupture_environ_bottom

    def FC_cmd_bottom(MATERIAL_COST, API_COMPONENT_TYPE_NAME, TANK_DIAMETER):
        # obj = DAL_CAL.POSTGRESQL.GET_API_COM(API_COMPONENT_TYPE_NAME)
        obj = [0.00072, 0, 0, 0.000002, 0.00072, 5000, 0, 0, 120000, 5, 0, 0, 50]
        C36 = ConversionFactorCOF._C36
        summ = obj[0] * obj[5] + obj[1] * obj[6] + obj[2] * \
            obj[7] + obj[3] * obj[8] * pow(TANK_DIAMETER / C36, 2)
        return summ * MATERIAL_COST / obj[4]

    def FC_PROD_BOTTOM(PRODUCTION_COST, API_COMPONENT_TYPE_NAME):
        # obj = DAL_CAL.POSTGRESQL.GET_API_COM(API_COMPONENT_TYPE_NAME) 
        obj = [0.00072, 0, 0, 0.000002, 0.00072, 5000, 0, 0, 120000, 5, 0, 0, 50]
        t = obj[0] * obj[9] + obj[1] * obj[10] + \
            obj[2] * obj[11] + obj[3] * obj[12]
        return t * PRODUCTION_COST / obj[4]

    def FC_total_bottom(FC_cmd_bottom, FC_environ_bottom, FC_PROD_BOTTOM):
        FC_TOTAL_BOTTOM = FC_cmd_bottom() + FC_environ_bottom() + FC_PROD_BOTTOM()
        if FC_TOTAL_BOTTOM == 0:
            return 100000000
        else:
            return FC_cmd_bottom() + FC_environ_bottom() + FC_PROD_BOTTOM() 
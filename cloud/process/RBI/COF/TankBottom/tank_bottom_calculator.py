from cloud.process.RBI.COF.TankBottom import tank_bottom_util
Utilclass = tank_bottom_util.CaTankBottomUtil


class CA_TANK_BOTTOM:
    def __init__(self, Soil_type, TANK_FLUID, Swg, TANK_DIAMETER, FLUID_HEIGHT, API_COMPONENT_TYPE_NAME, PREVENTION_BARRIER, EnvironSensitivity, MATERIAL_COST, PRODUCTION_COST, P_lvdike, P_onsite, P_offsite, Concrete_Asphalt):
        self.Soil_type = Soil_type
        self.TANK_FLUID = TANK_FLUID
        self.Swg = Swg
        self.TANK_DIAMETER = TANK_DIAMETER
        self.FLUID_HEIGHT = FLUID_HEIGHT
        self.API_COMPONENT_TYPE_NAME = API_COMPONENT_TYPE_NAME
        self.PREVENTION_BARRIER = PREVENTION_BARRIER
        self.EnvironSensitivity = EnvironSensitivity
        self.MATERIAL_COST = MATERIAL_COST
        self.PRODUCTION_COST = PRODUCTION_COST
        self.P_lvdike = P_lvdike
        self.P_onsite = P_onsite
        self.P_offsite = P_offsite
        self.Concrete_Asphalt = Concrete_Asphalt

    def SequenceCalculator(self):
        n_rh = Utilclass.n_rh(self.TANK_DIAMETER)  # dict
        k_h_bottom = Utilclass.k_h_bottom(self.Soil_type)  # list
        k_h_water = Utilclass.k_h_water(k_h_bottom)  # float
        dn_bottom = Utilclass.dn_bottom(
            self.PREVENTION_BARRIER, self.TANK_DIAMETER)  # dict
        pl_ul = Utilclass.GET_PL_UL(self.TANK_FLUID)  # array 2 element
        k_h_prod = Utilclass.k_h_prod(pl_ul, k_h_water)  # float
        t_ld_tank_bottom = Utilclass.t_ld_tank_bottom(
            self.Concrete_Asphalt, self.PREVENTION_BARRIER)  # int
        rate_n_tank_bottom = Utilclass.rate_n_tank_bottom(
            self.PREVENTION_BARRIER, self.FLUID_HEIGHT, dn_bottom, k_h_prod, n_rh)  # dict
        # BBL_TOTAL_TANKBOTTOM = Utilclass.BBL_TOTAL_TANKBOTTOM(self.TANK_DIAMETER, self.FLUID_HEIGHT) #float
        ld_n_tank_bottom = Utilclass.ld_n_tank_bottom(
            self.TANK_DIAMETER, self.FLUID_HEIGHT, rate_n_tank_bottom, t_ld_tank_bottom)  # dict
        Bbl_leak_n_bottom = Utilclass.Bbl_leak_n_bottom(
            self.TANK_DIAMETER, self.FLUID_HEIGHT, rate_n_tank_bottom, ld_n_tank_bottom)  # dict
        Bbl_rupture_bottom = Utilclass.Bbl_rupture_bottom(self.TANK_DIAMETER, self.FLUID_HEIGHT) #float
        vel_s_prod = Utilclass.vel_s_prod(k_h_bottom, k_h_prod)  # float
        t_gl_bottom = Utilclass.t_gl_bottom(self.Swg, vel_s_prod)  # float
        Bbl_leak_groundwater = Utilclass.Bbl_leak_groundwater(
            t_gl_bottom, t_ld_tank_bottom, Bbl_leak_n_bottom)  # dict
        Bbl_leak_subsoil = Utilclass.Bbl_leak_subsoil(
            Bbl_leak_n_bottom, Bbl_leak_groundwater)  # dict
        getCost = Utilclass.getCost(self.EnvironSensitivity)  # list
        # kiem tra lai FC_leak_environ_bottom
        FC_leak_environ_bottom = Utilclass.FC_leak_environ_bottom(
            self.TANK_FLUID, getCost, Bbl_leak_groundwater, Bbl_leak_subsoil)
        Bbl_rupture_release_bottom = Utilclass.Bbl_rupture_release_bottom(
            self.API_COMPONENT_TYPE_NAME, self.TANK_DIAMETER, self.FLUID_HEIGHT)  # float
        Bbl_rupture_indike_bottom = Utilclass.Bbl_rupture_indike_bottom(
            Bbl_rupture_release_bottom, self.P_lvdike)  # float
        Bbl_rupture_ssonsite_bottom = Utilclass.Bbl_rupture_ssonsite_bottom(
            self.P_onsite, Bbl_rupture_release_bottom, Bbl_rupture_indike_bottom)  # float
        Bbl_rupture_ssoffsite_bottom = Utilclass.Bbl_rupture_ssoffsite_bottom(
            self.P_offsite, Bbl_rupture_release_bottom, Bbl_rupture_indike_bottom, Bbl_rupture_ssonsite_bottom)  # float
        Bbl_rupture_water_bottom = Utilclass.Bbl_rupture_water_bottom(
            Bbl_rupture_release_bottom, Bbl_rupture_indike_bottom, Bbl_rupture_ssonsite_bottom, Bbl_rupture_ssoffsite_bottom)  # float
        FC_rupture_environ_bottom = Utilclass.FC_rupture_environ_bottom(
            getCost, self.TANK_FLUID, Bbl_rupture_indike_bottom, Bbl_rupture_ssonsite_bottom, Bbl_rupture_water_bottom, Bbl_rupture_ssoffsite_bottom)  # float
        FC_environ_bottom = Utilclass.FC_environ_bottom(
            FC_leak_environ_bottom, FC_rupture_environ_bottom)  # float
        FC_cmd_bottom = Utilclass.FC_cmd_bottom(
            self.MATERIAL_COST, self.API_COMPONENT_TYPE_NAME, self.TANK_DIAMETER)  # float
        FC_PROD_BOTTOM = Utilclass.FC_PROD_BOTTOM(
            self.PRODUCTION_COST,  self.API_COMPONENT_TYPE_NAME)  # float
        FC_total_bottom = Utilclass.FC_total_bottom(
            FC_cmd_bottom, FC_environ_bottom, FC_PROD_BOTTOM)  # float
        output = {}
        output["k_h_water"] = k_h_water
        output["k_h_prod"] = k_h_prod
        output["vel_s_prod"] = vel_s_prod
        output["rate_n_tank_bottom"] = rate_n_tank_bottom
        output["ld_n_tank_bottom"] = ld_n_tank_bottom
        output["Bbl_leak_n_bottom"] = Bbl_leak_n_bottom
        output["Bbl_rupture_bottom"] = Bbl_rupture_bottom 
        
        output["t_gl_bottom"] = t_gl_bottom
        output["Bbl_leak_subsoil"] = Bbl_leak_subsoil
        output["Bbl_leak_groundwater"] = Bbl_leak_groundwater
        output["Bbl_rupture_indike_bottom"] = Bbl_rupture_indike_bottom
        output["Bbl_rupture_ssonsite_bottom"] = Bbl_rupture_ssonsite_bottom
        output["Bbl_rupture_ssoffsite_bottom"] = Bbl_rupture_ssoffsite_bottom
        output["Bbl_rupture_water_bottom"] = Bbl_rupture_water_bottom
        output["FC_leak_environ_bottom"] = FC_leak_environ_bottom
        output["FC_rupture_environ_bottom"] = FC_rupture_environ_bottom
        output["FC_environ_bottom"] = FC_environ_bottom
        output["FC_total_bottom"] = FC_total_bottom
        output["FC_cmd_bottom"] = FC_cmd_bottom
        output["FC_PROD_BOTTOM"] = FC_PROD_BOTTOM
        return output

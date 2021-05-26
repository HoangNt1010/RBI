from cloud.process.RBI import DM_CAL
from cloud.process.RBI import CA_CAL


def ThreadCofNormal(nominaldiameter, costfactor, api_fluid, storagephase, maxoperatingtemperature,
                    apicomponenttypename, detection_type, isulation_type, maxoperatingpressure,
                    minoperatingtemperature, mass_inventory, mass_component,
                    mitigation_system, toxic_percent, release_duration,
                    production_cost, toxic_fluid, injure_cost, evironment_cost,
                    personal_density, equipment_cost, output):
    ca_cal = CA_CAL.CA_NORMAL(NominalDiametter=nominaldiameter,
                              MATERIAL_COST=costfactor, FLUID=api_fluid,
                              FLUID_PHASE=storagephase,
                              MAX_OPERATING_TEMP=maxoperatingtemperature,
                              API_COMPONENT_TYPE_NAME=apicomponenttypename,
                              DETECTION_TYPE=detection_type,
                              ISOLATION_TYPE=isulation_type,
                              STORED_PRESSURE=maxoperatingpressure*1000,
                              ATMOSPHERIC_PRESSURE=101.325, STORED_TEMP=minoperatingtemperature,
                              MASS_INVERT=mass_inventory,
                              MASS_COMPONENT=mass_component,
                              MITIGATION_SYSTEM=mitigation_system,
                              TOXIC_PERCENT=toxic_percent,
                              RELEASE_DURATION=release_duration,
                              PRODUCTION_COST=production_cost, TOXIC_FLUID=toxic_fluid,
                              INJURE_COST=injure_cost, ENVIRON_COST=evironment_cost,
                              PERSON_DENSITY=personal_density,
                              EQUIPMENT_COST=equipment_cost)

    output["gff_small"] = ca_cal.gff(1)
    output["rwholegff_medium"] = ca_cal.gff(2)
    output["rwholeff_large"] = ca_cal.gff(3)
    output["rwhoff_rupture"] = ca_cal.gff(4)
    output["rwan_small"] = ca_cal.a_n(1)
    output["an_medium"] = ca_cal.a_n(2)
    output["an_large"] = ca_cal.a_n(3)
    output["an_rupture"] = ca_cal.a_n(4)
    output["wn_small"] = ca_cal.W_n(1)
    output["wn_medium"] = ca_cal.W_n(2)
    output["wn_large"] = ca_cal.W_n(3)
    output["wn_rupture"] = ca_cal.W_n(4)
    output["mass_add_n_small"] = ca_cal.mass_addn(1)
    output["mass_add_n_medium"] = ca_cal.mass_addn(2)
    output["mass_add_n_large"] = ca_cal.mass_addn(3)
    output["mass_add_n_rupture"] = ca_cal.mass_addn(4)
    output["mass_avail_n_small"] = ca_cal.mass_avail_n(1)
    output["mass_avail_n_medium"] = ca_cal.mass_avail_n(2)
    output["mass_avail_n_large"] = ca_cal.mass_avail_n(3)
    output["mass_avail_n_rupture"] = ca_cal.mass_avail_n(4)
    output["t_n_small"] = ca_cal.t_n(1)
    output["t_n_medium"] = ca_cal.t_n(2)
    output["releasetype_small"] = ca_cal.releaseType(1)
    output["t_n_large"] = ca_cal.t_n(3)
    output["t_n_rupture"] = ca_cal.t_n(4)
    output["releasetype_medium"] = ca_cal.releaseType(2)
    output["releasetype_large"] = ca_cal.releaseType(3)
    output["releasetype_rupture"] = ca_cal.releaseType(4)
    output["ld_max_n_small"] = ca_cal.ld_n_max(1)
    output["ld_max_n_medium"] = ca_cal.ld_n_max(2)
    output["ld_max_n_large"] = ca_cal.ld_n_max(3)
    output["ld_max_n_rupture"] = ca_cal.ld_n_max(4)
    output["rate_n_small"] = ca_cal.rate_n(1)
    output["rate_n_medium"] = ca_cal.rate_n(2)
    output["rate_n_large"] = ca_cal.rate_n(3)
    output["rate_n_rupture"] = ca_cal.rate_n(4)
    output["ld_n_small"] = ca_cal.ld_n(1)
    output["ld_n_medium"] = ca_cal.ld_n(2)
    output["ld_n_large"] = ca_cal.ld_n(3)
    output["ld_n_rupture"] = ca_cal.ld_n(4)
    output["mass_n_small"] = ca_cal.mass_n(1)
    output["mass_n_medium"] = ca_cal.mass_n(2)
    output["mass_n_large"] = ca_cal.mass_n(3)
    output["mass_n_rupture"] = ca_cal.mass_n(4)
    output["eneff_n_small"] = ca_cal.eneff_n(1)
    output["eneff_n_medium"] = ca_cal.eneff_n(2)
    output["eneff_n_large"] = ca_cal.eneff_n(3)
    output["eneff_n_rupture"] = ca_cal.eneff_n(4)
    output["factIC_n_small"] = ca_cal.fact_n_ic(1)
    output["factIC_n_medium"] = ca_cal.fact_n_ic(2)
    output["factIC_n_large"] = ca_cal.fact_n_ic(3)
    output["factIC_n_rupture"] = ca_cal.fact_n_ic(4)
    # save() cal level 1

    output["release_phase"] = ca_cal.ReleasePhase()
    output["fact_di"] = ca_cal.fact_di()
    output["ca_inj_flame"] = ca_cal.ca_inj_flame()
    output["ca_final"] = ca_cal.ca_final()
    output["ca_inj_toxic"] = ca_cal.ca_inj_tox()
    output["ca_inj_ntnf"] = ca_cal.ca_inj_nfnt()
    output["fact_mit"] = ca_cal.fact_mit()
    output["fact_ait"] = ca_cal.fact_ait()
    output["ca_cmd"] = ca_cal.ca_cmd()
    output["ca_inj"] = ca_cal.ca_inj()
    output["fc_cmd"] = ca_cal.fc_cmd()
    output["fc_affa"] = ca_cal.fc_affa()
    output["fc_envi"] = ca_cal.fc_environ()
    output["fc_prod"] = ca_cal.fc_prod()
    output["fc_inj"] = ca_cal.fc_inj()

    output["auto_ignition"] = ca_cal.auto_ignition_temp()
    output["ideal_gas"] = ca_cal.C_P()
    output["ideal_gas_ratio"] = ca_cal.ideal_gas_ratio()
    output["liquid_density"] = ca_cal.liquid_density()
    output["ambient"] = ca_cal.ambient()
    output["mw"] = ca_cal.moleculer_weight()
    output["nbp"] = ca_cal.NBP()
    output["model_fluid_type"] = ca_cal.model_fluid_type()

    # output["fc_total"] = fullcof.FC_total()
    # output["fcof_category"] = fullcof.FC_Category()
    # output.get("fcof_category")


# dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
#                        Commissiondate=rwassessment.commisstiondate,
#                        AssessmentDate=rwassessment.assessmentdate,
#                        APIComponentType=models.ApiComponentType.objects.get(
#     apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
#     Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
#     CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
#     CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
#     CladdingCorrosionRate=rwcoat.claddingcorrosionrate, CladdingThickness=rwcoat.claddingthickness,
#     InternalCladding=bool(rwcoat.internalcladding),
#     OnlineMonitoring=rwequipment.onlinemonitoring,
#     HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
#     ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
#     LinningType=rwcoat.internallinertype,
#     LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
#     LINNER_CONDITION=rwcoat.internallinercondition,
#     INTERNAL_LINNING=bool(rwcoat.internallining),
#     HEAT_TREATMENT=rwmaterial.heattreatment,
#     NaOHConcentration=rwstream.naohconcentration,
#     HEAT_TRACE=bool(rwequipment.heattraced),
#     STEAM_OUT=bool(rwequipment.steamoutwaterflush),
#     AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
#     AMINE_SOLUTION=rwstream.aminesolution,
#     ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
#     AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
#     AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
#     H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
#     PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
#     SULFUR_CONTENT=rwmaterial.sulfurcontent,
#     CO3_CONTENT=rwstream.co3concentration,
#     PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
#     EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
#     ExposedSH2OOperation=bool(
#                            rwequipment.presencesulphideso2),
#     ExposedSH2OShutdown=bool(
#                            rwequipment.presencesulphideso2shutdown),
#     ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
#     DOWNTIME_PROTECTED=bool(
#                            rwequipment.downtimeprotectionused),
#     INTERNAL_EXPOSED_FLUID_MIST=bool(
#                            rwstream.materialexposedtoclint),
#     EXTERNAL_EXPOSED_FLUID_MIST=bool(
#                            rwequipment.materialexposedtoclext),
#     CHLORIDE_ION_CONTENT=rwstream.chloride,
#     HF_PRESENT=bool(rwstream.hydrofluoric),
#     INTERFACE_SOIL_WATER=bool(
#                            rwequipment.interfacesoilwater),
#     SUPPORT_COATING=bool(
#                            rwcoat.supportconfignotallowcoatingmaint),
#     INSULATION_TYPE=rwcoat.externalinsulationtype,
#     CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
#     CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
#     CUI_PERCENT_5=rwexcor.plus71toplus107,
#     CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
#     CUI_PERCENT_8=rwexcor.plus135toplus162,
#     CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
#     EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
#     COMPONENT_INSTALL_DATE=rwassessment.commisstiondate,
#     CRACK_PRESENT=bool(rwcomponent.crackspresent),
#     EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
#     EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
#     PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
#     INSULATION_CONDITION=rwcoat.insulationcondition,
#     INSULATION_CHLORIDE=bool(
#                            rwcoat.insulationcontainschloride),
#     MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
#     HTHA_MATERIAL=rwmaterial.hthamaterialcode,
#     # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
#     HTHA_PRESSURE=rwstream.h2spartialpressure,
#     CRITICAL_TEMP=rwstream.criticalexposuretemperature,
#     DAMAGE_FOUND=bool(
#     rwcomponent.damagefoundinspection),
#     LOWEST_TEMP=bool(
#     rwequipment.yearlowestexptemp),
#     TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
#     BRITTLE_THICK=rwcomponent.brittlefracturethickness,
#     CARBON_ALLOY=bool(
#     rwmaterial.carbonlowalloy),
#     DELTA_FATT=rwcomponent.deltafatt,
#     MAX_OP_TEMP=rwstream.maxoperatingtemperature,
#     CHROMIUM_12=bool(
#     rwmaterial.chromemoreequal12),
#     MIN_OP_TEMP=rwstream.minoperatingtemperature,
#     MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
#     Hydrogen=rwstream.hydrogen,
#     REF_TEMP=rwmaterial.referencetemperature,
#     AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
#     EquipmentType=models.EquipmentType.objects.get(
#     equipmenttypeid=models.EquipmentMaster.objects.get(
#         equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
#     PREVIOUS_FAIL=rwcomponent.previousfailures,
#     AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
#     CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
#     CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
#     PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
#     BRANCH_DIAMETER=rwcomponent.branchdiameter, TensileStrengthDesignTemp=rwmaterial.tensilestrength,
#     StructuralThickness=rwcomponent.structuralthickness, MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
#     WeldJonintEfficiency=rwcomponent.weldjointefficiency, AllowableStress=rwcomponent.allowablestress,
#     YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
#     ShapeFactor=comptype.shapefactor, CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
#     PRESSSURE_CONTROL=bool(
#     rwequipment.pressurisationcontrolled),
#     FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel), EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
#     NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions), CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
#     CYCLIC_SERVICE=bool(rwcomponent.cyclicservice), EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
#     MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)

# dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
#                                    Commissiondate=rwassessment.commisstiondate,
#                                    AssessmentDate=rwassessment.assessmentdate,
#                                    APIComponentType=models.ApiComponentType.objects.get(
#                                    apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
#                                    Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
#                                    CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
#                                    CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
#                                    CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
#                                    InternalCladding=bool(rwcoat.internalcladding),
#                                    OnlineMonitoring=rwequipment.onlinemonitoring,
#                                    HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
#                                    ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
#                                    LinningType=rwcoat.internallinertype,
#                                    LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
#                                    LINNER_CONDITION=rwcoat.internallinercondition,
#                                    INTERNAL_LINNING=bool(rwcoat.internallining),
#                                    HEAT_TREATMENT=rwmaterial.heattreatment,
#                                    NaOHConcentration=rwstream.naohconcentration,
#                                    HEAT_TRACE=bool(rwequipment.heattraced),
#                                    STEAM_OUT=bool(rwequipment.steamoutwaterflush),
#                                    AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
#                                    AMINE_SOLUTION=rwstream.aminesolution,
#                                    ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
#                                    AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
#                                    AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
#                                    H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
#                                    PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
#                                    SULFUR_CONTENT=rwmaterial.sulfurcontent,
#                                    CO3_CONTENT=rwstream.co3concentration,
#                                    PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
#                                    EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
#                                    Hydrogen= rwstream.hydrogen,
#                                    ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
#                                    ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
#                                    ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
#                                    DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
#                                    INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
#                                    EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
#                                    CHLORIDE_ION_CONTENT=rwstream.chloride,
#                                    HF_PRESENT=bool(rwstream.hydrofluoric),
#                                    INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
#                                    SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
#                                    INSULATION_TYPE=rwcoat.externalinsulationtype,
#                                    CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
#                                    CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
#                                    CUI_PERCENT_5=rwexcor.plus71toplus107,
#                                    CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
#                                    CUI_PERCENT_8=rwexcor.plus135toplus162,
#                                    CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
#                                    EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
#                                    COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
#                                    CRACK_PRESENT=bool(rwcomponent.crackspresent),
#                                    EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
#                                    EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
#                                    PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
#                                    INSULATION_CONDITION=rwcoat.insulationcondition,
#                                    INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
#                                    MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
#                                    HTHA_MATERIAL=rwmaterial.hthamaterialcode,
#                                    # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
#                                    HTHA_PRESSURE=rwstream.h2spartialpressure,
#                                    CRITICAL_TEMP=rwstream.criticalexposuretemperature,
#                                    DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
#                                    LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
#                                    TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
#                                    BRITTLE_THICK=rwcomponent.brittlefracturethickness,
#                                    CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
#                                    DELTA_FATT=rwcomponent.deltafatt,
#                                    MAX_OP_TEMP=rwstream.maxoperatingtemperature,
#                                    CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
#                                    MIN_OP_TEMP=rwstream.minoperatingtemperature,
#                                    MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
#                                    REF_TEMP=rwmaterial.referencetemperature,
#                                    AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
#                                    EquipmentType=models.EquipmentType.objects.get(
#                                        equipmenttypeid=models.EquipmentMaster.objects.get(
#                                            equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
#                                    PREVIOUS_FAIL=rwcomponent.previousfailures,
#                                    AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
#                                    CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
#                                    CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
#                                    PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
#                                    BRANCH_DIAMETER=rwcomponent.branchdiameter, TensileStrengthDesignTemp=rwmaterial.tensilestrength,
#                                    StructuralThickness=rwcomponent.structuralthickness, MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
#                                    WeldJonintEfficiency=rwcomponent.weldjointefficiency, AllowableStress=rwcomponent.allowablestress,
#                                    YeildStrengthDesignTemp=rwmaterial.yieldstrength,Pressure=rwmaterial.designpressure,
#                                    ShapeFactor=comptype.shapefactor,CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
#                                    PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
#                                    FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
#                                    NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
#                                    CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
#                                    MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)

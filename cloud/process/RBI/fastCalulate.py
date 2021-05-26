import os,sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from cloud import models
from cloud.process.RBI import Postgresql
from cloud.process.RBI import DM_CAL as DM_CAL
from cloud.process.RBI import CA_CAL
from cloud.process.RBI import pofConvert
from cloud.process.RBI import CO_CAL
from cloud.process.RBI import CA_Flammable
from cloud.process.RBI import ToxicConsequenceArea
from cloud.process.RBI import FinancialCOF,mitigation
from cloud.process.RBI import CA_CAL_LV2
from cloud.process.WebUI import date2Str

# def SaveReCalculateResult(rwassessment, proposalID, riskList, nameField):
#     #nameField = risk
#     chart = models.RwDataChart.objects.filter(id=proposalID)
#     dmChart = models.RwDataDMFactor.objects.filter(id=proposalID)
#     pofChart = models.RwDataChartPoF.objects.filter(id=proposalID)
#     if(nameField == 'risk'):
#         chartData = models.RwDataChart.objects.get(id=proposalID)
#     elif(nameField == 'df_factor'):
#         chartData = models.RwDataDMFactor.objects.get(id=proposalID)
#     else:
#         chartData = models.RwDataChartPoF.objects.get(id=proposalID) #pof
#     if chart.count() != 0:
#             chartData = models.RwDataChart.objects.get(id=proposalID)
#             chartData.risktarget = riskList[0][nameField]
#             chartData.riskage1 = riskList[1][nameField]
#             chartData.riskage2 = riskList[2][nameField]
#             chartData.riskage3 = riskList[3][nameField]
#             chartData.riskage4 = riskList[4][nameField]
#             chartData.riskage5 = riskList[5][nameField]
#             chartData.riskage6 = riskList[6][nameField]
#             chartData.riskage7 = riskList[7][nameField]
#             chartData.riskage8 = riskList[8][nameField]
#             chartData.riskage9 = riskList[9][nameField]
#             chartData.riskage10 = riskList[10][nameField]
#             chartData.riskage11 = riskList[11][nameField]
#             chartData.riskage12 = riskList[12][nameField]
#             chartData.riskage13 = riskList[13][nameField]
#             chartData.riskage14 = riskList[14][nameField]
#             chartData.riskage15 = riskList[15][nameField]
#             chartData.riskage16 = riskList[16][nameField]
#             chartData.riskage17 = riskList[17][nameField]
#             chartData.riskage18 = riskList[18][nameField]
#             chartData.riskage19 = riskList[19][nameField]
#             chartData.riskage20 = riskList[20][nameField]
#             chartData.riskage21 = riskList[21][nameField]
#             chartData.riskage22 = riskList[22][nameField]
#             chartData.riskage23 = riskList[23][nameField]
#             chartData.riskage24 = riskList[24][nameField]
#             chartData.riskage25 = riskList[25][nameField]
#             chartData.riskage26 = riskList[26][nameField]
#             chartData.riskage27 = riskList[27][nameField]
#             chartData.riskage28 = riskList[28][nameField] 
#             chartData.save()
#     else:
#         chartData = models.RwDataChart(id=rwassessment, riskage1=riskList[1][nameField],
#                                         riskage2=riskList[2][nameField],
#                                         riskage3=riskList[3][nameField],
#                                         riskage4=riskList[4][nameField], riskage5=riskList[5][nameField],
#                                         riskage6=riskList[6][nameField],
#                                         riskage7=riskList[7][nameField],
#                                         riskage8=riskList[8][nameField], riskage9=riskList[9][nameField],
#                                         riskage10=riskList[10][nameField],
#                                         riskage11=riskList[11][nameField],
#                                         riskage12=riskList[12][nameField], riskage13=riskList[13][nameField],
#                                         riskage14=riskList[14][nameField],
#                                         riskage15=riskList[15][nameField], riskage16=riskList[16][nameField],
#                                         riskage17=riskList[17][nameField],
#                                         riskage18=riskList[18][nameField], riskage19=riskList[19][nameField],
#                                         riskage20=riskList[20][nameField],
#                                         riskage21=riskList[21][nameField], riskage22=riskList[22][nameField],
#                                         riskage23=riskList[23][nameField],
#                                         riskage24=riskList[24][nameField], riskage25=riskList[25][nameField],
#                                         riskage26=riskList[26][nameField], riskage27=riskList[27][nameField],
#                                         riskage28=riskList[28][nameField], risktarget=riskList[0][nameField])
#         chartData.save()
#     return 0

def CheckSite(request):
    try:
        if request.session['kind'] == 'factory':
            UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
            # print("check site")
            # print("userid",UserID)
            toemail = models.ZUser.objects.get(id = UserID).email_service
            # print(toemail)
            return toemail
    except Exception as e:
        print(e)
def calulateRiskChartTank(proposalID):
    listDamage = []
    DF_EXT_TOTAL_API = []
    DF_THINNING_TOTAL_API = []
    DF_SSC_TOTAL_API = []
    DF_HTHA_API = []
    DF_BRIT_TOTAL_API = []
    DF_PIPE_API = []
    rwassessment = models.RwAssessment.objects.get(id=proposalID)
    rwequipment = models.RwEquipment.objects.get(id=proposalID)
    rwcomponent = models.RwComponent.objects.get(id=proposalID)
    rwstream = models.RwStream.objects.get(id=proposalID)
    rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
    rwcoat = models.RwCoating.objects.get(id=proposalID)
    rwmaterial = models.RwMaterial.objects.get(id=proposalID)
    comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
    eq = models.EquipmentMaster.objects.get(equipmentid=rwassessment.equipmentid_id)
    # target = models.ComponentMaster.objects.get(facilityid=eq.facilityid_id)
    comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
    try:
        if not rwcoat.externalcoating:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   Hydrogen=rwstream.hydrogen,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation,
                                   TankMaintain653=rwequipment.tankismaintained,
                                   ComponentIsWeld=rwequipment.componentiswelded,
                                   AdjustmentSettle=rwequipment.adjustmentsettle)
        else:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   Hydrogen=rwstream.hydrogen,
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation,
                                   TankMaintain653=rwequipment.tankismaintained,
                                   ComponentIsWeld=rwequipment.componentiswelded,
                                   AdjustmentSettle=rwequipment.adjustmentsettle)
        for a in dm_cal.DF_RISK_CHART_THINNING():
            DF_THINNING_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_EXT():
            DF_EXT_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_SSC():
            DF_SSC_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_HTHA():
            DF_HTHA_API.append(a)
        for a in dm_cal.DF_RISK_CHART_BRIT():
            DF_BRIT_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_PIPE():
            DF_PIPE_API.append(a)
        listDamage = [DF_THINNING_TOTAL_API, DF_EXT_TOTAL_API, DF_SSC_TOTAL_API, DF_HTHA_API, DF_BRIT_TOTAL_API,
                      DF_PIPE_API]
    except Exception as e:
        print(e)
    return listDamage
def caculateRiskChart(proposalID):
    listDamage = []
    DF_EXT_TOTAL_API = []
    DF_THINNING_TOTAL_API = []
    DF_SSC_TOTAL_API = []
    DF_HTHA_API = []
    DF_BRIT_TOTAL_API = []
    DF_PIPE_API = []
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)

        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)

        if not rwcoat.externalcoating:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   Hydrogen=rwstream.hydrogen,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)
        else:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   Hydrogen=rwstream.hydrogen,
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)
        for a in dm_cal.DF_RISK_CHART_THINNING():
            DF_THINNING_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_EXT():
            DF_EXT_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_SSC():
            DF_SSC_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_HTHA():
            DF_HTHA_API.append(a)
        for a in dm_cal.DF_RISK_CHART_BRIT():
            DF_BRIT_TOTAL_API.append(a)
        for a in dm_cal.DF_RISK_CHART_PIPE():
            DF_PIPE_API.append(a)
        listDamage = [DF_THINNING_TOTAL_API, DF_EXT_TOTAL_API,DF_SSC_TOTAL_API,DF_HTHA_API,DF_BRIT_TOTAL_API,DF_PIPE_API]
    except Exception as e:
        print(e)
    return listDamage

def caculateCorrisionRate(proposalID):
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwcorrosionratetank = models.CorrosionRateTank.objects.filter(id_id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        for a in rwcorrosionratetank:
            co_cal = CO_CAL.CO_CAL(SoilResistivity=a.potentialcorrosion, ASTPADTYPE=a.tankpadmaterial,
                                   AST_DRAINAGE_TYPE=a.tankdrainagetype,
                                   CATHODIC_PROTECTION_TYPE=a.cathodicprotectiontype,
                                   AST_PAD_TYPE_BOTTOM=a.tankbottomtype,
                                   SoilSideTemperature=a.soilsidetemperature,
                                   PRODUCT_SIDE_CONDITION=a.productcondition,
                                   ProductSideTemp=a.productsidetemp, STRAM_COIL=a.steamcoil,
                                   WATER_DRAW_OFF=a.waterdrawoff, crpb=a.productsidecorrosionrate,
                                   ProductSideBottomCR=a.productsidebottom,crsb=a.soilsidecorrosionrate)
            co_cal.CR_S()
            # print(co_cal.CR_S())
            co_cal.CR_P()
            co_cal.FinalEstimated_CR()
            corri = models.CorrosionRateTank.objects.get(corrosionid=a.corrosionid)
            corri.modifiedsoilsidecorrosionrate = co_cal.CR_S()
            corri.modifiedproductsidecorrosionrate = co_cal.CR_P()
            corri.finalestimatedcorrosionrate = co_cal.FinalEstimated_CR()
            corri.save()
    except Exception as e:
        print("Exception at fast calculate")
        print(e)

def calculateNormal(proposalID,request):
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwinputca = models.RwInputCaLevel1.objects.get(id=proposalID)
        countRefullPOF = models.RwFullPof.objects.filter(id=proposalID)
        countCalv1 = models.RwCaLevel1.objects.filter(id=proposalID)
        rwcofholesize = models.RwFullCoFHoleSize.objects.filter(id=proposalID)
        damageMachinsm = models.RwDamageMechanism.objects.filter(id_dm=proposalID)
        countRefullfc = models.RwFullFcof.objects.filter(id=proposalID)
        chart = models.RwDataChart.objects.filter(id=proposalID)
        dmChart = models.RwDataDMFactor.objects.filter(id=proposalID)
        pofChart = models.RwDataChartPoF.objects.filter(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        # target = models.FacilityRiskTarget.objects.get(
        #     facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
        datafaci = models.Facility.objects.get(
            facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        try:
            if not rwassessment.commisstiondate:
                rwassessment.commisstiondate = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).commissiondate
                rwassessment.save()
        except:
            print(e)
        if not rwcoat.externalcoating:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=rwassessment.commisstiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwassessment.commisstiondate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   Hydrogen=rwstream.hydrogen,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter, TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness, MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency, AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength,Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)
        else:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=rwassessment.commisstiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                   apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   Hydrogen= rwstream.hydrogen,
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter, TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness, MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency, AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength,Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)
        ca_cal = CA_CAL.CA_NORMAL(NominalDiametter=rwcomponent.nominaldiameter,
                                  MATERIAL_COST=rwmaterial.costfactor, FLUID=rwinputca.api_fluid,
                                  FLUID_PHASE=rwstream.storagephase,
                                  MAX_OPERATING_TEMP=rwstream.maxoperatingtemperature,
                                  API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(
                                      apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                  DETECTION_TYPE=rwinputca.detection_type,
                                  ISOLATION_TYPE=rwinputca.isulation_type,
                                  STORED_PRESSURE=rwstream.maxoperatingpressure*1000,
                                  ATMOSPHERIC_PRESSURE=101.325, STORED_TEMP=rwstream.minoperatingtemperature ,
                                  MASS_INVERT=rwinputca.mass_inventory,
                                  MASS_COMPONENT=rwinputca.mass_component,
                                  MITIGATION_SYSTEM=rwinputca.mitigation_system,
                                  TOXIC_PERCENT=rwinputca.toxic_percent,
                                  RELEASE_DURATION=rwinputca.release_duration,
                                  PRODUCTION_COST=rwinputca.production_cost, TOXIC_FLUID=rwinputca.toxic_fluid,
                                  INJURE_COST=rwinputca.injure_cost, ENVIRON_COST=rwinputca.evironment_cost,
                                  PERSON_DENSITY=rwinputca.personal_density,
                                  EQUIPMENT_COST=rwinputca.equipment_cost)

        TOTAL_DF_API1 = dm_cal.DF_TOTAL_API(0)
        TOTAL_DF_API2 = dm_cal.DF_TOTAL_API(3)
        TOTAL_DF_API3 = dm_cal.DF_TOTAL_API(6)

        TOTAL_DF_GENERAL_1 = dm_cal.DF_TOTAL_GENERAL(0)
        TOTAL_DF_GENERAL_2 = dm_cal.DF_TOTAL_GENERAL(3)
        TOTAL_DF_GENERAL_3 = dm_cal.DF_TOTAL_GENERAL(6)

        gffTotal = models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).gfftotal
        pofap1 = pofConvert.convert(TOTAL_DF_API1 * datafaci.managementfactor * gffTotal)
        pofap2 = pofConvert.convert(TOTAL_DF_API2 * datafaci.managementfactor * gffTotal)
        pofap3 = pofConvert.convert(TOTAL_DF_API3 * datafaci.managementfactor * gffTotal)

        pof_general_ap1 = pofConvert.convert(TOTAL_DF_GENERAL_1 * datafaci.managementfactor * gffTotal)
        pof_general_ap2 = pofConvert.convert(TOTAL_DF_GENERAL_2 * datafaci.managementfactor * gffTotal)
        pof_general_ap3 = pofConvert.convert(TOTAL_DF_GENERAL_3 * datafaci.managementfactor * gffTotal)
        # full pof
        if countRefullPOF.count() != 0:
            refullPOF = models.RwFullPof.objects.get(id=proposalID)
            refullPOF.thinningap1 = dm_cal.DF_THINNING_TOTAL_API(0)
            refullPOF.thinningap2 = dm_cal.DF_THINNING_TOTAL_API(3)
            refullPOF.thinningap3 = dm_cal.DF_THINNING_TOTAL_API(6)
            refullPOF.sccap1 = dm_cal.DF_SSC_TOTAL_API(0)
            refullPOF.sccap2 = dm_cal.DF_SSC_TOTAL_API(3)
            refullPOF.sccap3 = dm_cal.DF_SSC_TOTAL_API(6)
            refullPOF.externalap1 = dm_cal.DF_EXT_TOTAL_API(0)
            refullPOF.externalap2 = dm_cal.DF_EXT_TOTAL_API(3)
            refullPOF.externalap3 = dm_cal.DF_EXT_TOTAL_API(6)
            refullPOF.brittleap1 = dm_cal.DF_BRIT_TOTAL_API(0)
            refullPOF.brittleap2 = dm_cal.DF_BRIT_TOTAL_API(3)
            refullPOF.brittleap3 = dm_cal.DF_BRIT_TOTAL_API(6)
            refullPOF.htha_ap1 = dm_cal.DF_HTHA_API(0)
            refullPOF.htha_ap2 = dm_cal.DF_HTHA_API(3)
            refullPOF.htha_ap3 = dm_cal.DF_HTHA_API(6)
            refullPOF.fatigueap1 = dm_cal.DF_PIPE_API(0)
            refullPOF.fatigueap2 = dm_cal.DF_PIPE_API(3)
            refullPOF.fatigueap3 = dm_cal.DF_PIPE_API(6)
            refullPOF.fms = datafaci.managementfactor
            refullPOF.thinninglocalap1 = max(dm_cal.DF_THINNING_TOTAL_API(0),
                                             dm_cal.DF_EXT_TOTAL_API(0))
            refullPOF.thinninglocalap2 = max(dm_cal.DF_THINNING_TOTAL_API(3),
                                             dm_cal.DF_EXT_TOTAL_API(3))
            refullPOF.thinninglocalap3 = max(dm_cal.DF_THINNING_TOTAL_API(6),
                                             dm_cal.DF_EXT_TOTAL_API(6))
            refullPOF.thinninggeneralap1 = dm_cal.DF_THINNING_TOTAL_API(0) + dm_cal.DF_EXT_TOTAL_API(0)
            refullPOF.thinninggeneralap2 = dm_cal.DF_THINNING_TOTAL_API(3) + dm_cal.DF_EXT_TOTAL_API(3)
            refullPOF.thinninggeneralap3 = dm_cal.DF_THINNING_TOTAL_API(6) + dm_cal.DF_EXT_TOTAL_API(6)
            if refullPOF.thinningtype == "General":
                refullPOF.totaldfap1 = TOTAL_DF_GENERAL_1
                refullPOF.totaldfap2 = TOTAL_DF_GENERAL_2
                refullPOF.totaldfap3 = TOTAL_DF_GENERAL_3
                refullPOF.pofap1 = pof_general_ap1
                refullPOF.pofap2 = pof_general_ap2
                refullPOF.pofap3 = pof_general_ap3
                refullPOF.pofap1category = dm_cal.PoFCategory(TOTAL_DF_GENERAL_1)
                refullPOF.pofap2category = dm_cal.PoFCategory(TOTAL_DF_GENERAL_2)
                refullPOF.pofap3category = dm_cal.PoFCategory(TOTAL_DF_GENERAL_3)
            else:
                refullPOF.thinningtype = "Local"
                refullPOF.totaldfap1 = TOTAL_DF_API1
                refullPOF.totaldfap2 = TOTAL_DF_API2
                refullPOF.totaldfap3 = TOTAL_DF_API3
                refullPOF.pofap1 = pofap1
                refullPOF.pofap2 = pofap2
                refullPOF.pofap3 = pofap3
                refullPOF.pofap1category = dm_cal.PoFCategory(TOTAL_DF_API1)
                refullPOF.pofap2category = dm_cal.PoFCategory(TOTAL_DF_API2)
                refullPOF.pofap3category = dm_cal.PoFCategory(TOTAL_DF_API3)
            refullPOF.gfftotal = gffTotal
            refullPOF.save()
        else:
            refullPOF = models.RwFullPof(id=rwassessment, thinningap1=dm_cal.DF_THINNING_TOTAL_API(0),
                                         thinningap2=dm_cal.DF_THINNING_TOTAL_API(3),
                                         thinningap3=dm_cal.DF_THINNING_TOTAL_API(6),
                                         sccap1=dm_cal.DF_SSC_TOTAL_API(0), sccap2=dm_cal.DF_SSC_TOTAL_API(3),
                                         sccap3=dm_cal.DF_SSC_TOTAL_API(6),
                                         externalap1=dm_cal.DF_EXT_TOTAL_API(0),
                                         externalap2=dm_cal.DF_EXT_TOTAL_API(3),
                                         externalap3=dm_cal.DF_EXT_TOTAL_API(6),
                                         brittleap1=dm_cal.DF_BRIT_TOTAL_API(0),
                                         brittleap2=dm_cal.DF_BRIT_TOTAL_API(3),
                                         brittleap3=dm_cal.DF_BRIT_TOTAL_API(6),
                                         htha_ap1=dm_cal.DF_HTHA_API(0), htha_ap2=dm_cal.DF_HTHA_API(3),
                                         htha_ap3=dm_cal.DF_HTHA_API(6),
                                         fatigueap1=dm_cal.DF_PIPE_API(0), fatigueap2=dm_cal.DF_PIPE_API(3),
                                         fatigueap3=dm_cal.DF_PIPE_API(6),
                                         fms=datafaci.managementfactor, thinningtype="Local",
                                         thinninglocalap1=max(dm_cal.DF_THINNING_TOTAL_API(0),
                                                              dm_cal.DF_EXT_TOTAL_API(0)),
                                         thinninglocalap2=max(dm_cal.DF_THINNING_TOTAL_API(3),
                                                              dm_cal.DF_EXT_TOTAL_API(3)),
                                         thinninglocalap3=max(dm_cal.DF_THINNING_TOTAL_API(6),
                                                              dm_cal.DF_EXT_TOTAL_API(6)),
                                         thinninggeneralap1=dm_cal.DF_THINNING_TOTAL_API(
                                             0) + dm_cal.DF_EXT_TOTAL_API(0),
                                         thinninggeneralap2=dm_cal.DF_THINNING_TOTAL_API(
                                             3) + dm_cal.DF_EXT_TOTAL_API(3),
                                         thinninggeneralap3=dm_cal.DF_THINNING_TOTAL_API(
                                             6) + dm_cal.DF_EXT_TOTAL_API(6),
                                         totaldfap1=TOTAL_DF_API1, totaldfap2=TOTAL_DF_API2,
                                         totaldfap3=TOTAL_DF_API3,
                                         pofap1=pofap1, pofap2=pofap2, pofap3=pofap3, gfftotal=gffTotal,
                                         pofap1category=dm_cal.PoFCategory(TOTAL_DF_API1),
                                         pofap2category=dm_cal.PoFCategory(TOTAL_DF_API2),
                                         pofap3category=dm_cal.PoFCategory(TOTAL_DF_API3))

            refullPOF.save()
        # ca level 1( CoF)
        try:
            if rwcofholesize.count() != 0:
                rwholesize = models.RwFullCoFHoleSize.objects.get(id=proposalID)

                rwholesize.gff_small = ca_cal.gff(1)
                rwholesize.gff_medium = ca_cal.gff(2)
                rwholesize.gff_large = ca_cal.gff(3)
                rwholesize.gff_rupture = ca_cal.gff(4)
                rwholesize.an_small = ca_cal.a_n(1)
                rwholesize.an_medium = ca_cal.a_n(2)
                rwholesize.an_large = ca_cal.a_n(3)
                rwholesize.an_rupture = ca_cal.a_n(4)
                rwholesize.wn_small = ca_cal.W_n(1)
                rwholesize.wn_medium = ca_cal.W_n(2)
                rwholesize.wn_large = ca_cal.W_n(3)
                rwholesize.wn_rupture = ca_cal.W_n(4)
                rwholesize.mass_add_n_small = ca_cal.mass_addn(1)
                rwholesize.mass_add_n_medium = ca_cal.mass_addn(2)
                rwholesize.mass_add_n_large = ca_cal.mass_addn(3)
                rwholesize.mass_add_n_rupture = ca_cal.mass_addn(4)
                rwholesize.mass_avail_n_small = ca_cal.mass_avail_n(1)
                rwholesize.mass_avail_n_medium = ca_cal.mass_avail_n(2)
                rwholesize.mass_avail_n_large = ca_cal.mass_avail_n(3)
                rwholesize.mass_avail_n_rupture = ca_cal.mass_avail_n(4)
                rwholesize.t_n_small = ca_cal.t_n(1)
                rwholesize.t_n_medium = ca_cal.t_n(2)
                rwholesize.t_n_large = ca_cal.t_n(3)
                rwholesize.t_n_rupture = ca_cal.t_n(4)
                rwholesize.releasetype_small = ca_cal.releaseType(1)
                rwholesize.releasetype_medium = ca_cal.releaseType(2)
                rwholesize.releasetype_large = ca_cal.releaseType(3)
                rwholesize.releasetype_rupture = ca_cal.releaseType(4)
                rwholesize.ld_max_n_small = ca_cal.ld_n_max(1)
                rwholesize.ld_max_n_medium = ca_cal.ld_n_max(2)
                rwholesize.ld_max_n_large = ca_cal.ld_n_max(3)
                rwholesize.ld_max_n_rupture = ca_cal.ld_n_max(4)
                rwholesize.rate_n_small = ca_cal.rate_n(1)
                rwholesize.rate_n_medium = ca_cal.rate_n(2)
                rwholesize.rate_n_large = ca_cal.rate_n(3)
                rwholesize.rate_n_rupture = ca_cal.rate_n(4)
                rwholesize.ld_n_small = ca_cal.ld_n(1)
                rwholesize.ld_n_medium = ca_cal.ld_n(2)
                rwholesize.ld_n_large = ca_cal.ld_n(3)
                rwholesize.ld_n_rupture = ca_cal.ld_n(4)
                rwholesize.mass_n_small = ca_cal.mass_n(1)
                rwholesize.mass_n_medium = ca_cal.mass_n(2)
                rwholesize.mass_n_large = ca_cal.mass_n(3)
                rwholesize.mass_n_rupture = ca_cal.mass_n(4)
                rwholesize.eneff_n_small = ca_cal.eneff_n(1)
                rwholesize.eneff_n_medium = ca_cal.eneff_n(2)
                rwholesize.eneff_n_large = ca_cal.eneff_n(3)
                rwholesize.eneff_n_rupture = ca_cal.eneff_n(4)
                rwholesize.factIC_n_small = ca_cal.fact_n_ic(1)
                rwholesize.factIC_n_medium = ca_cal.fact_n_ic(2)
                rwholesize.factIC_n_large = ca_cal.fact_n_ic(3)
                rwholesize.factIC_n_rupture = ca_cal.fact_n_ic(4)
                rwholesize.save()
                calv1list = models.RwCaLevel1.objects.filter(id=proposalID)
                if calv1list.count() != 0:
                    calv1 = models.RwCaLevel1.objects.get(id=proposalID)
                    # if ca_cal.NominalDiametter == 0 or ca_cal.STORED_PRESSURE == 0 or ca_cal.MASS_INVERT == 0 or ca_cal.MASS_COMPONENT == 0 or ca_cal.FLUID is None:
                    #     print('vao if 0')
                    #     calv1.save()
                    # else:
                    print('vao day')
                    toxic_fluid = rwinputca.toxic_fluid
                    phase_fluid_storage = rwstream.storagephase
                    api_com_type = models.ApiComponentType.objects.get(
                        apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
                    toxic_fluid_percentage = rwinputca.toxic_percent
                    model_fluid = rwinputca.api_fluid
                    MATERIAL_COST = rwmaterial.costfactor
                    store_pressure = rwstream.maxoperatingpressure
                    caflammable = CA_Flammable.CA_Flammable(model_fluid, phase_fluid_storage,
                                                            rwinputca.mitigation_system, proposalID,
                                                            rwstream.maxoperatingtemperature,
                                                            api_com_type, toxic_fluid_percentage, toxic_fluid)
                    catoxic = ToxicConsequenceArea.CA_Toxic(proposalID, rwinputca.toxic_fluid,
                                                            caflammable.ReleasePhase(),
                                                            toxic_fluid_percentage, api_com_type, model_fluid,
                                                            store_pressure)
                    CA_cmd = caflammable.CA_Flam_Cmd()
                    # print(caflammable.CA_Flam_inj())
                    # print(caflammable.CA_Flam_inj_toxic())
                    # print(catoxic.CA_toxic_inj())
                    # print(catoxic.CA_toxic_inj2())
                    # print(catoxic.NoneCA_leck())
                    CA_inj = max(caflammable.CA_Flam_inj(), caflammable.CA_Flam_inj_toxic(), catoxic.CA_toxic_inj(),
                                 catoxic.CA_toxic_inj2(), catoxic.NoneCA_leck())
                    fullcof = FinancialCOF.FinancialCOF(proposalID, model_fluid, toxic_fluid,
                                                        toxic_fluid_percentage, api_com_type,
                                                        MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                        rwinputca.mitigation_system,
                                                        rwstream.maxoperatingtemperature, store_pressure)
                    calv1.release_phase = ca_cal.ReleasePhase()
                    calv1.fact_di = ca_cal.fact_di()
                    calv1.ca_inj_flame = ca_cal.ca_inj_flame()
                    calv1.ca_final = ca_cal.ca_final()
                    calv1.ca_inj_toxic = ca_cal.ca_inj_tox()
                    calv1.ca_inj_ntnf = ca_cal.ca_inj_nfnt()
                    calv1.fact_mit = ca_cal.fact_mit()
                    calv1.fact_ait = ca_cal.fact_ait()
                    calv1.ca_cmd = max(ca_cal.ca_cmd(), ca_cal.ca_inj())
                    calv1.fc_cmd = ca_cal.fc_cmd()
                    calv1.fc_affa = ca_cal.fc_affa()
                    calv1.fc_envi = ca_cal.fc_environ()
                    calv1.fc_prod = ca_cal.fc_prod()
                    calv1.fc_inj = ca_cal.fc_inj()

                    calv1.auto_ignition = ca_cal.auto_ignition_temp()
                    calv1.ideal_gas = ca_cal.C_P()
                    calv1.ideal_gas_ratio = ca_cal.ideal_gas_ratio()
                    calv1.liquid_density = ca_cal.liquid_density()
                    calv1.ambient = ca_cal.ambient()
                    calv1.mw = ca_cal.moleculer_weight()
                    calv1.nbp = ca_cal.NBP()
                    calv1.model_fluid_type = ca_cal.model_fluid_type()
                    # calv1.toxic_fluid_type = ca_cal.toxic_fluid_type()
                    calv1.fc_total = fullcof.FC_total()
                    calv1.fcof_category = fullcof.FC_Category()
                    calv1.save()
                else:
                    toxic_fluid = rwinputca.toxic_fluid
                    phase_fluid_storage = rwstream.storagephase
                    api_com_type = models.ApiComponentType.objects.get(
                        apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
                    toxic_fluid_percentage = rwinputca.toxic_percent
                    model_fluid = rwinputca.api_fluid
                    MATERIAL_COST = rwmaterial.costfactor
                    store_pressure = rwstream.maxoperatingpressure
                    caflammable = CA_Flammable.CA_Flammable(model_fluid, phase_fluid_storage,
                                                            rwinputca.mitigation_system, proposalID,
                                                            rwstream.maxoperatingtemperature,
                                                            api_com_type, toxic_fluid_percentage, toxic_fluid)
                    catoxic = ToxicConsequenceArea.CA_Toxic(proposalID, rwinputca.toxic_fluid,
                                                            caflammable.ReleasePhase(),
                                                            toxic_fluid_percentage, api_com_type, model_fluid,
                                                            store_pressure)
                    CA_cmd = caflammable.CA_Flam_Cmd()
                    # print(caflammable.CA_Flam_inj())
                    # print(caflammable.CA_Flam_inj_toxic())
                    # print(catoxic.CA_toxic_inj())
                    # print(catoxic.CA_toxic_inj2())
                    # print(catoxic.NoneCA_leck())
                    CA_inj = max(caflammable.CA_Flam_inj(), caflammable.CA_Flam_inj_toxic(), catoxic.CA_toxic_inj(),
                                 catoxic.CA_toxic_inj2(), catoxic.NoneCA_leck())
                    fullcof = FinancialCOF.FinancialCOF(proposalID, model_fluid, toxic_fluid,
                                                        toxic_fluid_percentage, api_com_type,
                                                        MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                        rwinputca.mitigation_system,
                                                        rwstream.maxoperatingtemperature, store_pressure)
                    if (model_fluid is None):
                        calv1 = models.RwCaLevel1(id=rwassessment, release_phase=ca_cal.GET_RELEASE_PHASE(),
                                                  fact_di=ca_cal.fact_di(), fact_mit=ca_cal.fact_mit(),
                                                  fact_ait=ca_cal.fact_ait(), ca_cmd=ca_cal.ca_cmd(),
                                                  ca_inj_flame=ca_cal.ca_inj_flame(), ca_inj_toxic=ca_cal.ca_inj_tox(),
                                                  ca_inj_ntnf=ca_cal.ca_inj_nfnt(), fc_cmd=ca_cal.fc_cmd(),
                                                  fc_affa=ca_cal.fc_affa(), fc_prod=ca_cal.fc_prod(),
                                                  fc_inj=ca_cal.fc_inj(),
                                                  fc_total=100000000,
                                                  fcof_category='E',
                                                  ca_final=ca_cal.ca_final(), auto_ignition=ca_cal.auto_ignition_temp(),
                                                  ideal_gas=ca_cal.C_P(), ideal_gas_ratio=0,
                                                  liquid_density=0, ambient=0,
                                                  mw=0,
                                                  nbp=0,
                                                  model_fluid_type='')  # bo di toxic_fluid_type=ca_cal.toxic_fluid_type()
                        print('_____check 3______')
                        calv1.save()
                    else:
                        print('dieu kien cua model_fluid none')
                        calv1 = models.RwCaLevel1(id=rwassessment, release_phase=ca_cal.GET_RELEASE_PHASE(),
                                                  fact_di=ca_cal.fact_di(), fact_mit=ca_cal.fact_mit(),
                                                  fact_ait=ca_cal.fact_ait(), ca_cmd=ca_cal.ca_cmd(),
                                                  ca_inj_flame=ca_cal.ca_inj_flame(), ca_inj_toxic=ca_cal.ca_inj_tox(),
                                                  ca_inj_ntnf=ca_cal.ca_inj_nfnt(), fc_cmd=ca_cal.fc_cmd(),
                                                  fc_affa=ca_cal.fc_affa(), fc_prod=ca_cal.fc_prod(),
                                                  fc_inj=ca_cal.fc_inj(),
                                                  fc_total=fullcof.FC_total(),
                                                  fcof_category=fullcof.FC_Category(),
                                                  ca_final=ca_cal.ca_final(), auto_ignition=ca_cal.auto_ignition_temp(),
                                                  ideal_gas=ca_cal.C_P(), ideal_gas_ratio=ca_cal.ideal_gas_ratio(),
                                                  liquid_density=ca_cal.liquid_density(), ambient=ca_cal.ambient(),
                                                  mw=ca_cal.moleculer_weight(),
                                                  nbp=ca_cal.NBP(),
                                                  model_fluid_type='')  # bo di toxic_fluid_type=ca_cal.toxic_fluid_type()
                        print('_____check 6______')
                    calv1.save()
            else:
                rwholesize = models.RwFullCoFHoleSize(id=rwassessment, gff_small=ca_cal.gff(1),
                                                      gff_medium=ca_cal.gff(2),
                                                      gff_large=ca_cal.gff(3), gff_rupture=ca_cal.gff(4),
                                                      an_small=ca_cal.a_n(1),an_medium=ca_cal.a_n(2),
                                                      an_large=ca_cal.a_n(3),an_rupture=ca_cal.a_n(4),
                                                      wn_small=ca_cal.W_n(1),wn_medium=ca_cal.W_n(2),
                                                      wn_large=ca_cal.W_n(3),wn_rupture=ca_cal.W_n(4),
                                                      mass_add_n_small=ca_cal.mass_addn(1),mass_add_n_medium=ca_cal.mass_addn(2),
                                                      mass_add_n_large=ca_cal.mass_addn(3),mass_add_n_rupture=ca_cal.mass_addn(4),
                                                      mass_avail_n_small=ca_cal.mass_avail_n(1),
                                                      mass_avail_n_medium=ca_cal.mass_avail_n(2),mass_avail_n_large=ca_cal.mass_avail_n(3),
                                                      mass_avail_n_rupture=ca_cal.mass_avail_n(4),
                                                      t_n_small=ca_cal.t_n(1),t_n_medium=ca_cal.t_n(2),
                                                      t_n_large=ca_cal.t_n(3),t_n_rupture=ca_cal.t_n(4),
                                                      releasetype_small=ca_cal.releaseType(1),releasetype_medium=ca_cal.releaseType(2),
                                                      releasetype_large=ca_cal.releaseType(3),
                                                      releasetype_rupture=ca_cal.releaseType(4),ld_max_n_small=ca_cal.ld_n_max(1),
                                                      ld_max_n_medium=ca_cal.ld_n_max(2),ld_max_n_large=ca_cal.ld_n_max(3),
                                                      ld_max_n_rupture=ca_cal.ld_n_max(4),rate_n_small=ca_cal.rate_n(1),
                                                      rate_n_medium=ca_cal.rate_n(2),rate_n_large=ca_cal.rate_n(3),
                                                      rate_n_rupture=ca_cal.rate_n(4),
                                                      ld_n_small=ca_cal.ld_n(1),ld_n_medium=ca_cal.ld_n(2),
                                                      ld_n_large=ca_cal.ld_n(3),ld_n_rupture=ca_cal.ld_n(4),
                                                      mass_n_small=ca_cal.mass_n(1),mass_n_medium=ca_cal.mass_n(2),
                                                      mass_n_large=ca_cal.mass_n(3),mass_n_rupture=ca_cal.mass_n(4),
                                                      eneff_n_small = ca_cal.eneff_n(1),
                                                      eneff_n_medium = ca_cal.eneff_n(2),eneff_n_large = ca_cal.eneff_n(3),
                                                      eneff_n_rupture = ca_cal.eneff_n(4),factIC_n_small = ca_cal.fact_n_ic(1),
                                                      factIC_n_medium = ca_cal.fact_n_ic(2),factIC_n_large = ca_cal.fact_n_ic(3),
                                                      factIC_n_rupture = ca_cal.fact_n_ic(4))
                rwholesize.save()

                # if ca_cal.NominalDiametter == 0 or ca_cal.STORED_PRESSURE == 0 or ca_cal.MASS_INVERT == 0 or ca_cal.MASS_COMPONENT == 0 or ca_cal.FLUID is None:
                if ca_cal.NominalDiametter == 0 or ca_cal.STORED_PRESSURE == 0 or ca_cal.FLUID is None:
                    print("go 123")
                    print(ca_cal.STORED_PRESSURE)
                    print(ca_cal.MASS_INVERT)
                    print(ca_cal.MASS_COMPONENT)
                    calv1 = models.RwCaLevel1(id=rwassessment,fc_total=100000000, fcof_category="E")
                    calv1.save()
                else:
                    print("go 456")
                    toxic_fluid = rwinputca.toxic_fluid
                    phase_fluid_storage = rwstream.storagephase
                    api_com_type = models.ApiComponentType.objects.get(
                        apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
                    toxic_fluid_percentage = rwinputca.toxic_percent
                    model_fluid = rwinputca.api_fluid
                    MATERIAL_COST = rwmaterial.costfactor
                    store_pressure = rwstream.maxoperatingpressure
                    caflammable = CA_Flammable.CA_Flammable(model_fluid, phase_fluid_storage,
                                                            rwinputca.mitigation_system, proposalID,
                                                            rwstream.maxoperatingtemperature,
                                                            api_com_type, toxic_fluid_percentage, toxic_fluid)
                    catoxic = ToxicConsequenceArea.CA_Toxic(proposalID, rwinputca.toxic_fluid,
                                                            caflammable.ReleasePhase(),
                                                            toxic_fluid_percentage, api_com_type, model_fluid,
                                                            store_pressure)
                    CA_cmd = caflammable.CA_Flam_Cmd()
                    # print(caflammable.CA_Flam_inj())
                    # print(caflammable.CA_Flam_inj_toxic())
                    # print(catoxic.CA_toxic_inj())
                    # print(catoxic.CA_toxic_inj2())
                    # print(catoxic.NoneCA_leck())
                    CA_inj = max(caflammable.CA_Flam_inj(), caflammable.CA_Flam_inj_toxic(), catoxic.CA_toxic_inj(),
                                 catoxic.CA_toxic_inj2(), catoxic.NoneCA_leck())
                    fullcof = FinancialCOF.FinancialCOF(proposalID, model_fluid, toxic_fluid,
                                                        toxic_fluid_percentage, api_com_type,
                                                        MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                        rwinputca.mitigation_system,
                                                        rwstream.maxoperatingtemperature, store_pressure)
                    try:
                        calv1 = models.RwCaLevel1(id=rwassessment,release_phase=ca_cal.GET_RELEASE_PHASE(),
                                                  fact_di=ca_cal.fact_di(),fact_mit=ca_cal.fact_mit(),
                                                  fact_ait=ca_cal.fact_ait(),ca_cmd = ca_cal.ca_cmd(),
                                                  ca_inj_flame=ca_cal.ca_inj_flame(),ca_inj_toxic=ca_cal.ca_inj_tox(),
                                                  ca_inj_ntnf=ca_cal.ca_inj_nfnt(),fc_cmd=ca_cal.fc_cmd(),
                                                  fc_affa=ca_cal.fc_affa(),fc_prod=ca_cal.fc_prod(),
                                                  fc_inj=ca_cal.fc_inj(),
                                                  fc_total=fullcof.FC_total(),
                                                  fcof_category=fullcof.FC_Category(),
                                                  ca_final=ca_cal.ca_final(),auto_ignition=ca_cal.auto_ignition_temp(),
                                                  ideal_gas=ca_cal.C_P(),ideal_gas_ratio=ca_cal.ideal_gas_ratio(),
                                                  liquid_density=ca_cal.liquid_density(),ambient=ca_cal.ambient(),mw=ca_cal.moleculer_weight(),
                                                  nbp=ca_cal.NBP(),model_fluid_type=ca_cal.model_fluid_type())#bo di toxic_fluid_type=ca_cal.toxic_fluid_type()
                        calv1.save()
                    except Exception as e:
                        print(e)
            # print('ca_final = ',ca_cal.ca_final() )
            # print('fact_di = ', calv1.fact_di, )
        except Exception as e:
            print(e)
            print('test ca_cal.final')
        #Chart data
        # fcTotal = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
        fcTotal = models.RwCaLevel1.objects.get(id=proposalID).fc_total
        fullPOF = models.RwFullPof.objects.get(id=proposalID)
        if fullPOF.thinningtype == "General":
            riskList = dm_cal.DF_LIST_16_GENERAL(fcTotal, gffTotal, datafaci.managementfactor, comp.risktarget)
        else:
            riskList = dm_cal.DF_LIST_16(fcTotal, gffTotal, datafaci.managementfactor, comp.risktarget)
        # print('riskList')
        # print(riskList)
        if chart.count() != 0:
            chartData = models.RwDataChart.objects.get(id=proposalID)
            # chartData.riskage0 = riskList[0]
            chartData.riskage1 = riskList[1]['risk']
            chartData.riskage2 = riskList[2]['risk']
            chartData.riskage3 = riskList[3]['risk']
            chartData.riskage4 = riskList[4]['risk']
            chartData.riskage5 = riskList[5]['risk']
            chartData.riskage6 = riskList[6]['risk']
            chartData.riskage7 = riskList[7]['risk']
            chartData.riskage8 = riskList[8]['risk']
            chartData.riskage9 = riskList[9]['risk']
            chartData.riskage10 = riskList[10]['risk']
            chartData.riskage11 = riskList[11]['risk']
            chartData.riskage12 = riskList[12]['risk']
            chartData.riskage13 = riskList[13]['risk']
            chartData.riskage14 = riskList[14]['risk']
            chartData.riskage15 = riskList[15]['risk']
            chartData.riskage16 = riskList[16]['risk']
            chartData.riskage17 = riskList[17]['risk']
            chartData.riskage18 = riskList[18]['risk']
            chartData.riskage19 = riskList[19]['risk']
            chartData.riskage20 = riskList[20]['risk']
            chartData.riskage21 = riskList[21]['risk']
            chartData.riskage22 = riskList[22]['risk']
            chartData.riskage23 = riskList[23]['risk']
            chartData.riskage24 = riskList[24]['risk']
            chartData.riskage25 = riskList[25]['risk']
            chartData.riskage26 = riskList[26]['risk']
            chartData.riskage27 = riskList[27]['risk']
            chartData.riskage28 = riskList[28]['risk']

            # riskList[0] luu nam bat dau bam de tim diem cat risktarget, cach nhau 0.1 nam
            chartData.risktarget = riskList[0]['risk']
            chartData.save()
        else:
            chartData = models.RwDataChart(id=rwassessment, riskage1=riskList[1]['risk'], riskage2=riskList[2]['risk'],
                                           riskage3=riskList[3]['risk'],
                                           riskage4=riskList[4]['risk'], riskage5=riskList[5]['risk'],
                                           riskage6=riskList[6]['risk'],
                                           riskage7=riskList[7]['risk'],
                                           riskage8=riskList[8]['risk'], riskage9=riskList[9]['risk'],
                                           riskage10=riskList[10]['risk'],
                                           riskage11=riskList[11]['risk'],
                                           riskage12=riskList[12]['risk'], riskage13=riskList[13]['risk'],
                                           riskage14=riskList[14]['risk'],
                                           riskage15=riskList[15]['risk'], riskage16=riskList[16]['risk'],
                                           riskage17=riskList[17]['risk'],
                                           riskage18=riskList[18]['risk'], riskage19=riskList[19]['risk'],
                                           riskage20=riskList[20]['risk'],
                                           riskage21=riskList[21]['risk'], riskage22=riskList[22]['risk'],
                                           riskage23=riskList[23]['risk'],
                                           riskage24=riskList[24]['risk'], riskage25=riskList[25]['risk'],
                                           riskage26=riskList[26]['risk'], riskage27=riskList[27]['risk'],
                                           riskage28=riskList[28]['risk'], risktarget=riskList[0]['risk'])
            chartData.save()
        if dmChart.count() != 0:
            chartData = models.RwDataDMFactor.objects.get(id=proposalID)
            # chartData.riskage0 = riskList[0]
            chartData.riskage1 = riskList[1]['df_factor']
            chartData.riskage2 = riskList[2]['df_factor']
            chartData.riskage3 = riskList[3]['df_factor']
            chartData.riskage4 = riskList[4]['df_factor']
            chartData.riskage5 = riskList[5]['df_factor']
            chartData.riskage6 = riskList[6]['df_factor']
            chartData.riskage7 = riskList[7]['df_factor']
            chartData.riskage8 = riskList[8]['df_factor']
            chartData.riskage9 = riskList[9]['df_factor']
            chartData.riskage10 = riskList[10]['df_factor']
            chartData.riskage11 = riskList[11]['df_factor']
            chartData.riskage12 = riskList[12]['df_factor']
            chartData.riskage13 = riskList[13]['df_factor']
            chartData.riskage14 = riskList[14]['df_factor']
            chartData.riskage15 = riskList[15]['df_factor']
            chartData.riskage16 = riskList[16]['df_factor']
            chartData.riskage17 = riskList[17]['df_factor']
            chartData.riskage18 = riskList[18]['df_factor']
            chartData.riskage19 = riskList[19]['df_factor']
            chartData.riskage20 = riskList[20]['df_factor']
            chartData.riskage21 = riskList[21]['df_factor']
            chartData.riskage22 = riskList[22]['df_factor']
            chartData.riskage23 = riskList[23]['df_factor']
            chartData.riskage24 = riskList[24]['df_factor']
            chartData.riskage25 = riskList[25]['df_factor']
            chartData.riskage26 = riskList[26]['df_factor']
            chartData.riskage27 = riskList[27]['df_factor']
            chartData.riskage28 = riskList[28]['df_factor']

            chartData.risktarget = riskList[0]['df_factor']
            chartData.save()
        else:
            chartData = models.RwDataDMFactor(id=rwassessment, riskage1=riskList[1]['df_factor'],
                                              riskage2=riskList[2]['df_factor'],
                                              riskage3=riskList[3]['df_factor'],
                                              riskage4=riskList[4]['df_factor'], riskage5=riskList[5]['df_factor'],
                                              riskage6=riskList[6]['df_factor'],
                                              riskage7=riskList[7]['df_factor'],
                                              riskage8=riskList[8]['df_factor'], riskage9=riskList[9]['df_factor'],
                                              riskage10=riskList[10]['df_factor'],
                                              riskage11=riskList[11]['df_factor'],
                                              riskage12=riskList[12]['df_factor'], riskage13=riskList[13]['df_factor'],
                                              riskage14=riskList[14]['df_factor'],
                                              riskage15=riskList[15]['df_factor'], riskage16=riskList[16]['df_factor'],
                                              riskage17=riskList[17]['df_factor'],
                                              riskage18=riskList[18]['df_factor'], riskage19=riskList[19]['df_factor'],
                                              riskage20=riskList[20]['df_factor'],
                                              riskage21=riskList[21]['df_factor'], riskage22=riskList[22]['df_factor'],
                                              riskage23=riskList[23]['df_factor'],
                                              riskage24=riskList[24]['df_factor'], riskage25=riskList[25]['df_factor'],
                                              riskage26=riskList[26]['df_factor'], riskage27=riskList[27]['df_factor'],
                                              riskage28=riskList[28]['df_factor'], risktarget=riskList[0]['df_factor'])
            chartData.save()
        if pofChart.count() != 0:
            chartData = models.RwDataChartPoF.objects.get(id=proposalID)
            # chartData.riskage0 = riskList[0]
            chartData.riskage1 = riskList[1]['pof']
            chartData.riskage2 = riskList[2]['pof']
            chartData.riskage3 = riskList[3]['pof']
            chartData.riskage4 = riskList[4]['pof']
            chartData.riskage5 = riskList[5]['pof']
            chartData.riskage6 = riskList[6]['pof']
            chartData.riskage7 = riskList[7]['pof']
            chartData.riskage8 = riskList[8]['pof']
            chartData.riskage9 = riskList[9]['pof']
            chartData.riskage10 = riskList[10]['pof']
            chartData.riskage11 = riskList[11]['pof']
            chartData.riskage12 = riskList[12]['pof']
            chartData.riskage13 = riskList[13]['pof']
            chartData.riskage14 = riskList[14]['pof']
            chartData.riskage15 = riskList[15]['pof']
            chartData.riskage16 = riskList[16]['pof']
            chartData.riskage17 = riskList[17]['pof']
            chartData.riskage18 = riskList[18]['pof']
            chartData.riskage19 = riskList[19]['pof']
            chartData.riskage20 = riskList[20]['pof']
            chartData.riskage21 = riskList[21]['pof']
            chartData.riskage22 = riskList[22]['pof']
            chartData.riskage23 = riskList[23]['pof']
            chartData.riskage24 = riskList[24]['pof']
            chartData.riskage25 = riskList[25]['pof']
            chartData.riskage26 = riskList[26]['pof']
            chartData.riskage27 = riskList[27]['pof']
            chartData.riskage28 = riskList[28]['pof']

            chartData.risktarget = riskList[0]['df_factor']
            chartData.save()
        else:
            chartData = models.RwDataChartPoF(id=rwassessment, riskage1=riskList[1]['pof'], riskage2=riskList[2]['pof'],
                                              riskage3=riskList[3]['pof'],
                                              riskage4=riskList[4]['pof'], riskage5=riskList[5]['pof'],
                                              riskage6=riskList[6]['pof'],
                                              riskage7=riskList[7]['pof'],
                                              riskage8=riskList[8]['pof'], riskage9=riskList[9]['pof'],
                                              riskage10=riskList[10]['pof'],
                                              riskage11=riskList[11]['pof'],
                                              riskage12=riskList[12]['pof'], riskage13=riskList[13]['pof'],
                                              riskage14=riskList[14]['pof'],
                                              riskage15=riskList[15]['pof'], riskage16=riskList[16]['pof'],
                                              riskage17=riskList[17]['pof'],
                                              riskage18=riskList[18]['pof'], riskage19=riskList[19]['pof'],
                                              riskage20=riskList[20]['pof'],
                                              riskage21=riskList[21]['pof'], riskage22=riskList[22]['pof'],
                                              riskage23=riskList[23]['pof'],
                                              riskage24=riskList[24]['pof'], riskage25=riskList[25]['pof'],
                                              riskage26=riskList[26]['pof'], riskage27=riskList[27]['pof'],
                                              riskage28=riskList[28]['pof'], risktarget=riskList[0]['pof'])
            chartData.save()
        # damage machinsm
        # print(chartData.riskage0,chartData.riskage1,)
        damageList = dm_cal.ISDF()
        # print('lenggth'+str(damageList))
        for dm in damageMachinsm:
            dm.delete()
        ErrDammage = []
        poin = models.RwDataChart.objects.get(id=proposalID).riskage28
        month = round((poin - int(poin)) * 12)
        # print((poin - int(poin)) * 12)
        # print('poin')
        # print(int(poin))
        # print(month)

        duedate = date2Str.dateFuturebyMonth(rwassessment.assessmentdate, int(poin), month, 0).strftime(
            '%Y-%m-%d')
        # print(duedate)
        # print("ID", rwassessment.id)
        # print(rwassessment.assessmentdate)
        for damage in damageList:
            calv1 = models.RwCaLevel1.objects.get(id=proposalID)
            dm = models.RwDamageMechanism(id_dm=rwassessment, dmitemid_id=damage['DM_ITEM_ID'],
                                          isactive=damage['isActive'],
                                          df1=damage['DF1'], df2=damage['DF2'], df3=damage['DF3'],
                                          highestinspectioneffectiveness=damage['highestEFF'],
                                          secondinspectioneffectiveness=damage['secondEFF'],
                                          numberofinspections=damage['numberINSP'],
                                          lastinspdate=damage['lastINSP'].date().strftime('%Y-%m-%d'),
                                          inspduedate=duedate)
            print('save')
            # print(dm)
            # inspduedate = dm_cal.INSP_DUE_DATE(calv1.fc_total, gffTotal,
            #                                    datafaci.managementfactor,
            #                                    comp.risktarget).date().strftime(
            #     '%Y-%m-%d')
            dm.save()
            ErrDammage.append(damage['DM_ITEM_ID'])
        # SEND EMAIL
        fc_total = models.RwCaLevel1.objects.get(id = proposalID).fc_total
        # print(fc_total)
        dm_cal.SEND_EMAIL(fc_total, gffTotal,
                          datafaci.managementfactor,
                          comp.risktarget, ErrDammage, datafaci.facilityname, request)
        #full FC
        if countRefullfc.count() != 0:
            refullfc = models.RwFullFcof.objects.get(id= proposalID)
            refullfc.fcofvalue=calv1.fc_total
            refullfc.fcofcategory=calv1.fcof_category
            refullfc.envcost=rwinputca.evironment_cost
            refullfc.equipcost=rwinputca.equipment_cost
            refullfc.prodcost=rwinputca.production_cost
            refullfc.popdens=rwinputca.personal_density
            refullfc.injcost=rwinputca.injure_cost
            refullfc.save()
        else:
            refullfc = models.RwFullFcof(id=rwassessment, fcofvalue=calv1.fc_total,
                                             fcofcategory=calv1.fcof_category, envcost=rwinputca.evironment_cost,
                                             equipcost=rwinputca.equipment_cost, prodcost=rwinputca.production_cost,
                                             popdens=rwinputca.personal_density, injcost=rwinputca.injure_cost)
            refullfc.save()
    #     mitigation
    #     mitigation.ShowThining(proposalID)

    except Exception as e:
        print("Exception at fast calculate")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(e)

def calculateTank(proposalID,request):
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwinputca = models.RwInputCaTank.objects.get(id=proposalID)
        countRwcatank = models.RwCaTank.objects.filter(id=proposalID)
        countRefullPOF = models.RwFullPof.objects.filter(id=proposalID)
        damageMachinsm = models.RwDamageMechanism.objects.filter(id_dm=proposalID)
        countRefullfc = models.RwFullFcof.objects.filter(id=proposalID)
        chart = models.RwDataChart.objects.filter(id=proposalID)
        dmChart = models.RwDataDMFactor.objects.filter(id=proposalID)
        pofChart = models.RwDataChartPoF.objects.filter(id=proposalID)
        FullFCof = models.RwFullFcof.objects.filter(id=proposalID)
        rwFullCofTank =models.RWFullCofTank.objects.filter(id=proposalID)
        # print(proposalID)
        # print(rwFullCofTank.prodcost)

        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        eq = models.EquipmentMaster.objects.get(equipmentid=rwassessment.equipmentid_id)
        # target = models.ComponentMaster.objects.get(facilityid=eq.facilityid_id)
        datafaci = models.Facility.objects.get(facilityid=eq.facilityid_id)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        try:
            if not rwassessment.commisstiondate:
                rwassessment.commisstiondate = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).commissiondate
                rwassessment.save()
        except:
            print(e)
        isshell = False
        # if comp.componenttypeid_id == 9 or comp.componenttypeid_id == 13:
        if comp.componenttypeid_id == 13:
            isshell = True
        if not rwcoat.externalcoating:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=rwassessment.commisstiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwassessment.commisstiondate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   Hydrogen=rwstream.hydrogen,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation,
                                   TankMaintain653=rwequipment.tankismaintained,ComponentIsWeld=rwequipment.componentiswelded,
                                   AdjustmentSettle=rwequipment.adjustmentsettle)
        else:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=rwassessment.commisstiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   Hydrogen=rwstream.hydrogen,
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure ,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation,
                                   TankMaintain653=rwequipment.tankismaintained,
                                   ComponentIsWeld=rwequipment.componentiswelded,
                                   AdjustmentSettle=rwequipment.adjustmentsettle)

        if isshell:
            if rwFullCofTank.count()==0:
                phase_fluid_storage = rwstream.storagephase
                cacal = CA_CAL.CA_SHELL(FLUID=rwinputca.api_fluid, FLUID_HEIGHT=rwstream.fluidheight,
                                        SHELL_COURSE_HEIGHT=rwinputca.shell_course_height,
                                        TANK_DIAMETER=rwinputca.tank_diametter,
                                        EnvironSensitivity=rwequipment.environmentsensitivity,
                                        P_lvdike=rwstream.fluidleavedikepercent,
                                        P_onsite=rwstream.fluidleavedikeremainonsitepercent,
                                        P_offsite=rwstream.fluidgooffsitepercent,
                                        MATERIAL_COST=rwmaterial.costfactor,
                                        API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(
                                            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                        PRODUCTION_COST=rwinputca.productioncost,
                                        Soil_type=rwinputca.soil_type,
                                        TANK_FLUID=rwstream.tankfluidname,
                                        CHT=rwcomponent.shellheight,PROD_COST=0,
                                        EQUIP_OUTAGE_MULTIPLIER=0,
                                        EQUIP_COST=0,POP_DENS=0,
                                        INJ_COST=0, release_Fluid_Percent_Toxic=rwstream.releasefluidpercenttoxic,FLUID_PHASE=phase_fluid_storage,proposalID=proposalID)
                                        # EQUIPMENT_COST=FullFCof.equipcost)
            else:
                rwFullCofTank = models.RWFullCofTank.objects.get(id=proposalID)
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
                                        CHT=rwcomponent.shellheight, PROD_COST=rwFullCofTank.prodcost,
                                        EQUIP_OUTAGE_MULTIPLIER=rwFullCofTank.equipoutagemultiplier,
                                        EQUIP_COST=rwFullCofTank.equipcost, POP_DENS=rwFullCofTank.popdens,
                                        INJ_COST=rwFullCofTank.injcost,
                                        release_Fluid_Percent_Toxic=rwstream.releasefluidpercenttoxic,FLUID_PHASE=phase_fluid_storage,proposalID=proposalID)
                # EQUIPMENT_COST=FullFCof.equipcost)
            if countRwcatank.count() != 0:
                rwcatank = models.RwCaTank.objects.get(id=proposalID)
                rwcatank.hydraulic_water = cacal.k_h_water()
                rwcatank.hydraulic_fluid = cacal.k_h_prod()
                rwcatank.seepage_velocity = cacal.vel_s_prod()
                rwcatank.flow_rate_d1 = cacal.W_n_Tank(1)
                rwcatank.flow_rate_d2 = cacal.W_n_Tank(2)
                rwcatank.flow_rate_d3 = cacal.W_n_Tank(3)
                rwcatank.flow_rate_d4 = cacal.W_n_Tank(4)
                rwcatank.leak_duration_d1 = cacal.ld_tank(1)
                rwcatank.leak_duration_d2 = cacal.ld_tank(2)
                rwcatank.leak_duration_d3 = cacal.ld_tank(3)
                rwcatank.leak_duration_d4 = cacal.ld_tank(4)
                rwcatank.release_volume_leak_d1 = cacal.Bbl_leak_n(1)
                rwcatank.release_volume_leak_d2 = cacal.Bbl_leak_n(2)
                rwcatank.release_volume_leak_d3 = cacal.Bbl_leak_n(3)
                rwcatank.release_volume_leak_d4 = cacal.Bbl_leak_n(4)
                rwcatank.release_volume_rupture = cacal.Bbl_rupture_n()
                rwcatank.liquid_height = cacal.LHT_above()
                rwcatank.volume_fluid = cacal.Lvol_abouve()
                rwcatank.time_leak_ground = cacal.ld_tank(4)
                rwcatank.volume_subsoil_leak_d1 = cacal.Bbl_leak_release()
                rwcatank.volume_subsoil_leak_d4 = cacal.Bbl_rupture_release()
                rwcatank.volume_ground_water_leak_d1 = cacal.Bbl_leak_water()
                rwcatank.volume_ground_water_leak_d4 = cacal.Bbl_rupture_water()
                rwcatank.barrel_dike_leak = cacal.Bbl_leak_indike()
                rwcatank.barrel_dike_rupture = cacal.Bbl_rupture_indike()
                rwcatank.barrel_onsite_leak = cacal.Bbl_leak_ssonsite()
                rwcatank.barrel_onsite_rupture = cacal.Bbl_rupture_ssonsite()
                rwcatank.barrel_offsite_leak = cacal.Bbl_leak_ssoffsite()
                rwcatank.barrel_offsite_rupture = cacal.Bbl_rupture_ssoffsite()
                rwcatank.barrel_water_leak = cacal.Bbl_leak_water()
                rwcatank.barrel_water_rupture = cacal.Bbl_rupture_water()
                rwcatank.fc_environ_leak = cacal.FC_leak_environ()
                rwcatank.fc_environ_rupture = cacal.FC_rupture_environ()
                rwcatank.fc_environ = cacal.FC_environ_shell()
                rwcatank.material_factor = rwmaterial.costfactor
                rwcatank.component_damage_cost = cacal.fc_cmd()
                #rwcatank.business_cost = cacal.FC_PROD_SHELL()
                rwcatank.business_cost = cacal.fc_prod_tank()
                rwcatank.consequence = cacal.CA_total_shell()
                rwcatank.consequencecategory = cacal.FC_Category(cacal.CA_total_shell())
                #bổ sung 3 tham số đầu ra
                rwcatank.damage_surrounding_equipment_cost=cacal.fc_affa_tank()
                rwcatank.business_cost = cacal.fc_prod_tank()
                rwcatank.associated_personnel_injury_cost = cacal.fc_inj_tank()
                rwcatank.save()
            else:
                rwcatank = models.RwCaTank(id=rwassessment, hydraulic_water=cacal.k_h_water(),
                                           hydraulic_fluid=cacal.k_h_prod(),
                                           seepage_velocity=cacal.vel_s_prod(),
                                           flow_rate_d1=cacal.W_n_Tank(1),
                                           flow_rate_d2=cacal.W_n_Tank(2),
                                           flow_rate_d3=cacal.W_n_Tank(3),
                                           flow_rate_d4=cacal.W_n_Tank(4),
                                           leak_duration_d1=cacal.ld_tank(1),
                                           leak_duration_d2=cacal.ld_tank(2),
                                           leak_duration_d3=cacal.ld_tank(3), leak_duration_d4=cacal.ld_tank(4),
                                           release_volume_leak_d1=cacal.Bbl_leak_n(1),
                                           release_volume_leak_d2=cacal.Bbl_leak_n(2),
                                           release_volume_leak_d3=cacal.Bbl_leak_n(3),
                                           release_volume_leak_d4=cacal.Bbl_leak_n(4),
                                           release_volume_rupture=cacal.Bbl_rupture_release(),
                                           liquid_height=cacal.LHT_above(),
                                           volume_fluid=cacal.Lvol_abouve(),
                                           time_leak_ground=cacal.ld_tank(4),
                                           volume_subsoil_leak_d1=cacal.Bbl_leak_release(),
                                           volume_subsoil_leak_d4=cacal.Bbl_rupture_release(),
                                           volume_ground_water_leak_d1=cacal.Bbl_leak_water(),
                                           volume_ground_water_leak_d4=cacal.Bbl_rupture_water(),
                                           barrel_dike_leak=cacal.Bbl_leak_indike(),
                                           barrel_dike_rupture=cacal.Bbl_rupture_indike(),
                                           barrel_onsite_leak=cacal.Bbl_leak_ssonsite(),
                                           barrel_onsite_rupture=cacal.Bbl_rupture_ssonsite(),
                                           barrel_offsite_leak=cacal.Bbl_leak_ssoffsite(),
                                           barrel_offsite_rupture=cacal.Bbl_rupture_ssoffsite(),
                                           barrel_water_leak=cacal.Bbl_leak_water(),
                                           barrel_water_rupture=cacal.Bbl_rupture_water(),
                                           fc_environ_leak=cacal.FC_leak_environ(),
                                           fc_environ_rupture=cacal.FC_rupture_environ(),
                                           fc_environ=cacal.FC_environ_shell(),
                                           material_factor=rwinputca.productioncost,
                                           component_damage_cost=cacal.fc_cmd(),
                                           #business_cost=cacal.FC_PROD_SHELL(),
                                           business_cost=cacal.fc_prod_tank(),
                                           consequence=cacal.FC_total_shell(),
                                           consequencecategory=cacal.FC_Category(cacal.CA_total_shell()),
                                           damage_surrounding_equipment_cost=cacal.fc_affa_tank(),
                                           associated_personnel_injury_cost=cacal.fc_inj_tank())
                rwcatank.save()
            FC_TOTAL = cacal.CA_total_shell()
            FC_CATEGORY = cacal.FC_Category(cacal.CA_total_shell())
        else:
            cacal = CA_CAL.CA_TANK_BOTTOM(Soil_type=rwequipment.typeofsoil, TANK_FLUID=rwstream.tankfluidname,
                                          Swg=rwequipment.distancetogroundwater,
                                          TANK_DIAMETER=rwcomponent.nominaldiameter,
                                          FLUID_HEIGHT=rwstream.fluidheight,
                                          API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(apicomponenttypeid= comp.apicomponenttypeid).apicomponenttypename,
                                          PREVENTION_BARRIER=bool(rwcomponent.releasepreventionbarrier),
                                          EnvironSensitivity=rwequipment.environmentsensitivity,
                                          MATERIAL_COST=rwmaterial.costfactor,
                                          PRODUCTION_COST=rwinputca.productioncost,
                                          P_lvdike=rwstream.fluidleavedikepercent, P_onsite=rwstream.fluidleavedikeremainonsitepercent,
                                          P_offsite=rwstream.fluidgooffsitepercent,Concrete_Asphalt = rwcomponent.concretefoundation)
            if countRwcatank.count() != 0:
                rwcatank = models.RwCaTank.objects.get(id=proposalID)
                rwcatank.hydraulic_water = cacal.k_h_water()
                rwcatank.hydraulic_fluid = cacal.k_h_prod()
                rwcatank.seepage_velocity = cacal.vel_s_prod()
                rwcatank.flow_rate_d1 = cacal.rate_n_tank_bottom(1)
                rwcatank.flow_rate_d4 = cacal.rate_n_tank_bottom(4)
                rwcatank.leak_duration_d1 = cacal.ld_n_tank_bottom(1)
                rwcatank.leak_duration_d4 = cacal.ld_n_tank_bottom(4)
                rwcatank.release_volume_leak_d1 = cacal.Bbl_leak_n_bottom(1)
                rwcatank.release_volume_leak_d4 = cacal.Bbl_leak_n_bottom(4)
                rwcatank.release_volume_rupture = cacal.Bbl_rupture_bottom()
                rwcatank.liquid_height = cacal.FLUID_HEIGHT
                rwcatank.volume_fluid = cacal.BBL_TOTAL_TANKBOTTOM()
                rwcatank.time_leak_ground = cacal.t_gl_bottom()
                rwcatank.volume_subsoil_leak_d1 = cacal.Bbl_leak_subsoil(1)
                rwcatank.volume_subsoil_leak_d4 = cacal.Bbl_leak_subsoil(4)
                rwcatank.volume_ground_water_leak_d1 = cacal.Bbl_leak_groundwater(1)
                rwcatank.volume_ground_water_leak_d4 = cacal.Bbl_leak_groundwater(4)
                rwcatank.barrel_dike_rupture = cacal.Bbl_rupture_indike_bottom()
                rwcatank.barrel_onsite_rupture = cacal.Bbl_rupture_ssonsite_bottom()
                rwcatank.barrel_offsite_rupture = cacal.Bbl_rupture_ssoffsite_bottom()
                rwcatank.barrel_water_rupture = cacal.Bbl_rupture_water_bottom()
                rwcatank.fc_environ_leak = cacal.FC_leak_environ_bottom()
                rwcatank.fc_environ_rupture = cacal.FC_rupture_environ_bottom()
                rwcatank.fc_environ = cacal.FC_environ_bottom()
                rwcatank.material_factor = rwmaterial.costfactor
                rwcatank.component_damage_cost = cacal.FC_cmd_bottom()
                rwcatank.business_cost = cacal.FC_PROD_BOTTOM()
                rwcatank.consequence = cacal.FC_total_bottom()
                rwcatank.consequencecategory = cacal.FC_Category(cacal.FC_total_bottom())
                rwcatank.save()
            else:
                print(rwassessment)
                rwcatank = models.RwCaTank(id=rwassessment, hydraulic_water=cacal.k_h_water(),
                                           hydraulic_fluid=cacal.k_h_prod(),
                                           seepage_velocity=cacal.vel_s_prod(),
                                           flow_rate_d1=cacal.rate_n_tank_bottom(1),
                                           flow_rate_d4=cacal.rate_n_tank_bottom(4),
                                           leak_duration_d1=cacal.ld_n_tank_bottom(1),
                                           leak_duration_d4=cacal.ld_n_tank_bottom(4),
                                           release_volume_leak_d1=cacal.Bbl_leak_n_bottom(1),
                                           release_volume_leak_d4=cacal.Bbl_leak_n_bottom(4),
                                           release_volume_rupture=cacal.Bbl_rupture_release_bottom(),
                                           time_leak_ground=cacal.t_gl_bottom(),
                                           volume_subsoil_leak_d1=cacal.Bbl_leak_subsoil(1),
                                           volume_subsoil_leak_d4=cacal.Bbl_leak_subsoil(4),
                                           volume_ground_water_leak_d1=cacal.Bbl_leak_groundwater(1),
                                           volume_ground_water_leak_d4=cacal.Bbl_leak_groundwater(4),
                                           barrel_dike_rupture=cacal.Bbl_rupture_indike_bottom(),
                                           barrel_onsite_rupture=cacal.Bbl_rupture_ssonsite_bottom(),
                                           barrel_offsite_rupture=cacal.Bbl_rupture_ssoffsite_bottom(),
                                           barrel_water_rupture=cacal.Bbl_rupture_water_bottom(),
                                           fc_environ_leak=cacal.FC_leak_environ_bottom(),
                                           fc_environ_rupture=cacal.FC_rupture_environ_bottom(),
                                           fc_environ=cacal.FC_environ_bottom(),
                                           material_factor=rwmaterial.costfactor,
                                           component_damage_cost=cacal.FC_cmd_bottom(),
                                           business_cost=cacal.FC_PROD_BOTTOM(),
                                           consequence=cacal.FC_total_bottom(),
                                           consequencecategory=cacal.FC_Category(cacal.FC_total_bottom()),
                                           liquid_height=cacal.FLUID_HEIGHT,
                                           volume_fluid=cacal.BBL_TOTAL_TANKBOTTOM())
                rwcatank.save()
            FC_TOTAL = cacal.FC_total_bottom()
            FC_CATEGORY = cacal.FC_Category(cacal.FC_total_bottom())
        TOTAL_DF_API1 = dm_cal.DF_TOTAL_API(0)
        TOTAL_DF_API2 = dm_cal.DF_TOTAL_API(3)
        TOTAL_DF_API3 = dm_cal.DF_TOTAL_API(6)

        TOTAL_DF_GENERAL_1 = dm_cal.DF_TOTAL_GENERAL(0)
        TOTAL_DF_GENERAL_2 = dm_cal.DF_TOTAL_GENERAL(3)
        TOTAL_DF_GENERAL_3 = dm_cal.DF_TOTAL_GENERAL(6)

        gffTotal = models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).gfftotal
        pofap1 = pofConvert.convert(float(TOTAL_DF_API1) * float(datafaci.managementfactor) * float(gffTotal))
        pofap2 = pofConvert.convert(float(TOTAL_DF_API2) * float(datafaci.managementfactor) * float(gffTotal))
        pofap3 = pofConvert.convert(float(TOTAL_DF_API3) * float(datafaci.managementfactor) * float(gffTotal))

        pof_general_ap1 = pofConvert.convert(TOTAL_DF_GENERAL_1 * datafaci.managementfactor * gffTotal)
        pof_general_ap2 = pofConvert.convert(TOTAL_DF_GENERAL_2 * datafaci.managementfactor * gffTotal)
        pof_general_ap3 = pofConvert.convert(TOTAL_DF_GENERAL_3 * datafaci.managementfactor * gffTotal)
        # thinningtype = General or Local
        if countRefullPOF.count() != 0:
            refullPOF = models.RwFullPof.objects.get(id=proposalID)
            refullPOF.thinningap1 = dm_cal.DF_THINNING_TOTAL_API(0)
            refullPOF.thinningap2 = dm_cal.DF_THINNING_TOTAL_API(3)
            refullPOF.thinningap3 = dm_cal.DF_THINNING_TOTAL_API(6)
            refullPOF.sccap1 = dm_cal.DF_SSC_TOTAL_API(0)
            refullPOF.sccap2 = dm_cal.DF_SSC_TOTAL_API(3)
            refullPOF.sccap3 = dm_cal.DF_SSC_TOTAL_API(6)
            refullPOF.externalap1 = dm_cal.DF_EXT_TOTAL_API(0)
            refullPOF.externalap2 = dm_cal.DF_EXT_TOTAL_API(3)
            refullPOF.externalap3 = dm_cal.DF_EXT_TOTAL_API(6)
            refullPOF.brittleap1 = dm_cal.DF_BRIT_TOTAL_API(0)
            refullPOF.brittleap2 = dm_cal.DF_BRIT_TOTAL_API(3)
            refullPOF.brittleap3 = dm_cal.DF_BRIT_TOTAL_API(6)
            refullPOF.htha_ap1 = dm_cal.DF_HTHA_API(0)
            refullPOF.htha_ap2 = dm_cal.DF_HTHA_API(3)
            refullPOF.htha_ap3 = dm_cal.DF_HTHA_API(6)
            refullPOF.fatigueap1 = dm_cal.DF_PIPE_API(0)
            refullPOF.fatigueap2 = dm_cal.DF_PIPE_API(3)
            refullPOF.fatigueap3 = dm_cal.DF_PIPE_API(6)
            refullPOF.fms = datafaci.managementfactor
            refullPOF.thinninglocalap1 = max(dm_cal.DF_THINNING_TOTAL_API(0), dm_cal.DF_EXT_TOTAL_API(0))
            refullPOF.thinninglocalap2 = max(dm_cal.DF_THINNING_TOTAL_API(3), dm_cal.DF_EXT_TOTAL_API(3))
            refullPOF.thinninglocalap3 = max(dm_cal.DF_THINNING_TOTAL_API(6), dm_cal.DF_EXT_TOTAL_API(6))
            refullPOF.thinninggeneralap1 = dm_cal.DF_THINNING_TOTAL_API(0) + dm_cal.DF_EXT_TOTAL_API(0)
            refullPOF.thinninggeneralap2 = dm_cal.DF_THINNING_TOTAL_API(3) + dm_cal.DF_EXT_TOTAL_API(3)
            refullPOF.thinninggeneralap3 = dm_cal.DF_THINNING_TOTAL_API(6) + dm_cal.DF_EXT_TOTAL_API(6)
            if refullPOF.thinningtype == "General": 
                refullPOF.totaldfap1 = TOTAL_DF_GENERAL_1
                refullPOF.totaldfap2 = TOTAL_DF_GENERAL_2
                refullPOF.totaldfap3 = TOTAL_DF_GENERAL_3
                refullPOF.pofap1 = pof_general_ap1
                refullPOF.pofap2 = pof_general_ap2
                refullPOF.pofap3 = pof_general_ap3
                refullPOF.pofap1category = dm_cal.PoFCategory(TOTAL_DF_GENERAL_1)
                refullPOF.pofap2category = dm_cal.PoFCategory(TOTAL_DF_GENERAL_2)
                refullPOF.pofap3category = dm_cal.PoFCategory(TOTAL_DF_GENERAL_3)
            else:
                refullPOF.thinningtype = "Local"
                refullPOF.totaldfap1 = TOTAL_DF_API1
                refullPOF.totaldfap2 = TOTAL_DF_API2
                refullPOF.totaldfap3 = TOTAL_DF_API3
                refullPOF.pofap1 = pofap1
                refullPOF.pofap2 = pofap2
                refullPOF.pofap3 = pofap3
                refullPOF.pofap1category = dm_cal.PoFCategory(TOTAL_DF_API1)
                refullPOF.pofap2category = dm_cal.PoFCategory(TOTAL_DF_API2)
                refullPOF.pofap3category = dm_cal.PoFCategory(TOTAL_DF_API3)
            refullPOF.gfftotal = gffTotal
            refullPOF.save()
        else:
            refullPOF = models.RwFullPof(id=rwassessment, thinningap1=dm_cal.DF_THINNING_TOTAL_API(0),
                                         thinningap2=dm_cal.DF_THINNING_TOTAL_API(3),
                                         thinningap3=dm_cal.DF_THINNING_TOTAL_API(6),
                                         sccap1=dm_cal.DF_SSC_TOTAL_API(0), sccap2=dm_cal.DF_SSC_TOTAL_API(3),
                                         sccap3=dm_cal.DF_SSC_TOTAL_API(6),
                                         externalap1=dm_cal.DF_EXT_TOTAL_API(0),
                                         externalap2=dm_cal.DF_EXT_TOTAL_API(3),
                                         externalap3=dm_cal.DF_EXT_TOTAL_API(6),
                                         brittleap1=dm_cal.DF_BRIT_TOTAL_API(0),
                                         brittleap2=dm_cal.DF_BRIT_TOTAL_API(3),
                                         brittleap3=dm_cal.DF_BRIT_TOTAL_API(6),
                                         htha_ap1=dm_cal.DF_HTHA_API(0), htha_ap2=dm_cal.DF_HTHA_API(3),
                                         htha_ap3=dm_cal.DF_HTHA_API(6),
                                         fatigueap1=dm_cal.DF_PIPE_API(0), fatigueap2=dm_cal.DF_PIPE_API(3),
                                         fatigueap3=dm_cal.DF_PIPE_API(6),
                                         fms=datafaci.managementfactor, thinningtype="Local",
                                         thinninglocalap1=max(dm_cal.DF_THINNING_TOTAL_API(0),
                                                              dm_cal.DF_EXT_TOTAL_API(0)),
                                         thinninglocalap2=max(dm_cal.DF_THINNING_TOTAL_API(3),
                                                              dm_cal.DF_EXT_TOTAL_API(3)),
                                         thinninglocalap3=max(dm_cal.DF_THINNING_TOTAL_API(6),
                                                              dm_cal.DF_EXT_TOTAL_API(6)),
                                         thinninggeneralap1=dm_cal.DF_THINNING_TOTAL_API(
                                             0) + dm_cal.DF_EXT_TOTAL_API(0),
                                         thinninggeneralap2=dm_cal.DF_THINNING_TOTAL_API(
                                             3) + dm_cal.DF_EXT_TOTAL_API(3),
                                         thinninggeneralap3=dm_cal.DF_THINNING_TOTAL_API(
                                             6) + dm_cal.DF_EXT_TOTAL_API(6),
                                         totaldfap1=TOTAL_DF_API1, totaldfap2=TOTAL_DF_API2,
                                         totaldfap3=TOTAL_DF_API3,
                                         pofap1=pofap1, pofap2=pofap2, pofap3=pofap3, gfftotal=gffTotal,
                                         pofap1category=dm_cal.PoFCategory(TOTAL_DF_API1),
                                         pofap2category=dm_cal.PoFCategory(TOTAL_DF_API2),
                                         pofap3category=dm_cal.PoFCategory(TOTAL_DF_API3))
            refullPOF.save()
        # data for chart
        fullPOF = models.RwFullPof.objects.get(id=proposalID)
        if fullPOF.thinningtype == "General":
            riskList = dm_cal.DF_LIST_16_GENERAL(FC_TOTAL, gffTotal, datafaci.managementfactor, comp.risktarget)
            # print('length')
            # print(len(riskList))
        else:
            riskList = dm_cal.DF_LIST_16(FC_TOTAL, gffTotal, datafaci.managementfactor, comp.risktarget)

            # print('length')
            # print(len(riskList))

        if chart.count() != 0:
            chartData = models.RwDataChart.objects.get(id=proposalID)
            # chartData.riskage0 = riskList[0]
            chartData.riskage1 = riskList[1]['risk']
            chartData.riskage2 = riskList[2]['risk']
            chartData.riskage3 = riskList[3]['risk']
            chartData.riskage4 = riskList[4]['risk']
            chartData.riskage5 = riskList[5]['risk']
            chartData.riskage6 = riskList[6]['risk']
            chartData.riskage7 = riskList[7]['risk']
            chartData.riskage8 = riskList[8]['risk']
            chartData.riskage9 = riskList[9]['risk']
            chartData.riskage10 = riskList[10]['risk']
            chartData.riskage11 = riskList[11]['risk']
            chartData.riskage12 = riskList[12]['risk']
            chartData.riskage13 = riskList[13]['risk']
            chartData.riskage14 = riskList[14]['risk']
            chartData.riskage15 = riskList[15]['risk']
            chartData.riskage16 = riskList[16]['risk']
            chartData.riskage17 = riskList[17]['risk']
            chartData.riskage18 = riskList[18]['risk']
            chartData.riskage19 = riskList[19]['risk']
            chartData.riskage20 = riskList[20]['risk']
            chartData.riskage21 = riskList[21]['risk']
            chartData.riskage22 = riskList[22]['risk']
            chartData.riskage23 = riskList[23]['risk']
            chartData.riskage24 = riskList[24]['risk']
            chartData.riskage25 = riskList[25]['risk']
            chartData.riskage26 = riskList[26]['risk']
            chartData.riskage27 = riskList[27]['risk']
            chartData.riskage28 = riskList[28]['risk']

            chartData.risktarget = riskList[0]['risk']
            chartData.save()
        else:
            chartData = models.RwDataChart(id=rwassessment, riskage1=riskList[1]['risk'],
                                           riskage2=riskList[2]['risk'],
                                           riskage3=riskList[3]['risk'],
                                           riskage4=riskList[4]['risk'], riskage5=riskList[5]['risk'],
                                           riskage6=riskList[6]['risk'],
                                           riskage7=riskList[7]['risk'],
                                           riskage8=riskList[8]['risk'], riskage9=riskList[9]['risk'],
                                           riskage10=riskList[10]['risk'],
                                           riskage11=riskList[11]['risk'],
                                           riskage12=riskList[12]['risk'], riskage13=riskList[13]['risk'],
                                           riskage14=riskList[14]['risk'],
                                           riskage15=riskList[15]['risk'], riskage16=riskList[16]['risk'],
                                           riskage17=riskList[17]['risk'],
                                           riskage18=riskList[18]['risk'], riskage19=riskList[19]['risk'],
                                           riskage20=riskList[20]['risk'],
                                           riskage21=riskList[21]['risk'], riskage22=riskList[22]['risk'],
                                           riskage23=riskList[23]['risk'],
                                           riskage24=riskList[24]['risk'], riskage25=riskList[25]['risk'],
                                           riskage26=riskList[26]['risk'], riskage27=riskList[27]['risk'],
                                           riskage28=riskList[28]['risk'], risktarget=riskList[0]['risk'])
            chartData.save()
        if dmChart.count() != 0:
            chartData = models.RwDataDMFactor.objects.get(id=proposalID)
            # chartData.riskage0 = riskList[0]
            chartData.riskage1 = riskList[1]['df_factor']
            chartData.riskage2 = riskList[2]['df_factor']
            chartData.riskage3 = riskList[3]['df_factor']
            chartData.riskage4 = riskList[4]['df_factor']
            chartData.riskage5 = riskList[5]['df_factor']
            chartData.riskage6 = riskList[6]['df_factor']
            chartData.riskage7 = riskList[7]['df_factor']
            chartData.riskage8 = riskList[8]['df_factor']
            chartData.riskage9 = riskList[9]['df_factor']
            chartData.riskage10 = riskList[10]['df_factor']
            chartData.riskage11 = riskList[11]['df_factor']
            chartData.riskage12 = riskList[12]['df_factor']
            chartData.riskage13 = riskList[13]['df_factor']
            chartData.riskage14 = riskList[14]['df_factor']
            chartData.riskage15 = riskList[15]['df_factor']
            chartData.riskage16 = riskList[16]['df_factor']
            chartData.riskage17 = riskList[17]['df_factor']
            chartData.riskage18 = riskList[18]['df_factor']
            chartData.riskage19 = riskList[19]['df_factor']
            chartData.riskage20 = riskList[20]['df_factor']
            chartData.riskage21 = riskList[21]['df_factor']
            chartData.riskage22 = riskList[22]['df_factor']
            chartData.riskage23 = riskList[23]['df_factor']
            chartData.riskage24 = riskList[24]['df_factor']
            chartData.riskage25 = riskList[25]['df_factor']
            chartData.riskage26 = riskList[26]['df_factor']
            chartData.riskage27 = riskList[27]['df_factor']
            chartData.riskage28 = riskList[28]['df_factor']

            chartData.risktarget = riskList[0]['df_factor']
            chartData.save()
        else:
            chartData = models.RwDataDMFactor(id=rwassessment, riskage1=riskList[1]['df_factor'],
                                              riskage2=riskList[2]['df_factor'],
                                              riskage3=riskList[3]['df_factor'],
                                              riskage4=riskList[4]['df_factor'], riskage5=riskList[5]['df_factor'],
                                              riskage6=riskList[6]['df_factor'],
                                              riskage7=riskList[7]['df_factor'],
                                              riskage8=riskList[8]['df_factor'], riskage9=riskList[9]['df_factor'],
                                              riskage10=riskList[10]['df_factor'],
                                              riskage11=riskList[11]['df_factor'],
                                              riskage12=riskList[12]['df_factor'],
                                              riskage13=riskList[13]['df_factor'],
                                              riskage14=riskList[14]['df_factor'],
                                              riskage15=riskList[15]['df_factor'],
                                              riskage16=riskList[16]['df_factor'],
                                              riskage17=riskList[17]['df_factor'],
                                              riskage18=riskList[18]['df_factor'],
                                              riskage19=riskList[19]['df_factor'],
                                              riskage20=riskList[20]['df_factor'],
                                              riskage21=riskList[21]['df_factor'],
                                              riskage22=riskList[22]['df_factor'],
                                              riskage23=riskList[23]['df_factor'],
                                              riskage24=riskList[24]['df_factor'],
                                              riskage25=riskList[25]['df_factor'],
                                              riskage26=riskList[26]['df_factor'],
                                              riskage27=riskList[27]['df_factor'],
                                              riskage28=riskList[28]['df_factor'],
                                              risktarget=riskList[0]['df_factor'])
            chartData.save()
        if pofChart.count() != 0:
            chartData = models.RwDataChartPoF.objects.get(id=proposalID)
            # chartData.riskage0 = riskList[0]
            chartData.riskage1 = riskList[1]['pof']
            chartData.riskage2 = riskList[2]['pof']
            chartData.riskage3 = riskList[3]['pof']
            chartData.riskage4 = riskList[4]['pof']
            chartData.riskage5 = riskList[5]['pof']
            chartData.riskage6 = riskList[6]['pof']
            chartData.riskage7 = riskList[7]['pof']
            chartData.riskage8 = riskList[8]['pof']
            chartData.riskage9 = riskList[9]['pof']
            chartData.riskage10 = riskList[10]['pof']
            chartData.riskage11 = riskList[11]['pof']
            chartData.riskage12 = riskList[12]['pof']
            chartData.riskage13 = riskList[13]['pof']
            chartData.riskage14 = riskList[14]['pof']
            chartData.riskage15 = riskList[15]['pof']
            chartData.riskage16 = riskList[16]['pof']
            chartData.riskage17 = riskList[17]['pof']
            chartData.riskage18 = riskList[18]['pof']
            chartData.riskage19 = riskList[19]['pof']
            chartData.riskage20 = riskList[20]['pof']
            chartData.riskage21 = riskList[21]['pof']
            chartData.riskage22 = riskList[22]['pof']
            chartData.riskage23 = riskList[23]['pof']
            chartData.riskage24 = riskList[24]['pof']
            chartData.riskage25 = riskList[25]['pof']
            chartData.riskage26 = riskList[26]['pof']
            chartData.riskage27 = riskList[27]['pof']
            chartData.riskage28 = riskList[28]['pof']

            chartData.risktarget = riskList[0]['df_factor']
            chartData.save()
        else:
            chartData = models.RwDataChartPoF(id=rwassessment, riskage1=riskList[1]['pof'],
                                              riskage2=riskList[2]['pof'],
                                              riskage3=riskList[3]['pof'],
                                              riskage4=riskList[4]['pof'], riskage5=riskList[5]['pof'],
                                              riskage6=riskList[6]['pof'],
                                              riskage7=riskList[7]['pof'],
                                              riskage8=riskList[8]['pof'], riskage9=riskList[9]['pof'],
                                              riskage10=riskList[10]['pof'],
                                              riskage11=riskList[11]['pof'],
                                              riskage12=riskList[12]['pof'], riskage13=riskList[13]['pof'],
                                              riskage14=riskList[14]['pof'],
                                              riskage15=riskList[15]['pof'], riskage16=riskList[16]['pof'],
                                              riskage17=riskList[17]['pof'],
                                              riskage18=riskList[18]['pof'], riskage19=riskList[19]['pof'],
                                              riskage20=riskList[20]['pof'],
                                              riskage21=riskList[21]['pof'], riskage22=riskList[22]['pof'],
                                              riskage23=riskList[23]['pof'],
                                              riskage24=riskList[24]['pof'], riskage25=riskList[25]['pof'],
                                              riskage26=riskList[26]['pof'], riskage27=riskList[27]['pof'],
                                              riskage28=riskList[28]['pof'], risktarget=riskList[0]['pof'])
            chartData.save()
        # damage machinsm
        damageList = dm_cal.ISDF()
        for dm in damageMachinsm:
            dm.delete()
        ErrDammage = []
        poin = models.RwDataChart.objects.get(id=proposalID).riskage28
        # print('poin')
        # print(poin)
        month = int((poin - int(poin)) * 12)

        duedate = date2Str.dateFuturebyMonth(rwassessment.assessmentdate, int(poin), month, 0).strftime('%Y-%m-%d')
        # print('assessmentdate')
        # print(rwassessment.assessmentdate)
        # print('duedate')
        # print(duedate)
        for damage in damageList:
            dm = models.RwDamageMechanism(id_dm=rwassessment, dmitemid_id=damage['DM_ITEM_ID'],
                                          isactive=damage['isActive'],
                                          df1=damage['DF1'], df2=damage['DF2'], df3=damage['DF3'],
                                          highestinspectioneffectiveness=damage['highestEFF'],
                                          secondinspectioneffectiveness=damage['secondEFF'],
                                          numberofinspections=damage['numberINSP'],
                                          lastinspdate=damage['lastINSP'].date().strftime('%Y-%m-%d'),
                                          inspduedate=duedate)
            # inspduedate = dm_cal.INSP_DUE_DATE(FC_TOTAL, gffTotal,
            #                                    datafaci.managementfactor,
            #                                    comp.risktarget).date().strftime(
            #     '%Y-%m-%d'))
            dm.save()
            ErrDammage.append(damage['DM_ITEM_ID'])

        dm_cal.SEND_EMAIL(FC_TOTAL, gffTotal,
                          datafaci.managementfactor,
                          comp.risktarget,ErrDammage,datafaci.facilityname,request)

        if countRefullfc.count() != 0:
            refullfc = models.RwFullFcof.objects.get(id=proposalID)
            refullfc.fcofvalue = FC_TOTAL
            refullfc.fcofcategory = FC_CATEGORY
            refullfc.prodcost = rwinputca.productioncost
            refullfc.save()
        else:
            refullfc = models.RwFullFcof(id=rwassessment, fcofvalue=FC_TOTAL, fcofcategory=FC_CATEGORY,
                                         prodcost=rwinputca.productioncost)
            refullfc.save()

    except Exception as e:
        print("Exception at tank fast calculate")
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

def ReCalculate(proposalID,request):
    try:
        rwAss = models.RwAssessment.objects.get(id=proposalID)
        component = models.ComponentMaster.objects.get(componentid=rwAss.componentid_id)
        if component.componenttypeid_id == 9 or component.componenttypeid_id == 12 or component.componenttypeid_id == 13 or component.componenttypeid_id == 15:
            isTank = 1
        else:
            isTank = 0
        if isTank:

            calculateTank(proposalID,request)
            caculateCorrisionRate(proposalID)
        else:
            calculateNormal(proposalID,request)
            caculateCorrisionRate(proposalID)
    except Exception as e:
        print("Exception at Fast Calculate General!")
        print(e)
def calculateHelpNormal(proposalID):
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwinputca = models.RwInputCaLevel1.objects.get(id=proposalID)
        countRefullPOF = models.RwFullPof.objects.filter(id=proposalID)
        countCalv1 = models.RwCaLevel1.objects.filter(id=proposalID)
        rwcofholesize = models.RwFullCoFHoleSize.objects.filter(id=proposalID)
        damageMachinsm = models.RwDamageMechanism.objects.filter(id_dm=proposalID)
        countRefullfc = models.RwFullFcof.objects.filter(id=proposalID)
        chart = models.RwDataChart.objects.filter(id=proposalID)
        dmChart = models.RwDataDMFactor.objects.filter(id=proposalID)
        pofChart = models.RwDataChartPoF.objects.filter(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        # target = models.FacilityRiskTarget.objects.get(
        #     facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
        datafaci = models.Facility.objects.get(
            facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)

        if not rwcoat.externalcoating:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=rwassessment.commisstiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwassessment.commisstiondate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   Hydrogen=rwstream.hydrogen,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter, TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness, MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency, AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength,Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)
        else:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=rwassessment.commisstiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                   apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   Hydrogen= rwstream.hydrogen,
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter, TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness, MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency, AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength,Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation)
        ca_cal = CA_CAL.CA_NORMAL(NominalDiametter=rwcomponent.nominaldiameter,
                                  MATERIAL_COST=rwmaterial.costfactor, FLUID=rwinputca.api_fluid,
                                  FLUID_PHASE=rwstream.storagephase,
                                  MAX_OPERATING_TEMP=rwstream.maxoperatingtemperature,
                                  API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(
                                      apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                  DETECTION_TYPE=rwinputca.detection_type,
                                  ISOLATION_TYPE=rwinputca.isulation_type,
                                  STORED_PRESSURE=rwstream.maxoperatingpressure*1000,
                                  ATMOSPHERIC_PRESSURE=101.325, STORED_TEMP=rwstream.minoperatingtemperature ,
                                  MASS_INVERT=rwinputca.mass_inventory,
                                  MASS_COMPONENT=rwinputca.mass_component,
                                  MITIGATION_SYSTEM=rwinputca.mitigation_system,
                                  TOXIC_PERCENT=rwinputca.toxic_percent,
                                  RELEASE_DURATION=rwinputca.release_duration,
                                  PRODUCTION_COST=rwinputca.production_cost, TOXIC_FLUID=rwinputca.toxic_fluid,
                                  INJURE_COST=rwinputca.injure_cost, ENVIRON_COST=rwinputca.evironment_cost,
                                  PERSON_DENSITY=rwinputca.personal_density,
                                  EQUIPMENT_COST=rwinputca.equipment_cost)

        TOTAL_DF_API1 = dm_cal.DF_TOTAL_API(0)

        TOTAL_DF_GENERAL_1 = dm_cal.DF_TOTAL_GENERAL(0)


        gffTotal = models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).gfftotal
        pofap1 = pofConvert.convert(TOTAL_DF_API1 * datafaci.managementfactor * gffTotal)


        pof_general_ap1 = pofConvert.convert(TOTAL_DF_GENERAL_1 * datafaci.managementfactor * gffTotal)

        # full pof
        DMFactor={}
        DMFactor['thin']=dm_cal.DF_THINNING_API(0)
        DMFactor['lin']=dm_cal.DF_LINNING_API(0)
        DMFactor['caustic']=dm_cal.DF_CAUTISC_API(0)
        DMFactor['amine']=dm_cal.DF_AMINE_API(0)
        DMFactor['sulphide']=dm_cal.DF_SULPHIDE_API(0)
        DMFactor['hicsohic_h2s']=dm_cal.DF_HICSOHIC_H2S_API(0)
        DMFactor['cacbonat']=dm_cal.DF_CACBONATE_API(0)
        DMFactor['pta']=dm_cal.DF_PTA_API(0)
        DMFactor['clscc']=dm_cal.DF_CLSCC_API(0)
        DMFactor['hschf']=dm_cal.DF_HSCHF_API(0)
        DMFactor['sohic']=dm_cal.DF_HIC_SOHIC_HF_API(0)
        DMFactor['external_corrosion']=dm_cal.DF_EXTERNAL_CORROSION_API(0)
        DMFactor['cui']=dm_cal.DF_CUI_API(0)
        DMFactor['extern_clscc']=dm_cal.DF_EXTERN_CLSCC_API(0)
        DMFactor['cui_clscc']=dm_cal.DF_CUI_CLSCC_API(0)
        DMFactor['htha']=dm_cal.DF_HTHA_API(0)
        DMFactor['brittle']=dm_cal.DF_BRITTLE_API(0)
        DMFactor['embrittle']=dm_cal.DF_TEMP_EMBRITTLE_API(0)
        DMFactor['885']=dm_cal.DF_885_API(0)
        DMFactor['sigma']=dm_cal.DF_SIGMA_API(0)
        DMFactor['pipe']=dm_cal.DF_PIPE_API(0)
        
        refullPOF = models.RwFullPof.objects.get(id=proposalID)
        if refullPOF.thinningtype == "General":
            DMFactor['pof'] = pof_general_ap1
        else:

            DMFactor['pof'] = pofap1

        return DMFactor

    except Exception as e:
        print("Exception at fast calculate")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(e)
def thinningTotalAPI(proposalID,thin,lin):
    try:
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        INTERNAL_LINNING=bool(rwcoat.internallining)

        if INTERNAL_LINNING and (lin != 0):
            DF_THINNING_TOTAL = min(thin, lin)
        else:
            DF_THINNING_TOTAL = lin
        return DF_THINNING_TOTAL
    except Exception as e:
        print(e)
def calculateHelpTank(proposalID):
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwinputca = models.RwInputCaTank.objects.get(id=proposalID)
        countRwcatank = models.RwCaTank.objects.filter(id=proposalID)
        countRefullPOF = models.RwFullPof.objects.filter(id=proposalID)
        damageMachinsm = models.RwDamageMechanism.objects.filter(id_dm=proposalID)
        countRefullfc = models.RwFullFcof.objects.filter(id=proposalID)
        chart = models.RwDataChart.objects.filter(id=proposalID)
        FullFCof = models.RwFullFcof.objects.filter(id=proposalID)
        rwFullCofTank =models.RWFullCofTank.objects.filter(id=proposalID)
        # print(proposalID)
        # print(rwFullCofTank.prodcost)

        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        eq = models.EquipmentMaster.objects.get(equipmentid=rwassessment.equipmentid_id)
        # target = models.ComponentMaster.objects.get(facilityid=eq.facilityid_id)
        datafaci = models.Facility.objects.get(facilityid=eq.facilityid_id)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)

        isshell = False
        if comp.componenttypeid_id == 9 or comp.componenttypeid_id == 13:
            isshell = True
        if not rwcoat.externalcoating:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   Hydrogen=rwstream.hydrogen,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation,
                                   TankMaintain653=rwequipment.tankismaintained,ComponentIsWeld=rwequipment.componentiswelded)
        else:
            dm_cal = DM_CAL.DM_CAL(ComponentNumber=str(comp.componentnumber),
                                   Commissiondate=models.EquipmentMaster.objects.get(
                                       equipmentid=comp.equipmentid_id).commissiondate,
                                   AssessmentDate=rwassessment.assessmentdate,
                                   APIComponentType=models.ApiComponentType.objects.get(
                                       apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename,
                                   Diametter=rwcomponent.nominaldiameter, NomalThick=rwcomponent.nominalthickness,
                                   CurrentThick=rwcomponent.currentthickness, MinThickReq=rwcomponent.minreqthickness,
                                   CorrosionRate=rwcomponent.currentcorrosionrate, CA=rwmaterial.corrosionallowance,
                                   CladdingCorrosionRate=rwcoat.claddingcorrosionrate,CladdingThickness= rwcoat.claddingthickness,
                                   InternalCladding=bool(rwcoat.internalcladding),
                                   OnlineMonitoring=rwequipment.onlinemonitoring,
                                   HighlyEffectDeadleg=bool(rwequipment.highlydeadleginsp),
                                   ContainsDeadlegs=bool(rwequipment.containsdeadlegs),
                                   LinningType=rwcoat.internallinertype,
                                   LINNER_ONLINE=bool(rwequipment.lineronlinemonitoring),
                                   LINNER_CONDITION=rwcoat.internallinercondition,
                                   INTERNAL_LINNING=bool(rwcoat.internallining),
                                   HEAT_TREATMENT=rwmaterial.heattreatment,
                                   NaOHConcentration=rwstream.naohconcentration,
                                   HEAT_TRACE=bool(rwequipment.heattraced),
                                   STEAM_OUT=bool(rwequipment.steamoutwaterflush),
                                   AMINE_EXPOSED=bool(rwstream.exposedtogasamine),
                                   AMINE_SOLUTION=rwstream.aminesolution,
                                   ENVIRONMENT_H2S_CONTENT=bool(rwstream.h2s),
                                   AQUEOUS_OPERATOR=bool(rwstream.aqueousoperation),
                                   AQUEOUS_SHUTDOWN=bool(rwstream.aqueousshutdown),
                                   H2SContent=rwstream.h2sinwater, PH=rwstream.waterph,
                                   PRESENT_CYANIDE=bool(rwstream.cyanide), BRINNEL_HARDNESS=rwcomponent.brinnelhardness,
                                   SULFUR_CONTENT=rwmaterial.sulfurcontent,
                                   CO3_CONTENT=rwstream.co3concentration,
                                   PTA_SUSCEP=bool(rwmaterial.ispta), NICKEL_ALLOY=bool(rwmaterial.nickelbased),
                                   EXPOSED_SULFUR=bool(rwstream.exposedtosulphur),
                                   Hydrogen=rwstream.hydrogen,
                                   ExposedSH2OOperation=bool(rwequipment.presencesulphideso2),
                                   ExposedSH2OShutdown=bool(rwequipment.presencesulphideso2shutdown),
                                   ThermalHistory=rwequipment.thermalhistory, PTAMaterial=rwmaterial.ptamaterialcode,
                                   DOWNTIME_PROTECTED=bool(rwequipment.downtimeprotectionused),
                                   INTERNAL_EXPOSED_FLUID_MIST=bool(rwstream.materialexposedtoclint),
                                   EXTERNAL_EXPOSED_FLUID_MIST=bool(rwequipment.materialexposedtoclext),
                                   CHLORIDE_ION_CONTENT=rwstream.chloride,
                                   HF_PRESENT=bool(rwstream.hydrofluoric),
                                   INTERFACE_SOIL_WATER=bool(rwequipment.interfacesoilwater),
                                   SUPPORT_COATING=bool(rwcoat.supportconfignotallowcoatingmaint),
                                   INSULATION_TYPE=rwcoat.externalinsulationtype,
                                   CUI_PERCENT_1=rwexcor.minus12tominus8, CUI_PERCENT_2=rwexcor.minus8toplus6,
                                   CUI_PERCENT_3=rwexcor.plus6toplus32, CUI_PERCENT_4=rwexcor.plus32toplus71,
                                   CUI_PERCENT_5=rwexcor.plus71toplus107,
                                   CUI_PERCENT_6=rwexcor.plus107toplus121, CUI_PERCENT_7=rwexcor.plus121toplus135,
                                   CUI_PERCENT_8=rwexcor.plus135toplus162,
                                   CUI_PERCENT_9=rwexcor.plus162toplus176, CUI_PERCENT_10=rwexcor.morethanplus176,
                                   EXTERNAL_INSULATION=bool(rwcoat.externalinsulation),
                                   COMPONENT_INSTALL_DATE=rwcoat.externalcoatingdate,
                                   CRACK_PRESENT=bool(rwcomponent.crackspresent),
                                   EXTERNAL_EVIRONMENT=rwequipment.externalenvironment,
                                   EXTERN_COAT_QUALITY=rwcoat.externalcoatingquality,
                                   PIPING_COMPLEXITY=rwcomponent.complexityprotrusion,
                                   INSULATION_CONDITION=rwcoat.insulationcondition,
                                   INSULATION_CHLORIDE=bool(rwcoat.insulationcontainschloride),
                                   MATERIAL_SUSCEP_HTHA=bool(rwmaterial.ishtha),
                                   HTHA_MATERIAL=rwmaterial.hthamaterialcode,
                                   # HTHA_PRESSURE=rwstream.h2spartialpressure * 0.006895,
                                   HTHA_PRESSURE=rwstream.h2spartialpressure,
                                   CRITICAL_TEMP=rwstream.criticalexposuretemperature,
                                   DAMAGE_FOUND=bool(rwcomponent.damagefoundinspection),
                                   LOWEST_TEMP=bool(rwequipment.yearlowestexptemp),
                                   TEMPER_SUSCEP=bool(rwmaterial.temper), PWHT=bool(rwequipment.pwht),
                                   BRITTLE_THICK=rwcomponent.brittlefracturethickness,
                                   CARBON_ALLOY=bool(rwmaterial.carbonlowalloy),
                                   DELTA_FATT=rwcomponent.deltafatt,
                                   MAX_OP_TEMP=rwstream.maxoperatingtemperature,
                                   CHROMIUM_12=bool(rwmaterial.chromemoreequal12),
                                   MIN_OP_TEMP=rwstream.minoperatingtemperature,
                                   MIN_DESIGN_TEMP=rwmaterial.mindesigntemperature,
                                   REF_TEMP=rwmaterial.referencetemperature,
                                   AUSTENITIC_STEEL=bool(rwmaterial.austenitic), PERCENT_SIGMA=rwmaterial.sigmaphase,
                                   EquipmentType=models.EquipmentType.objects.get(
                                       equipmenttypeid=models.EquipmentMaster.objects.get(
                                           equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename,
                                   PREVIOUS_FAIL=rwcomponent.previousfailures,
                                   AMOUNT_SHAKING=rwcomponent.shakingamount, TIME_SHAKING=rwcomponent.shakingtime,
                                   CYLIC_LOAD=rwcomponent.cyclicloadingwitin15_25m,
                                   CORRECT_ACTION=rwcomponent.correctiveaction, NUM_PIPE=rwcomponent.numberpipefittings,
                                   PIPE_CONDITION=rwcomponent.pipecondition, JOINT_TYPE=rwcomponent.branchjointtype,
                                   BRANCH_DIAMETER=rwcomponent.branchdiameter,
                                   TensileStrengthDesignTemp=rwmaterial.tensilestrength,
                                   StructuralThickness=rwcomponent.structuralthickness,
                                   MINIUM_STRUCTURAL_THICKNESS_GOVERS=rwcomponent.minstructuralthickness,
                                   WeldJonintEfficiency=rwcomponent.weldjointefficiency,
                                   AllowableStress=rwcomponent.allowablestress,
                                   YeildStrengthDesignTemp=rwmaterial.yieldstrength, Pressure=rwmaterial.designpressure,
                                   ShapeFactor=comptype.shapefactor,
                                   CR_Confidents_Level=rwcomponent.confidencecorrosionrate,
                                   PRESSSURE_CONTROL=bool(rwequipment.pressurisationcontrolled),
                                   FABRICATED_STEEL=bool(rwcomponent.fabricatedsteel),
                                   EQUIPMENT_SATISFIED=bool(rwcomponent.equipmentsatisfied),
                                   NOMINAL_OPERATING_CONDITIONS=bool(rwcomponent.nominaloperatingconditions),
                                   CET_THE_MAWP=bool(rwcomponent.cetgreaterorequal),
                                   CYCLIC_SERVICE=bool(rwcomponent.cyclicservice),
                                   EQUIPMENT_CIRCUIT_SHOCK=bool(rwcomponent.equipmentcircuitshock),
                                   MIN_TEMP_PRESSURE=rwequipment.minreqtemperaturepressurisation,
                                   TankMaintain653=rwequipment.tankismaintained,
                                   ComponentIsWeld=rwequipment.componentiswelded)


        TOTAL_DF_API1 = dm_cal.DF_TOTAL_API(0)


        TOTAL_DF_GENERAL_1 = dm_cal.DF_TOTAL_GENERAL(0)


        gffTotal = models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).gfftotal
        pofap1 = pofConvert.convert(float(TOTAL_DF_API1) * float(datafaci.managementfactor) * float(gffTotal))


        pof_general_ap1 = pofConvert.convert(TOTAL_DF_GENERAL_1 * datafaci.managementfactor * gffTotal)

        # full pof
        DMFactor = {}
        DMFactor['thin'] = dm_cal.DF_THINNING_API(0)
        DMFactor['lin'] = dm_cal.DF_LINNING_API(0)
        DMFactor['caustic'] = dm_cal.DF_CAUTISC_API(0)
        DMFactor['amine'] = dm_cal.DF_AMINE_API(0)
        DMFactor['sulphide'] = dm_cal.DF_SULPHIDE_API(0)
        DMFactor['hicsohic_h2s'] = dm_cal.DF_HICSOHIC_H2S_API(0)
        DMFactor['cacbonat'] = dm_cal.DF_CACBONATE_API(0)
        DMFactor['pta'] = dm_cal.DF_PTA_API(0)
        DMFactor['clscc'] = dm_cal.DF_CLSCC_API(0)
        DMFactor['hschf'] = dm_cal.DF_HSCHF_API(0)
        DMFactor['sohic'] = dm_cal.DF_HIC_SOHIC_HF_API(0)
        DMFactor['external_corrosion'] = dm_cal.DF_EXTERNAL_CORROSION_API(0)
        DMFactor['cui'] = dm_cal.DF_CUI_API(0)
        DMFactor['extern_clscc'] = dm_cal.DF_EXTERN_CLSCC_API(0)
        DMFactor['cui_clscc'] = dm_cal.DF_CUI_CLSCC_API(0)
        DMFactor['htha'] = dm_cal.DF_HTHA_API(0)
        DMFactor['brittle'] = dm_cal.DF_BRITTLE_API(0)
        DMFactor['embrittle'] = dm_cal.DF_TEMP_EMBRITTLE_API(0)
        DMFactor['885'] = dm_cal.DF_885_API(0)
        DMFactor['sigma'] = dm_cal.DF_SIGMA_API(0)
        DMFactor['pipe'] = dm_cal.DF_PIPE_API(0)
        # thinningtype = General or Local
        refullPOF = models.RwFullPof.objects.get(id=proposalID)

        if refullPOF.thinningtype == "General":
            DMFactor['pof'] = pof_general_ap1
            # refullPOF.totaldfap1 = TOTAL_DF_GENERAL_1
        else:
            DMFactor['pof'] = pofap1
        return DMFactor
    except Exception as e:
        print("Exception at tank fast calculate")
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def EXT_TOTAL_API(EXTERNAL_CORROSION_API,CUI_API,EXTERN_CLSCC_API,CUI_CLSCC_API):
    return max(EXTERNAL_CORROSION_API,CUI_API,EXTERN_CLSCC_API,CUI_CLSCC_API)
def SSC_TOTAL_API(CAUTISC_API, AMINE_API,SULPHIDE_API,HIC_SOHIC_HF,HICSOHIC_H2S,CACBONATE_API, PTA, CLSCC_API, HSCHF):
    return max(CAUTISC_API, AMINE_API,SULPHIDE_API,HIC_SOHIC_HF,HICSOHIC_H2S,CACBONATE_API, PTA, CLSCC_API, HSCHF)
def BRIT_TOTAL_API(BRITTLE_API, TEMP_EMBRITTLE_API, SIGMA_API,DF_885_API):
    return max(BRITTLE_API,TEMP_EMBRITTLE_API,SIGMA_API, DF_885_API)
def calculatePoF(proposalID,DMFactor):
    refullPOF = models.RwFullPof.objects.get(id=proposalID)
    if refullPOF.thinningtype == "General":
        TOTAL_DF_API = thinningTotalAPI(proposalID,DMFactor['thin'],DMFactor['lin']) + EXT_TOTAL_API(DMFactor['external_corrosion'],DMFactor['cui'],DMFactor['extern_clscc'],DMFactor['cui_clscc']) +\
        SSC_TOTAL_API(DMFactor['caustic'],DMFactor['amine'],DMFactor['sulphide'],DMFactor['sohic'],DMFactor['hicsohic_h2s'],DMFactor['cacbonat'],DMFactor['pta'],DMFactor['clscc'],DMFactor['hschf']) + \
                       DMFactor['htha'] + BRIT_TOTAL_API(DMFactor['brittle'],DMFactor['embrittle'],DMFactor['sigma'],DMFactor['885']) + DMFactor['pipe']
    else:

        TOTAL_DF_API = max(thinningTotalAPI(proposalID, DMFactor['thin'], DMFactor['lin']) , EXT_TOTAL_API(DMFactor['external_corrosion'], DMFactor['cui'], DMFactor['extern_clscc'], DMFactor['cui_clscc'])) + SSC_TOTAL_API(DMFactor['caustic'], DMFactor['amine'], DMFactor['sulphide'], DMFactor['sohic'],DMFactor['hicsohic_h2s'], DMFactor['cacbonat'], DMFactor['pta'], DMFactor['clscc'],DMFactor['hschf']) + DMFactor['htha'] + BRIT_TOTAL_API(DMFactor['brittle'], DMFactor['embrittle'], DMFactor['sigma'],DMFactor['885']) + DMFactor['pipe']
    rwassessment = models.RwAssessment.objects.get(id=proposalID)
    comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
    datafaci = models.Facility.objects.get(facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
    comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
    gffTotal = models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).gfftotal
    obj={}
    obj['PoF']=pofConvert.convert(TOTAL_DF_API * datafaci.managementfactor * gffTotal)
    obj['damageTotal']=TOTAL_DF_API
    return obj
def Consequencelv2(proposalID):
    rwassessment = models.RwAssessment.objects.get(id=proposalID)
    rwequipment = models.RwEquipment.objects.get(id=proposalID)
    rwcomponent = models.RwComponent.objects.get(id=proposalID)
    rwstream = models.RwStream.objects.get(id=proposalID)
    rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
    rwcoat = models.RwCoating.objects.get(id=proposalID)
    rwmaterial = models.RwMaterial.objects.get(id=proposalID)
    rwinputca = models.RwInputCaLevel1.objects.get(id=proposalID)
    countRefullPOF = models.RwFullPof.objects.filter(id=proposalID)
    countCalv1 = models.RwCaLevel1.objects.filter(id=proposalID)
    rwcofholesize = models.RwFullCoFHoleSize.objects.filter(id=proposalID)
    damageMachinsm = models.RwDamageMechanism.objects.filter(id_dm=proposalID)
    countRefullfc = models.RwFullFcof.objects.filter(id=proposalID)
    chart = models.RwDataChart.objects.filter(id=proposalID)
    cainputlv2=models.RwInputCaLevel2.objects.get(id=proposalID)

    comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
    target = models.FacilityRiskTarget.objects.get(
        facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
    datafaci = models.Facility.objects.get(
        facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
    comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
    try:
        ca_cal_lv2=CA_CAL_LV2.CA_CAL_LV2(Psat=cainputlv2.Psat, FRACT_Liquid=cainputlv2.Frac_l, FRACT_Vapor=cainputlv2.Frac_v, LOWER_FLAMABILITY=cainputlv2.Lower_flammable, UPPER_FLAMABILITY=cainputlv2.Upper_flammable,
                                         HEAT_COMBUSTION=cainputlv2.Hcs, TEMP_FLASH=cainputlv2.temp_flash, FRACT_FLASH=cainputlv2.Fract_flash, HEAT_COMBUSTION_Liquid=cainputlv2.Heat_combustion_l, HEAT_COMBUSTION_Vapor=cainputlv2.Heat_combustion_v,
                                         TEMP_BUBBLE=cainputlv2.temp_bubble, TEMP_DEW=cainputlv2.temp_dew, deltaHv=cainputlv2.delta, STORED_PRESSURE=rwstream.maxoperatingpressure, ATMOSPHERIC_PRESSURE=101.325, NominalDiametter=rwcomponent.nominaldiameter,
                                         STORED_TEMP=rwstream.maxoperatingtemperature, MASS_INVERT=rwinputca.mass_inventory, DETECTION_TYPE=rwinputca.detection_type, ISOLATION_TYPE=rwinputca.isulation_type, SURFACE=cainputlv2.surface, TEMP_GROUND=cainputlv2.temp_ground,
                                         BUBBLE_POINT_PRESSURE=cainputlv2.pressure_bp, WIND_SPEED_MEASURED=cainputlv2.wind_speed_measured, MFRAC_FLAM=cainputlv2.mfrac_flam, TEMP_FLASH_POINT=cainputlv2.temp_fp, FLUID=rwinputca.api_fluid, ATMOSPHERIC_TEMP=cainputlv2.atmospheric_temp,
                                         ATMOSPHERIC_AIR_DENSITY=1.225, ATMOSPHERIC_RELATIVE_HUMIDITY=cainputlv2.atmospheric_rh, ATMOSPHERIC_WATER_PARTIAL_PRESSURE=cainputlv2.atmospheric_wrp, BRUST_PRESSURE=cainputlv2.brust_pressure, XS_FBALL=cainputlv2.xs_fball, YIELD_FACTOR=cainputlv2.yield_factor,
                                         API_COMPONENT_TYPE_NAME=models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename, TOX_LIM=cainputlv2.tox_lim, MOL_FRAC_TOX=cainputlv2.mol_frac_tox, EQUIPMENT_STORED_VAPOR=cainputlv2.equipment_stored_vapor, N_V=cainputlv2.n_v)
    except Exception as e:
        print("Exception at Fast Calculate General!")
        print(e)
def notiVerifications(siteID):
    faci = models.Facility.objects.filter(siteid=siteID)

    notiVerification = []
    for i in faci:
        Ver = models.Verification.objects.filter(facility=i.facilityid)
        if Ver:
            for j in Ver:
                if not j.Is_active:
                    notiVerification.append(j)
    return notiVerification
def notiVerificationmana(siteID):
    print('siteid', siteID)
    faci = models.Facility.objects.filter(siteid=siteID)
    notiVerification = []
    # print('vao')
    ver = models.Verificationsend.objects.filter(id_user=siteID)
    if ver:
        for j in ver:
            if not j.state:
                notiVerification.append(j)
    return notiVerification
def emmua159compare(pof):
    if pof<0.00001:
        return "Remote"
    elif (0.00001 <= pof <0.0001):
        return "Very Low"
    elif (0.0001 <= pof < 0.001):
        return "Low"
    elif (0.001 <= pof < 0.01):
        return "Moderate"
    elif (0.01 <= pof < 0.1):
        return "High"
    elif (pof >= 0.1):
        return "Very High"
    else:
        return "None"
def emmua159comparecof(cof):
    if cof > 100000000:
        return "I - Catastrophic"
    elif (10000000 < cof <= 100000000):
        return "II - Major"
    elif (1000000 < cof <= 10000000):
        return "III - Serious"
    elif (100000 < cof <= 1000000):
        return "IV - Significant"
    elif (10000 < cof <= 100000):
        return "V - Minor"
    elif (cof <= 10000):
        return "VI - Insignificant"
    else:
        return "None"

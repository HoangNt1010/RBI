# Python program to create
# a pdf file


from django.http import Http404, HttpResponse

from cloud.process.RBI import FinancialCOF, Detail_DM_CAL

from fpdf import FPDF
from fpdf import *
from cloud import models
from reportlab.platypus import *
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from pylab import *
import sympy
from matplotlib.backends.backend_pdf import PdfPages

title = 'RBICortek Wtritten Scheme of Examination'


def ChuanHoa(textstr, a):
    txt = textstr.split(' ')
    b = len(txt)
    x = 0
    for x in range(b - 1):
        try:
            while (len(txt[x] + ' ' + txt[x + 1]) <= a):
                for i in range(len(txt) - 1):
                    if (i < x):
                        continue
                    elif (i == x):
                        txt[i] = txt[i] + ' ' + txt[i + 1]
                        continue
                    txt[i] = txt[i + 1]
                    if ((i + 1) == (len(txt) - 1)):
                        c = len(txt)
                        txt = txt[:c - 1]
                        b = len(txt)
        except:
            pass
    return txt


def thining(proposalID):
    try:
        data = []
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        damageMachinsm = models.RwDamageMechanism.objects.filter(id_dm=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        APIComponentType = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        obj = {}
        Diameter = rwcomponent.nominaldiameter
        Normalthickness = rwcomponent.nominalthickness
        Currenthickness = rwcomponent.currentthickness
        Minthickreq = rwcomponent.minreqthickness
        Corrosionrate = rwcomponent.currentcorrosionrate
        ca = rwmaterial.corrosionallowance
        protectbarrier = rwcomponent.releasepreventionbarrier
        claddingthickness = rwcoat.claddingthickness
        claddingcorrosion = rwcoat.claddingcorrosionrate
        internalcladding = rwcoat.internalcladding
        onlinemonitoring = rwequipment.onlinemonitoring
        higheffective = rwequipment.highlydeadleginsp
        deadleg = rwequipment.containsdeadlegs
        tankmaintain = rwequipment.tankismaintained
        adjust = rwequipment.adjustmentsettle
        componentiswelded = rwequipment.componentiswelded
        weldjoint = rwcomponent.weldjointefficiency
        allowablstess = rwcomponent.allowablestress
        tensile = rwmaterial.tensilestrength
        yeild = rwmaterial.yieldstrength
        structural = rwcomponent.structuralthickness
        minstrctural = rwcomponent.minstructuralthickness
        designpressure = rwmaterial.designpressure
        shapefactor = comptype.shapefactor
        confidencecorrosionrate = rwcomponent.confidencecorrosionrate
        assessmentdate = rwassessment.assessmentdate

        thin = Detail_DM_CAL.Df_Thin(Diameter, Normalthickness, Currenthickness, Minthickreq, Corrosionrate, ca,
                                     protectbarrier, claddingthickness,
                                     claddingcorrosion, internalcladding, 0, "E", onlinemonitoring, higheffective,
                                     deadleg, tankmaintain,
                                     adjust, componentiswelded, weldjoint, allowablstess, tensile, yeild,
                                     structural, minstrctural, designpressure,
                                     shapefactor, confidencecorrosionrate, EquipmentType, assessmentdate,
                                     COMPONENT_INSTALL_DATE, ComponentNumber, APIComponentType)
        obj['ThinningDamageFactor1'] = thin.DF_THINNING_API(0)
        obj['ThinningDamageFactor2'] = thin.DF_THINNING_API(3)
        obj['ThinningDamageFactor3'] = thin.DF_THINNING_API(6)
        result = ['Thinning Damage Factor ', obj['ThinningDamageFactor1'], obj['ThinningDamageFactor2'],
                  obj['ThinningDamageFactor3']]
        return result
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return 0


def lining(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        lining = Detail_DM_CAL.Df_Lining(bool(rwcoat.internallining), rwcoat.internallinertype,
                                         rwcoat.internallinercondition, bool(rwequipment.lineronlinemonitoring),
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber)
        obj['lin1'] = lining.DFB_LINNING_API(0)
        obj['lin2'] = lining.DFB_LINNING_API(3)
        obj['lin3'] = lining.DFB_LINNING_API(6)
        result = ['Internal Lining Degradation Damage Factor ', obj['lin1'], obj['lin2'], obj['lin3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def anime(proposalID):
    try:
        obj = {}
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        ComponentNumber = str(comp.componentnumber)
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentName'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname

        obj['AMINE_EXPOSED'] = bool(rwstream.exposedtogasamine)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['AMINE_SOLUTION'] = rwstream.aminesolution

        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['HEAT_TRACE'] = bool(rwequipment.heattraced)
        obj['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)

        obj['AMINE_INSP_EFF'] = 'E'
        obj['AMINE_INSP_NUM'] = 0
        obj['PWHT'] = bool(rwequipment.pwht)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['ComponentNumber'] = str(comp.componentnumber)
        obj2 = {}
        obj2['HEAT_TRACE'] = False
        obj2['STEAM_OUT'] = False
        obj2['MAX_OP_TEMP'] = 30
        animeTem = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                          obj['AMINE_SOLUTION'], obj2['MAX_OP_TEMP'], obj2['HEAT_TRACE'],
                                          obj2['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                          obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                          obj['ComponentNumber'])
        obj2['amine1'] = animeTem.DF_AMINE_API(0)
        obj2['amine2'] = animeTem.DF_AMINE_API(3)
        obj2['amine3'] = animeTem.DF_AMINE_API(6)
        result = ['Anime Stress Cracking Damage Factor ', obj2['amine1'], obj2['amine2'], obj2['amine3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def caustic(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['HEAT_TREATMENT'] = rwmaterial.heattreatment
        obj['NaOHConcentration'] = rwstream.naohconcentration
        obj['HEAT_TRACE'] = bool(rwequipment.heattraced)
        obj['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['PWHT'] = bool(rwequipment.pwht)

        caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'], obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'], obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'], rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        obj['caustic1'] = caustic.DF_CAUSTIC_API(0)
        obj['caustic2'] = caustic.DF_CAUSTIC_API(3)
        obj['caustic3'] = caustic.DF_CAUSTIC_API(6)
        result = ['Caustic Stress Cracking Damage Factor ', obj['caustic1'], obj['caustic2'], obj['caustic3']]
        print(caustic.DF_CAUSTIC(3))
    except Exception as e:
        print(e)
        raise Http404
    return result


def sulphide(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['PH'] = rwstream.waterph
        obj['H2SContent'] = rwstream.h2sinwater
        obj['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['PWHT'] = bool(rwequipment.pwht)
        obj['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        obj['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)

        sulphide = Detail_DM_CAL.Df_Sulphide(obj['PH'], obj['H2SContent'], obj['PRESENT_CYANIDE'],
                                             obj['CRACK_PRESENT'], obj['PWHT'], obj['BRINNEL_HARDNESS'],
                                             obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'],
                                             obj['ENVIRONMENT_H2S_CONTENT'], 'E', 0, rwassessment.assessmentdate,
                                             COMPONENT_INSTALL_DATE, ComponentNumber)
        obj['Sulphide1'] = sulphide.DF_SULPHIDE_API(0)
        obj['Sulphide2'] = sulphide.DFB_SULPHIDE_API(3)
        obj['Sulphide3'] = sulphide.DFB_SULPHIDE_API(6)
        result = ['Sulfide Stress Cracking Damage Factor ', obj['Sulphide1'], obj['Sulphide2'], obj['Sulphide3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def hicsohich2s(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['PH'] = rwstream.waterph
        obj['H2SContent'] = rwstream.h2sinwater
        obj['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['PWHT'] = bool(rwequipment.pwht)

        obj['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        obj['OnlineMonitoring'] = rwequipment.onlinemonitoring
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        obj['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)

        Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(obj['PH'], obj['H2SContent'], obj['PRESENT_CYANIDE'],
                                                     obj['CRACK_PRESENT'], obj['PWHT'], obj['SULFUR_CONTENT'],
                                                     obj['OnlineMonitoring'], obj['CARBON_ALLOY'],
                                                     obj['AQUEOUS_OPERATOR'], obj['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                     0, rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        obj['HicsohicH2s1'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
        obj['HicsohicH2s2'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(3)
        obj['HicsohicH2s3'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(6)
        result = ['HIC/SOHIC-H2S Damage Factor ', obj['HicsohicH2s1'], obj['HicsohicH2s2'], obj['HicsohicH2s3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def alkaline(proposalID):
    try:
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        # rwcoat = models.RwCoating.objects.get(id=proposalID)
        # rwequipment = models.RwEquipment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        obj = {}
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname

        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        CRACK_PRESENT = bool(rwcomponent.crackspresent)
        obj['CRACK_PRESENT'] = CRACK_PRESENT

        PWHT = bool(rwequipment.pwht)
        # PWHT=bool(1)
        CO3_CONTENT = rwstream.co3concentration
        PH = rwstream.waterph
        CARBON_ALLOY = bool(rwmaterial.carbonlowalloy)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)

        AQUEOUS_OPERATOR = bool(rwstream.aqueousoperation)
        obj['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        Alkaline = Detail_DM_CAL.Df_Cacbonate(CRACK_PRESENT, PWHT, CO3_CONTENT, PH, CARBON_ALLOY, AQUEOUS_OPERATOR,
                                              'E', 0, rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                              ComponentNumber)
        obj['ALKALINE_INSP_EFF'] = Alkaline.CACBONATE_INSP_EFF
        obj['ALKALINE_INSP_NUM'] = Alkaline.CACBONATE_INSP_NUM
        obj['co3'] = Alkaline.CO3_CONTENT
        obj['ph'] = Alkaline.PH
        obj['Susceptibility'] = Alkaline.GET_SUSCEPTIBILITY_CARBONATE()
        obj['PWHT'] = PWHT
        obj['SVI'] = Alkaline.SVI_CARBONATE()
        obj['age1'] = Alkaline.GET_AGE()
        obj['age2'] = Alkaline.GET_AGE() + 3
        obj['age3'] = Alkaline.GET_AGE() + 6
        obj['base1'] = Alkaline.DFB_CACBONATE_API(0)
        obj['base2'] = Alkaline.DFB_CACBONATE_API(3)
        obj['base3'] = Alkaline.DFB_CACBONATE_API(6)
        obj['CACBONATE1'] = Alkaline.DF_CACBONATE_API(0)
        obj['CACBONATE2'] = Alkaline.DF_CACBONATE_API(3)
        obj['CACBONATE3'] = Alkaline.DF_CACBONATE_API(6)
        obj2 = {}
        obj2['PWHT'] = True
        obj2['CRACK_PRESENT'] = False
        obj2['ph'] = 4
        obj2['CARBON_ALLOY'] = True
        obj2['AQUEOUS_OPERATOR'] = True
        Alkaline2 = Detail_DM_CAL.Df_Cacbonate(False, bool(1), CO3_CONTENT, obj2['ph'], CARBON_ALLOY,
                                               AQUEOUS_OPERATOR, 'E', 0, rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
        obj2['CACBONATE1'] = Alkaline2.DF_CACBONATE_API(0)
        obj2['CACBONATE2'] = Alkaline2.DF_CACBONATE_API(3)
        obj2['CACBONATE3'] = Alkaline2.DF_CACBONATE_API(6)
        result = ['Carbonate Cracking Damage Factor ', obj2['CACBONATE1'], obj2['CACBONATE2'], obj2['CACBONATE3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def PASCC(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['ExposedSH2OOperation'] = bool(rwequipment.presencesulphideso2)
        obj['ExposedSH2OShutdown'] = bool(rwequipment.presencesulphideso2shutdown)
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['ThermalHistory'] = rwequipment.thermalhistory
        obj['PTAMaterial'] = rwmaterial.ptamaterialcode
        obj['DOWNTIME_PROTECTED'] = bool(rwequipment.downtimeprotectionused)
        obj['PTA_SUSCEP'] = bool(rwmaterial.ispta)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['NICKEL_ALLOY'] = bool(rwmaterial.nickelbased)
        obj['EXPOSED_SULFUR'] = bool(rwstream.exposedtosulphur)

        PASCC = Detail_DM_CAL.Df_PTA(obj['CRACK_PRESENT'], obj['ExposedSH2OOperation'], obj['ExposedSH2OShutdown'],
                                     obj['MAX_OP_TEMP'], obj['ThermalHistory'], obj['PTAMaterial'],
                                     obj['DOWNTIME_PROTECTED'], obj['PTA_SUSCEP'],
                                     obj['CARBON_ALLOY'], obj['NICKEL_ALLOY'], obj['EXPOSED_SULFUR'], 'E', 0,
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        obj['PASCC1'] = PASCC.DF_PTA_API(0)
        obj['PASCC2'] = PASCC.DF_PTA_API(3)
        obj['PASCC3'] = PASCC.DF_PTA_API(6)
        result = ['Polythionic Acid Cracking Damage Factor ', obj['PASCC1'], obj['PASCC2'], obj['PASCC3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def CLSCC(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['ph'] = rwstream.waterph
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        obj['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        obj['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)

        CLSCC = Detail_DM_CAL.Df_CLSCC(obj['CRACK_PRESENT'], obj['ph'], obj['MAX_OP_TEMP'], obj['MIN_OP_TEMP'],
                                       obj['CHLORIDE_ION_CONTENT'], obj['INTERNAL_EXPOSED_FLUID_MIST'],
                                       obj['AUSTENITIC_STEEL']
                                       , 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        obj['CLSCC1'] = CLSCC.DF_CLSCC_API(0)
        obj['CLSCC2'] = CLSCC.DF_CLSCC_API(3)
        obj['CLSCC3'] = CLSCC.DF_CLSCC_API(6)
        result = ['CLSCC Damage Factor', obj['CLSCC1'], obj['CLSCC2'], obj['CLSCC3']]
    except Exception as e:
        print(e)
        raise Http404
    return result


def HSCHF(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['HF_PRESENT'] = bool(rwstream.hydrofluoric)

        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['PWHT'] = bool(rwequipment.pwht)
        obj['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness

        HSCHF = Detail_DM_CAL.Df_HSCHF(obj['CRACK_PRESENT'], obj['HF_PRESENT'], obj['CARBON_ALLOY'],
                                       obj['PWHT'], obj['BRINNEL_HARDNESS'], 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        obj['HSCHF1'] = HSCHF.DF_HSCHF_API(0)
        obj['HSCHF2'] = HSCHF.DF_HSCHF_API(3)
        obj['HSCHF3'] = HSCHF.DF_HSCHF_API(6)
        result = ['HSCHF Damage Factor ', obj['HSCHF1'], obj['HSCHF2'], obj['HSCHF3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def HICSOPHICHF(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['HF_PRESENT'] = bool(rwstream.hydrofluoric)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['PWHT'] = bool(rwequipment.pwht)
        obj['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        obj['OnlineMonitoring'] = rwequipment.onlinemonitoring
        HIC_SOHIC_HF = Detail_DM_CAL.Df_HIC_SOHIC_HF(obj['CRACK_PRESENT'], obj['HF_PRESENT'], obj['CARBON_ALLOY'],
                                                     obj['PWHT'], obj['SULFUR_CONTENT'], obj['OnlineMonitoring'],
                                                     'E', 0,
                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        obj['HICSOHICHF1'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(0)
        obj['HICSOHICHF2'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(3)
        obj['HICSOHICHF3'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(6)
        result = ['HIC/SOHIC_HF Damage Factor ', obj['HICSOHICHF1'], obj['HICSOHICHF2'], obj['HICSOHICHF3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def EXTERNAL_CORROSION(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = comp.componentnumber
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        # obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        externalcoatingquality = rwcoat.externalcoatingquality
        evironment = rwequipment.externalenvironment
        percent2 = rwexcor.plus6toplus32
        percent3 = rwexcor.plus32toplus71
        percent4 = rwexcor.plus71toplus107
        percent5 = rwexcor.plus107toplus121
        percent6 = rwexcor.plus121toplus135
        support = bool(rwcoat.supportconfignotallowcoatingmaint)
        interfacsoilwater = bool(rwequipment.interfacesoilwater)
        materialexpose = bool(rwequipment.materialexposedtoclext)
        carbonlowablloy = bool(rwmaterial.carbonlowalloy)
        maxtemp = rwstream.maxoperatingtemperature
        mintemp = rwstream.minoperatingtemperature
        APIcomponenttype = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        nominalthickness = rwcomponent.nominalthickness
        currentthickness = rwcomponent.currentthickness
        weldjoint = rwcomponent.weldjointefficiency
        yeild = rwmaterial.yieldstrength
        tensile = rwmaterial.tensilestrength
        shapefactor = comptype.shapefactor
        minthickreq = rwcomponent.minreqthickness
        # obj['ExternalCoatingInstallationDate'] = rwcoat.externalcoatingdate.strftime('%Y-%m-%d')

        minstructural = rwcomponent.minstructuralthickness
        confidence = rwcomponent.confidencecorrosionrate
        allowstress = rwcomponent.allowablestress
        # obj['MinThickReq'] = rwcomponent.minreqthickness
        structurathickness = rwcomponent.structuralthickness
        designpressure = rwmaterial.designpressure
        diameter = rwcomponent.nominaldiameter
        API_COMPONENT_TYPE_NAME = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        externalexpose = rwstream.materialexposedtoclint
        assessmentdate = rwassessment.assessmentdate
        EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE, externalcoatingquality,
                                                                 evironment, percent2, percent3, percent4, percent5,
                                                                 percent6, support,
                                                                 interfacsoilwater, externalexpose, carbonlowablloy,
                                                                 maxtemp,
                                                                 mintemp, "E", 0, 0, APIcomponenttype,
                                                                 nominalthickness, currentthickness,
                                                                 weldjoint, yeild, tensile, shapefactor, minstructural,
                                                                 confidence, allowstress, minthickreq,
                                                                 structurathickness, designpressure, diameter,
                                                                 assessmentdate, COMPONENT_INSTALL_DATE,
                                                                 ComponentNumber)
        obj['extf1'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
        obj['extf2'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(3)
        obj['extf3'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(6)
        result = ['External Corrosion Damage Factor ', obj['extf1'], obj['extf1'], obj['extf1']]


    except Exception as e:
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        raise Http404
    return result


def CUIF(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        obj['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        obj['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        obj['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        obj['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        obj['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        obj['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        obj['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        obj['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        obj['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        obj['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        obj['INSULATION_CONDITION'] = rwcoat.insulationcondition
        obj['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        obj['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        obj['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj['CUI_INSP_EFF'] = 'E'
        obj['CUI_INSP_NUM'] = 0
        obj['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        obj['NomalThick'] = rwcomponent.nominalthickness
        obj['CurrentThick'] = rwcomponent.currentthickness
        obj['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        obj['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        obj['ShapeFactor'] = comptype.shapefactor
        obj['Pressure'] = rwmaterial.designpressure
        obj['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        obj['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        obj['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        obj['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        obj['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        obj['AllowableStress'] = rwcomponent.allowablestress
        obj['MinThickReq'] = rwcomponent.minreqthickness
        obj['StructuralThickness'] = rwcomponent.structuralthickness
        obj['Pressure'] = rwmaterial.designpressure
        obj['Diametter'] = rwcomponent.nominaldiameter
        obj['ShapeFactor'] = comptype.shapefactor
        obj['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        obj['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        obj['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        CUIF = Detail_DM_CAL.Df_CUI(obj['EXTERNAL_EVIRONMENT'], obj['CUI_PERCENT_2'], obj['CUI_PERCENT_3'],
                                    obj['CUI_PERCENT_4'], obj['CUI_PERCENT_5'], obj['CUI_PERCENT_6'],
                                    obj['CUI_PERCENT_7'], obj['CUI_PERCENT_8'], obj['CUI_PERCENT_9'],
                                    obj['INSULATION_TYPE'], obj['PIPING_COMPLEXITY'],
                                    obj['INSULATION_CONDITION'], obj['SUPPORT_COATING'],
                                    obj['INTERFACE_SOIL_WATER'], obj['EXTERNAL_EXPOSED_FLUID_MIST']
                                    , obj['CARBON_ALLOY'], obj['MAX_OP_TEMP'], obj['MIN_OP_TEMP'],
                                    obj['CUI_INSP_EFF'], obj['CUI_INSP_NUM'], obj['APIComponentType']
                                    , obj['NomalThick'], obj['CurrentThick'], obj['CR_Confidents_Level'],
                                    obj['MINIUM_STRUCTURAL_THICKNESS_GOVERS'], obj['WeldJointEffciency'],
                                    obj['YieldStrengthDesignTemp'], obj['TensileStrengthDesignTemp'],
                                    obj['AllowableStress'], obj['MinThickReq'], obj['StructuralThickness'],
                                    obj['Pressure'], obj['Diametter'], obj['ShapeFactor'],
                                    obj['COMPONENT_INSTALL_DATE'], obj['EXTERN_COAT_QUALITY'],
                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber)
        obj['CUIF1'] = CUIF.DF_CUI_API(0)
        obj['CUIF2'] = CUIF.DF_CUI_API(3)
        obj['CUIF3'] = CUIF.DF_CUI_API(6)
        result = ['Corrosion Under Insulation Damage Factor ', obj['CUIF1'], obj['CUIF2'], obj['CUIF3']]
        return result
    except Exception as e:
        print(e)
        return 0


def extCLSCC(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        obj['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        obj['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature

        CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(obj['CRACK_PRESENT'], obj['EXTERNAL_EVIRONMENT'], obj['MAX_OP_TEMP'],
                                              'E', 0,
                                              obj['AUSTENITIC_STEEL'], obj['EXTERNAL_EXPOSED_FLUID_MIST'],
                                              obj['MIN_DESIGN_TEMP'],

                                              rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                              ComponentNumber)
        obj['EXTERN_CLSCC1'] = CLSCC.DF_EXTERN_CLSCC_API(0)
        obj['EXTERN_CLSCC2'] = CLSCC.DF_EXTERN_CLSCC_API(3)
        obj['EXTERN_CLSCC3'] = CLSCC.DF_EXTERN_CLSCC_API(6)
        result = ['External CLSCC Damage Factor ', obj['EXTERN_CLSCC1'], obj['EXTERN_CLSCC2'], obj['EXTERN_CLSCC3']]


    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        raise Http404
    return result


def cuiCLSCC(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        obj['INSULATION_CONDITION'] = rwcoat.insulationcondition
        obj['INSULATION_CHLORIDE'] = bool(rwcoat.insulationcontainschloride)
        obj['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        obj['EXTERNAL_INSULATION'] = bool(rwcoat.externalinsulation)

        obj['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        obj['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(obj['CRACK_PRESENT'], obj['EXTERNAL_EVIRONMENT'], obj['MAX_OP_TEMP'],
                                               obj['PIPING_COMPLEXITY'], obj['INSULATION_CONDITION'],
                                               obj['INSULATION_CHLORIDE'], 'E', 0,
                                               obj['AUSTENITIC_STEEL'], obj['EXTERNAL_INSULATION'],
                                               obj['EXTERNAL_EXPOSED_FLUID_MIST'], obj['MIN_OP_TEMP'],
                                               obj['EXTERN_COAT_QUALITY'],

                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
        obj['CUI_CLSCC1'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
        obj['CUI_CLSCC2'] = CUI_CLSCC.DF_CUI_CLSCC_API(3)
        obj['CUI_CLSCC3'] = CUI_CLSCC.DF_CUI_CLSCC_API(6)
        result = ['External CUI CLSCC Damage Factor ', obj['CUI_CLSCC1'], obj['CUI_CLSCC2'], obj['CUI_CLSCC3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def HTHA(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['HTHA_PRESSURE'] = rwstream.h2spartialpressure * 0.006895
        obj['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj['HTHADamageObserved'] = rwcomponent.hthadamage
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['MATERIAL_SUSCEP_HTHA'] = bool(rwmaterial.ishtha)
        obj['HTHA_MATERIAL'] = rwmaterial.hthamaterialcode
        obj['Hydrogen'] = rwstream.hydrogen

        HTHA = Detail_DM_CAL.DF_HTHA(obj['HTHA_PRESSURE'], obj['CRITICAL_TEMP'], obj['HTHADamageObserved'],
                                     obj['MAX_OP_TEMP'], obj['MATERIAL_SUSCEP_HTHA'], obj['HTHA_MATERIAL'],
                                     obj['Hydrogen'],
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        obj['HTHA1'] = HTHA.DF_HTHA_API(0)
        obj['HTHA2'] = HTHA.DF_HTHA_API(3)
        obj['HTHA3'] = HTHA.DF_HTHA_API(6)
        result = ['High Temperature Hydrogen Attack Damage Factor ', obj['HTHA1'], obj['HTHA2'], obj['HTHA3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def BRITTLE(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj['PWHT'] = bool(rwequipment.pwht)
        obj['REF_TEMP'] = rwmaterial.referencetemperature
        obj['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness
        obj['FABRICATED_STEEL'] = bool(rwcomponent.fabricatedsteel)
        obj['EQUIPMENT_SATISFIED'] = bool(rwcomponent.equipmentsatisfied)
        obj['NOMINAL_OPERATING_CONDITIONS'] = bool(rwcomponent.nominaloperatingconditions)
        obj['CET_THE_MAWP'] = bool(rwcomponent.cetgreaterorequal)
        obj['CYCLIC_SERVICE'] = bool(rwcomponent.cyclicservice)
        obj['PresenceCyanides'] = bool(rwstream.cyanide)
        obj['EQUIPMENT_CIRCUIT_SHOCK'] = bool(rwcomponent.equipmentcircuitshock)
        obj['NomalThick'] = rwcomponent.nominalthickness
        if obj['NomalThick'] <= 12.7:
            obj['equal_127'] = True
        else:
            obj['equal_127'] = False
        if obj['NomalThick'] <= 50.8:
            obj['equal_508'] = True
        else:
            obj['equal_508'] = False
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        BRITTLE = Detail_DM_CAL.DF_BRITTLE(obj['PRESSSURE_CONTROL'], obj['MIN_TEMP_PRESSURE'], obj['CRITICAL_TEMP'],
                                           obj['PWHT'], obj['REF_TEMP'], obj['BRITTLE_THICK'],
                                           obj['FABRICATED_STEEL'], obj['EQUIPMENT_SATISFIED'],
                                           obj['NOMINAL_OPERATING_CONDITIONS'],
                                           obj['CET_THE_MAWP'], obj['CYCLIC_SERVICE'],
                                           obj['EQUIPMENT_CIRCUIT_SHOCK'], obj['NomalThick'], obj['CARBON_ALLOY'],
                                           obj['MIN_DESIGN_TEMP'], obj['MAX_OP_TEMP'],
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)
        obj['BRITTLE1'] = BRITTLE.DF_BRITTLE(0)
        obj['BRITTLE2'] = BRITTLE.DF_BRITTLE_API(3)
        obj['BRITTLE3'] = BRITTLE.DF_BRITTLE_API(6)
        result = ['Brittle Facture Damage Factor ', obj['BRITTLE1'], obj['BRITTLE2'], obj['BRITTLE3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def TEMP_EMBRITTLE(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['TEMPER_SUSCEP'] = bool(rwmaterial.temper)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj['REF_TEMP'] = rwmaterial.referencetemperature
        obj['DELTA_FATT'] = rwcomponent.deltafatt
        obj['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj['PWHT'] = bool(rwequipment.pwht)
        obj['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness

        obj['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature

        TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(obj['TEMPER_SUSCEP'], obj['CARBON_ALLOY'],
                                                         obj['MAX_OP_TEMP'], obj['MIN_OP_TEMP'],
                                                         obj['PRESSSURE_CONTROL'], obj['MIN_TEMP_PRESSURE'],
                                                         obj['REF_TEMP'],
                                                         obj['DELTA_FATT'], obj['CRITICAL_TEMP'], obj['PWHT'],
                                                         obj['BRITTLE_THICK'], obj['MIN_DESIGN_TEMP'],
                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
        obj['TEMP_EMBRITTLE1'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
        obj['TEMP_EMBRITTLE2'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(3)
        obj['TEMP_EMBRITTLE3'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(6)
        result = ['Temper Embrittlement Damage Factor ', obj['TEMP_EMBRITTLE1'], obj['TEMP_EMBRITTLE2'],
                  obj['TEMP_EMBRITTLE3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def d885(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CHROMIUM_12'] = bool(rwmaterial.chromemoreequal12)
        obj['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj['REF_TEMP'] = rwmaterial.referencetemperature
        obj['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        df885 = Detail_DM_CAL.Df_885(obj['CHROMIUM_12'], obj['MIN_OP_TEMP'], obj['MAX_OP_TEMP'],
                                     obj['PRESSSURE_CONTROL'], obj['MIN_TEMP_PRESSURE'], obj['REF_TEMP'],
                                     obj['CRITICAL_TEMP'], obj['MIN_DESIGN_TEMP'],
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        obj['f885f1'] = df885.DF_885_API(0)
        obj['f885f2'] = df885.DF_885_API(3)
        obj['f885f3'] = df885.DF_885_API(6)
        result = ['885F Embrittlement Damage Factor ', obj['f885f1'], obj['f885f2'], obj['f885f3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


def SIGMA(proposalID):
    try:
        obj = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        # obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['MIN_TEM'] = rwstream.minoperatingtemperature
        obj['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        obj['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation

        obj['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj['PERCENT_SIGMA'] = rwmaterial.sigmaphase
        # chua thay su dung MIN_DESIGN_TEMP
        obj['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        dfSigma = Detail_DM_CAL.Df_SIGMA(obj['MIN_TEM'], obj['AUSTENITIC_STEEL'], obj['MIN_OP_TEMP'],
                                         obj['MAX_OP_TEMP'],
                                         obj['PRESSSURE_CONTROL'], obj['MIN_TEMP_PRESSURE'], obj['CRITICAL_TEMP'],
                                         obj['PERCENT_SIGMA'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
        obj['SIGMA1'] = dfSigma.DF_SIGMA_API(0)
        obj['SIGMA2'] = dfSigma.DF_SIGMA_API(3)
        obj['SIGMA3'] = dfSigma.DF_SIGMA_API(6)
        result = ['Sigma Phase Embrittlement Damage Factor', obj['SIGMA1'], obj['SIGMA2'], obj['SIGMA3']]


    except Exception as e:
        print(e)
        raise Http404
    return result


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('static/image/logo/logorbi.jpg', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 16)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, str(title), 0, 0, 'C')
        # Line break
        self.ln(20)
        # Page footer
        self.set_font('Arial', size=15)
        self.cell(190, 10, 'Proposal Report', ln=1, align='R')

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def vcell(self, c_width, c_height, x_axis, text):
        wrap = c_height / 7
        wrap0 = wrap + 3
        wrap1 = 2 * wrap + 9
        wrap2 = 3 * wrap + 15
        wrap3 = 4 * wrap + 21
        wrap4 = 5 * wrap + 27
        wrap5 = 6 * wrap + 33
        wrap6 = 7 * wrap + 39
        strlen = len(text)
        if (strlen > 43):
            x = 43
            w_text = ChuanHoa(text, 43)
            self.set_x(x_axis)
            self.cell(c_width, wrap0, w_text[0], 0, 0, 0)
            self.set_x(x_axis)
            self.cell(c_width, wrap1, w_text[1], 0, 0, 0)
            try:
                self.set_x(x_axis)
                self.cell(c_width, wrap2, w_text[2], 0, 0, 0)
                try:
                    self.set_x(x_axis)
                    self.cell(c_width, wrap3, w_text[3], 0, 0, 0)
                    try:
                        self.set_x(x_axis)
                        self.cell(c_width, wrap4, w_text[4], 0, 0, 0)
                        try:
                            self.set_x(x_axis)
                            self.cell(c_width, wrap5, w_text[5], 0, 0, 0)
                            try:
                                self.set_x(x_axis)
                                self.cell(c_width, wrap6, w_text[6], 0, 0, 0)
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
            self.set_x(x_axis)
            self.cell(c_width, c_height, '', 'LTRB', 0, 'L', 0)
        else:
            self.set_x(x_axis)
            self.cell(c_width, c_height, text, 'LTRB', 0, 'L', 0)
            # def chapter_title(self, num, label):
            #     # Arial 12
            #     self.set_font('Arial', '', 12)
            #     # Background color
            #     self.set_fill_color(200, 220, 255)
            #     # Title
            #     self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
            #     # Line break
            #     self.ln(4)


def data(IDProposal):
    try:
        pdf = PDF()
        pdf.alias_nb_pages()
        # Add a page
        pdf.add_page()

        pdf.set_title(title=title)

        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size=15)

        # create a cell
        # table information
        datainfo = {}
        RwAssessment = models.RwAssessment.objects.get(id=IDProposal)
        equipment_id = RwAssessment.equipmentid_id
        component_id = RwAssessment.componentid_id
        Equipmentmaster = models.EquipmentMaster.objects.get(equipmentid=equipment_id)
        datainfo['ProposalName'] = RwAssessment.proposalname
        datadate = str(RwAssessment.assessmentdate)
        datainfo['AssessmentDate'] = datadate[:10]
        if (RwAssessment.assessmentmethod == ''):
            datainfo['AssessmentMethod'] = 'None'
        else:
            datainfo['AssessmentMethod'] = RwAssessment.assessmentmethod
        datainfo['RiskPeriod'] = RwAssessment.riskanalysisperiod
        datainfo['EquipmentNumber'] = Equipmentmaster.equipmentnumber
        designcodeid = Equipmentmaster.designcodeid_id
        siteid = Equipmentmaster.siteid_id
        manuid = Equipmentmaster.manufacturerid_id
        equipmenttypeid = Equipmentmaster.equipmenttypeid_id
        datadate = str(Equipmentmaster.commissiondate)
        datainfo['CommissionDate'] = datadate[:10]
        datainfo['EquipmentName'] = Equipmentmaster.equipmentname
        datainfo['ProcessDescription'] = Equipmentmaster.processdescription
        Site = models.Sites.objects.get(siteid=siteid)
        datainfo['SiteName'] = Site.sitename
        DesignCode = models.DesignCode.objects.get(designcodeid=designcodeid)
        datainfo['DesignCodeName'] = DesignCode.designcode
        Manu = models.Manufacturer.objects.get(manufacturerid=manuid)
        datainfo['Manu'] = Manu.manufacturername
        equipmenttype = models.EquipmentType.objects.get(equipmenttypeid=equipmenttypeid)
        datainfo['EquipmentType'] = equipmenttype.equipmenttypename
        facilityid_id = Equipmentmaster.facilityid_id
        Facility = models.Facility.objects.get(facilityid=facilityid_id)
        datainfo['Facility'] = Facility.facilityname
        Componentmaster = models.ComponentMaster.objects.get(componentid=component_id)
        datainfo['ComponentNumber'] = Componentmaster.componentnumber
        componenttype_id = Componentmaster.componenttypeid_id
        componentapi_id = Componentmaster.apicomponenttypeid
        ComponentType = models.ComponentType.objects.get(componenttypeid=componenttype_id)
        ComponentAPI = models.ApiComponentType.objects.get(apicomponenttypeid=componentapi_id)
        datainfo['ComponentType'] = ComponentType.componenttypename
        datainfo['API'] = ComponentAPI.apicomponenttypename
        datainfo['ComponentName'] = Componentmaster.componentname
        if (Componentmaster.isequipmentlinked == 0):
            datainfo['Risk'] = "No"
        else:
            datainfo['Risk'] = "Yes"

        pdf.ln(5)
        epw = pdf.w - 2 * pdf.l_margin
        col_width1 = epw
        col_width2 = epw / 2
        col_width = epw / 4

        datainfo1 = ['Assessment General Information']
        datainfo2 = ['Assessment Name:', datainfo['ProposalName']]
        datainfo20 = ['Assessment Date:', datainfo['AssessmentDate']]
        datainfo3 = ['Assessment Method:', datainfo['AssessmentMethod']]
        datainfo4 = ['Risk Analysis Period (months):', datainfo['RiskPeriod']]
        datainfo5 = ['EquipmentGeneral Information']
        datainfo6 = ['Equipment Number: ', datainfo['EquipmentNumber']]
        datainfo7 = ['Equipment Type: ', datainfo['EquipmentType']]
        datainfo8 = ['Design Code: ', datainfo['EquipmentType']]
        datainfo9 = ['Site: ', datainfo['SiteName']]
        datainfo10 = ['Facility: ', datainfo['Facility']]
        datainfo11 = ['Manufacturer: ', datainfo['Manu']]
        datainfo12 = ['Commission Date: ', datainfo['CommissionDate']]
        datainfo13 = ['Equipment Name: ', datainfo['EquipmentName']]
        datainfo14 = ['Process Description: ', 'Day la Process Description']
        datainfo15 = ['Component General Information']
        datainfo16 = ['Component Number: ', 'cai nay la Component Number']
        datainfo17 = ['Component Type: ', datainfo['ComponentType']]
        datainfo21 = ['API Component Type: ', datainfo['API']]
        datainfo18 = ['Component Name: ', 'cai nay la Component Name']
        datainfo19 = ['Risk Links to Equipment Risk: ', datainfo['Risk']]
        datainfo = [datainfo1, datainfo2, datainfo20, datainfo3, datainfo4, datainfo5, datainfo6, datainfo7, datainfo8,
                    datainfo9, datainfo10, datainfo11, datainfo12, datainfo13, datainfo14, datainfo15, datainfo16,
                    datainfo17, datainfo21, datainfo18, datainfo19]
        # print('dem= ', len(data3))
        th = pdf.font_size
        for row in datainfo:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)

        # Line break equivalent to 4 lines
        # table equipment
        dataequip = {}
        RwEquipment = models.RwEquipment.objects.get(id=IDProposal)
        if (RwEquipment.adminupsetmanagement == 0):
            dataequip['Administative'] = "No"
        else:
            dataequip['Administative'] = "Yes"
        if (RwEquipment.steamoutwaterflush == 0):
            dataequip['Steamed'] = "No"
        else:
            dataequip['Steamed'] = "Yes"
        if (RwEquipment.downtimeprotectionused == 0):
            dataequip['downtime'] = "No"
        else:
            dataequip['downtime'] = "Yes"
        if (RwEquipment.pwht == 0):
            dataequip['PWHT'] = "No"
        else:
            dataequip['PWHT'] = "Yes"
        if (RwEquipment.heattraced == 0):
            dataequip['HeatTrace'] = "No"
        else:
            dataequip['HeatTrace'] = "Yes"
        if (RwEquipment.lineronlinemonitoring == 0):
            dataequip['Liner'] = "No"
        else:
            dataequip['Liner'] = "Yes"
        dataequip['MinRequired'] = RwEquipment.minreqtemperaturepressurisation
        if (RwEquipment.materialexposedtoclext == 0):
            dataequip['Material'] = "No"
        else:
            dataequip['Material'] = "Yes"

        if (RwEquipment.pressurisationcontrolled == 0):
            dataequip['PressurisationControlled'] = "No"
        else:
            dataequip['PressurisationControlled'] = "Yes"
        if (RwEquipment.presencesulphideso2shutdown == 0):
            dataequip['PresenceShutdown'] = "No"
        else:
            dataequip['PresenceShutdown'] = "Yes"
        if (RwEquipment.interfacesoilwater == 0):
            dataequip['Soil'] = "No"
        else:
            dataequip['Soil'] = "Yes"
        if (RwEquipment.presencesulphideso2 == 0):
            dataequip['Presence'] = "No"
        else:
            dataequip['Presence'] = "Yes"

        dataequip['ExternalEnvor'] = RwEquipment.environmentsensitivity
        dataequip['ThemeHistory'] = RwEquipment.thermalhistory
        dataequip['SystemFactor'] = RwEquipment.managementfactor
        dataequip['EquipmentVolume'] = round(RwEquipment.volume, 4)
        dataequip['OnlineMonitoring'] = RwEquipment.onlinemonitoring

        pdf.ln(5)
        epw = pdf.w - 2 * pdf.l_margin
        col_width1 = epw
        col_width2 = epw / 2
        col_width = epw / 4

        dataequip1 = ['Equipment Properties']
        dataequip2 = ['Administrative Control for Upset Management: ', dataequip['Administative']]
        dataequip3 = ['Steamed Out Prior to Water Flushing: ', dataequip['Steamed']]
        dataequip4 = ['Downtime Protection Used: ', dataequip['downtime']]
        dataequip5 = ['PWHT: ', dataequip['PWHT']]
        dataequip6 = ['Heat Traced: ', dataequip['HeatTrace']]
        dataequip7 = ['Liner Online Monitoring: ', dataequip['Liner']]
        dataequip8 = ['Min. Required Temperature Before Pressurisation Allowed by Admin: ',
                      str(dataequip['MinRequired']) + u' \u00B0C']
        dataequip9 = ['Material is Exposed to Fluids, Mists or Solids Containing Chlorine Extemally: ',
                      dataequip['Material']]
        dataequip10 = ['Pressurisation Controlled by Admin: ', dataequip['PressurisationControlled']]
        dataequip11 = ['Presence of Sulphides, Moisture and Oxygen Duruing Shutdown: ', dataequip['PresenceShutdown']]
        dataequip12 = ['Interface at Soil or Water', dataequip['Soil']]
        dataequip13 = ['Presence of Sulphides, Moisture and Oxygen Duruing Operation: ', dataequip['Presence']]
        dataequip14 = ['External Environment: ', dataequip['ExternalEnvor']]
        dataequip15 = ['Thermal History: ', dataequip['ThemeHistory']]
        dataequip16 = ['System Management Factor: ', dataequip['SystemFactor']]
        dataequip17 = ['Equipment Volume: ', str(dataequip['EquipmentVolume']) + ' m^3']
        dataequip18 = ['Online Monitoring: ', dataequip['OnlineMonitoring']]
        dataequip = [dataequip1, dataequip2, dataequip3, dataequip4, dataequip5, dataequip6, dataequip7, dataequip8,
                     dataequip9, dataequip10, dataequip11, dataequip12, dataequip13, dataequip14, dataequip15, dataequip16,
                     dataequip17, dataequip18]
        print('ok equipment normal')
        th = pdf.font_size
        for row in dataequip:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table Component
        datacomp = {}
        component = models.RwComponent.objects.get(id=IDProposal)
        datacomp['Diameter'] = round(component.nominaldiameter, 4)
        datacomp['NormalThickness'] = round(component.nominalthickness, 4)
        datacomp['MeasuredThickness'] = round(component.currentthickness, 4)
        datacomp['RequiredThicknees'] = round(component.minreqthickness, 4)
        datacomp['CorrosionRate'] = round(component.currentcorrosionrate, 4)
        datacomp['FATT'] = component.deltafatt
        if (component.crackspresent == 0):
            datacomp['PresenceCracks'] = "No"
        else:
            datacomp['PresenceCracks'] = "Yes"
        datacomp['StructuralThickness'] = component.structuralthickness
        datacomp['Weld'] = component.weldjointefficiency
        datacomp['ComponentVolume'] = component.componentvolume
        datacomp['MaximumBrinnell'] = component.brinnelhardness
        datacomp['Allowable'] = component.allowablestress
        datacomp['Confidence'] = component.confidencecorrosionrate
        if (component.minstructuralthickness == 0):
            datacomp['MinStructurelThickness'] = "No"
        else:
            datacomp['MinStructurelThickness'] = "Yes"
        if (component.fabricatedsteel == 0):
            datacomp['Fabricatedsteel'] = "No"
        else:
            datacomp['Fabricatedsteel'] = "Yes"
        if (component.equipmentsatisfied == 0):
            datacomp['EquipmentStatisfied'] = "No"
        else:
            datacomp['EquipmentStatisfied'] = "Yes"
        if (component.nominaloperatingconditions == 0):
            datacomp['NominalOperatingConditions'] = "No"
        else:
            datacomp['NominalOperatingConditions'] = "Yes"
        if (component.cyclicservice == 0):
            datacomp['CyclicService'] = "No"
        else:
            datacomp['CyclicService'] = "Yes"
        if (component.cetgreaterorequal == 0):
            datacomp['CET'] = "No"
        else:
            datacomp['CET'] = "Yes"
        datacomp['Complexity'] = component.complexityprotrusion
        if (component.equipmentcircuitshock == 0):
            datacomp['EquipmentCircuitShock'] = "No"
        else:
            datacomp['EquipmentCircuitShock'] = "Yes"
        datacomp['BrittleFracture'] = component.brittlefracturethickness

        pdf.ln(5)
        epw = pdf.w - 2 * pdf.l_margin
        col_width1 = epw
        col_width2 = epw / 2
        col_width = epw / 4

        datacomp1 = ['Component Properties']
        datacomp2 = ['Nominal Diameter: ', str(datacomp['Diameter']) + ' mm']
        datacomp3 = ['Nominal Thickness: ', str(datacomp['NormalThickness']) + ' mm']
        datacomp4 = ['Minimum Measured Thickness: ', str(datacomp['MeasuredThickness']) + ' mm']
        datacomp5 = ['Min. Required Thickness: ', str(datacomp['RequiredThicknees']) + ' mm']
        datacomp6 = ['Current Corrosion Rate: ', str(datacomp['CorrosionRate']) + ' mm/yr']
        datacomp7 = ['Delta FATT', datacomp['FATT']]
        datacomp8 = ['Presence of Cracks: ', datacomp['PresenceCracks']]
        datacomp9 = ['Structural Thickness: ', str(datacomp['StructuralThickness']) + ' mm']
        datacomp10 = ['Weld Joint Efficiency: ', datacomp['Weld']]
        datacomp11 = ['Component Valume: ', str(datacomp['ComponentVolume']) + ' m^3']
        datacomp23 = ['Maximum brinnell Hardness of Weld: ', datacomp['MaximumBrinnell']]
        datacomp12 = ['Allowable Stress at Assessment Temperature: ', str(datacomp['Allowable']) + ' MPa']
        datacomp13 = ['Level of Confidence in Corrosion Rate: ', datacomp['Confidence']]
        datacomp14 = ['Minimum Structurel Thickness Governs: ', datacomp['MinStructurelThickness']]
        datacomp15 = [
            'It is fabricated from P-1 and P-3 steels where the design temperature is less than or equal to 343oC (650oF): ',
            datacomp['Fabricatedsteel']]
        datacomp16 = [
            'The equipment satisfied all requirements of a reecognized code or standard at the time of fabrication: ',
            datacomp['EquipmentStatisfied']]
        datacomp17 = [
            'The nominal operating conditions have been essentially the same and consistent with the specified design conditions for a significant period of time, and more severe conditions are not expected in the future: ',
            datacomp['NominalOperatingConditions']]
        datacomp18 = ['Cyclic service, fatigue or vibration service is not a design requirement per design code: ',
                      datacomp['CyclicService']]
        datacomp19 = [
            'The CET at the MAWP is greater than or equal to -29oC (-20oF) if it is a pressure vessel or -104oC(-155oF) if it is a piping circuit: ',
            datacomp['CET']]
        datacomp20 = ['Complexity of Protrusions: ', datacomp['Complexity']]
        datacomp21 = ['The equipment or circuit is no subject to shock chilling: ', datacomp['EquipmentCircuitShock']]
        datacomp22 = ['Brittle Fracture Governing Thickness: ', str(datacomp['BrittleFracture']) + ' mm']
        datacomp = [datacomp1, datacomp2, datacomp3, datacomp4, datacomp5, datacomp6, datacomp7, datacomp8, datacomp9,
                    datacomp10, datacomp11, datacomp23, datacomp12, datacomp13, datacomp14, datacomp15, datacomp16,
                    datacomp17, datacomp18, datacomp19, datacomp20, datacomp21, datacomp22]

        th = pdf.font_size
        for row in datacomp:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table Operating Conditions
        dataopera = {}
        Stream = models.RwStream.objects.get(id=IDProposal)
        Extcor = models.RwExtcorTemperature.objects.get(id=IDProposal)
        dataopera['maxOT'] = round(Stream.maxoperatingtemperature, 4)
        dataopera['minOT'] = round(Stream.minoperatingtemperature, 4)
        dataopera['maxOP'] = round(Stream.maxoperatingpressure, 4)
        dataopera['minOP'] = round(Stream.minoperatingpressure, 4)
        dataopera['criticalTemp'] = round(Stream.criticalexposuretemperature, 4)
        dataopera['flowrate'] = round(Stream.flowrate, 4)
        dataopera['_12_8'] = round(Extcor.minus12tominus8, 4)
        dataopera['_86'] = round(Extcor.minus8toplus6, 4)
        dataopera['632'] = round(Extcor.plus6toplus32, 4)
        dataopera['3271'] = round(Extcor.plus32toplus71, 4)
        dataopera['71107'] = round(Extcor.plus71toplus107, 4)
        dataopera['107121'] = round(Extcor.plus107toplus121, 4)
        dataopera['121135'] = round(Extcor.plus121toplus135, 4)
        dataopera['135162'] = round(Extcor.plus135toplus162, 4)
        dataopera['162176'] = round(Extcor.plus162toplus176, 4)
        dataopera['176plus'] = round(Extcor.morethanplus176, 4)
        dataopera['OpHydroPressure'] = round(Stream.hydrogen, 4)

        dataopera1 = ['Operating Conditions Properties']
        dataopera2 = ['Max. Operating Temperature: ', str(dataopera['maxOT']) + u' \u00B0C']
        dataopera3 = ['Min. Operating Temperature: ', str(dataopera['minOT']) + u' \u00B0C']
        dataopera4 = ['Max. Operating Pressure: ', str(dataopera['maxOP']) + ' MPa']
        dataopera5 = ['Min. Operating Pressure: ', str(dataopera['minOP']) + ' MPa']
        dataopera6 = ['Critical Exposure Temperature: ', str(dataopera['criticalTemp']) + u' \u00B0C']
        dataopera7 = ['Flow Rate: ', str(dataopera['flowrate']) + ' m^3/hr']
        dataopera8 = [u'% Operating at -12\u00B0C to -8\u00B0C: ', str(dataopera['_12_8']) + ' %']
        dataopera9 = [u'% Operating at -8\u00B0C to 6\u00B0C: ', str(dataopera['_86']) + ' %']
        dataopera10 = [u'% Operating at 6\u00B0C to 32\u00B0C: ', str(dataopera['632']) + ' %']
        dataopera11 = [u'% Operating at 32\u00B0C to 71\u00B0C: ', str(dataopera['3271']) + ' %']
        dataopera12 = [u'% Operating at 71\u00B0C to 107\u00B0C: ', str(dataopera['71107']) + ' %']
        dataopera13 = [u'% Operating at 107\u00B0C to 121\u00B0C: ', str(dataopera['107121']) + ' %']
        dataopera14 = [u'% Operating at 121\u00B0C to 135\u00B0C: ', str(dataopera['121135']) + ' %']
        dataopera15 = [u'% Operating at 135\u00B0C to 162\u00B0C: ', str(dataopera['135162']) + ' %']
        dataopera16 = [u'% Operating at 162\u00B0C to 176\u00B0C: ', str(dataopera['162176']) + ' %']
        dataopera17 = [u'% Operating at 176\u00B0C or Above: ', str(dataopera['176plus']) + ' %']
        dataopera18 = [u'Operating Hydrogen Partial Pressure: ', str(dataopera['OpHydroPressure']) + ' MPa']
        dataopera = [dataopera1, dataopera2, dataopera3, dataopera4, dataopera5, dataopera6, dataopera7, dataopera8,
                     dataopera9, dataopera10, dataopera11, dataopera12, dataopera12, dataopera13, dataopera14, dataopera15,
                     dataopera16, dataopera17, dataopera18]
        th = pdf.font_size
        for row in dataopera:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table Streaam
        datastream = {}
        inputCA = models.RwInputCaLevel1.objects.get(id=IDProposal)
        datastream['ModelFluid'] = inputCA.model_fluid
        datastream['ToxicFluid'] = inputCA.toxic_fluid
        datastream['FluidPhase'] = Stream.storagephase
        datastream['ToxicPercent'] = round(Stream.releasefluidpercenttoxic, 4)
        datastream['LiquidLevel'] = round(Stream.liquidlevel, 4)
        datastream['NAOH'] = round(Stream.naohconcentration, 4)
        datastream['ChlorideIon'] = round(Stream.chloride, 4)
        datastream['Co3'] = round(Stream.co3concentration, 4)
        datastream['H2S'] = round(Stream.h2sinwater, 4)
        datastream['PH'] = round(Stream.waterph, 4)
        datastream['maxOT'] = round(Stream.maxoperatingtemperature, 4)
        datastream['minOT'] = round(Stream.minoperatingtemperature, 4)
        datastream['maxOP'] = round(Stream.maxoperatingpressure, 4)
        datastream['minOP'] = round(Stream.minoperatingpressure, 4)
        datastream['OHPressure'] = "day la Operating Hydrogen Partial Pressure"
        datastream['flowrate'] = Stream.flowrate
        if (Stream.toxicconstituent == 0):
            datastream['ToxicConstituents'] = "No"
        else:
            datastream['ToxicConstituents'] = "Yes"
        if (Stream.exposedtogasamine == 0):
            datastream['ExposedtoAcidGas'] = "No"
        else:
            datastream['ExposedtoAcidGas'] = "Yes"
        datastream['ExposedtoAmine'] = Stream.exposuretoamine
        datastream['AmineSolution'] = Stream.aminesolution
        if (Stream.aqueousoperation == 0):
            datastream['AqueousOperating'] = "No"
        else:
            datastream['AqueousOperating'] = "Yes"
        if (Stream.aqueousshutdown == 0):
            datastream['AqueousShutdown'] = "No"
        else:
            datastream['AqueousShutdown'] = "Yes"
        if (Stream.h2s == 0):
            datastream['EnviH2S'] = "No"
        else:
            datastream['EnviH2S'] = "Yes"
        if (Stream.hydrofluoric == 0):
            datastream['PresenceHydrofluoric'] = "No"
        else:
            datastream['PresenceHydrofluoric'] = "Yes"
        if (Stream.cyanide == 0):
            datastream['Cyanides'] = "No"
        else:
            datastream['Cyanides'] = "Yes"
        if (Stream.hydrogen == 0):
            datastream['Hydrogen'] = "No"
        else:
            datastream['Hydrogen'] = "Yes"
        if (Stream.caustic == 0):
            datastream['Caustic'] = "No"
        else:
            datastream['Caustic'] = "Yes"
        if (Stream.exposedtosulphur == 0):
            datastream['SulphurBeaning'] = "No"
        else:
            datastream['SulphurBeaning'] = "Yes"
        if (Stream.materialexposedtoclint == 0):
            datastream['material'] = "No"
        else:
            datastream['material'] = "Yes"
        if (Stream.exposedtogasamine == 0):
            datastream['AcidGas'] = "No"
        else:
            datastream['AcidGas'] = "Yes"
        datastream1 = ['Stream/Process Flow']
        datastream2 = ['Fluid']
        datastream3 = ['Model Fluid: ', datastream['ModelFluid']]
        datastream4 = ['Toxic Fluid: ', datastream['ToxicFluid']]
        datastream5 = ['Phase of Fluid at Storage: ', datastream['FluidPhase']]
        datastream6 = ['Toxic Fluid percentage(%): ', datastream['ToxicPercent']]
        datastream7 = ['Liquid Level(%): ', datastream['LiquidLevel']]
        datastream8 = ['Operating Condition']
        datastream9 = ['Maxium Operating Temperature: ', str(datastream['maxOT']) + u' \u00B0C']
        datastream10 = ['Minium Operating Temperature: ', str(datastream['minOT']) + u' \u00B0C']
        datastream11 = ['Maxium Operating Pressure:', str(datastream['maxOP']) + ' MPa']
        datastream12 = ['Minium Operating Pressure: ', str(datastream['minOP']) + ' MPa']
        datastream13 = ['Operating Hydrogen Partial Pressure: ', str(datastream['OHPressure']) + ' MPa']
        datastream14 = ['Flow Rate:', str(datastream['flowrate']) + ' m^3/yr']
        datastream15 = ['Environment Condition']
        datastream16 = ['NaOH Concentration(%): ', datastream['NAOH']]
        datastream17 = ['Chloride Ion (ppm): ', datastream['ChlorideIon']]
        datastream18 = ['CO3 Concentration in Water (ppm): ', datastream['Co3']]
        datastream19 = ['H2S Content in Water (ppm): ', datastream['H2S']]
        datastream20 = ['pH of Water: ', datastream['PH']]
        datastream21 = ['Toxic Constituents: ', datastream['ToxicConstituents']]
        datastream22 = ['Exposed To Acid Gas Treating Amine: ', datastream['ExposedtoAcidGas']]
        datastream23 = ['Exposed To Amine: ', datastream['ExposedtoAmine']]
        datastream24 = ['Amine Solution Composition: ', datastream['AmineSolution']]
        datastream25 = ['Aqueous Phase During Operation: ', datastream['AqueousOperating']]
        datastream26 = ['Aqueous Phase During Shutdown: ', datastream['AqueousShutdown']]
        datastream27 = ['Environment Consatins H2S: ', datastream['EnviH2S']]
        datastream28 = ['Presence of Hydrofluoric Acid: ', datastream['PresenceHydrofluoric']]
        datastream29 = ['Presence of Cyanides: ', datastream['Cyanides']]
        datastream30 = ['Process Contains Hydrogen: ', datastream['Hydrogen']]
        datastream31 = ['Environment Contains Caustic in Any Concentration: ', datastream['Caustic']]
        datastream32 = ['Exposed to Sulphur-Beaning Compounds: ', datastream['SulphurBeaning']]
        datastream33 = ['Material is Exposed to Fluids, Mists, or Solids: ', datastream['material']]
        datastream34 = ['Exposed to Acid Gas Treating Amine: ', datastream['ExposedtoAcidGas']]
        datastream = [datastream1, datastream2, datastream3, datastream4, datastream5, datastream6, datastream7,
                      datastream8, datastream9, datastream10, datastream11, datastream12, datastream13
            , datastream14, datastream15, datastream16, datastream17, datastream18, datastream19, datastream20,
                      datastream21, datastream22, datastream23, datastream24, datastream25, datastream26, datastream27,
                      datastream28, datastream29, datastream30, datastream31, datastream32, datastream33, datastream34]
        th = pdf.font_size
        for row in datastream:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)

        # table material
        datamaterial = {}
        RwMaterial = models.RwMaterial.objects.get(id=IDProposal)
        datamaterial['Material'] = RwMaterial.materialname
        datamaterial['DesignPressure'] = round(RwMaterial.designpressure, 4)
        datamaterial['DesignTemperature'] = round(RwMaterial.designtemperature, 4)
        datamaterial['TensileStrength'] = round(RwMaterial.tensilestrength, 4)
        datamaterial['YieldStrength'] = round(RwMaterial.yieldstrength, 4)
        datamaterial['ReferenceTem'] = round(RwMaterial.referencetemperature, 4)
        datamaterial['SigmaPhase'] = round(RwMaterial.sigmaphase, 4)
        datamaterial['CorrosionAllow'] = RwMaterial.corrosionallowance
        datamaterial['SulfuContent'] = RwMaterial.sulfurcontent
        datamaterial['MinDesignTem'] = round(RwMaterial.mindesigntemperature, 4)
        datamaterial['HeatTreatment'] = RwMaterial.heattreatment
        datamaterial['MaterialCostFactor'] = round(RwMaterial.costfactor, 4)
        datamaterial['MaxDesignTem'] = round(RwMaterial.designtemperature, 4)
        datamaterial['PTAMataterialGrade'] = RwMaterial.ptamaterialcode
        datamaterial['SteelProductForm'] = RwMaterial.steelproductform
        datamaterial['HTHAMaterialGrade'] = RwMaterial.hthamaterialcode
        if (RwMaterial.austenitic == 0):
            datamaterial['AusteniticSteel'] = 'No'
        else:
            datamaterial['AusteniticSteel'] = 'Yes'
        if (RwMaterial.carbonlowalloy == 0):
            datamaterial['CarbonLowAlloy'] = 'No'
        else:
            datamaterial['CarbonLowAlloy'] = 'Yes'
        if (RwMaterial.nickelbased == 0):
            datamaterial['NickelBased'] = 'No'
        else:
            datamaterial['NickelBased'] = 'Yes'
        if (RwMaterial.temper == 0):
            datamaterial['SuscestibleTemper'] = 'No'
        else:
            datamaterial['SuscestibleTemper'] = 'Yes'
        if (RwMaterial.chromemoreequal12 == 0):
            datamaterial['Chromium'] = 'No'
        else:
            datamaterial['Chromium'] = 'Yes'
        if (RwMaterial.ispta == 0):
            datamaterial['PTA'] = 'No'
        else:
            datamaterial['PTA'] = 'Yes'
        if (RwMaterial.ishtha == 0):
            datamaterial['HTHA'] = 'No'
        else:
            datamaterial['HTHA'] = 'Yes'
        datamaterial1 = ['Material Properties']
        datamaterial2 = ['Material:', datamaterial['Material']]
        datamaterial3 = ['Design Pressure: ', str(datamaterial['DesignPressure']) + ' MPa']
        datamaterial4 = ['Design Temperature: ', str(datamaterial['DesignTemperature']) + u' \u00B0C']
        datamaterial5 = ['Tensile Strength: ', str(datamaterial['TensileStrength']) + ' MPa']
        datamaterial6 = ['Yield Strength: ', str(datamaterial['YieldStrength']) + ' MPa']
        datamaterial7 = ['Reference Temperature', str(datamaterial['ReferenceTem']) + u' \u00B0C']
        datamaterial8 = ['Sigma Phase(%): ', datamaterial['SigmaPhase']]
        datamaterial9 = ['Corrosion Allowance: ', str(datamaterial['CorrosionAllow']) + ' mm']
        datamaterial10 = ['Austenitic Steel: ', datamaterial['AusteniticSteel']]
        datamaterial11 = ['Carbon or Low Alloy Steel: ', datamaterial['CarbonLowAlloy']]
        datamaterial12 = ['Nickel-based Alloy: ', datamaterial['NickelBased']]
        datamaterial13 = ['Susceptible to Temper: ', datamaterial['SuscestibleTemper']]
        datamaterial14 = ['Sulfur Content: ', datamaterial['SulfuContent']]
        datamaterial15 = ['Chromium >= 12%: ', datamaterial['Chromium']]
        datamaterial16 = ['Min. Design Temperature: ', str(datamaterial['MinDesignTem']) + u' \u00B0C']
        datamaterial17 = ['Heat Treatment: ', datamaterial['HeatTreatment']]
        datamaterial18 = ['Material Cost Factor: ', str(datamaterial['MaterialCostFactor']) + u' \u00B0C']
        datamaterial19 = ['Material is Susceptible to PTA: ', datamaterial['PTA']]
        datamaterial20 = ['Max. Design Temperature: ', str(datamaterial['MaxDesignTem']) + u' \u00B0C']
        datamaterial21 = ['PTA Material Grade: ', datamaterial['PTAMataterialGrade']]
        datamaterial22 = ['Material is Susceptible to HTHA: ', datamaterial['HTHA']]
        datamaterial23 = ['Steel Product Form: ', datamaterial['SteelProductForm']]
        datamaterial24 = ['HTHA Material Grade: ', datamaterial['HTHAMaterialGrade']]
        datamaterial = [datamaterial1, datamaterial2, datamaterial3, datamaterial4, datamaterial5, datamaterial6,
                        datamaterial7,
                        datamaterial8, datamaterial9, datamaterial10, datamaterial11, datamaterial12, datamaterial13
            , datamaterial14, datamaterial15, datamaterial16, datamaterial17, datamaterial18, datamaterial19,
                        datamaterial20,
                        datamaterial21, datamaterial22, datamaterial23, datamaterial24]
        th = pdf.font_size
        for row in datamaterial:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)

        # table coating
        datacoating = {}
        RwCoating = models.RwCoating.objects.get(id=IDProposal)
        exdate = str(RwCoating.externalcoatingdate)
        datacoating['ExternalDate'] = exdate[:10]
        datacoating['ExternalCoatingQuality'] = RwCoating.externalcoatingquality
        datacoating['CladdingRate'] = round(RwCoating.claddingcorrosionrate, 4)
        datacoating['CladdingThickness'] = round(RwCoating.claddingthickness, 4)
        datacoating['InsulationType'] = RwCoating.externalinsulationtype
        datacoating['InsulationCondition'] = RwCoating.insulationcondition
        datacoating['LinerCondition'] = RwCoating.internallinercondition
        datacoating['LinerType'] = RwCoating.internallinertype
        if (RwCoating.internalcoating == 0):
            datacoating['InternalCoating'] = 'No'
        else:
            datacoating['InternalCoating'] = 'Yes'
        if (RwCoating.externalcoating == 0):
            datacoating['ExternalCoating'] = 'No'
        else:
            datacoating['ExternalCoating'] = 'Yes'
        if (RwCoating.supportconfignotallowcoatingmaint == 0):
            datacoating['Support'] = 'No'
        else:
            datacoating['Support'] = 'Yes'
        if (RwCoating.internalcladding == 0):
            datacoating['InternalCladding'] = 'No'
        else:
            datacoating['InternalCladding'] = 'Yes'
        if (RwCoating.externalinsulation == 0):
            datacoating['ExternalInsulation'] = 'No'
        else:
            datacoating['ExternalInsulation'] = 'Yes'
        if (RwCoating.insulationcontainschloride == 0):
            datacoating['Chloride'] = 'No'
        else:
            datacoating['Chloride'] = 'Yes'
        if (RwCoating.internallining == 0):
            datacoating['InternalLining'] = 'No'
        else:
            datacoating['InternalLining'] = 'Yes'
        datacoating1 = ['Coating, Cladding, Insulation, and Lining']
        datacoating2 = ['Coating']
        datacoating3 = ['Internal Coating: ', datacoating['InternalCoating']]
        datacoating4 = ['External Coating: ', datacoating['ExternalCoating']]
        datacoating5 = ['External Coating Installation Date: ', datacoating['ExternalDate']]
        datacoating6 = ['External Coating Quality: ', datacoating['ExternalCoatingQuality']]
        datacoating7 = ['Support Configuration Which Does not Allow Coating Maintenance: ', datacoating['Support']]
        datacoating8 = ['Cladding']
        datacoating9 = ['Internal Cladding: ', datacoating['InternalCladding']]
        datacoating10 = ['Cladding Corrosion Rate: ', str(datacoating['CladdingRate']) + ' mm/yr']
        datacoating11 = ['Cladding Thickness: ', str(datacoating['CladdingThickness']) + ' mm']
        datacoating12 = ['Insulation']
        datacoating13 = ['External Insulation: ', datacoating['ExternalInsulation']]
        datacoating14 = ['Insulation Contain Chloride: ', datacoating['Chloride']]
        datacoating15 = ['External Insulation Type: ', datacoating['InsulationType']]
        datacoating16 = ['Insulation Condition: ', datacoating['InsulationCondition']]
        datacoating17 = ['Lining']
        datacoating18 = ['Internal Lining: ', datacoating['InternalLining']]
        datacoating19 = ['Internal Liner Condition: ', datacoating['LinerCondition']]
        datacoating20 = ['Internal Liner Type: ', datacoating['LinerType']]
        datacoating = [datacoating1, datacoating2, datacoating3, datacoating4, datacoating6,
                       datacoating7,
                       datacoating8, datacoating9, datacoating10, datacoating11, datacoating12, datacoating13
            , datacoating14, datacoating15, datacoating16, datacoating17, datacoating18, datacoating19, datacoating20]
        th = pdf.font_size
        for row in datacoating:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # Here we add more padding by passing 2*th as height
        # Chart
        pof = {}
        RwFullFcof = models.RwFullFcof.objects.get(id=IDProposal)
        RwFullPof = models.RwFullPof.objects.get(id=IDProposal)
        pof['API1'] = RwFullPof.pofap1category
        pof['API2'] = RwFullPof.pofap2category
        pof['API3'] = RwFullPof.pofap3category
        cof = RwFullFcof.fcofcategory
        api1 = str(pof['API1']) + str(cof)
        api2 = str(pof['API2']) + str(cof)
        api3 = str(pof['API3']) + str(cof)

        def ChuanHoaX(xcof):
            if (xcof == 'A'):
                a = 0
                return a
            if (xcof == 'B'):
                a = 1
                return a
            if (xcof == 'C'):
                a = 2
                return a
            if (xcof == 'D'):
                a = 3
                return a
            if (xcof == 'E'):
                a = 4
                return a

        def ChuanHoaY(ypof):
            if (ypof == 5):
                a = 0
                return a
            if (ypof == 4):
                a = 1
                return a
            if (ypof == 3):
                a = 2
                return a
            if (ypof == 2):
                a = 3
                return a
            if (ypof == 1):
                a = 4
                return a

        pdf.add_page()
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(105, 105, 105)
        pdf.cell(col_width1, th, 'Risk Summary', border=1, fill=1)
        pdf.ln(th)
        pdf.cell(col_width1, 140, border=1, fill=0)
        pdf.ln(2)
        x_cur = pdf.get_x()
        y_cur = pdf.get_y()
        pdf.ln(138)
        data = np.array([
            [1, 1, 1, 3, 3],
            [2, 2, 1, 1, 3],
            [0, 0, 2, 1, 3],
            [0, 0, 2, 2, 1],
            [0, 0, 2, 2, 1]
        ])
        mycolor = 'green orange yellow red'.split()
        mycmap = matplotlib.colors.ListedColormap(mycolor, name='colors', N=4)
        plt.imshow(data, cmap=mycmap, interpolation='nearest')
        plt.xticks(np.arange(0, 5), ['A', 'B', 'C', 'D', 'E'])
        plt.yticks(np.arange(0, 5), ['5', '4', '3', '2', '1'])
        plt.xlabel('Consequense')
        plt.ylabel('Probability')
        # plt.grid(which = 'minor', color='black', linestyle='-', linewidth=1)
        ax = plt.gca()
        # Minor ticks
        ax.set_xticks(np.arange(-.5, 5, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 5, 1), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        plt.plot(ChuanHoaX(cof), ChuanHoaY(int(pof['API1'])), 'co', label='API1')
        plt.plot(ChuanHoaX(cof), ChuanHoaY(int(pof['API2'])), 'bs', label='API2')
        plt.plot(ChuanHoaX(cof), ChuanHoaY(int(pof['API3'])), 'm^', label='API3')
        # plt.legend(loc="upper right ")
        plt.savefig('cloud/process/ExportPDF/Chart.png')
        # plt.switch_backend('Agg')
        pdf.image('cloud/process/ExportPDF/Chart.png', x_cur + 2, y_cur, 170, 120)
        print('hello')
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width2 - 20, th, 'Description', border=1)
        pdf.cell((col_width2 + 20) / 4, th, '36 months', border=1)
        pdf.cell((col_width2 + 20) / 4, th, '72 months', border=1)
        pdf.cell((col_width2 + 20) / 4, th, '108 months', border=1)
        pdf.cell((col_width2 + 20) / 4, th, 'RLI (months)', border=1)
        pdf.ln(th)
        pdf.cell(col_width2 - 20, th, 'Risk', border=1)
        pdf.cell((col_width2 + 20) / 4, th, api1, border=1)
        pdf.cell((col_width2 + 20) / 4, th, api2, border=1)
        pdf.cell((col_width2 + 20) / 4, th, api3, border=1)
        pdf.cell((col_width2 + 20) / 4, th, '0', border=1)
        pdf.ln(10)
        # damage mechanisms table
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(105, 105, 105)
        pdf.cell(col_width1, th, 'Damage Mechanisms', border=1, fill=1)
        pdf.ln(th)
        damagetable = ['Damage Mechanisms', 'DF AP1', 'DF AP2', 'DF AP3']
        pdf.cell(col_width2 + 20, th, damagetable[0], border=1, fill=1)
        pdf.cell((col_width2 - 20) / 3, th, damagetable[1], border=1, fill=1)
        pdf.cell((col_width2 - 20) / 3, th, damagetable[2], border=1, fill=1)
        pdf.cell((col_width2 - 20) / 3, th, damagetable[3], border=1, fill=1)
        pdf.ln(th)
        datathining = thining(IDProposal)
        datalining = lining(IDProposal)
        dataanime = anime(IDProposal)
        datacaustic = caustic(IDProposal)
        datasulphide = sulphide(IDProposal)
        datahicsohich2s = hicsohich2s(IDProposal)
        dataalkaline = alkaline(IDProposal)
        dataPASCC = PASCC(IDProposal)
        dataCLSCC = CLSCC(IDProposal)
        dataHSCHF = HSCHF(IDProposal)
        dataHICSOPHIC = HICSOPHICHF(IDProposal)
        dataEXTERNAL = EXTERNAL_CORROSION(IDProposal)
        dataCUIF = CUIF(IDProposal)
        dataextCLSCC = extCLSCC(IDProposal)
        dataCUICLSCC = cuiCLSCC(IDProposal)
        dataHTHA = HTHA(IDProposal)
        dataBRITTLE = BRITTLE(IDProposal)
        dataTEMPLE = TEMP_EMBRITTLE(IDProposal)
        datad855 = d885(IDProposal)
        dataSIGMA = SIGMA(IDProposal)
        abc = [datathining, datalining, dataanime, datacaustic, datasulphide, datahicsohich2s, dataalkaline, dataPASCC,
               dataCLSCC, dataHSCHF, dataHICSOPHIC,
               dataEXTERNAL, dataCUIF, dataextCLSCC, dataCUICLSCC, dataHTHA, dataBRITTLE, dataTEMPLE, datad855, dataSIGMA]
        print('hello cac ban')
        pdf.set_text_color(0, 0, 0)
        for tung in abc:
            try:
                tung[1] = float(tung[1])
            except:
                tung[1] = 0
            try:
                tung[2] = float(tung[2])
            except:
                tung[2] = 0
            try:
                tung[3] = float(tung[3])
            except:
                tung[3] = 0
            if ((tung[1] == tung[2] == tung[3] == 0) == False):
                pdf.cell(col_width2 + 20, th, tung[0], border=1)
                pdf.cell((col_width2 - 20) / 3, th, str(round(tung[1], 4)), border=1)
                pdf.cell((col_width2 - 20) / 3, th, str(round(tung[2], 4)), border=1)
                pdf.cell((col_width2 - 20) / 3, th, str(round(tung[3], 4)), border=1)
                pdf.ln(th)
        pdf.ln(10)


        print('rat la ok ')
        pdf.output("cloud/process/ExportPDF/Baocao.pdf")
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass


def dataTank(IDProposal):
    try:
        pdf = PDF()
        pdf.alias_nb_pages()
        # Add a page
        pdf.add_page()

        pdf.set_title(title=title)

        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size=15)

        # create a cell
        # table information
        datainfo = {}
        RwAssessment = models.RwAssessment.objects.get(id=IDProposal)
        equipment_id = RwAssessment.equipmentid_id
        component_id = RwAssessment.componentid_id
        Equipmentmaster = models.EquipmentMaster.objects.get(equipmentid=equipment_id)
        datainfo['ProposalName'] = RwAssessment.proposalname
        datadate = str(RwAssessment.assessmentdate)
        datainfo['AssessmentDate'] = datadate[:10]
        if (RwAssessment.assessmentmethod == ''):
            datainfo['AssessmentMethod'] = 'None'
        else:
            datainfo['AssessmentMethod'] = RwAssessment.assessmentmethod
        datainfo['RiskPeriod'] = RwAssessment.riskanalysisperiod
        datainfo['EquipmentNumber'] = Equipmentmaster.equipmentnumber
        designcodeid = Equipmentmaster.designcodeid_id
        siteid = Equipmentmaster.siteid_id
        manuid = Equipmentmaster.manufacturerid_id
        equipmenttypeid = Equipmentmaster.equipmenttypeid_id
        datadate = str(Equipmentmaster.commissiondate)
        datainfo['CommissionDate'] = datadate[:10]
        datainfo['EquipmentName'] = Equipmentmaster.equipmentname
        datainfo['ProcessDescription'] = Equipmentmaster.processdescription
        Site = models.Sites.objects.get(siteid=siteid)
        datainfo['SiteName'] = Site.sitename
        DesignCode = models.DesignCode.objects.get(designcodeid=designcodeid)
        datainfo['DesignCodeName'] = DesignCode.designcode
        Manu = models.Manufacturer.objects.get(manufacturerid=manuid)
        datainfo['Manu'] = Manu.manufacturername
        equipmenttype = models.EquipmentType.objects.get(equipmenttypeid=equipmenttypeid)
        datainfo['EquipmentType'] = equipmenttype.equipmenttypename
        facilityid_id = Equipmentmaster.facilityid_id
        Facility = models.Facility.objects.get(facilityid=facilityid_id)
        datainfo['Facility'] = Facility.facilityname
        Componentmaster = models.ComponentMaster.objects.get(componentid=component_id)
        datainfo['ComponentNumber'] = Componentmaster.componentnumber
        componenttype_id = Componentmaster.componenttypeid_id
        componentapi_id = Componentmaster.apicomponenttypeid
        ComponentType = models.ComponentType.objects.get(componenttypeid=componenttype_id)
        ComponentAPI = models.ApiComponentType.objects.get(apicomponenttypeid=componentapi_id)
        datainfo['ComponentType'] = ComponentType.componenttypename
        datainfo['API'] = ComponentAPI.apicomponenttypename
        datainfo['ComponentName'] = Componentmaster.componentname
        if (Componentmaster.isequipmentlinked == 0):
            datainfo['Risk'] = "No"
        else:
            datainfo['Risk'] = "Yes"

        pdf.ln(5)
        epw = pdf.w - 2 * pdf.l_margin
        col_width1 = epw
        col_width2 = epw / 2
        col_width = epw / 4

        datainfo1 = ['Assessment General Information']
        datainfo2 = ['Assessment Name:', datainfo['ProposalName']]
        datainfo20 = ['Assessment Date:', datainfo['AssessmentDate']]
        datainfo3 = ['Assessment Method:', datainfo['AssessmentMethod']]
        datainfo4 = ['Risk Analysis Period (months):', datainfo['RiskPeriod']]
        datainfo5 = ['Equipment General Information']
        datainfo6 = ['Equipment Number: ', datainfo['EquipmentNumber']]
        datainfo7 = ['Equipment Type: ', datainfo['EquipmentType']]
        datainfo8 = ['Design Code: ', datainfo['EquipmentType']]
        datainfo9 = ['Site: ', datainfo['SiteName']]
        datainfo10 = ['Facility: ', datainfo['Facility']]
        datainfo11 = ['Manufacturer: ', datainfo['Manu']]
        datainfo12 = ['Commission Date: ', datainfo['CommissionDate']]
        datainfo13 = ['Equipment Name: ', 'Day la Equiment Name']
        datainfo14 = ['Process Description: ', 'Day la Process Description']
        datainfo15 = ['Component General Information']
        datainfo16 = ['Component Number: ', 'cai nay la Component Number']
        datainfo17 = ['Component Type: ', datainfo['ComponentType']]
        datainfo21 = ['API Component Type: ', datainfo['API']]
        datainfo18 = ['Component Name: ', 'cai nay la Component Name']
        datainfo19 = ['Risk Links to Equipment Risk: ', datainfo['Risk']]
        datainfo = [datainfo1, datainfo2, datainfo20, datainfo3, datainfo4, datainfo5, datainfo6, datainfo7, datainfo8,
                    datainfo9, datainfo10, datainfo11, datainfo12, datainfo13, datainfo14, datainfo15, datainfo16,
                    datainfo17, datainfo21, datainfo18, datainfo19]
        # print('dem= ', len(data3))
        th = pdf.font_size
        for row in datainfo:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table equipment
        dataequip = {}
        RwEquipment = models.RwEquipment.objects.get(id=IDProposal)
        if (RwEquipment.adminupsetmanagement == 0):
            dataequip['Administative'] = "No"
        else:
            dataequip['Administative'] = "Yes"
        if (RwEquipment.steamoutwaterflush == 0):
            dataequip['Steamed'] = "No"
        else:
            dataequip['Steamed'] = "Yes"
        if (RwEquipment.downtimeprotectionused == 0):
            dataequip['downtime'] = "No"
        else:
            dataequip['downtime'] = "Yes"
        if (RwEquipment.pwht == 0):
            dataequip['PWHT'] = "No"
        else:
            dataequip['PWHT'] = "Yes"
        if (RwEquipment.heattraced == 0):
            dataequip['HeatTrace'] = "No"
        else:
            dataequip['HeatTrace'] = "Yes"
        if (RwEquipment.cyclicoperation == 0):
            dataequip['Cyclic'] = "No"
        else:
            dataequip['Cyclic'] = "Yes"
        if (RwEquipment.lineronlinemonitoring == 0):
            dataequip['Liner'] = "No"
        else:
            dataequip['Liner'] = "Yes"
        dataequip['MinRequired'] = RwEquipment.minreqtemperaturepressurisation
        if (RwEquipment.materialexposedtoclext == 0):
            dataequip['Material'] = "No"
        else:
            dataequip['Material'] = "Yes"

        if (RwEquipment.pressurisationcontrolled == 0):
            dataequip['PressurisationControlled'] = "No"
        else:
            dataequip['PressurisationControlled'] = "Yes"
        if (RwEquipment.presencesulphideso2shutdown == 0):
            dataequip['PresenceShutdown'] = "No"
        else:
            dataequip['PresenceShutdown'] = "Yes"
        if (RwEquipment.interfacesoilwater == 0):
            dataequip['Soil'] = "No"
        else:
            dataequip['Soil'] = "Yes"
        if (RwEquipment.presencesulphideso2 == 0):
            dataequip['Presence'] = "No"
        else:
            dataequip['Presence'] = "Yes"
        if (RwEquipment.componentiswelded == 0):
            dataequip['ComponentWelded'] = "No"
        else:
            dataequip['ComponentWelded'] = "Yes"
        if (RwEquipment.tankismaintained == 0):
            dataequip['TankIsManintained'] = "No"
        else:
            dataequip['TankIsManintained'] = "Yes"
        if (RwEquipment.yearlowestexptemp == 0):
            dataequip['YearLowestExpected'] = "No"
        else:
            dataequip['YearLowestExpected'] = "Yes"
        if (RwEquipment.materialexposedtoclext == 0):
            dataequip['MaterialExposed'] = "No"
        else:
            dataequip['MaterialExposed'] = "Yes"

        dataequip['ExternalEnvor'] = RwEquipment.environmentsensitivity
        dataequip['ThemeHistory'] = RwEquipment.thermalhistory
        dataequip['SystemFactor'] = RwEquipment.managementfactor
        dataequip['EquipmentVolume'] = round(RwEquipment.volume, 4)
        dataequip['OnlineMonitoring'] = RwEquipment.onlinemonitoring
        dataequip['TypeOfSoil'] = RwEquipment.typeofsoil
        dataequip['Distance'] = round(RwEquipment.distancetogroundwater, 4)
        dataequip['Adjustment'] = RwEquipment.adjustmentsettle
        dataequip['Environmental'] = RwEquipment.environmentsensitivity

        pdf.ln(5)
        epw = pdf.w - 2 * pdf.l_margin
        col_width1 = epw
        col_width2 = epw / 2
        col_width = epw / 4

        dataequip1 = ['Equipment Properties']
        dataequip2 = ['Administrative Control for Upset Management: ', dataequip['Administative']]
        dataequip3 = ['Steamed Out Prior to Water Flushing: ', dataequip['Steamed']]
        dataequip4 = ['Downtime Protection Used: ', dataequip['downtime']]
        dataequip5 = ['PWHT: ', dataequip['PWHT']]
        dataequip6 = ['Heat Traced: ', dataequip['HeatTrace']]
        # dataequip7 = ['Liner Online Monitoring: ', dataequip['Liner']]
        dataequip7 = ['Cyclic Operation: ', dataequip['Cyclic']]
        dataequip8 = ['Min. Required Temperature Before Pressurisation Allowed by Admin: ', dataequip['MinRequired'], 4]
        # dataequip9 = ['Material is Exposed to Fluids, Mists or Solids Containing Chlorine Extemally: ',dataequip['Material']]
        dataequip9 = ['Pressurisation Controlled by Admin: ', dataequip['PressurisationControlled']]
        # dataequip11 = ['Presence of Sulphides, Moisture and Oxygen Duruing Shutdown: ', dataequip['PresenceShutdown']]
        dataequip10 = ['Interface at Soil or Water', dataequip['Soil']]
        dataequip11 = ['Liner Online Monitoring: ', dataequip['Liner']]
        dataequip12 = ['Type of Soil: ', dataequip['TypeOfSoil']]
        dataequip13 = ['Distance to Ground Water: ', dataequip['Distance']]
        dataequip14 = ['Component is Welded: ', dataequip['ComponentWelded']]
        dataequip15 = ['Tank is Maintained in Accordance with API 653:', dataequip['TankIsManintained']]
        dataequip16 = ['Equipment is Operating for Many Years at Lowest Expected Temperature: ',
                       dataequip['YearLowestExpected']]
        dataequip17 = ['Material is Exposed to Fluids, Mists or Soids Containing Chlorine Externally: ',
                       dataequip['MaterialExposed']]
        dataequip18 = ['Presence of Sulphides, Moisture and Oxygen Duruing Operation: ', dataequip['Presence']]
        dataequip19 = ['Presence of Sulphides, Moisture and Oxygen Duruing Shutdown: ', dataequip['PresenceShutdown']]
        dataequip20 = ['External Environment: ', dataequip['ExternalEnvor']]
        dataequip21 = ['Thermal History: ', dataequip['ThemeHistory']]
        dataequip22 = ['System Management Factor: ', dataequip['SystemFactor']]
        dataequip23 = ['Equipment Volume: ', dataequip['EquipmentVolume']]
        dataequip24 = ['Adjustment for Settlement: ', dataequip['Adjustment']]
        dataequip25 = ['Environmental Sensitivity: ', dataequip['Environmental']]
        dataequip26 = ['Online Monitoring: ', dataequip['OnlineMonitoring']]
        dataequip = [dataequip1, dataequip2, dataequip3, dataequip4, dataequip5, dataequip6, dataequip7, dataequip8,
                     dataequip9, dataequip10, dataequip11, dataequip12, dataequip13, dataequip14, dataequip15,
                     dataequip16,
                     dataequip17, dataequip18, dataequip19, dataequip20, dataequip21, dataequip22, dataequip23,
                     dataequip24, dataequip25, dataequip26]
        print('ok equipment tank')
        th = pdf.font_size
        for row in dataequip:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table Component
        datacomp = {}
        componenttank = models.RwInputCaTank.objects.get(id=IDProposal)
        component = models.RwComponent.objects.get(id=IDProposal)
        datacomp['TankDiameter'] = round(componenttank.tank_diametter, 4)
        datacomp['NormalThickness'] = round(component.nominalthickness, 4)
        datacomp['MeasuredThickness'] = round(component.currentthickness, 4)
        datacomp['RequiredThicknees'] = round(component.minreqthickness, 4)
        datacomp['CorrosionRate'] = round(component.currentcorrosionrate, 4)
        datacomp['FATT'] = round(component.deltafatt, 4)
        if (component.crackspresent == 0):
            datacomp['PresenceCracks'] = "No"
        else:
            datacomp['PresenceCracks'] = "Yes"
        datacomp['StructuralThickness'] = round(component.structuralthickness, 4)
        datacomp['Weld'] = round(component.weldjointefficiency, 4)
        datacomp['ComponentVolume'] = round(component.componentvolume, 4)
        datacomp['MaximumBrinnell'] = component.brinnelhardness
        datacomp['Allowable'] = round(component.allowablestress, 4)
        datacomp['Confidence'] = component.confidencecorrosionrate
        if (component.minstructuralthickness == 0):
            datacomp['MinStructurelThickness'] = "No"
        else:
            datacomp['MinStructurelThickness'] = "Yes"
        if (component.fabricatedsteel == 0):
            datacomp['Fabricatedsteel'] = "No"
        else:
            datacomp['Fabricatedsteel'] = "Yes"
        if (component.equipmentsatisfied == 0):
            datacomp['EquipmentStatisfied'] = "No"
        else:
            datacomp['EquipmentStatisfied'] = "Yes"
        if (component.nominaloperatingconditions == 0):
            datacomp['NominalOperatingConditions'] = "No"
        else:
            datacomp['NominalOperatingConditions'] = "Yes"
        if (component.cyclicservice == 0):
            datacomp['CyclicService'] = "No"
        else:
            datacomp['CyclicService'] = "Yes"
        if (component.cetgreaterorequal == 0):
            datacomp['CET'] = "No"
        else:
            datacomp['CET'] = "Yes"
        datacomp['Complexity'] = component.complexityprotrusion
        if (component.equipmentcircuitshock == 0):
            datacomp['EquipmentCircuitShock'] = "No"
        else:
            datacomp['EquipmentCircuitShock'] = "Yes"
        datacomp['BrittleFracture'] = round(component.brittlefracturethickness, 4)
        if (component.shellheight == 0):
            datacomp['ShellHeight'] = "No"
        else:
            datacomp['ShellHeight'] = "Yes"
        if (component.releasepreventionbarrier == 0):
            datacomp['Barrier'] = "No"
        else:
            datacomp['Barrier'] = "Yes"
        if (component.concretefoundation == 0):
            datacomp['ConcreteFoundation'] = "No"
        else:
            datacomp['ConcreteFoundation'] = "Yes"
        datacomp['SeverityVibration'] = component.severityofvibration

        pdf.ln(5)
        epw = pdf.w - 2 * pdf.l_margin
        col_width1 = epw
        col_width2 = epw / 2
        col_width = epw / 4

        datacomp1 = ['Component Properties']
        datacomp2 = ['Tank Diameter: ', str(datacomp['TankDiameter']) + ' mm']
        datacomp3 = ['Nominal Thickness: ', str(datacomp['NormalThickness']) + ' mm']
        datacomp4 = ['Minimum Measured Thickness: ', str(datacomp['MeasuredThickness']) + ' mm']
        datacomp5 = ['Min. Required Thickness: ', str(datacomp['RequiredThicknees']) + ' mm']
        datacomp6 = ['Current Corrosion Rate: ', str(datacomp['CorrosionRate']) + ' mm/yr']
        datacomp7 = ['Delta FATT', datacomp['FATT']]
        datacomp8 = ['Presence of Cracks: ', datacomp['PresenceCracks']]
        datacomp9 = ['Structural Thickness: ', str(datacomp['StructuralThickness']) + ' mm']
        datacomp10 = ['Weld Joint Efficiency: ', datacomp['Weld']]
        datacomp11 = ['Component Volume: ', str(datacomp['ComponentVolume']) + ' m^3']
        datacomp27 = ['Maximum brinnell Hardness of Weld: ', datacomp['MaximumBrinnell']]
        datacomp12 = ['Allowable Stress at Assessment Temperature: ', str(datacomp['Allowable']) + 'MPa']
        datacomp13 = ['Level of Confidence in Corrosion Rate: ', datacomp['Confidence']]
        datacomp14 = ['Minimum Structurel Thickness Governs: ', datacomp['MinStructurelThickness']]
        datacomp15 = [
            u'It is fabricated from P-1 and P-3 steels where the design temperature is less than or equal to 343\u00B0C(650\u00B0F): ',
            datacomp['Fabricatedsteel']]
        datacomp16 = [
            'The equipment satisfied all requirements of a reecognized code or standard at the time of fabrication: ',
            datacomp['EquipmentStatisfied']]
        datacomp17 = ['The equipment or circuit is no subject to shock chilling: ', datacomp['EquipmentCircuitShock']]
        datacomp19 = [
            'The nominal operating conditions have been essentially the same and consistent with the specified design conditions for a significant period of time, and more severe conditions are not expected in the future: ',
            datacomp['NominalOperatingConditions']]
        datacomp18 = ['Cyclic service, fatigue or vibration service is not a design requirement per design code: ',
                      datacomp['CyclicService']]
        datacomp20 = [
            'The CET at the MAWP is greater than or equal to -29\u00B0C (-20\u00B0F) if it is a pressure vessel or -104\u00B0C(-155\u00B0F) if it is a piping circuit: ',
            datacomp['CET']]
        datacomp21 = ['Complexity of Protrusions: ', datacomp['Complexity']]
        datacomp22 = ['Brittle Fracture Governing Thickness: ', datacomp['BrittleFracture']]
        datacomp23 = ['Shell Course Height: ', str(datacomp['ShellHeight']) + ' m']
        datacomp24 = ['Release Prevention Barrier: ', datacomp['Barrier']]
        datacomp25 = ['Concrete or Asphalt Foundation: ', datacomp['ConcreteFoundation']]
        datacomp26 = ['Severity of Vibration:', datacomp['SeverityVibration']]
        datacomp = [datacomp1, datacomp2, datacomp3, datacomp4, datacomp5, datacomp6, datacomp7, datacomp8, datacomp9,
                    datacomp10, datacomp11, datacomp27, datacomp12, datacomp13, datacomp14, datacomp15, datacomp16,
                    datacomp17, datacomp18, datacomp19, datacomp20, datacomp21, datacomp22, datacomp23, datacomp24,
                    datacomp25, datacomp26]

        th = pdf.font_size
        for row in datacomp:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # Line break equivalent to 4 lines
        # table Operating Conditions
        dataopera = {}
        Stream = models.RwStream.objects.get(id=IDProposal)
        Extcor = models.RwExtcorTemperature.objects.get(id=IDProposal)
        dataopera['maxOT'] = round(Stream.maxoperatingtemperature, 4)
        dataopera['minOT'] = round(Stream.minoperatingtemperature, 4)
        dataopera['maxOP'] = round(Stream.maxoperatingpressure, 4)
        dataopera['minOP'] = round(Stream.minoperatingpressure, 4)
        dataopera['criticalTemp'] = round(Stream.criticalexposuretemperature, 4)
        dataopera['flowrate'] = round(Stream.flowrate, 4)
        dataopera['_12_8'] = round(Extcor.minus12tominus8, 4)
        dataopera['_86'] = round(Extcor.minus8toplus6, 4)
        dataopera['632'] = round(Extcor.plus6toplus32, 4)
        dataopera['3271'] = round(Extcor.plus32toplus71, 4)
        dataopera['71107'] = round(Extcor.plus71toplus107, 4)
        dataopera['107121'] = round(Extcor.plus107toplus121, 4)
        dataopera['121135'] = round(Extcor.plus121toplus135, 4)
        dataopera['135162'] = round(Extcor.plus135toplus162, 4)
        dataopera['162176'] = round(Extcor.plus162toplus176, 4)
        dataopera['176plus'] = round(Extcor.morethanplus176, 4)
        dataopera['OpHydroPressure'] = round(Stream.hydrogen, 4)

        dataopera1 = ['Operating Conditions Properties']
        dataopera2 = ['Max. Operating Temperature: ', str(dataopera['maxOT']) + u' \u00B0C']
        dataopera3 = ['Min. Operating Temperature: ', str(dataopera['minOT']) + u' \u00B0C']
        dataopera4 = ['Max. Operating Pressure: ', str(dataopera['maxOP']) + ' MPa']
        dataopera5 = ['Min. Operating Pressure: ', str(dataopera['minOP']) + ' MPa']
        dataopera6 = ['Critical Exposure Temperature: ', str(dataopera['criticalTemp']) + u' \u00B0C']
        dataopera7 = ['Flow Rate: ', str(dataopera['flowrate']) + ' m^3/hr']
        dataopera8 = [u'% Operating at -12\u00B0C to -8\u00B0C: ', str(dataopera['_12_8']) + ' %']
        dataopera9 = [u'% Operating at -8\u00B0C to 6\u00B0C: ', str(dataopera['_86']) + ' %']
        dataopera10 = [u'% Operating at 6\u00B0C to 32\u00B0C: ', str(dataopera['632']) + ' %']
        dataopera11 = [u'% Operating at 32\u00B0C to 71\u00B0C: ', str(dataopera['3271']) + ' %']
        dataopera12 = [u'% Operating at 71\u00B0C to 107\u00B0C: ', str(dataopera['71107']) + ' %']
        dataopera13 = [u'% Operating at 107\u00B0C to 121\u00B0C: ', str(dataopera['107121']) + ' %']
        dataopera14 = [u'% Operating at 121\u00B0C to 135\u00B0C: ', str(dataopera['121135']) + ' %']
        dataopera15 = [u'% Operating at 135\u00B0C to 162\u00B0C: ', str(dataopera['135162']) + ' %']
        dataopera16 = [u'% Operating at 162\u00B0C to 176\u00B0C: ', str(dataopera['162176']) + ' %']
        dataopera17 = [u'% Operating at 176\u00B0C or Above: ', str(dataopera['176plus']) + ' %']
        dataopera18 = ['Operating Hydrogen Partial Pressure: ', str(dataopera['OpHydroPressure']) + ' %']
        dataopera = [dataopera1, dataopera2, dataopera3, dataopera4, dataopera5, dataopera6, dataopera7, dataopera8,
                     dataopera9, dataopera10, dataopera11, dataopera12, dataopera12, dataopera13, dataopera14,
                     dataopera15,
                     dataopera16, dataopera17, dataopera18]
        th = pdf.font_size
        for row in dataopera:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table Stream
        datastream = {}
        RwStream = models.RwStream.objects.get(id=IDProposal)
        inputCATank = models.RwInputCaTank.objects.get(id=IDProposal)
        datastream['FluidTank'] = inputCATank.tank_fluid
        datastream['FluidHeight'] = round(inputCATank.fluid_height, 4)
        datastream['PercentageDike'] = round(RwStream.fluidleavedikepercent, 4)
        datastream['PercentageRemainSite'] = round(RwStream.fluidleavedikeremainonsitepercent, 4)
        datastream['PercentageOffsite'] = round(RwStream.fluidgooffsitepercent, 4)
        datastream['maxOT'] = round(RwStream.maxoperatingtemperature, 4)
        datastream['minOT'] = round(RwStream.minoperatingtemperature, 4)
        datastream['maxOP'] = round(RwStream.maxoperatingpressure, 4)
        datastream['minOP'] = round(RwStream.minoperatingpressure, 4)
        datastream['OHPressure'] = "day la Operating Hydrogen Partial Pressure"
        datastream['flowrate'] = round(RwStream.flowrate, 4)
        datastream['NAOH'] = round(RwStream.naohconcentration, 4)
        datastream['ChlorideIon'] = round(RwStream.chloride, 4)
        datastream['Co3'] = round(RwStream.co3concentration, 4)
        datastream['H2S'] = round(RwStream.h2sinwater, 4)
        datastream['PH'] = round(RwStream.waterph, 4)
        datastream['PercentToxic'] = round(RwStream.releasefluidpercenttoxic, 4)
        if (RwStream.toxicconstituent == 0):
            datastream['ToxicConstituents'] = "No"
        else:
            datastream['ToxicConstituents'] = "Yes"
        if (RwStream.exposedtogasamine == 0):
            datastream['ExposedtoAcidGas'] = "No"
        else:
            datastream['ExposedtoAcidGas'] = "Yes"
        datastream['ExposedtoAmine'] = RwStream.exposuretoamine
        datastream['AmineSolution'] = RwStream.aminesolution
        if (RwStream.aqueousoperation == 0):
            datastream['AqueousOperating'] = "No"
        else:
            datastream['AqueousOperating'] = "Yes"
        if (RwStream.aqueousshutdown == 0):
            datastream['AqueousShutdown'] = "No"
        else:
            datastream['AqueousShutdown'] = "Yes"
        if (RwStream.h2s == 0):
            datastream['EnviH2S'] = "No"
        else:
            datastream['EnviH2S'] = "Yes"
        if (RwStream.hydrofluoric == 0):
            datastream['PresenceHydrofluoric'] = "No"
        else:
            datastream['PresenceHydrofluoric'] = "Yes"
        if (RwStream.cyanide == 0):
            datastream['Cyanides'] = "No"
        else:
            datastream['Cyanides'] = "Yes"
        if (RwStream.hydrogen == 0):
            datastream['Hydrogen'] = "No"
        else:
            datastream['Hydrogen'] = "Yes"
        if (RwStream.caustic == 0):
            datastream['Caustic'] = "No"
        else:
            datastream['Caustic'] = "Yes"
        if (RwStream.exposedtosulphur == 0):
            datastream['SulphurBeaning'] = "No"
        else:
            datastream['SulphurBeaning'] = "Yes"
        if (RwStream.materialexposedtoclint == 0):
            datastream['material'] = "No"
        else:
            datastream['material'] = "Yes"
        if (RwStream.exposedtogasamine == 0):
            datastream['AcidGas'] = "No"
        else:
            datastream['AcidGas'] = "Yes"
        datastream1 = ['Stream/Process Flow']
        datastream2 = ['Fluid']
        datastream3 = ['Fluid in Tank: ', datastream['FluidTank']]
        datastream4 = ['Fluid Height: ', str(datastream['FluidHeight']) + ' m']
        datastream5 = ['Percentage of Fluid Leaving the Dike: ', datastream['PercentageDike']]
        datastream6 = ['Percentage of Fluid Leaving the Dike but Remains on Site: ', datastream['PercentageRemainSite']]
        datastream7 = ['Percentage of Fluid Going Offsite: ', datastream['PercentageOffsite']]
        datastream8 = ['Maxium Operating Temperature: ', str(datastream['maxOT']) + u' \u00B0C']
        datastream9 = ['Minium Operating Temperature: ', str(datastream['minOT']) + u' \u00B0C']
        datastream10 = ['Maxium Operating Pressure:', str(datastream['maxOP']) + ' MPa']
        datastream11 = ['Minium Operating Pressure: ', str(datastream['minOP']) + ' MPa']
        datastream12 = ['Operating Hydrogen Partial Pressure: ', str(datastream['OHPressure']) + ' MPa']
        datastream13 = ['Flow Rate:', str(datastream['flowrate']) + ' m^3/yr']
        # datastream5 = ['Phase of Fluid at Storage: ', datastream['FluidPhase']]
        # datastream6 = ['Toxic Fluid percentage(%): ', datastream['ToxicPercent']]
        # datastream7 = ['Liquid Level(%): ', datastream['LiquidLevel']]
        # datastream8 = ['Environment Condition']
        datastream14 = ['NaOH Concentration(%): ', datastream['NAOH']]
        datastream15 = ['Release Fluid Percent Toxic(%): ', datastream['PercentToxic']]
        datastream16 = ['Chloride Ion (ppm): ', datastream['ChlorideIon']]
        datastream17 = ['CO3 Concentration in Water (ppm): ', datastream['Co3']]
        datastream18 = ['H2S Content in Water (ppm): ', datastream['H2S']]
        datastream19 = ['pH of Water: ', datastream['PH']]
        datastream20 = ['Toxic Constituents: ', datastream['ToxicConstituents']]
        datastream21 = ['Exposed To Acid Gas Treating Amine: ', datastream['ExposedtoAcidGas']]
        datastream22 = ['Exposed To Amine: ', datastream['ExposedtoAmine']]
        datastream23 = ['Amine Solution Composition: ', datastream['AmineSolution']]
        datastream24 = ['Aqueous Phase During Operation: ', datastream['AqueousOperating']]
        datastream25 = ['Aqueous Phase During Shutdown: ', datastream['AqueousShutdown']]
        datastream26 = ['Environment Consatins H2S: ', datastream['EnviH2S']]
        datastream27 = ['Presence of Hydrofluoric Acid: ', datastream['PresenceHydrofluoric']]
        datastream28 = ['Presence of Cyanides: ', datastream['Cyanides']]
        datastream29 = ['Process Contains Hydrogen: ', datastream['Hydrogen']]
        datastream30 = ['Environment Contains Caustic in Any Concentration: ', datastream['Caustic']]
        datastream31 = ['Exposed to Sulphur-Beaning Compounds: ', datastream['SulphurBeaning']]
        datastream32 = ['Material is Exposed to Fluids, Mists, or Solids: ', datastream['material']]
        # datastream27 = ['Exposed to Acid Gas Treating Amine: ', datastream['ExposedtoAcidGas']]
        datastream = [datastream1, datastream2, datastream3, datastream4, datastream5, datastream6, datastream7,
                      datastream8, datastream9, datastream10, datastream11, datastream12, datastream13
            , datastream14, datastream15, datastream16, datastream17, datastream18, datastream19, datastream20,
                      datastream21, datastream22, datastream23, datastream24, datastream25, datastream26, datastream27,
                      datastream28,
                      datastream29, datastream30, datastream31, datastream32]
        th = pdf.font_size
        for row in datastream:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table material
        datamaterial = {}
        RwMaterial = models.RwMaterial.objects.get(id=IDProposal)
        datamaterial['Material'] = RwMaterial.materialname
        datamaterial['DesignPressure'] = round(RwMaterial.designpressure, 4)
        datamaterial['DesignTemperature'] = round(RwMaterial.designtemperature, 4)
        datamaterial['TensileStrength'] = round(RwMaterial.tensilestrength, 4)
        datamaterial['YieldStrength'] = round(RwMaterial.yieldstrength, 4)
        datamaterial['ReferenceTem'] = round(RwMaterial.referencetemperature, 4)
        datamaterial['SigmaPhase'] = round(RwMaterial.sigmaphase, 4)
        datamaterial['CorrosionAllow'] = round(RwMaterial.corrosionallowance, 4)
        datamaterial['SulfuContent'] = RwMaterial.sulfurcontent
        datamaterial['MinDesignTem'] = round(RwMaterial.mindesigntemperature, 4)
        datamaterial['HeatTreatment'] = RwMaterial.heattreatment
        datamaterial['MaterialCostFactor'] = round(RwMaterial.costfactor, 4)
        datamaterial['MaxDesignTem'] = round(RwMaterial.designtemperature, 4)
        datamaterial['PTAMataterialGrade'] = RwMaterial.ptamaterialcode
        datamaterial['SteelProductForm'] = RwMaterial.steelproductform
        datamaterial['HTHAMaterialGrade'] = RwMaterial.hthamaterialcode
        if (RwMaterial.austenitic == 0):
            datamaterial['AusteniticSteel'] = 'No'
        else:
            datamaterial['AusteniticSteel'] = 'Yes'
        if (RwMaterial.carbonlowalloy == 0):
            datamaterial['CarbonLowAlloy'] = 'No'
        else:
            datamaterial['CarbonLowAlloy'] = 'Yes'
        if (RwMaterial.nickelbased == 0):
            datamaterial['NickelBased'] = 'No'
        else:
            datamaterial['NickelBased'] = 'Yes'
        if (RwMaterial.temper == 0):
            datamaterial['SuscestibleTemper'] = 'No'
        else:
            datamaterial['SuscestibleTemper'] = 'Yes'
        if (RwMaterial.chromemoreequal12 == 0):
            datamaterial['Chromium'] = 'No'
        else:
            datamaterial['Chromium'] = 'Yes'
        if (RwMaterial.ispta == 0):
            datamaterial['PTA'] = 'No'
        else:
            datamaterial['PTA'] = 'Yes'
        if (RwMaterial.ishtha == 0):
            datamaterial['HTHA'] = 'No'
        else:
            datamaterial['HTHA'] = 'Yes'
        datamaterial1 = ['Material Properties']
        datamaterial2 = ['Material:', datamaterial['Material']]
        datamaterial3 = ['Design Pressure: ', str(datamaterial['DesignPressure']) + ' MPa']
        datamaterial4 = ['Design Temperature: ', str(datamaterial['DesignTemperature']) + u' \u00B0C']
        datamaterial5 = ['Tensile Strength: ', str(datamaterial['TensileStrength']) + ' MPa']
        datamaterial6 = ['Yield Strength: ', str(datamaterial['YieldStrength']) + ' MPa']
        datamaterial7 = ['Reference Temperature', str(datamaterial['ReferenceTem']) + u' \u00B0C']
        datamaterial8 = ['Sigma Phase(%): ', datamaterial['SigmaPhase']]
        datamaterial9 = ['Corrosion Allowance: ', str(datamaterial['CorrosionAllow']) + ' mm']
        datamaterial10 = ['Austenitic Steel: ', datamaterial['AusteniticSteel']]
        datamaterial11 = ['Carbon or Low Alloy Steel: ', datamaterial['CarbonLowAlloy']]
        datamaterial12 = ['Nickel-based Alloy: ', datamaterial['NickelBased']]
        datamaterial13 = ['Susceptible to Temper: ', datamaterial['SuscestibleTemper']]
        datamaterial14 = ['Sulfur Content: ', datamaterial['SulfuContent']]
        datamaterial15 = ['Chromium >= 12%: ', datamaterial['Chromium']]
        datamaterial16 = ['Min. Design Temperature: ', str(datamaterial['MinDesignTem']) + u' \u00B0C']
        datamaterial17 = ['Heat Treatment: ', datamaterial['HeatTreatment']]
        datamaterial18 = ['Material Cost Factor: ', datamaterial['MaterialCostFactor']]
        datamaterial19 = ['Material is Susceptible to PTA: ', datamaterial['PTA']]
        datamaterial20 = ['Max. Design Temperature: ', str(datamaterial['MaxDesignTem']) + u' \u00B0C']
        datamaterial21 = ['PTA Material Grade: ', datamaterial['PTAMataterialGrade']]
        datamaterial22 = ['Material is Susceptible to HTHA: ', datamaterial['HTHA']]
        datamaterial23 = ['Steel Product Form: ', datamaterial['SteelProductForm']]
        datamaterial24 = ['HTHA Material Grade: ', datamaterial['HTHAMaterialGrade']]
        datamaterial = [datamaterial1, datamaterial2, datamaterial3, datamaterial4, datamaterial5, datamaterial6,
                        datamaterial7,
                        datamaterial8, datamaterial9, datamaterial10, datamaterial11, datamaterial12, datamaterial13
            , datamaterial14, datamaterial15, datamaterial16, datamaterial17, datamaterial18, datamaterial19,
                        datamaterial20,
                        datamaterial21, datamaterial22, datamaterial23, datamaterial24]
        th = pdf.font_size
        for row in datamaterial:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # table coating
        datacoating = {}
        RwCoating = models.RwCoating.objects.get(id=IDProposal)
        exdate = str(RwCoating.externalcoatingdate)
        datacoating['ExternalDate'] = exdate[:10]
        datacoating['ExternalCoatingQuality'] = RwCoating.externalcoatingquality
        datacoating['CladdingRate'] = round(RwCoating.claddingcorrosionrate, 4)
        datacoating['CladdingThickness'] = RwCoating.claddingthickness
        datacoating['InsulationType'] = RwCoating.externalinsulationtype
        datacoating['InsulationCondition'] = RwCoating.insulationcondition
        datacoating['LinerCondition'] = RwCoating.internallinercondition
        datacoating['LinerType'] = RwCoating.internallinertype
        if (RwCoating.internalcoating == 0):
            datacoating['InternalCoating'] = 'No'
        else:
            datacoating['InternalCoating'] = 'Yes'
        if (RwCoating.externalcoating == 0):
            datacoating['ExternalCoating'] = 'No'
        else:
            datacoating['ExternalCoating'] = 'Yes'
        if (RwCoating.supportconfignotallowcoatingmaint == 0):
            datacoating['Support'] = 'No'
        else:
            datacoating['Support'] = 'Yes'
        if (RwCoating.internalcladding == 0):
            datacoating['InternalCladding'] = 'No'
        else:
            datacoating['InternalCladding'] = 'Yes'
        if (RwCoating.externalinsulation == 0):
            datacoating['ExternalInsulation'] = 'No'
        else:
            datacoating['ExternalInsulation'] = 'Yes'
        if (RwCoating.insulationcontainschloride == 0):
            datacoating['Chloride'] = 'No'
        else:
            datacoating['Chloride'] = 'Yes'
        if (RwCoating.internallining == 0):
            datacoating['InternalLining'] = 'No'
        else:
            datacoating['InternalLining'] = 'Yes'
        datacoating1 = ['Coating, Cladding, Insulation, and Lining']
        datacoating2 = ['Coating']
        datacoating3 = ['Internal Coating: ', datacoating['InternalCoating']]
        datacoating4 = ['External Coating: ', datacoating['ExternalCoating']]
        datacoating5 = ['External Coating Installation Date: ', datacoating['ExternalDate']]
        datacoating6 = ['External Coating Quality: ', datacoating['ExternalCoatingQuality']]
        datacoating7 = ['Support Configuration Which Does not Allow Coating Maintenance: ', datacoating['Support']]
        datacoating8 = ['Cladding']
        datacoating9 = ['Internal Cladding: ', datacoating['InternalCladding']]
        datacoating10 = ['Cladding Corrosion Rate: ', str(datacoating['CladdingRate']) + ' mm/yr']
        datacoating11 = ['Cladding Thickness: ', str(datacoating['CladdingThickness']) + ' mm']
        datacoating12 = ['Insulation']
        datacoating13 = ['External Insulation: ', datacoating['ExternalInsulation']]
        datacoating14 = ['Insulation Contain Chloride: ', datacoating['Chloride']]
        datacoating15 = ['External Insulation Type: ', datacoating['InsulationType']]
        datacoating16 = ['Insulation Condition: ', datacoating['InsulationCondition']]
        datacoating17 = ['Lining']
        datacoating18 = ['Internal Lining: ', datacoating['InternalLining']]
        datacoating19 = ['Internal Liner Condition: ', datacoating['LinerCondition']]
        datacoating20 = ['Internal Liner Type: ', datacoating['LinerType']]
        datacoating = [datacoating1, datacoating2, datacoating3, datacoating4, datacoating5, datacoating6,
                       datacoating7,
                       datacoating8, datacoating9, datacoating10, datacoating11, datacoating12, datacoating13
            , datacoating14, datacoating15, datacoating16, datacoating17, datacoating18, datacoating19, datacoating20, ]
        th = pdf.font_size
        for row in datacoating:
            pdf.set_font('Times', '', 14.0)
            if len(row) == 1:
                pdf.set_font('Times', 'B', 16.0)
                pdf.set_text_color(255, 255, 255)
                pdf.set_fill_color(105, 105, 105)
                pdf.cell(col_width1, th, str(row[0]), border=1, fill=1)
                pdf.ln(th)
            elif len(row) == 2:
                pdf.set_text_color(0, 0, 0)
                x_axis = pdf.get_x()
                if (len(str(row[0])) > 43):
                    th0 = math.ceil(len(str(row[0])) / 43)
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th0, x_axis, str(row[1]))
                    pdf.ln(th * th0)
                else:
                    th1 = math.ceil(len(str(row[1])) / 43)
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[0]))
                    x_axis = pdf.get_x()
                    pdf.vcell(col_width2, th * th1, x_axis, str(row[1]))
                    pdf.ln(th * th1)
        pdf.ln(4)
        # Chart
        pof = {}
        RwFullFcof = models.RwFullFcof.objects.get(id=IDProposal)
        RwFullPof = models.RwFullPof.objects.get(id=IDProposal)
        pof['API1'] = RwFullPof.pofap1category
        pof['API2'] = RwFullPof.pofap2category
        pof['API3'] = RwFullPof.pofap3category
        cof = RwFullFcof.fcofcategory
        api1 = str(pof['API1']) + str(cof)
        api2 = str(pof['API2']) + str(cof)
        api3 = str(pof['API3']) + str(cof)

        def ChuanHoaX(xcof):
            if (xcof == 'A'):
                a = 0
                return a
            if (xcof == 'B'):
                a = 1
                return a
            if (xcof == 'C'):
                a = 2
                return a
            if (xcof == 'D'):
                a = 3
                return a
            if (xcof == 'E'):
                a = 4
                return a

        def ChuanHoaY(ypof):
            if (ypof == 5):
                a = 0
                return a
            if (ypof == 4):
                a = 1
                return a
            if (ypof == 3):
                a = 2
                return a
            if (ypof == 2):
                a = 3
                return a
            if (ypof == 1):
                a = 4
                return a

        pdf.add_page()
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(105, 105, 105)
        pdf.cell(col_width1, th, 'Risk Summary', border=1, fill=1)
        pdf.ln(th)
        pdf.cell(col_width1, 140, border=1, fill=0)
        pdf.ln(2)
        x_cur = pdf.get_x()
        y_cur = pdf.get_y()
        pdf.ln(138)
        data = np.array([
            [1, 1, 1, 3, 3],
            [2, 2, 1, 1, 3],
            [0, 0, 2, 1, 3],
            [0, 0, 2, 2, 1],
            [0, 0, 2, 2, 1]
        ])
        mycolor = 'green orange yellow red'.split()
        mycmap = matplotlib.colors.ListedColormap(mycolor, name='colors', N=4)
        plt.imshow(data, cmap=mycmap, interpolation='nearest')
        plt.xticks(np.arange(0, 5), ['A', 'B', 'C', 'D', 'E'])
        plt.yticks(np.arange(0, 5), ['5', '4', '3', '2', '1'])
        plt.xlabel('Consequense')
        plt.ylabel('Probability')
        # plt.grid(which = 'minor', color='black', linestyle='-', linewidth=1)
        ax = plt.gca()
        # Minor ticks
        ax.set_xticks(np.arange(-.5, 5, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 5, 1), minor=True)

        # Gridlines based on minor ticks
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        plt.plot(ChuanHoaX(cof), ChuanHoaY(int(pof['API1'])), 'co', label='API1')
        plt.plot(ChuanHoaX(cof), ChuanHoaY(int(pof['API2'])), 'bs', label='API2')
        plt.plot(ChuanHoaX(cof), ChuanHoaY(int(pof['API3'])), 'm^', label='API3')
        # plt.legend(loc="upper right ")
        plt.savefig('cloud/process/ExportPDF/Chart.png')
        pdf.image('cloud/process/ExportPDF/Chart.png', x_cur + 2, y_cur, 170, 120)
        print('hello')
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width2 - 20, th, 'Description', border=1)
        pdf.cell((col_width2 + 20) / 4, th, '36 months', border=1)
        pdf.cell((col_width2 + 20) / 4, th, '72 months', border=1)
        pdf.cell((col_width2 + 20) / 4, th, '108 months', border=1)
        pdf.cell((col_width2 + 20) / 4, th, 'RLI (months)', border=1)
        pdf.ln(th)
        pdf.cell(col_width2 - 20, th, 'Risk', border=1)
        pdf.cell((col_width2 + 20) / 4, th, api1, border=1)
        pdf.cell((col_width2 + 20) / 4, th, api2, border=1)
        pdf.cell((col_width2 + 20) / 4, th, api3, border=1)
        pdf.cell((col_width2 + 20) / 4, th, '0', border=1)
        pdf.ln(10)
        print("toi day roi ma van khong doc ghi duoc la the nao")
        # damage mechanisms table
        pdf.set_text_color(255, 255, 255)
        pdf.set_fill_color(105, 105, 105)
        pdf.cell(col_width1, th, 'Damage Mechanisms', border=1, fill=1)
        pdf.ln(th)
        damagetable = ['Damage Mechnisms', 'DF AP1', 'DF AP2', 'DF AP3']
        pdf.cell(col_width2 + 20, th, damagetable[0], border=1, fill=1)
        pdf.cell((col_width2 - 20) / 3, th, damagetable[1], border=1, fill=1)
        pdf.cell((col_width2 - 20) / 3, th, damagetable[2], border=1, fill=1)
        pdf.cell((col_width2 - 20) / 3, th, damagetable[3], border=1, fill=1)
        pdf.ln(th)
        datathining = thining(IDProposal)
        datalining = lining(IDProposal)
        dataanime = anime(IDProposal)
        datacaustic = caustic(IDProposal)
        datasulphide = sulphide(IDProposal)
        datahicsohich2s = hicsohich2s(IDProposal)
        dataalkaline = alkaline(IDProposal)
        dataPASCC = PASCC(IDProposal)
        dataCLSCC = CLSCC(IDProposal)
        dataHSCHF = HSCHF(IDProposal)
        dataHICSOPHIC = HICSOPHICHF(IDProposal)
        dataEXTERNAL = EXTERNAL_CORROSION(IDProposal)
        dataCUIF = CUIF(IDProposal)
        # dataextCLSCC = extCLSCC(IDProposal) #cho nay loi vcl nhung eo biet sua loi the nao :((
        dataCUICLSCC = cuiCLSCC(IDProposal)
        dataHTHA = HTHA(IDProposal)
        dataBRITTLE = BRITTLE(IDProposal)
        dataTEMPLE = TEMP_EMBRITTLE(IDProposal)
        datad855 = d885(IDProposal)
        dataSIGMA = SIGMA(IDProposal)
        abc = [datathining, datalining, dataanime, datacaustic, datasulphide, datahicsohich2s, dataalkaline, dataPASCC,
               dataHSCHF,
               dataHICSOPHIC, dataEXTERNAL, dataCUIF, dataCUICLSCC, dataHTHA, dataBRITTLE, dataTEMPLE,
               datad855, dataSIGMA]
        print('hello cac ban')
        pdf.set_text_color(0, 0, 0)
        for tung in abc:
            try:
                tung[1] = float(tung[1])
            except:
                tung[1] = 0
            try:
                tung[2] = float(tung[2])
            except:
                tung[2] = 0
            try:
                tung[3] = float(tung[3])
            except:
                tung[3] = 0
            if ((tung[1] == tung[2] == tung[3] == 0) == False):
                pdf.cell(col_width2 + 20, th, tung[0], border=1)
                pdf.cell((col_width2 - 20) / 3, th, str(round(tung[1], 4)), border=1)
                pdf.cell((col_width2 - 20) / 3, th, str(round(tung[2], 4)), border=1)
                pdf.cell((col_width2 - 20) / 3, th, str(round(tung[3], 4)), border=1)
                pdf.ln(th)
        pdf.ln(10)
        pdf.output("cloud/process/ExportPDF/Baocao.pdf")
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass





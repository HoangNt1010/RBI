import os,sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()
from cloud.process.RBI import pofConvert
from cloud import models

def save_rw_full_pof(proposalID,thinningtype):
    df = models.RwFullPof.objects.get(id=proposalID)
    df.thinningtype = thinningtype
    df.save()
    # ---------------
    rwassessment = models.RwAssessment.objects.get(id=proposalID)
    comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
    gffTotal = models.ApiComponentType.objects.get(apicomponenttypeid=comp.apicomponenttypeid).gfftotal
    #-----------------
    datafaci = models.Facility.objects.get(
        facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
    if df.thinningtype == 'Local':
        TOTAL_DF_API1 = df.thinninglocalap1 +df.sccap1 + df.brittleap1 + df.htha_ap1 + df.fatigueap1
        TOTAL_DF_API2 = df.thinninglocalap2 +df.sccap2 + df.brittleap2 + df.htha_ap2 + df.fatigueap2
        TOTAL_DF_API3 = df.thinninglocalap3 +df.sccap3 + df.brittleap3 + df.htha_ap3 + df.fatigueap3
        df.totaldfap1 = TOTAL_DF_API1
        df.totaldfap2 = TOTAL_DF_API2
        df.totaldfap3 = TOTAL_DF_API3
        df.pofap1 = pofConvert.convert(TOTAL_DF_API1 * datafaci.managementfactor * gffTotal)
        df.pofap2 = pofConvert.convert(TOTAL_DF_API2 * datafaci.managementfactor * gffTotal)
        df.pofap3 = pofConvert.convert(TOTAL_DF_API3 * datafaci.managementfactor * gffTotal)
        df.pofap1category = PoFCategory(TOTAL_DF_API1)
        df.pofap2category = PoFCategory(TOTAL_DF_API2)
        df.pofap3category = PoFCategory(TOTAL_DF_API3)
        df.save()
    else:
        TOTAL_DF_GENERAL_1 = df.thinninggeneralap1 + df.sccap1 + df.brittleap1 + df.htha_ap1 + df.fatigueap1
        TOTAL_DF_GENERAL_2 = df.thinninggeneralap2 + df.sccap2 + df.brittleap2 + df.htha_ap2 + df.fatigueap2
        TOTAL_DF_GENERAL_3 = df.thinninggeneralap1 + df.sccap3 + df.brittleap3 + df.htha_ap3 + df.fatigueap3
        df.totaldfap1 = TOTAL_DF_GENERAL_1
        df.totaldfap2 = TOTAL_DF_GENERAL_2
        df.totaldfap3 = TOTAL_DF_GENERAL_3
        df.pofap1 = pofConvert.convert(TOTAL_DF_GENERAL_1 * datafaci.managementfactor * gffTotal)
        df.pofap2 = pofConvert.convert(TOTAL_DF_GENERAL_2 * datafaci.managementfactor * gffTotal)
        df.pofap3 = pofConvert.convert(TOTAL_DF_GENERAL_3 * datafaci.managementfactor * gffTotal)
        df.pofap1category = PoFCategory(TOTAL_DF_GENERAL_1)
        df.pofap2category = PoFCategory(TOTAL_DF_GENERAL_2)
        df.pofap3category = PoFCategory(TOTAL_DF_GENERAL_3)
        df.save()
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
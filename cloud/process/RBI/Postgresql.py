import os,sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from cloud import models
import numpy as np

class POSTGRESQL:
    def GET_TBL_52(fluid):
        row = np.zeros(10)
        tbl_52 = models.Tbl52CaPropertiesLevel1.objects.get(fluid= fluid)
        row[0] = tbl_52.mw
        row[1] = tbl_52.density
        row[2] = tbl_52.nbp
        row[3] = tbl_52.ideal
        row[4] = tbl_52.a
        row[5] = tbl_52.b
        row[6] = tbl_52.c
        row[7] = tbl_52.d
        row[8] = tbl_52.e
        row[9] = tbl_52.auto
        return row

    def GET_RELEASE_PHASE(fluid):
        tbl_52 = models.Tbl52CaPropertiesLevel1.objects.get(fluid=fluid)
        return tbl_52.ambient

    def GET_TBL_58(fluid):
        row = np.zeros(16)
        tbl_58 = models.Tbl58CaComponentDm.objects.get(fluid= fluid)
        row[0] = tbl_58.cainl_gas_a
        row[1] = tbl_58.cainl_gas_b
        row[2] = tbl_58.cainl_liquid_a
        row[3] = tbl_58.cainl_liquid_b
        row[4] = tbl_58.cail_gas_a
        row[5] = tbl_58.cail_gas_b
        row[6] = tbl_58.cail_liquid_a
        row[7] = tbl_58.cail_liquid_b
        row[8] = tbl_58.iainl_gas_a
        row[9] = tbl_58.iainl_gas_b
        row[10] = tbl_58.iainl_liquid_a
        row[11] = tbl_58.iainl_liquid_b
        row[12] = tbl_58.iail_gas_a
        row[13] = tbl_58.iail_gas_b
        row[14] = tbl_58.iail_liquid_a
        row[15] = tbl_58.iail_liquid_b
        return row

    def GET_TBL_59(fluid):
        row = np.zeros(16)
        tbl_59 = models.Tbl59ComponentDamagePerson.objects.get(fluid= fluid)
        row[0] = tbl_59.cainl_gas_a
        row[1] = tbl_59.cainl_gas_b
        row[2] = tbl_59.cainl_liquid_a
        row[3] = tbl_59.cainl_liquid_b
        row[4] = tbl_59.call_gas_a
        row[5] = tbl_59.call_gas_b
        row[6] = tbl_59.call_liquid_a
        row[7] = tbl_59.call_liquid_b
        row[8] = tbl_59.iainl_gas_a
        row[9] = tbl_59.iainl_gas_b
        row[10] = tbl_59.iainl_liquid_a
        row[11] = tbl_59.iainl_liquid_b
        row[12] = tbl_59.iail_gas_a
        row[13] = tbl_59.iail_gas_b
        row[14] = tbl_59.iail_liquid_a
        row[15] = tbl_59.iail_liquid_b
        return row

    def GET_TBL_204(susceptibility):
        row = np.zeros(7)
        tbl_204 = models.Tbl204DmHtha.objects.get(susceptibility= susceptibility)
        row[0] = tbl_204.no_inspection
        row[1] = tbl_204.number_1d
        row[2] = tbl_204.number_1c
        row[3] = tbl_204.number_1b
        row[4] = tbl_204.number_2d
        row[5] = tbl_204.number_2c
        row[6] = tbl_204.number_2b
        #2B=1A nen truong hop A tuong duong 2B
        return row

    def GET_TBL_214(DeltaT, size):
        tbl_214 = models.Tbl214DmNotPwht.objects.get(tmin_tref= DeltaT)
        if size == 6.4:
            return tbl_214.number_6_4
        elif size == 12.7:
            return tbl_214.number_12_7
        elif size == 25.4:
            return tbl_214.number_25_4
        elif size == 38.1:
            return tbl_214.number_38_1
        elif size == 50.8:
            return tbl_214.number_50_8
        elif size == 63.5:
            return tbl_214.number_63_5
        elif size == 76.2:
            return tbl_214.number_76_2
        elif size == 88.9:
            return tbl_214.number_88_9
        else:
            return tbl_214.number_101_6

    def GET_TBL_215(DeltaT, size):
        tbl_215 = models.Tbl215DmPwht.objects.get(tmin_tref= DeltaT)
        if size == 6.4:
            return tbl_215.number_6_4
        elif size == 12.7:
            return tbl_215.number_12_7
        elif size == 25.4:
            return tbl_215.number_25_4
        elif size == 38.1:
            return tbl_215.number_38_1
        elif size == 50.8:
            return tbl_215.number_50_8
        elif size == 63.5:
            return tbl_215.number_63_5
        elif size == 76.2:
            return tbl_215.number_76_2
        elif size == 88.9:
            return tbl_215.number_88_9
        else:
            return tbl_215.number_101_6

    def GET_TBL_511(ART, INSP, Effective):
        if Effective == "E" or INSP == 0:
            tbl_511 = models.Tbl511DfbThin.objects.get(art=ART, insp= 1)
        else:
            tbl_511 = models.Tbl511DfbThin.objects.get(art=ART, insp= INSP)

        if Effective == "A":
            return tbl_511.a
        elif Effective == "B":
            return tbl_511.b
        elif Effective == "C":
            return tbl_511.c
        elif Effective == "D":
            return tbl_511.d
        else:
            return tbl_511.e

    def GET_TBL_512(ART, INSP,Effective):
        if Effective == "E" or INSP == 0:
            tbl_512 = models.Tbl512DfbThinTankBottom.objects.get(art=ART, insp= 1)
        else:
            tbl_512 = models.Tbl512DfbThinTankBottom.objects.get(art=ART, insp= INSP)
        if Effective == "A":
            return tbl_512.a
        elif Effective == "D":
            return tbl_512.d
        elif Effective == "C":
            return tbl_512.c
        elif Effective == "B":
            return tbl_512.b
        else:
            return tbl_512.e

    def GET_TBL_64(YEAR, Suscep):
        if YEAR < 1:
            yr = 1
        elif YEAR >=25:
            yr = 25
        else:
            yr = YEAR
        tbl_64 = models.Tbl64DmLinningInorganic.objects.get(yearssincelastinspection= yr)
        if Suscep == "Strip lined alloy":
            return tbl_64.strip_lined_alloy
        elif Suscep == "Castable refractory":
            return tbl_64.castable_refractory
        elif Suscep == "Castable refractory severe condition":
            return tbl_64.castable_refractory_severe_condition
        elif Suscep == "Glass lined":
            return tbl_64.glass_lined
        elif Suscep == "Acid Brick":
            return tbl_64.acid_brick
        else:
            return tbl_64.fiberglass

    def GET_TBL_65(YEAR, Suscep):
        if YEAR < 1:
            yr = 1
        elif YEAR >=25:
            yr = 25
        else:
            yr = YEAR
        tbl_65 = models.Tbl65DmLinningOrganic.objects.get(yearinservice= yr)
        if Suscep == "WithinLast3Years":
            return tbl_65.withinlast3years
        elif Suscep == "WithinLast6Years":
            return tbl_65.withinlast6years
        else:
            return tbl_65.morethan6years

    def GET_TBL_74(SVI, field):
        tbl_74 = models.Tbl74SccDmPwht.objects.get(svi= SVI)
        if field == "E":
            return tbl_74.e
        elif field == "1D":
            return tbl_74.number_1d
        elif field == "1C":
            return tbl_74.number_1c
        elif field == "1B":
            return tbl_74.number_1b
        elif field == "1A":
            return tbl_74.number_1a
        elif field == "2D":
            return tbl_74.number_2d
        elif field == "2C":
            return tbl_74.number_2c
        elif field == "2B":
            return tbl_74.number_2b
        elif field == "2A":
            return tbl_74.number_2a
        elif field == "3D":
            return tbl_74.number_3d
        elif field == "3C":
            return tbl_74.number_3c
        elif field == "3B":
            return tbl_74.number_3b
        elif field == "3A":
            return tbl_74.number_3a
        elif field == "4D":
            return tbl_74.number_4d
        elif field == "4C":
            return tbl_74.number_4c
        elif field == "4B":
            return tbl_74.number_4b
        elif field == "4A":
            return tbl_74.number_4a
        elif field == "5D":
            return tbl_74.number_5d
        elif field == "5C":
            return tbl_74.number_5c
        elif field == "5B":
            return tbl_74.number_5b
        elif field == "5A":
            return tbl_74.number_5a
        elif field == "6D":
            return tbl_74.number_6d
        elif field == "6C":
            return tbl_74.number_6c
        elif field == "6B":
            return tbl_74.number_6b
        else:
            return tbl_74.number_6a

    def GET_TBL_3B21(locat):
        tbl_3b21 = models.Tbl3B21SiConversion.objects.get(conversionfactory= locat)
        return tbl_3b21.siunits

    def GET_TBL_71_PROPERTIES(FluidTank):
        row = np.zeros(3)
        tbl_71 = models.Tbl71PropertiesStorageTank.objects.get(fluid= FluidTank)
        row[0] = tbl_71.molecular_weight
        row[1] = tbl_71.liquid_density
        row[2] = tbl_71.liquid_density_viscosity
        return row

    def GET_API_COM(APIComponentTypeName):
        row = np.zeros(13)
        api = models.ApiComponentType.objects.get(apicomponenttypename= APIComponentTypeName)
        row[0] = api.gffsmall
        row[1] = api.gffmedium
        row[2] = api.gfflarge
        row[3] = api.gffrupture
        row[4] = api.gfftotal
        row[5] = api.holecostsmall
        row[6] = api.holecostmedium
        row[7] = api.holecostlarge
        row[8] = api.holecostrupture
        row[9] = api.outagesmall
        row[10] = api.outagemedium
        row[11] = api.outagelarge
        row[12] = api.outagerupture
        return row

    def GET_LAST_INSP(ComponentNumber, DamageName, CommissionDate):
        insp_his = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm= DamageName).order_by('-inspectiondate')
        if insp_his.count() == 0:
            return CommissionDate
        else:
            return insp_his[0].inspectiondate

    def GET_MAX_INSP(ComponentNumber, DamageName):
        insp_his = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm=DamageName).order_by('-inspectioneffective')
        if insp_his.count() == 0:
            return "E"
        else:
            return insp_his[insp_his.count()-1].inspectioneffective

    def GET_NUMBER_INSP(ComponentNumber, DamageName):
        insp_his = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm= DamageName).count()
        return insp_his
    def GET_NUMBER_INSP_FOR_THIN_EFFA(ComponentNumber, DamageName):
        a = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm=DamageName,  inspectioneffective="A").count()
        # a = 0
        return a
    def GET_NUMBER_INSP_FOR_THIN_EEFB(ComponentNumber, DamageName):
        b = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm=DamageName,  inspectioneffective="B").count()
        return b
    def GET_NUMBER_INSP_FOR_THIN_EEFC(ComponentNumber, DamageName):
        c = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm=DamageName,  inspectioneffective="C").count()
        return c
    def GET_NUMBER_INSP_FOR_THIN_EEFD(ComponentNumber, DamageName):
        d = models.RwInspectionHistory.objects.filter(componentnumber=ComponentNumber, dm=DamageName, inspectioneffective="D").count()
        return d
    def GET_AGE_INSP(ComponentNumber, DamageName, CommissionDate, AssessmentDate):
        try:
            insp_his = models.RwInspectionHistory.objects.filter(componentnumber= ComponentNumber, dm= DamageName).order_by('-inspectiondate')
            if insp_his.count() == 0:
                date = CommissionDate
            else:
                date = insp_his[0].inspectiondate
            # print("date",date)
            #age_insp = int((AssessmentDate.date() - date.date()).days/365)
            # age_insp = (AssessmentDate.date() - date.date()).days/365
            s1=AssessmentDate.year * 365 + AssessmentDate.month * 30 + AssessmentDate.day
            s2=date.year * 365 + date.month * 30 + date.day
            age_insp=round((s1-s2)/365,3)
            # print(age_insp)
            return round(age_insp,2)
        except Exception as e:
            print("error get ageinspec")
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    ### them vao trong tinh toan ca level 1
    def GET_MODEL_FLUID_TYPE(coffluid):
        cof_fluid = models.CofFluid.objects.get(coffluid=coffluid)
        if (cof_fluid.fluidtype == 0):
            return "Flammable"
        elif (cof_fluid.fluidtype == 1):
            return "Toxic"
        elif (cof_fluid.fluidtype == 2):
            return "Flammable & Toxic"
        else:
            return "No Flammable & No Toxic"

    def GET_TOXIC_FLUID_TYPE(toxicfluid):
        if (toxicfluid == "H2S" or toxicfluid == "CO" or toxicfluid == "PO", toxicfluid == "EE"
        or toxicfluid == "EO" or toxicfluid == "Pyrophoric"):
            return "Flammable & Toxic"
        else:
            return "Toxic"

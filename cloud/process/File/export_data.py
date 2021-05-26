import os
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from cloud import models
from dateutil import relativedelta
from django.http import Http404, HttpResponse
import xlsxwriter
from io import BytesIO
from datetime import datetime

inspMethod = ['Inspection Type', 'ACFM',
                  'Angled Compression Wave',
                  'Angled Shear Wave',
                  'A-scan Thickness Survey',
                  'B-scan',
                  'Chime',
                  'Compton Scatter',
                  'Crack Detection',
                  'C-scan',
                  'Digital Ultrasonic Thickness Gauge',
                  'Endoscopy',
                  'Gamma Radiography',
                  'Hardness Surveys',
                  'Hydrotesting',
                  'Leak Detection',
                  'Liquid Penetrant Inspection',
                  'Lorus',
                  'Low frequency',
                  'Magnetic Fluorescent Inspection',
                  'Magnetic Flux Leakage',
                  'Magnetic Particle Inspection',
                  'Microstructure Replication',
                  'Naked Eye',
                  'On-line Monitoring',
                  'Passive Thermography',
                  'Penetrant Leak Detection',
                  'Pulsed',
                  'Real-time Radiography',
                  'Remote field',
                  'Standard (flat coil)',
                  'Surface Waves',
                  'Teletest',
                  'TOFD',
                  'Transient Thermography',
                  'Video',
                  'X-Radiography']

def convertDF(DF):
    if DF == 0 or DF is None:
        return 'N/A'
    elif DF <= 2:
        return 'A'
    elif DF <= 20:
        return 'B'
    elif DF <= 100:
        return 'C'
    elif DF <= 1000:
        return 'D'
    else:
        return 'E'

def convertCA(CA):
    if CA == 0 or CA is None:
        return 0
    elif CA <= 10000:
        return 1
    elif CA <= 100000:
        return 2
    elif CA <= 1000000:
        return 3
    elif CA <= 10000000:
        return 4
    else:
        return 5

def convertRisk(CA, DF):
    if CA == 0 or DF == 'N/A':
        return 'N/A'
    elif CA in (1, 2) and DF in ('A', 'B', 'C'):
        return "Low"
    elif (CA in (1, 2) and DF == 'D') or (CA in (3, 4) and DF in ('A', 'B')) or (CA == 3 and DF == 'C'):
        return "Medium"
    elif (CA == 5 and DF in ('C', 'D', 'E')) or (CA == 4 and DF == 'E'):
        return "High"
    else:
        return "Medium High"

def checkData(data):
    if data is None:
        return 0
    else:
        return data

def getC_risk(idx):
    dataGeneral = {}
    new = models.RwAssessment.objects.filter(componentid=idx).order_by('-id')
    idxData = 0
    print(new)
    for rwNewAss in new:
        if models.RwFullFcof.objects.filter(id= rwNewAss.id).count() != 0 and models.RwFullPof.objects.filter(id= rwNewAss.id).count() != 0:
            idxData = rwNewAss.id
            break
    print(idxData)
    if idxData != 0:
        newest = models.RwAssessment.objects.get(id= idxData)
        component = models.ComponentMaster.objects.get(componentid=idx)
        if component.componenttypeid_id == 12 or component.componenttypeid_id == 13 or component.componenttypeid_id == 14 or component.componenttypeid_id == 15:
            isTank = 1
        else:
            isTank = 0
        equip = models.EquipmentMaster.objects.get(equipmentid=component.equipmentid_id)
        fcof = models.RwFullFcof.objects.get(id=newest.id)
        fpof = models.RwFullPof.objects.get(id=newest.id)

        dataGeneral['equipment_name'] = equip.equipmentname
        print('cuong',dataGeneral['equipment_name'])
        dataGeneral['equipment_desc'] = equip.equipmentdesc
        dataGeneral['equipment_type'] = models.EquipmentType.objects.get(
            equipmenttypeid=equip.equipmenttypeid_id).equipmenttypename
        dataGeneral['component_name'] = component.componentname
        dataGeneral['init_thinning'] = fpof.thinningap1
        dataGeneral['init_cracking'] = fpof.sccap1
        dataGeneral['init_other'] = fpof.htha_ap1 + fpof.brittleap1 + fpof.fatigueap1
        dataGeneral['init_pof'] = fpof.thinningap1 + fpof.sccap1 + fpof.htha_ap1 + fpof.brittleap1
        dataGeneral['ext_thinning'] = fpof.externalap1
        dataGeneral['pof_catalog'] = fpof.totaldfap1
        dataGeneral['pof_catalog2'] = fpof.totaldfap2
        dataGeneral['pof_val'] = fpof.pofap1
        dataGeneral['risk'] = fpof.pofap1 * fcof.fcofvalue
        dataGeneral['risk_future'] = fpof.pofap2 * fcof.fcofvalue

        if isTank:
            data1 = models.RwCaTank.objects.get(id=newest.id)
            data2 = models.RwInputCaTank.objects.get(id=newest.id)
            dataGeneral['flamable'] = checkData(data1.component_damage_cost)
            dataGeneral['inj'] = 0
            dataGeneral['business'] = checkData(data1.business_cost)
            dataGeneral['env'] = checkData(data1.fc_environ)
            dataGeneral['consequence'] = checkData(data1.consequence)
            dataGeneral['fluid'] = checkData(data2.api_fluid)
            dataGeneral['fluid_phase'] = 'Liquid'
        else:
            data1 = models.RwCaLevel1.objects.get(id=newest.id)
            data2 = models.RwInputCaLevel1.objects.get(id=newest.id)
            dataGeneral['flamable'] = checkData(data1.fc_cmd)
            dataGeneral['inj'] = checkData(data1.fc_inj)
            dataGeneral['business'] = checkData(data1.fc_prod)
            dataGeneral['env'] = checkData(data1.fc_envi)
            dataGeneral['consequence'] = checkData(data1.fc_total)
            dataGeneral['fluid'] = checkData(data2.api_fluid)
            dataGeneral['fluid_phase'] = data2.system
        return dataGeneral

def getE_risk(idx):
    riskE = []
    listComponent = models.ComponentMaster.objects.filter(equipmentid=idx)
    if listComponent.count() != 0:
        for com in listComponent:
            comRisk = getC_risk(com.componentid)
            riskE.append(comRisk)
        return riskE

def getF_risk(idx):
    riskF = []
    lisEquipment = models.EquipmentMaster.objects.filter(facilityid=idx)
    if lisEquipment.count() != 0:
        for eq in lisEquipment:
            riskF.append(getE_risk(eq.equipmentid))
        return riskF

def getS_risk(idx):
    riskS = []
    lisFacility = models.Facility.objects.filter(siteid=idx)
    if lisFacility.count() != 0:
        for fa in lisFacility:
            riskS.append(getF_risk(fa.facilityid))
        return riskS

def getC_insp(idx):
    data = []
    new = models.RwAssessment.objects.filter(componentid=idx).order_by('-id')
    idxData = 0
    for rwNewAss in new:
        if models.RwFullFcof.objects.filter(id=rwNewAss.id).count() != 0 and models.RwFullPof.objects.filter(
                id=rwNewAss.id).count() != 0:
            idxData = rwNewAss.id
            break
    if idxData != 0:
        newest = models.RwAssessment.objects.get(id=idxData)
        equip = models.EquipmentMaster.objects.get(equipmentid= newest.equipmentid_id)
        insp = models.RwDamageMechanism.objects.filter(id_dm= newest.id)
        if insp.count() > 0:
            for a in insp:
                dataGeneral = {}
                dataGeneral['System'] = str(models.ComponentMaster.objects.get(componentid= newest.componentid_id).componentname)
                dataGeneral['Equipment'] = equip.equipmentname
                dataGeneral['Damage'] = models.DmItems.objects.get(dmitemid= a.dmitemid_id).dmdescription
                dataGeneral['Method'] = 'ACFM'
                dataGeneral['Coverage'] = 'N/A'
                dataGeneral['Avaiable'] = 'online'
                dataGeneral['Last'] = a.lastinspdate.date()
                dataGeneral['Duedate'] = a.inspduedate.date()
                dataGeneral['Interval'] = round((insp[0].inspduedate - insp[0].lastinspdate).days/365 ,2)
                data.append(dataGeneral)
    return data

def getE_insp(idx):
    riskE = []
    listComponent = models.ComponentMaster.objects.filter(equipmentid=idx)
    if listComponent.count() != 0:
        for com in listComponent:
            comRisk = getC_insp(com.componentid)
            riskE.append(comRisk)
        return riskE

def getF_insp(idx):
    riskF = []
    lisEquipment = models.EquipmentMaster.objects.filter(facilityid=idx)
    if lisEquipment.count() != 0:
        for eq in lisEquipment:
            riskF.append(getE_insp(eq.equipmentid))
        return riskF

def getS_insp(idx):
    riskS = []
    lisFacility = models.Facility.objects.filter(siteid=idx)
    if lisFacility.count() != 0:
        for fa in lisFacility:
            riskS.append(getF_insp(fa.facilityid))
        return riskS

def getP_risk(idx):
    dataGeneral = {}
    new = models.RwAssessment.objects.filter(id= idx)
    newPof = models.RwFullPof.objects.filter(id= idx)
    newFcof = models.RwFullFcof.objects.filter(id=idx)
    if new.count() != 0 and newPof.count() != 0 and newFcof.count() != 0:
        newest = new[0]
        print('1')
        component = models.ComponentMaster.objects.get(componentid= newest.componentid_id)
        print('component.componenttypeid_id',component.componenttypeid_id)
        if component.componenttypeid_id == 12 or component.componenttypeid_id == 13 or component.componenttypeid_id == 14 or component.componenttypeid_id == 15:
            isTank = 1
        else:
            isTank = 0
        equip = models.EquipmentMaster.objects.get(equipmentid=newest.equipmentid_id)
        fcof = models.RwFullFcof.objects.get(id= idx)
        fpof = models.RwFullPof.objects.get(id= idx)

        dataGeneral['equipment_name'] = equip.equipmentname
        dataGeneral['equipment_desc'] = equip.equipmentdesc
        dataGeneral['equipment_type'] = models.EquipmentType.objects.get(
            equipmenttypeid=equip.equipmenttypeid_id).equipmenttypename
        dataGeneral['component_name'] = component.componentname
        dataGeneral['init_thinning'] = fpof.thinningap1
        dataGeneral['init_cracking'] = fpof.sccap1
        dataGeneral['init_other'] = fpof.htha_ap1 + fpof.brittleap1 + fpof.fatigueap1
        dataGeneral['init_pof'] = fpof.thinningap1 + fpof.sccap1 + fpof.htha_ap1 + fpof.brittleap1
        dataGeneral['ext_thinning'] = fpof.externalap1
        dataGeneral['pof_catalog'] = fpof.totaldfap1
        dataGeneral['pof_catalog2'] = fpof.totaldfap2
        dataGeneral['pof_val'] = fpof.pofap1
        dataGeneral['risk'] = fpof.pofap1 * fcof.fcofvalue
        dataGeneral['risk_future'] = fpof.pofap2 * fcof.fcofvalue
        if isTank:
            data1 = models.RwCaTank.objects.get(id= idx)
            data2 = models.RwInputCaTank.objects.get(id= idx)
            dataGeneral['flamable'] = checkData(data1.component_damage_cost)
            dataGeneral['inj'] = 0
            dataGeneral['business'] = checkData(data1.business_cost)
            dataGeneral['env'] = checkData(data1.fc_environ)
            dataGeneral['consequence'] = checkData(data1.consequence)
            dataGeneral['fluid'] = checkData(data2.api_fluid)
            dataGeneral['fluid_phase'] = 'Liquid'
        else:
            data1 = models.RwCaLevel1.objects.get(id= idx)
            data2 = models.RwInputCaLevel1.objects.get(id= idx)
            dataGeneral['flamable'] = checkData(data1.fc_cmd)
            dataGeneral['inj'] = checkData(data1.fc_inj)
            dataGeneral['business'] = checkData(data1.fc_prod)
            dataGeneral['env'] = checkData(data1.fc_envi)
            dataGeneral['consequence'] = checkData(data1.fc_total)
            dataGeneral['fluid'] = checkData(data2.api_fluid)
            dataGeneral['fluid_phase'] = 'Liquid'

        return dataGeneral

def getP_insp(idx):
    data = []
    new = models.RwAssessment.objects.filter(id= idx)
    newPof = models.RwFullPof.objects.filter(id=idx)
    newFcof = models.RwFullFcof.objects.filter(id=idx)
    if new.count() != 0 and newPof.count() != 0 and newFcof.count() != 0:
        newest = new[0]
        equip = models.EquipmentMaster.objects.get(equipmentid= newest.equipmentid_id)
        insp = models.RwDamageMechanism.objects.filter(id_dm= newest.id)
        print('insp.count',insp.count())
        if insp.count() > 0:
            for a in insp:
                dmitem=models.DMItems.objects.get(dmitemid= a.dmitemid_id)
                dataGeneral = {}
                dataGeneral['System'] = str(models.ComponentMaster.objects.get(componentid= newest.componentid_id).componentname)
                dataGeneral['Equipment'] = equip.equipmentname
                dataGeneral['Damage'] = dmitem.dmdescription

                dataGeneral['Method'] = 'ACFM'
                dataGeneral['Coverage'] = 'N/A'
                dataGeneral['Avaiable'] = 'online'
                dataGeneral['Last'] = a.lastinspdate.date()

                dataGeneral['Duedate'] = a.inspduedate.date()
                dataGeneral['Interval'] = round((insp[0].inspduedate - insp[0].lastinspdate).days/365 ,2)
                data.append(dataGeneral)
    return data
def getP_insp_show(idx):
    dataGeneral = {}
    new = models.RwAssessment.objects.filter(id= idx)
    newPof = models.RwFullPof.objects.filter(id=idx)
    newFcof = models.RwFullFcof.objects.filter(id=idx)
    if new.count() != 0 and newPof.count() != 0 and newFcof.count() != 0:
        newest = new[0]
        equip = models.EquipmentMaster.objects.get(equipmentid= newest.equipmentid_id)
        insp = models.RwDamageMechanism.objects.filter(id_dm= newest.id)
        print('insp.count',insp.count())
        if insp.count() > 0:
            for a in insp:
                dmitem=models.DMItems.objects.get(dmitemid= a.dmitemid_id)
                dataGeneral = {}
                dataGeneral['System'] = str(models.ComponentMaster.objects.get(componentid= newest.componentid_id).componentname)

                dataGeneral['Equipment'] = equip.equipmentname
                print('id',dmitem.dmdescription)
                dataGeneral['Damage'] = dmitem.dmdescription

                dataGeneral['Method'] = 'ACFM'
                dataGeneral['Coverage'] = 'N/A'
                dataGeneral['Avaiable'] = 'online'
                dataGeneral['Last'] = a.lastinspdate.date()

                dataGeneral['Duedate'] = a.inspduedate.date()
                dataGeneral['Interval'] = round((insp[0].inspduedate - insp[0].lastinspdate).days/365 ,2)
                # data.append(dataGeneral)
    return dataGeneral
def getP_name(idx):
    data = {}
    obj = models.RwAssessment.objects.filter(id = idx)
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    if obj.count() != 0:
        data['name'] = obj[0].proposalname
    return 'Proposal:' + data['name'] + '-' + date

def getC_name(idx):
    data = {}
    obj = models.ComponentMaster.objects.filter(componentid= idx)
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    if obj.count() != 0:
        data['name'] = obj[0].componentname
    return 'Component:' + data['name'] + '-' + date

def getE_name(idx):
    data = {}
    obj = models.EquipmentMaster.objects.filter(equipmentid= idx)
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    if obj.count() != 0:
        data['name'] = obj[0].equipmentname
    return 'Equipment:' + data['name'] + '-' + date

def getF_name(idx):
    data = {}
    obj = models.Facility.objects.filter(facilityid= idx)
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    if obj.count() != 0:
        data['name'] = obj[0].facilityname
    return 'Facility:' + data['name'] + '-' + date

def getS_name(idx):
    data = {}
    obj = models.Sites.objects.filter(siteid= idx)
    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    if obj.count() != 0:
        data['name'] = obj[0].sitename
    return 'Site:' + data['name'] + '-' + date

def excelExport(idx, status):
    if status == 'Site':
        rank = 1
    elif status == 'Facility':
        rank = 2
    elif status == 'Equipment':
        rank = 3
    elif status == 'Component':
        rank = 4
    elif status == 'Proposal':
        print('status=',status)
        rank = 5
    else:
        raise Http404

    ################ CREATE FORMAT EXCEL FILE#################
    # print('himolaha')
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Risk Summary')
    worksheet1 = workbook.add_worksheet('Risk Summary Detail')
    worksheet2 = workbook.add_worksheet('Inspection Plan')
    worksheet3 = workbook.add_worksheet('Lookup')
    worksheet4 = workbook.add_worksheet('RBMI.EQs Data Collection')

    format = workbook.add_format()
    format.set_font_name('Times New Roman')
    format.set_font_size(14)
    format.set_border()
    format.set_rotation(90)
    format.set_align('center')
    format.set_bg_color('#B7B7B7')

    format1 = workbook.add_format()
    format1.set_font_name('Times New Roman')
    format1.set_font_size(14)
    format1.set_border()
    format1.set_align('center')
    format1.set_align('vcenter')
    format1.set_bg_color('#B7B7B7')

    format2 = workbook.add_format()
    format2.set_font_name('Arial')
    format2.set_font_size(14)
    format2.set_border()
    format2.set_align('center')
    format2.set_align('vcenter')
    format2.set_bg_color('#B7B7B7')

    format3 = workbook.add_format()
    format3.set_font_name('Arial')
    format3.set_font_size(11)
    format3.set_border()
    format3.set_align('left')
    format3.set_align('vcenter')
    format3.set_bg_color('#B7B7B7')

    format49 = workbook.add_format()
    format49.set_font_name('Times New Roman')
    format49.set_font_size(14)
    format49.set_border()
    format49.set_rotation(90)
    format49.set_align('center')
    format49.set_bg_color('FFFFFF')
    format4 = workbook.add_format()
    format4.set_font_name('Times New Roman')
    format4.set_font_size(14)
    format4.set_border()
    format4.set_align('center')
    format4.set_bg_color('FFFF99')
    format42 = workbook.add_format()
    format42.set_font_name('Times New Roman')
    format42.set_font_size(14)
    format42.set_bg_color('CCFF99')
    format43 = workbook.add_format()
    format43.set_font_name('Times New Roman')
    format43.set_font_size(14)
    format43.set_bg_color('#FFFF00')
    format44 = workbook.add_format()
    format44.set_font_name('Times New Roman')
    format44.set_font_size(14)
    format44.set_bg_color('FF9999')
    format45 = workbook.add_format()
    format45.set_font_name('Times New Roman')
    format45.set_font_size(14)
    format45.set_bg_color('#CD96CD')
    format46 = workbook.add_format()
    format46.set_font_name('Times New Roman')
    format46.set_font_size(14)
    format46.set_bg_color('#CD8162')
    format47 = workbook.add_format()
    format47.set_font_name('Times New Roman')
    format47.set_font_size(14)
    format47.set_bg_color('#EE2C2C')
    format48 = workbook.add_format()
    format48.set_font_name('Times New Roman')
    format48.set_font_size(14)
    format48.set_bg_color('FFFFFF')

    formatdata = workbook.add_format()
    formatdata.set_font_name('Times New Roman')
    formatdata.set_font_size(13)

    formattime = workbook.add_format({'num_format': 'dd/mm/yyyy'})
    formatdata.set_font_name('Times New Roman')
    formattime.set_font_size(13)

    red = workbook.add_format({'bg_color': '#FF0000'})
    green = workbook.add_format({'bg_color': '#00FF00'})
    yellow = workbook.add_format({'bg_color': '#F9F400'})
    orange = workbook.add_format({'bg_color': '#FF9900'})
    gray = workbook.add_format({'bg_color': '#AAAAAA'})

    ## Sheet lookup
    for i in range(1, len(inspMethod) + 1):
        worksheet3.write('A' + str(i), inspMethod[i - 1], formatdata)
    worksheet3.hide()

    ### SHEET HEADING
    ### sheet 1 RiskSummary Ban Tho
    worksheet.merge_range('A1:D1', 'Indentification', format1)
    worksheet.set_column('A2:A2', 20)
    worksheet.set_column('C2:C2', 30)
    worksheet.set_column('B2:B2', 30)
    worksheet.set_column('D2:D2', 20)
    worksheet.write('A2', 'Equipment', format)
    worksheet.write('B2', 'Equipment Description', format)
    worksheet.write('C2', 'Equipment Type', format)
    worksheet.write('D2', 'Components', format)
    worksheet.merge_range('E1:E2', 'Represent.fluid', format)
    worksheet.merge_range('F1:F2', 'Fluid phase', format)
    worksheet.merge_range('G1:M1', 'Consequence (COF)', format1)
    worksheet.merge_range('O1:W1', 'Probability (POF)', format1)
    worksheet.merge_range('X1:Y1', 'Risk', format1)
    worksheet.write('G2', 'Current Risk', format)
    worksheet.write('H2', 'Cofcat.Flammable', format)
    worksheet.write('I2', 'Cofcat.People', format)
    worksheet.write('J2', 'Cofcat.Asset', format)
    worksheet.write('K2', 'Cofcat.Env', format)
    worksheet.write('L2', 'Cofcat.Reputation', format)
    worksheet.write('M2', 'Cofcat.Combined', format)
    worksheet.merge_range('N1:N2', 'Component Material Glade', format)
    worksheet.write('O2', 'InitThinningPOFCatalog', format)
    worksheet.write('P2', 'InitEnv.Cracking', format)
    worksheet.write('Q2', 'InitOtherPOFCatalog', format)
    worksheet.write('R2', 'InitPOFCatelog', format)
    worksheet.write('S2', 'ExtThinningPOF', format)
    worksheet.write('T2', 'ExtEnvCrackingProbabilityCatelog', format)
    worksheet.write('U2', 'ExtOtherPOFCatelog', format)
    worksheet.write('V2', 'ExtPOFCatelog', format)
    worksheet.write('W2', 'POFCategory', format)
    worksheet.write('X2', 'Current Risk', format)
    worksheet.set_column('X2:X2', 20)
    worksheet.write('Y2', 'Future Risk', format)
    worksheet.set_column('Y2:Y2', 20)

    ### sheet 2 RiskSummary Ban Tinh
    worksheet1.merge_range('A1:D1', 'Indentification', format1)
    worksheet1.set_column('A2:A2', 20)
    worksheet1.set_column('C2:C2', 30)
    worksheet1.set_column('B2:B2', 30)
    worksheet1.set_column('D2:D2', 20)
    worksheet1.write('A2', 'Equipment', format)
    worksheet1.write('B2', 'Equipment Description', format)
    worksheet1.write('C2', 'Equipment Type', format)
    worksheet1.write('D2', 'Components', format)
    worksheet1.merge_range('E1:E2', 'Represent.fluid', format)
    worksheet1.merge_range('F1:F2', 'Fluid phase', format)
    worksheet1.merge_range('G1:M1', 'Consequence (COF), $', format1)
    worksheet1.merge_range('O1:W1', 'Probability (POF)', format1)
    worksheet1.merge_range('X1:Y1', 'Risk, $/year', format1)
    worksheet1.write('G2', 'Current Risk', format)
    worksheet1.write('H2', 'Cofcat.Flammable', format)
    worksheet1.write('I2', 'Cofcat.People', format)
    worksheet1.write('J2', 'Cofcat.Asset', format)
    worksheet1.write('K2', 'Cofcat.Env', format)
    worksheet1.write('L2', 'Cofcat.Reputation', format)
    worksheet1.write('M2', 'Cofcat.Combined', format)
    worksheet1.merge_range('N1:N2', 'Component Material Glade', format)
    worksheet1.write('O2', 'InitThinningPOFCatalog', format)
    worksheet1.write('P2', 'InitEnv.Cracking', format)
    worksheet1.write('Q2', 'InitOtherPOFCatalog', format)
    worksheet1.write('R2', 'InitPOFCatelog', format)
    worksheet1.write('S2', 'ExtThinningPOF', format)
    worksheet1.write('T2', 'ExtEnvCrackingProbabilityCatelog', format)
    worksheet1.write('U2', 'ExtOtherPOFCatelog', format)
    worksheet1.write('V2', 'ExtPOFCatelog', format)
    worksheet1.write('W2', 'POFCategory', format)
    worksheet1.write('X2', 'Current Risk', format)
    worksheet1.set_column('X2:X2', 20)
    worksheet1.write('Y2', 'Future Risk', format)
    worksheet1.set_column('Y2:Y2', 20)

    ### sheet 4
    worksheet4.write('A3', 'No.', format49)
    worksheet4.write('B3', 'Unit', format49)
    worksheet4.write('C3', 'Equipment ID', format49)
    worksheet4.write('D3', 'Equipment Description', format49)
    worksheet4.write('E3', 'Equipment Type', format49)
    worksheet4.write('F3', 'Component Type', format49)
    worksheet4.write('G3', 'P&ID Code', format49)
    worksheet4.write('H3', 'Contruction Code', format49)
    worksheet4.write('I3', 'Year built', format49)
    worksheet4.write('J3', 'Date in service', format49)
    worksheet4.write('K3', 'Bundle Type', format49)
    worksheet4.write('L3', 'No.of tubes', format49)
    worksheet4.write('M3', 'Orientation', format49)
    worksheet4.write('N3', 'Lenggth(mm)', format49)
    worksheet4.write('O3', 'No.of shellbands', format49)
    worksheet4.write('P3', 'No.of heads/covers', format49)
    worksheet4.write('Q3', 'No.of nozzles', format49)
    worksheet4.write('R3', 'Internal entry possible(Y/N)', format49)
    worksheet4.write('S3', 'Des.Press(barg)', format49)
    worksheet4.write('T3', 'Des.Temp(C)', format49)
    worksheet4.write('U3', 'Material Specification', format49)
    worksheet4.write('V3', 'Material Grade', format49)
    worksheet4.write('W3', 'Linning/Cladding', format49)
    worksheet4.write('X3', 'Diameter(mm)', format49)
    worksheet4.write('Y3', 'J.E)', format49)
    worksheet4.write('Z3', 'Rep.Thickness(mm)', format49)
    worksheet4.write('AA3', 'Corrosion Allowance', format49)
    worksheet4.write('AB3', 'M.D.M.T(C)', format49)
    worksheet4.write('AC3', 'PWHT(C)', format49)
    worksheet4.write('AD3', 'Op.Press(barg)', format49)
    worksheet4.write('AE3', 'Op.Temp(C)', format49)
    worksheet4.write('AF3', 'Fluild Initial State)', format49)
    worksheet4.write('AG3', 'Rep.Fluid', format49)
    worksheet4.write('AH3', 'Rep.Fuild(%wt)', format49)
    worksheet4.write('AI3', 'Major Component', format49)
    worksheet4.write('AJ3', 'Major Com.p(%wt)', format49)
    worksheet4.write('AK3', 'Water(Y/N?)', format49)
    worksheet4.write('AL3', 'Water content(%)', format49)
    worksheet4.write('AM3', 'Water pH', format49)
    worksheet4.write('AN3', 'Other Contaminant', format49)
    worksheet4.write('AO3', 'Content(%)', format49)
    worksheet4.write('AP3', 'Toxic Fluid', format49)
    worksheet4.write('AQ3', 'Toxic fluid(wt%)', format49)
    worksheet4.write('AR3', 'Suggested Damage Mechanism', format49)
    worksheet4.write('AS3', 'Suggested Corrosion Type', format49)
    worksheet4.write('AT3', 'Exp.Internal C.R(mm/yr)', format49)
    worksheet4.write('AU3', 'Pitting Potential(H/M/L)', format49)
    worksheet4.write('AV3', 'Linning/Coating(Enter material if Yes)', format49)
    worksheet4.write('AW3', 'Insulated', format49)
    worksheet4.write('AX3', 'Suggested External Damage Mechanism', format49)
    worksheet4.write('AY3', 'Susceptible to Ex.Corr?', format49)
    worksheet4.write('AZ3', 'Coating(Best/Average/None)', format49)
    worksheet4.write('BA3', 'Area Humidity(H/M/L)', format49)
    worksheet4.write('BB3', 'External Wetting (Y/N)', format49)
    worksheet4.write('BC3', 'Intermittent Service(Y/N)', format49)
    worksheet4.write('BD3', 'Traced(Steam/Electric/None)', format49)
    worksheet4.write('BE3', 'Exp.external C.R(mm/yr)', format49)
    worksheet4.write('BF3', 'Initial Potential', format49)
    worksheet4.write('BG3', 'Cracking agent1', format49)
    worksheet4.write('BH3', 'Concentration1(%)', format49)
    worksheet4.write('BI3', 'Enviromental Cracking Mechanism', format49)
    worksheet4.write('BJ3', 'Env.Cracking Probability Category', format49)
    worksheet4.write('BK3', 'Initial Potential2', format49)
    worksheet4.write('BL3', 'Consequence Flammable', format49)
    worksheet4.write('BM3', 'Production Loss', format49)
    worksheet4.write('BN3', 'Consequence prodution Leak', format49)
    worksheet4.write('BO3', 'Consequence Toxic', format49)
    worksheet4.write('BP3', 'Criticality Run(12/2020)', format49)
    worksheet4.write('BQ3', 'Inspection History', format49)

    worksheet4.write('A1', '1', format4)
    worksheet4.merge_range('A2:AQ2', 'Basic Data', format42)
    worksheet4.write('B1', '2', format4)
    worksheet4.write('C1', '3', format4)
    worksheet4.write('D1', '4', format4)
    worksheet4.write('E1', '5', format4)
    worksheet4.write('F1', '6', format4)
    worksheet4.write('G1', '7', format4)
    worksheet4.write('H1', '8', format4)
    worksheet4.write('I1', '9', format4)
    worksheet4.write('J1', '10', format4)
    worksheet4.write('K1', '11', format4)
    worksheet4.write('L1', '12', format4)
    worksheet4.write('M1', '13', format4)
    worksheet4.write('N1', '14', format4)
    worksheet4.write('O1', '15', format4)
    worksheet4.write('P1', '16', format4)
    worksheet4.write('Q1', '17', format4)
    worksheet4.write('R1', '18', format4)
    worksheet4.write('S1', '19', format4)
    worksheet4.write('T1', '20', format4)
    worksheet4.write('U1', '21', format4)
    worksheet4.write('V1', '22', format4)
    worksheet4.write('W1', '23', format4)
    worksheet4.write('X1', '24', format4)
    worksheet4.write('Y1', '25', format4)
    worksheet4.write('Z1', '26', format4)
    worksheet4.write('AA1', '27', format4)
    worksheet4.write('AB1', '28', format4)
    worksheet4.write('AC1', '29', format4)
    worksheet4.write('AD1', '30', format4)
    worksheet4.write('AE1', '31', format4)
    worksheet4.write('AF1', '32', format4)
    worksheet4.write('AG1', '33', format4)
    worksheet4.write('AH1', '34', format4)
    worksheet4.write('AI1', '35', format4)
    worksheet4.write('AJ1', '36', format4)
    worksheet4.write('AK1', '37', format4)
    worksheet4.write('AL1', '38', format4)
    worksheet4.write('AM1', '39', format4)
    worksheet4.write('AN1', '40', format4)
    worksheet4.write('AO1', '41', format4)
    worksheet4.write('AP1', '42', format4)
    worksheet4.write('AQ1', '43', format4)
    worksheet4.merge_range('AR2:AW2', 'Internal Corrosion', format43)
    worksheet4.write('AR1', '44', format4)
    worksheet4.write('AS1', '45', format4)
    worksheet4.write('AT1', '46', format4)
    worksheet4.write('AU1', '47', format4)
    worksheet4.write('AV1', '48', format4)
    worksheet4.write('AW1', '49', format4)
    worksheet4.write('AX1', '50', format4)
    worksheet4.merge_range('AX2:BE2', 'External Corrosion', format44)
    worksheet4.write('AY1', '51', format4)
    worksheet4.write('AZ1', '52', format4)
    worksheet4.write('BA1', '53', format4)
    worksheet4.write('BB1', '54', format4)
    worksheet4.write('BC1', '55', format4)
    worksheet4.write('BD1', '56', format4)
    worksheet4.write('BE1', '57', format4)
    worksheet4.write('BF1', '58', format4)
    worksheet4.merge_range('BF2:BK2', 'External Env. Cracking', format45)
    worksheet4.write('BG1', '59', format4)
    worksheet4.write('BH1', '60', format4)
    worksheet4.write('BI1', '61', format4)
    worksheet4.write('BJ1', '62', format4)
    worksheet4.write('BK1', '63', format4)
    worksheet4.write('BL1', '64', format4)
    worksheet4.merge_range('BL2:BR2', 'ODM', format46)
    worksheet4.write('BM1', '65', format4)
    worksheet4.write('BN1', '66', format4)
    worksheet4.write('BO1', '67', format4)
    worksheet4.write('BP1', '68', format4)
    worksheet4.write('BQ1', '69', format4)
    worksheet4.write('BR1', '70', format4)
    worksheet4.write('BS1', '71', format4)
    worksheet4.write('BS2', 'RISK', format47)
    ### sheet 3 InspectionPlan
    try:
        number = 41333.5
        worksheet2.set_row(0, 60)
        worksheet2.merge_range('C1:G1', 'INSPECTION WORK PLANNING FOR COMPONENT', format2)

        worksheet2.write('C2', 'Methods', format3)
        worksheet2.set_column('C2:C2', 20)
        worksheet2.write('D2', 'All Methods', format3)
        worksheet2.set_column('D2:D2', 20)

        worksheet2.write('C3', 'Risk Levels', format3)
        worksheet2.set_column('C3:C3', 20)
        worksheet2.write('D3:D3', 'H,MH,M,H', format3)
        worksheet2.set_column('D3:D3', 20)

        worksheet2.write('C4', 'Planning Date', format3)
        worksheet2.set_column('C4:C4', 20)
        format4 = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        format4.set_font_name('Arial')
        format4.set_font_size(11)
        format4.set_border()
        format4.set_align('left')
        format4.set_align('vcenter')
        format4.set_bg_color('#B7B7B7')
        worksheet2.write('D4', datetime.now(), format4)
        worksheet2.set_column('D4:D4', 20)

        worksheet2.write('F2', 'Equipment Type', format3)
        worksheet2.set_column('F2:F2', 20)
        worksheet2.write('G2', 'ALL  EQUIPMENTS & PIPES', format3)
        worksheet2.set_column('G2:G2', 20)

        rwass = models.RwAssessment.objects.get(id = idx)
        equip = models.EquipmentMaster.objects.filter(equipmentid=rwass.equipmentid_id)[0].facilityid_id
        print(equip)
        unit = models.Facility.objects.filter(facilityid=equip)[0].facilityname
        worksheet2.write('F3', 'Units', format3)
        worksheet2.set_column('F3:F3', 20)
        worksheet2.write('G3', unit, format3)
        worksheet2.set_column('G3:G3', 20)

        worksheet2.write('F4', 'Total', format3)
        worksheet2.set_column('F4:F4', 20)
        worksheet2.write('G4', '1', format3)
        worksheet2.set_column('G4:G4', 20)


        worksheet2.write('A5', 'Unit', format1)
        worksheet2.set_column('A5:A5', 10)
        worksheet2.write('B5', 'Equipment ID', format1)
        worksheet2.set_column('B5:B5', 15)
        worksheet2.write('C5', 'Equipment Type', format1)
        worksheet2.set_column('C5:C5', 20)
        worksheet2.write('D5', 'Damage Mechanism', format1)
        worksheet2.set_column('D5:D5', 30)
        worksheet2.write('E5', 'Inspec Priority', format1)
        worksheet2.set_column('E5:E5', 17)
        worksheet2.write('F5', 'Method', format1)
        worksheet2.set_column('F5:F5', 40)
        worksheet2.write('G5', 'Extend', format1)
        worksheet2.set_column('G5:G5', 40)
        worksheet2.write('H5', 'Availability', format1)
        worksheet2.set_column('H5:H5', 20)
        worksheet2.write('I5', 'Last Insp. Date', format1)
        worksheet2.set_column('I5:I5', 20)
        worksheet2.write('J5', 'Date Due', format1)
        worksheet2.set_column('J5:J5', 15)

        print('rank=',rank)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)



    ###### CONTENT ########
    # Write Risk
    # proposal
    if rank == 5:

        dataP = getP_risk(idx)
        # insp_P = getP_insp(idx)
        insp_P = get_inspection_work_planning(idx)
        name = getP_name(idx)
        insp_ind = 6
        print("dat")
        if dataP is not None:
            worksheet.write('A3', dataP['equipment_name'], formatdata)
            worksheet.write('B3', dataP['equipment_desc'], formatdata)
            worksheet.write('C3', dataP['equipment_type'], formatdata)
            worksheet.write('D3', dataP['component_name'], formatdata)
            worksheet.write('O3', convertDF(dataP['init_thinning']), formatdata)
            worksheet.write('P3', convertDF(dataP['init_cracking']), formatdata)
            worksheet.write('Q3', convertDF(dataP['init_other']), formatdata)
            worksheet.write('R3', convertDF(dataP['init_pof']), formatdata)
            worksheet.write('S3', convertDF(dataP['ext_thinning']), formatdata)
            worksheet.write('T3', convertDF(0), formatdata)
            worksheet.write('U3', convertDF(0), formatdata)
            worksheet.write('V3', convertDF(dataP['ext_thinning']), formatdata)
            worksheet.write('W3', convertDF(dataP['pof_catalog']), formatdata)
            worksheet.write('E3', dataP['fluid'], formatdata)
            worksheet.write('F3', dataP['fluid_phase'], formatdata)
            worksheet.write('G3', 'N/A', formatdata)
            worksheet.write('H3', convertCA(dataP['flamable']), formatdata)
            worksheet.write('I3', convertCA(dataP['inj']), formatdata)
            worksheet.write('J3', convertCA(dataP['business']), formatdata)
            worksheet.write('K3', convertCA(dataP['env']), formatdata)
            worksheet.write('L3', 'N/A', formatdata)
            worksheet.write('M3', convertCA(dataP['consequence']), formatdata)
            worksheet.write('X3', convertRisk(convertCA(dataP['consequence']), convertDF(dataP['pof_catalog'])), formatdata)
            worksheet.write('Y3', convertRisk(convertCA(dataP['consequence']), convertDF(dataP['pof_catalog2'])), formatdata)

            worksheet1.write('A3', dataP['equipment_name'], formatdata)
            worksheet1.write('B3', dataP['equipment_desc'], formatdata)
            worksheet1.write('C3', dataP['equipment_type'], formatdata)
            worksheet1.write('D3', dataP['component_name'], formatdata)
            worksheet1.write('O3', dataP['init_thinning'], formatdata)
            worksheet1.write('P3', dataP['init_cracking'], formatdata)
            worksheet1.write('Q3', dataP['init_other'], formatdata)
            worksheet1.write('R3', dataP['init_pof'], formatdata)
            worksheet1.write('S3', dataP['ext_thinning'], formatdata)
            worksheet1.write('T3', 'N/A', formatdata)
            worksheet1.write('U3', 'N/A', formatdata)
            worksheet1.write('V3', dataP['ext_thinning'], formatdata)
            worksheet1.write('W3', dataP['pof_catalog'], formatdata)
            worksheet1.write('E3', dataP['fluid'], formatdata)
            worksheet1.write('F3', dataP['fluid_phase'], formatdata)
            worksheet1.write('G3', 'N/A', formatdata)
            worksheet1.write('H3', dataP['flamable'], formatdata)
            worksheet1.write('I3', dataP['inj'], formatdata)
            worksheet1.write('J3', dataP['business'], formatdata)
            worksheet1.write('K3', dataP['env'], formatdata)
            worksheet1.write('L3', 'N/A', formatdata)
            worksheet1.write('M3', dataP['consequence'], formatdata)
            worksheet1.write('X3', dataP['risk'], formatdata)
            worksheet1.write('Y3', dataP['risk_future'], formatdata)

        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"High"', 'format': red})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"Medium High"', 'format': orange})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"Medium"', 'format': yellow})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"Low"', 'format': green})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"N/A"', 'format': gray})

        if insp_P is not None:
            for insp in insp_P:
                if insp is not None:
                    worksheet2.write('A' + str(insp_ind), insp['unit'], formatdata)
                    worksheet2.write('B' + str(insp_ind), insp['equipment_id'], formatdata)
                    worksheet2.write('C' + str(insp_ind), insp['equipment_type'],
                                     formatdata)
                    worksheet2.write('D' + str(insp_ind), insp['damage'], formatdata)

                    worksheet2.write('E' + str(insp_ind), insp['inspec_priority'], formatdata)
                    worksheet2.write('F' + str(insp_ind), insp['method'], formatdata)
                    # worksheet2.data_validation('F' + str(insp_ind), {'validate': 'list', 'source': '=Lookup!$A$2:$A$37'})

                    worksheet2.write('G' + str(insp_ind), insp['extend'], formatdata)
                    worksheet2.write('H' + str(insp_ind), insp['avaiable'], formatdata)
                    # worksheet2.data_validation('H' + str(insp_ind), {'validate': 'list',
                    #                                                  'source': ['online', 'shutdown']})
                    worksheet2.write('I' + str(insp_ind), insp['Last'], formattime)
                    worksheet2.write('J' + str(insp_ind), insp['Duedate'], formattime)
                    insp_ind += 1
    elif rank == 4:
        dataC = getC_risk(idx)
        insp_C = getC_insp(idx)
        insp_ind = 2
        name = getC_name(idx)
        if dataC is not None:
            worksheet.write('A3', dataC['equipment_name'], formatdata)
            worksheet.write('B3', dataC['equipment_desc'], formatdata)
            worksheet.write('C3', dataC['equipment_type'], formatdata)
            worksheet.write('D3', dataC['component_name'], formatdata)
            worksheet.write('O3', convertDF(dataC['init_thinning']), formatdata)
            worksheet.write('P3', convertDF(dataC['init_cracking']), formatdata)
            worksheet.write('Q3', convertDF(dataC['init_other']), formatdata)
            worksheet.write('R3', convertDF(dataC['init_pof']), formatdata)
            worksheet.write('S3', convertDF(dataC['ext_thinning']), formatdata)
            worksheet.write('T3', convertDF(0), formatdata)
            worksheet.write('U3', convertDF(0), formatdata)
            worksheet.write('V3', convertDF(dataC['ext_thinning']), formatdata)
            worksheet.write('W3', convertDF(dataC['pof_catalog']), formatdata)
            worksheet.write('E3', dataC['fluid'], formatdata)
            worksheet.write('F3', dataC['fluid_phase'], formatdata)
            worksheet.write('G3', 'N/A', formatdata)
            worksheet.write('H3', convertCA(dataC['flamable']), formatdata)
            worksheet.write('I3', convertCA(dataC['inj']), formatdata)
            worksheet.write('J3', convertCA(dataC['business']), formatdata)
            worksheet.write('K3', convertCA(dataC['env']), formatdata)
            worksheet.write('L3', 'N/A', formatdata)
            worksheet.write('M3', convertCA(dataC['consequence']), formatdata)
            worksheet.write('X3', convertRisk(convertCA(dataC['consequence']), convertDF(dataC['pof_catalog'])), formatdata)
            worksheet.write('Y3', convertRisk(convertCA(dataC['consequence']), convertDF(dataC['pof_catalog2'])), formatdata)

            worksheet1.write('A3', dataC['equipment_name'], formatdata)
            worksheet1.write('B3', dataC['equipment_desc'], formatdata)
            worksheet1.write('C3', dataC['equipment_type'], formatdata)
            worksheet1.write('D3', dataC['component_name'], formatdata)
            worksheet1.write('O3', dataC['init_thinning'], formatdata)
            worksheet1.write('P3', dataC['init_cracking'], formatdata)
            worksheet1.write('Q3', dataC['init_other'], formatdata)
            worksheet1.write('R3', dataC['init_pof'], formatdata)
            worksheet1.write('S3', dataC['ext_thinning'], formatdata)
            worksheet1.write('T3', 'N/A', formatdata)
            worksheet1.write('U3', 'N/A', formatdata)
            worksheet1.write('V3', dataC['ext_thinning'], formatdata)
            worksheet1.write('W3', dataC['pof_catalog'], formatdata)
            worksheet1.write('E3', dataC['fluid'], formatdata)
            worksheet1.write('F3', dataC['fluid_phase'], formatdata)
            worksheet1.write('G3', 'N/A', formatdata)
            worksheet1.write('H3', dataC['flamable'], formatdata)
            worksheet1.write('I3', dataC['inj'], formatdata)
            worksheet1.write('J3', dataC['business'], formatdata)
            worksheet1.write('K3', dataC['env'], formatdata)
            worksheet1.write('L3', 'N/A', formatdata)
            worksheet1.write('M3', dataC['consequence'], formatdata)
            worksheet1.write('X3', dataC['risk'], formatdata)
            worksheet1.write('Y3', dataC['risk_future'], formatdata)

        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"High"', 'format': red})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"Medium High"', 'format': orange})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"Medium"', 'format': yellow})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"Low"', 'format': green})
        worksheet.conditional_format('X3:Y3',
                                     {'type': 'cell', 'criteria': '==', 'value': '"N/A"', 'format': gray})

        if insp_C is not None:
            for insp in insp_C:
                if insp is not None:
                    worksheet2.write('B' + str(insp_ind) , insp['System'], formatdata)
                    worksheet2.write('A' + str(insp_ind), insp['Equipment'], formatdata)
                    worksheet2.write('C' + str(insp_ind), insp['Damage'],
                                     formatdata)
                    worksheet2.write('D' + str(insp_ind), insp['Method'], formatdata)
                    worksheet2.data_validation('D' + str(insp_ind), {'validate': 'list', 'source': '=Lookup!$A$2:$A$37'})
                    worksheet2.write('E' + str(insp_ind), insp['Coverage'], formatdata)
                    worksheet2.write('F' + str(insp_ind), insp['Avaiable'], formatdata)
                    worksheet2.data_validation('F' + str(insp_ind), {'validate': 'list',
                                                              'source': ['online', 'shutdown']})
                    worksheet2.write('G' + str(insp_ind), insp['Last'], formattime)
                    worksheet2.write('H' + str(insp_ind), insp['Interval'], formatdata)
                    worksheet2.write('I' + str(insp_ind), insp['Duedate'], formattime)

                    insp_ind += 1
    elif rank == 3:
        dataE = getE_risk(idx)
        insp_E = getE_insp(idx)
        name = getE_name(idx)
        ind = 3
        insp_ind = 2
        if dataE is not None:
            for dataC in dataE:
                if dataC is not None:
                    worksheet.write('A' + str(ind), (dataC['equipment_name']), formatdata)
                    worksheet.write('B' + str(ind), (dataC['equipment_desc']), formatdata)
                    worksheet.write('C' + str(ind), (dataC['equipment_type']), formatdata)
                    worksheet.write('D' + str(ind), (dataC['component_name']), formatdata)
                    worksheet.write('O' + str(ind), convertDF(dataC['init_thinning']), formatdata)
                    worksheet.write('P' + str(ind), convertDF(dataC['init_cracking']), formatdata)
                    worksheet.write('Q' + str(ind), convertDF(dataC['init_other']), formatdata)
                    worksheet.write('R' + str(ind), convertDF(dataC['init_pof']), formatdata)
                    worksheet.write('S' + str(ind), convertDF(dataC['ext_thinning']), formatdata)
                    worksheet.write('T' + str(ind), convertDF(0), formatdata)
                    worksheet.write('U' + str(ind), convertDF(0), formatdata)
                    worksheet.write('V' + str(ind), convertDF(dataC['ext_thinning']), formatdata)
                    worksheet.write('W' + str(ind), convertDF(dataC['pof_catalog']), formatdata)
                    worksheet.write('E' + str(ind), dataC['fluid'], formatdata)
                    worksheet.write('F' + str(ind), dataC['fluid_phase'], formatdata)
                    worksheet.write('G' + str(ind), 'N/A', formatdata)
                    worksheet.write('H' + str(ind), convertCA(dataC['flamable']), formatdata)
                    worksheet.write('I' + str(ind), convertCA(dataC['inj']), formatdata)
                    worksheet.write('J' + str(ind), convertCA(dataC['business']), formatdata)
                    worksheet.write('K' + str(ind), convertCA(dataC['env']), formatdata)
                    worksheet.write('L' + str(ind), 'N/A', formatdata)
                    worksheet.write('M' + str(ind), convertCA(dataC['consequence']), formatdata)
                    worksheet.write('X' + str(ind), convertRisk(convertCA(dataC['consequence']), convertDF(dataC['pof_catalog'])), formatdata)
                    worksheet.write('Y' + str(ind), convertRisk(convertCA(dataC['consequence']), convertDF(dataC['pof_catalog2'])), formatdata)

                    worksheet1.write('A' + str(ind), dataC['equipment_name'], formatdata)
                    worksheet1.write('B' + str(ind), dataC['equipment_desc'], formatdata)
                    worksheet1.write('C' + str(ind), dataC['equipment_type'], formatdata)
                    worksheet1.write('D' + str(ind), dataC['component_name'], formatdata)
                    worksheet1.write('O' + str(ind), dataC['init_thinning'], formatdata)
                    worksheet1.write('P' + str(ind), dataC['init_cracking'], formatdata)
                    worksheet1.write('Q' + str(ind), dataC['init_other'], formatdata)
                    worksheet1.write('R' + str(ind), dataC['init_pof'], formatdata)
                    worksheet1.write('S' + str(ind), dataC['ext_thinning'], formatdata)
                    worksheet1.write('T' + str(ind), 'N/A', formatdata)
                    worksheet1.write('U' + str(ind), 'N/A', formatdata)
                    worksheet1.write('V' + str(ind), dataC['ext_thinning'], formatdata)
                    worksheet1.write('W' + str(ind), dataC['pof_catalog'], formatdata)
                    worksheet1.write('E' + str(ind), dataC['fluid'], formatdata)
                    worksheet1.write('F' + str(ind), dataC['fluid_phase'], formatdata)
                    worksheet1.write('G' + str(ind), 'N/A', formatdata)
                    worksheet1.write('H' + str(ind), dataC['flamable'], formatdata)
                    worksheet1.write('I' + str(ind), dataC['inj'], formatdata)
                    worksheet1.write('J' + str(ind), dataC['business'], formatdata)
                    worksheet1.write('K' + str(ind), dataC['env'], formatdata)
                    worksheet1.write('L' + str(ind), 'N/A', formatdata)
                    worksheet1.write('M' + str(ind), dataC['consequence'], formatdata)
                    worksheet1.write('X' + str(ind), dataC['risk'], formatdata)
                    worksheet1.write('Y' + str(ind), dataC['risk_future'], formatdata)
                    ind += 1
                worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"High"', 'format': red})
                worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"Medium High"',
                                              'format': orange})
                worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"Medium"', 'format': yellow})
                worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"Low"', 'format': green})
                worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"N/A"', 'format': gray})
        if insp_E is not None:
            for C in insp_E:
                if C is not None:
                    for insp in C:
                        if insp is not None:
                            worksheet2.write('B' + str(insp_ind), insp['System'], formatdata)
                            worksheet2.write('A' + str(insp_ind), insp['Equipment'], formatdata)
                            worksheet2.write('C' + str(insp_ind), insp['Damage'],
                                             formatdata)
                            worksheet2.write('D' + str(insp_ind), insp['Method'], formatdata)
                            worksheet2.data_validation('D' + str(insp_ind),
                                                       {'validate': 'list', 'source': '=Lookup!$A$2:$A$37'})
                            worksheet2.write('E' + str(insp_ind), insp['Coverage'], formatdata)
                            worksheet2.write('F' + str(insp_ind), insp['Avaiable'], formatdata)
                            worksheet2.data_validation('F' + str(insp_ind), {'validate': 'list',
                                                                             'source': ['online', 'shutdown']})
                            worksheet2.write('G' + str(insp_ind), insp['Last'], formattime)
                            worksheet2.write('H' + str(insp_ind), insp['Interval'], formatdata)
                            worksheet2.write('I' + str(insp_ind), insp['Duedate'], formattime)
                            insp_ind += 1
    elif rank == 2:
        dataF = getF_risk(idx)
        insp_F = getF_insp(idx)
        name = getF_name(idx)
        ind = 3
        insp_ind = 2
        if dataF is not None:
            for dataE in dataF:
                if dataE is not None:
                    for dataC in dataE:
                        if dataC is not None:
                            worksheet.write('A' + str(ind), (dataC['equipment_name']), formatdata)
                            worksheet.write('B' + str(ind), (dataC['equipment_desc']), formatdata)
                            worksheet.write('C' + str(ind), (dataC['equipment_type']), formatdata)
                            worksheet.write('D' + str(ind), (dataC['component_name']), formatdata)
                            worksheet.write('O' + str(ind), convertDF(dataC['init_thinning']),
                                                formatdata)
                            worksheet.write('P' + str(ind), convertDF(dataC['init_cracking']),
                                                formatdata)
                            worksheet.write('Q' + str(ind), convertDF(dataC['init_other']), formatdata)
                            worksheet.write('R' + str(ind), convertDF(dataC['init_pof']), formatdata)
                            worksheet.write('S' + str(ind), convertDF(dataC['ext_thinning']),
                                                formatdata)
                            worksheet.write('T' + str(ind), convertDF(0), formatdata)
                            worksheet.write('U' + str(ind), convertDF(0), formatdata)
                            worksheet.write('V' + str(ind), convertDF(dataC['ext_thinning']), formatdata)
                            worksheet.write('W' + str(ind), convertDF(dataC['pof_catalog']), formatdata)
                            worksheet.write('E' + str(ind), dataC['fluid'], formatdata)
                            worksheet.write('F' + str(ind), dataC['fluid_phase'], formatdata)
                            worksheet.write('G' + str(ind), 'N/A', formatdata)
                            worksheet.write('H' + str(ind), convertCA(dataC['flamable']), formatdata)
                            worksheet.write('I' + str(ind), convertCA(dataC['inj']), formatdata)
                            worksheet.write('J' + str(ind), convertCA(dataC['business']), formatdata)
                            worksheet.write('K' + str(ind), convertCA(dataC['env']), formatdata)
                            worksheet.write('L' + str(ind), 'N/A', formatdata)
                            worksheet.write('M' + str(ind), convertCA(dataC['consequence']), formatdata)
                            worksheet.write('X' + str(ind),
                                                convertRisk(convertCA(dataC['consequence']),
                                                                        convertDF(dataC['pof_catalog'])),
                                                formatdata)
                            worksheet.write('Y' + str(ind),
                                                convertRisk(convertCA(dataC['consequence']),
                                                                        convertDF(dataC['pof_catalog2'])),
                                                formatdata)

                            worksheet1.write('A' + str(ind), dataC['equipment_name'], formatdata)
                            worksheet1.write('B' + str(ind), dataC['equipment_desc'], formatdata)
                            worksheet1.write('C' + str(ind), dataC['equipment_type'], formatdata)
                            worksheet1.write('D' + str(ind), dataC['component_name'], formatdata)
                            worksheet1.write('O' + str(ind), dataC['init_thinning'], formatdata)
                            worksheet1.write('P' + str(ind), dataC['init_cracking'], formatdata)
                            worksheet1.write('Q' + str(ind), dataC['init_other'], formatdata)
                            worksheet1.write('R' + str(ind), dataC['init_pof'], formatdata)
                            worksheet1.write('S' + str(ind), dataC['ext_thinning'], formatdata)
                            worksheet1.write('T' + str(ind), 'N/A', formatdata)
                            worksheet1.write('U' + str(ind), 'N/A', formatdata)
                            worksheet1.write('V' + str(ind), dataC['ext_thinning'], formatdata)
                            worksheet1.write('W' + str(ind), dataC['pof_catalog'], formatdata)
                            worksheet1.write('E' + str(ind), dataC['fluid'], formatdata)
                            worksheet1.write('F' + str(ind), dataC['fluid_phase'], formatdata)
                            worksheet1.write('G' + str(ind), 'N/A', formatdata)
                            worksheet1.write('H' + str(ind), dataC['flamable'], formatdata)
                            worksheet1.write('I' + str(ind), dataC['inj'], formatdata)
                            worksheet1.write('J' + str(ind), dataC['business'], formatdata)
                            worksheet1.write('K' + str(ind), dataC['env'], formatdata)
                            worksheet1.write('L' + str(ind), 'N/A', formatdata)
                            worksheet1.write('M' + str(ind), dataC['consequence'], formatdata)
                            worksheet1.write('X' + str(ind), dataC['risk'], formatdata)
                            worksheet1.write('Y' + str(ind), dataC['risk_future'], formatdata)
                            ind += 1
            worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"High"', 'format': red})
            worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"Medium High"',
                                              'format': orange})
            worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"Medium"', 'format': yellow})
            worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"Low"', 'format': green})
            worksheet.conditional_format('X3:Y' + str(ind),
                                             {'type': 'cell', 'criteria': '==', 'value': '"N/A"', 'format': gray})
        if insp_F is not None:
            for E in insp_F:
                if E is not None:
                    for C in E:
                        if C is not None:
                            for insp in C:
                                if insp is not None:
                                    worksheet2.write('B' + str(insp_ind), insp['System'], formatdata)
                                    worksheet2.write('A' + str(insp_ind), insp['Equipment'], formatdata)
                                    worksheet2.write('C' + str(insp_ind), insp['Damage'],
                                                         formatdata)
                                    worksheet2.write('D' + str(insp_ind), insp['Method'], formatdata)
                                    worksheet2.data_validation('D' + str(insp_ind),
                                                                   {'validate': 'list', 'source': '=Lookup!$A$2:$A$37'})
                                    worksheet2.write('E' + str(insp_ind), insp['Coverage'], formatdata)
                                    worksheet2.write('F' + str(insp_ind), insp['Avaiable'], formatdata)
                                    worksheet2.data_validation('F' + str(insp_ind), {'validate': 'list',
                                                                                         'source': ['online',
                                                                                                    'shutdown']})
                                    worksheet2.write('G' + str(insp_ind), insp['Last'], formattime)
                                    worksheet2.write('H' + str(insp_ind), insp['Interval'], formatdata)
                                    worksheet2.write('I' + str(insp_ind), insp['Duedate'], formattime)
                                    insp_ind += 1
    else:
        dataS = getS_risk(idx)
        insp_S = getS_insp(idx)
        ind = 3
        insp_ind = 2
        name = getS_name(idx)
        if dataS is not None:
            for dataF in dataS:
                if dataF is not None:
                    for dataE in dataF:
                        if dataE is not None:
                            for dataC in dataE:
                                if dataC is not None:
                                    worksheet.write('A' + str(ind), (dataC['equipment_name']), formatdata)
                                    worksheet.write('B' + str(ind), (dataC['equipment_desc']), formatdata)
                                    worksheet.write('C' + str(ind), (dataC['equipment_type']), formatdata)
                                    worksheet.write('D' + str(ind), (dataC['component_name']), formatdata)
                                    worksheet.write('O' + str(ind), convertDF(dataC['init_thinning']), formatdata)
                                    worksheet.write('P' + str(ind), convertDF(dataC['init_cracking']), formatdata)
                                    worksheet.write('Q' + str(ind), convertDF(dataC['init_other']), formatdata)
                                    worksheet.write('R' + str(ind), convertDF(dataC['init_pof']), formatdata)
                                    worksheet.write('S' + str(ind), convertDF(dataC['ext_thinning']), formatdata)
                                    worksheet.write('T' + str(ind), convertDF(0), formatdata)
                                    worksheet.write('U' + str(ind), convertDF(0), formatdata)
                                    worksheet.write('V' + str(ind), convertDF(dataC['ext_thinning']), formatdata)
                                    worksheet.write('W' + str(ind), convertDF(dataC['pof_catalog']), formatdata)
                                    worksheet.write('E' + str(ind), dataC['fluid'], formatdata)
                                    worksheet.write('F' + str(ind), dataC['fluid_phase'], formatdata)
                                    worksheet.write('G' + str(ind), 'N/A', formatdata)
                                    worksheet.write('H' + str(ind), convertCA(dataC['flamable']), formatdata)
                                    worksheet.write('I' + str(ind), convertCA(dataC['inj']), formatdata)
                                    worksheet.write('J' + str(ind), convertCA(dataC['business']), formatdata)
                                    worksheet.write('K' + str(ind), convertCA(dataC['env']), formatdata)
                                    worksheet.write('L' + str(ind), 'N/A', formatdata)
                                    worksheet.write('M' + str(ind), convertCA(dataC['consequence']), formatdata)
                                    worksheet.write('X' + str(ind), convertRisk(convertCA(dataC['consequence']), convertDF(dataC['pof_catalog'])),
                                                    formatdata)
                                    worksheet.write('Y' + str(ind),
                                                    convertRisk(convertCA(dataC['consequence']),
                                                                            convertDF(dataC['pof_catalog2'])),
                                                    formatdata)

                                    worksheet1.write('A' + str(ind), dataC['equipment_name'], formatdata)
                                    worksheet1.write('B' + str(ind), dataC['equipment_desc'], formatdata)
                                    worksheet1.write('C' + str(ind), dataC['equipment_type'], formatdata)
                                    worksheet1.write('D' + str(ind), dataC['component_name'], formatdata)
                                    worksheet1.write('O' + str(ind), dataC['init_thinning'], formatdata)
                                    worksheet1.write('P' + str(ind), dataC['init_cracking'], formatdata)
                                    worksheet1.write('Q' + str(ind), dataC['init_other'], formatdata)
                                    worksheet1.write('R' + str(ind), dataC['init_pof'], formatdata)
                                    worksheet1.write('S' + str(ind), dataC['ext_thinning'], formatdata)
                                    worksheet1.write('T' + str(ind), 'N/A', formatdata)
                                    worksheet1.write('U' + str(ind), 'N/A', formatdata)
                                    worksheet1.write('V' + str(ind), dataC['ext_thinning'], formatdata)
                                    worksheet1.write('W' + str(ind), dataC['pof_catalog'], formatdata)
                                    worksheet1.write('E' + str(ind), dataC['fluid'], formatdata)
                                    worksheet1.write('F' + str(ind), dataC['fluid_phase'], formatdata)
                                    worksheet1.write('G' + str(ind), 'N/A', formatdata)
                                    worksheet1.write('H' + str(ind), dataC['flamable'], formatdata)
                                    worksheet1.write('I' + str(ind), dataC['inj'], formatdata)
                                    worksheet1.write('J' + str(ind), dataC['business'], formatdata)
                                    worksheet1.write('K' + str(ind), dataC['env'], formatdata)
                                    worksheet1.write('L' + str(ind), 'N/A', formatdata)
                                    worksheet1.write('M' + str(ind), dataC['consequence'], formatdata)
                                    worksheet1.write('X' + str(ind), dataC['risk'], formatdata)
                                    worksheet1.write('Y' + str(ind), dataC['risk_future'], formatdata)
                                    ind += 1
            worksheet.conditional_format('X3:Y' + str(ind),
                                         {'type': 'cell', 'criteria': '==', 'value': '"High"', 'format': red})
            worksheet.conditional_format('X3:Y' + str(ind),
                                         {'type': 'cell', 'criteria': '==', 'value': '"Medium High"',
                                          'format': orange})
            worksheet.conditional_format('X3:Y' + str(ind),
                                         {'type': 'cell', 'criteria': '==', 'value': '"Medium"', 'format': yellow})
            worksheet.conditional_format('X3:Y' + str(ind),
                                         {'type': 'cell', 'criteria': '==', 'value': '"Low"', 'format': green})
            worksheet.conditional_format('X3:Y' + str(ind),
                                         {'type': 'cell', 'criteria': '==', 'value': '"N/A"', 'format': gray})
        if insp_S is not None:
            for F in insp_S:
                if F is not None:
                    for E in F:
                        if E is not None:
                            for C in E:
                                if C is not None:
                                    for insp in C:
                                        if insp is not None:
                                            worksheet2.write('B' + str(insp_ind), insp['System'], formatdata)
                                            worksheet2.write('A' + str(insp_ind), insp['Equipment'], formatdata)
                                            worksheet2.write('C' + str(insp_ind), insp['Damage'],
                                                             formatdata)
                                            worksheet2.write('D' + str(insp_ind), insp['Method'], formatdata)
                                            worksheet2.data_validation('D' + str(insp_ind),
                                                                       {'validate': 'list',
                                                                        'source': '=Lookup!$A$2:$A$37'})
                                            worksheet2.write('E' + str(insp_ind), insp['Coverage'], formatdata)
                                            worksheet2.write('F' + str(insp_ind), insp['Avaiable'], formatdata)
                                            worksheet2.data_validation('F' + str(insp_ind), {'validate': 'list',
                                                                                             'source': ['online',
                                                                                                        'shutdown']})
                                            worksheet2.write('G' + str(insp_ind), insp['Last'], formattime)
                                            worksheet2.write('H' + str(insp_ind), insp['Interval'], formatdata)
                                            worksheet2.write('I' + str(insp_ind), insp['Duedate'], formattime)
                                            insp_ind += 1

    workbook.close()
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=' + name + '.xlsx'
    return response
def get_inspection_work_planning(idx):
    try:
        data = []
        new = models.RwAssessment.objects.filter(id=idx)
        newPof = models.RwFullPof.objects.filter(id=idx)
        newFcof = models.RwFullFcof.objects.filter(id=idx)
        damage = models.RwDamageMechanism.objects.filter(id_dm = idx)
        if new.count() != 0 and newPof.count() != 0 and newFcof.count() != 0:
            newest = new[0]
            inspec_coverage = models.InspectionCoverage.objects.filter(componentid=newest.componentid_id)

            equip = models.EquipmentMaster.objects.get(equipmentid=newest.equipmentid_id)
            faci = models.Facility.objects.get(facilityid = equip.facilityid_id)
            insp = models.RwDamageMechanism.objects.filter(id_dm=newest.id)

            if insp.count():
                for a in insp:
                    dmitem = models.DMItems.objects.get(dmitemid=a.dmitemid_id)
                    dataGeneral = {}
                    dataGeneral['unit'] = faci.facilityname
                    dataGeneral['equipment_id'] = equip.equipmentnumber
                    dataGeneral['equipment_type'] = models.EquipmentType.objects.get(
                        equipmenttypeid=equip.equipmenttypeid_id).equipmenttypename
                    dataGeneral['damage'] = dmitem.dmdescription
                    dataGeneral['inspec_priority'] = round((insp[0].inspduedate - insp[0].lastinspdate).days / 365, 2)

                    dataGeneral['method'] = ""
                    dataGeneral['extend'] = ""

                    if inspec_coverage.count():
                        inspec_coverage_detail = models.InspectionCoverageDetail.objects.filter(
                            coverageid_id=inspec_coverage[0].id)
                        inspec_tech = models.InspectionTechnique.objects.filter(coverageid_id=inspec_coverage[0].id)
                        for b in inspec_tech:
                            dataGeneral['method'] = dataGeneral['method'] + models.IMItem.objects.get(
                                imitemid=b.imitemid_id).imdescription
                        dataGeneral['extend'] = inspec_coverage_detail[0].inspsummary
                    dataGeneral['avaiable'] = 'online'
                    dataGeneral['Last'] = a.lastinspdate.date()
                    dataGeneral['Duedate'] = a.inspduedate.date()
                    data.append(dataGeneral)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    return data

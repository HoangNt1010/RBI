import os,sys
from operator import eq

import xlrd
import math

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from cloud.process.RBI import fastCalulate as ReCalculate
from xlrd import open_workbook
from django.shortcuts import Http404
from cloud import models
from datetime import datetime
import datetime

def checkEquipmentComponentExist(equipmentNumber,componentNumber):
    try:
        eq = models.EquipmentMaster.objects.get(equipmentnumber=equipmentNumber)
        count = models.ComponentMaster.objects.filter(equipmentid = eq.equipmentid,componentnumber=componentNumber).exists()
        return count
    except Exception as e:
        print(e)
        print("error in checkEquipmentComponentExist")
        return False

def convertInt(floatnumber):
    try:
        return int(floatnumber)
    except:
        return 0

def getDMItemID(damagename):
    try:
        dmitem = models.DMItems.objects.get(dmdescription=damagename)
        return dmitem.dmitemid
    except Exception as e:
        print(e)
        print("exception at getDMItemID")

def xldate_to_datetime(xldatetime):  # something like 43705.6158241088
    try:
        # print(xldatetime)
        # xldatetime1 = str(xldatetime)
        # print(xldatetime1)
        # time = datetime.datetime.strptime(xldatetime1, "%d/%m/%Y").strftime("%Y-%m-%d")
        # my_time = datetime.datetime.min.time()
        # print("ddd")
        # my_datetime = datetime.datetime.combine(time, my_time)
        # print(my_datetime)
        # print(time)
        tempDate = datetime.datetime(1899, 12, 31)

        (days, portion) = math.modf(xldatetime)

        deltaDays = datetime.timedelta(days=days-1)
        # changing the variable name in the edit
        secs = int(24 * 60 * 60 * portion)
        detlaSeconds = datetime.timedelta(seconds=secs)
        TheTime = (tempDate + deltaDays + detlaSeconds)
        timeinsp = TheTime.strftime("%Y-%m-%d %H:%M:%S")
        inspdatetime = datetime.datetime.strptime(timeinsp, "%Y-%m-%d %H:%M:%S")
        return inspdatetime
    except Exception as e:
        print("error in xldate_to_datetime")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(e)


def checkDate(datestring):
    try:
        data = datetime.strptime(datestring, '%m-%d-%y')
        return data
    except:
        return False

def convertDate(dateString):
    try:
        return datetime.strptime(dateString, '%m-%d-%y')
    except:
        return datetime.now().date()

def convertDateInsp(dateString):
    try:
        seconds = (dateString - 25569) * 86400
        return datetime.utcfromtimestamp(seconds)
    except Exception as e:
        print(e)
        print("error in convertDateInsp")
        return datetime.now().date()

def convertTF(data):
    if data == 'TRUE' or data == 'True' or data == 1:
        return 1
    else:
        return 0

def convertFloat(data):
    try:
        return float(data)
    except:
        return 0

# def getCoverageID(planid):
#     return models.InspectionCoverage.objects.get(planid=planid).id
#

method1a = ''
method2a = ''
method3a = ''
def getInspSummary(coverage1, coverage2, coverage3, method1, method2, method3, intrusive):
    try:
        global method1a, method2a, method3a
        if (method1 == 'Crack Detection' or method1 == 'Leak Detection'):
            method1a = 'Aucoustic Emission'
        elif (method1 == 'ACFM' or method1 == 'Low frequency' or method1 == 'Pulsed' or method1 == 'Remote field' or method1 == 'Standard (flat coil)'):
            method1a = 'Eddy Current'
        elif (method1 == 'Magnetic Fluorescent Inspection' or method1 == 'Magnetic Flux Leakage' or method1 == 'Magnetic Particle Inspection'):
            method1a = 'Magnetic'
        elif (method1 == 'Hardness Surveys' or method1 == 'Microstructure Replication'):
            method1a = 'Metallurgical'
        elif (method1 == 'On-line Monitoring'):
            method1a = 'Monitoring'
        elif (method1 == 'Liquid Penetrant Inspection' or method1 == 'Penetrant Leak Detection'):
            method1a = 'Penetrant'
        elif (method1 == 'Compton Scatter' or method1 == 'Gamma Radiography' or method1 == 'Real-time Radiography' or method1 == 'X-Radiography'):
             method1a = 'Radiography'
        elif (method1 == 'Passive Thermography' or method1 == 'Transient Thermography'):
            method1a = 'Thermography'
        elif (method1 == 'Advanced Ultrasonic Backscatter Technique' or method1 == 'Angled Compression Wave' or method1 == 'Angled Shear Wave' or method1 == 'A-scan Thickness Survey' or method1 == 'B-scan' or method1 == 'Chime' or
              method1 == 'C-scan' or method1 == 'Digital Ultrasonic Thickness Gauge' or method1 == 'Internal Rotational Inspection System' or method1 == 'Lorus' or
                method1 == 'Surface Waves' or method1 == 'Teletest' or method1 == 'TOFD'):
              method1a = 'Ultrasonic'
        else:
            method1a = 'Visual'

        method1sum = intrusive + " " + method1a + " " + method1 + "-"+str(coverage1) + "%"

        if (method2 == 'Crack Detection' or method2 == 'Leak Detection'):
            method2a = 'Aucoustic Emission'
        elif (method2 == 'ACFM' or method2 == 'Low frequency' or method2 == 'Pulsed' or method2 == 'Remote field' or method2 == 'Standard (flat coil)'):
            method2a = 'Eddy Current'
        elif (method2 == 'Magnetic Fluorescent Inspection' or method2 == 'Magnetic Flux Leakage' or method2 == 'Magnetic Particle Inspection'):
            method2a = 'Magnetic'
        elif (method2 == 'Hardness Surveys' or method2 == 'Microstructure Replication'):
            method2a = 'Metallurgical'
        elif (method2 == 'On-line Monitoring'):
            method2a = 'Monitoring'
        elif (method2 == 'Liquid Penetrant Inspection' or method2 == 'Penetrant Leak Detection'):
            method2a = 'Penetrant'
        elif (method2 == 'Compton Scatter' or method2 == 'Gamma Radiography' or method2 == 'Real-time Radiography' or method2 == 'X-Radiography'):
             method2a = 'Radiography'
        elif (method2 == 'Passive Thermography' or method2 == 'Transient Thermography'):
            method2a = 'Thermography'
        elif (method2 == 'Advanced Ultrasonic Backscatter Technique' or method2 == 'Angled Compression Wave' or method2 == 'Angled Shear Wave' or method2 == 'A-scan Thickness Survey' or method2 == 'B-scan' or method2 == 'Chime' or
              method2 == 'C-scan' or method2 == 'Digital Ultrasonic Thickness Gauge' or method2 == 'Internal Rotational Inspection System' or method2 == 'Lorus' or
                method2 == 'Surface Waves' or method2 == 'Teletest' or method2 == 'TOFD'):
              method2a = 'Ultrasonic'
        else:
            method2a = 'Visual'
        method2sum = intrusive + " " + method2a + " " + method2 + "-" + str(coverage2) + "%"

        if (method3 == 'Crack Detection' or method3 == 'Leak Detection'):
            method3a = 'Aucoustic Emission'
        elif (
                            method3 == 'ACFM' or method3 == 'Low frequency' or method3 == 'Pulsed' or method3 == 'Remote field' or method3 == 'Standard (flat coil)'):
            method3a = 'Eddy Current'
        elif (
                    method3 == 'Magnetic Fluorescent Inspection' or method3 == 'Magnetic Flux Leakage' or method3 == 'Magnetic Particle Inspection'):
            method3a = 'Magnetic'
        elif (method3 == 'Hardness Surveys' or method3 == 'Microstructure Replication'):
            method3a = 'Metallurgical'
        elif (method3 == 'On-line Monitoring'):
            method3a = 'Monitoring'
        elif (method3 == 'Liquid Penetrant Inspection' or method3 == 'Penetrant Leak Detection'):
            method3a = 'Penetrant'
        elif (
                        method3 == 'Compton Scatter' or method3 == 'Gamma Radiography' or method3 == 'Real-time Radiography' or method3 == 'X-Radiography'):
            method3a = 'Radiography'
        elif (method3 == 'Passive Thermography' or method3 == 'Transient Thermography'):
            method3a = 'Thermography'
        elif (
                                                            method3 == 'Advanced Ultrasonic Backscatter Technique' or method3 == 'Angled Compression Wave' or method3 == 'Angled Shear Wave' or method3 == 'A-scan Thickness Survey' or method3 == 'B-scan' or method3 == 'Chime' or
                                        method3 == 'C-scan' or method3 == 'Digital Ultrasonic Thickness Gauge' or method3 == 'Internal Rotational Inspection System' or method3 == 'Lorus' or
                        method3 == 'Surface Waves' or method3 == 'Teletest' or method3 == 'TOFD'):
            method3a = 'Ultrasonic'
        else:
            method3a = 'Visual'
        method3sum = intrusive + " " + method3a + " " + method3 + "-" + str(coverage3) + "%"
        return method1sum + "\n" + "AND" +" "+ method2sum + "\n" + "AND" +" "+ method3sum
    except Exception as e:
        print(e)
        print("exception at getSum")

def importInspectionPlan(filename):
    try:
        print("vào hàm")
        excel = open_workbook(filename)
        ws = excel.sheet_by_name('Inspections')
        rowdata = ws.nrows
        coldata = ws.ncols
        if coldata == 13:
            for row in range(1,rowdata):
                if ws.cell(row,1).value and ws.cell(row,2).value and ws.cell(row,3).value and ws.cell(row,11).value and ws.cell(row,12).value:
                    if checkEquipmentComponentExist(convertInt(ws.cell_value(row,1)),convertInt(ws.cell_value(row,2))):
                        his = models.RwInspectionDetail(id = convertInt(ws.cell(row,0).value), inspectiondate = xldate_to_datetime(ws.cell(row,11).value), equipmentid = getEquipmentID(convertInt(ws.cell_value(row,1))),
                                                             componentid = getComponentID(convertInt(ws.cell_value(row,2))), effcode = ws.cell(row,12).value, inspsum = getInspSummary(ws.cell(row,5).value,ws.cell(row,7).value,ws.cell(row,9).value,ws.cell(row,4).value,ws.cell(row,6).value,ws.cell(row,8).value,ws.cell(row,10).value),
                                                             dmitemid=getDMItemID(ws.cell_value(row,3)))
                        his.save()
        print("lưu hàm")
    except Exception as e:
        print(" exception at inspection plan")
        print(e)
        raise Http404

# --------------COUNT SHEET COL-------------
#  Worksheet | PlantProcess | StorageTank
# 	0			32				36
# 	1			32				24
# 	2			18				18
# 	3			22				25
# 	4			22				18
# 	5			15				15
# ------------------------------------------

# kiem tra dieu kien thoa man va dieu kien ton tai cua du lieu

def checkFacilityAvaiable(site, facility):
    try:
        site = models.Sites.objects.get(sitename= site)
        if models.Facility.objects.filter(facilityname= facility, siteid=site.siteid).exists():
            return True
        else:
            return False
    except:
        return False

def checkEquipmentAvaiable(site,facility,equipmentnumber, equipmentName):
    try:
        site = models.Sites.objects.get(sitename= site)
        faci = models.Facility.objects.get(facilityname= facility)
        countE = models.EquipmentMaster.objects.filter(equipmentnumber= equipmentnumber ,siteid= site.siteid, facilityid=faci.facilityid).exists()
        avaiE = models.EquipmentMaster.objects.filter(equipmentnumber=equipmentnumber).exists()
        if ( countE or not avaiE ) and equipmentName :
            return True
        else:
            return False
    except:
        return False

def checkComponentAvaiable(equipmentnumber, componentnumber):
    try:
        equ = models.EquipmentMaster.objects.get(equipmentnumber= equipmentnumber)
        countComp = models.ComponentMaster.objects.filter(componentnumber= componentnumber, equipmentid= equ.equipmentid).exists()
        avaiComp = models.ComponentMaster.objects.filter(componentnumber= componentnumber).exists()
        if countComp or not avaiComp:
            return True
        else:
            return False
    except:
        return False

def checkFacilityExist(facilityname):
    existF = models.Facility.objects.filter(facilityname= facilityname).exists()
    return existF

def checkEquipmentExist(equipmentNumber):
    existE = models.EquipmentMaster.objects.filter(equipmentnumber= equipmentNumber).exists()
    return existE

def checkComponentExist(componentNumber):
    existC = models.ComponentMaster.objects.filter(componentnumber= componentNumber).exists()
    return existC

def checkDesigncodeAvaiable(designcode, sitename):
    try:
        site = models.Sites.objects.get(sitename= sitename)
        avaiDesign = models.DesignCode.objects.filter(designcode= designcode, siteid= site.siteid).exists()
        design = models.DesignCode.objects.filter(designcode= designcode).exists()
        if avaiDesign or not design:
            return True
        else:
            return False
    except:
        return False

def checkDesigncodeExist(designcode):
    existDesign = models.DesignCode.objects.filter(designcode= designcode).exists()
    return existDesign

def checkManufactureExist(manufacturename):
    existManu = models.Manufacturer.objects.filter(manufacturername= manufacturename).exists()
    return existManu

def checkManufactureAvaiable(manufacture, sitename):
    try:
        site = models.Sites.objects.get(sitename= sitename)
        avaiManufacture = models.Manufacturer.objects.filter(manufacturername= manufacture, siteid= site.siteid).exists()
        existManu = models.Manufacturer.objects.filter(manufacturername= manufacture).exists()
        if avaiManufacture or not existManu:
            return True
        else:
            return False
    except:
        return False

def checkSiteAvaiable(sitename):
    existSite = models.Sites.objects.filter(sitename= sitename).exists()
    return existSite

def getSiteID(sitename):
    return models.Sites.objects.get(sitename= sitename).siteid

def getFacilityID(facilityname):
    return models.Facility.objects.get(facilityname=facilityname).facilityid

def getEquipmentTypeID(equipmentTypeName):
    equipmentType = models.EquipmentType.objects.get(equipmenttypename= equipmentTypeName)
    return equipmentType.equipmenttypeid

def getComponentTypeID(componentTypeName):
    componentType = models.ComponentType.objects.get(componenttypename= componentTypeName)
    return componentType.componenttypeid

def getApiComponentTypeID(apicomponentType):
    api = models.ApiComponentType.objects.get(apicomponenttypename= apicomponentType)
    return api.apicomponenttypeid

def getDesigncodeID(designcode):
    return models.DesignCode.objects.get(designcode=designcode).designcodeid

def getManufactureID(manufacture):
    return models.Manufacturer.objects.get(manufacturername= manufacture).manufacturerid

def getEquipmentID(equipmentNumber):
    return models.EquipmentMaster.objects.get(equipmentnumber= equipmentNumber).equipmentid

def getComponentID(componentNumber):
    return models.ComponentMaster.objects.get(componentnumber=componentNumber).componentid

def getApiTankFluid(fluidname):
    if fluidname == "Gasoline":
        return "C6-C8"
    elif fluidname == "Light Diesel Oil":
        return "C9-C12"
    elif fluidname == "Heavy Diesel Oil":
        return "C13-C16"
    elif fluidname == "Fuel Oil" or fluidname == "Crude Oil":
        return "C17-C25"
    else:
        return "C25+"


#RBI Data Collection


#sheet 0
def saveSheetEquip(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['5'] and a['6'] and a['7']:
                    if checkSiteAvaiable(a['4']):
                        if checkFacilityAvaiable(a['4'], a['5']):
                            print(a['5'])
                            if checkFacilityExist(a['5']):
                                fc = models.Facility.objects.get(facilityname=a['5'])
                                try:
                                    managefactor = float(a['14'])
                                except:
                                    managefactor = 0.1
                                fc.managementfactor = managefactor
                                fc.save()

                        if checkDesigncodeAvaiable(a['3'], a['4']):
                            if not checkDesigncodeExist(a['3']):
                                ds = models.DesignCode(designcode=a['3'], designcodeapp='None',
                                                       siteid_id=getSiteID(a['4']))
                                ds.save()

                        if checkManufactureAvaiable(a['6'], a['4']):
                            if not checkManufactureExist(a['6']):
                                mn = models.Manufacturer(manufacturername=a['6'],
                                                         siteid_id=getSiteID(a['4']))
                                mn.save()

                        if checkEquipmentAvaiable(a['4'], a['5'],a['0'] , a['2']):
                            if checkEquipmentExist(a['0']):
                                eq = models.EquipmentMaster.objects.get(equipmentnumber=a['0'])
                                eq.equipmenttypeid_id = getEquipmentTypeID(a['1'])
                                eq.equipmentname = a['2']
                                eq.commissiondate = a['7']
                                eq.designcodeid_id = getDesigncodeID(a['3'])
                                eq.siteid_id = getSiteID(a['4'])
                                eq.facilityid_id = getFacilityID(a['5'])
                                eq.manufacturerid_id = getManufactureID(a['6'])
                                eq.pfdno = a['8']
                                eq.processdescription = a['9']
                                eq.equipmentdesc = a['10']
                                eq.save()
                                print("save1")
                            else:
                                eq = models.EquipmentMaster(equipmentnumber= a['0'], equipmenttypeid_id= getEquipmentTypeID(a['1']),
                                                            equipmentname= a['2'], commissiondate = a['7'],
                                                            designcodeid_id=getDesigncodeID(a['3']), siteid_id = getSiteID(a['4']),
                                                            facilityid_id=getFacilityID(a['5']), manufacturerid_id = getManufactureID(a['6']),
                                                            pfdno=a['8'], processdescription = a['9'], equipmentdesc = a['10'])
                                eq.save()
                                print("save2")
            else:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['5'] and a['6'] and a['7']:
                    if checkSiteAvaiable(a['4']):
                        if checkFacilityAvaiable(a['4'], a['5']):
                            if checkFacilityExist(a['5']):
                                fc = models.Facility.objects.get(facilityname=a['5'])
                                try:
                                    managefactor = float(a['14'])
                                except:
                                    managefactor = 0.1
                                fc.managementfactor = managefactor
                                fc.save()
                        if checkDesigncodeAvaiable(a['3'], a['4']):
                            if not checkDesigncodeExist(a['3']):
                                ds = models.DesignCode(designcode=a['3'], designcodeapp='None',
                                                       siteid_id=getSiteID(a['4']))
                                ds.save()
                        if checkManufactureAvaiable(a['6'], a['4']):
                            if not checkManufactureExist(a['6']):
                                mn = models.Manufacturer(manufacturername=a['6'],
                                                         siteid_id=getSiteID(a['4']))
                                mn.save()
                        if checkEquipmentAvaiable(a['4'], a['5'], a['0'],a['2']):
                            if checkEquipmentExist(a['0']):
                                eq = models.EquipmentMaster.objects.get(equipmentnumber=a['0'])
                                eq.equipmenttypeid_id = getEquipmentTypeID(a['1'])
                                eq.equipmentname = a['2']
                                eq.commissiondate = a['7']
                                eq.designcodeid_id = getDesigncodeID(a['3'])
                                eq.siteid_id = getSiteID(a['4'])
                                eq.facilityid_id = getFacilityID(a['5'])
                                eq.manufacturerid_id = getManufactureID(a['6'])
                                eq.pfdno = a['8']
                                eq.processdescription = a['9']
                                eq.equipmentdesc = a['10']
                                eq.save()
                            else:
                                eq = models.EquipmentMaster(equipmentnumber=a['0'],
                                                            equipmenttypeid_id=getEquipmentTypeID(
                                                                a['1']),
                                                            equipmentname=a['2'],
                                                            commissiondate=a['7'],
                                                            designcodeid_id=getDesigncodeID(a['3']),
                                                            siteid_id=getSiteID(a['4']),
                                                            facilityid_id=getFacilityID(a['5']),
                                                            manufacturerid_id=getManufactureID(a['6']),
                                                            pfdno=a['8'],
                                                            processdescription=a['9'],
                                                            equipmentdesc=a['10'])
                                eq.save()
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print("error at saveSheetEquip")
def processEquipmentMaster(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 30:
            for row in range(1, nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,3).value and ws.cell(
                        row, 4).value and ws.cell(row, 5).value and ws.cell(row, 6).value and ws.cell(row, 7).value:
                    if checkSiteAvaiable(ws.cell(row, 4).value):
                        if checkFacilityAvaiable(ws.cell(row, 4).value, ws.cell(row, 5).value):
                            if checkFacilityExist(ws.cell(row, 5).value):
                                fc = models.Facility.objects.get(facilityname=ws.cell(row, 5).value)
                                try:
                                    managefactor = float(ws.cell(row, 14).value)
                                except:
                                    managefactor = 0.1
                                fc.managementfactor = managefactor
                                fc.save()
                        if checkDesigncodeAvaiable(ws.cell(row, 3).value, ws.cell(row, 4).value):
                            if not checkDesigncodeExist(ws.cell(row, 3).value):
                                ds = models.DesignCode(designcode=ws.cell(row, 3).value, designcodeapp='None',
                                                       siteid_id=getSiteID(ws.cell(row, 4).value))
                                ds.save()
                        if checkManufactureAvaiable(ws.cell(row, 6).value, ws.cell(row, 4).value):
                            if not checkManufactureExist(ws.cell(row, 6).value):
                                mn = models.Manufacturer(manufacturername=ws.cell(row, 6).value,
                                                         siteid_id=getSiteID(ws.cell(row, 4).value))
                                mn.save()
                        if checkEquipmentAvaiable(ws.cell(row, 4).value, ws.cell(row, 5).value,ws.cell(row,0).value, ws.cell(row, 2).value):
                            if checkEquipmentExist(ws.cell(row, 0).value):
                                eq = models.EquipmentMaster.objects.get(equipmentnumber=ws.cell(row, 0).value)
                                eq.equipmenttypeid_id = getEquipmentTypeID(ws.cell(row, 1).value)
                                eq.equipmentname = ws.cell(row, 2).value
                                eq.commissiondate = xldate_to_datetime(ws.cell(row, 7).value)
                                eq.designcodeid_id = getDesigncodeID(ws.cell(row, 3).value)
                                eq.siteid_id = getSiteID(ws.cell(row, 4).value)
                                eq.facilityid_id = getFacilityID(ws.cell(row, 5).value)
                                eq.manufacturerid_id = getManufactureID(ws.cell(row, 6).value)
                                eq.pfdno = ws.cell(row, 8).value
                                eq.processdescription = ws.cell(row, 9).value
                                eq.equipmentdesc = ws.cell(row, 10).value
                                eq.save()
                            else:
                                eq = models.EquipmentMaster(equipmentnumber= ws.cell(row,0).value, equipmenttypeid_id= getEquipmentTypeID(ws.cell(row, 1).value),
                                                            equipmentname= ws.cell(row,2).value, commissiondate = xldate_to_datetime(ws.cell(row, 7).value),
                                                            designcodeid_id=getDesigncodeID(ws.cell(row, 3).value), siteid_id = getSiteID(ws.cell(row, 4).value),
                                                            facilityid_id=getFacilityID(ws.cell(row, 5).value), manufacturerid_id = getManufactureID(ws.cell(row, 6).value),
                                                            pfdno=ws.cell(row, 8).value, processdescription = ws.cell(row, 9).value, equipmentdesc = ws.cell(row, 10).value)
                                eq.save()
        elif ncol == 34:
            for row in range(1, nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row, 3).value and ws.cell(
                        row, 4).value and ws.cell(row, 5).value and ws.cell(row, 6).value and ws.cell(row, 7).value:
                    if checkSiteAvaiable(ws.cell(row, 4).value):
                        if checkFacilityAvaiable(ws.cell(row, 4).value, ws.cell(row, 5).value):
                            if checkFacilityExist(ws.cell(row, 5).value):
                                fc = models.Facility.objects.get(facilityname=ws.cell(row, 5).value)
                                try:
                                    managefactor = float(ws.cell(row, 14).value)
                                except:
                                    managefactor = 0.1
                                fc.managementfactor = managefactor
                                fc.save()

                        if checkDesigncodeAvaiable(ws.cell(row, 3).value, ws.cell(row, 4).value):
                            if not checkDesigncodeExist(ws.cell(row, 3).value):
                                ds = models.DesignCode(designcode=ws.cell(row, 3).value, designcodeapp='None',
                                                       siteid_id=getSiteID(ws.cell(row, 4).value))
                                ds.save()

                        if checkManufactureAvaiable(ws.cell(row, 6).value, ws.cell(row, 4).value):
                            if not checkManufactureExist(ws.cell(row, 6).value):
                                mn = models.Manufacturer(manufacturername=ws.cell(row, 6).value,
                                                         siteid_id=getSiteID(ws.cell(row, 4).value))
                                mn.save()

                        if checkEquipmentAvaiable(ws.cell(row, 4).value, ws.cell(row, 5).value,ws.cell(row,0).value , ws.cell(row, 2).value):
                            if checkEquipmentExist(ws.cell(row, 0).value):
                                eq = models.EquipmentMaster.objects.get(equipmentnumber=ws.cell(row, 0).value)
                                eq.equipmenttypeid_id = getEquipmentTypeID(ws.cell(row, 1).value)
                                eq.equipmentname = ws.cell(row, 2).value
                                eq.commissiondate = xldate_to_datetime(ws.cell(row, 7).value)
                                eq.designcodeid_id = getDesigncodeID(ws.cell(row, 3).value)
                                eq.siteid_id = getSiteID(ws.cell(row, 4).value)
                                eq.facilityid_id = getFacilityID(ws.cell(row, 5).value)
                                eq.manufacturerid_id = getManufactureID(ws.cell(row, 6).value)
                                eq.pfdno = ws.cell(row, 8).value
                                eq.processdescription = ws.cell(row, 9).value
                                eq.equipmentdesc = ws.cell(row, 10).value
                                eq.save()
                            else:
                                eq = models.EquipmentMaster(equipmentnumber= ws.cell(row,0).value, equipmenttypeid_id= getEquipmentTypeID(ws.cell(row, 1).value),
                                                            equipmentname= ws.cell(row,2).value, commissiondate = xldate_to_datetime(ws.cell(row, 7).value),
                                                            designcodeid_id=getDesigncodeID(ws.cell(row, 3).value), siteid_id = getSiteID(ws.cell(row, 4).value),
                                                            facilityid_id=getFacilityID(ws.cell(row, 5).value), manufacturerid_id = getManufactureID(ws.cell(row, 6).value),
                                                            pfdno=ws.cell(row, 8).value, processdescription = ws.cell(row, 9).value, equipmentdesc = ws.cell(row, 10).value)
                                eq.save()
        # neu k phai format tren thi bo qua. k thuc hien
    except Exception as e:
        print('Exception at Equipment Master Excel')
        print(e)

#sheet 1
def saveSheetComponent(data):
    try:
        for a in data:
            if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['7']:
                if checkComponentAvaiable(a['0'], a['1']):
                    if checkComponentExist(a['1']):
                        comp = models.ComponentMaster.objects.get(componentnumber=a['1'])
                        comp.componenttypeid_id = getComponentTypeID(a['2'])
                        comp.componentname = a['4']
                        comp.componentdesc = a['6']
                        comp.isequipmentlinked = a['5']
                        comp.apicomponenttypeid = getApiComponentTypeID(a['3'])
                        comp.save()
                        print("saveComponent1")
                    else:
                        comp = models.ComponentMaster(componentnumber=a['1'],
                                                      componenttypeid_id=getComponentTypeID(a['2']),
                                                      componentname=a['4'],
                                                      componentdesc=a['6'],
                                                      equipmentid_id=getEquipmentID(a['0']),
                                                      isequipmentlinked=a['5'],
                                                      apicomponenttypeid=getApiComponentTypeID(a['3']))
                        comp.save()
                        print("saveComponent2")
    except Exception as e:
        print(e)
        print("error at saveSheetComponent")
def processComponentMaster(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 33 or ncol == 44:
            for row in range(1,nrow):
                if ws.cell(row,0).value and ws.cell(row,1).value and ws.cell(row,2).value and ws.cell(row,3).value and ws.cell(row,4).value and ws.cell(row,7).value:
                    if checkComponentAvaiable(ws.cell(row,0).value, ws.cell(row,1).value):
                        if checkComponentExist(ws.cell(row,1).value):
                            comp = models.ComponentMaster.objects.get(componentnumber= ws.cell(row,1).value)
                            comp.componenttypeid_id = getComponentTypeID(ws.cell(row,2).value)
                            comp.componentname = ws.cell(row,4).value
                            comp.componentdesc = ws.cell(row,6).value
                            comp.isequipmentlinked = convertTF(ws.cell(row,5).value)
                            comp.apicomponenttypeid = getApiComponentTypeID(ws.cell(row,3).value)
                            comp.save()
                        else:
                            comp = models.ComponentMaster(componentnumber= ws.cell(row,1).value, componenttypeid_id= getComponentTypeID(ws.cell(row,2).value),
                                                          componentname= ws.cell(row,4).value, componentdesc= ws.cell(row,6).value,equipmentid_id = getEquipmentID(ws.cell(row,0).value),
                                                          isequipmentlinked=convertTF(ws.cell(row,5).value), apicomponenttypeid = getApiComponentTypeID(ws.cell(row,3).value))
                            comp.save()
    except Exception as e:
        print("Exception at Component Master Excel")
        print(e)

listProposal = []
listProposalData=[]
#sheet 1
def saveSheetAssessment(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['7']:
                    if checkComponentAvaiable(a['0'],a['1']):
                        rwAss = models.RwAssessment(equipmentid_id=getEquipmentID(a['0']),
                                                    componentid_id=getComponentID(a['1']),
                                                    assessmentdate=a['7'],commisstiondate=datetime.datetime.now(),
                                                    riskanalysisperiod=36,
                                                    isequipmentlinked=a['5'],
                                                    proposalname="New Excel Proposal " + str(
                                                        datetime.datetime.now().strftime('%m-%d-%y')))
                        rwAss.save()
                        # Luu lai cac bang trung gian
                        rwEquip = models.RwEquipment(id= rwAss, commissiondate= datetime.datetime.now())
                        # rwEquip = models.RwEquipment(id=rwAss)  # Cương Sửa
                        rwEquip.save()
                        rwComp = models.RwComponent(id=rwAss)
                        rwComp.save()
                        rwExco = models.RwExtcorTemperature(id=rwAss)
                        rwExco.save()
                        rwStream = models.RwStream(id=rwAss)
                        rwStream.save()
                        rwMater = models.RwMaterial(id=rwAss)
                        rwMater.save()
                        print("test6")
                        rwCoat = models.RwCoating(id= rwAss, externalcoatingdate= datetime.datetime.now())
                        # rwCoat = models.RwCoating(id=rwAss)  # Cương Sửa
                        rwCoat.save()

                        rwInputTank = models.RwInputCaTank(id= rwAss)
                        rwInputTank.save()
                        listProposalData.append(rwAss)
                        print("save Assessment")
            else:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['7']:
                    if checkComponentAvaiable(a['0'],a['1']):
                        rwAss = models.RwAssessment(equipmentid_id=getEquipmentID(a['0']),
                                                    componentid_id=getComponentID(a['1']),
                                                    assessmentdate=a['7'],commisstiondate=datetime.datetime.now(),
                                                    riskanalysisperiod=36,
                                                    isequipmentlinked=convertTF(a['5']),
                                                    proposalname="New Excel Proposal " + str(
                                                        datetime.datetime.now().strftime('%m-%d-%y')))
                        rwAss.save()
                        # Luu lai cac bang trung gian
                        rwEquip = models.RwEquipment(id=rwAss, commissiondate=datetime.datetime.now())
                        # rwEquip = models.RwEquipment(id= rwAss) #Cương Sửa
                        rwEquip.save()
                        rwComp = models.RwComponent(id=rwAss)
                        rwComp.save()
                        rwExco = models.RwExtcorTemperature(id=rwAss)
                        rwExco.save()

                        rwStream = models.RwStream(id=rwAss)
                        rwStream.save()

                        rwMater = models.RwMaterial(id=rwAss)
                        rwMater.save()

                        rwCoat = models.RwCoating(id=rwAss, externalcoatingdate=datetime.datetime.now())
                        # rwCoat = models.RwCoating(id= rwAss)#Cương Sửa
                        rwCoat.save()
                        rwInputCa = models.RwInputCaLevel1(id=rwAss)
                        rwInputCa.save()
                        listProposalData.append(rwAss)
                        print("save Assessment")
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print("error at saveSheetAssessment")
def processAssessment(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 44:
            for row in range(1,nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,
                                                                                                         3).value and ws.cell(
                    row, 4).value and ws.cell(row, 7).value:
                    if checkComponentAvaiable(ws.cell(row, 0).value, ws.cell(row, 1).value):
                        rwAss = models.RwAssessment(equipmentid_id= getEquipmentID(ws.cell(row,0).value), componentid_id= getComponentID(ws.cell(row,1).value),
                                                    assessmentdate= xldate_to_datetime(ws.cell(row,7).value), riskanalysisperiod= 36,
                                                    isequipmentlinked= convertTF(ws.cell(row,5).value), proposalname= "New Excel Proposal " + str(datetime.datetime.now().strftime('%m-%d-%y')))
                        rwAss.save()

                        #Luu lai cac bang trung gian
                        rwEquip = models.RwEquipment(id= rwAss, commissiondate= datetime.datetime.now())
                        # rwEquip = models.RwEquipment(id= rwAss) #Cương Sửa
                        rwEquip.save()

                        rwComp = models.RwComponent(id = rwAss)
                        rwComp.save()

                        rwExco = models.RwExtcorTemperature(id = rwAss)
                        rwExco.save()

                        rwStream = models.RwStream(id= rwAss)
                        rwStream.save()

                        rwMater = models.RwMaterial(id= rwAss)
                        rwMater.save()

                        rwCoat = models.RwCoating(id= rwAss, externalcoatingdate= datetime.datetime.now())
                        # rwCoat = models.RwCoating(id= rwAss)#Cương Sửa
                        rwCoat.save()

                        rwInputCa = models.RwInputCaLevel1(id = rwAss)
                        rwInputCa.save()
                        listProposal.append(rwAss)
        elif ncol == 33:
            for row in range(1, nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,
                                                                                                         3).value and ws.cell(
                    row, 4).value and ws.cell(row, 7).value:
                    if checkComponentAvaiable(ws.cell(row, 0).value, ws.cell(row, 1).value):
                        rwAss = models.RwAssessment(equipmentid_id=getEquipmentID(ws.cell(row, 0).value),
                                                    componentid_id=getComponentID(ws.cell(row, 1).value),
                                                    assessmentdate=xldate_to_datetime(ws.cell(row, 7).value),
                                                    riskanalysisperiod=36,
                                                    isequipmentlinked=convertTF(ws.cell(row, 5).value),
                                                    proposalname="New Excel Proposal " + str(
                                                        datetime.datetime.now().strftime('%m-%d-%y')))
                        rwAss.save()

                        # Luu lai cac bang trung gian
                        rwEquip = models.RwEquipment(id= rwAss, commissiondate= datetime.datetime.now())
                        # rwEquip = models.RwEquipment(id=rwAss)  # Cương Sửa
                        rwEquip.save()

                        rwComp = models.RwComponent(id=rwAss)
                        rwComp.save()

                        rwExco = models.RwExtcorTemperature(id=rwAss)
                        rwExco.save()

                        rwStream = models.RwStream(id=rwAss)
                        rwStream.save()

                        rwMater = models.RwMaterial(id=rwAss)
                        rwMater.save()

                        rwCoat = models.RwCoating(id= rwAss, externalcoatingdate= datetime.datetime.now())
                        # rwCoat = models.RwCoating(id=rwAss)  # Cương Sửa
                        rwCoat.save()

                        rwInputTank = models.RwInputCaTank(id= rwAss)
                        rwInputTank.save()
                        listProposal.append(rwAss)

    except Exception as e:
        print("Exception at Assessment")
        print(e)

#sheet 0
def saveSheetRwEquipment(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['5'] and a['6'] and a['7']:
                    if checkEquipmentAvaiable(a['4'], a['5'], a['0'],a['2']):
                        for b in listProposalData:
                            if b.equipmentid_id == getEquipmentID(a['0']):
                                rwEq = models.RwEquipment.objects.get(id=b.id)
                                rwInputCaTank = models.RwInputCaTank.objects.get(id=b.id)
                                rwEq.commissiondate = a['7']
                                rwEq.adminupsetmanagement = a['15']

                                # rwEq.cyclicoperation = convertTF(ws.cell(row,12).value)
                                rwEq.downtimeprotectionused = a['23']
                                rwEq.steamoutwaterflush = a['24']
                                rwEq.heattraced = a['25']
                                rwEq.pwht = a['11']
                                rwEq.interfacesoilwater = a['21']
                                rwEq.pressurisationcontrolled = a['29']
                                rwEq.minreqtemperaturepressurisation = convertFloat(a['30'])
                                # rwEq.yearlowestexptemp = convertTF(ws.cell(row,20).value)
                                rwEq.materialexposedtoclext = a['20']
                                rwEq.lineronlinemonitoring = a['16']
                                rwEq.presencesulphideso2 = convertTF(a['26'])
                                rwEq.presencesulphideso2shutdown = convertTF(a['27'])
                                if a['22']:
                                    rwEq.externalenvironment = a['22']
                                if a['28']:
                                    rwEq.thermalhistory = a['28']
                                if a['12']:
                                    rwEq.onlinemonitoring = a['12']
                                rwEq.volume = convertFloat(a['13'])
                                try:
                                    rwEq.managementfactor = float(a['14'])
                                except:
                                    rwEq.managementfactor = 0.1
                                if a['31']:
                                    rwEq.typeofsoil = a['31']
                                    rwInputCaTank.soil_type = a['31']
                                rwEq.distancetogroundwater = convertFloat(a['33'])
                                if a['32']:
                                    rwEq.environmentsensitivity = a['32']
                                    rwInputCaTank.environ_sensitivity = a['32']
                                if a['17']:
                                    rwEq.adjustmentsettle = a['17']
                                rwEq.componentiswelded = convertTF(a['18'])
                                rwEq.tankismaintained = convertTF(a['19'])
                                rwInputCaTank.sw = convertFloat(a['29'])
                                rwEq.save()
                                rwInputCaTank.save()
                                print("save RwEquipment")
            else:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['5'] and a['6'] and a['7']:
                    if checkEquipmentAvaiable(a['4'], a['5'], a['0'],a['2']):
                        for b in listProposalData:
                            if b.equipmentid_id == getEquipmentID(a['0']):
                                rwEq = models.RwEquipment.objects.get(id=b.id)
                                rwEq.commissiondate = a['7']
                                rwEq.adminupsetmanagement = a['15']
                                rwEq.containsdeadlegs = a['28']
                                # rwEq.cyclicoperation= convertTF(ws.cell(row,14).value)
                                rwEq.highlydeadleginsp = a['29']
                                rwEq.downtimeprotectionused = a['20']
                                if a['19']:
                                    rwEq.externalenvironment = a['19']
                                rwEq.heattraced = a['22']
                                rwEq.interfacesoilwater = a['18']
                                rwEq.lineronlinemonitoring = a['16']
                                rwEq.materialexposedtoclext = a['17']
                                rwEq.minreqtemperaturepressurisation = convertFloat(a['27'])
                                if a['12']:
                                    rwEq.onlinemonitoring = a['12']
                                rwEq.presencesulphideso2 = a['23']
                                rwEq.presencesulphideso2shutdown = a['24']
                                rwEq.pressurisationcontrolled = a['26']
                                rwEq.pwht = a['11']
                                rwEq.steamoutwaterflush = a['21']
                                try:
                                    rwEq.managementfactor = float(a['14'])
                                except:
                                    rwEq.managementfactor = 0.1
                                if a['25']:
                                    rwEq.thermalhistory = a['25']
                                # rwEq.yearlowestexptemp = convertTF(ws.cell(row,22).value)
                                rwEq.volume = convertFloat(a['13'])
                                rwEq.save()
                                print("save RwEquipment")
    except Exception as e:
        print(e)
        print("error at saveSheetRwEquipment")
def processRwEquipment(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 30: ## process plan
            for row in range(1,nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,
                                                                                                         3).value and ws.cell(
                    row, 4).value and ws.cell(row, 5).value and ws.cell(row, 6).value and ws.cell(row, 7).value:
                    if checkEquipmentAvaiable(ws.cell(row, 4).value, ws.cell(row, 5).value,ws.cell(row,0).value, ws.cell(row, 2).value):
                        for a in listProposal:
                            if a.equipmentid_id == getEquipmentID(ws.cell(row,0).value):
                                rwEq = models.RwEquipment.objects.get(id=a.id)
                                rwEq.commissiondate = xldate_to_datetime(ws.cell(row,7).value)
                                rwEq.adminupsetmanagement = convertTF(ws.cell(row,15).value)
                                rwEq.containsdeadlegs= convertTF(ws.cell(row,28).value)
                                # rwEq.cyclicoperation= convertTF(ws.cell(row,14).value)
                                rwEq.highlydeadleginsp= convertTF(ws.cell(row,29).value)
                                rwEq.downtimeprotectionused= convertTF(ws.cell(row,20).value)
                                if ws.cell(row,19).value:
                                    rwEq.externalenvironment = ws.cell(row,19).value
                                rwEq.heattraced = convertTF(ws.cell(row,22).value)
                                rwEq.interfacesoilwater = convertTF(ws.cell(row,18).value)
                                rwEq.lineronlinemonitoring = convertTF(ws.cell(row,16).value)
                                rwEq.materialexposedtoclext = convertTF(ws.cell(row,17).value)
                                rwEq.minreqtemperaturepressurisation= convertFloat(ws.cell(row,27).value)
                                if ws.cell(row,12).value:
                                    rwEq.onlinemonitoring = ws.cell(row,12).value
                                rwEq.presencesulphideso2 = convertTF(ws.cell(row,23).value)
                                rwEq.presencesulphideso2shutdown = convertTF(ws.cell(row,24).value)
                                rwEq.pressurisationcontrolled = convertTF(ws.cell(row,26).value)
                                rwEq.pwht = convertTF(ws.cell(row,11).value)
                                rwEq.steamoutwaterflush = convertTF(ws.cell(row,21).value)
                                try:
                                    rwEq.managementfactor = float(ws.cell(row,14).value)
                                except:
                                    rwEq.managementfactor = 0.1
                                if ws.cell(row,25).value:
                                    rwEq.thermalhistory = ws.cell(row,25).value
                                # rwEq.yearlowestexptemp = convertTF(ws.cell(row,22).value)
                                rwEq.volume = convertFloat(ws.cell(row, 13).value)

                                rwEq.save()
        elif ncol == 34: #storage tank
            for row in range(1,nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,
                                                                                                         3).value and ws.cell(
                    row, 4).value and ws.cell(row, 5).value and ws.cell(row, 6).value and ws.cell(row, 7).value:
                    if checkEquipmentAvaiable(ws.cell(row, 4).value, ws.cell(row, 5).value,ws.cell(row,0).value, ws.cell(row, 2).value):
                        for a in listProposal:
                            if a.equipmentid_id == getEquipmentID(ws.cell(row,0).value):
                                rwEq = models.RwEquipment.objects.get(id= a.id)
                                rwInputCaTank = models.RwInputCaTank.objects.get(id= a.id)
                                rwEq.commissiondate = xldate_to_datetime(ws.cell(row,7).value)
                                rwEq.adminupsetmanagement = convertTF(ws.cell(row,15).value)

                                # rwEq.cyclicoperation = convertTF(ws.cell(row,12).value)
                                rwEq.downtimeprotectionused = convertTF(ws.cell(row,23).value)
                                rwEq.steamoutwaterflush = convertTF(ws.cell(row,24).value)
                                rwEq.heattraced = convertTF(ws.cell(row,25).value)
                                rwEq.pwht = convertTF(ws.cell(row,11).value)
                                rwEq.interfacesoilwater = convertTF(ws.cell(row,21).value)
                                rwEq.pressurisationcontrolled = convertTF(ws.cell(row,29).value)
                                rwEq.minreqtemperaturepressurisation = convertFloat(ws.cell(row,30).value)
                                # rwEq.yearlowestexptemp = convertTF(ws.cell(row,20).value)
                                rwEq.materialexposedtoclext = convertTF(ws.cell(row,20).value)
                                rwEq.lineronlinemonitoring = convertTF(ws.cell(row,16).value)
                                rwEq.presencesulphideso2 = convertTF(ws.cell(row,26).value)
                                rwEq.presencesulphideso2shutdown = convertTF(ws.cell(row,27).value)
                                if ws.cell(row,22).value:
                                    rwEq.externalenvironment = ws.cell(row,22).value
                                if ws.cell(row,28).value:
                                    rwEq.thermalhistory = ws.cell(row,28).value
                                if ws.cell(row,12).value:
                                    rwEq.onlinemonitoring = ws.cell(row,12).value
                                rwEq.volume = convertFloat(ws.cell(row,13).value)
                                try:
                                    rwEq.managementfactor = float(ws.cell(row,14).value)
                                except:
                                    rwEq.managementfactor = 0.1
                                if ws.cell(row,31).value:
                                    rwEq.typeofsoil = ws.cell(row,31).value
                                    rwInputCaTank.soil_type = ws.cell(row,31).value
                                rwEq.distancetogroundwater = convertFloat(ws.cell(row,33).value)
                                if ws.cell(row,32).value:
                                    rwEq.environmentsensitivity = ws.cell(row,32).value
                                    rwInputCaTank.environ_sensitivity = ws.cell(row,32).value
                                if ws.cell(row,17).value:
                                    rwEq.adjustmentsettle = ws.cell(row,17).value
                                rwEq.componentiswelded = convertTF(ws.cell(row,18).value)
                                rwEq.tankismaintained = convertTF(ws.cell(row,19).value)

                                rwInputCaTank.sw = convertFloat(ws.cell(row, 29).value)
                                rwEq.save()
                                rwInputCaTank.save()
    except Exception as e:
        print("Exception RwEquipment")
        print(e)

#sheet 1
def saveSheetRwComponent(data):#dang test
    try:
        for a in data:
            if a['isTank']:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['7']:
                    if checkComponentAvaiable(a['0'], a['1']):
                        for b in listProposalData:
                            if b.componentid_id == getComponentID(a['1']):
                                rwCom = models.RwComponent.objects.get(id=b.id)
                                rwInputCaTank = models.RwInputCaTank.objects.get(id=b.id)
                                rwCom.nominaldiameter = convertFloat(a['9'])
                                rwInputCaTank.tank_diametter = convertFloat(a['9'])
                                rwCom.nominalthickness = convertFloat(a['10'])
                                rwCom.currentthickness = convertFloat(a['11'])
                                rwCom.minstructuralthickness = convertFloat(a['11'])
                                rwCom.minreqthickness = convertFloat(a['13'])
                                rwCom.currentcorrosionrate = convertFloat(a['12'])
                                rwCom.weldjointefficiency = convertFloat(a['15'])
                                rwCom.allowablestress = convertFloat(a['16'])
                                rwCom.confidencecorrosionrate = a['17']
                                rwCom.minstructuralthickness = convertFloat(a['18'])
                                rwCom.structuralthickness = convertFloat(a['19'])
                                rwCom.componentvolume = convertFloat(a['20'])
                                rwCom.fabricatedsteel = convertTF(a['23'])
                                rwCom.equipmentsatisfied = convertTF(a['24'])
                                rwCom.nominaloperatingconditions = convertTF(a['25'])
                                rwCom.cetgreaterorequal = convertTF(a['26'])
                                rwCom.cyclicservice = convertTF(a['27'])
                                rwCom.equipmentcircuitshock = convertTF(a['28'])
                                if a['22']:
                                    rwCom.brinnelhardness = a['22']
                                if a['21']:
                                    rwCom.complexityprotrusion = a['21']
                                if a['29']:
                                    rwCom.severityofvibration = a['29']
                                rwCom.releasepreventionbarrier = a['30']
                                rwInputCaTank.prevention_barrier = a['30']
                                rwCom.concretefoundation = a['32']
                                rwCom.shellheight = convertFloat(a['31'])
                                rwInputCaTank.shell_course_height = convertFloat(a['31'])
                                rwCom.crackspresent = a['14']
                                # rwCom.damagefoundinspection = convertTF(ws.cell(row,15).value)
                                # rwCom.deltafatt = convertFloat(ws.cell(row,14).value)
                                # rwCom.trampelements = convertTF(ws.cell(row,17).value)
                                rwCom.save()
                                rwInputCaTank.save()
                                print("save RwComponent")
            else:
                if a['0'] and a['1'] and a['2'] and a['3'] and a['4'] and a['7']:
                    if checkComponentAvaiable(a['0'], a['1']):
                        for b in listProposalData:
                            if b.componentid_id == getComponentID(a['1']):
                                rwCom = models.RwComponent.objects.get(id= b.id)
                                rwCom.nominaldiameter = convertFloat(a['9'])
                                rwCom.nominalthickness = convertFloat(a['10'])
                                # rwCom.currentthickness = convertFloat(ws.cell(row,11).value)
                                rwCom.minreqthickness = convertFloat(a['13'])
                                rwCom.currentcorrosionrate = convertFloat(a['12'])
                                if a['35']:
                                    rwCom.branchdiameter = a['35']
                                if a['36']:
                                    rwCom.branchjointtype = a['36']
                                if a['32']:
                                    rwCom.brinnelhardness = a['22']
                                rwCom.chemicalinjection = a['42']
                                rwCom.highlyinjectioninsp = a['43']
                                if a['21']:
                                    rwCom.complexityprotrusion = a['21']
                                if a['41']:
                                    rwCom.correctiveaction = a['41']
                                rwCom.crackspresent = a['14']
                                if a['33']:
                                    rwCom.cyclicloadingwitin15_25m = a['33']
                                # rwCom.damagefoundinspection = convertTF(ws.cell(row,15).value)
                                rwCom.deltafatt = convertFloat(a['24'])
                                if a['37']:
                                    rwCom.numberpipefittings = a['37']
                                if a['38']:
                                    rwCom.pipecondition = a['38']
                                if a['34']:
                                    rwCom.previousfailures = a['34']
                                if a['39']:
                                    rwCom.shakingamount = a['39']
                                rwCom.shakingdetected = a['32']
                                if a['40']:
                                    rwCom.shakingtime = a['40']
                                rwCom.weldjointefficiency = convertFloat(a['15'])
                                rwCom. allowablestress = convertFloat(a['16'])
                                rwCom.confidencecorrosionrate = a['17']
                                rwCom.minstructuralthickness = a['18']
                                rwCom.structuralthickness = convertFloat(a['19'])
                                rwCom.componentvolume = convertFloat(a['20'])
                                rwCom.hthadamage = a['23']
                                rwCom.fabricatedsteel = a['25']
                                rwCom.equipmentsatisfied = a['26']
                                rwCom.nominaloperatingconditions = a['27']
                                rwCom.cetgreaterorequal = a['28']
                                rwCom.cyclicservice = a['29']
                                rwCom.equipmentcircuitshock = a['30']
                                rwCom.brittlefracturethickness = a['31']
                                # rwCom.trampelements = convertTF(ws.cell(row,18).value)
                                rwCom.save()
    except Exception as e:
        print(e)
        print("error at saveSheetRwComponent")
def processRwComponent(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 44: #plan process
            for row in range(1, nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,
                                                                                                         3).value and ws.cell(
                    row, 4).value and ws.cell(row, 7).value:
                    if checkComponentAvaiable(ws.cell(row, 0).value, ws.cell(row, 1).value):
                        for a in listProposal:
                            if a.componentid_id == getComponentID(ws.cell(row, 1).value):
                                rwCom = models.RwComponent.objects.get(id= a.id)
                                rwCom.nominaldiameter = convertFloat(ws.cell(row,9).value)
                                rwCom.nominalthickness = convertFloat(ws.cell(row,10).value)
                                # rwCom.currentthickness = convertFloat(ws.cell(row,11).value)
                                rwCom.minreqthickness = convertFloat(ws.cell(row,13).value)
                                rwCom.currentcorrosionrate = convertFloat(ws.cell(row,12).value)
                                if ws.cell(row,35).value:
                                    rwCom.branchdiameter = ws.cell(row,35).value
                                if ws.cell(row,36).value:
                                    rwCom.branchjointtype = ws.cell(row,36).value
                                if ws.cell(row,22).value:
                                    rwCom.brinnelhardness = ws.cell(row,22).value
                                rwCom.chemicalinjection = convertTF(ws.cell(row,42).value)
                                rwCom.highlyinjectioninsp = convertTF(ws.cell(row,43).value)
                                if ws.cell(row,21).value:
                                    rwCom.complexityprotrusion = ws.cell(row,21).value
                                if ws.cell(row,41).value:
                                    rwCom.correctiveaction = ws.cell(row,41).value
                                rwCom.crackspresent = convertTF(ws.cell(row,14).value)
                                if ws.cell(row,33).value:
                                    rwCom.cyclicloadingwitin15_25m = ws.cell(row,33).value
                                # rwCom.damagefoundinspection = convertTF(ws.cell(row,15).value)
                                rwCom.deltafatt = convertFloat(ws.cell(row,24).value)
                                if ws.cell(row,37).value:
                                    rwCom.numberpipefittings = ws.cell(row,37).value
                                if ws.cell(row,38).value:
                                    rwCom.pipecondition = ws.cell(row,38).value
                                if ws.cell(row,34).value:
                                    rwCom.previousfailures = ws.cell(row,34).value
                                if ws.cell(row,39).value:
                                    rwCom.shakingamount = ws.cell(row,39).value
                                rwCom.shakingdetected = convertTF(ws.cell(row,32).value)
                                if ws.cell(row,40).value:
                                    rwCom.shakingtime = ws.cell(row,40).value
                                rwCom.weldjointefficiency = convertFloat(ws.cell(row,15).value)
                                rwCom. allowablestress = convertFloat(ws.cell(row,16).value)
                                rwCom.confidencecorrosionrate = ws.cell(row,17).value
                                rwCom.minstructuralthickness = convertTF(ws.cell(row,18).value)
                                rwCom.structuralthickness = convertFloat(ws.cell(row,19).value)
                                rwCom.componentvolume = convertFloat(ws.cell(row,20).value)
                                rwCom.hthadamage = convertTF(ws.cell(row,23).value)
                                rwCom.fabricatedsteel = convertTF(ws.cell(row,25).value)
                                rwCom.equipmentsatisfied = convertTF(ws.cell(row,26).value)
                                rwCom.nominaloperatingconditions = convertTF(ws.cell(row,27).value)
                                rwCom.cetgreaterorequal = convertTF(ws.cell(row,28).value)
                                rwCom.cyclicservice = convertTF(ws.cell(row,29).value)
                                rwCom.equipmentcircuitshock = convertTF(ws.cell(row,30).value)
                                rwCom.brittlefracturethickness = convertTF(ws.cell(row,31).value)
                                # rwCom.trampelements = convertTF(ws.cell(row,18).value)
                                rwCom.save()
        elif ncol == 33: #storage tank
            for row in range(1, nrow):
                if ws.cell(row, 0).value and ws.cell(row, 1).value and ws.cell(row, 2).value and ws.cell(row,
                                                                                                         3).value and ws.cell(
                    row, 4).value and ws.cell(row, 7).value:
                    if checkComponentAvaiable(ws.cell(row, 0).value, ws.cell(row, 1).value):
                        for a in listProposal:
                            if a.componentid_id == getComponentID(ws.cell(row, 1).value):
                                rwCom = models.RwComponent.objects.get(id= a.id)
                                rwInputCaTank = models.RwInputCaTank.objects.get(id= a.id)
                                rwCom.nominaldiameter = convertFloat(ws.cell(row,9).value)
                                rwInputCaTank.tank_diametter = convertFloat(ws.cell(row,9).value)
                                rwCom.nominalthickness = convertFloat(ws.cell(row,10).value)
                                rwCom.currentthickness = convertFloat(ws.cell(row,11).value)
                                rwCom.minstructuralthickness = convertFloat(ws.cell(row,11).value)
                                rwCom.minreqthickness = convertFloat(ws.cell(row,13).value)
                                rwCom.currentcorrosionrate = convertFloat(ws.cell(row,12).value)
                                rwCom. weldjointefficiency = convertFloat(ws.cell(row,15).value)
                                rwCom. allowablestress = convertFloat(ws.cell(row,16).value)
                                rwCom.confidencecorrosionrate = ws.cell(row,17).value
                                rwCom.minstructuralthickness = convertFloat(ws.cell(row,18).value)
                                rwCom.structuralthickness = convertFloat(ws.cell(row,19).value)
                                rwCom.componentvolume = convertFloat(ws.cell(row,20).value)
                                rwCom.fabricatedsteel = convertTF(ws.cell(row,23).value)
                                rwCom.equipmentsatisfied = convertTF(ws.cell(row,24).value)
                                rwCom.nominaloperatingconditions = convertTF(ws.cell(row,25).value)
                                rwCom.cetgreaterorequal = convertTF(ws.cell(row,26).value)
                                rwCom.cyclicservice = convertTF(ws.cell(row,27).value)
                                rwCom.equipmentcircuitshock = convertTF(ws.cell(row,28).value)
                                if ws.cell(row,22).value:
                                    rwCom.brinnelhardness = ws.cell(row,22).value
                                if ws.cell(row,21).value:
                                    rwCom.complexityprotrusion = ws.cell(row,21).value
                                if ws.cell(row,29).value:
                                    rwCom.severityofvibration = ws.cell(row,29).value
                                rwCom.releasepreventionbarrier = convertTF(ws.cell(row,30).value)
                                rwInputCaTank.prevention_barrier = convertTF(ws.cell(row,30).value)
                                rwCom.concretefoundation = convertTF(ws.cell(row,32).value)
                                rwCom.shellheight = convertFloat(ws.cell(row,31).value)
                                rwInputCaTank.shell_course_height = convertFloat(ws.cell(row,31).value)
                                rwCom.crackspresent = convertTF(ws.cell(row,14).value)
                                # rwCom.damagefoundinspection = convertTF(ws.cell(row,15).value)
                                # rwCom.deltafatt = convertFloat(ws.cell(row,14).value)
                                # rwCom.trampelements = convertTF(ws.cell(row,17).value)
                                rwCom.save()
                                rwInputCaTank.save()
    except Exception as e:
        print("Exception at RwComponent")
        print(e)

#sheet 2
def saveSheetRwExtcor(data):
    try:
        for a in data:
            if a['0']:
                for b in listProposalData:
                    if b.componentid_id == getComponentID(a['0']):
                        rwExt = models.RwExtcorTemperature.objects.get(id=b.id)
                        rwExt.minus12tominus8 = convertFloat(a['7'])
                        rwExt.minus8toplus6 = convertFloat(a['8'])
                        rwExt.plus6toplus32 = convertFloat(a['9'])
                        rwExt.plus32toplus71 = convertFloat(a['10'])
                        rwExt.plus71toplus107 = convertFloat(a['11'])
                        rwExt.plus107toplus121 = convertFloat(a['12'])
                        rwExt.plus121toplus135 = convertFloat(a['13'])
                        rwExt.plus135toplus162 = convertFloat(a['14'])
                        rwExt.plus162toplus176 = convertFloat(a['15'])
                        rwExt.morethanplus176 = convertFloat(a['16'])
                        rwExt.save()
                        print("save RwExtcor")
    except Exception as e:
        print(e)
        print("error at saveSheetRwExtcor")
def processRwExtcor(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 18 or ncol == 17: # process plan and storage tank
            for row in range(1,nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwExt = models.RwExtcorTemperature.objects.get(id= a.id)
                            rwExt.minus12tominus8 = convertFloat(ws.cell(row,7).value)
                            rwExt.minus8toplus6 = convertFloat(ws.cell(row,8).value)
                            rwExt.plus6toplus32 = convertFloat(ws.cell(row,9).value)
                            rwExt.plus32toplus71 = convertFloat(ws.cell(row,10).value)
                            rwExt.plus71toplus107 = convertFloat(ws.cell(row,11).value)
                            rwExt.plus107toplus121 = convertFloat(ws.cell(row,12).value)
                            rwExt.plus121toplus135 = convertFloat(ws.cell(row,13).value)
                            rwExt.plus135toplus162 = convertFloat(ws.cell(row,14).value)
                            rwExt.plus162toplus176 = convertFloat(ws.cell(row,15).value)
                            rwExt.morethanplus176 = convertFloat(ws.cell(row,16).value)
                            rwExt.save()
    except Exception as e:
        print("Exception at RwExtcor")
        print(e)

#sheet 2
def saveSheetStream1(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0']:
                    for b in listProposalData:
                        if b.componentid_id == getComponentID(a['0']):
                            rwStream = models.RwStream.objects.get(id=b.id)
                            rwStream.maxoperatingtemperature = convertFloat(a['1'])
                            rwStream.minoperatingtemperature = convertFloat(a['2'])
                            rwStream.criticalexposuretemperature = convertFloat(a['3'])
                            rwStream.maxoperatingpressure = convertFloat(a['4'])
                            rwStream.minoperatingpressure = convertFloat(a['5'])
                            rwStream.flowrate = convertFloat(a['6'])
                            rwStream.save()
                            print("save Stream1")
            else:
                if a['0']:
                    for b in listProposalData:
                        if b.componentid_id == getComponentID(a['0']):
                            rwStream = models.RwStream.objects.get(id=b.id)
                            rwStream.maxoperatingtemperature = convertFloat(a['1'])
                            rwStream.minoperatingtemperature = convertFloat(a['2'])
                            rwStream.criticalexposuretemperature = convertFloat(a['3'])
                            rwStream.maxoperatingpressure = convertFloat(a['4'])
                            rwStream.minoperatingpressure = convertFloat(a['5'])
                            rwStream.flowrate = convertFloat(a['6'])
                            rwStream.h2spartialpressure = convertFloat(
                                a['17'])  # h2s == operating hydrogen partial pressure
                            rwStream.save()
                            print("save Stream1")
    except Exception as e:
        print(e)
        print("error at saveSheetStream1")
def processStream1(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 18: # process plan
            for row in range(1, nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwStream = models.RwStream.objects.get(id= a.id)
                            rwStream.maxoperatingtemperature = convertFloat(ws.cell(row,1).value)
                            rwStream.minoperatingtemperature = convertFloat(ws.cell(row,2).value)
                            rwStream.criticalexposuretemperature = convertFloat(ws.cell(row,3).value)
                            rwStream.maxoperatingpressure = convertFloat(ws.cell(row,4).value)
                            rwStream.minoperatingpressure = convertFloat(ws.cell(row,5).value)
                            rwStream.flowrate = convertFloat(ws.cell(row,6).value)
                            rwStream.h2spartialpressure = convertFloat(ws.cell(row,17).value) # h2s == operating hydrogen partial pressure
                            rwStream.save()
        elif ncol == 17: #storage tank
            for row in range(1, nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwStream = models.RwStream.objects.get(id= a.id)
                            rwStream.maxoperatingtemperature = convertFloat(ws.cell(row,1).value)
                            rwStream.minoperatingtemperature = convertFloat(ws.cell(row,2).value)
                            rwStream.criticalexposuretemperature = convertFloat(ws.cell(row,3).value)
                            rwStream.maxoperatingpressure = convertFloat(ws.cell(row,4).value)
                            rwStream.minoperatingpressure = convertFloat(ws.cell(row,5).value)
                            rwStream.flowrate = convertFloat(ws.cell(row, 6).value)
                            rwStream.save()
    except Exception as e:
        print("Exception at RwStream sheet 2")
        print(e)

#sheet 3
def saveSheetStream2(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0']:
                    for b in listProposalData:

                        if b.componentid_id == getComponentID(a['0']):
                            rwStream = models.RwStream.objects.get(id= b.id)
                            rwInputCaTank = models.RwInputCaTank.objects.get(id= b.id)
                            rwStream.naohconcentration = convertFloat(a['22'])
                            rwStream.releasefluidpercenttoxic = convertFloat(a['8'])
                            rwStream.chloride = convertFloat(a['23'])
                            rwStream.co3concentration = convertFloat(a['24'])
                            rwStream.h2sinwater = convertFloat(a['25'])
                            rwStream.waterph = convertFloat(a['10'])
                            rwStream.exposedtogasamine = convertInt(a['11'])
                            rwStream.toxicconstituent = convertInt(a['9'])
                            if a['20']:
                                rwStream.exposuretoamine = a['20']
                            if a['21']:
                                rwStream.aminesolution = a['21']
                            rwStream.aqueousoperation = convertInt(a['12'])
                            rwStream.aqueousshutdown = convertInt(a['13'])
                            rwStream.h2s = convertInt(a['14'])
                            rwStream.hydrofluoric = convertInt(a['15'])
                            rwStream.cyanide = convertInt(a['19'])
                            # rwStream.hydrogen = convertTF(ws.cell(row,16).value)
                            rwStream.caustic = convertInt(a['16'])
                            rwStream.exposedtosulphur = convertInt(a['17'])
                            rwStream.materialexposedtoclint = convertInt(a['18'])
                            if a['1']:
                                rwStream.tankfluidname = a['1']
                                rwInputCaTank.tank_fluid = a['1']
                            rwStream.fluidheight = convertFloat(a['2'])
                            rwStream.fluidleavedikepercent = convertFloat(a['3'])
                            rwStream.fluidleavedikeremainonsitepercent = convertFloat(a['4'])
                            rwStream.fluidgooffsitepercent = convertFloat(a['5'])
                            # add input for input ca tank
                            rwInputCaTank.fluid_height = convertFloat(a['2'])
                            rwInputCaTank.p_lvdike = convertFloat(a['22'])
                            rwInputCaTank.p_onsite = convertFloat(a['23'])
                            rwInputCaTank.p_offsite = convertFloat(a['24'])
                            rwInputCaTank.api_fluid = getApiTankFluid(a['1'])
                            rwInputCaTank.primary_fluid = convertFloat(a['6'])
                            rwInputCaTank.volatile_fluid = convertFloat(a['7'])
                            rwStream.save()
                            rwInputCaTank.save()
                            print("save Stream2")
            else:
                if a['0']:
                    for b in listProposalData:
                        print(a['0'])
                        getComponentID(a['0'])
                        if b.componentid_id == getComponentID(a['0']):
                            rwStream = models.RwStream.objects.get(id=b.id)
                            rwInputCaLevel1 = models.RwInputCaLevel1.objects.get(id=b.id)
                            rwStream.naohconcentration = convertFloat(a['22'])
                            rwStream.releasefluidpercenttoxic = convertFloat(a['8'])
                            rwStream.chloride = convertFloat(a['23'])
                            rwStream.co3concentration = convertFloat(a['24'])
                            rwStream.h2sinwater = convertFloat(a['25'])
                            rwStream.waterph = convertFloat(a['10'])
                            rwStream.exposedtogasamine = convertTF(a['11'])
                            rwStream.toxicconstituent = convertTF(a['9'])
                            if a['20']:
                                rwStream.exposuretoamine = a['20']
                            if a['21']:
                                rwStream.aminesolution = a['21']
                            rwStream.aqueousoperation = convertTF(a['12'])
                            rwStream.aqueousshutdown = convertTF(a['13'])
                            rwStream.h2s = convertTF(a['14'])
                            rwStream.hydrofluoric = convertTF(a['15'])
                            rwStream.cyanide = convertTF(a['19'])
                            rwStream.hydrogen = convertTF(a['26'])
                            rwStream.caustic = convertTF(a['16'])
                            rwStream.exposedtosulphur = convertTF(a['17'])
                            rwStream.materialexposedtoclint = convertTF(a['18'])
                            # add new input for rbi6
                            rwStream.storagephase = a['3']
                            rwStream.liquidlevel = convertFloat(a['4'])
                            rwInputCaLevel1.model_fluid = a['1']
                            rwInputCaLevel1.toxic_fluid = a['2']
                            rwInputCaLevel1.toxic_percent = convertFloat(a['5'])
                            rwInputCaLevel1.primary_fluid = convertFloat(a['6'])
                            rwInputCaLevel1.volatile_fluid = convertFloat(a['7'])
                            rwInputCaLevel1.save()
                            rwStream.save()
                            print("save Stream2")
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print("error at saveSheetStream2")
def processStream2(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 27: #plan process
            for row in range(1,nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwStream = models.RwStream.objects.get(id=a.id)
                            rwInputCaLevel1 = models.RwInputCaLevel1.objects.get(id=a.id)
                            rwStream.naohconcentration = convertFloat(ws.cell(row,22).value)
                            rwStream.releasefluidpercenttoxic = convertFloat(ws.cell(row,8).value)
                            rwStream.chloride = convertFloat(ws.cell(row,23).value)
                            rwStream.co3concentration = convertFloat(ws.cell(row,24).value)
                            rwStream.h2sinwater = convertFloat(ws.cell(row,25).value)
                            rwStream.waterph = convertFloat(ws.cell(row,10).value)
                            rwStream.exposedtogasamine = convertTF(ws.cell(row,11).value)
                            rwStream.toxicconstituent = convertTF(ws.cell(row,9).value)
                            if ws.cell(row,20).value:
                                rwStream.exposuretoamine = ws.cell(row,20).value
                            if ws.cell(row,21).value:
                                rwStream.aminesolution = ws.cell(row,21).value
                            rwStream.aqueousoperation = convertTF(ws.cell(row,12).value)
                            rwStream.aqueousshutdown = convertTF(ws.cell(row,13).value)
                            rwStream.h2s = convertTF(ws.cell(row,14).value)
                            rwStream.hydrofluoric = convertTF(ws.cell(row,15).value)
                            rwStream.cyanide = convertTF(ws.cell(row,19).value)
                            rwStream.hydrogen = convertTF(ws.cell(row,26).value)
                            rwStream.caustic = convertTF(ws.cell(row,16).value)
                            rwStream.exposedtosulphur = convertTF(ws.cell(row,17).value)
                            rwStream.materialexposedtoclint = convertTF(ws.cell(row,18).value)
                            # add new input for rbi6
                            rwStream.storagephase = ws.cell(row,3).value
                            rwStream.liquidlevel = convertFloat(ws.cell(row,4).value)
                            rwInputCaLevel1.model_fluid = ws.cell(row,1).value
                            rwInputCaLevel1.toxic_fluid = ws.cell(row,2).value
                            rwInputCaLevel1.toxic_percent = convertFloat(ws.cell(row,5).value)
                            rwInputCaLevel1.primary_fluid = convertFloat(ws.cell(row,6).value)
                            rwInputCaLevel1.volatile_fluid = convertFloat(ws.cell(row,7).value)
                            rwInputCaLevel1.save()
                            rwStream.save()
        elif ncol == 26: #storage tank
            for row in range(1,nrow):
                if ws.cell(row,0).value and ws.cell(row,20).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwStream = models.RwStream.objects.get(id= a.id)
                            rwInputCaTank = models.RwInputCaTank.objects.get(id= a.id)
                            rwStream.naohconcentration = convertFloat(ws.cell(row,22).value)
                            rwStream.releasefluidpercenttoxic = convertFloat(ws.cell(row,8).value)
                            rwStream.chloride = convertFloat(ws.cell(row,23).value)
                            rwStream.co3concentration = convertFloat(ws.cell(row,24).value)
                            rwStream.h2sinwater = convertFloat(ws.cell(row,25).value)
                            rwStream.waterph = convertFloat(ws.cell(row,10).value)
                            rwStream.exposedtogasamine = convertTF(ws.cell(row,11).value)
                            rwStream.toxicconstituent = convertTF(ws.cell(row,9).value)
                            if ws.cell(row,20).value:
                                rwStream.exposuretoamine = ws.cell(row,20).value
                            if ws.cell(row,21).value:
                                rwStream.aminesolution = ws.cell(row,21).value
                            rwStream.aqueousoperation = convertTF(ws.cell(row,12).value)
                            rwStream.aqueousshutdown = convertTF(ws.cell(row,13).value)
                            rwStream.h2s = convertTF(ws.cell(row,14).value)
                            rwStream.hydrofluoric = convertTF(ws.cell(row,15).value)
                            rwStream.cyanide = convertTF(ws.cell(row,19).value)
                            # rwStream.hydrogen = convertTF(ws.cell(row,16).value)
                            rwStream.caustic = convertTF(ws.cell(row,16).value)
                            rwStream.exposedtosulphur = convertTF(ws.cell(row,17).value)
                            rwStream.materialexposedtoclint = convertTF(ws.cell(row,18).value)
                            if ws.cell(row,1).value:
                                rwStream.tankfluidname = ws.cell(row,1).value
                                rwInputCaTank.tank_fluid = ws.cell(row,1).value
                            rwStream.fluidheight = convertFloat(ws.cell(row,2).value)
                            rwStream.fluidleavedikepercent = convertFloat(ws.cell(row,3).value)
                            rwStream.fluidleavedikeremainonsitepercent = convertFloat(ws.cell(row,4).value)
                            rwStream.fluidgooffsitepercent = convertFloat(ws.cell(row,5).value)
                            # add input for input ca tank
                            rwInputCaTank.fluid_height = convertFloat(ws.cell(row, 2).value)
                            rwInputCaTank.p_lvdike = convertFloat(ws.cell(row,22).value)
                            rwInputCaTank.p_onsite = convertFloat(ws.cell(row,23).value)
                            rwInputCaTank.p_offsite = convertFloat(ws.cell(row,24).value)
                            rwInputCaTank.api_fluid = getApiTankFluid(ws.cell(row,1).value)
                            rwInputCaTank.primary_fluid = convertFloat(ws.cell(row,6).value)
                            rwInputCaTank.volatile_fluid = convertFloat(ws.cell(row,7).value)
                            rwStream.save()
                            rwInputCaTank.save()
    except Exception as e:
        print("Exception at RwStream sheet 3")
        print(e)

#sheet 4
def saveSheetMaterial(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0']:
                    for b in listProposalData:
                        if b.componentid_id == getComponentID(a['0']):
                            rwMaterial = models.RwMaterial.objects.get(id=b.id)
                            rwMaterial.materialname = a['1']
                            rwMaterial.designpressure = convertFloat(a['4'])
                            rwMaterial.designtemperature = convertFloat(a['5'])
                            rwMaterial.mindesigntemperature = convertFloat(a['14'])
                            rwMaterial.referencetemperature = convertFloat(a['16'])
                            # rwMaterial.brittlefracturethickness = convertFloat(ws.cell(row, 6).value)
                            # rwMaterial.allowablestress = convertFloat(ws.cell(row, 7).value)
                            rwMaterial.corrosionallowance = convertFloat(a['9'])
                            rwMaterial.carbonlowalloy = a['2']
                            rwMaterial.austenitic = a['3']
                            rwMaterial.nickelbased = a['10']
                            rwMaterial.chromemoreequal12 = a['15']
                            if a['11']:
                                rwMaterial.sulfurcontent = a['11']
                            # if ws.cell(row, 14).value:
                            #     rwMaterial.heattreatment = ws.cell(row, 14).value
                            rwMaterial.ispta = a['12']
                            if a['13']:
                                rwMaterial.ptamaterialcode = a['13']
                            rwMaterial.yieldstrength = convertFloat(a['6'])
                            rwMaterial.tensilestrength = convertFloat(a['7'])
                            rwMaterial.costfactor = convertFloat(a['8'])
                            rwMaterial.save()
                            print("test save for material")
            else:
                if a['0']:
                    for b in listProposalData:
                        if b.componentid_id == getComponentID(a['0']):
                            rwMaterial = models.RwMaterial.objects.get(id= b.id)
                            rwMaterial.materialname = a['1']
                            rwMaterial.designpressure = convertFloat(a['4'])
                            # rwMaterial.designtemperature = convertFloat(ws.cell(row,5).value)
                            rwMaterial.mindesigntemperature = convertFloat(a['17'])
                            rwMaterial.referencetemperature = convertFloat(a['18'])
                            # rwMaterial.brittlefracturethickness = convertFloat(ws.cell(row,6).value)
                            # rwMaterial.allowablestress = convertFloat(ws.cell(row,7).value)
                            rwMaterial.corrosionallowance = convertFloat(a['9'])
                            rwMaterial.sigmaphase = convertFloat(a['20'])
                            rwMaterial.carbonlowalloy = a['2']
                            rwMaterial.austenitic = a['3']
                            rwMaterial.temper = a['10']

                            rwMaterial.nickelbased = a['11']
                            rwMaterial.chromemoreequal12 = a['18']
                            if a['12']:
                                rwMaterial.sulfurcontent = a['12']
                            # if ws.cell(row,16).value:
                            #     rwMaterial.heattreatment = ws.cell(row,16).value
                            # i'm doing here
                            rwMaterial.ishtha = a['15']
                            if a['16']:
                                rwMaterial.hthamaterialcode = a['16']
                            rwMaterial.ispta = a['13']
                            if a['14']:
                                rwMaterial.ptamaterialcode = a['14']
                            rwMaterial.costfactor = convertFloat(a['8'])
                            # add new input for rbi6
                            rwMaterial.designtemperature = convertFloat(a['5'])
                            rwMaterial.yieldstrength = convertFloat(a['6'])
                            rwMaterial.tensilestrength = convertFloat(a['7'])
                            rwMaterial.sigmaphase = convertFloat(a['20'])
                            rwMaterial.save()
                            print("test save for material")
    except Exception as e:
        print(e)
        print("error at Material")
def processMaterial(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 21: # plan process
            for row in range(1, nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwMaterial = models.RwMaterial.objects.get(id= a.id)
                            rwMaterial.materialname = ws.cell(row,1).value
                            rwMaterial.designpressure = convertFloat(ws.cell(row,4).value)
                            # rwMaterial.designtemperature = convertFloat(ws.cell(row,5).value)
                            rwMaterial.mindesigntemperature = convertFloat(ws.cell(row,17).value)
                            rwMaterial.referencetemperature = convertFloat(ws.cell(row,18).value)
                            # rwMaterial.brittlefracturethickness = convertFloat(ws.cell(row,6).value)
                            # rwMaterial.allowablestress = convertFloat(ws.cell(row,7).value)
                            rwMaterial.corrosionallowance = convertFloat(ws.cell(row,9).value)
                            rwMaterial.sigmaphase = convertFloat(ws.cell(row,19).value)
                            rwMaterial.carbonlowalloy = convertTF(ws.cell(row,2).value)
                            rwMaterial.austenitic = convertTF(ws.cell(row,3).value)
                            rwMaterial.temper = convertTF(ws.cell(row,10).value)

                            rwMaterial.nickelbased = convertTF(ws.cell(row,11).value)
                            rwMaterial.chromemoreequal12 = convertTF(ws.cell(row,19).value)
                            if ws.cell(row,12).value:
                                rwMaterial.sulfurcontent = ws.cell(row,12).value
                            # if ws.cell(row,16).value:
                            #     rwMaterial.heattreatment = ws.cell(row,16).value
                            # i'm doing here
                            rwMaterial.ishtha = convertTF(ws.cell(row,15).value)
                            if ws.cell(row,16).value:
                                rwMaterial.hthamaterialcode = ws.cell(row,16).value
                            rwMaterial.ispta = convertTF(ws.cell(row,13).value)
                            if ws.cell(row,14).value:
                                rwMaterial.ptamaterialcode = ws.cell(row,14).value
                            rwMaterial.costfactor = convertFloat(ws.cell(row,8).value)
                            # add new input for rbi6
                            rwMaterial.designtemperature = convertFloat(ws.cell(row,5).value)
                            rwMaterial.yieldstrength = convertFloat(ws.cell(row,6).value)
                            rwMaterial.tensilestrength = convertFloat(ws.cell(row,7).value)
                            rwMaterial.sigmaphase = convertFloat(ws.cell(row,20).value)
                            rwMaterial.save()
        elif ncol == 17: #storage tank
            for row in range(1,nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwMaterial = models.RwMaterial.objects.get(id=a.id)
                            rwMaterial.materialname = ws.cell(row, 1).value
                            rwMaterial.designpressure = convertFloat(ws.cell(row, 4).value)
                            rwMaterial.designtemperature = convertFloat(ws.cell(row, 5).value)
                            rwMaterial.mindesigntemperature = convertFloat(ws.cell(row, 14).value)
                            rwMaterial.referencetemperature = convertFloat(ws.cell(row, 16).value)
                            # rwMaterial.brittlefracturethickness = convertFloat(ws.cell(row, 6).value)
                            # rwMaterial.allowablestress = convertFloat(ws.cell(row, 7).value)
                            rwMaterial.corrosionallowance = convertFloat(ws.cell(row, 9).value)
                            rwMaterial.carbonlowalloy = convertTF(ws.cell(row, 2).value)
                            rwMaterial.austenitic = convertTF(ws.cell(row, 3).value)
                            rwMaterial.nickelbased = convertTF(ws.cell(row, 10).value)
                            rwMaterial.chromemoreequal12 = convertTF(ws.cell(row, 15).value)
                            if ws.cell(row, 11).value:
                                rwMaterial.sulfurcontent = ws.cell(row, 11).value
                            # if ws.cell(row, 14).value:
                            #     rwMaterial.heattreatment = ws.cell(row, 14).value
                            rwMaterial.ispta = convertTF(ws.cell(row, 12).value)
                            if ws.cell(row, 13).value:
                                rwMaterial.ptamaterialcode = ws.cell(row, 13).value
                            rwMaterial.yieldstrength = convertFloat(ws.cell(row,6).value)
                            rwMaterial.tensilestrength = convertFloat(ws.cell(row,7).value)
                            rwMaterial.costfactor = convertFloat(ws.cell(row, 8).value)
                            rwMaterial.save()
    except Exception as e:
        print("Exception at RwMaterial")
        print(e)

#sheet 5
def saveSheetCoating(data):
    try:
        for a in data:
            if a['0']:
                for b in listProposalData:
                    print(a['0'])
                    if b.componentid_id == getComponentID(a['0']):
                        rwCoating = models.RwCoating.objects.get(id=b.id)
                        rwCoating.internalcoating = a['8']
                        rwCoating.externalcoating = a['7']
                        if a['9']:
                            rwCoating.externalcoatingdate = a['9']
                        if a['10']:
                            rwCoating.externalcoatingquality = a['10']
                        rwCoating.supportconfignotallowcoatingmaint = a['11']
                        rwCoating.internalcladding = a['1']
                        rwCoating.claddingcorrosionrate = convertFloat(a['2'])
                        rwCoating.internallining = a['4']
                        if a['5']:
                            rwCoating.internallinertype = a['5']
                        if a['6']:
                            rwCoating.internallinercondition = a['6']
                        rwCoating.externalinsulation = a['12']
                        rwCoating.insulationcontainschloride = a['13']
                        if a['14']:
                            rwCoating.externalinsulationtype = a['14']
                        if a['15']:
                            rwCoating.insulationcondition = a['15']
                        rwCoating.claddingthickness = convertFloat(a['3'])
                        rwCoating.save()
                        print("save Coating")
    except Exception as e:
        print(e)
        print("error at saveSheetCoating")
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print('loi tai day')
#         sheet 6
def saveSheetCOF(data):
    try:
        for a in data:
            if a['isTank']:
                if a['0']:
                    for b in listProposalData:
                        if b.componentid_id == getComponentID(a['0']):
                            # rwinputca = models.RwInputCaLevel1.objects.get(id=b.id)
                            rwfullcoftank = models.RWFullCofTank.objects.filter(id=b.id)
                            if(rwfullcoftank.count() == 0):
                                rwfullcoftank = models.RWFullCofTank(id=b,
                                                            equipcost=a['1'],
                                                            equipoutagemultiplier=a['2'],
                                                            prodcost=a['3'],
                                                            popdens=a['4'],
                                                            injcost=a['5'])
                                rwfullcoftank.save()
                            else:
                                rwfullcoftank = models.RWFullCofTank.objects.get(id=b.id)

                                rwfullcoftank.equipcost=a['1']

                                rwfullcoftank.equipoutagemultiplier=a['2']

                                rwfullcoftank.prodcost=a['3']

                                rwfullcoftank.popdens=a['4']

                                rwfullcoftank.injcost=a['5']
                                rwfullcoftank.save()
            else:
                if a['0']:
                    for b in listProposalData:
                        if b.componentid_id == getComponentID(a['0']):
                            rwinputca = models.RwInputCaLevel1.objects.filter(id=b.id)
                            if (rwinputca.count() == 0):
                                rwinputca = models.RwInputCaLevel1(id=b,
                                                                   mass_inventory=a['1'],
                                                                   detection_type=a['2'],
                                                                   isulation_type=a['3'],
                                                                   mitigation_system=a['4'],
                                                                   process_unit=a['5'],
                                                                   outage_multiplier=a['6'],
                                                                   productioncost=a['7'],
                                                                   personal_density=a['8'],
                                                                   injure_cost=a['9'],
                                                                   evironment_cost=a['10'])
                                rwfullcoftank.save()
                            else:
                                rwinputca = models.RwInputCaLevel1.objects.get(id=b.id)
                                # rwfullcoftank = models.RWFullCofTank.objects.get(id=proposalID)
                                if a['1']:
                                    rwinputca.mass_inventory=a['1']

                                rwinputca.detection_type=a['2']

                                rwinputca.isulation_type=a['3']

                                rwinputca.mitigation_system=a['4']
                                if a['5']:
                                    rwinputca.process_unit=a['5']
                                if a['6']:
                                    rwinputca.outage_multiplier=a['6']
                                if a['7']:
                                    rwinputca.productioncost=a['7']
                                if a['8']:
                                    rwinputca.personal_density=a['8']
                                if a['9']:
                                    rwinputca.injure_cost=a['9']
                                if a['10']:
                                    rwinputca.evironment_cost=a['10']
                            rwinputca.save()
                        print("save COF")
    except Exception as e:
        print(e)
        print("error at saveSheetCOF")
def processCoating(ws):
    try:
        ncol = ws.ncols
        nrow = ws.nrows
        if ncol == 16:
            for row in range(1,nrow):
                if ws.cell(row,0).value:
                    for a in listProposal:
                        if a.componentid_id == getComponentID(ws.cell(row,0).value):
                            rwCoating = models.RwCoating.objects.get(id= a.id)
                            rwCoating.internalcoating = convertTF(ws.cell(row,8).value)
                            rwCoating.externalcoating = convertTF(ws.cell(row,7).value)
                            if ws.cell(row,9).value:
                                rwCoating.externalcoatingdate = xldate_to_datetime(ws.cell(row,9).value)
                            if ws.cell(row,10).value:
                                rwCoating.externalcoatingquality = ws.cell(row,10).value
                            rwCoating.supportconfignotallowcoatingmaint = convertTF(ws.cell(row,11).value)
                            rwCoating.internalcladding = convertTF(ws.cell(row,1).value)
                            rwCoating.claddingcorrosionrate = convertFloat(ws.cell(row,2).value)
                            rwCoating.internallining = convertTF(ws.cell(row,4).value)
                            if ws.cell(row,5).value:
                                rwCoating.internallinertype = ws.cell(row,5).value
                            if ws.cell(row,6).value:
                                rwCoating.internallinercondition = ws.cell(row,6).value
                            rwCoating.externalinsulation = convertTF(ws.cell(row,12).value)
                            rwCoating.insulationcontainschloride = convertTF(ws.cell(row,13).value)
                            if ws.cell(row,14).value:
                                rwCoating.externalinsulationtype = ws.cell(row,14).value
                            if ws.cell(row,15).value:
                                rwCoating.insulationcondition = ws.cell(row,15).value
                            rwCoating.claddingthickness = convertFloat(ws.cell(row,3).value)
                            rwCoating.save()
    except Exception as e:
        print("Exception at RwCoating")
        print(e)

def importPlanProcess(filename):
    try:
        workbook = open_workbook(filename)
        ws0 = workbook.sheet_by_name("Equipment")
        ws1 = workbook.sheet_by_name("Component")
        ws2 = workbook.sheet_by_name("Operating Condition")
        ws3 = workbook.sheet_by_name("Stream")
        ws4 = workbook.sheet_by_name("Material")
        ws5 = workbook.sheet_by_name("CoatingCladdingLiningInsulation")

        ncol0 = ws0.ncols
        ncol1 = ws1.ncols
        ncol2 = ws2.ncols
        ncol3 = ws3.ncols
        ncol4 = ws4.ncols
        ncol5 = ws5.ncols

        if (ncol0 == 30 and ncol1 == 44 and ncol2 == 18 and ncol3 == 27 and ncol4 == 21 and ncol5 == 16) or (ncol0 == 34 and ncol1 == 33 and ncol2 == 17 and ncol3 == 26 and ncol4 == 17 and ncol5 == 16
                                                                                                             ):
            # step 1: processing data Equipment master
            processEquipmentMaster(ws0)
            # step 2: processing data Component master
            processComponentMaster(ws1)
            # step 3: processing data RwAssessment
            processAssessment(ws1)
            # step 4: processing data other Rw
            processRwEquipment(ws0)
            processRwComponent(ws1)
            processRwExtcor(ws2)
            processStream1(ws2)
            processStream2(ws3)
            processMaterial(ws4)
            processCoating(ws5)
    except Exception as e:
        print("Exception at import")
        print(e)
        raise Http404
def ImportSCADA_extend(data,proposalID):
    try:
        print("Goo")
        print(data)
        row = data[0]
        eq = models.RwEquipment.objects.get(id=proposalID)
        print(row[3])
        eq.volume = row[3]
        eq.minreqtemperaturepressurisation = row[4]
        eq.save()
        com = models.RwComponent.objects.get(id=proposalID)
        com.nominaldiameter = row[5]
        com.structuralthickness = row[6]
        com.save()
        stream = models.RwStream.objects.get(id=proposalID)
        stream.flowrate = row[7]
        stream.waterph = row[8]
        stream.save()
    except Exception as e:
        print(e)

def ImportSCADA(filename,proposalID):
    try:
        workbook = open_workbook(filename)
        sheet_names = workbook.sheet_names()
        for name in sheet_names:
            ws0 = workbook.sheet_by_name(name)
            key = ws0.row_values(0, 3, 9)
            value = ws0.row_values(1, 3, 9)
            eq = models.RwEquipment.objects.get(id=proposalID)
            eq.volume = value[0]
            eq.minreqtemperaturepressurisation = value[1]
            eq.save()
            com = models.RwComponent.objects.get(id=proposalID)
            com.nominaldiameter = value[2]
            com.structuralthickness = value[3]
            com.save()
            stream = models.RwStream.objects.get(id=proposalID)
            stream.flowrate = value[4]
            stream.waterph = value[5]
            stream.save()
    except Exception as e:
        print(e)
        print("Exception at import Scada")
        raise Http404

#show excel to table
#sheet 0
def importSheetEquipment(filename):
    try:
        workbook = open_workbook(filename)
        ws0 = workbook.sheet_by_name("Equipment")

        ncol0 = ws0.ncols

    except Exception as e:
        print(e)
        print ("error in importExcel")
def saveRBIData(data):
    try:
        print("testRBI")
        for a in data:
            comp = models.ComponentMaster.objects.filter(equipmentid_id = a['2'])[0]
            # print("cuong",comp.componentid)
            rwass = models.RwAssessment.objects.filter(componentid_id = comp.componentid)[0]
            # print("pro",rwass.id)
            rwEquip = models.RwEquipment.objects.filter(id = rwass)[0]
            rwComp = models.RwComponent.objects.filter(id = rwass)[0]
            rwExco = models.RwExtcorTemperature.objects.filter(id=rwass)[0]
            rwStream = models.RwStream.objects.filter(id = rwass)[0]
            rwMater = models.RwMaterial.objects.filter(id = rwass)[0]
            rwCoat = models.RwCoating.objects.filter(id = rwass)[0]

            rwassCP = models.RwAssessment(equipmentid_id=rwass.equipmentid_id,
                                        componentid_id=rwass.componentid_id,
                                        assessmentdate=rwass.assessmentdate, commisstiondate=rwass.commisstiondate,
                                        riskanalysisperiod=36,
                                        isequipmentlinked=rwass.isequipmentlinked,
                                        proposalname="RBI EQs Data " + str(datetime.datetime.now().strftime('%m-%d-%y,%H:%M:%S')))
            rwassCP.save()
            # Luu lai cac bang trung gian
            # save RwEquipment
            rwEquipCP = models.RwEquipment(id=rwassCP , commissiondate= datetime.datetime.now())
            rwEquipCP.save()
            try:
                if a['28']=="Y":
                    rwEquipCP.pwht = 1
                else:
                    rwEquipCP.pwht = 0
                rwEquipCP.save()
            except:
                rwEquipCP.pwht = 0
                rwEquipCP.save()
            rwEquipCP.commissiondate = rwEquip.commissiondate
            rwEquipCP.adminupsetmanagement = rwEquip.adminupsetmanagement
            rwEquipCP.containsdeadlegs = rwEquip.containsdeadlegs
            rwEquipCP.cyclicoperation= rwEquip.cyclicoperation
            rwEquipCP.highlydeadleginsp = rwEquip.highlydeadleginsp
            rwEquipCP.downtimeprotectionused = rwEquip.downtimeprotectionused
            rwEquipCP.externalenvironment = rwEquip.externalenvironment
            rwEquipCP.heattraced = rwEquip.heattraced
            rwEquipCP.interfacesoilwater = rwEquip.interfacesoilwater
            rwEquipCP.lineronlinemonitoring = rwEquip.lineronlinemonitoring
            rwEquipCP.materialexposedtoclext = rwEquip.materialexposedtoclext
            rwEquipCP.minreqtemperaturepressurisation = rwEquip.minreqtemperaturepressurisation
            rwEquipCP.onlinemonitoring = rwEquip.onlinemonitoring
            rwEquipCP.presencesulphideso2 = rwEquip.presencesulphideso2
            rwEquipCP.presencesulphideso2shutdown = rwEquip.presencesulphideso2shutdown
            rwEquipCP.pressurisationcontrolled = rwEquip.pressurisationcontrolled
            rwEquipCP.steamoutwaterflush = rwEquip.steamoutwaterflush
            rwEquipCP.managementfactor = rwEquip.managementfactor
            rwEquipCP.thermalhistory = rwEquip.thermalhistory
            rwEquipCP.yearlowestexptemp = rwEquip.yearlowestexptemp
            rwEquipCP.volume = rwEquip.volume
            rwEquipCP.typeofsoil = rwEquip.typeofsoil
            rwEquipCP.environmentsensitivity = rwEquip.environmentsensitivity
            rwEquipCP.distancetogroundwater = rwEquip.distancetogroundwater
            rwEquipCP.adjustmentsettle = rwEquip.adjustmentsettle
            rwEquipCP.componentiswelded = rwEquip.componentiswelded
            rwEquipCP.tankismaintained = rwEquip.tankismaintained
            rwEquipCP.save()

            # save RwComponent
            rwCompCP = models.RwComponent(id=rwassCP)
            rwCompCP.save()
            try:
                rwCompCP.nominaldiameter = a['23']
                rwCompCP.minreqthickness = a['25']
                rwCompCP.weldjointefficiency = a['24']
                rwCompCP.save()
            except:
                rwCompCP.nominaldiameter = 0
                rwCompCP.minreqthickness = 0
                rwCompCP.weldjointefficiency = 0
                rwCompCP.save()
            rwCompCP.nominalthickness = rwComp.nominalthickness
            rwCompCP.currentthickness = rwComp.currentthickness
            rwCompCP.currentcorrosionrate = rwComp.currentcorrosionrate
            rwCompCP.branchdiameter = rwComp.branchdiameter
            rwCompCP.branchjointtype = rwComp.branchjointtype
            rwCompCP.brinnelhardness = rwComp.brinnelhardness
            rwCompCP.chemicalinjection = rwComp.chemicalinjection
            rwCompCP.highlyinjectioninsp = rwComp.highlyinjectioninsp
            rwCompCP.complexityprotrusion = rwComp.complexityprotrusion
            rwCompCP.correctiveaction = rwComp.correctiveaction
            rwCompCP.crackspresent = rwComp.crackspresent
            rwCompCP.cyclicloadingwitin15_25m = rwComp.cyclicloadingwitin15_25m
            rwCompCP.damagefoundinspection = rwComp.damagefoundinspection
            rwCompCP.deltafatt = rwComp.deltafatt
            rwCompCP.numberpipefittings = rwComp.numberpipefittings
            rwCompCP.pipecondition = rwComp.pipecondition
            rwCompCP.previousfailures = rwComp.previousfailures
            rwCompCP.shakingamount = rwComp.shakingamount
            rwCompCP.shakingdetected = rwComp.shakingdetected
            rwCompCP.shakingtime = rwComp.shakingtime
            rwCompCP.releasepreventionbarrier = rwComp.releasepreventionbarrier
            rwCompCP.concretefoundation = rwComp.concretefoundation
            rwCompCP.severityofvibration = rwComp.severityofvibration
            rwCompCP.allowablestress = rwComp.allowablestress
            rwCompCP.structuralthickness = rwComp.structuralthickness
            rwCompCP.crackscurrentcondition = rwComp.crackscurrentcondition
            rwCompCP.componentvolume = rwComp.componentvolume
            rwCompCP.minstructuralthickness = rwComp.minstructuralthickness
            rwCompCP.hthadamage = rwComp.hthadamage
            rwCompCP.fabricatedsteel = rwComp.fabricatedsteel
            rwCompCP.equipmentsatisfied = rwComp.equipmentsatisfied
            rwCompCP.nominaloperatingconditions = rwComp.nominaloperatingconditions
            rwCompCP.cetgreaterorequal = rwComp.cetgreaterorequal
            rwCompCP.cyclicservice = rwComp.cyclicservice
            rwCompCP.equipmentcircuitshock = rwComp.equipmentcircuitshock
            rwCompCP.confidencecorrosionrate = rwComp.confidencecorrosionrate
            rwCompCP.brittlefracturethickness = rwComp.brittlefracturethickness
            # rwCom.trampelements = convertTF(ws.cell(row,18).value)
            rwCompCP.save()

            rwExcoCP = models.RwExtcorTemperature(id=rwassCP)
            rwExcoCP.save()
            rwExcoCP.minus12tominus8 = rwExco.minus12tominus8
            rwExcoCP.minus8toplus6 = rwExco.minus8toplus6
            rwExcoCP.plus6toplus32 = rwExco.plus6toplus32
            rwExcoCP.plus32toplus71 = rwExco.plus32toplus71
            rwExcoCP.plus71toplus107 = rwExco.plus71toplus107
            rwExcoCP.plus107toplus121 = rwExco.plus107toplus121
            rwExcoCP.plus121toplus135 = rwExco.plus121toplus135
            rwExcoCP.plus135toplus162 = rwExco.plus135toplus162
            rwExcoCP.plus162toplus176 = rwExco.plus162toplus176
            rwExcoCP.morethanplus176 = rwExco.morethanplus176
            rwExcoCP.save()

            rwStreamCP = models.RwStream(id=rwassCP)
            rwStreamCP.save()
            try:
                rwStreamCP.maxoperatingpressure = a['29']
                rwStreamCP.maxoperatingtemperature = a['30']
                rwStreamCP.storagephase = a['31']
                rwStreamCP.save()
            except:
                rwStreamCP.maxoperatingpressure = 0
                rwStreamCP.maxoperatingtemperature = 0
                rwStreamCP.storagephase = ""
                rwStreamCP.save()
            rwStreamCP.aminesolution = rwStream.aminesolution
            rwStreamCP.aqueousoperation = rwStream.aqueousoperation
            rwStreamCP.aqueousshutdown = rwStream.aqueousshutdown
            rwStreamCP.toxicconstituent = rwStream.toxicconstituent
            rwStreamCP.caustic = rwStream.caustic
            rwStreamCP.chloride = rwStream.chloride  # h2s == operating hydrogen partial pressure
            rwStreamCP.co3concentration = rwStream.co3concentration  # h2s == operating hydrogen partial pressure
            rwStreamCP.cyanide = rwStream.cyanide  # h2s == operating hydrogen partial pressure
            rwStreamCP.exposedtogasamine = rwStream.exposedtogasamine  # h2s == operating hydrogen partial pressure
            rwStreamCP.exposedtosulphur = rwStream.exposedtosulphur  # h2s == operating hydrogen partial pressure
            rwStreamCP.exposuretoamine = rwStream.exposuretoamine  # h2s == operating hydrogen partial pressure
            rwStreamCP.flammablefluidid = rwStream.flammablefluidid  # h2s == operating hydrogen partial pressure
            rwStreamCP.h2s = rwStream.h2s  # h2s == operating hydrogen partial pressure
            rwStreamCP.h2sinwater = rwStream.h2sinwater  # h2s == operating hydrogen partial pressure
            rwStreamCP.hydrogen = rwStream.hydrogen  # h2s == operating hydrogen partial pressure
            rwStreamCP.h2spartialpressure = rwStream.h2spartialpressure  # h2s == operating hydrogen partial pressure
            rwStreamCP.hydrofluoric = rwStream.hydrofluoric  # h2s == operating hydrogen partial pressure
            rwStreamCP.materialexposedtoclint = rwStream.materialexposedtoclint  # h2s == operating hydrogen partial pressure
            rwStreamCP.minoperatingpressure = rwStream.minoperatingpressure  # h2s == operating hydrogen partial pressure
            rwStreamCP.minoperatingtemperature = rwStream.minoperatingtemperature  # h2s == operating hydrogen partial pressure
            rwStreamCP.criticalexposuretemperature = rwStream.criticalexposuretemperature  # h2s == operating hydrogen partial pressure
            rwStreamCP.naohconcentration = rwStream.naohconcentration  # h2s == operating hydrogen partial pressure
            rwStreamCP.releasefluidpercenttoxic = rwStream.releasefluidpercenttoxic  # h2s == operating hydrogen partial pressure
            rwStreamCP.waterph = rwStream.waterph  # h2s == operating hydrogen partial pressure
            rwStreamCP.tankfluidname = rwStream.tankfluidname  # h2s == operating hydrogen partial pressure
            rwStreamCP.fluidheight = rwStream.fluidheight  # h2s == operating hydrogen partial pressure
            rwStreamCP.fluidleavedikepercent = rwStream.fluidleavedikepercent  # h2s == operating hydrogen partial pressure
            rwStreamCP.fluidleavedikeremainonsitepercent = rwStream.fluidleavedikeremainonsitepercent  # h2s == operating hydrogen partial pressure
            rwStreamCP.fluidgooffsitepercent = rwStream.fluidgooffsitepercent  # h2s == operating hydrogen partial pressure
            rwStreamCP.flowrate = rwStream.flowrate  # h2s == operating hydrogen partial pressure
            rwStreamCP.liquidlevel = rwStream.liquidlevel  # h2s == operating hydrogen partial pressure
            rwStreamCP.save()
            if comp.componenttypeid_id == 12 or comp.componenttypeid_id == 13 or comp.componenttypeid_id == 14 or comp.componenttypeid_id == 15:
                rwInputCaTank = models.RwInputCaTank.objects.filter(id=rwass)[0]
                rwInputCaTankCP = models.RwInputCaTank(id=rwassCP)
                rwInputCaTankCP.save()
                rwInputCaTankCP.fluid_height = rwInputCaTank.fluid_height
                rwInputCaTankCP.shell_course_height = rwInputCaTank.shell_course_height
                rwInputCaTankCP.tank_diametter = rwInputCaTank.tank_diametter
                rwInputCaTankCP.prevention_barrier = rwInputCaTank.prevention_barrier
                rwInputCaTankCP.environ_sensitivity = rwInputCaTank.environ_sensitivity
                rwInputCaTankCP.p_lvdike = rwInputCaTank.p_lvdike
                rwInputCaTankCP.p_onsite = rwInputCaTank.p_onsite
                rwInputCaTankCP.p_offsite = rwInputCaTank.p_offsite
                rwInputCaTankCP.soil_type = rwInputCaTank.soil_type
                rwInputCaTankCP.tank_fluid = rwInputCaTank.tank_fluid
                rwInputCaTankCP.api_fluid = rwInputCaTank.api_fluid
                rwInputCaTankCP.sw = rwInputCaTank.sw
                rwInputCaTankCP.productioncost = rwInputCaTank.productioncost
                rwInputCaTankCP.primary_fluid = rwInputCaTank.primary_fluid
                rwInputCaTankCP.volatile_fluid = rwInputCaTank.volatile_fluid
                rwInputCaTankCP.save()

                rwfullcoftank = models.RWFullCofTank.objects.filter(id=rwass)
                rwfullcoftankCP = models.RWFullCofTank(id=rwassCP)
                rwfullcoftankCP.save()
                if rwfullcoftank.count():
                    rwfullcoftankCP.cofvalue = rwfullcoftank[0].cofvalue
                    rwfullcoftankCP.cofcategory = rwfullcoftank[0].cofcategory
                    rwfullcoftankCP.prodcost = rwfullcoftank[0].prodcost
                    rwfullcoftankCP.equipoutagemultiplier = rwfullcoftank[0].equipoutagemultiplier
                    rwfullcoftankCP.equipcost = rwfullcoftank[0].equipcost
                    rwfullcoftankCP.popdens = rwfullcoftank[0].popdens
                    rwfullcoftankCP.injcost = rwfullcoftank[0].injcost
                    rwfullcoftankCP.cofmatrixvalue = rwfullcoftank[0].cofmatrixvalue
                    rwfullcoftankCP.save()
            else:
                rwInputCaLevel1 = models.RwInputCaLevel1.objects.filter(id = rwass)[0]
                rwInputCaLevel1CP = models.RwInputCaLevel1(id=rwassCP)
                rwInputCaLevel1CP.save()
                rwInputCaLevel1CP.api_fluid = rwInputCaLevel1.api_fluid
                rwInputCaLevel1CP.release_duration = rwInputCaLevel1.release_duration
                rwInputCaLevel1CP.detection_type = rwInputCaLevel1.detection_type
                rwInputCaLevel1CP.isulation_type = rwInputCaLevel1.isulation_type
                rwInputCaLevel1CP.equipment_cost = rwInputCaLevel1.equipment_cost
                rwInputCaLevel1CP.injure_cost = rwInputCaLevel1.injure_cost
                rwInputCaLevel1CP.evironment_cost = rwInputCaLevel1.evironment_cost
                rwInputCaLevel1CP.toxic_percent = rwInputCaLevel1.toxic_percent
                rwInputCaLevel1CP.personal_density = rwInputCaLevel1.personal_density
                rwInputCaLevel1CP.material_cost = rwInputCaLevel1.material_cost
                rwInputCaLevel1CP.production_cost = rwInputCaLevel1.production_cost
                rwInputCaLevel1CP.mass_inventory = rwInputCaLevel1.mass_inventory
                rwInputCaLevel1CP.mass_component = rwInputCaLevel1.mass_component
                rwInputCaLevel1CP.stored_pressure = rwInputCaLevel1.stored_pressure
                rwInputCaLevel1CP.stored_temp = rwInputCaLevel1.stored_temp
                rwInputCaLevel1CP.model_fluid = rwInputCaLevel1.model_fluid
                rwInputCaLevel1CP.toxic_fluid = rwInputCaLevel1.toxic_fluid
                rwInputCaLevel1CP.primary_fluid = rwInputCaLevel1.primary_fluid
                rwInputCaLevel1CP.volatile_fluid = rwInputCaLevel1.volatile_fluid
                rwInputCaLevel1CP.mitigation_system = rwInputCaLevel1.mitigation_system
                rwInputCaLevel1CP.process_unit = rwInputCaLevel1.process_unit
                rwInputCaLevel1CP.outage_multiplier = rwInputCaLevel1.outage_multiplier
                rwInputCaLevel1CP.save()
            rwMaterCP = models.RwMaterial(id=rwassCP)
            rwMaterCP.save()
            try:
                rwMaterCP.materialname = a['20']
                rwMaterCP.designpressure = a['18'] * 0.1
                rwMaterCP.designtemperature = a['19']
                rwMaterCP.mindesigntemperature = a['27']
                rwMaterCP.corrosionallowance = a['26']
                rwMaterCP.save()
            except:
                rwMaterCP.materialname = a['20']
                rwMaterCP.designpressure = 0
                rwMaterCP.designtemperature = 0
                rwMaterCP.mindesigntemperature = 0
                rwMaterCP.corrosionallowance = 0
                rwMaterCP.save()
            rwMaterCP.brittlefracturethickness = rwMater.brittlefracturethickness
            rwMaterCP.sigmaphase = rwMater.sigmaphase
            rwMaterCP.sulfurcontent = rwMater.sulfurcontent
            rwMaterCP.heattreatment = rwMater.heattreatment
            rwMaterCP.steelproductform = rwMater.steelproductform
            rwMaterCP.referencetemperature = rwMater.referencetemperature
            rwMaterCP.ptamaterialcode = rwMater.ptamaterialcode
            rwMaterCP.hthamaterialcode = rwMater.hthamaterialcode
            rwMaterCP.ispta = rwMater.ispta
            rwMaterCP.ishtha = rwMater.ishtha
            rwMaterCP.austenitic = rwMater.austenitic
            rwMaterCP.temper = rwMater.temper
            rwMaterCP.carbonlowalloy = rwMater.carbonlowalloy
            rwMaterCP.nickelbased = rwMater.nickelbased
            rwMaterCP.chromemoreequal12 = rwMater.chromemoreequal12
            rwMaterCP.costfactor = rwMater.costfactor
            rwMaterCP.yieldstrength = rwMater.yieldstrength
            rwMaterCP.tensilestrength = rwMater.tensilestrength
            rwMaterCP.save()

            rwCoatCP = models.RwCoating(id= rwassCP, externalcoatingdate= datetime.datetime.now())
            rwCoatCP.save()
            try:
                if a['22'] == 'Y':
                    rwCoatCP.internalcladding = 1
                    rwCoatCP.internallining = 1
                else:
                    rwCoatCP.internalcladding = 0
                    rwCoatCP.internallining = 0
                rwCoatCP.save()
            except:
                rwCoatCP.internalcladding = 0
                rwCoatCP.internallining = 0
                rwCoatCP.save()
            rwCoatCP.externalcoating = rwCoat.externalcoating
            rwCoatCP.externalinsulation = rwCoat.externalinsulation
            rwCoatCP.internalcoating = rwCoat.internalcoating
            rwCoatCP.externalcoatingdate = rwCoat.externalcoatingdate
            rwCoatCP.externalcoatingquality = rwCoat.externalcoatingquality
            rwCoatCP.externalinsulationtype = rwCoat.externalinsulationtype
            rwCoatCP.insulationcondition = rwCoat.insulationcondition
            rwCoatCP.insulationcontainschloride =rwCoat.insulationcontainschloride
            rwCoatCP.internallinercondition = rwCoat.internallinercondition
            rwCoatCP.internallinertype = rwCoat.internallinertype
            rwCoatCP.claddingcorrosionrate = rwCoat.claddingcorrosionrate
            rwCoatCP.supportconfignotallowcoatingmaint = rwCoat.supportconfignotallowcoatingmaint
            rwCoatCP.claddingthickness = rwCoat.claddingthickness
            rwCoatCP.save()
            # rwCoat = models.RwCoating(id= rwAss)#Cương Sửa
            # rwCoat.save()
            listProposalData.append(rwassCP)
            print("save Assessment")

        print(data)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def getRBIData(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("RBMI.EQs Data")
        ncol = ws.ncols
        nrow = ws.nrows
        print(ncol, nrow)
        data = []
        i=0
        if ncol == 72:
            # print("gogo")
            for row in range(3, nrow):
                fc = {}
                fc["id"] = i
                fc['check'] = 1
                fc['0'] = str(ws.cell(row, 0).value)
                fc["1"] = ws.cell(row, 1).value
                fc["2"] = ws.cell(row, 2).value
                fc["3"] = ws.cell(row, 3).value
                fc["4"] = ws.cell(row, 4).value
                fc["5"] = ws.cell(row, 5).value
                fc["6"] = ws.cell(row, 6).value
                fc["7"] = ws.cell(row, 7).value
                fc["8"] = ws.cell(row, 8).value
                fc["9"] = ws.cell(row, 9).value
                fc["10"] = ws.cell(row, 10).value
                fc["11"] = ws.cell(row, 11).value
                fc["12"] = ws.cell(row, 12).value
                fc["13"] = ws.cell(row, 13).value
                fc["14"] = ws.cell(row, 14).value
                fc["15"] = ws.cell(row, 15).value
                fc["16"] = ws.cell(row, 16).value
                fc["17"] = ws.cell(row, 17).value
                fc["18"] = ws.cell(row, 18).value
                fc["19"] = ws.cell(row, 19).value
                fc["20"] = ws.cell(row, 20).value
                fc["21"] = ws.cell(row, 21).value
                fc["22"] = ws.cell(row, 22).value
                fc["23"] = ws.cell(row, 23).value
                fc["24"] = ws.cell(row, 24).value
                fc["25"] = ws.cell(row, 25).value
                fc["26"] = ws.cell(row, 26).value
                fc["27"] = ws.cell(row, 27).value
                fc["28"] = ws.cell(row, 28).value
                fc["29"] = ws.cell(row, 29).value
                fc["30"] = ws.cell(row, 30).value
                fc["31"] = ws.cell(row, 31).value
                fc["32"] = ws.cell(row, 32).value
                fc["33"] = ws.cell(row, 33).value
                fc["34"] = ws.cell(row, 34).value
                fc["35"] = ws.cell(row, 35).value
                fc["36"] = ws.cell(row, 36).value
                fc["37"] = ws.cell(row, 37).value
                fc["38"] = ws.cell(row, 38).value
                fc["39"] = ws.cell(row, 39).value
                fc["40"] = ws.cell(row, 40).value
                fc["41"] = ws.cell(row, 41).value
                fc["42"] = ws.cell(row, 42).value
                fc["43"] = ws.cell(row, 43).value
                fc["44"] = ws.cell(row, 44).value
                fc["45"] = ws.cell(row, 45).value
                fc["46"] = ws.cell(row, 46).value
                fc["47"] = ws.cell(row, 47).value
                fc["48"] = ws.cell(row, 48).value
                fc["49"] = ws.cell(row, 49).value
                fc["50"] = ws.cell(row, 50).value
                fc["51"] = ws.cell(row, 51).value
                fc["52"] = ws.cell(row, 52).value
                fc["53"] = ws.cell(row, 53).value
                fc["54"] = ws.cell(row, 54).value
                fc["55"] = ws.cell(row, 55).value
                fc["56"] = ws.cell(row, 56).value
                fc["57"] = ws.cell(row, 57).value
                fc["58"] = ws.cell(row, 58).value
                fc["59"] = ws.cell(row, 59).value
                fc["60"] = ws.cell(row, 60).value
                fc["61"] = ws.cell(row, 61).value
                fc["62"] = ws.cell(row, 62).value
                fc["63"] = ws.cell(row, 63).value
                fc["64"] = ws.cell(row, 64).value
                fc["65"] = ws.cell(row, 65).value
                fc["66"] = ws.cell(row, 66).value
                i = i+1
                data.append(fc)
        # print(data)
    except Exception as e:
        print("error in getRBIData",e)
    return data
def getSheetEquip(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("Equipment")
        ncol = ws.ncols
        nrow = ws.nrows
        data = []
        i = 0
        # loai Tank
        if ncol == 34:
            for row in range(1, nrow):
                fc = {}
                fc["id"]=i
                fc['isTank'] = 1
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"] = ws.cell(row, 2).value
                fc["3"] = ws.cell(row, 3).value
                fc["4"] = ws.cell(row, 4).value
                fc["5"] = ws.cell(row, 5).value
                fc["6"] = ws.cell(row, 6).value
                if ws.cell(row, 7).value:
                    fc["7"] = xldate_to_datetime(ws.cell(row, 7).value).strftime('%Y-%m-%d')
                else:
                    fc["7"] = datetime.datetime.now().strftime('%Y-%m-%d')
                fc["8"] = ws.cell(row, 8).value
                fc["9"] = ws.cell(row, 9).value
                fc["10"] = ws.cell(row, 10).value
                fc["11"] = ws.cell(row, 11).value
                fc["12"] = ws.cell(row, 12).value
                if ws.cell(row, 13).value:
                    fc["13"]= ws.cell(row, 13).value
                else:
                    fc["13"] =0
                if ws.cell(row, 14).value:
                    fc["14"]= ws.cell(row, 14).value
                else:
                    fc["14"] =0.1
                fc["15"] = ws.cell(row, 15).value
                fc["16"] = ws.cell(row, 16).value
                fc["17"] = ws.cell(row, 17).value
                fc["18"] = ws.cell(row, 18).value
                fc["19"] = ws.cell(row, 19).value
                fc["20"] = ws.cell(row, 20).value
                fc["21"] = ws.cell(row, 21).value
                fc["22"] = ws.cell(row, 22).value
                fc["23"] = ws.cell(row, 23).value
                fc["24"] = ws.cell(row, 24).value
                fc["25"] = ws.cell(row, 25).value
                fc["26"] = ws.cell(row, 26).value
                fc["27"] = ws.cell(row, 27).value
                fc["28"] = ws.cell(row, 28).value
                fc["29"] = ws.cell(row, 29).value
                if ws.cell(row, 30).value:
                    fc["30"] = ws.cell(row, 30).value
                else:
                    fc["30"] =0
                fc["31"] = ws.cell(row, 31).value
                fc["32"] = ws.cell(row, 32).value
                if ws.cell(row, 33).value:
                    fc["33"] = ws.cell(row, 33).value
                else:
                    fc["33"] =0
                i=i+1
                data.append(fc)
        elif ncol==30:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 0
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"] = ws.cell(row, 2).value
                fc["3"] = ws.cell(row, 3).value
                fc["4"] = ws.cell(row, 4).value
                fc["5"] = ws.cell(row, 5).value
                fc["6"] = ws.cell(row, 6).value
                if ws.cell(row, 7).value:
                    fc["7"] = xldate_to_datetime(ws.cell(row, 7).value).strftime('%Y-%m-%d')
                else:
                    fc["7"] = datetime.datetime.now().strftime('%Y-%m-%d')
                fc["8"] = ws.cell(row, 8).value
                fc["9"] = ws.cell(row, 9).value
                fc["10"] = ws.cell(row, 10).value
                fc["11"] = ws.cell(row, 11).value
                fc["12"] = ws.cell(row, 12).value
                if ws.cell(row, 13).value:
                    fc["13"] = ws.cell(row, 13).value
                else:
                    fc["13"] =0
                if ws.cell(row, 14).value:
                    fc["14"] = ws.cell(row, 14).value
                else:
                    fc["14"] =0.1
                fc["15"] = ws.cell(row, 15).value
                fc["16"] = ws.cell(row, 16).value
                fc["17"] = ws.cell(row, 17).value
                fc["18"] = ws.cell(row, 18).value
                fc["19"] = ws.cell(row, 19).value
                fc["20"] = ws.cell(row, 20).value
                fc["21"] = ws.cell(row, 21).value
                fc["22"] = ws.cell(row, 22).value
                fc["23"] = ws.cell(row, 23).value
                fc["24"] = ws.cell(row, 24).value
                fc["25"] = ws.cell(row, 25).value
                fc["26"] = ws.cell(row, 26).value
                if ws.cell(row, 27).value:
                    fc["27"] = ws.cell(row, 27).value
                else:
                    fc["27"] =0
                fc["28"] = ws.cell(row, 28).value
                fc["29"] = ws.cell(row, 29).value
                i=i+1
                data.append(fc)

    except Exception as e:
        print('Exception at sheet Equipment')
        print(e)
    return data
#sheet 1
def getSheetCom(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("Component")
        ncol = ws.ncols
        nrow = ws.nrows
        data = []
        i=0
        # loai Tank
        if ncol == 33:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 1
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"]=ws.cell(row, 2).value
                fc["3"]=ws.cell(row, 3).value
                fc["4"]=ws.cell(row, 4).value
                fc["5"]=ws.cell(row, 5).value
                fc["6"]=ws.cell(row, 6).value
                if ws.cell(row, 7).value:
                    fc["7"]=xldate_to_datetime(ws.cell(row, 7).value).strftime('%Y-%m-%d')
                else:
                    fc["7"] = datetime.datetime.now().strftime('%Y-%m-%d')
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] ='36'
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else:
                    fc["9"] =0
                if ws.cell(row, 10).value:
                    fc["10"]= ws.cell(row, 10).value
                else:
                    fc["10"] =0
                if ws.cell(row, 11).value:
                    fc["11"]= ws.cell(row, 11).value
                else:
                    fc["11"] =0
                if ws.cell(row, 12).value:
                    fc["12"]= ws.cell(row, 12).value
                else:
                    fc["12"] =0
                if ws.cell(row, 13).value:
                    fc["13"]= ws.cell(row, 13).value
                else:
                    fc["13"] =0

                fc["14"]= ws.cell(row, 14).value
                if ws.cell(row, 15).value:
                    fc["15"]= ws.cell(row, 15).value
                else:
                    fc["15"] =0
                if ws.cell(row, 16).value:
                    fc["16"]= ws.cell(row, 16).value
                else:
                    fc["16"] =0
                fc["17"]= ws.cell(row, 17).value
                fc["18"]= ws.cell(row, 18).value
                if ws.cell(row, 19).value:
                    fc["19"]= ws.cell(row, 19).value
                else:
                    fc["19"] =0
                if ws.cell(row, 20).value:
                    fc["20"]= ws.cell(row, 20).value
                else:
                    fc["20"] =0
                fc["21"]= ws.cell(row, 21).value
                fc["22"]= ws.cell(row, 22).value
                fc["23"]= ws.cell(row, 23).value
                fc["24"]= ws.cell(row, 24).value
                fc["25"]= ws.cell(row, 25).value
                fc["26"]= ws.cell(row, 26).value
                fc["27"]= ws.cell(row, 27).value
                fc["28"]= ws.cell(row, 28).value
                fc["29"]= ws.cell(row, 29).value

                fc["30"]= ws.cell(row, 30).value
                if ws.cell(row,31).value:
                    fc["31"]= ws.cell(row,31).value
                else:
                    fc["31"] =0
                fc["32"]= ws.cell(row, 32).value
                i=i+1
                data.append(fc)
        elif ncol==44:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 0
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"]=ws.cell(row, 2).value
                fc["3"]=ws.cell(row, 3).value
                fc["4"]=ws.cell(row, 4).value
                fc["5"]=ws.cell(row, 5).value
                fc["6"]=ws.cell(row, 6).value
                if ws.cell(row, 7).value:
                    fc["7"]=xldate_to_datetime(ws.cell(row, 7).value).strftime('%Y-%m-%d')
                else:
                    fc["7"]=datetime.datetime.now().strftime('%Y-%m-%d')
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =36
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else: fc["9"]=0
                if ws.cell(row, 10).value:
                    fc["10"]= ws.cell(row, 10).value
                else:
                    fc["10"] =0
                if ws.cell(row, 11).value:
                    fc["11"]= ws.cell(row, 11).value
                else:
                    fc["11"] =0
                if ws.cell(row, 12).value:
                    fc["12"]= ws.cell(row, 12).value
                else:
                    fc["12"] =0
                if ws.cell(row, 13).value:
                    fc["13"]= ws.cell(row, 13).value
                else:
                    fc["13"] =0

                fc["14"]= ws.cell(row, 14).value

                if ws.cell(row, 15).value:
                    fc["15"]= ws.cell(row, 15).value
                else:
                    fc["15"] =0
                if ws.cell(row, 16).value:
                    fc["16"]= ws.cell(row, 16).value
                else:
                    fc["16"] =0
                fc["17"]= ws.cell(row, 17).value

                fc["18"]= ws.cell(row, 18).value

                if ws.cell(row, 19).value:
                    fc["19"]= ws.cell(row, 19).value
                else:
                    fc["19"] =0
                if ws.cell(row, 20).value:
                    fc["20"]= ws.cell(row, 20).value
                else:
                    fc["20"] =0
                fc["21"]= ws.cell(row, 21).value
                fc["22"]= ws.cell(row, 22).value
                fc["23"]= ws.cell(row, 23).value
                if ws.cell(row, 24).value:
                    fc["24"]= ws.cell(row, 24).value
                else:
                    fc["24"] =0
                fc["25"]= ws.cell(row, 25).value
                fc["26"]= ws.cell(row, 26).value
                fc["27"]= ws.cell(row, 27).value
                fc["28"]= ws.cell(row, 28).value
                fc["29"]= ws.cell(row, 29).value
                fc["30"]= ws.cell(row, 30).value
                if ws.cell(row,31).value:
                    fc["31"]= ws.cell(row,31).value
                else:
                    fc["31"] =0
                fc["32"]= ws.cell(row, 32).value
                fc["33"]= ws.cell(row, 33).value
                fc["34"]= ws.cell(row, 34).value
                fc["35"]= ws.cell(row, 35).value
                fc["36"]= ws.cell(row, 36).value
                fc["37"]= ws.cell(row, 37).value
                fc["38"]= ws.cell(row, 38).value
                fc["39"]= ws.cell(row, 39).value
                fc["40"]= ws.cell(row, 40).value
                fc["41"]= ws.cell(row, 41).value
                fc["42"]= ws.cell(row, 42).value
                fc["43"]= ws.cell(row, 43).value
                i=i+1
                data.append(fc)
    except Exception as e:
        print('Exception at sheet component')
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(e)
    return data
#sheet 2
def getSheetOperCon(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("Operating Condition")
        ncol = ws.ncols
        nrow = ws.nrows
        data = []
        i=0
        # loai Tank
        if ncol == 17:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 1
                fc["0"] = ws.cell(row, 0).value
                if ws.cell(row, 1).value:
                    fc["1"] = ws.cell(row, 1).value
                else:
                    fc["1"] =0
                if ws.cell(row, 2).value:
                    fc["2"]=ws.cell(row, 2).value
                else:
                    fc["2"] =0
                if ws.cell(row, 3).value:
                    fc["3"]=ws.cell(row, 3).value
                else:
                    fc["3"] =0
                if ws.cell(row, 4).value:
                    fc["4"]=ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =0
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else:
                    fc["9"] =0
                if ws.cell(row, 10).value:
                    fc["10"]= ws.cell(row, 10).value
                else:
                    fc["10"] =0
                if ws.cell(row, 11).value:
                    fc["11"]= ws.cell(row, 11).value
                else:
                    fc["11"] =0
                if ws.cell(row, 12).value:
                    fc["12"]= ws.cell(row, 12).value
                else:
                    fc["12"] =0
                if ws.cell(row, 13).value:
                    fc["13"]= ws.cell(row, 13).value
                else:
                    fc["13"] =0
                if ws.cell(row, 14).value:
                    fc["14"]= ws.cell(row, 14).value
                else:
                    fc["14"] =0
                if ws.cell(row, 15).value:
                    fc["15"]= ws.cell(row, 15).value
                else:
                    fc["15"] =0
                if ws.cell(row, 16).value:
                    fc["16"]= ws.cell(row, 16).value
                else:
                    fc["16"] =0
                i=i+1
                data.append(fc)
        elif ncol==18:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 0
                fc["0"] = ws.cell(row, 0).value
                if ws.cell(row, 1).value:
                    fc["1"] = ws.cell(row, 1).value
                else:
                    fc["1"] =0
                if ws.cell(row, 2).value:
                    fc["2"]=ws.cell(row, 2).value
                else:
                    fc["2"] =0
                if ws.cell(row, 3).value:
                    fc["3"]=ws.cell(row, 3).value
                else:
                    fc["3"] =0
                if ws.cell(row, 4).value:
                    fc["4"]=ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =0
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else:
                    fc["9"] =0
                if ws.cell(row, 10).value:
                    fc["10"]= ws.cell(row, 10).value
                else:
                    fc["10"] =0
                if ws.cell(row, 11).value:
                    fc["11"]= ws.cell(row, 11).value
                else:
                    fc["11"] =0
                if ws.cell(row, 12).value:
                    fc["12"]= ws.cell(row, 12).value
                else:
                    fc["12"] =0
                if ws.cell(row, 13).value:
                    fc["13"]= ws.cell(row, 13).value
                else:
                    fc["13"] =0
                if ws.cell(row, 14).value:
                    fc["14"]= ws.cell(row, 14).value
                else:
                    fc["14"] =0
                if ws.cell(row, 15).value:
                    fc["15"]= ws.cell(row, 15).value
                else:
                    fc["15"] =0
                if ws.cell(row, 16).value:
                    fc["16"]= ws.cell(row, 16).value
                else:
                    fc["16"] =0
                if ws.cell(row, 17).value:
                    fc["17"]= ws.cell(row, 17).value
                else:
                    fc["17"] =0
                i=i+1
                data.append(fc)
    except Exception as e:
        print('Exception at sheet OperCon')
        print(e)
    return data
#sheet 3
def getSheetStream(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("Stream")
        ncol = ws.ncols
        nrow = ws.nrows
        data = []
        i=0
        # loai Tank
        if ncol == 26:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 1
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                if ws.cell(row, 2).value:
                    fc["2"] = ws.cell(row, 4).value
                else:
                    fc["2"] =0
                if ws.cell(row, 3).value:
                    fc["3"]=ws.cell(row, 5).value
                else:
                    fc["3"] =0
                if ws.cell(row, 4).value:
                    fc["4"] = ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =0
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else:
                    fc["9"] =0
                if ws.cell(row, 10).value:
                    fc["10"]= ws.cell(row, 10).value
                else:
                    fc["10"] =0
                fc["11"]= ws.cell(row, 11).value
                fc["12"]= ws.cell(row, 12).value
                fc["13"]= ws.cell(row, 13).value
                fc["14"]= ws.cell(row, 14).value
                fc["15"]= ws.cell(row, 15).value
                fc["16"]= ws.cell(row, 16).value
                fc["17"]= ws.cell(row, 17).value
                fc["18"]= ws.cell(row, 18).value
                fc["19"]= ws.cell(row, 19).value
                fc["20"]= ws.cell(row, 20).value
                fc["21"]= ws.cell(row, 21).value
                if ws.cell(row, 22).value:
                    fc["22"]= ws.cell(row, 22).value
                else:
                    fc["22"] =0
                if ws.cell(row, 23).value:
                    fc["23"]= ws.cell(row, 23).value
                else:
                    fc["23"] =0
                if ws.cell(row, 24).value:
                    fc["24"]= ws.cell(row, 24).value
                else:
                    fc["24"] =0
                if ws.cell(row, 25).value:
                    fc["25"]= ws.cell(row, 25).value
                else:
                    fc["25"] =0
                i=i+1
                data.append(fc)
        elif ncol==27:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 0
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"]=ws.cell(row, 2).value
                fc["3"]=ws.cell(row, 3).value
                if ws.cell(row, 4).value:
                    fc["4"] = ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =0

                fc["9"]= ws.cell(row, 9).value


                if ws.cell(row, 10).value:
                    fc["10"]= ws.cell(row, 10).value
                else:
                    fc["10"] =0
                fc["11"]= ws.cell(row, 11).value
                fc["12"]= ws.cell(row, 12).value
                fc["13"]= ws.cell(row, 13).value
                fc["14"]= ws.cell(row, 14).value
                fc["15"]= ws.cell(row, 15).value
                fc["16"]= ws.cell(row, 16).value
                fc["17"]= ws.cell(row, 17).value
                fc["18"]= ws.cell(row, 18).value
                fc["19"]= ws.cell(row, 19).value
                fc["20"]= ws.cell(row, 20).value
                fc["21"]= ws.cell(row, 21).value
                if ws.cell(row, 22).value:
                    fc["22"]= ws.cell(row, 22).value
                else:
                    fc["22"] =0
                if ws.cell(row, 23).value:
                    fc["23"]= ws.cell(row, 23).value
                else:
                    fc["23"] =0
                if ws.cell(row, 24).value:
                    fc["24"]= ws.cell(row, 24).value
                else:
                    fc["24"] =0
                if ws.cell(row, 25).value:
                    fc["25"]= ws.cell(row, 25).value
                else:
                    fc["25"] =0
                fc["26"]= ws.cell(row, 26).value
                i=i+1
                data.append(fc)
    except Exception as e:
        print('Exception at sheet Stream')
        print(e)
    return data
#sheet 4
def getSheetMaterial(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("Material")
        ncol = ws.ncols
        nrow = ws.nrows
        i=0
        data = []
        # loai Tank
        if ncol == 17:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 1
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"]=ws.cell(row, 2).value
                fc["3"]=ws.cell(row, 3).value
                if ws.cell(row, 4).value:
                    fc["4"]=ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =0
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else:
                    fc["9"] =0

                fc["10"]= ws.cell(row, 10).value
                fc["11"]= ws.cell(row, 11).value
                fc["12"]= ws.cell(row, 12).value
                fc["13"]= ws.cell(row, 13).value
                if  ws.cell(row, 14).value:
                    fc["14"]= ws.cell(row, 14).value
                else:
                    fc["14"] =0
                fc["15"]= ws.cell(row, 15).value
                if  ws.cell(row, 16).value:
                    fc["16"]= ws.cell(row, 16).value
                else:
                    fc["16"] = 0
                i=i+1
                data.append(fc)
        elif ncol==21:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                fc['isTank'] = 0
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                fc["2"]=ws.cell(row, 2).value
                fc["3"]=ws.cell(row, 3).value
                if ws.cell(row, 4).value:
                    fc["4"]=ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"] = ws.cell(row, 8).value
                else:
                    fc["8"] =0
                if ws.cell(row, 9).value:
                    fc["9"]= ws.cell(row, 9).value
                else:
                    fc["9"] =0
                fc["10"]= ws.cell(row, 10).value
                fc["11"]= ws.cell(row, 11).value
                fc["12"]= ws.cell(row, 12).value
                fc["13"]= ws.cell(row, 13).value
                fc["14"]= ws.cell(row, 14).value
                fc["15"]= ws.cell(row, 15).value
                fc["16"]= ws.cell(row, 16).value
                if ws.cell(row, 17).value:
                    fc["17"]= ws.cell(row, 17).value
                else:
                    fc["17"] =0
                fc["18"]= ws.cell(row, 18).value
                if ws.cell(row, 19).value:
                    fc["19"]= ws.cell(row, 19).value
                else:
                    fc["19"] =0
                if ws.cell(row, 20).value:
                    fc["20"]= ws.cell(row, 20).value
                else:
                    fc["20"] =0
                i=i+1
                data.append(fc)
    except Exception as e:
        print('Exception at sheet Material')
        print(e)
    return data
#sheet 5
def getSheetCoat(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("CoatingCladdingLiningInsulation")
        ncol = ws.ncols
        nrow = ws.nrows
        data = []
        i=0
        # loai Tank=nomal
        if ncol == 16:
            for row in range(1, nrow):
                fc = {}
                fc["id"] = i
                # fc['isTank'] = 1
                fc["0"] = ws.cell(row, 0).value
                fc["1"] = ws.cell(row, 1).value
                if ws.cell(row, 2).value:
                    fc["2"]=ws.cell(row, 2).value
                else:
                    fc["2"] =0
                if ws.cell(row, 3).value:
                    fc["3"]=ws.cell(row, 3).value
                else:
                    fc["3"] =0
                fc["4"]=ws.cell(row, 4).value
                fc["5"]=ws.cell(row, 5).value
                fc["6"]=ws.cell(row, 6).value
                fc["7"]=ws.cell(row, 7).value
                fc["8"] = ws.cell(row, 8).value
                if ws.cell(row, 9).value:
                    fc["9"]= xldate_to_datetime(ws.cell(row, 9).value).strftime('%Y-%m-%d')
                else:
                    fc["9"] = datetime.datetime.now().strftime('%Y-%m-%d')
                fc["10"]= ws.cell(row, 10).value
                fc["11"]= ws.cell(row, 11).value
                fc["12"]= ws.cell(row, 12).value
                fc["13"]= ws.cell(row, 13).value
                fc["14"]= ws.cell(row, 14).value
                fc["15"]= ws.cell(row, 15).value
                i=i+1
                data.append(fc)
    except Exception as e:
        print('Exception at sheet Coating')
        print(e)
    return data
#sheet 6
def getSheetFullCoF(filename):
    try:
        workbook = open_workbook(filename)
        ws = workbook.sheet_by_name("Fully CoF")
        ncol = ws.ncols
        nrow = ws.nrows
        i=0
        data = []
        # loai Tank
        if ncol == 6:
            for row in range(1, nrow):
                fc = {}
                fc['isTank'] = 1
                fc["id"] = i
                fc["0"] = ws.cell(row, 0).value
                if ws.cell(row, 1).value:
                    fc["1"] = ws.cell(row, 1).value
                else:
                    fc["1"] =0
                if ws.cell(row, 2).value:
                    fc["2"]=ws.cell(row, 2).value
                else:
                    fc["2"] =0
                if ws.cell(row, 3).value:
                    fc["3"]=ws.cell(row, 3).value
                else:
                    fc["3"] =0
                if ws.cell(row, 4).value:
                    fc["4"]=ws.cell(row, 4).value
                else:
                    fc["4"] =0
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                i=i+1
                data.append(fc)
        elif ncol == 11:
            for row in range(1, nrow):
                fc = {}
                fc['isTank'] = 0
                fc["id"] = i
                fc["0"] = ws.cell(row, 0).value
                if ws.cell(row, 1).value:
                    fc["1"] = ws.cell(row, 1).value
                else:
                    fc["1"] =0
                fc["2"]=ws.cell(row, 2).value
                fc["3"]=ws.cell(row, 3).value
                fc["4"]=ws.cell(row, 4).value
                if ws.cell(row, 5).value:
                    fc["5"]=ws.cell(row, 5).value
                else:
                    fc["5"] =0
                if ws.cell(row, 6).value:
                    fc["6"]=ws.cell(row, 6).value
                else:
                    fc["6"] =0
                if ws.cell(row, 7).value:
                    fc["7"]=ws.cell(row, 7).value
                else:
                    fc["7"] =0
                if ws.cell(row, 8).value:
                    fc["8"]=ws.cell(row, 8).value
                else:
                    fc["8"] =0
                if ws.cell(row, 9).value:
                    fc["9"]=ws.cell(row, 9).value
                else:
                    fc["9"] =0
                if ws.cell(row, 10).value:
                    fc["10"]=ws.cell(row, 10).value
                else:
                    fc["10"] =0
                i=i+1
                data.append(fc)

    except Exception as e:
        print('Exception at sheet component')
        print(e)
    return data
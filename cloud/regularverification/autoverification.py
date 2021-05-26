import os,sys


from django.core.wsgi import get_wsgi_application
import paho.mqtt.client as mqtt

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from django.http import Http404,HttpResponse
from cloud import models
from datetime import datetime
import time
import json
import math
import paho.mqtt.client as mqtt
from cloud.process.RBI import fastCalulate as ReCalculate
from django.shortcuts import render, redirect, render_to_response
from cloud.regularverification.interpolation import Newton
# from ctypes import *
import requests
import json
class Verification:
    #lựa chọn dữ liệu định kì hoặc nôi suy. Điều kiện nội suy: số bản ghi >1 và người dùng chọn nội suy.
    #Điều kiện định kì: người dùng lựa chọn định kì. Có thể cấu hình định kì tại 4 vị trí: site( chọn cho tất
    # cả nhà máy cùng một cấu hình) / facility(Chọn cho tất cả equipment cùng một cấu hình), equipment(Chọn cho tất
    # component cùng một cấu hình) / component( chọn cho riêng thành phần thiết bị một cấu hình)
    def Regular(self,request):
    # def Regular(self):
        try:
            veri = models.VerificationPeriodically.objects.all()
            while True:
                for a in veri:
                    if a.componentid_id:
                        # print(a.componentid_id)
                        dem = 0
                        demgiay = 0
                        dem1 = 0
                        demgiay1 = 0
                        q = 'SELECT ID FROM rw_assessment where ComponentID = %s order by AssessmentDate desc limit 1'
                        Query = models.RwAssessment.objects.raw(q, [a.componentid_id])
                        for b in Query:
                            # print("test")
                            assdate = b.assessmentdate
                            # print(b.assessmentdate)
                            dem = assdate.year * 365 + assdate.month * 30 + assdate.day
                            demgiay = assdate.hour*3600 + assdate.minute*60 + assdate.second
                        date = datetime.now()
                        dem1 = date.year * 365 + date.month * 30 + date.day
                        # print("check",dem1,dem)
                        demgiay1 = date.hour*3600 + date.minute*60 + date.second
                        timer1 = (dem1-dem)*24*3600+(demgiay1-demgiay)
                        s = a.timer.split(":")
                        timer2 = int(s[0])*3600 + int(s[1])*60+int(s[2])
                        print(timer1,timer2)
                        # print("so sanh",timer1, timer2,4*60)
                        comp = models.ComponentMaster.objects.get(componentid=a.componentid_id)
                        if a.mode and timer1 >= timer2 and a.interpolation:
                            data = self.getdataVerification(componentID=a.componentid_id)
                            # print("lấy dữ liệu")
                            # print(data)
                            #------------------------
                            LOG_FILENAME = 'logging_rotatingfile_RBI.log'

                            # Set up a specific logger with our desired output level
                            UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
                            # print("check site")
                            # print(UserID)
                            Name = models.ZUser.objects.get(id=UserID).username
                            my_logger = logging.getLogger(Name)
                            my_logger.setLevel(logging.DEBUG)

                            # Add the log message handler to the logger
                            handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=52428800,
                                                                           backupCount=5)  # 50 MB = 52 428 800 bytes
                            f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
                            handler.setFormatter(f)
                            my_logger.addHandler(handler)
                            # Mess = "cuong"
                            # Log some messages
                            # for i in range(10):
                            my_logger.info('%s' % data)

                            # See what files are created
                            logfiles = glob.glob('%s*' % LOG_FILENAME)

                            # for filename in logfiles:
                                # print(filename)
                            #------------------------------
                            if comp.componenttypeid_id == 12 or comp.componenttypeid_id == 13 or comp.componenttypeid_id == 14 or comp.componenttypeid_id == 15:
                                # self.saveTank(data, a.componentid_id)
                                self.saveTank(data, a.componentid_id,request)
                            else:
                                # self.saveNormal(data, a.componentid_id)
                                self.saveNormal(data, a.componentid_id,request)
                        elif(a.mode and timer1 >= timer2 and not a.interpolation):
                            data = self.getdataVerification(componentID=a.componentid_id)
                            # print("lấy dữ liệu")
                            # print(data)
                            # ------------------------
                            LOG_FILENAME = 'logging_rotatingfile_RBI.log'

                            # Set up a specific logger with our desired output level
                            UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
                            # print("check site")
                            # print(UserID)
                            Name = models.ZUser.objects.get(id=UserID).username
                            my_logger = logging.getLogger(Name)
                            my_logger.setLevel(logging.DEBUG)

                            # Add the log message handler to the logger
                            handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=52428800,
                                                                           backupCount=5)  # 50 MB = 52 428 800 bytes
                            f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
                            handler.setFormatter(f)
                            my_logger.addHandler(handler)
                            # Mess = "cuong"
                            # Log some messages
                            # for i in range(10):
                            my_logger.info('%s' % data)

                            # See what files are created
                            logfiles = glob.glob('%s*' % LOG_FILENAME)

                            # for filename in logfiles:
                            #     print(filename)
                            # ------------------------------
                            if comp.componenttypeid_id == 12 or comp.componenttypeid_id == 13 or comp.componenttypeid_id == 14 or comp.componenttypeid_id == 15:
                                self.saveTankOnlyVeri(data, a.componentid_id, request)
                                # self.saveTank(data, a.componentid_id,request)
                            else:
                                print("go else")
                                self.saveNormalOnlyVeri(data, a.componentid_id,request)
                                # self.saveNormal(data, a.componentid_id,request)
                        else:
                            # data = self.getdataVerification(componentID=a.componentid_id)
                            # # ------------------------
                            # LOG_FILENAME = 'logging_rotatingfile_RBI.log'
                            #
                            # # Set up a specific logger with our desired output level
                            # UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
                            # # print("check site")
                            # # print(UserID)
                            # Name = models.ZUser.objects.get(id=UserID).username
                            # my_logger = logging.getLogger(Name)
                            # my_logger.setLevel(logging.DEBUG)
                            #
                            # # Add the log message handler to the logger
                            # handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=52428800,
                            #                                                backupCount=5)  # 50 MB = 52 428 800 bytes
                            # f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
                            # handler.setFormatter(f)
                            # my_logger.addHandler(handler)
                            # # Mess = "cuong"
                            # # Log some messages
                            # # for i in range(10):
                            # my_logger.info('%s' % data)
                            #
                            # # See what files are created
                            # logfiles = glob.glob('%s*' % LOG_FILENAME)
                            #
                            # for filename in logfiles:
                            #     print(filename)
                            # ------------------------------
                            print("đang chờ thời gian đến hạn kiểm tra định kì")
                time.sleep(30)
        except Exception as e:
            print(e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    def getdataVerification(self,componentID):
        try:
            data= []
            ACCESS_TOKEN = models.ZSensor.objects.filter(Componentid=componentID)[0].Token
            # print(ACCESS_TOKEN)
            # get_data = CDLL('/home/cortekr1/RBICloudv1/cloud/regularverification/datajson/get_data.so')
            # a = "993a75f0-bcd6-11ea-b4ad-47e5929eed78"  # voi a la ma id cua thiet bi
            # link = "/home/cortekr1/RBICloudv1/cloud/regularverification/datajson/data.js"
            # get_data.get_data(ACCESS_TOKEN, link)
            # with open('cloud/regularverification/datajson/data2.js') as json_file:
            #     data = json.load(json_file)
            # with open('/home/cortekr1/RBICloudv1/cloud/regularverification/datajson/data.js') as json_file:
            #     data = json.load(json_file)
            # sensor = models.ZSensor.objects.filter(Componentid=componentID)[0].idsensor
            # print (sensor)
            # package = models.PackageSensor(idsensor_id=sensor, package=data)
            # package.save()
            headers = {
                'Content-Type': 'application/json',
                'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlbmwubGFiNDExQGdtYWlsLmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiNzlkYjhhZTAtNmEyNy0xMWU4LTk2NjUtMTMyMDYzOTIxYjExIiwiZmlyc3ROYW1lIjoibGFiIiwibGFzdE5hbWUiOiI0MTEiLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiI3OWQ2MGNhMC02YTI3LTExZTgtOTY2NS0xMzIwNjM5MjFiMTEiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE2MTg4MDI1NTAsImV4cCI6MTYyMDYwMjU1MH0.D5GGD1gq4vI13wVgfUhPlfD7eKWjqqAS2Xlgww8U_hA3WHgZ71kwSwr3cLPYHim7VtGB06lkjRpJI0z5FtbAjg',
            }
            response = requests.get(
                'http://demo.thingsboard.io/api/plugins/telemetry/DEVICE/' + ACCESS_TOKEN + '/values/timeseries?keys=',
                headers=headers)
            return response.json()
        except Exception as e:
            print(e)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    def getDate(self,ComponentID):
        try:
            # print("getDate")
            insdate = models.RwAssessment.objects.filter(componentid_id=ComponentID)
            # for i in range(len(insdate)):
            # print(insdate[len(insdate)-1].assessmentdate)
            return insdate[len(insdate)-1].assessmentdate
        except Exception as e:
            print(e)
            return 0
    def saveTankOnlyVeri(self,data,ComponentID,request):
    # def saveTank(self,data,ComponentID,request):
        list = models.RwAssessment.objects.filter(componentid_id=ComponentID)
        # ass = list[list.count()-1]
        ass = list[0]
        rwequipment = models.RwEquipment.objects.get(id=ass.id)
        rwcomponent = models.RwComponent.objects.get(id=ass.id)
        rwstream = models.RwStream.objects.get(id=ass.id)
        excor = models.RwExtcorTemperature.objects.get(id=ass.id)
        rwcoat = models.RwCoating.objects.get(id=ass.id)
        rwmaterial = models.RwMaterial.objects.get(id=ass.id)
        comp = models.ComponentMaster.objects.get(componentid=ComponentID)
        Proposalname = "Re-verification Proposal " + str(datetime.now().strftime('%m-%d-%y,%H:%M:%S'))
        # Equipment
        try:
            PWHT = data['PWHT']
            # print("da luu")
        except:
            PWHT = rwequipment.pwht
        try:
            OnlineMonitoring = data['OnlineMonitoring']
        except:
            OnlineMonitoring = rwequipment.onlinemonitoring
        try:
            EquipmentVolumn = data['Equipment Volume'][0]['value']
        except:
            EquipmentVolumn = rwequipment.volume
        try:
            AdminControlUpset = data["AdminControlUpset"]
        except:
            AdminControlUpset = rwequipment.adminupsetmanagement
        try:
            CylicOper = data['CylicOper']
        except:
            CylicOper = rwequipment.cyclicoperation
        try:
            LOM = data['LOM']
        except:
            LOM = rwequipment.lineronlinemonitoring
        try:
            adjustSettlement = data['adjustSettlement']
        except:
            adjustSettlement = rwequipment.adjustmentsettle
        try:
            MFTF = data['MFTF']
        except:
            MFTF = rwequipment.materialexposedtoclext
        try:
            InterfaceSoilWater = data['InterfaceSoilWater']
        except:
            InterfaceSoilWater = rwequipment.interfacesoilwater
        try:
            ExternalEnvironment = data['ExternalEnvironment']
        except:
            ExternalEnvironment = rwequipment.externalenvironment
        try:
            Downtime = data['Downtime']
        except:
            Downtime = rwequipment.downtimeprotectionused
        try:
            SteamedOut = data['Steamed']
        except:
            SteamedOut = rwequipment.steamoutwaterflush
        try:
            HeatTraced = data['HeatTraced']
        except:
            HeatTraced = rwequipment.heattraced
        try:
            PresenceofSulphides = data['PresenceofSulphides']
        except:
            PresenceofSulphides = rwequipment.presencesulphideso2
        try:
            PresenceofSulphidesShutdown = data['PresenceofSulphidesShutdown']
        except:
            PresenceofSulphidesShutdown = rwequipment.presencesulphideso2shutdown
        try:
            ThermalHistory = data['ThermalHistory']
        except:
            ThermalHistory = rwequipment.thermalhistory
        try:
            PressurisationControlled = data['PressurisationControlled']
        except:
            PressurisationControlled = rwequipment.pressurisationcontrolled
        try:
            EquOper = data['lowestTemp']
        except:
            EquOper = rwequipment.yearlowestexptemp
        try:
            minTemp = data['Required Temperature'][0]['value']
        except:
            minTemp = rwequipment.minreqtemperaturepressurisation
        try:
            soiltype = data['soiltype']
        except:
            soiltype = rwequipment.typeofsoil
        try:
            EnvSensitivity = data['EnvSensitivity']
        except:
            EnvSensitivity = rwequipment.environmentsensitivity
        try:
            distance = data['distance_to_ground_water'][0]['value']
        except:
            distance = rwequipment.distancetogroundwater
        try:
            Highly = data['Highly']
        except:
            Highly = rwequipment.highlydeadleginsp
        try:
            tankIsMaintain = data['tankIsMaintain']
        except:
            tankIsMaintain = rwequipment.tankismaintained
        try:
            componentWelded = data['componentWelded']
        except:
            componentWelded = rwequipment.componentiswelded
        #Component
        try:
            confidencecr = data['confidencecr']
        except:
            confidencecr = rwcomponent.confidencecorrosionrate
        try:
            tankDiameter = float(data['Diameter'][0]['value'])
        except:
            tankDiameter = rwcomponent.nominaldiameter
        try:
            NorminalThickness = data['NorminalThickness']
        except:
            NorminalThickness = rwcomponent.nominalthickness
        try:
            CurrentThickness = data['current_thickness'][0]['value']
        except:
            CurrentThickness = rwcomponent.currentthickness
        try:
            MinReqThickness = data['MinReqThickness']
        except:
            MinReqThickness = rwcomponent.minreqthickness
        try:
            structuralthickness = data['structuralthickness']
        except:
            structuralthickness= rwcomponent.structuralthickness
        try:
            CurrentCorrosionRate = data['current_corrosion-rate'][0]['value']
        except:
            CurrentCorrosionRate= rwcomponent.currentcorrosionrate
        try:
            shellHieght = data['shellHieght']
        except:
            shellHieght = rwcomponent.shellheight
        try:
            DFDI = data['DFDI']
        except:
            DFDI = rwcomponent.damagefoundinspection
        try:
            PresenceCracks = data['PresenceCracks']
        except:
            PresenceCracks = rwcomponent.crackspresent
        try:
            MinStructuralThickness = data['MinStructuralThickness']
        except:
            MinStructuralThickness = rwcomponent.minstructuralthickness
        try:
            weldjointeff = data['weldjointeff']
        except:
            weldjointeff= rwcomponent.weldjointefficiency
        try:
            compvolume = data['Component Volume'][0]['value']
        except:
            compvolume= rwcomponent.componentvolume
        try:
            allowablestresss = data['allowablestresss']
        except:
            allowablestresss= rwcomponent.allowablestress
        try:
            complex = data['complex']
        except:
            complex = rwcomponent.complexityprotrusion
        try:
            MaxBrinell = data['MaxBrinell']
        except:
            MaxBrinell= rwcomponent.brinnelhardness
        try:
            Fabricatedsteel = data['Fabricatedsteel']
        except:
            Fabricatedsteel = rwcomponent.fabricatedsteel
        try:
            EquipmentSatisfied = data['EquipmentSatisfied']
        except:
            EquipmentSatisfied = rwcomponent.equipmentsatisfied
        try:
            NominalOperating = data['NominalOperating']
        except:
            NominalOperating = rwcomponent.nominaloperatingconditions
        try:
            Cetgreaterorequal = data['Cetgreaterorequal']
        except:
            Cetgreaterorequal = rwcomponent.cetgreaterorequal
        try:
            Cyclicservice = data['Cyclicservice']
        except:
            Cyclicservice = rwcomponent.cyclicservice
        try:
            equipmentCircuit = data['equipmentCircuit']
        except:
            equipmentCircuit = rwcomponent.equipmentcircuitshock
        try:
            BrittleFacture = data['BrittleFacture']
        except:
            BrittleFacture = rwcomponent.brittlefracturethickness
        try:
            severityVibration = data['severityVibration']
        except:
            severityVibration = rwcomponent.severityofvibration
        try:
            preventBarrier = data['preventBarrier']
        except:
            preventBarrier = rwcomponent.releasepreventionbarrier
        try:
            concreteFoundation = data['concreteFoundation']
        except:
            concreteFoundation = rwcomponent.concretefoundation
        #Stream
        try:
            maxOT = data['Max Temperature'][0]['value']
        except:
            maxOT = rwstream.maxoperatingtemperature
        try:
            maxOP = data['Max Pressure'][0]['value']
        except:
            maxOP = rwstream.maxoperatingpressure
        try:
            minOT = data['minOT']
        except:
            minOT = rwstream.minoperatingtemperature
        try:
            minOP = data['minOP']
        except:
            minOP = rwstream.minoperatingpressure
        try:
            H2Spressure = data['H2Spressure']
        except:
            H2Spressure = rwstream.h2spartialpressure
        try:
            criticalTemp = data['critical_exposure_temperature'][0]['value']
        except:
            criticalTemp = rwstream.criticalexposuretemperature
        try:
            fluid = data['fluid']
        except:
            fluid = rwstream.tankfluidname
        try:
            fluidHeight = data['fluidHeight']
        except:
            fluidHeight = rwstream.fluidheight
        try:
            fluidLeaveDike = data['fluidLeaveDike']
        except:
            fluidLeaveDike = rwstream.fluidleavedikepercent
        try:
            fluidOnsite = data['fluidOnsite']
        except:
            fluidOnsite = rwstream.fluidleavedikeremainonsitepercent
        try:
            fluidOffsite = data['fluidOffsite']
        except:
            fluidOffsite = rwstream.fluidgooffsitepercent
        try:
            naohConcent = data['naohConcent']
        except:
            naohConcent = rwstream.naohconcentration
        try:
            releasePercentToxic = data['releasePercentToxic']
        except:
            releasePercentToxic = rwstream.releasefluidpercenttoxic()
        try:
            chlorideIon = data['chlorideIon']
        except:
            chlorideIon = rwstream.chloride
        try:
            co3 = data['co3']
        except:
            co3 = rwstream.co3concentration
        try:
            h2sContent = data['h2sContent']
        except:
            h2sContent = rwstream.h2sinwater
        try:
            PHWater = data['pH of Water'][0]['value']
        except:
            PHWater = rwstream.waterph
        try:
            flowrate = data['Flow Rate'][0]['value']
        except:
            flowrate = rwstream.flowrate
        try:
            exposedAmine = data['exposed_to_acid_gas_treating_amine'][0]['value']
        except:
            exposedAmine = rwstream.exposedtogasamine
        try:
            amineSolution = data['amineSolution']
        except:
            amineSolution = rwstream.aminesolution
        try:
            exposureAmine = data['exposureAmine']
        except:
            exposureAmine = rwstream.exposuretoamine
        try:
            aqueosOP = data['aqueosOP']
        except:
            aqueosOP = rwstream.aqueousoperation
        try:
            environtH2S = data['environment_contains_H2S'][0]['value']
        except:
            environtH2S = rwstream.h2s
        try:
            aqueosShut = data['aqueosShut']
        except:
            aqueosShut = rwstream.aqueousshutdown
        try:
            cyanidesPresence = data['cyanidesPresence']
        except:
            cyanidesPresence = rwstream.cyanide
        try:
            presentHF = data['presentHF']
        except:
            presentHF = rwstream.hydrofluoric
        try:
            environtCaustic = data['environtCaustic']
        except:
            environtCaustic = rwstream.caustic
        try:
            processContainHydro = data['processContainHydro']
        except:
            processContainHydro = rwstream.hydrogen
        try:
            materialChlorineIntern = data['materialChlorineIntern']
        except:
            materialChlorineIntern = rwstream.materialexposedtoclint
        try:
            exposedSulfur = data['exposedSulfur']
        except:
            exposedSulfur = rwstream.exposedtosulphur
        #Operating
        try:
            OP1 = data['OP1']
        except:
            OP1 = excor.minus12tominus8
        try:
            OP2 = data['OP2']
        except:
            OP2 = excor.minus8toplus6
        try:
            OP3 = data['OP3']
        except:
            OP3 = excor.plus6toplus32
        try:
            OP4 = data['OP4']
        except:
            OP4 = excor.plus32toplus71
        try:
            OP5 = data['OP5']
        except:
            OP5 = excor.plus71toplus107()
        try:
            OP6 = data['OP6']
        except:
            OP6 = excor.plus107toplus121
        try:
            OP7 = data['OP7']
        except:
            OP7 = excor.plus121toplus135
        try:
            OP8 = data['OP8']
        except:
            OP8 = excor.plus135toplus162
        try:
            OP9 = data['OP9']
        except:
            OP9 = excor.plus162toplus176
        try:
            OP10 = data['OP10']
        except:
            OP10 = excor.morethanplus176
        #Coating
        try:
            internalcoating = data['internalcoating']
        except:
            internalcoating = rwcoat.internalcoating
        try:
            externalcoating = data['external_coating'][0]['value']
        except:
            externalcoating = rwcoat.externalcoating
        try:
            externalcoatingdate = rwcoat.externalcoatingdate.date().strftime('%Y-%m-%d')
        except:
            externalcoatingdate = datetime.now()
        try:
            externalcoatingquality = data['externalcoatingquality']
        except:
            externalcoatingquality = rwcoat.externalcoatingquality
        try:
            supportCoatingMaintain = data['supportCoatingMaintain']
        except:
            supportCoatingMaintain = rwcoat.supportconfignotallowcoatingmaint
        try:
            internalcladding = data['Internal Cladding'][0]['value']
        except:
            internalcladding = rwcoat.internalcladding
        try:
            cladCorrosion = data['Cladding Corrosion Rate'][0]['value']
        except:
            cladCorrosion = rwcoat.claddingcorrosionrate
        try:
            claddingthickness = float(data['Cladding Thickness'][0]['value']) # data of thingsboard
        except:
            claddingthickness = rwcoat.claddingthickness
        try:
            internallining = data['Internal Lining'][0]['value']
        except:
            internallining = rwcoat.internallining
        try:
            a = int(data['Internal Liner Type'][0]['value'])
            if (0<= a and a <=10):
                internallinertype = 'Organic - Low Quality'
            elif(10<a and a<=20):
                internallinertype = 'Organic - Medium  Quality'
            elif(20<a and a<=30):
                internallinertype = 'Organic - High Quality'
            elif(30<a and a<=40):
                internallinertype = 'Castable refractory'
            elif (40<a and a<=50):
                internallinertype = 'Strip lined alloy'
            elif(50< a and a<=60):
                internallinertype = 'Castable refractory severe condition'
            elif(60<a and a<= 70):
                internallinertype = 'Glass lined'
            elif(70<a and a<=80):
                internallinertype='Acid Brick'
            else:
                internallinertype = 'Fiberglass'
        except:
            internallinertype = rwcoat.internallinertype
        try:
            b = int(data['Internal_Liner_Condition'][0]['value'])
            if(0<=b and b<=20):
                internallinercondition = 'Good'
            elif(20<b and b<= 40):
                internallinercondition = 'Average'
            elif(40<b and b<=60):
                internallinercondition = 'Poor'
            else:
                internallinercondition = 'Unknown'
        except:
            internallinercondition = rwcoat.internallinercondition
        try:
            externalinsulation = externalinsulation
        except:
            externalinsulation = rwcoat.externalinsulation
        try:
            insulationcontainschloride = insulationcontainschloride
        except:
            insulationcontainschloride = rwcoat.insulationcontainschloride
        try:
            extInsulationType = extInsulationType
        except:
            extInsulationType = rwcoat.externalinsulationtype
        try:
            insulationCondition = insulationCondition
        except:
            insulationCondition = rwcoat.insulationcondition
        #Material
        try:
            materialname = data['materialname']
        except:
            materialname = "M1 "+str(list.count())
        try:
            designtemperature = data['designtemperature']
        except:
            designtemperature = rwmaterial.designtemperature
        try:
            mindesigntemperature = data['mindesigntemperature']
        except:
            mindesigntemperature = rwmaterial.mindesigntemperature
        try:
            designpressure = data['designpressure']
        except:
            designpressure = rwmaterial.designpressure
        try:
            refTemp = data['refTemp']
        except:
            refTemp = rwmaterial.referencetemperature
        try:
            corrosionAllow = data['corrosionAllow']
        except:
            corrosionAllow = rwmaterial.corrosionallowance
        try:
            carbonlowalloy = data['carbonlowalloy']
        except:
            carbonlowalloy = rwmaterial.carbonlowalloy
        try:
            austeniticSteel = data['austeniticSteel']
        except:
            austeniticSteel = rwmaterial.austenitic
        try:
            nickelAlloy = data['nickelAlloy']
        except:
            nickelAlloy = rwmaterial.nickelbased
        try:
            chromium = data['chromium']
        except:
            chromium = rwmaterial.chromemoreequal12
        try:
            sulfurContent = data['sulfurContent']
        except:
            sulfurContent = rwmaterial.sulfurcontent
        try:
            heatTreatment = data['heatTreatment']
        except:
            heatTreatment = rwmaterial.heattreatment
        try:
            materialPTA = data['materialPTA']
        except:
            materialPTA = rwmaterial.ispta
        try:
            PTAMaterialGrade = data['PTAMaterialGrade']
        except:
            PTAMaterialGrade = rwmaterial.ptamaterialcode
        try:
            materialCostFactor = data['materialCostFactor']
        except:
            materialCostFactor = rwmaterial.costfactor
        try:
            yieldstrength = data['yieldstrength']
        except:
            yieldstrength = rwmaterial.yieldstrength
        try:
            tensilestrength = data['tensilestrength']
        except:
            tensilestrength = rwmaterial.tensilestrength
            #rw ca input
        try:
            if str(data['fluid']) == "Gasoline":
                apiFluid = "C6-C8"
            elif str(data['fluid']) == "Light Diesel Oil":
                apiFluid = "C9-C12"
            elif str(data['fluid']) == "Heavy Diesel Oil":
                apiFluid = "C13-C16"
            elif str(data['fluid']) == "Fuel Oil" or str(data['fluid']) == "Crude Oil":
                apiFluid = "C17-C25"
            else:
                apiFluid = "C25+"
        except:
            apiFluid = "C6-C8"
        try:
            productioncost = data['productioncost']
        except:
            obj = Newton(ComponentID, "productioncost")
            productioncost = obj.calculate_Equipment()
        try:
            rwassessment = models.RwAssessment(equipmentid_id=comp.equipmentid_id, componentid_id=comp.componentid,
                                               assessmentdate=list[0].assessmentdate,commisstiondate=list[0].commisstiondate,
                                               riskanalysisperiod=36,
                                               isequipmentlinked=comp.isequipmentlinked,
                                               assessmentmethod="",
                                               proposalname=Proposalname)
            rwassessment.save()
            eq = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id)
            faci = models.Facility.objects.get(
                facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)

            rwequipment = models.RwEquipment(id=rwassessment, commissiondate=eq.commissiondate,
                                             adminupsetmanagement=AdminControlUpset,
                                             cyclicoperation=CylicOper, highlydeadleginsp=Highly,
                                             downtimeprotectionused=Downtime, steamoutwaterflush=SteamedOut,
                                             pwht=PWHT, heattraced=HeatTraced, distancetogroundwater=distance,
                                             interfacesoilwater=InterfaceSoilWater, typeofsoil=soiltype,
                                             pressurisationcontrolled=PressurisationControlled,
                                             minreqtemperaturepressurisation=minTemp,
                                             yearlowestexptemp=EquOper,
                                             materialexposedtoclext=MFTF,
                                             lineronlinemonitoring=LOM,
                                             presencesulphideso2=PresenceofSulphides,
                                             presencesulphideso2shutdown=PresenceofSulphidesShutdown,
                                             componentiswelded=componentWelded, tankismaintained=tankIsMaintain,
                                             adjustmentsettle=adjustSettlement,
                                             externalenvironment=ExternalEnvironment,
                                             environmentsensitivity=EnvSensitivity,
                                             onlinemonitoring=OnlineMonitoring, thermalhistory=ThermalHistory,
                                             managementfactor=faci.managementfactor,
                                             volume=EquipmentVolumn)
            rwequipment.save()
            rwcomponent = models.RwComponent(id=rwassessment, nominaldiameter=tankDiameter,
                                             allowablestress=allowablestresss,
                                             nominalthickness=NorminalThickness,
                                             currentthickness=CurrentThickness,
                                             minreqthickness=MinReqThickness,
                                             currentcorrosionrate=CurrentCorrosionRate,
                                             shellheight=shellHieght, damagefoundinspection=DFDI,
                                             crackspresent=PresenceCracks, componentvolume=compvolume,
                                             weldjointefficiency=weldjointeff,
                                             # trampelements=trampElements,
                                             brittlefracturethickness=BrittleFacture,
                                             releasepreventionbarrier=preventBarrier,
                                             concretefoundation=concreteFoundation,
                                             brinnelhardness=MaxBrinell,
                                             structuralthickness=structuralthickness,
                                             complexityprotrusion=complex,
                                             minstructuralthickness=MinStructuralThickness,
                                             severityofvibration=severityVibration,
                                             fabricatedsteel=Fabricatedsteel, equipmentsatisfied=EquipmentSatisfied,
                                             nominaloperatingconditions=NominalOperating,
                                             cetgreaterorequal=Cetgreaterorequal, cyclicservice=Cyclicservice,
                                             equipmentcircuitshock=equipmentCircuit,
                                             confidencecorrosionrate=confidencecr)
            rwcomponent.save()
            rwstream = models.RwStream(id=rwassessment, maxoperatingtemperature=maxOT,
                                       maxoperatingpressure=maxOP,
                                       minoperatingtemperature=minOT, minoperatingpressure=minOP,
                                       h2spartialpressure=H2Spressure,
                                       criticalexposuretemperature=criticalTemp,
                                       tankfluidname=fluid, fluidheight=fluidHeight,
                                       fluidleavedikepercent=fluidLeaveDike,
                                       fluidleavedikeremainonsitepercent=fluidOnsite,
                                       fluidgooffsitepercent=fluidOffsite,
                                       naohconcentration=naohConcent,
                                       releasefluidpercenttoxic=releasePercentToxic,
                                       chloride=chlorideIon, co3concentration=co3,
                                       h2sinwater=h2sContent,
                                       waterph=PHWater, exposedtogasamine=exposedAmine,
                                       aminesolution=amineSolution,
                                       exposuretoamine=exposureAmine, aqueousoperation=aqueosOP,
                                       h2s=environtH2S,
                                       aqueousshutdown=aqueosShut, cyanide=cyanidesPresence, hydrofluoric=presentHF,
                                       caustic=environtCaustic, hydrogen=processContainHydro,
                                       materialexposedtoclint=materialChlorineIntern,
                                       exposedtosulphur=exposedSulfur, flowrate=float(flowrate))
            rwstream.save()
            rwexcor = models.RwExtcorTemperature(id=rwassessment, minus12tominus8=OP1,
                                                 minus8toplus6=OP2,
                                                 plus6toplus32=OP3, plus32toplus71=OP4,
                                                 plus71toplus107=OP5,
                                                 plus107toplus121=OP6, plus121toplus135=OP7,
                                                 plus135toplus162=OP8, plus162toplus176=OP9,
                                                 morethanplus176=OP10)
            rwexcor.save()
            rwcoat = models.RwCoating(id=rwassessment, internalcoating=internalcoating, externalcoating=externalcoating,
                                      externalcoatingdate=externalcoatingdate,
                                      externalcoatingquality=externalcoatingquality,
                                      supportconfignotallowcoatingmaint=supportCoatingMaintain,
                                      internalcladding=internalcladding,
                                      claddingcorrosionrate=cladCorrosion, internallining=internallining,
                                      internallinertype=internallinertype,
                                      internallinercondition=internallinercondition,
                                      externalinsulation=externalinsulation,
                                      insulationcontainschloride=insulationcontainschloride,
                                      externalinsulationtype=extInsulationType,
                                      insulationcondition=insulationCondition,
                                      claddingthickness=claddingthickness)
            rwcoat.save()
            rwmaterial = models.RwMaterial(id=rwassessment, materialname=materialname,
                                           designtemperature=designtemperature,
                                           mindesigntemperature=mindesigntemperature,
                                           designpressure=designpressure,
                                           referencetemperature=refTemp,
                                           # allowablestress=data['allowStress'],
                                           corrosionallowance=corrosionAllow,
                                           carbonlowalloy=carbonlowalloy, austenitic=austeniticSteel,
                                           nickelbased=nickelAlloy,
                                           chromemoreequal12=chromium,
                                           sulfurcontent=sulfurContent, heattreatment=heatTreatment,
                                           ispta=materialPTA, ptamaterialcode=PTAMaterialGrade,
                                           costfactor=materialCostFactor, yieldstrength=yieldstrength,
                                           tensilestrength=tensilestrength)
            rwmaterial.save()
            rwinputca = models.RwInputCaTank(id=rwassessment, fluid_height=fluidHeight,
                                             shell_course_height=shellHieght,
                                             tank_diametter=tankDiameter, prevention_barrier=preventBarrier,
                                             environ_sensitivity=EnvSensitivity,
                                             p_lvdike=fluidLeaveDike, p_offsite=fluidOffsite,
                                             p_onsite=fluidOnsite, soil_type=soiltype,
                                             tank_fluid=fluid, api_fluid=apiFluid, sw=distance,
                                             productioncost=productioncost)
            rwinputca.save()
            ReCalculate.ReCalculate(rwassessment.id,request)
        except Exception as e:
            print(e)
    def saveNormalOnlyVeri(self,data,ComponentID,request):
        try:
    # def saveNormal(self,data,ComponentID,request):
            list = models.RwAssessment.objects.filter(componentid_id=ComponentID)
            # ass = list[list.count() - 1]
            ass = list[0]
            rwequipment = models.RwEquipment.objects.get(id=ass.id)
            rwcomponent = models.RwComponent.objects.get(id=ass.id)
            rwstream = models.RwStream.objects.get(id=ass.id)
            rwcoat = models.RwCoating.objects.get(id=ass.id)
            rwmaterial = models.RwMaterial.objects.get(id=ass.id)
            rw = models.RwInputCaLevel1.objects.filter(id=ass.id)
            print("count",rw.count())
            comp = models.ComponentMaster.objects.get(componentid=ComponentID)
            excor = models.RwExtcorTemperature.objects.get(id=ass.id)
            Proposalname = "Re-verification Proposal " + str(datetime.now().strftime('%m-%d-%y,%H:%M:%S'))
            try:
                AdminControlUpset = data["AdminControlUpset"]
            except:
                AdminControlUpset = rwequipment.adminupsetmanagement
            try:
                CylicOper = data['CylicOper']
            except:
                CylicOper = rwequipment.cyclicoperation
            try:
                containsDeadlegs = data['containsDeadlegs']
            except:
                containsDeadlegs = rwequipment.containsdeadlegs
            try:
                HighlyEffe = data['HighlyEffe']
            except:
                HighlyEffe = rwequipment.highlydeadleginsp
            try:
                Downtime = data['Downtime']
            except:
                Downtime = rwequipment.downtimeprotectionused
            try:
                ExternalEnvironment = data['ExternalEnvironment']
            except:
                ExternalEnvironment = rwequipment.externalenvironment
            try:
                HeatTraced = data['HeatTraced']
            except:
                HeatTraced = rwequipment.heattraced
            try:
                InterfaceSoilWater = data['InterfaceSoilWater']
            except:
                InterfaceSoilWater = rwequipment.interfacesoilwater
            try:
                LOM = data['LOM']
            except:
                LOM = rwequipment.lineronlinemonitoring
            try:
                MFTF = data['MFTF']
            except:
                MFTF = rwequipment.materialexposedtoclext
            try:
                minTemp = data['Required Temperature'][0]['value']
            except:
                minTemp = rwequipment.minreqtemperaturepressurisation
            try:
                OnlineMonitoring = data['OnlineMonitoring']
            except:
                OnlineMonitoring = rwequipment.onlinemonitoring
            try:
                PresenceofSulphides = data['PresenceofSulphides']
            except:
                PresenceofSulphides = rwequipment.presencesulphideso2
            try:
                PresenceofSulphidesShutdown = data['PresenceofSulphidesShutdown']
            except:
                PresenceofSulphidesShutdown = rwequipment.presencesulphideso2shutdown
            try:
                PressurisationControlled = data['PressurisationControlled']
            except:
                PressurisationControlled = rwequipment.pressurisationcontrolled
            try:
                PWHT = data['PWHT']
            except:
                PWHT = rwequipment.pwht
            try:
                SteamedOut = data['Steamed']
            except:
                SteamedOut = rwequipment.steamoutwaterflush
            try:
                ThermalHistory = data['ThermalHistory']
            except:
                ThermalHistory = rwequipment.thermalhistory
            try:
                EquOper = data['lowestTemp']
            except:
                EquOper = rwequipment.yearlowestexptemp
            try:
                EquipmentVolumn = data['Equipment Volume'][0]['value']
            except Exception as e:
                EquipmentVolumn = rwequipment.volume
            #Component
            try:
                nominaldiameter = float(data['Diameter'][0]['value'])
            except:
                nominaldiameter = rwcomponent.nominaldiameter
            try:
                NorminalThickness = data['NorminalThickness']
            except:
                NorminalThickness = rwcomponent.nominalthickness
            try:
                CurrentThickness = data['current_thickness'][0]['value']
            except:
                CurrentThickness = rwcomponent.currentthickness
            try:
                MinReqThickness = data['MinReqThickness']
            except:
                MinReqThickness = rwcomponent.minreqthickness
            try:
                CurrentCorrosionRate = data['current_corrosion-rate'][0]['value']
            except:
                CurrentCorrosionRate= rwcomponent.currentcorrosionrate
            try:
                branchdiameter = data['branchdiameter']
            except:
                branchdiameter = rwcomponent.branchdiameter
            try:
                branchjointtype = data['branchjointtype']
            except:
                branchjointtype = rwcomponent.branchjointtype
            try:
                MaxBrinell = data['MaxBrinell']
            except:
                MaxBrinell= rwcomponent.brinnelhardness
            try:
                HFICI = data['HFICI']
            except:
                HFICI= rwcomponent.highlyinjectioninsp
            try:
                ChemicalInjection = data['ChemicalInjection']
            except:
                ChemicalInjection= rwcomponent.chemicalinjection
            try:
                BrittleFacture = data['BrittleFacture']
            except:
                BrittleFacture = rwcomponent.brittlefracturethickness
            try:
                deltafatt = data['deltafatt']
            except:
                deltafatt = rwcomponent.deltafatt
            try:
                complex = data['complex']
            except:
                complex = rwcomponent.complexityprotrusion
            try:
                correctiveaction = data['correctiveaction']
            except:
                correctiveaction = rwcomponent.correctiveaction
            try:
                PresenceCracks = data['PresenceCracks']
            except:
                PresenceCracks = rwcomponent.crackspresent
            try:
                CylicLoad = data['CylicLoad']
            except:
                CylicLoad = rwcomponent.cyclicloadingwitin15_25m
            try:
                DFDI = data['DFDI']
            except:
                DFDI = rwcomponent.damagefoundinspection
            try:
                numberPipe = data['numberPipe']
            except:
                numberPipe = rwcomponent.numberpipefittings
            try:
                pipecondition = data['pipecondition']
            except:
                pipecondition = rwcomponent.pipecondition
            try:
                previousfailures = data['previousfailures']
            except:
                previousfailures = rwcomponent.previousfailures
            try:
                shakingamount = data['shakingamount']
            except:
                shakingamount = rwcomponent.shakingamount
            try:
                VASD = data['VASD']
            except:
                VASD = rwcomponent.shakingdetected
            try:
                shakingtime = data['shakingtime']
            except:
                shakingtime = rwcomponent.shakingtime
            try:
                hthadamage = data['hthadamage']
            except:
                hthadamage = rwcomponent.hthadamage
            try:
                weldjointeff = data['weldjointeff']
            except:
                weldjointeff= rwcomponent.weldjointefficiency
            try:
                allowablestresss = data['allowablestresss']
            except:
                allowablestresss= rwcomponent.allowablestress
            try:
                structuralthickness = data['structuralthickness']
            except:
                structuralthickness= rwcomponent.structuralthickness
            try:
                compvolume = data['Component Volume'][0]['value']
            except:
                compvolume= rwcomponent.componentvolume
            try:
                MinStructuralThickness = data['MinStructuralThickness']
            except:
                MinStructuralThickness = rwcomponent.minstructuralthickness
            try:
                Fabricatedsteel = data['Fabricatedsteel']
            except:
                Fabricatedsteel = rwcomponent.fabricatedsteel
            try:
                EquipmentSatisfied = data['EquipmentSatisfied']
            except:
                EquipmentSatisfied = rwcomponent.equipmentsatisfied
            try:
                NominalOperating = data['NominalOperating']
            except:
                NominalOperating = rwcomponent.nominaloperatingconditions
            try:
                Cetgreaterorequal = data['Cetgreaterorequal']
            except:
                Cetgreaterorequal = rwcomponent.cetgreaterorequal
            try:
                Cyclicservice = data['Cyclicservice']
            except:
                Cyclicservice = rwcomponent.cyclicservice
            try:
                equipmentCircuit = data['equipmentCircuit']
            except:
                equipmentCircuit = rwcomponent.equipmentcircuitshock
            try:
                confidencecr = data['confidencecr']
            except:
                confidencecr = rwcomponent.confidencecorrosionrate
            #Stream
            try:
                amineSolution = data['amineSolution']
            except:
                amineSolution = rwstream.aminesolution
            try:
                aqueosOP = data['aqueosOP']
            except:
                aqueosOP = rwstream.aqueousoperation
            try:
                aqueosShut = data['aqueosShut']
            except:
                aqueosShut = rwstream.aqueousshutdown
            try:
                toxicconstituent = data['toxicconstituent']
            except:
                toxicconstituent = rwstream.toxicconstituent
            try:
                environtCaustic = data['environtCaustic']
            except:
                environtCaustic = rwstream.caustic
            try:
                chlorideIon = data['chlorideIon']
            except:
                chlorideIon = rwstream.chloride
            try:
                co3 = data['co3']
            except:
                co3 = rwstream.co3concentration
            try:
                h2sinwater = data['h2sinwater']
            except:
                h2sinwater = rwstream.h2sinwater
            try:
                cyanidesPresence = data['cyanidesPresence']
            except:
                cyanidesPresence = rwstream.cyanide
            try:
                exposedAmine = data['exposed_to_acid_gas_treating_amine'][0]['value']
            except:
                exposedAmine = rwstream.exposedtogasamine
            try:
                exposedSulfur = data['exposedSulfur']
            except:
                exposedSulfur = rwstream.exposedtosulphur
            try:
                exposureAmine = data['exposureAmine']
            except:
                exposureAmine = rwstream.exposuretoamine
            try:
                environtH2S = data['environment_contains_H2S'][0]['value']
            except:
                environtH2S = rwstream.h2s
            try:
                processContainHydro = data['processContainHydro']
            except:
                processContainHydro = rwstream.hydrogen
            try:
                storagephase = data['storagephase']
            except:
                storagephase = rwstream.storagephase
            try:
                presentHF = data['presentHF']
            except:
                presentHF = rwstream.hydrofluoric
            try:
                materialChlorineIntern = data['materialChlorineIntern']
            except:
                materialChlorineIntern = rwstream.materialexposedtoclint
            try:
                maxOP = data['Max Pressure'][0]['value']
            except:
                maxOP = rwstream.maxoperatingpressure
            try:
                maxOT = data['Max Temperature'][0]['value']
            except:
                maxOT = rwstream.maxoperatingtemperature
            try:
                minOP = data['minOP']
            except:
                minOP = rwstream.minoperatingpressure
            try:
                minOT = rwstream.minoperatingtemperature
            except:
                minOT = rwstream.minoperatingtemperature
            try:
                criticalTemp = data['critical_exposure_temperature'][0]['value']
            except:
                criticalTemp = rwstream.criticalexposuretemperature
            try:
                naohConcent = data['naohConcent']
            except:
                naohConcent = rwstream.naohconcentration
            try:
                releasePercentToxic = data['releasePercentToxic']
            except:
                releasePercentToxic = rwstream.releasefluidpercenttoxic
            try:
                PHWater = data['pH of Water'][0]['value']
            except:
                PHWater = rwstream.waterph
            try:
                H2Spressure = data['H2Spressure']
            except:
                H2Spressure = rwstream.h2spartialpressure
            try:
                flowrate = data['Flow Rate'][0]['value']
            except:
                flowrate = rwstream.flowrate
            try:
                liquidlevel = data['liquidlevel']
            except:
                liquidlevel = rwstream.liquidlevel
            try:
                OP1 = data['OP1']
            except:
                OP1 = excor.minus12tominus8
            try:
                OP2 = data['OP2']
            except:
                OP2 = excor.minus8toplus6
            try:
                OP3 = data['OP3']
            except:
                OP3 = excor.plus6toplus32
            try:
                OP4 = data['OP4']
            except:
                OP4 = excor.plus32toplus71
            try:
                OP5 = data['OP5']
            except:
                OP5 = excor.plus71toplus107
            try:
                OP6 = data['OP6']
            except:
                OP6 = excor.plus107toplus121
            try:
                OP7 = data['OP7']
            except:
                OP7 = excor.plus121toplus135
            try:
                OP8 = data['OP8']
            except:
                OP8 = excor.plus135toplus162
            try:
                OP9 = data['OP9']
            except:
                OP9 = excor.plus162toplus176
            try:
                OP10 = data['OP10']
            except:
                OP10 = excor.morethanplus176
            #RwExtcorTemperature
            try:
                externalcoating = data['external_coating'][0]['value']
            except:
                externalcoating = rwcoat.externalcoating
            try:
                externalinsulation = data['externalinsulation']
            except:
                externalinsulation = rwcoat.externalinsulation
            try:
                internalcladding = data['Internal Cladding'][0]['value']
            except:
                internalcladding = rwcoat.internalcladding
            try:
                internalcoating = data['internalcoating']
            except:
                internalcoating = rwcoat.internalcoating
            try:
                internallining = data['Internal Lining'][0]['value']
            except:
                internallining = rwcoat.internallining
            try:
                externalcoatingdate = rwcoat.externalcoatingdate.date().strftime('%Y-%m-%d')
            except:
                externalcoatingdate = datetime.now()
            try:
                externalcoatingquality = data['externalcoatingquality']
            except:
                externalcoatingquality = rwcoat.externalcoatingquality
            try:
                extInsulationType = data['extInsulationType']
            except:
                extInsulationType = rwcoat.externalinsulationtype
            try:
                insulationCondition = data['insulationCondition']
            except:
                insulationCondition = rwcoat.insulationcondition
            try:
                insulationcontainschloride = data['insulationcontainschloride']
            except:
                insulationcontainschloride = rwcoat.insulationcontainschloride
            try:
                internallinercondition = data['internallinercondition']
            except:
                internallinercondition = rwcoat.internallinercondition
            try:
                internallinertype = data['Internal Liner Type'][0]['value']
            except:
                internallinertype = rwcoat.internallinertype
            try:
                cladCorrosion = data['Cladding Corrosion Rate'][0]['value']
            except:
                cladCorrosion = rwcoat.claddingcorrosionrate
            try:
                supportCoatingMaintain = data['supportCoatingMaintain']
            except:
                supportCoatingMaintain = rwcoat.supportconfignotallowcoatingmaint
            try:
                claddingthickness = float(data['Cladding Thickness'][0]['value'])
            except:
                claddingthickness = rwcoat.claddingthickness
            try:
                corrosionAllow = data['corrosionAllow']
            except:
                corrosionAllow = rwmaterial.corrosionallowance
            try:
                materialname = data['materialname']
            except:
                materialname = "M1 " + str(list.count())
            try:
                designpressure = data['designpressure']
            except:
                designpressure = rwmaterial.designpressure
            try:
                designtemperature = data['designtemperature']
            except:
                designtemperature = rwmaterial.mindesigntemperature
            try:
                mindesigntemperature = data['mindesigntemperature']
            except:
                mindesigntemperature = rwmaterial.mindesigntemperature
            try:
                SigmaPhase = data['SigmaPhase']
            except:
                SigmaPhase = rwmaterial.sigmaphase
            try:
                sulfurContent = data['sulfurContent']
            except:
                sulfurContent = rwmaterial.sulfurcontent
            try:
                heatTreatment = data['heatTreatment']
            except:
                heatTreatment = rwmaterial.heattreatment
            try:
                refTemp = data['refTemp']
            except:
                refTemp = rwmaterial.referencetemperature
            try:
                PTAMaterialGrade = data['PTAMaterialGrade']
            except:
                PTAMaterialGrade = rwmaterial.ptamaterialcode
            try:
                hthamaterialcode = data['hthamaterialcode']
            except:
                hthamaterialcode = rwmaterial.hthamaterialcode
            try:
                materialPTA = data['materialPTA']
            except:
                materialPTA = rwmaterial.ispta
            try:
                ishtha = data['ishtha']
            except:
                ishtha = rwmaterial.ishtha
            try:
                austeniticSteel = data['austeniticSteel']
            except:
                austeniticSteel = rwmaterial.austenitic
            try:
                temper = data['temper']
            except:
                temper = rwmaterial.temper
            try:
                carbonlowalloy = data['carbonlowalloy']
            except:
                carbonlowalloy = rwmaterial.carbonlowalloy
            try:
                nickelAlloy = data['nickelAlloy']
            except:
                nickelAlloy = rwmaterial.nickelbased
            try:
                chromium = data['chromium']
            except:
                chromium = rwmaterial.chromemoreequal12
            try:
                materialCostFactor = data['materialCostFactor']
            except:
                materialCostFactor = rwmaterial.costfactor
            try:
                yieldstrength = data['yieldstrength']
            except:
                yieldstrength = rwmaterial.yieldstrength
            try:
                tensilestrength = data['tensilestrength']
            except:
                tensilestrength = rwmaterial.tensilestrength
            try:
                rwassessment = models.RwAssessment(equipmentid_id=comp.equipmentid_id, componentid_id=comp.componentid,
                                                   assessmentdate=list[0].assessmentdate,commisstiondate=list[0].commisstiondate,
                                                   riskanalysisperiod=36,
                                                   isequipmentlinked=comp.isequipmentlinked,
                                                   assessmentmethod="",
                                                   proposalname=Proposalname)
                rwassessment.save()
                faci = models.Facility.objects.get(
                    facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
                rwequipment = models.RwEquipment(id=rwassessment, commissiondate=models.EquipmentMaster.objects.get(
                    equipmentid=comp.equipmentid_id).commissiondate,
                                                 adminupsetmanagement=AdminControlUpset, containsdeadlegs=containsDeadlegs,
                                                 cyclicoperation=CylicOper, highlydeadleginsp=HighlyEffe,
                                                 downtimeprotectionused=Downtime,
                                                 externalenvironment=ExternalEnvironment,
                                                 heattraced=HeatTraced, interfacesoilwater=InterfaceSoilWater,
                                                 lineronlinemonitoring=LOM,
                                                 materialexposedtoclext=MFTF,
                                                 minreqtemperaturepressurisation=minTemp,
                                                 onlinemonitoring=OnlineMonitoring,
                                                 presencesulphideso2=PresenceofSulphides,
                                                 presencesulphideso2shutdown=PresenceofSulphidesShutdown,
                                                 pressurisationcontrolled=PressurisationControlled, pwht=PWHT,
                                                 steamoutwaterflush=SteamedOut,
                                                 managementfactor=faci.managementfactor,
                                                 thermalhistory=ThermalHistory,
                                                 yearlowestexptemp=EquOper, volume=EquipmentVolumn)
                rwequipment.save()
                rwcomponent = models.RwComponent(id=rwassessment, nominaldiameter=nominaldiameter,
                                                 nominalthickness=NorminalThickness,
                                                 currentthickness=CurrentThickness,
                                                 minreqthickness=MinReqThickness, currentcorrosionrate=CurrentCorrosionRate,
                                                 branchdiameter=branchdiameter,
                                                 branchjointtype=branchjointtype,
                                                 brinnelhardness=MaxBrinell,
                                                 brittlefracturethickness=BrittleFacture,
                                                 deltafatt=deltafatt, chemicalinjection=ChemicalInjection,
                                                 highlyinjectioninsp=HFICI, complexityprotrusion=complex,
                                                 correctiveaction=correctiveaction, crackspresent=PresenceCracks,
                                                 cyclicloadingwitin15_25m=CylicLoad,
                                                 damagefoundinspection=DFDI,
                                                 numberpipefittings=numberPipe,
                                                 pipecondition=pipecondition,
                                                 previousfailures=previousfailures, shakingamount=shakingamount,
                                                 shakingdetected=VASD,
                                                 shakingtime=shakingtime,
                                                 weldjointefficiency=weldjointeff,
                                                 allowablestress=allowablestresss,
                                                 structuralthickness=structuralthickness,
                                                 componentvolume=compvolume, hthadamage=hthadamage,
                                                 minstructuralthickness=MinStructuralThickness,
                                                 fabricatedsteel=Fabricatedsteel, equipmentsatisfied=EquipmentSatisfied,
                                                 nominaloperatingconditions=NominalOperating,
                                                 cetgreaterorequal=Cetgreaterorequal, cyclicservice=Cyclicservice,
                                                 equipmentcircuitshock=equipmentCircuit,
                                                 confidencecorrosionrate=confidencecr)
                rwcomponent.save()
                rwstream = models.RwStream(id=rwassessment, aminesolution=amineSolution,
                                           aqueousoperation=aqueosOP,
                                           aqueousshutdown=aqueosShut, toxicconstituent=toxicconstituent,
                                           caustic=environtCaustic,
                                           chloride=chlorideIon, co3concentration=co3,
                                           cyanide=cyanidesPresence,
                                           exposedtogasamine=exposedAmine, exposedtosulphur=exposedSulfur,
                                           exposuretoamine=exposureAmine,
                                           h2s=environtH2S, h2sinwater=h2sinwater, hydrogen=processContainHydro,
                                           hydrofluoric=presentHF, materialexposedtoclint=materialChlorineIntern,
                                           maxoperatingpressure=maxOP,
                                           maxoperatingtemperature=float(maxOT),
                                           minoperatingpressure=float(minOP),
                                           minoperatingtemperature=minOT,
                                           criticalexposuretemperature=criticalTemp,
                                           naohconcentration=naohConcent,
                                           releasefluidpercenttoxic=float(releasePercentToxic),
                                           waterph=float(PHWater),
                                           h2spartialpressure=float(H2Spressure),
                                           flowrate=float(flowrate), liquidlevel=float(liquidlevel),
                                           storagephase=storagephase)
                rwstream.save()
                rwexcor = models.RwExtcorTemperature(id=rwassessment, minus12tominus8=OP1,
                                                     minus8toplus6=OP2,
                                                     plus6toplus32=OP3, plus32toplus71=OP4,
                                                     plus71toplus107=OP5,
                                                     plus107toplus121=OP6, plus121toplus135=OP7,
                                                     plus135toplus162=OP8, plus162toplus176=OP9,
                                                     morethanplus176=OP10)
                rwexcor.save()
                rwcoat = models.RwCoating(id=rwassessment, externalcoating=externalcoating,
                                          externalinsulation=externalinsulation,
                                          internalcladding=internalcladding, internalcoating=internalcoating,
                                          internallining=internallining,
                                          externalcoatingdate=externalcoatingdate,
                                          externalcoatingquality=externalcoatingquality,
                                          externalinsulationtype=extInsulationType,
                                          insulationcondition=insulationCondition,
                                          insulationcontainschloride=insulationcontainschloride,
                                          internallinercondition=internallinercondition,
                                          internallinertype=internallinertype,
                                          claddingcorrosionrate=cladCorrosion,
                                          supportconfignotallowcoatingmaint=supportCoatingMaintain,
                                          claddingthickness=claddingthickness)
                rwcoat.save()
                rwmaterial = models.RwMaterial(id=rwassessment, corrosionallowance=corrosionAllow,
                                               materialname=materialname,
                                               designpressure=designpressure,
                                               designtemperature=designtemperature,
                                               mindesigntemperature=mindesigntemperature,
                                               sigmaphase=SigmaPhase,
                                               sulfurcontent=sulfurContent, heattreatment=heatTreatment,
                                               referencetemperature=refTemp,
                                               ptamaterialcode=PTAMaterialGrade,
                                               hthamaterialcode=hthamaterialcode, ispta=materialPTA,
                                               ishtha=ishtha,
                                               austenitic=austeniticSteel, temper=temper, carbonlowalloy=carbonlowalloy,
                                               nickelbased=nickelAlloy, chromemoreequal12=chromium,
                                               costfactor=materialCostFactor,
                                               yieldstrength=yieldstrength, tensilestrength=tensilestrength)
                rwmaterial.save()
                rwcalevel1 = models.RwCaLevel1(id=rwassessment)
                rwcalevel1.save()
                if rw.count() == 1:
                    rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                    print("go test")
                    apiFluid = rwinputca.model_fluid
                    print(apiFluid)
                    release_duration = rwinputca.release_duration
                    detection_type = rwinputca.detection_type
                    isulation_type = rwinputca.isulation_type
                    mitigation_system = rwinputca.mitigation_system
                    equipment_cost = rwinputca.equipment_cost
                    injure_cost = rwinputca.injure_cost
                    evironment_cost = rwinputca.evironment_cost
                    personal_density = rwinputca.personal_density
                    mass_inventory = rwinputca.mass_inventory
                    production_cost = rwinputca.production_cost
                    toxic_fluid = rwinputca.toxic_fluid
                    print(toxic_fluid)
                    mass_component = rwinputca.mass_component
                    toxic_percent = rwinputca.toxic_percent
                    process_unit = rwinputca.process_unit
                    outage_multiplier = rwinputca.outage_multiplier
                    rwinputca = models.RwInputCaLevel1(id=rwassessment,api_fluid = apiFluid,
                                                       release_duration=release_duration,
                                                       detection_type=detection_type,
                                                       isulation_type=isulation_type,
                                                       mitigation_system=mitigation_system,
                                                       equipment_cost=equipment_cost, injure_cost=injure_cost,
                                                       evironment_cost=evironment_cost,
                                                       personal_density=personal_density,
                                                       material_cost=materialCostFactor,
                                                       production_cost=production_cost,
                                                       mass_inventory=mass_inventory,
                                                       mass_component=mass_component,
                                                       stored_pressure=float(minOP) * 6.895, stored_temp=minOT,
                                                       model_fluid=apiFluid, toxic_fluid=toxic_fluid,
                                                       toxic_percent=float(toxic_percent),
                                                       process_unit=float(process_unit),
                                                       outage_multiplier=float(outage_multiplier))
                    rwinputca.save()
                else:
                    print("go else")
                    try:
                        if str(data['fluid']) == "Gasoline":
                            apiFluid = "C6-C8"
                        elif str(data['fluid']) == "Light Diesel Oil":
                            apiFluid = "C9-C12"
                        elif str(data['fluid']) == "Heavy Diesel Oil":
                            apiFluid = "C13-C16"
                        elif str(data['fluid']) == "Fuel Oil" or str(data['fluid']) == "Crude Oil":
                            apiFluid = "C17-C25"
                        else:
                            apiFluid = "C25+"
                    except:
                        apiFluid = "C6-C8"
                    rwinputca = models.RwInputCaLevel1(id=rwassessment,api_fluid = apiFluid,
                                                       release_duration=0.0,
                                                       detection_type="",
                                                       isulation_type="",
                                                       mitigation_system="",
                                                       equipment_cost=0.0, injure_cost=0.0,
                                                       evironment_cost=0.0,
                                                       personal_density=0.0,
                                                       material_cost=0.0,
                                                       production_cost=0.0,
                                                       mass_inventory=0.0,
                                                       mass_component=0.0,
                                                       stored_pressure=float(minOP) * 6.895, stored_temp=minOT,
                                                       model_fluid="", toxic_fluid="",
                                                       toxic_percent=0.0,
                                                       process_unit=0.0,
                                                       outage_multiplier=0.0)
                    rwinputca.save()

                ReCalculate.ReCalculate(rwassessment.id,request)
            except Exception as e:
                print(e)
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    # def saveTank(self,data,ComponentID):
    def saveTank(self,data,ComponentID,request):
        list = models.RwAssessment.objects.filter(componentid_id=ComponentID)
        ass = list[list.count()-1]
        rwequipment = models.RwEquipment.objects.get(id=ass.id)
        rwcomponent = models.RwComponent.objects.get(id=ass.id)
        rwstream = models.RwStream.objects.get(id=ass.id)
        rwcoat = models.RwCoating.objects.get(id=ass.id)
        rwmaterial = models.RwMaterial.objects.get(id=ass.id)
        comp = models.ComponentMaster.objects.get(componentid=ComponentID)
        Proposalname = "Re-verification Proposal " + str(datetime.now().strftime('%m-%d-%y,%H:%M:%S'))
        # Equipment
        try:
            PWHT = data['PWHT']
            # print("da luu")
        except:
            PWHT = rwequipment.pwht
        try:
            OnlineMonitoring = data['OnlineMonitoring']
        except:
            OnlineMonitoring = rwequipment.onlinemonitoring
        try:
            EquipmentVolumn = data['Equipment Volume'][0]['value']
        except Exception as e:
            obj = Newton(ComponentID, "EquipmentVolumn")
            EquipmentVolumn = obj.calculate_Equipment()
        try:
            AdminControlUpset = data["AdminControlUpset"]
        except:
            AdminControlUpset = rwequipment.adminupsetmanagement
        try:
            CylicOper = data['CylicOper']
        except:
            CylicOper = rwequipment.cyclicoperation
        try:
            LOM = data['LOM']
        except:
            LOM = rwequipment.lineronlinemonitoring
        try:
            adjustSettlement = data['adjustSettlement']
        except:
            adjustSettlement = rwequipment.adjustmentsettle
        try:
            MFTF = data['MFTF']
        except:
            MFTF = rwequipment.materialexposedtoclext
        try:
            InterfaceSoilWater = data['InterfaceSoilWater']
        except:
            InterfaceSoilWater = rwequipment.interfacesoilwater
        try:
            ExternalEnvironment = data['ExternalEnvironment']
        except:
            ExternalEnvironment = rwequipment.externalenvironment
        try:
            Downtime = data['Downtime']
        except:
            Downtime = rwequipment.downtimeprotectionused
        try:
            SteamedOut = data['Steamed']
        except:
            SteamedOut = rwequipment.steamoutwaterflush
        try:
            HeatTraced = data['HeatTraced']
        except:
            HeatTraced = rwequipment.heattraced
        try:
            PresenceofSulphides = data['PresenceofSulphides']
        except:
            PresenceofSulphides = rwequipment.presencesulphideso2
        try:
            PresenceofSulphidesShutdown = data['PresenceofSulphidesShutdown']
        except:
            PresenceofSulphidesShutdown = rwequipment.presencesulphideso2shutdown
        try:
            ThermalHistory = data['ThermalHistory']
        except:
            ThermalHistory = rwequipment.thermalhistory
        try:
            PressurisationControlled = data['PressurisationControlled']
        except:
            PressurisationControlled = rwequipment.pressurisationcontrolled
        try:
            EquOper = data['lowestTemp']
        except:
            EquOper = rwequipment.yearlowestexptemp
        try:
            minTemp = data['Required Temperature'][0]['value']
        except:
            obj = Newton(ComponentID,"minTemp")
            minTemp = obj.calculate_Equipment()
        try:
            soiltype = data['soiltype']
        except:
            soiltype = rwequipment.typeofsoil
        try:
            EnvSensitivity = data['EnvSensitivity']
        except:
            EnvSensitivity = rwequipment.environmentsensitivity
        try:
            distance = data['distance_to_ground_water'][0]['value']
        except:
            obj = Newton(ComponentID, "distance")
            distance = obj.calculate_Equipment()
        try:
            Highly = data['Highly']
        except:
            Highly = rwequipment.highlydeadleginsp
        try:
            tankIsMaintain = data['tankIsMaintain']
        except:
            tankIsMaintain = rwequipment.tankismaintained
        try:
            componentWelded = data['componentWelded']
        except:
            componentWelded = rwequipment.componentiswelded
        #Component
        try:
            confidencecr = data['confidencecr']
        except:
            confidencecr = rwcomponent.confidencecorrosionrate
        try:
            tankDiameter = float(data['Diameter'][0]['value'])
        except:
            obj = Newton(ComponentID, "tankDiameter")
            tankDiameter = obj.calculate_Component()
        try:
            NorminalThickness = data['NorminalThickness']
        except:
            obj = Newton(ComponentID,"NorminalThickness")
            NorminalThickness = obj.calculate_Component()
        try:
            CurrentThickness = data['current_thickness'][0]['value']
        except:
            obj=Newton(ComponentID,"CurrentThickness")
            CurrentThickness = obj.calculate_Component()
        try:
            MinReqThickness = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            MinReqThickness = obj.calculate_Component()
        try:
            structuralthickness = data['structuralthickness']
        except:
            obj = Newton(ComponentID,"structuralthickness")
            structuralthickness= obj.calculate_Component()
        try:
            CurrentCorrosionRate = data['current_corrosion-rate'][0]['value']
        except:
            obj = Newton(ComponentID,"CurrentCorrosionRate")
            CurrentCorrosionRate= obj.calculate_Component()
        try:
            shellHieght = data['shellHieght']
        except:
            obj = Newton(ComponentID, "shellHieght")
            shellHieght = obj.calculate_Component()
        try:
            DFDI = data['DFDI']
        except:
            DFDI = rwcomponent.damagefoundinspection
        try:
            PresenceCracks = data['PresenceCracks']
        except:
            PresenceCracks = rwcomponent.crackspresent
        try:
            MinStructuralThickness = data['MinStructuralThickness']
        except:
            MinStructuralThickness = rwcomponent.minstructuralthickness
        try:
            weldjointeff = data['weldjointeff']
        except:
            obj = Newton(ComponentID,"weldjointeff")
            weldjointeff= obj.calculate_Component()
        try:
            compvolume = data['Component Volume'][0]['value']
        except:
            obj = Newton(ComponentID,"compvolume")
            compvolume= obj.calculate_Component()
        try:
            allowablestresss = data['allowablestresss']
        except:
            obj = Newton(ComponentID,"allowablestresss")
            allowablestresss= obj.calculate_Component()
        try:
            complex = data['complex']
        except:
            complex = rwcomponent.complexityprotrusion
        try:
            MaxBrinell = data['MaxBrinell']
        except:
            MaxBrinell= rwcomponent.brinnelhardness
        try:
            Fabricatedsteel = data['Fabricatedsteel']
        except:
            Fabricatedsteel = rwcomponent.fabricatedsteel
        try:
            EquipmentSatisfied = data['EquipmentSatisfied']
        except:
            EquipmentSatisfied = rwcomponent.equipmentsatisfied
        try:
            NominalOperating = data['NominalOperating']
        except:
            NominalOperating = rwcomponent.nominaloperatingconditions
        try:
            Cetgreaterorequal = data['Cetgreaterorequal']
        except:
            Cetgreaterorequal = rwcomponent.cetgreaterorequal
        try:
            Cyclicservice = data['Cyclicservice']
        except:
            Cyclicservice = rwcomponent.cyclicservice
        try:
            equipmentCircuit = data['equipmentCircuit']
        except:
            equipmentCircuit = rwcomponent.equipmentcircuitshock
        try:
            BrittleFacture = data['BrittleFacture']
        except:
            obj = Newton(ComponentID, "BrittleFacture")
            BrittleFacture = obj.calculate_Component()
        try:
            severityVibration = data['severityVibration']
        except:
            severityVibration = rwcomponent.severityofvibration
        try:
            preventBarrier = data['preventBarrier']
        except:
            preventBarrier = rwcomponent.releasepreventionbarrier
        try:
            concreteFoundation = data['concreteFoundation']
        except:
            concreteFoundation = rwcomponent.concretefoundation
        #Stream
        try:
            maxOT = data['Max Temperature'][0]['value']
        except:
            obj = Newton(ComponentID, "maxOT")
            maxOT = obj.calculate_Operating()
        try:
            maxOP = data['Max Pressure'][0]['value']
        except:
            obj = Newton(ComponentID, "maxOP")
            maxOP = obj.calculate_Operating()
        try:
            minOT = data['minOT']
        except:
            obj = Newton(ComponentID, "minOT")
            minOT = obj.calculate_Operating()
        try:
            minOP = data['minOP']
        except:
            obj = Newton(ComponentID, "minOP")
            minOP = obj.calculate_Operating()
        try:
            H2Spressure = data['H2Spressure']
        except:
            obj = Newton(ComponentID, "H2Spressure")
            H2Spressure = obj.calculate_Operating()
        try:
            criticalTemp = data['critical_exposure_temperature'][0]['value']
        except:
            obj = Newton(ComponentID, "criticalTemp")
            criticalTemp = obj.calculate_Operating()
        try:
            fluid = data['fluid']
        except:
            fluid = rwstream.tankfluidname
        try:
            fluidHeight = data['fluidHeight']
        except:
            obj = Newton(ComponentID, "fluidHeight")
            fluidHeight = obj.calculate_Operating()
        try:
            fluidLeaveDike = data['fluidLeaveDike']
        except:
            obj = Newton(ComponentID, "fluidLeaveDike")
            fluidLeaveDike = obj.calculate_Operating()
        try:
            fluidOnsite = data['fluidOnsite']
        except:
            obj = Newton(ComponentID, "fluidOnsite")
            fluidOnsite = obj.calculate_Operating()
        try:
            fluidOffsite = data['fluidOffsite']
        except:
            obj = Newton(ComponentID, "fluidOffsite")
            fluidOffsite = obj.calculate_Operating()
        try:
            naohConcent = data['naohConcent']
        except:
            obj = Newton(ComponentID, "naohConcent")
            naohConcent = obj.calculate_Operating()
        try:
            releasePercentToxic = data['releasePercentToxic']
        except:
            obj = Newton(ComponentID, "releasePercentToxic")
            releasePercentToxic = obj.calculate_Operating()
        try:
            chlorideIon = data['chlorideIon']
        except:
            obj = Newton(ComponentID, "chlorideIon")
            chlorideIon = obj.calculate_Operating()
        try:
            co3 = data['co3']
        except:
            obj = Newton(ComponentID, "co3")
            co3 = obj.calculate_Operating()
        try:
            h2sContent = data['h2sContent']
        except:
            obj = Newton(ComponentID, "h2sContent")
            h2sContent = obj.calculate_Operating()
        try:
            PHWater = data['pH of Water'][0]['value']
        except:
            obj = Newton(ComponentID, "PHWater")
            PHWater = obj.calculate_Operating()
        try:
            flowrate = data['Flow Rate'][0]['value']
        except:
            obj = Newton(ComponentID, "flowrate")
            flowrate = obj.calculate_Operating()
        try:
            exposedAmine = data['exposed_to_acid_gas_treating_amine'][0]['value']
        except:
            exposedAmine = rwstream.exposedtogasamine
        try:
            amineSolution = data['amineSolution']
        except:
            amineSolution = rwstream.aminesolution
        try:
            exposureAmine = data['exposureAmine']
        except:
            exposureAmine = rwstream.exposuretoamine
        try:
            aqueosOP = data['aqueosOP']
        except:
            aqueosOP = rwstream.aqueousoperation
        try:
            environtH2S = data['environment_contains_H2S'][0]['value']
        except:
            environtH2S = rwstream.h2s
        try:
            aqueosShut = data['aqueosShut']
        except:
            aqueosShut = rwstream.aqueousshutdown
        try:
            cyanidesPresence = data['cyanidesPresence']
        except:
            cyanidesPresence = rwstream.cyanide
        try:
            presentHF = data['presentHF']
        except:
            presentHF = rwstream.hydrofluoric
        try:
            environtCaustic = data['environtCaustic']
        except:
            environtCaustic = rwstream.caustic
        try:
            processContainHydro = data['processContainHydro']
        except:
            processContainHydro = rwstream.hydrogen
        try:
            materialChlorineIntern = data['materialChlorineIntern']
        except:
            materialChlorineIntern = rwstream.materialexposedtoclint
        try:
            exposedSulfur = data['exposedSulfur']
        except:
            exposedSulfur = rwstream.exposedtosulphur
        #Operating
        try:
            OP1 = data['OP1']
        except:
            obj = Newton(ComponentID, "OP1")
            OP1 = obj.calculate_RwExtcorTemperature()
        try:
            OP2 = data['OP2']
        except:
            obj = Newton(ComponentID, "OP2")
            OP2 = obj.calculate_RwExtcorTemperature()
        try:
            OP3 = data['OP3']
        except:
            obj = Newton(ComponentID, "OP3")
            OP3 = obj.calculate_RwExtcorTemperature()
        try:
            OP4 = data['OP4']
        except:
            obj = Newton(ComponentID, "OP4")
            OP4 = obj.calculate_RwExtcorTemperature()
        try:
            OP5 = data['OP5']
        except:
            obj = Newton(ComponentID, "OP5")
            OP5 = obj.calculate_RwExtcorTemperature()
        try:
            OP6 = data['OP6']
        except:
            obj = Newton(ComponentID, "OP6")
            OP6 = obj.calculate_RwExtcorTemperature()
        try:
            OP7 = data['OP7']
        except:
            obj = Newton(ComponentID, "OP7")
            OP7 = obj.calculate_RwExtcorTemperature()
        try:
            OP8 = data['OP8']
        except:
            obj = Newton(ComponentID, "OP8")
            OP8 = obj.calculate_RwExtcorTemperature()
        try:
            OP9 = data['OP9']
        except:
            obj = Newton(ComponentID, "OP9")
            OP9 = obj.calculate_RwExtcorTemperature()
        try:
            OP10 = data['OP10']
        except:
            obj = Newton(ComponentID, "OP10")
            OP10 = obj.calculate_RwExtcorTemperature()
        #Coating
        try:
            internalcoating = data['internalcoating']
        except:
            internalcoating = rwcoat.internalcoating
        try:
            externalcoating = data['external_coating'][0]['value']
        except:
            externalcoating = rwcoat.externalcoating
        try:
            externalcoatingdate = rwcoat.externalcoatingdate.date().strftime('%Y-%m-%d')
        except:
            externalcoatingdate = datetime.now()
        try:
            externalcoatingquality = data['externalcoatingquality']
        except:
            externalcoatingquality = rwcoat.externalcoatingquality
        try:
            supportCoatingMaintain = data['supportCoatingMaintain']
        except:
            supportCoatingMaintain = rwcoat.supportconfignotallowcoatingmaint
        try:
            internalcladding = data['Internal Cladding'][0]['value']
        except:
            internalcladding = rwcoat.internalcladding
        try:
            cladCorrosion = data['Cladding Corrosion Rate'][0]['value']
        except:
            obj = Newton(ComponentID, "cladCorrosion")
            cladCorrosion = obj.calculate_Equipment()
        try:
            claddingthickness = float(data['Cladding Thickness'][0]['value']) # data of thingsboard
        except:
            obj = Newton(ComponentID, "claddingthickness")
            claddingthickness = obj.calculate_Equipment()
        try:
            internallining = data['Internal Lining'][0]['value']
        except:
            internallining = rwcoat.internallining
        try:
            internallinertype = data['Internal Liner Type'][0]['value']
        except:
            internallinertype = rwcoat.internallinertype
        try:
            internallinercondition = internallinercondition
        except:
            internallinercondition = rwcoat.internallinercondition
        try:
            externalinsulation = externalinsulation
        except:
            externalinsulation = rwcoat.externalinsulation
        try:
            insulationcontainschloride = insulationcontainschloride
        except:
            insulationcontainschloride = rwcoat.insulationcontainschloride
        try:
            extInsulationType = extInsulationType
        except:
            extInsulationType = rwcoat.externalinsulationtype
        try:
            insulationCondition = insulationCondition
        except:
            insulationCondition = rwcoat.insulationcondition
        #Material
        try:
            materialname = data['materialname']
        except:
            materialname = "M1 "+str(list.count())
        try:
            designtemperature = data['designtemperature']
        except:
            obj = Newton(ComponentID, "designtemperature")
            designtemperature = obj.calculate_Material()
        try:
            mindesigntemperature = data['mindesigntemperature']
        except:
            obj = Newton(ComponentID, "mindesigntemperature")
            mindesigntemperature = obj.calculate_Material()
        try:
            designpressure = data['designpressure']
        except:
            obj = Newton(ComponentID, "designpressure")
            designpressure = obj.calculate_Material()
        try:
            refTemp = data['refTemp']
        except:
            obj = Newton(ComponentID, "refTemp")
            refTemp = obj.calculate_Material()
        try:
            corrosionAllow = data['corrosionAllow']
        except:
            obj = Newton(ComponentID, "corrosionAllow")
            corrosionAllow = obj.calculate_Material()
        try:
            carbonlowalloy = data['carbonlowalloy']
        except:
            carbonlowalloy = rwmaterial.carbonlowalloy
        try:
            austeniticSteel = data['austeniticSteel']
        except:
            austeniticSteel = rwmaterial.austenitic
        try:
            nickelAlloy = data['nickelAlloy']
        except:
            nickelAlloy = rwmaterial.nickelbased
        try:
            chromium = data['chromium']
        except:
            chromium = rwmaterial.chromemoreequal12
        try:
            sulfurContent = data['sulfurContent']
        except:
            sulfurContent = rwmaterial.sulfurcontent
        try:
            heatTreatment = data['heatTreatment']
        except:
            heatTreatment = rwmaterial.heattreatment
        try:
            materialPTA = data['materialPTA']
        except:
            materialPTA = rwmaterial.ispta
        try:
            PTAMaterialGrade = data['PTAMaterialGrade']
        except:
            PTAMaterialGrade = rwmaterial.ptamaterialcode
        try:
            materialCostFactor = data['materialCostFactor']
        except:
            obj = Newton(ComponentID, "materialCostFactor")
            materialCostFactor = obj.calculate_Material()
        try:
            yieldstrength = data['yieldstrength']
        except:
            obj = Newton(ComponentID, "yieldstrength")
            yieldstrength = obj.calculate_Material()
        try:
            tensilestrength = data['tensilestrength']
        except:
            obj = Newton(ComponentID, "tensilestrength")
            tensilestrength = obj.calculate_Material()
            #rw ca input
        try:
            if str(data['fluid']) == "Gasoline":
                apiFluid = "C6-C8"
            elif str(data['fluid']) == "Light Diesel Oil":
                apiFluid = "C9-C12"
            elif str(data['fluid']) == "Heavy Diesel Oil":
                apiFluid = "C13-C16"
            elif str(data['fluid']) == "Fuel Oil" or str(data['fluid']) == "Crude Oil":
                apiFluid = "C17-C25"
            else:
                apiFluid = "C25+"
        except:
            apiFluid = "C6-C8"
        try:
            productioncost = data['productioncost']
        except:
            obj = Newton(ComponentID, "productioncost")
            productioncost = obj.calculate_Equipment()
        try:
            rwassessment = models.RwAssessment(equipmentid_id=comp.equipmentid_id, componentid_id=comp.componentid,
                                               assessmentdate=datetime.now(),commisstiondate=datetime.now(),
                                               riskanalysisperiod=36,
                                               isequipmentlinked=comp.isequipmentlinked,
                                               assessmentmethod="",
                                               proposalname=Proposalname)
            rwassessment.save()
            eq = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id)
            faci = models.Facility.objects.get(
                facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)

            rwequipment = models.RwEquipment(id=rwassessment, commissiondate=eq.commissiondate,
                                             adminupsetmanagement=AdminControlUpset,
                                             cyclicoperation=CylicOper, highlydeadleginsp=Highly,
                                             downtimeprotectionused=Downtime, steamoutwaterflush=SteamedOut,
                                             pwht=PWHT, heattraced=HeatTraced, distancetogroundwater=distance,
                                             interfacesoilwater=InterfaceSoilWater, typeofsoil=soiltype,
                                             pressurisationcontrolled=PressurisationControlled,
                                             minreqtemperaturepressurisation=minTemp,
                                             yearlowestexptemp=EquOper,
                                             materialexposedtoclext=MFTF,
                                             lineronlinemonitoring=LOM,
                                             presencesulphideso2=PresenceofSulphides,
                                             presencesulphideso2shutdown=PresenceofSulphidesShutdown,
                                             componentiswelded=componentWelded, tankismaintained=tankIsMaintain,
                                             adjustmentsettle=adjustSettlement,
                                             externalenvironment=ExternalEnvironment,
                                             environmentsensitivity=EnvSensitivity,
                                             onlinemonitoring=OnlineMonitoring, thermalhistory=ThermalHistory,
                                             managementfactor=faci.managementfactor,
                                             volume=EquipmentVolumn)
            rwequipment.save()
            rwcomponent = models.RwComponent(id=rwassessment, nominaldiameter=tankDiameter,
                                             allowablestress=allowablestresss,
                                             nominalthickness=NorminalThickness,
                                             currentthickness=CurrentThickness,
                                             minreqthickness=MinReqThickness,
                                             currentcorrosionrate=CurrentCorrosionRate,
                                             shellheight=shellHieght, damagefoundinspection=DFDI,
                                             crackspresent=PresenceCracks, componentvolume=compvolume,
                                             weldjointefficiency=weldjointeff,
                                             # trampelements=trampElements,
                                             brittlefracturethickness=BrittleFacture,
                                             releasepreventionbarrier=preventBarrier,
                                             concretefoundation=concreteFoundation,
                                             brinnelhardness=MaxBrinell,
                                             structuralthickness=structuralthickness,
                                             complexityprotrusion=complex,
                                             minstructuralthickness=MinStructuralThickness,
                                             severityofvibration=severityVibration,
                                             fabricatedsteel=Fabricatedsteel, equipmentsatisfied=EquipmentSatisfied,
                                             nominaloperatingconditions=NominalOperating,
                                             cetgreaterorequal=Cetgreaterorequal, cyclicservice=Cyclicservice,
                                             equipmentcircuitshock=equipmentCircuit,
                                             confidencecorrosionrate=confidencecr)
            rwcomponent.save()
            rwstream = models.RwStream(id=rwassessment, maxoperatingtemperature=maxOT,
                                       maxoperatingpressure=maxOP,
                                       minoperatingtemperature=minOT, minoperatingpressure=minOP,
                                       h2spartialpressure=H2Spressure,
                                       criticalexposuretemperature=criticalTemp,
                                       tankfluidname=fluid, fluidheight=fluidHeight,
                                       fluidleavedikepercent=fluidLeaveDike,
                                       fluidleavedikeremainonsitepercent=fluidOnsite,
                                       fluidgooffsitepercent=fluidOffsite,
                                       naohconcentration=naohConcent,
                                       releasefluidpercenttoxic=releasePercentToxic,
                                       chloride=chlorideIon, co3concentration=co3,
                                       h2sinwater=h2sContent,
                                       waterph=PHWater, exposedtogasamine=exposedAmine,
                                       aminesolution=amineSolution,
                                       exposuretoamine=exposureAmine, aqueousoperation=aqueosOP,
                                       h2s=environtH2S,
                                       aqueousshutdown=aqueosShut, cyanide=cyanidesPresence, hydrofluoric=presentHF,
                                       caustic=environtCaustic, hydrogen=processContainHydro,
                                       materialexposedtoclint=materialChlorineIntern,
                                       exposedtosulphur=exposedSulfur, flowrate=float(flowrate))
            rwstream.save()
            rwexcor = models.RwExtcorTemperature(id=rwassessment, minus12tominus8=OP1,
                                                 minus8toplus6=OP2,
                                                 plus6toplus32=OP3, plus32toplus71=OP4,
                                                 plus71toplus107=OP5,
                                                 plus107toplus121=OP6, plus121toplus135=OP7,
                                                 plus135toplus162=OP8, plus162toplus176=OP9,
                                                 morethanplus176=OP10)
            rwexcor.save()
            rwcoat = models.RwCoating(id=rwassessment, internalcoating=internalcoating, externalcoating=externalcoating,
                                      externalcoatingdate=externalcoatingdate,
                                      externalcoatingquality=externalcoatingquality,
                                      supportconfignotallowcoatingmaint=supportCoatingMaintain,
                                      internalcladding=internalcladding,
                                      claddingcorrosionrate=cladCorrosion, internallining=internallining,
                                      internallinertype=internallinertype,
                                      internallinercondition=internallinercondition,
                                      externalinsulation=externalinsulation,
                                      insulationcontainschloride=insulationcontainschloride,
                                      externalinsulationtype=extInsulationType,
                                      insulationcondition=insulationCondition,
                                      claddingthickness=claddingthickness)
            rwcoat.save()
            rwmaterial = models.RwMaterial(id=rwassessment, materialname=materialname,
                                           designtemperature=designtemperature,
                                           mindesigntemperature=mindesigntemperature,
                                           designpressure=designpressure,
                                           referencetemperature=refTemp,
                                           # allowablestress=data['allowStress'],
                                           corrosionallowance=corrosionAllow,
                                           carbonlowalloy=carbonlowalloy, austenitic=austeniticSteel,
                                           nickelbased=nickelAlloy,
                                           chromemoreequal12=chromium,
                                           sulfurcontent=sulfurContent, heattreatment=heatTreatment,
                                           ispta=materialPTA, ptamaterialcode=PTAMaterialGrade,
                                           costfactor=materialCostFactor, yieldstrength=yieldstrength,
                                           tensilestrength=tensilestrength)
            rwmaterial.save()
            rwinputca = models.RwInputCaTank(id=rwassessment, fluid_height=fluidHeight,
                                             shell_course_height=shellHieght,
                                             tank_diametter=tankDiameter, prevention_barrier=preventBarrier,
                                             environ_sensitivity=EnvSensitivity,
                                             p_lvdike=fluidLeaveDike, p_offsite=fluidOffsite,
                                             p_onsite=fluidOnsite, soil_type=soiltype,
                                             tank_fluid=fluid, api_fluid=apiFluid, sw=distance,
                                             productioncost=productioncost)
            rwinputca.save()
            ReCalculate.ReCalculate(rwassessment.id,request)
        except Exception as e:
            print(e)
    # def saveNormal(self,data,ComponentID):
    def saveNormal(self,data,ComponentID,request):
        list = models.RwAssessment.objects.filter(componentid_id=ComponentID)
        ass = list[list.count() - 1]
        rwequipment = models.RwEquipment.objects.get(id=ass.id)
        rwcomponent = models.RwComponent.objects.get(id=ass.id)
        rwstream = models.RwStream.objects.get(id=ass.id)
        rwcoat = models.RwCoating.objects.get(id=ass.id)
        rwmaterial = models.RwMaterial.objects.get(id=ass.id)
        rw = models.RwInputCaLevel1.objects.filter(id=ass.id)
        comp = models.ComponentMaster.objects.get(componentid=ComponentID)
        Proposalname = "Re-verification Proposal " + str(datetime.now().strftime('%m-%d-%y,%H:%M:%S'))
        try:
            AdminControlUpset = data["AdminControlUpset"]
        except:
            AdminControlUpset = rwequipment.adminupsetmanagement
        try:
            CylicOper = data['CylicOper']
        except:
            CylicOper = rwequipment.cyclicoperation
        try:
            containsDeadlegs = data['containsDeadlegs']
        except:
            containsDeadlegs = rwequipment.containsdeadlegs
        try:
            HighlyEffe = data['HighlyEffe']
        except:
            HighlyEffe = rwequipment.highlydeadleginsp
        try:
            Downtime = data['Downtime']
        except:
            Downtime = rwequipment.downtimeprotectionused
        try:
            ExternalEnvironment = data['ExternalEnvironment']
        except:
            ExternalEnvironment = rwequipment.externalenvironment
        try:
            HeatTraced = data['HeatTraced']
        except:
            HeatTraced = rwequipment.heattraced
        try:
            InterfaceSoilWater = data['InterfaceSoilWater']
        except:
            InterfaceSoilWater = rwequipment.interfacesoilwater
        try:
            LOM = data['LOM']
        except:
            LOM = rwequipment.lineronlinemonitoring
        try:
            MFTF = data['MFTF']
        except:
            MFTF = rwequipment.materialexposedtoclext
        try:
            minTemp = data['Required Temperature'][0]['value']
        except:
            obj = Newton(ComponentID,"minTemp")
            minTemp = obj.calculate_Equipment()
        try:
            OnlineMonitoring = data['OnlineMonitoring']
        except:
            OnlineMonitoring = rwequipment.onlinemonitoring
        try:
            PresenceofSulphides = data['PresenceofSulphides']
        except:
            PresenceofSulphides = rwequipment.presencesulphideso2
        try:
            PresenceofSulphidesShutdown = data['PresenceofSulphidesShutdown']
        except:
            PresenceofSulphidesShutdown = rwequipment.presencesulphideso2shutdown
        try:
            PressurisationControlled = data['PressurisationControlled']
        except:
            PressurisationControlled = rwequipment.pressurisationcontrolled
        try:
            PWHT = data['PWHT']
        except:
            PWHT = rwequipment.pwht
        try:
            SteamedOut = data['Steamed']
        except:
            SteamedOut = rwequipment.steamoutwaterflush
        try:
            ThermalHistory = data['ThermalHistory']
        except:
            ThermalHistory = rwequipment.thermalhistory
        try:
            EquOper = data['lowestTemp']
        except:
            EquOper = rwequipment.yearlowestexptemp
        try:
            EquipmentVolumn = data['Equipment Volume'][0]['value']
        except Exception as e:
            obj = Newton(ComponentID, "EquipmentVolumn")
            EquipmentVolumn = obj.calculate_Equipment()
        #Component
        try:
            nominaldiameter = float(data['Diameter'][0]['value'])
        except:
            obj = Newton(ComponentID, "nominaldiameter")
            nominaldiameter = obj.calculate_Component()
        try:
            NorminalThickness = data['NorminalThickness']
        except:
            obj = Newton(ComponentID,"NorminalThickness")
            NorminalThickness = obj.calculate_Component()
        try:
            CurrentThickness = data['current_thickness'][0]['value']
        except:
            obj=Newton(ComponentID,"CurrentThickness")
            CurrentThickness = obj.calculate_Component()
        try:
            MinReqThickness = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            MinReqThickness = obj.calculate_Component()
        try:
            CurrentCorrosionRate = data['current_corrosion-rate'][0]['value']
        except:
            obj = Newton(ComponentID,"CurrentCorrosionRate")
            CurrentCorrosionRate= obj.calculate_Component()
        try:
            branchdiameter = data['branchdiameter']
        except:
            branchdiameter = rwcomponent.branchdiameter
        try:
            branchjointtype = data['branchjointtype']
        except:
            branchjointtype = rwcomponent.branchjointtype
        try:
            MaxBrinell = data['MaxBrinell']
        except:
            MaxBrinell= rwcomponent.brinnelhardness
        try:
            HFICI = data['HFICI']
        except:
            HFICI= rwcomponent.highlyinjectioninsp
        try:
            ChemicalInjection = data['ChemicalInjection']
        except:
            ChemicalInjection= rwcomponent.chemicalinjection
        try:
            BrittleFacture = data['BrittleFacture']
        except:
            obj = Newton(ComponentID, "BrittleFacture")
            BrittleFacture = obj.calculate_Component()
        try:
            deltafatt = data['deltafatt']
        except:
            obj = Newton(ComponentID, "deltafatt")
            deltafatt = obj.calculate_Component()
        try:
            complex = data['complex']
        except:
            complex = rwcomponent.complexityprotrusion
        try:
            correctiveaction = data['correctiveaction']
        except:
            correctiveaction = rwcomponent.correctiveaction
        try:
            PresenceCracks = data['PresenceCracks']
        except:
            PresenceCracks = rwcomponent.crackspresent
        try:
            CylicLoad = data['CylicLoad']
        except:
            CylicLoad = rwcomponent.cyclicloadingwitin15_25m
        try:
            DFDI = data['DFDI']
        except:
            DFDI = rwcomponent.damagefoundinspection
        try:
            numberPipe = data['numberPipe']
        except:
            numberPipe = rwcomponent.numberpipefittings
        try:
            pipecondition = data['pipecondition']
        except:
            pipecondition = rwcomponent.pipecondition
        try:
            previousfailures = data['previousfailures']
        except:
            previousfailures = rwcomponent.previousfailures
        try:
            shakingamount = data['shakingamount']
        except:
            shakingamount = rwcomponent.shakingamount
        try:
            VASD = data['VASD']
        except:
            VASD = rwcomponent.shakingdetected
        try:
            shakingtime = data['shakingtime']
        except:
            shakingtime = rwcomponent.shakingtime
        try:
            hthadamage = data['hthadamage']
        except:
            hthadamage = rwcomponent.hthadamage
        try:
            weldjointeff = data['weldjointeff']
        except:
            obj = Newton(ComponentID,"weldjointeff")
            weldjointeff= obj.calculate_Component()
        try:
            allowablestresss = data['allowablestresss']
        except:
            obj = Newton(ComponentID,"allowablestresss")
            allowablestresss= obj.calculate_Component()
        try:
            structuralthickness = data['structuralthickness']
        except:
            obj = Newton(ComponentID,"structuralthickness")
            structuralthickness= obj.calculate_Component()
        try:
            compvolume = data['Component Volume'][0]['value']
        except:
            obj = Newton(ComponentID,"compvolume")
            compvolume= obj.calculate_Component()
        try:
            MinStructuralThickness = data['MinStructuralThickness']
        except:
            MinStructuralThickness = rwcomponent.minstructuralthickness
        try:
            Fabricatedsteel = data['Fabricatedsteel']
        except:
            Fabricatedsteel = rwcomponent.fabricatedsteel
        try:
            EquipmentSatisfied = data['EquipmentSatisfied']
        except:
            EquipmentSatisfied = rwcomponent.equipmentsatisfied
        try:
            NominalOperating = data['NominalOperating']
        except:
            NominalOperating = rwcomponent.nominaloperatingconditions
        try:
            Cetgreaterorequal = data['Cetgreaterorequal']
        except:
            Cetgreaterorequal = rwcomponent.cetgreaterorequal
        try:
            Cyclicservice = data['Cyclicservice']
        except:
            Cyclicservice = rwcomponent.cyclicservice
        try:
            equipmentCircuit = data['equipmentCircuit']
        except:
            equipmentCircuit = rwcomponent.equipmentcircuitshock
        try:
            confidencecr = data['confidencecr']
        except:
            confidencecr = rwcomponent.confidencecorrosionrate
        #Stream
        try:
            amineSolution = data['amineSolution']
        except:
            amineSolution = rwstream.aminesolution
        try:
            aqueosOP = data['aqueosOP']
        except:
            aqueosOP = rwstream.aqueousoperation
        try:
            aqueosShut = data['aqueosShut']
        except:
            aqueosShut = rwstream.aqueousshutdown
        try:
            toxicconstituent = data['toxicconstituent']
        except:
            toxicconstituent = rwstream.toxicconstituent
        try:
            environtCaustic = data['environtCaustic']
        except:
            environtCaustic = rwstream.caustic
        try:
            chlorideIon = data['chlorideIon']
        except:
            obj = Newton(ComponentID, "chlorideIon")
            chlorideIon = obj.calculate_Operating()
        try:
            co3 = data['co3']
        except:
            obj = Newton(ComponentID, "co3")
            co3 = obj.calculate_Operating()
        try:
            h2sinwater = data['h2sinwater']
        except:
            obj = Newton(ComponentID, "h2sinwater")
            h2sinwater = obj.calculate_Operating()
        try:
            cyanidesPresence = data['cyanidesPresence']
        except:
            cyanidesPresence = rwstream.cyanide
        try:
            exposedAmine = data['exposed_to_acid_gas_treating_amine'][0]['value']
        except:
            exposedAmine = rwstream.exposedtogasamine
        try:
            exposedSulfur = data['exposedSulfur']
        except:
            exposedSulfur = rwstream.exposedtosulphur
        try:
            exposureAmine = data['exposureAmine']
        except:
            exposureAmine = rwstream.exposuretoamine
        try:
            environtH2S = data['environment_contains_H2S'][0]['value']
        except:
            environtH2S = rwstream.h2s
        try:
            processContainHydro = data['processContainHydro']
        except:
            processContainHydro = rwstream.hydrogen
        try:
            storagephase = data['storagephase']
        except:
            storagephase = rwstream.storagephase
        try:
            presentHF = data['presentHF']
        except:
            presentHF = rwstream.hydrofluoric
        try:
            materialChlorineIntern = data['materialChlorineIntern']
        except:
            materialChlorineIntern = rwstream.materialexposedtoclint
        try:
            maxOP = data['Max Pressure'][0]['value']
        except:
            obj = Newton(ComponentID, "maxOP")
            maxOP = obj.calculate_Operating()
        try:
            maxOT = data['Max Temperature'][0]['value']
        except:
            obj = Newton(ComponentID, "maxOT")
            maxOT = obj.calculate_Operating()
        try:
            minOP = data['minOP']
        except:
            obj = Newton(ComponentID, "minOP")
            minOP = obj.calculate_Operating()
        try:
            minOT = data['minOT']
        except:
            obj = Newton(ComponentID, "minOT")
            minOT = obj.calculate_Operating()
        try:
            criticalTemp = data['critical_exposure_temperature'][0]['value']
        except:
            obj = Newton(ComponentID, "criticalTemp")
            criticalTemp = obj.calculate_Operating()
        try:
            naohConcent = data['naohConcent']
        except:
            obj = Newton(ComponentID, "naohConcent")
            naohConcent = obj.calculate_Operating()
        try:
            releasePercentToxic = data['releasePercentToxic']
        except:
            obj = Newton(ComponentID, "releasePercentToxic")
            releasePercentToxic = obj.calculate_Operating()
        try:
            PHWater = data['pH of Water'][0]['value']
        except:
            obj = Newton(ComponentID, "PHWater")
            PHWater = obj.calculate_Operating()
        try:
            H2Spressure = data['H2Spressure']
        except:
            obj = Newton(ComponentID, "H2Spressure")
            H2Spressure = obj.calculate_Operating()
        try:
            flowrate = data['Flow Rate'][0]['value']
        except:
            obj = Newton(ComponentID, "flowrate")
            flowrate = obj.calculate_Operating()
        try:
            liquidlevel = data['liquidlevel']
        except:
            obj = Newton(ComponentID, "liquidlevel")
            liquidlevel = obj.calculate_Operating()
        try:
            OP1 = data['OP1']
        except:
            obj = Newton(ComponentID, "OP1")
            OP1 = obj.calculate_RwExtcorTemperature()
        try:
            OP2 = data['OP2']
        except:
            obj = Newton(ComponentID, "OP2")
            OP2 = obj.calculate_RwExtcorTemperature()
        try:
            OP3 = data['OP3']
        except:
            obj = Newton(ComponentID, "OP3")
            OP3 = obj.calculate_RwExtcorTemperature()
        try:
            OP4 = data['OP4']
        except:
            obj = Newton(ComponentID, "OP4")
            OP4 = obj.calculate_RwExtcorTemperature()
        try:
            OP5 = data['OP5']
        except:
            obj = Newton(ComponentID, "OP5")
            OP5 = obj.calculate_RwExtcorTemperature()
        try:
            OP6 = data['OP6']
        except:
            obj = Newton(ComponentID, "OP6")
            OP6 = obj.calculate_RwExtcorTemperature()
        try:
            OP7 = data['OP7']
        except:
            obj = Newton(ComponentID, "OP7")
            OP7 = obj.calculate_RwExtcorTemperature()
        try:
            OP8 = data['OP8']
        except:
            obj = Newton(ComponentID, "OP8")
            OP8 = obj.calculate_RwExtcorTemperature()
        try:
            OP9 = data['OP9']
        except:
            obj = Newton(ComponentID, "OP9")
            OP9 = obj.calculate_RwExtcorTemperature()
        try:
            OP10 = data['OP10']
        except:
            obj = Newton(ComponentID, "OP10")
            OP10 = obj.calculate_RwExtcorTemperature()
        #RwExtcorTemperature
        try:
            externalcoating = data['external_coating'][0]['value']
        except:
            externalcoating = rwcoat.externalcoating
        try:
            externalinsulation = data['externalinsulation']
        except:
            externalinsulation = rwcoat.externalinsulation
        try:
            internalcladding = data['Internal Cladding'][0]['value']
        except:
            internalcladding = rwcoat.internalcladding
        try:
            internalcoating = data['internalcoating']
        except:
            internalcoating = rwcoat.internalcoating
        try:
            internallining = data['Internal Lining'][0]['value']
        except:
            internallining = rwcoat.internallining
        try:
            externalcoatingdate = rwcoat.externalcoatingdate.date().strftime('%Y-%m-%d')
        except:
            externalcoatingdate = datetime.now()
        try:
            externalcoatingquality = data['externalcoatingquality']
        except:
            externalcoatingquality = rwcoat.externalcoatingquality
        try:
            extInsulationType = data['extInsulationType']
        except:
            extInsulationType = rwcoat.externalinsulationtype
        try:
            insulationCondition = data['insulationCondition']
        except:
            insulationCondition = rwcoat.insulationcondition
        try:
            insulationcontainschloride = data['insulationcontainschloride']
        except:
            insulationcontainschloride = rwcoat.insulationcontainschloride
        try:
            # if  0<=data['Internal Liner Condition'][0]['value'] and data['Internal Liner Condition'][0]['value']<=10:
            internallinercondition = data['Internal Liner Condition']
        except:
            internallinercondition = rwcoat.internallinercondition
        try:
            internallinertype = data['Internal Liner Type'][0]['value']
        except:
            internallinertype = rwcoat.internallinertype
        try:
            cladCorrosion = data['Cladding Corrosion Rate'][0]['value']
        except:
            obj = Newton(ComponentID, "cladCorrosion")
            cladCorrosion = obj.calculate_Equipment()
        try:
            supportCoatingMaintain = data['supportCoatingMaintain']
        except:
            supportCoatingMaintain = rwcoat.supportconfignotallowcoatingmaint
        try:
            claddingthickness = float(data['Cladding Thickness'][0]['value'])
        except:
            obj = Newton(ComponentID, "claddingthickness")
            claddingthickness = obj.calculate_Equipment()
        try:
            corrosionAllow = data['corrosionAllow']
        except:
            obj = Newton(ComponentID, "corrosionAllow")
            corrosionAllow = obj.calculate_Material()
        try:
            materialname = data['materialname']
        except:
            materialname = "M1 " + str(list.count())
        try:
            designpressure = data['designpressure']
        except:
            obj = Newton(ComponentID, "designpressure")
            designpressure = obj.calculate_Material()
        try:
            designtemperature = data['designtemperature']
        except:
            obj = Newton(ComponentID, "designtemperature")
            designtemperature = obj.calculate_Material()
        try:
            mindesigntemperature = data['mindesigntemperature']
        except:
            obj = Newton(ComponentID, "mindesigntemperature")
            mindesigntemperature = obj.calculate_Material()
        try:
            SigmaPhase = data['SigmaPhase']
        except:
            obj = Newton(ComponentID, "SigmaPhase")
            SigmaPhase = obj.calculate()
        try:
            sulfurContent = data['sulfurContent']
        except:
            sulfurContent = rwmaterial.sulfurcontent
        try:
            heatTreatment = data['heatTreatment']
        except:
            heatTreatment = rwmaterial.heattreatment
        try:
            refTemp = data['refTemp']
        except:
            obj = Newton(ComponentID, "refTemp")
            refTemp = obj.calculate_Material()
        try:
            PTAMaterialGrade = data['PTAMaterialGrade']
        except:
            PTAMaterialGrade = rwmaterial.ptamaterialcode
        try:
            hthamaterialcode = data['hthamaterialcode']
        except:
            hthamaterialcode = rwmaterial.hthamaterialcode
        try:
            materialPTA = data['materialPTA']
        except:
            materialPTA = rwmaterial.ispta
        try:
            ishtha = data['ishtha']
        except:
            ishtha = rwmaterial.ishtha
        try:
            austeniticSteel = data['austeniticSteel']
        except:
            austeniticSteel = rwmaterial.austenitic
        try:
            temper = data['temper']
        except:
            temper = rwmaterial.temper
        try:
            carbonlowalloy = data['carbonlowalloy']
        except:
            carbonlowalloy = rwmaterial.carbonlowalloy
        try:
            nickelAlloy = data['nickelAlloy']
        except:
            nickelAlloy = rwmaterial.nickelbased
        try:
            chromium = data['chromium']
        except:
            chromium = rwmaterial.chromemoreequal12
        try:
            materialCostFactor = data['materialCostFactor']
        except:
            obj = Newton(ComponentID, "materialCostFactor")
            materialCostFactor = obj.calculate_Material()
        try:
            yieldstrength = data['yieldstrength']
        except:
            obj = Newton(ComponentID, "yieldstrength")
            yieldstrength = obj.calculate_Material()
        try:
            tensilestrength = data['tensilestrength']
        except:
            obj = Newton(ComponentID, "tensilestrength")
            tensilestrength = obj.calculate_Material()
        try:
            rwassessment = models.RwAssessment(equipmentid_id=comp.equipmentid_id, componentid_id=comp.componentid,
                                               assessmentdate=datetime.now(),commisstiondate=datetime.now(),
                                               riskanalysisperiod=36,
                                               isequipmentlinked=comp.isequipmentlinked,
                                               assessmentmethod="",
                                               proposalname=Proposalname)
            rwassessment.save()
            faci = models.Facility.objects.get(
                facilityid=models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).facilityid_id)
            rwequipment = models.RwEquipment(id=rwassessment, commissiondate=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).commissiondate,
                                             adminupsetmanagement=AdminControlUpset, containsdeadlegs=containsDeadlegs,
                                             cyclicoperation=CylicOper, highlydeadleginsp=HighlyEffe,
                                             downtimeprotectionused=Downtime,
                                             externalenvironment=ExternalEnvironment,
                                             heattraced=HeatTraced, interfacesoilwater=InterfaceSoilWater,
                                             lineronlinemonitoring=LOM,
                                             materialexposedtoclext=MFTF,
                                             minreqtemperaturepressurisation=minTemp,
                                             onlinemonitoring=OnlineMonitoring,
                                             presencesulphideso2=PresenceofSulphides,
                                             presencesulphideso2shutdown=PresenceofSulphidesShutdown,
                                             pressurisationcontrolled=PressurisationControlled, pwht=PWHT,
                                             steamoutwaterflush=SteamedOut,
                                             managementfactor=faci.managementfactor,
                                             thermalhistory=ThermalHistory,
                                             yearlowestexptemp=EquOper, volume=EquipmentVolumn)
            rwequipment.save()
            rwcomponent = models.RwComponent(id=rwassessment, nominaldiameter=nominaldiameter,
                                             nominalthickness=NorminalThickness,
                                             currentthickness=CurrentThickness,
                                             minreqthickness=MinReqThickness, currentcorrosionrate=CurrentCorrosionRate,
                                             branchdiameter=branchdiameter,
                                             branchjointtype=branchjointtype,
                                             brinnelhardness=MaxBrinell,
                                             brittlefracturethickness=BrittleFacture,
                                             deltafatt=deltafatt, chemicalinjection=ChemicalInjection,
                                             highlyinjectioninsp=HFICI, complexityprotrusion=complex,
                                             correctiveaction=correctiveaction, crackspresent=PresenceCracks,
                                             cyclicloadingwitin15_25m=CylicLoad,
                                             damagefoundinspection=DFDI,
                                             numberpipefittings=numberPipe,
                                             pipecondition=pipecondition,
                                             previousfailures=previousfailures, shakingamount=shakingamount,
                                             shakingdetected=VASD,
                                             shakingtime=shakingtime,
                                             weldjointefficiency=weldjointeff,
                                             allowablestress=allowablestresss,
                                             structuralthickness=structuralthickness,
                                             componentvolume=compvolume, hthadamage=hthadamage,
                                             minstructuralthickness=MinStructuralThickness,
                                             fabricatedsteel=Fabricatedsteel, equipmentsatisfied=EquipmentSatisfied,
                                             nominaloperatingconditions=NominalOperating,
                                             cetgreaterorequal=Cetgreaterorequal, cyclicservice=Cyclicservice,
                                             equipmentcircuitshock=equipmentCircuit,
                                             confidencecorrosionrate=confidencecr)
            rwcomponent.save()
            rwstream = models.RwStream(id=rwassessment, aminesolution=amineSolution,
                                       aqueousoperation=aqueosOP,
                                       aqueousshutdown=aqueosShut, toxicconstituent=toxicconstituent,
                                       caustic=environtCaustic,
                                       chloride=chlorideIon, co3concentration=co3,
                                       cyanide=cyanidesPresence,
                                       exposedtogasamine=exposedAmine, exposedtosulphur=exposedSulfur,
                                       exposuretoamine=exposureAmine,
                                       h2s=environtH2S, h2sinwater=h2sinwater, hydrogen=processContainHydro,
                                       hydrofluoric=presentHF, materialexposedtoclint=materialChlorineIntern,
                                       maxoperatingpressure=maxOP,
                                       maxoperatingtemperature=float(maxOT),
                                       minoperatingpressure=float(minOP),
                                       minoperatingtemperature=minOT,
                                       criticalexposuretemperature=criticalTemp,
                                       naohconcentration=naohConcent,
                                       releasefluidpercenttoxic=float(releasePercentToxic),
                                       waterph=float(PHWater),
                                       h2spartialpressure=float(H2Spressure),
                                       flowrate=float(flowrate), liquidlevel=float(liquidlevel),
                                       storagephase=storagephase)
            rwstream.save()
            rwexcor = models.RwExtcorTemperature(id=rwassessment, minus12tominus8=OP1,
                                                 minus8toplus6=OP2,
                                                 plus6toplus32=OP3, plus32toplus71=OP4,
                                                 plus71toplus107=OP5,
                                                 plus107toplus121=OP6, plus121toplus135=OP7,
                                                 plus135toplus162=OP8, plus162toplus176=OP9,
                                                 morethanplus176=OP10)
            rwexcor.save()
            rwcoat = models.RwCoating(id=rwassessment, externalcoating=externalcoating,
                                      externalinsulation=externalinsulation,
                                      internalcladding=internalcladding, internalcoating=internalcoating,
                                      internallining=internallining,
                                      externalcoatingdate=externalcoatingdate,
                                      externalcoatingquality=externalcoatingquality,
                                      externalinsulationtype=extInsulationType,
                                      insulationcondition=insulationCondition,
                                      insulationcontainschloride=insulationcontainschloride,
                                      internallinercondition=internallinercondition,
                                      internallinertype=internallinertype,
                                      claddingcorrosionrate=cladCorrosion,
                                      supportconfignotallowcoatingmaint=supportCoatingMaintain,
                                      claddingthickness=claddingthickness)
            rwcoat.save()
            rwmaterial = models.RwMaterial(id=rwassessment, corrosionallowance=corrosionAllow,
                                           materialname=materialname,
                                           designpressure=designpressure,
                                           designtemperature=designtemperature,
                                           mindesigntemperature=mindesigntemperature,
                                           sigmaphase=SigmaPhase,
                                           sulfurcontent=sulfurContent, heattreatment=heatTreatment,
                                           referencetemperature=refTemp,
                                           ptamaterialcode=PTAMaterialGrade,
                                           hthamaterialcode=hthamaterialcode, ispta=materialPTA,
                                           ishtha=ishtha,
                                           austenitic=austeniticSteel, temper=temper, carbonlowalloy=carbonlowalloy,
                                           nickelbased=nickelAlloy, chromemoreequal12=chromium,
                                           costfactor=materialCostFactor,
                                           yieldstrength=yieldstrength, tensilestrength=tensilestrength)
            rwmaterial.save()
            if rw.count() == 1:
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                # print("go test")
                try:
                    release_duration = data['release_duration']
                except:
                    release_duration = rwinputca.release_duration
                try:
                    fluid = data['fluid']
                except:
                    fluid = rwinputca.api_fluid
                try:
                    detection_type = data['detection_type']
                except:
                    detection_type = rwinputca.detection_type
                try:
                    isulation_type = data['isulation_type']
                except:
                    isulation_type = rwinputca.isulation_type
                try:
                    mitigation_system = data['mitigation_system']
                except:
                    mitigation_system = rwinputca.mitigation_system
                try:
                    toxic_fluid = data['toxic_fluid']
                except:
                    toxic_fluid = rwinputca.toxic_fluid
                try:
                    equipment_cost = data['equipment_cost']
                except:
                    obj = Newton(ComponentID, "equipment_cost")
                    equipment_cost = obj.calculate_RwinputCaLevel1()
                try:
                    injure_cost = data['injure_cost']
                except:
                    obj = Newton(ComponentID, "injure_cost")
                    injure_cost = obj.calculate_RwinputCaLevel1()
                try:
                    evironment_cost = data['evironment_cost']
                except:
                    obj = Newton(ComponentID, "evironment_cost")
                    evironment_cost = obj.calculate_RwinputCaLevel1()
                try:
                    personal_density = data['personal_density']
                except:
                    obj = Newton(ComponentID, "personal_density")
                    personal_density = obj.calculate_RwinputCaLevel1()
                try:
                    production_cost = data['production_cost']
                except:
                    obj = Newton(ComponentID, "production_cost")
                    production_cost = obj.calculate_RwinputCaLevel1()
                try:
                    mass_inventory = data['mass_inventory']
                except:
                    obj = Newton(ComponentID, "mass_inventory")
                    mass_inventory = obj.calculate_RwinputCaLevel1()
                try:
                    mass_component = data['mass_component']
                except:
                    obj = Newton(ComponentID, "mass_component")
                    mass_component = obj.calculate_RwinputCaLevel1()
                try:
                    toxic_percent = data['toxic_percent']
                except:
                    obj = Newton(ComponentID, "toxic_percent")
                    toxic_percent = obj.calculate_RwinputCaLevel1()
                try:
                    outage_multiplier = data['outage_multiplier']
                except:
                    obj = Newton(ComponentID, "outage_multiplier")
                    outage_multiplier = obj.calculate_RwinputCaLevel1()
                try:
                    process_unit = data['process_unit']
                except:
                    obj = Newton(ComponentID, "process_unit")
                    process_unit = obj.calculate_RwinputCaLevel1()
                try:
                    if str(data['fluid']) == "Gasoline":
                        apiFluid = "C6-C8"
                    elif str(data['fluid']) == "Light Diesel Oil":
                        apiFluid = "C9-C12"
                    elif str(data['fluid']) == "Heavy Diesel Oil":
                        apiFluid = "C13-C16"
                    elif str(data['fluid']) == "Fuel Oil" or str(data['fluid']) == "Crude Oil":
                        apiFluid = "C17-C25"
                    else:
                        apiFluid = "C25+"
                except:
                    apiFluid = "C6-C8"
                rwinputca = models.RwInputCaLevel1(id=rwassessment,api_fluid = apiFluid,
                                                   release_duration=release_duration,
                                                   detection_type=detection_type,
                                                   isulation_type=isulation_type,
                                                   mitigation_system=mitigation_system,
                                                   equipment_cost=equipment_cost, injure_cost=injure_cost,
                                                   evironment_cost=evironment_cost,
                                                   personal_density=personal_density,
                                                   material_cost=materialCostFactor,
                                                   production_cost=production_cost,
                                                   mass_inventory=mass_inventory,
                                                   mass_component=mass_component,
                                                   stored_pressure=float(minOP) * 6.895, stored_temp=minOT,
                                                   model_fluid=apiFluid, toxic_fluid=toxic_fluid,
                                                   toxic_percent=float(toxic_percent),
                                                   process_unit=float(process_unit),
                                                   outage_multiplier=float(outage_multiplier))
                rwinputca.save()
            else:
                # print("go else")
                try:
                    if str(data['fluid']) == "Gasoline":
                        apiFluid = "C6-C8"
                    elif str(data['fluid']) == "Light Diesel Oil":
                        apiFluid = "C9-C12"
                    elif str(data['fluid']) == "Heavy Diesel Oil":
                        apiFluid = "C13-C16"
                    elif str(data['fluid']) == "Fuel Oil" or str(data['fluid']) == "Crude Oil":
                        apiFluid = "C17-C25"
                    else:
                        apiFluid = "C25+"
                except:
                    apiFluid = "C6-C8"
                rwinputca = models.RwInputCaLevel1(id=rwassessment,api_fluid = apiFluid,
                                                   release_duration=0.0,
                                                   detection_type="",
                                                   isulation_type="",
                                                   mitigation_system="",
                                                   equipment_cost=0.0, injure_cost=0.0,
                                                   evironment_cost=0.0,
                                                   personal_density=0.0,
                                                   material_cost=0.0,
                                                   production_cost=0.0,
                                                   mass_inventory=0.0,
                                                   mass_component=0.0,
                                                   stored_pressure=float(minOP) * 6.895, stored_temp=minOT,
                                                   model_fluid="", toxic_fluid="",
                                                   toxic_percent=0.0,
                                                   process_unit=0.0,
                                                   outage_multiplier=0.0)
                rwinputca.save()
            ReCalculate.ReCalculate(rwassessment.id,request)
        except Exception as e:
            print(e)


from django.utils import timezone
import pytz

import glob
import logging
import logging.handlers

# You'll need these imports in your own code
import multiprocessing

# Next two import lines for this demo only
from random import choice, random
import time
# timezone.activate(pytz.timezone("Asia/Ho_Chi_Minh"))

if __name__ == "__main__":
    obj = Verification()
    data = []
    # obj.Regular()
    # obj.Regular(request)
    # q = 'SELECT ID FROM benchmark.rw_assessment where ComponentID = %s order by AssessmentDate desc limit 1;'
    # Query = models.RwAssessment.objects.raw(q, [423])
    # timer = models.VerificationPeriodically.objects.get(id=44)
    # for a in Query:
    #     ass= a.assessmentdate
    #     print(datetime.now().astimezone())
    #     # # print(datetime.now())
    #     # print(timezone.now())
    #     b = timezone.now()-a.assessmentdate
    #     dem = a.assessmentdate.hour * 3600 + a.assessmentdate.minute * 60 + a.assessmentdate.second
    #     realtime = datetime.now().hour*3600+ datetime.now().minute*60 +datetime.now().second
    #     demngay=ass.year*365+ ass.month*30+ass.day
    #     realngay = datetime.now().year*365+ datetime.now().month*30+datetime.now().day
    #     sub = realtime-dem +(realngay-demngay)*3600*24
    #     print(sub)
    #     print(b)
    #     s= timer.timer.split(":")
    #     t = int(s[0])*3600 + int(s[1])*60+int(s[2])
    #     print(t)
    #     print(str(datetime.now().strftime('%m-%d-%y,%H:%M:%S')))
        # print(a.assessmentdate-datetime.now().astimezone())
#------------------------------------------
    # while 1:
    #     logging.basicConfig(level=logging.DEBUG, filename='runtime.log', filemode='a') # a: ghi nối tiếp, w: ghi đè
    #     logging.warning('Watch out!')  # sẽ in ra warning trên console
    #     logging.info('I told you so')  # không in gì cả
#------------------------------------------
    # LOG_FILENAME = 'logging_rotatingfile_RBI.log'
    #
    # # Set up a specific logger with our desired output level
    # my_logger = logging.getLogger('MyLogger')
    # my_logger.setLevel(logging.DEBUG)
    #
    # # Add the log message handler to the logger
    # handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5) # 50 MB = 52 428 800 bytes
    # f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    # handler.setFormatter(f)
    # my_logger.addHandler(handler)
    # Mess="cuong"
    # # Log some messages
    # for i in range(10):
    #     my_logger.debug('i = %s' % Mess)
    #
    # # See what files are created
    # logfiles = glob.glob('%s*' % LOG_FILENAME)
    #
    # for filename in logfiles:
    #     print(filename)
#--------------------------------------------
    # ACCESS_TOKEN='736a1560-4750-11eb-a7a3-139a8c7a1ebd'
    # headers = {
    #     'Content-Type': 'application/json',
    #     'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlbmwubGFiNDExQGdtYWlsLmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiNzlkYjhhZTAtNmEyNy0xMWU4LTk2NjUtMTMyMDYzOTIxYjExIiwiZmlyc3ROYW1lIjoibGFiIiwibGFzdE5hbWUiOiI0MTEiLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiI3OWQ2MGNhMC02YTI3LTExZTgtOTY2NS0xMzIwNjM5MjFiMTEiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE2MDkxNDE0MjUsImV4cCI6MTYxMDk0MTQyNX0.jlPZRnZD5OczsiQyQHIY6bsCVVGbnBO__S68A5sUdeq75MmJ1FbSSe_NqgDaX9pOOx4dzbnTe_dniG7PIK2Esg',
    # }
    # response = requests.get(
    #     'http://demo.thingsboard.io/api/plugins/telemetry/DEVICE/' + ACCESS_TOKEN + '/values/timeseries?keys=',
    #     headers=headers)
    # print(response.json())
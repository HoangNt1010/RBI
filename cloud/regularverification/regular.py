import os, sys

from django.core.wsgi import get_wsgi_application
import paho.mqtt.client as mqtt

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from django.http import Http404, HttpResponse
from cloud import models
from datetime import datetime
import time
import json
import math
import paho.mqtt.client as mqtt
from cloud.process.RBI import fastCalulate as ReCalculate
from django.shortcuts import render, redirect, render_to_response
from cloud.regularverification.interpolation import Newton


class REGULAR:
    # def __init__(self):
    #     self.componentID

    def regular_1(self, siteid):
        try:
            print("start")
            modeOfSite = models.VerificationPeriodically.objects.filter(siteid_id=siteid)
            equip = models.EquipmentMaster.objects.filter(siteid_id=siteid)
            print(modeOfSite.count())
            oleMode = modeOfSite[modeOfSite.count() - 1].mode
            while oleMode:
                print("go regular")
                if equip.count():
                    for eq in equip:
                        component = models.ComponentMaster.objects.filter(equipmentid_id=eq.equipmentid)
                        for compo in component:
                            print("go for ")
                            ass = models.RwAssessment.objects.filter(componentid_id=compo.componentid).count()
                            if ass > 1:
                                print(compo.componentid)
                                dateins = self.getDate(compo.componentid)
                                if (dateins != 0):
                                    date = datetime.now()
                                    timer = (date.year * 365 + date.month * 30 + date.day) - (
                                                dateins.year * 365 + dateins.month * 30 + dateins.day)
                                    print("timer", timer)
                                    if (timer > modeOfSite[modeOfSite.count() - 1].timer):
                                        print("start new")
                                        self.NowProposal(compo.componentid)
                                        print("New ok")
                            modeOfSite = models.VerificationPeriodically.objects.filter(siteid_id=siteid)
                            oleMode = modeOfSite[modeOfSite.count() - 1].mode
                            print("oldmode", oleMode)
                time.sleep(7200)  # 86400
        except Exception as e:
            print("Error: unable to start thread:", e)

    def getDate(self, ComponentID):
        try:
            print("getDate")
            insdate = models.RwAssessment.objects.filter(componentid_id=ComponentID)
            # for i in range(len(insdate)):
            print(insdate[len(insdate) - 1].assessmentdate)
            return insdate[len(insdate) - 1].assessmentdate
        except Exception as e:
            print(e)
            return 0

    def NowProposal(self, componentID):
        try:
            print("tuan")
            print(componentID)
            THINGSBOARD_HOST = "demo.thingsboard.io"
            ACCESS_TOKEN = models.ZSensor.objects.filter(Componentid=componentID)[0].Token
            print(ACCESS_TOKEN)
            client = mqtt.Client()
            client.username_pw_set(ACCESS_TOKEN)
            # client.username_pw_set("Xl3AXEbRsuAvctwHLzFA")
            client.connect(THINGSBOARD_HOST, 1883)
            print("11111")
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            # client.on_message = self.on_message
            client.loop_forever()
        except Exception as e:
            print("eror at NowProposal:", e)
            data = []
            # self.saveData(data,componentID)
            comp = models.ComponentMaster.objects.get(componentid=componentID)
            if comp.componenttypeid_id == 12 or comp.componenttypeid_id == 13 or comp.componenttypeid_id == 14 or comp.componenttypeid_id == 15:
                self.saveTank(data, componentID)
            else:
                self.saveNormal(data, componentID)
            # raise Http404

    def on_connect(self, client, userdata, rc, *extra_params):
        print("Connected with result code " + str(rc))
        sensor_data = {"id": 1, "device": "Device A2", "client": 1, "key": "attribute1"}
        client.publish('v1/devices/me/attributes/request/1', json.dumps(sensor_data))

    def on_message(self, client, userdata, msg):
        print(msg)
        print(msg.topic)
        print(msg.payload)
        payload = msg.payload.decode()
        print(payload)
        self.Checkdatathingsboard(payload=payload)
        client.disconnect()

    def Checkdatathingsboard(self, payload):
        try:
            data_sensor = json.loads(payload)
            data = data_sensor['client']
            print("tesst dataa")
            print(data['componentid'])
            print()
            comp = models.ComponentMaster.objects.get(componentid=data['componentid'])
            if comp.componenttypeid_id == 12 or comp.componenttypeid_id == 13 or comp.componenttypeid_id == 14 or comp.componenttypeid_id == 15:
                self.saveTank(data, ComponentID=data['componentid'])
            else:
                self.saveNormal(data, ComponentID=data['componentid'])
            # self.saveData(data,data['componentid']) #anh tuan viet
        except Exception as e:
            print('connect data error:', e)

    def goinormal(self, data, ComponentID):
        toi = {}

        try:
            toi['deltafatt'] = data['deltafatt']
        except:
            obj = Newton(ComponentID, "deltafatt")
            toi['deltafatt'] = obj.calculate_Component()
        try:
            toi['toxic_percent'] = data['toxic_percent']
        except:
            obj = Newton(ComponentID, "toxic_percent")
            toi['toxic_percent'] = obj.calculate_RwinputCaLevel1()
        try:
            toi['nominaldiameter'] = data['nominaldiameter']
        except:
            obj = Newton(ComponentID, "nominaldiameter")
            toi['nominaldiameter'] = obj.calculate_Component()
        try:
            toi['naohConcent'] = data['naohConcent']
        except:
            obj = Newton(ComponentID, "naohConcent")
            toi['naohConcent'] = obj.calculate_Operating()
        try:
            toi['releasePercentToxic'] = data['releasePercentToxic']
        except:
            obj = Newton(ComponentID, "releasePercentToxic")
            toi['releasePercentToxic'] = obj.calculate_Operating()
        try:
            toi['chlorideIon'] = data['chlorideIon']
        except:
            obj = Newton(ComponentID, "chlorideIon")
            toi['chlorideIon'] = obj.calculate_Operating()
        try:
            toi['co3'] = data['co3']
        except:
            obj = Newton(ComponentID, "co3")
            toi['co3'] = obj.calculate_Operating()
        try:
            toi['h2sContent'] = data['h2sContent']
        except:
            obj = Newton(ComponentID, "h2sContent")
            toi['h2sContent'] = obj.calculate_Operating()
        try:
            toi['PHWater'] = data['PHWater']
        except:
            obj = Newton(ComponentID, "PHWater")
            toi['PHWater'] = obj.calculate_Operating()
        try:
            toi['cladCorrosion'] = data['cladCorrosion']
        except:
            obj = Newton(ComponentID, "cladCorrosion")
            toi['cladCorrosion'] = obj.calculate_Equipment()
        try:
            toi['claddingthickness'] = data['claddingthickness']
        except:
            obj = Newton(ComponentID, "claddingthickness")
            toi['claddingthickness'] = obj.calculate_Equipment()
        try:
            toi['H2Spressure'] = data['H2Spressure']
        except:
            obj = Newton(ComponentID, "H2Spressure")
            toi['H2Spressure'] = obj.calculate_Operating()
        try:
            toi['criticalTemp'] = data['criticalTemp']
        except:
            obj = Newton(ComponentID, "criticalTemp")
            toi['criticalTemp'] = obj.calculate_Operating()
        try:
            toi['minOT'] = data['minOT']
        except:
            obj = Newton(ComponentID, "minOT")
            toi['minOT'] = obj.calculate_Operating()
        try:
            toi['maxOT'] = data['maxOT']
        except:
            obj = Newton(ComponentID, "maxOT")
            toi['maxOT'] = obj.calculate_Operating()
        try:
            toi['shellHieght'] = data['shellHieght']
        except:
            obj = Newton(ComponentID, "shellHieght")
            toi['shellHieght'] = obj.calculate_Component()
        try:
            toi['BrittleFacture'] = data['BrittleFacture']
        except:
            obj = Newton(ComponentID, "BrittleFacture")
            toi['BrittleFacture'] = obj.calculate_Component()
        try:
            toi['NorminalThickness'] = data['NorminalThickness']
        except:
            obj = Newton(ComponentID, "NorminalThickness")
            toi['NorminalThickness'] = obj.calculate_Component()
        try:
            toi['CurrentThickness'] = data['CurrentThickness']
        except:
            obj = Newton(ComponentID, "CurrentThickness")
            toi['CurrentThickness'] = obj.calculate_Component()
        try:
            toi['distance'] = data['distance']
        except:
            obj = Newton(ComponentID, "distance")
            toi['distance'] = obj.calculate_Equipment()
        try:
            toi['EquipmentVolumn'] = data['EquipmentVolumn']
        except:
            obj = Newton(ComponentID, "EquipmentVolumn")
            toi['EquipmentVolumn'] = obj.calculate_Equipment()
        try:
            toi['CurrentCorrosionRate'] = data['CurrentCorrosionRate']
        except:
            obj = Newton(ComponentID, "CurrentCorrosionRate")
            toi['CurrentCorrosionRate'] = obj.calculate_Component()
        try:
            toi['MinRequiredThickness'] = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            toi['MinRequiredThickness'] = obj.calculate_Component()
        try:
            toi['MaximumOperatingPressure'] = data['maxOP']
        except:
            obj = Newton(ComponentID, "maxOP")
            toi['MaximumOperatingPressure'] = obj.calculate_Operating()
        try:
            toi['MinOperatingPressure'] = data['minOP']
        except:
            obj = Newton(ComponentID, "minOP")
            toi['MinOperatingPressure'] = obj.calculate_Operating()
        return toi

    def goitank(self, data, ComponentID):
        toi = {}
        try:
            toi['fluidHeight'] = data['fluidHeight']
        except:
            obj = Newton(ComponentID, "fluidHeight")
            toi['fluidHeight'] = obj.calculate_Operating()
        try:
            toi['fluidLeaveDike'] = data['fluidLeaveDike']
        except:
            obj = Newton(ComponentID, "fluidLeaveDike")
            toi['fluidLeaveDike'] = obj.calculate_Operating()
        try:
            toi['fluidOnsite'] = data['fluidOnsite']
        except:
            obj = Newton(ComponentID, "fluidOnsite")
            toi['fluidOnsite'] = obj.calculate_Operating()
        try:
            toi['fluidOffsite'] = data['fluidOffsite']
        except:
            obj = Newton(ComponentID, "fluidOffsite")
            toi['fluidOffsite'] = obj.calculate_Operating()
        try:
            toi['naohConcent'] = data['naohConcent']
        except:
            obj = Newton(ComponentID, "naohConcent")
            toi['naohConcent'] = obj.calculate_Operating()
        try:
            toi['releasePercentToxic'] = data['releasePercentToxic']
        except:
            obj = Newton(ComponentID, "releasePercentToxic")
            toi['releasePercentToxic'] = obj.calculate_Operating()
        try:
            toi['chlorideIon'] = data['chlorideIon']
        except:
            obj = Newton(ComponentID, "chlorideIon")
            toi['chlorideIon'] = obj.calculate_Operating()
        try:
            toi['co3'] = data['co3']
        except:
            obj = Newton(ComponentID, "co3")
            toi['co3'] = obj.calculate_Operating()
        try:
            toi['h2sContent'] = data['h2sContent']
        except:
            obj = Newton(ComponentID, "h2sContent")
            toi['h2sContent'] = obj.calculate_Operating()
        try:
            toi['PHWater'] = data['PHWater']
        except:
            obj = Newton(ComponentID, "PHWater")
            toi['PHWater'] = obj.calculate_Operating()
        try:
            toi['cladCorrosion'] = data['cladCorrosion']
        except:
            obj = Newton(ComponentID, "cladCorrosion")
            toi['cladCorrosion'] = obj.calculate_Equipment()
        try:
            toi['claddingthickness'] = data['claddingthickness']
        except:
            obj = Newton(ComponentID, "claddingthickness")
            toi['claddingthickness'] = obj.calculate_Equipment()
        try:
            toi['H2Spressure'] = data['H2Spressure']
        except:
            obj = Newton(ComponentID, "H2Spressure")
            toi['H2Spressure'] = obj.calculate_Operating()
        try:
            toi['criticalTemp'] = data['criticalTemp']
        except:
            obj = Newton(ComponentID, "criticalTemp")
            toi['criticalTemp'] = obj.calculate_Operating()
        try:
            toi['minOT'] = data['minOT']
        except:
            obj = Newton(ComponentID, "minOT")
            toi['minOT'] = obj.calculate_Operating()
        try:
            toi['maxOT'] = data['maxOT']
        except:
            obj = Newton(ComponentID, "maxOT")
            toi['maxOT'] = obj.calculate_Operating()
        try:
            toi['shellHieght'] = data['shellHieght']
        except:
            obj = Newton(ComponentID, "shellHieght")
            toi['shellHieght'] = obj.calculate_Component()
        try:
            toi['BrittleFacture'] = data['BrittleFacture']
        except:
            obj = Newton(ComponentID, "BrittleFacture")
            toi['BrittleFacture'] = obj.calculate_Component()
        try:
            toi['NorminalThickness'] = data['NorminalThickness']
        except:
            obj = Newton(ComponentID, "NorminalThickness")
            toi['NorminalThickness'] = obj.calculate_Component()
        try:
            toi['CurrentThickness'] = data['CurrentThickness']
        except:
            obj = Newton(ComponentID, "CurrentThickness")
            toi['CurrentThickness'] = obj.calculate_Component()
        try:
            toi['tankDiameter'] = data['tankDiameter']
        except:
            obj = Newton(ComponentID, "tankDiameter")
            toi['tankDiameter'] = obj.calculate_Component()
        try:
            toi['distance'] = data['distance']
        except:
            obj = Newton(ComponentID, "distance")
            toi['distance'] = obj.calculate_Equipment()
        try:
            toi['EquipmentVolumn'] = data['EquipmentVolumn']
        except:
            obj = Newton(ComponentID, "EquipmentVolumn")
            toi['EquipmentVolumn'] = obj.calculate_Equipment()
        try:
            toi['CurrentCorrosionRate'] = data['CurrentCorrosionRate']
        except:
            obj = Newton(ComponentID, "CurrentCorrosionRate")
            toi['CurrentCorrosionRate'] = obj.calculate_Component()
        try:
            toi['MinRequiredThickness'] = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            toi['MinRequiredThickness'] = obj.calculate_Component()
        try:
            toi['MaximumOperatingPressure'] = data['maxOP']
        except:
            obj = Newton(ComponentID, "maxOP")
            toi['MaximumOperatingPressure'] = obj.calculate_Operating()
        try:
            toi['MinOperatingPressure'] = data['minOP']
        except:
            obj = Newton(ComponentID, "minOP")
            toi['MinOperatingPressure'] = obj.calculate_Operating()
        return toi

    def saveTank(self, data, ComponentID):
        list = models.RwAssessment.objects.filter(componentid_id=ComponentID)
        ass = list[list.count() - 1]
        rwequipment = models.RwEquipment.objects.get(id=ass.id)
        rwcomponent = models.RwComponent.objects.get(id=ass.id)
        rwstream = models.RwStream.objects.get(id=ass.id)
        rwcoat = models.RwCoating.objects.get(id=ass.id)
        rwmaterial = models.RwMaterial.objects.get(id=ass.id)
        comp = models.ComponentMaster.objects.get(componentid=ComponentID)
        Proposalname = "proposal" + str(models.RwAssessment.objects.filter(componentid=comp.componentid).count())
        # Equipment
        try:
            PWHT = data['PWHT']
            print("da luu")
        except:
            PWHT = rwequipment.pwht
        try:
            OnlineMonitoring = data['OnlineMonitoring']
        except:
            OnlineMonitoring = rwequipment.onlinemonitoring
        try:
            EquipmentVolumn = data['EquipmentVolumn']
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
            minTemp = data['minTemp']
        except:
            obj = Newton(ComponentID, "minTemp")
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
            distance = data['distance']
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
        # Component
        try:
            confidencecr = data['confidencecr']
        except:
            confidencecr = rwcomponent.confidencecorrosionrate
        try:
            tankDiameter = data['tankDiameter']
        except:
            obj = Newton(ComponentID, "tankDiameter")
            tankDiameter = obj.calculate_Component()
        try:
            NorminalThickness = data['NorminalThickness']
        except:
            obj = Newton(ComponentID, "NorminalThickness")
            NorminalThickness = obj.calculate_Component()
        try:
            CurrentThickness = data['CurrentThickness']
        except:
            obj = Newton(ComponentID, "CurrentThickness")
            CurrentThickness = obj.calculate_Component()
        try:
            MinReqThickness = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            MinReqThickness = obj.calculate_Component()
        try:
            structuralthickness = data['structuralthickness']
        except:
            obj = Newton(ComponentID, "structuralthickness")
            structuralthickness = obj.calculate_Component()
        try:
            CurrentCorrosionRate = data['CurrentCorrosionRate']
        except:
            obj = Newton(ComponentID, "CurrentCorrosionRate")
            CurrentCorrosionRate = obj.calculate_Component()
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
            obj = Newton(ComponentID, "weldjointeff")
            weldjointeff = obj.calculate_Component()
        try:
            compvolume = data['compvolume']
        except:
            obj = Newton(ComponentID, "compvolume")
            compvolume = obj.calculate_Component()
        try:
            allowablestresss = data['allowablestresss']
        except:
            obj = Newton(ComponentID, "allowablestresss")
            allowablestresss = obj.calculate_Component()
        try:
            complex = data['complex']
        except:
            complex = rwcomponent.complexityprotrusion
        try:
            MaxBrinell = data['MaxBrinell']
        except:
            MaxBrinell = rwcomponent.brinnelhardness
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
        # Stream
        try:
            maxOT = data['maxOT']
        except:
            obj = Newton(ComponentID, "maxOT")
            maxOT = obj.calculate_Operating()
        try:
            maxOP = data['maxOP']
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
            criticalTemp = data['criticalTemp']
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
            PHWater = data['PHWater']
        except:
            obj = Newton(ComponentID, "PHWater")
            PHWater = obj.calculate_Operating()
        try:
            flowrate = data['flowrate']
        except:
            obj = Newton(ComponentID, "flowrate")
            flowrate = obj.calculate_Operating()
        try:
            exposedAmine = data['exposedAmine']
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
            environtH2S = data['environtH2S']
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
        # Operating
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
        # Coating
        try:
            internalcoating = data['internalcoating']
        except:
            internalcoating = rwcoat.internalcoating
        try:
            externalcoating = data['externalcoating']
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
            internalcladding = data['internalcladding']
        except:
            internalcladding = rwcoat.internalcladding
        try:
            cladCorrosion = data['cladCorrosion']
        except:
            obj = Newton(ComponentID, "cladCorrosion")
            cladCorrosion = obj.calculate_Equipment()
        try:
            claddingthickness = data['claddingthickness']
        except:
            obj = Newton(ComponentID, "claddingthickness")
            claddingthickness = obj.calculate_Equipment()
        try:
            internallining = data['internallining']
        except:
            internallining = rwcoat.internallining
        try:
            internallinertype = data['internallinertype']
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
        # Material
        try:
            materialname = data['materialname']
        except:
            materialname = "M1 " + str(list.count())
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
            # rw ca input
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
                                               assessmentdate=datetime.now(),
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
            ReCalculate.ReCalculate(rwassessment.id)
        except Exception as e:
            print(e)

    def saveNormal(self, data, ComponentID):
        list = models.RwAssessment.objects.filter(componentid_id=ComponentID)
        ass = list[list.count() - 1]
        rwequipment = models.RwEquipment.objects.get(id=ass.id)
        rwcomponent = models.RwComponent.objects.get(id=ass.id)
        rwstream = models.RwStream.objects.get(id=ass.id)
        rwcoat = models.RwCoating.objects.get(id=ass.id)
        rwmaterial = models.RwMaterial.objects.get(id=ass.id)
        rw = models.RwInputCaLevel1.objects.filter(id=ass.id)
        comp = models.ComponentMaster.objects.get(componentid=ComponentID)
        Proposalname = "proposal" + str(models.RwAssessment.objects.filter(componentid=comp.componentid).count())
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
            minTemp = data['minTemp']
        except:
            obj = Newton(ComponentID, "minTemp")
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
            EquipmentVolumn = data['EquipmentVolumn']
        except Exception as e:
            obj = Newton(ComponentID, "EquipmentVolumn")
            EquipmentVolumn = obj.calculate_Equipment()
        # Component
        try:
            nominaldiameter = data['nominaldiameter']
        except:
            obj = Newton(ComponentID, "nominaldiameter")
            nominaldiameter = obj.calculate_Component()
        try:
            NorminalThickness = data['NorminalThickness']
        except:
            obj = Newton(ComponentID, "NorminalThickness")
            NorminalThickness = obj.calculate_Component()
        try:
            CurrentThickness = data['CurrentThickness']
        except:
            obj = Newton(ComponentID, "CurrentThickness")
            CurrentThickness = obj.calculate_Component()
        try:
            MinReqThickness = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            MinReqThickness = obj.calculate_Component()
        try:
            CurrentCorrosionRate = data['CurrentCorrosionRate']
        except:
            obj = Newton(ComponentID, "CurrentCorrosionRate")
            CurrentCorrosionRate = obj.calculate_Component()
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
            MaxBrinell = rwcomponent.brinnelhardness
        try:
            HFICI = data['HFICI']
        except:
            HFICI = rwcomponent.highlyinjectioninsp
        try:
            ChemicalInjection = data['ChemicalInjection']
        except:
            ChemicalInjection = rwcomponent.chemicalinjection
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
            obj = Newton(ComponentID, "weldjointeff")
            weldjointeff = obj.calculate_Component()
        try:
            allowablestresss = data['allowablestresss']
        except:
            obj = Newton(ComponentID, "allowablestresss")
            allowablestresss = obj.calculate_Component()
        try:
            structuralthickness = data['structuralthickness']
        except:
            obj = Newton(ComponentID, "structuralthickness")
            structuralthickness = obj.calculate_Component()
        try:
            compvolume = data['compvolume']
        except:
            obj = Newton(ComponentID, "compvolume")
            compvolume = obj.calculate_Component()
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
        # Stream
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
            exposedAmine = data['exposedAmine']
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
            environtH2S = data['environtH2S']
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
            maxOP = data['maxOP']
        except:
            obj = Newton(ComponentID, "maxOP")
            maxOP = obj.calculate_Operating()
        try:
            maxOT = data['maxOT']
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
            criticalTemp = data['criticalTemp']
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
            PHWater = data['PHWater']
        except:
            obj = Newton(ComponentID, "PHWater")
            PHWater = obj.calculate_Operating()
        try:
            H2Spressure = data['H2Spressure']
        except:
            obj = Newton(ComponentID, "H2Spressure")
            H2Spressure = obj.calculate_Operating()
        try:
            flowrate = data['flowrate']
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
        # RwExtcorTemperature
        try:
            externalcoating = data['externalcoating']
        except:
            externalcoating = rwcoat.externalcoating
        try:
            externalinsulation = data['externalinsulation']
        except:
            externalinsulation = rwcoat.externalinsulation
        try:
            internalcladding = data['internalcladding']
        except:
            internalcladding = rwcoat.internalcladding
        try:
            internalcoating = data['internalcoating']
        except:
            internalcoating = rwcoat.internalcoating
        try:
            internallining = data['internallining']
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
            internallinertype = data['internallinertype']
        except:
            internallinertype = rwcoat.internallinertype
        try:
            cladCorrosion = data['cladCorrosion']
        except:
            obj = Newton(ComponentID, "cladCorrosion")
            cladCorrosion = obj.calculate_Equipment()
        try:
            supportCoatingMaintain = data['supportCoatingMaintain']
        except:
            supportCoatingMaintain = rwcoat.supportconfignotallowcoatingmaint
        try:
            claddingthickness = data['claddingthickness']
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
                                               assessmentdate=datetime.now(),
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
                print("go test")
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
                rwinputca = models.RwInputCaLevel1(id=rwassessment, api_fluid=apiFluid,
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
                rwinputca = models.RwInputCaLevel1(id=rwassessment, api_fluid=apiFluid,
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
            ReCalculate.ReCalculate(rwassessment.id)
        except Exception as e:
            print(e)

    def saveData(self, data, ComponentID):
        try:
            MinDesignTemp = data['MinDesignTemp']
        except:
            obj = Newton(ComponentID, "MinDesignTemp")
            MinDesignTemp = obj.calculate()
            print('MinDesignTemp', MinDesignTemp)
        try:
            MaxDesignTemp = data['MaxDesignTemp']
        except:
            obj = Newton(ComponentID, "MaxDesignTemp")
            MaxDesignTemp = obj.calculate()
        try:
            DesignPressure = data['DesignPressure']
        except:
            obj = Newton(ComponentID, "DesignPressure")
            DesignPressure = obj.calculate()
        try:
            MaterialCostFactor = data['MaterialCostFactor']
        except:
            obj = Newton(ComponentID, "MaterialCostFactor")
            MaterialCostFactor = obj.calculate()
        try:
            tempRef = data['tempRef']
        except:
            obj = Newton(ComponentID, "tempRef")
            tempRef = obj.calculate()
        try:
            shellHieght = data['shellHieght']
        except:
            obj = Newton(ComponentID, "shellHieght")
            shellHieght = obj.calculate()
        try:
            distance = data['distance']
        except:
            obj = Newton(ComponentID, "distance")
            distance = obj.calculate()
        try:
            AdminControlUpset = data["AdminControlUpset"]
        except:
            AdminControlUpset = False
        try:
            ContainsDeadlegs = data['ContainsDeadlegs']
        except:
            ContainsDeadlegs = False
        try:
            CylicOper = data['CylicOper']
        except:
            CylicOper = False
        try:
            Highly = data['Highly']
        except:
            Highly = False
        try:
            Downtime = data['Downtime']
        except:
            Downtime = False
        try:
            ExternalEnvironment = data['ExternalEnvironment']
        except:
            ExternalEnvironment = ""
        try:
            HeatTraced = data['HeatTraced']
        except:
            HeatTraced = False
        try:
            InterfaceSoilWater = data['InterfaceSoilWater']
        except:
            InterfaceSoilWater = False
        try:
            LOM = data['LOM']
        except:
            LOM = False
        try:
            MFTF = data['MFTF']
        except:
            MFTF = False
        try:
            minTemp = data['minTemp']
        except:
            obj = Newton(ComponentID, "minTemp")
            minTemp = obj.calculate()
        try:
            OnlineMonitoring = data['OnlineMonitoring']
        except:
            OnlineMonitoring = "Amine high velocity corrosion - Corrosion coupons"
        try:
            PresenceofSulphides = data['PresenceofSulphides']
        except:
            PresenceofSulphides = False
        try:
            PresenceofSulphidesShutdown = data['PresenceofSulphidesShutdown']
        except:
            PresenceofSulphidesShutdown = False
        try:
            PressurisationControlled = data['PressurisationControlled']
        except:
            PressurisationControlled = False
        try:
            PWHT = data['PWHT']
        except:
            PWHT = False
        try:
            SteamedOut = data['SteamedOut']
        except:
            SteamedOut = False
        try:
            ThermalHistory = data['ThermalHistory']
        except:
            ThermalHistory = "None"
        try:
            EquOper = data['EquOper']
        except:
            EquOper = False
        try:
            EquipmentVolumn = data['EquipmentVolumn']
        except Exception as e:
            obj = Newton(ComponentID, "EquipmentVolumn")
            EquipmentVolumn = obj.calculate()
        # component
        try:
            NorminalDiameter = data['NorminalDiameter']
        except:
            obj = Newton(ComponentID, "NorminalDiameter")
            NorminalDiameter = obj.calculate()
        # print(NorminalDiameter)
        try:
            NorminalThickness = data['NorminalThickness']
        except:
            obj = Newton(ComponentID, "NorminalThickness")
            NorminalThickness = obj.calculate()

        ##
        try:
            CurrentThickness = data['CurrentThickness']
        except:
            obj = Newton(ComponentID, "CurrentThickness")
            CurrentThickness = obj.calculate()
        try:
            MinReqThickness = data['MinReqThickness']
        except:
            obj = Newton(ComponentID, "MinReqThickness")
            MinReqThickness = obj.calculate()
        try:
            CurrentCorrosionRate = data['CurrentCorrosionRate']
        except:
            obj = Newton(ComponentID, "CurrentCorrosionRate")
            CurrentCorrosionRate = obj.calculate()
        # print("aa1.3")
        try:
            BranchDiameter = data['BranchDiameter']
        except:
            BranchDiameter = 'Any branch less than or equal to 2" Nominal OD'
        # print(BranchDiameter)
        try:
            BranchJointType = data['BranchDiameter']
        except:
            BranchJointType = 'None'
        # print("tt1.4")
        try:
            MaxBrinell = data['MaxBrinell']
        except:
            MaxBrinell = 'Below 200'
        try:
            DeltaFATT = data['DeltaFATT']
        except:
            obj = Newton(ComponentID, "DeltaFATT")
            DeltaFATT = obj.calculate()
        try:
            ChemicalInjection = data['ChemicalInjection']
        except:
            ChemicalInjection = False
        try:
            HFICI = data['HFICI']
        except:
            HFICI = False
        try:
            complex = data['complex']
        except:
            complex = "Above average"
        # print("tt1.44")
        try:
            CorrectiveAction = data['CorrectiveAction']
        except:
            CorrectiveAction = "None"
        try:
            PresenceCracks = data['PresenceCracks']
        except:
            PresenceCracks = False
        try:
            CylicLoad = data['CylicLoad']
        except:
            CylicLoad = "None"
        try:
            DFDI = data['DFDI']
        except:
            DFDI = False
        # print("tt.124")
        try:
            NumberPipeFittings = data['NumberPipeFittings']
        except:
            NumberPipeFittings = "More than 10"
        try:
            PipeCondition = data['PipeCondition']
        except:
            PipeCondition = "Broken gussets or gussets welded directly to pipe"
        try:
            PreviousFailures = data['PreviousFailures']
        except:
            PreviousFailures = "None"
        try:
            ShakingAmount = data['ShakingAmount']
        except:
            ShakingAmount = "Minor"
        try:
            VASD = data['VASD']
        except:
            VASD = False
        try:
            timeShakingPipe = data['timeShakingPipe']
        except:
            timeShakingPipe = "13 to 52 weeks"
        # print("aa99")
        try:
            weldjointeff = data['weldjointeff']
        except:
            obj = Newton(ComponentID, "weldjointeff")
            weldjointeff = obj.calculate()
        # print("mm1")
        try:
            allowablestresss = data['allowablestresss']
        except:
            obj = Newton(ComponentID, "allowablestresss")
            allowablestresss = obj.calculate()
        # print("tt1,5")
        try:
            structuralthickness = data['structuralthickness']
        except:
            obj = Newton(ComponentID, "structuralthickness")
            structuralthickness = obj.calculate()
        # print("11010")
        try:
            compvolume = data['compvolume']
        except:
            obj = Newton(ComponentID, "compvolume")
            compvolume = obj.calculate()
        try:
            HthaDamage = data['HthaDamage']
        except:
            HthaDamage = False
        try:
            MinStructuralThickness = data['MinStructuralThickness']
        except:
            MinStructuralThickness = False
        try:
            Fabricatedsteel = data['Fabricatedsteel']
        except:
            Fabricatedsteel = False
        try:
            EquipmentSatisfied = data['EquipmentSatisfied']
        except:
            EquipmentSatisfied = False
        try:
            NominalOperating = data['NominalOperating']
        except:
            NominalOperating = False
        try:
            Cetgreaterorequal = data['Cetgreaterorequal']
        except:
            Cetgreaterorequal = False
        try:
            Cyclicservice = data['Cyclicservice']
        except:
            Cyclicservice = False
        try:
            equipmentCircuit = data['equipmentCircuit']
        except:
            equipmentCircuit = False
        try:
            confidencecr = data['confidencecr']
        except:
            confidencecr = "Low"
        # print("10t")
        ##
        try:
            AminSolution = data['AminSolution']
        except:
            AminSolution = "Diethanolamine DEA"
        try:
            AqueOp = data['AqueOp']
        except:
            AqueOp = False
        try:
            AqueShutdown = data['AqueShutdown']
        except:
            AqueShutdown = False
        try:
            ToxicConstituents = data['ToxicConstituents']
        except:
            ToxicConstituents = False
        try:
            EnvCaustic = data['EnvCaustic']
        except:
            EnvCaustic = False
        try:
            ChlorideIon = data['ChlorideIon']
        except:
            obj = Newton(ComponentID, "ChlorideIon")
            ChlorideIon = obj.calculate()
        try:
            CO3 = data['CO3']
        except:
            obj = Newton(ComponentID, "CO3")
            CO3 = obj.calculate()
        try:
            PresenceCyanides = data['PresenceCyanides']
        except:
            PresenceCyanides = False
        try:
            exposureAcid = data['exposureAcid']
        except:
            exposureAcid = False
        try:
            ExposedSulfur = data['ExposedSulfur']
        except:
            ExposedSulfur = False
        try:
            ExposureAmine = data['ExposureAmine']
        except:
            ExposureAmine = "High Rich Amine"
        try:
            EnvCH2S = data['EnvCH2S']
        except:
            EnvCH2S = False
        try:
            H2SInWater = data['H2SInWater']
        except:
            obj = Newton(ComponentID, "H2SInWater")
            H2SInWater = obj.calculate()
        try:
            hydrogen = data['hydrogen']
        except:
            hydrogen = False
        try:
            HydrogenFluoric = data['HydrogenFluoric']
        except:
            HydrogenFluoric = False
        try:
            materialExposedFluid = data['materialExposedFluid']
        except:
            materialExposedFluid = False
        try:
            maxOP = data['maxOP']
        except:
            obj = Newton(ComponentID, "maxOP")
            maxOP = obj.calculate()
        try:
            maxOT = data['maxOT']
        except:
            obj = Newton(ComponentID, "maxOT")
            maxOT = obj.calculate()
        try:
            minOP = data['minOP']
        except:
            obj = Newton(ComponentID, "minOP")
            minOP = obj.calculate()
        try:
            minOT = data['minOT']
        except:
            obj = Newton(ComponentID, "minOT")
            minOT = obj.calculate()
        try:
            CriticalTemp = data['CriticalTemp']
        except:
            obj = Newton(ComponentID, "CriticalTemp")
            CriticalTemp = obj.calculate()
        try:
            NaOHConcentration = data['NaOHConcentration']
        except:
            obj = Newton(ComponentID, "NaOHConcentration")
            NaOHConcentration = obj.calculate()
        try:
            ReleasePercentToxic = data['ReleasePercentToxic']
        except:
            obj = Newton(ComponentID, "ReleasePercentToxic")
            ReleasePercentToxic = obj.calculate()
        try:
            PHWater = data['PHWater']
        except:
            obj = Newton(ComponentID, "PHWater")
            PHWater = obj.calculate()
        try:
            PHWater = data['OpHydroPressure']
        except:
            obj = Newton(ComponentID, "OpHydroPressure")
            OpHydroPressure = obj.calculate()
        try:
            flowrate = data['flowrate']
        except:
            obj = Newton(ComponentID, "flowrate")
            flowrate = obj.calculate()

        ##
        try:
            OP1 = data['OP1']
        except:
            obj = Newton(ComponentID, "OP1")
            OP1 = obj.calculate()
        try:
            OP2 = data['OP2']
        except:
            obj = Newton(ComponentID, "OP2")
            OP2 = obj.calculate()
        try:
            OP3 = data['OP3']
        except:
            obj = Newton(ComponentID, "OP3")
            OP3 = obj.calculate()
        try:
            OP4 = data['OP4']
        except:
            obj = Newton(ComponentID, "OP4")
            OP4 = obj.calculate()
        try:
            OP5 = data['OP5']
        except:
            obj = Newton(ComponentID, "OP5")
            OP5 = obj.calculate()
        try:
            OP6 = data['OP6']
        except:
            obj = Newton(ComponentID, "OP6")
            OP6 = obj.calculate()
        try:
            OP7 = data['OP7']
        except:
            obj = Newton(ComponentID, "OP7")
            OP7 = obj.calculate()
        try:
            OP8 = data['OP8']
        except:
            obj = Newton(ComponentID, "OP8")
            OP8 = obj.calculate()
        try:
            OP9 = data['OP9']
        except:
            obj = Newton(ComponentID, "OP9")
            OP9 = obj.calculate()
        try:
            OP10 = data['OP10']
        except:
            obj = Newton(ComponentID, "OP10")
            OP10 = obj.calculate()

        ##
        try:
            ExternalCoating = data['ExternalCoating']
        except:
            ExternalCoating = False
        try:
            ExternalInsulation = data['ExternalInsulation']
        except:
            ExternalInsulation = False
        try:
            InternalCladding = data['InternalCladding']
        except:
            InternalCladding = False
        try:
            InternalCoating = data['InternalCoating']
        except:
            InternalCoating = False
        try:
            InternalLining = data['InternalLining']
        except:
            InternalLining = False
        try:
            ExternalCoatingDate = data['ExternalCoatingDate']
        except:
            ExternalCoatingDate = datetime.now()
        try:
            ExternalCoatingQuality = data['ExternalCoatingQuality']
        except:
            ExternalCoatingQuality = "High coating quality"
        try:
            ExternalInsulationType = data['ExternalInsulationType']
        except:
            ExternalInsulationType = ""
        try:
            InsulationCondition = data['InsulationCondition']
        except:
            InsulationCondition = ""
        try:
            InsulationCholride = data['InsulationCholride']
        except:
            InsulationCholride = False
        try:
            InternalLinerCondition = data['InternalLinerCondition']
        except:
            InternalLinerCondition = ""
        try:
            InternalLinerType = data['InternalLinerType']
        except:
            InternalLinerType = ""
        try:
            CladdingCorrosionRate = data['CladdingCorrosionRate']
        except:
            obj = Newton(ComponentID, "CladdingCorrosionRate")
            CladdingCorrosionRate = obj.calculate()
        try:
            supportMaterial = data['supportMaterial']
        except:
            supportMaterial = False
        try:
            claddingthickness = data['claddingthickness']
        except:
            obj = Newton(ComponentID, "claddingthickness")
            claddingthickness = obj.calculate()

        ## input stream
        try:
            CorrosionAllowance = data['CorrosionAllowance']
        except:
            CorrosionAllowance = False
        try:
            Material = data['Material']
        except:
            Material = ""
        try:
            BrittleFacture = data['BrittleFacture']
        except:
            BrittleFacture = False
        try:
            SigmaPhase = data['SigmaPhase']
        except:
            obj = Newton(ComponentID, "SigmaPhase")
            SigmaPhase = obj.calculate()
        try:
            SulfurContent = data['SulfurContent']
        except:
            SulfurContent = ""
        try:
            heatTreatment = data['heatTreatment']
        except:
            heatTreatment = ""
        try:
            PTAMaterialGrade = data['PTAMaterialGrade']
        except:
            PTAMaterialGrade = ""
        try:
            HTHAMaterialGrade = data['HTHAMaterialGrade']
        except:
            HTHAMaterialGrade = ""
        try:
            MaterialPTA = data['MaterialPTA']
        except:
            MaterialPTA = False
        try:
            MaterialHTHA = data['MaterialHTHA']
        except:
            MaterialHTHA = False
        try:
            AusteniticSteel = data['AusteniticSteel']
        except:
            AusteniticSteel = False
        try:
            SusceptibleTemper = data['SusceptibleTemper']
        except:
            SusceptibleTemper = False
        try:
            CarbonAlloySteel = data['CarbonAlloySteel']
        except:
            obj = Newton(ComponentID, "CarbonAlloySteel")
            CarbonAlloySteel = obj.calculate()
        try:
            NickelAlloy = data['NickelAlloy']
        except:
            NickelAlloy = False
        try:
            Chromium = data['Chromium']
        except:
            Chromium = False
        try:
            yieldstrength = data['yieldstrength']
        except:
            obj = Newton(ComponentID, "yieldstrength")
            yieldstrength = obj.calculate()
        try:
            tensilestrength = data['tensilestrength']
        except:
            obj = Newton(ComponentID, "tensilestrength")
            tensilestrength = obj.calculate()
        # print("ooooo")
        ## input CA
        try:
            APIFluid = data['APIFluid']
        except:
            APIFluid = ""
        # try:
        #     Systerm = data['Systerm']
        # except:
        #     Systerm = ""
        try:
            ReleaseDuration = data['ReleaseDuration']
        except:
            ReleaseDuration = ""
        try:
            DetectionType = data['DetectionType']
        except:
            DetectionType = ""
        try:
            IsulationType = data['IsulationType']
        except:
            IsulationType = ""
        try:
            MittigationSysterm = data['MittigationSysterm']
        except:
            MittigationSysterm = ""
        try:
            EquipmentCost = data['EquipmentCost']
        except:
            EquipmentCost = 0
        try:
            InjureCost = data['InjureCost']
        except:
            InjureCost = 0
        try:
            EnvironmentCost = data['EnvironmentCost']
        except:
            EnvironmentCost = 0
        try:
            ToxicPercent = data['ToxicPercent']
        except:
            ToxicPercent = 0
        try:
            PersonDensity = data['PersonDensity']
        except:
            PersonDensity = 0
        try:
            ProductionCost = data['ProductionCost']
        except:
            ProductionCost = 0
        try:
            MassInventory = data['MassInventory']
        except:
            MassInventory = 0
        try:
            MassComponent = data['MassComponent']
        except:
            MassComponent = 0

        ### input tank CA
        try:
            fluidHeight = data['fluidHeight']
        except:
            obj = Newton(ComponentID, "fluidHeight")
            fluidHeight = obj.calculate()
        try:
            tankDiameter = data['tankDiameter']
        except:
            tankDiameter = 0
        try:
            preventBarrier = data['preventBarrier']
        except:
            preventBarrier = 0
        try:
            envsensitivity = data['envsensitivity']
        except:
            envsensitivity = "High"
        try:
            fluidLeaveDike = data['fluidLeaveDike']
        except:
            fluidLeaveDike = 0
        try:
            fluidOffsite = data['fluidOffsite']
        except:
            fluidOffsite = 0
        try:
            fluidOnsite = data['fluidOnsite']
        except:
            fluidOnsite = 0
        try:
            fluid = data['fluid']
        except:
            fluid = "Gasoline"

        ### input Equiment Tank
        try:
            componentWelded = data['componentWelded']
        except:
            componentWelded = False
        try:
            tankIsMaintain = data['tankIsMaintain']
        except:
            tankIsMaintain = False
        try:
            adjustSettlement = data['adjustSettlement']
        except:
            adjustSettlement = ""
        try:
            EnvSensitivity = data['EnvSensitivity']
        except:
            EnvSensitivity = ""

        try:
            soiltype = data['soiltype']
        except:
            soiltype = ""

        ## input component Tank
        # try:
        #     shellHieght = data['shellHieght']
        # except:
        #     obj = Newton(ComponentID, "shellHieght")
        #     shellHieght = obj.calculate()
        #     print("shellHieght",shellHieght)
        try:
            concreteFoundation = data['concreteFoundation']
        except:
            concreteFoundation = False
        try:
            severityVibration = data['severityVibration']
        except:
            severityVibration = ""

        print("Get data ok")

        comp = models.ComponentMaster.objects.get(componentid=ComponentID)
        if comp.componenttypeid_id == 8 or comp.componenttypeid_id == 9 or comp.componenttypeid_id == 12 or comp.componenttypeid_id == 13 or comp.componenttypeid_id == 14 or comp.componenttypeid_id == 15:
            checktank = 1
        else:
            checktank = 0
        Proposalname = "proposal" + str(models.RwAssessment.objects.filter(componentid=comp.componentid).count())
        print("Checktank", checktank)
        if (checktank == 0):
            try:
                rwassessment = models.RwAssessment(equipmentid_id=comp.equipmentid_id,
                                                   componentid_id=comp.componentid,
                                                   assessmentdate=datetime.datetime.now(),
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
                                                 containsdeadlegs=ContainsDeadlegs,
                                                 cyclicoperation=CylicOper,
                                                 highlydeadleginsp=Highly,
                                                 downtimeprotectionused=Downtime,
                                                 externalenvironment=ExternalEnvironment,
                                                 heattraced=HeatTraced,
                                                 interfacesoilwater=InterfaceSoilWater,
                                                 lineronlinemonitoring=LOM,
                                                 materialexposedtoclext=MFTF,
                                                 minreqtemperaturepressurisation=minTemp,
                                                 onlinemonitoring=OnlineMonitoring,
                                                 presencesulphideso2=PresenceofSulphides,
                                                 presencesulphideso2shutdown=PresenceofSulphidesShutdown,
                                                 pressurisationcontrolled=PressurisationControlled,
                                                 pwht=PWHT,
                                                 steamoutwaterflush=SteamedOut,
                                                 managementfactor=faci.managementfactor,
                                                 thermalhistory=ThermalHistory,
                                                 yearlowestexptemp=EquOper,
                                                 volume=EquipmentVolumn)
                rwequipment.save()
                rwcomponent = models.RwComponent(id=rwassessment,
                                                 nominaldiameter=NorminalDiameter,
                                                 nominalthickness=NorminalThickness,
                                                 currentthickness=CurrentThickness,
                                                 minreqthickness=MinReqThickness,
                                                 currentcorrosionrate=CurrentCorrosionRate,
                                                 branchdiameter=BranchDiameter,
                                                 branchjointtype=BranchJointType,
                                                 brinnelhardness=MaxBrinell,
                                                 deltafatt=DeltaFATT,
                                                 chemicalinjection=ChemicalInjection,
                                                 highlyinjectioninsp=HFICI,
                                                 complexityprotrusion=complex,
                                                 correctiveaction=CorrectiveAction,
                                                 crackspresent=PresenceCracks,
                                                 cyclicloadingwitin15_25m=CylicLoad,
                                                 damagefoundinspection=DFDI,
                                                 numberpipefittings=NumberPipeFittings,
                                                 pipecondition=PipeCondition,
                                                 previousfailures=PreviousFailures,
                                                 shakingamount=ShakingAmount,
                                                 shakingdetected=VASD,
                                                 shakingtime=timeShakingPipe,
                                                 weldjointefficiency=weldjointeff,
                                                 allowablestress=allowablestresss,
                                                 structuralthickness=structuralthickness,
                                                 componentvolume=compvolume,
                                                 hthadamage=HthaDamage,
                                                 minstructuralthickness=MinStructuralThickness,
                                                 fabricatedsteel=Fabricatedsteel,
                                                 equipmentsatisfied=EquipmentSatisfied,
                                                 nominaloperatingconditions=NominalOperating,
                                                 cetgreaterorequal=Cetgreaterorequal, cyclicservice=Cyclicservice,
                                                 equipmentcircuitshock=equipmentCircuit,
                                                 brittlefracturethickness=BrittleFacture,
                                                 confidencecorrosionrate=confidencecr)
                rwcomponent.save()
                rwstream = models.RwStream(id=rwassessment, aminesolution=AminSolution,
                                           aqueousoperation=AqueOp,
                                           aqueousshutdown=AqueShutdown,
                                           toxicconstituent=ToxicConstituents,
                                           caustic=EnvCaustic,
                                           chloride=ChlorideIon,
                                           co3concentration=CO3,
                                           cyanide=PresenceCyanides,
                                           exposedtogasamine=exposureAcid,
                                           exposedtosulphur=ExposedSulfur,
                                           exposuretoamine=ExposureAmine,
                                           h2s=EnvCH2S,
                                           h2sinwater=H2SInWater,
                                           hydrogen=hydrogen,
                                           hydrofluoric=HydrogenFluoric,
                                           materialexposedtoclint=materialExposedFluid,
                                           maxoperatingpressure=maxOP,
                                           maxoperatingtemperature=float(maxOT),
                                           minoperatingpressure=float(minOP),
                                           minoperatingtemperature=minOT,
                                           criticalexposuretemperature=CriticalTemp,
                                           naohconcentration=NaOHConcentration,
                                           releasefluidpercenttoxic=float(ReleasePercentToxic),
                                           waterph=float(PHWater),
                                           h2spartialpressure=float(OpHydroPressure),
                                           flowrate=float(flowrate))
                rwstream.save()
                rwexcor = models.RwExtcorTemperature(id=rwassessment, minus12tominus8=OP1,
                                                     minus8toplus6=OP2,
                                                     plus6toplus32=OP3,
                                                     plus32toplus71=OP4,
                                                     plus71toplus107=OP5,
                                                     plus107toplus121=OP6,
                                                     plus121toplus135=OP7,
                                                     plus135toplus162=OP8,
                                                     plus162toplus176=OP9,
                                                     morethanplus176=OP10)
                rwexcor.save()

                rwcoat = models.RwCoating(id=rwassessment, externalcoating=ExternalCoating,
                                          externalinsulation=ExternalInsulation,
                                          internalcladding=InternalCladding,
                                          internalcoating=InternalCoating,
                                          internallining=InternalLining,
                                          externalcoatingdate=ExternalCoatingDate,
                                          externalcoatingquality=ExternalCoatingQuality,
                                          externalinsulationtype=ExternalInsulationType,
                                          insulationcondition=InsulationCondition,
                                          insulationcontainschloride=InsulationCholride,
                                          internallinercondition=InternalLinerCondition,
                                          internallinertype=InternalLinerType,
                                          claddingcorrosionrate=CladdingCorrosionRate,
                                          supportconfignotallowcoatingmaint=supportMaterial,
                                          claddingthickness=claddingthickness)
                rwcoat.save()

                rwmaterial = models.RwMaterial(id=rwassessment, corrosionallowance=CorrosionAllowance,
                                               materialname=Material,
                                               designpressure=DesignPressure,
                                               designtemperature=MaxDesignTemp,
                                               mindesigntemperature=MinDesignTemp,
                                               brittlefracturethickness=BrittleFacture, sigmaphase=SigmaPhase,
                                               sulfurcontent=SulfurContent, heattreatment=heatTreatment,
                                               referencetemperature=tempRef,
                                               ptamaterialcode=PTAMaterialGrade,
                                               hthamaterialcode=HTHAMaterialGrade, ispta=MaterialPTA,
                                               ishtha=MaterialHTHA,
                                               austenitic=AusteniticSteel, temper=SusceptibleTemper,
                                               carbonlowalloy=CarbonAlloySteel,
                                               nickelbased=NickelAlloy, chromemoreequal12=Chromium,
                                               costfactor=MaterialCostFactor,
                                               yieldstrength=yieldstrength, tensilestrength=tensilestrength)
                rwmaterial.save()

                rwinputca = models.RwInputCaLevel1(id=rwassessment, api_fluid=APIFluid,
                                                   release_duration=ReleaseDuration,
                                                   detection_type=DetectionType,
                                                   isulation_type=IsulationType,
                                                   mitigation_system=MittigationSysterm,
                                                   equipment_cost=EquipmentCost, injure_cost=InjureCost,
                                                   evironment_cost=EnvironmentCost, toxic_percent=ToxicPercent,
                                                   personal_density=PersonDensity,
                                                   material_cost=MaterialCostFactor,
                                                   production_cost=ProductionCost, mass_inventory=MassInventory,
                                                   mass_component=MassComponent,
                                                   stored_pressure=float(minOP) * 6.895, stored_temp=minOT)
                rwinputca.save()
                ReCalculate.ReCalculate(rwassessment.id)
            except Exception as e:
                print (e)
        else:
            try:
                print("go tank")
                rwassessment = models.RwAssessment(equipmentid_id=comp.equipmentid_id, componentid_id=comp.componentid,
                                                   assessmentdate=datetime.datetime.now(),
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

                rwcomponent = models.RwComponent(id=rwassessment, nominaldiameter=NorminalDiameter,
                                                 allowablestress=allowablestresss,
                                                 nominalthickness=NorminalThickness, currentthickness=CurrentThickness,
                                                 minreqthickness=MinReqThickness,
                                                 currentcorrosionrate=CurrentCorrosionRate,
                                                 shellheight=shellHieght, damagefoundinspection=DFDI,
                                                 crackspresent=PresenceCracks,
                                                 # trampelements=trampElements,
                                                 releasepreventionbarrier=preventBarrier,
                                                 concretefoundation=concreteFoundation,
                                                 brinnelhardness=MaxBrinell,
                                                 structuralthickness=structuralthickness,
                                                 complexityprotrusion=complex,
                                                 minstructuralthickness=MinStructuralThickness,
                                                 severityofvibration=severityVibration,
                                                 brittlefracturethickness=BrittleFacture,
                                                 confidencecorrosionrate=confidencecr)
                rwcomponent.save()
                rwstream = models.RwStream(id=rwassessment, maxoperatingtemperature=maxOT,
                                           maxoperatingpressure=maxOP,
                                           minoperatingtemperature=minOT, minoperatingpressure=minOP,
                                           h2spartialpressure=float(OpHydroPressure),
                                           criticalexposuretemperature=CriticalTemp,
                                           tankfluidname=fluid, fluidheight=fluidHeight,
                                           fluidleavedikepercent=fluidLeaveDike,
                                           fluidleavedikeremainonsitepercent=fluidOnsite,
                                           fluidgooffsitepercent=fluidOffsite,
                                           naohconcentration=NaOHConcentration,
                                           releasefluidpercenttoxic=float(ReleasePercentToxic),
                                           chloride=ChlorideIon, co3concentration=CO3,
                                           h2sinwater=H2SInWater,
                                           waterph=float(PHWater), exposedtogasamine=exposureAcid,
                                           aminesolution=AminSolution,
                                           exposuretoamine=ExposureAmine, aqueousoperation=AqueOp, h2s=EnvCH2S,
                                           aqueousshutdown=AqueShutdown, cyanide=PresenceCyanides,
                                           hydrofluoric=HydrogenFluoric,
                                           caustic=EnvCaustic, hydrogen=hydrogen,
                                           materialexposedtoclint=materialExposedFluid,
                                           exposedtosulphur=ExposedSulfur)
                rwstream.save()

                rwexcor = models.RwExtcorTemperature(id=rwassessment, minus12tominus8=OP1, minus8toplus6=OP2,
                                                     plus6toplus32=OP3, plus32toplus71=OP4,
                                                     plus71toplus107=OP5,
                                                     plus107toplus121=OP6, plus121toplus135=OP7,
                                                     plus135toplus162=OP8, plus162toplus176=OP9,
                                                     morethanplus176=OP10)
                rwexcor.save()
                rwcoat = models.RwCoating(id=rwassessment, internalcoating=InternalCoating,
                                          externalcoating=ExternalCoating,
                                          externalcoatingdate=ExternalCoatingDate,
                                          externalcoatingquality=ExternalCoatingQuality,
                                          supportconfignotallowcoatingmaint=supportMaterial,
                                          internalcladding=InternalCladding,
                                          claddingcorrosionrate=CladdingCorrosionRate, internallining=InternalLining,
                                          internallinertype=InternalLinerType,
                                          internallinercondition=InternalLinerCondition,
                                          externalinsulation=ExternalInsulation,
                                          insulationcontainschloride=InsulationCholride,
                                          externalinsulationtype=ExternalInsulationType,
                                          insulationcondition=InsulationCondition,
                                          claddingthickness=claddingthickness
                                          )
                rwcoat.save()
                rwmaterial = models.RwMaterial(id=rwassessment, materialname=Material,
                                               designtemperature=MaxDesignTemp,
                                               mindesigntemperature=MinDesignTemp, designpressure=DesignPressure,
                                               referencetemperature=tempRef,
                                               # allowablestress=data['allowStress'],
                                               brittlefracturethickness=BrittleFacture,
                                               corrosionallowance=CorrosionAllowance,
                                               carbonlowalloy=CarbonAlloySteel, austenitic=AusteniticSteel,
                                               nickelbased=NickelAlloy,
                                               chromemoreequal12=Chromium,
                                               sulfurcontent=SulfurContent, heattreatment=heatTreatment,
                                               ispta=MaterialPTA, ptamaterialcode=PTAMaterialGrade,
                                               costfactor=MaterialCostFactor)
                rwmaterial.save()
                print("---------------1")
                rwinputca = models.RwInputCaTank(id=rwassessment, fluid_height=fluidHeight,
                                                 shell_course_height=shellHieght,
                                                 tank_diametter=tankDiameter, prevention_barrier=preventBarrier,
                                                 environ_sensitivity=envsensitivity,
                                                 p_lvdike=fluidLeaveDike, p_offsite=fluidOffsite,
                                                 p_onsite=fluidOnsite, soil_type=soiltype,
                                                 tank_fluid=fluid, api_fluid=APIFluid, sw=distance,
                                                 productioncost=ProductionCost)
                rwinputca.save()
                # Customize Caculate Here
                print("Save tank")
                ReCalculate.ReCalculate(rwassessment.id)
            except Exception as e:
                print("error check data:", e)
        # return redirect('damgeFactor', proposalID=rwassessment.id)
        print("okok")


if __name__ == "__main__":
    obj = REGULAR()
    data = []
    # obj.getDate(28)
    obj.regular_1(3)
    # obj.NowProposal(55)
    # obj.saveData(data, 206)
    # obj.saveTank(data,28)
    # obj.NowProposal(404)
    # obj.saveData(data,28)
    # obj.saveTank(data,76)
    # obj.goitank(data,25)

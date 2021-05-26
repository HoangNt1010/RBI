import os,sys
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

import traceback
import sys
import datetime
import math
from mpmath.calculus.optimization import Newton
from cloud import models

class Newton:
    X = []
    Y = []


    def __init__(self,ConponentID,value=""):
        self.n=len(self.X)
        self.componentID = ConponentID
        self.value=value
        self.n = len(self.X)
    def calculate_Equipment(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value == "minTemp":
                Thresholdmax = 10000
                Thresholdmin = -100
                output = self.AddListInterEquipment("minTemp")
            elif self.value == "distance":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterEquipment("distance")
            elif self.value == "EquipmentVolumn":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterEquipment("EquipmentVolumn")
            elif self.value == "cladCorrosion":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterEquipment("cladCorrosion")
            elif self.value == "claddingthickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterEquipment("claddingthickness")
            elif self.value == "productioncost":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterEquipment("productioncost")
            else:
                print("Value fail",)
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            if self.Y[0]:
                return self.Y[0]
            else:
                return self.Y[1]
    def calculate_Component(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value == "tankDiameter":
                Thresholdmax = 10000
                Thresholdmin = 0
                output = self.AddListInterComponent("tankDiameter")
            elif self.value == "NorminalThickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("NorminalThickness")
            elif self.value == "nominaldiameter":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("nominaldiameter")
            elif self.value == "CurrentThickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("CurrentThickness")
            elif self.value == "MinReqThickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("MinReqThickness")
            elif self.value == "structuralthickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("structuralthickness")
            elif self.value == "CurrentCorrosionRate":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("CurrentCorrosionRate")
            elif self.value == "shellHieght":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("shellHieght")
            elif self.value == "weldjointeff":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("weldjointeff")
            elif self.value == "compvolume":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("compvolume")
            elif self.value == "allowablestresss":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("allowablestresss")
            elif self.value == "BrittleFacture":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("BrittleFacture")
            elif self.value == "deltafatt":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterComponent("deltafatt")
            else:
                print("Value fail")
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            if self.Y[0]:
                return self.Y[0]
            elif self.Y[1]:
                return self.Y[1]

    def calculate_Operating(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value == "maxOT":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInterOperating("maxOT")
            elif self.value == "maxOP":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInterOperating("maxOP")
            elif self.value == "minOT":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInterOperating("minOT")
            elif self.value == "minOP":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInterOperating("minOP")
            elif self.value == "H2Spressure":
                Thresholdmax = 1000
                Thresholdmin = 0
                output = self.AddListInterOperating("H2Spressure")
            elif self.value == "criticalTemp":
                Thresholdmax = 1000
                Thresholdmin = 0
                output = self.AddListInterOperating("criticalTemp")
            elif self.value == "fluidHeight":
                Thresholdmax = 1000
                Thresholdmin = 0
                output = self.AddListInterOperating("fluidHeight")
            elif self.value == "fluidLeaveDike":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInterOperating("fluidLeaveDike")
            elif self.value == "fluidOnsite":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInterOperating("fluidOnsite")
            elif self.value == "fluidOffsite":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInterOperating("fluidOffsite")
            elif self.value == "naohConcent":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInterOperating("naohConcent")
            elif self.value == "releasePercentToxic":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInterOperating("releasePercentToxic")
            elif self.value == "chlorideIon":
                Thresholdmax = 1000000
                Thresholdmin = 0
            elif self.value == "co3":
                Thresholdmax = 1000000
                Thresholdmin = 0
                output = self.AddListInterOperating("co3")
            elif self.value == "h2sContent":
                Thresholdmax = 1000000
                Thresholdmin = 0
                output = self.AddListInterOperating("co3")
            elif self.value == "PHWater":
                Thresholdmax = 15
                Thresholdmin = 0
                output = self.AddListInterOperating("PHWater")
            elif self.value == "flowrate":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterOperating("flowrate")
            elif self.value == "h2sinwater":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterOperating("h2sinwater")
            elif self.value == "liquidlevel":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterOperating("liquidlevel")
            else:
                print("Value fail")
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            return self.Y[0]
    def calculate_RwExtcorTemperature(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value == "OP1":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP1")
            elif self.value == "OP2":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP2")
            elif self.value == "OP3":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP3")
            elif self.value == "OP4":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP4")
            elif self.value == "OP5":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP5")
            elif self.value == "OP6":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP6")
            elif self.value == "OP7":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP7")
            elif self.value == "OP8":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP8")
            elif self.value == "OP9":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP9")
            elif self.value == "OP10":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwExtcor("OP10")
            else:
                print("Value fail")
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            return self.Y[0]
    def calculate_Material(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value == "designtemperature":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("designtemperature")
            elif self.value == "mindesigntemperature":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("mindesigntemperature")
            elif self.value == "designpressure":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("designpressure")
            elif self.value == "refTemp":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("refTemp")
            elif self.value == "corrosionAllow":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("corrosionAllow")
            elif self.value == "materialCostFactor":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("materialCostFactor")
            elif self.value == "yieldstrength":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("yieldstrength")
            elif self.value == "tensilestrength":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterMaterial("tensilestrength")
            else:
                print("Value fail",)
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            if self.Y[0]:
                return self.Y[0]
            else:
                return self.Y[1]

    def calculate_RwinputCaLevel1(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value == "equipment_cost":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("equipment_cost")
            elif self.value == "injure_cost":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("injure_cost")
            elif self.value == "evironment_cost":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("evironment_cost")
            elif self.value == "personal_density":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("personal_density")
            elif self.value == "production_cost":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("production_cost")
            elif self.value == "mass_inventory":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("mass_inventory")
            elif self.value == "mass_component":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("mass_component")
            elif self.value == "toxic_percent":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("toxic_percent")
            elif self.value == "process_unit":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("process_unit")
            elif self.value == "outage_multiplier":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInterRwinputCaLevel1("outage_multiplier")
            else:
                print("Value fail",)
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            if self.Y[0]:
                return self.Y[0]
            elif self.Y[1]:
                return self.Y[1]
            else:
                return 0
    def calculate(self):
        try:
            Thresholdmax = 0
            Thresholdmin = 0
            output = 0
            if self.value=="minTemp":
                Thresholdmax = 10000
                Thresholdmin = -100
                output= self.AddListInter("minTemp")
            elif self.value == "distance":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("distance")
            elif self.value=="EquipmentVolumn":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("EquipmentVolumn")
            elif self.value == "NorminalDiameter":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("NorminalDiameter")
            elif self.value == "NorminalThickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("NorminalThickness")
            elif self.value == "CurrentThickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("CurrentThickness")
            elif self.value == "MinReqThickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("MinReqThickness")
            elif self.value == "CurrentCorrosionRate":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("CurrentCorrosionRate")
            elif self.value == "DeltaFATT":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("DeltaFATT")
            elif self.value == "weldjointeff":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("weldjointeff")
            elif self.value == "allowablestresss":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("allowablestresss")
            elif self.value == "structuralthickness":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("structuralthickness")
            elif self.value == "compvolume":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("compvolume")
            elif self.value == "ChlorideIon":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("ChlorideIon")
            elif self.value == "CO3":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("CO3")
            elif self.value == "H2SInWater":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("H2SInWater")
            elif self.value == "maxOP":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("maxOP")
            elif self.value == "maxOT":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("maxOT")
            elif self.value == "minOP":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("minOP")
            elif self.value == "minOT":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("minOT")
            elif self.value == "CriticalTemp":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("CriticalTemp")
            elif self.value == "NaOHConcentration":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("NaOHConcentration")
            elif self.value == "ReleasePercentToxic":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("ReleasePercentToxic")
            elif self.value == "PHWater":
                Thresholdmax = 15
                Thresholdmin = 0
                output = self.AddListInter("PHWater")
            elif self.value == "OpHydroPressure":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("OpHydroPressure")
            elif self.value == "flowrate":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("flowrate")
            elif self.value == "OP1":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP1")
            elif self.value == "OP2":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP2")
            elif self.value == "OP3":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP3")
            elif self.value == "OP4":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP4")
            elif self.value == "OP5":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP5")
            elif self.value == "OP6":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP6")
            elif self.value == "OP7":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP7")
            elif self.value == "OP8":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP8")
            elif self.value == "OP9":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP9")
            elif self.value == "OP10":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("OP10")
            elif self.value == "CladdingCorrosionRate":
                Thresholdmax = 1000
                Thresholdmin = 0
                output = self.AddListInter("CladdingCorrosionRate")
            elif self.value == "claddingthickness":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("claddingthickness")
            elif self.value == "DesignPressure":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("DesignPressure")
            elif self.value == "MaxDesignTemp":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("MaxDesignTemp")
            elif self.value == "MinDesignTemp":
                Thresholdmax = 1000
                Thresholdmin = -100
                output = self.AddListInter("MinDesignTemp")
            elif self.value == "SigmaPhase":
                Thresholdmax = 100
                Thresholdmin = 0
                output = self.AddListInter("SigmaPhase")
            elif self.value == "tempRef":
                Thresholdmax = 1000
                Thresholdmin = -10
                output = self.AddListInter("tempRef")
            elif self.value == "CarbonAlloySteel":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("CarbonAlloySteel")
            elif self.value == "MaterialCostFactor":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("MaterialCostFactor")
            elif self.value == "yieldstrength":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("yieldstrength")
            elif self.value == "tensilestrength":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("tensilestrength")
            elif self.value == "shellHieght":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("shellHieght")
            elif self.value == "fluidHeight":
                Thresholdmax = 100000
                Thresholdmin = 0
                output = self.AddListInter("fluidHeight")
            else:
                print("Value fail")
            if (output>Thresholdmax or output<Thresholdmin):
                output = (max(self.Y)+min(self.Y))/2
            self.X.clear()
            self.Y.clear()
            return output
        except Exception as e:
            print("error at calculate",e)
            return self.Y[0]
    def AddListInterRwinputCaLevel1(self,value6):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if (value6 == "equipment_cost"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.equipment_cost)
            elif (value6 == "injure_cost"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.injure_cost)
            elif (value6 == "evironment_cost"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.evironment_cost)
            elif (value6 == "personal_density"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.personal_density)
            elif (value6 == "production_cost"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.production_cost)
            elif (value6 == "mass_inventory"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.mass_inventory)
            elif (value6 == "mass_component"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.mass_component)
            elif (value6 == "toxic_percent"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.toxic_percent)
            elif (value6 == "process_unit"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.process_unit)
            elif (value6 == "outage_multiplier"):
                rwinputca = models.RwInputCaLevel1.objects.get(id=ass.id)
                self.Y.append(rwinputca.outage_multiplier)
            else:
                print("AddListInterEquipment")
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t = (datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a = self.__interpolation(t)
        return a
    def AddListInterMaterial(self,value5):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if (value5 == "designtemperature"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.designtemperature)
            elif (value5 == "mindesigntemperature"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.mindesigntemperature)
            elif (value5 == "designpressure"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.designpressure)
            elif (value5 == "refTemp"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.referencetemperature)
            elif (value5 == "corrosionAllow"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.corrosionallowance)
            elif (value5 == "materialCostFactor"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.costfactor)
            elif (value5 == "yieldstrength"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.yieldstrength)
            elif (value5 == "tensilestrength"):
                rwmaterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(rwmaterial.tensilestrength)
            else:
                print("AddListInterEquipment")
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t = (datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a = self.__interpolation(t)
        return a
    def AddListInterRwExtcor(self,value4):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if value4 == "OP1":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.minus12tominus8)
            elif value4 == "OP2":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.minus8toplus6)
            elif value4 == "OP3":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus6toplus32)
            elif value4 == "OP4":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus32toplus71)
            elif value4 == "OP5":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus71toplus107)
            elif value4 == "OP6":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus107toplus121)
            elif value4 == "OP7":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus121toplus135)
            elif value4 == "OP8":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus135toplus162)
            elif value4 == "OP9":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus162toplus176)
            elif value4 == "OP10":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.morethanplus176)
            else:
                print("AddListInterEquipment")
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t = (datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a = self.__interpolation(t)
        return a
    def AddListInterEquipment(self,value0):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if (value0 == "minTemp"):
                Equiment = models.RwEquipment.objects.get(id=ass.id)
                self.Y.append(Equiment.minreqtemperaturepressurisation)
            elif (value0 == "EquipmentVolumn"):
                Equiment = models.RwEquipment.objects.get(id=ass.id)
                self.Y.append(Equiment.volume)
            elif (value0 == "distance"):
                Equiment = models.RwEquipment.objects.get(id=ass.id)
                self.Y.append(Equiment.distancetogroundwater)
            elif (value0 == "cladCorrosion"):
                rwcoat = models.RwCoating.objects.get(id=ass.id)
                self.Y.append(rwcoat.claddingcorrosionrate)
            elif (value0 == "claddingthickness"):
                rwcoat = models.RwCoating.objects.get(id=ass.id)
                self.Y.append(rwcoat.claddingthickness)
            elif (value0 == "productioncost"):
                rwcatank = models.RwInputCaTank.objects.get(id=ass.id)
                self.Y.append(rwcatank.productioncost)
            else:
                print("AddListInterEquipment")
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t = (datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a = self.__interpolation(t)
        return a
    def AddListInterComponent(self,value2):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if (value2 == "tankDiameter"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.nominaldiameter)
            elif (value2 == "NorminalThickness"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.nominalthickness)
            elif (value2 == "nominaldiameter"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.nominaldiameter)
            elif (value2 == "CurrentThickness"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.currentthickness)
            elif (value2 == "MinReqThickness"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.minreqthickness)
            elif (value2 == "structuralthickness"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.structuralthickness)
            elif (value2 == "CurrentCorrosionRate"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.currentcorrosionrate)
            elif (value2 == "shellHieght"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.shellheight)
            elif (value2 == "weldjointeff"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.weldjointefficiency)
            elif (value2 == "compvolume"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.componentvolume)
            elif (value2 == "allowablestresss"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.allowablestress)
            elif (value2 == "BrittleFacture"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.brittlefracturethickness)
            elif (value2 == "deltafatt"):
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.deltafatt)
            else:
                print("AddListInterComponent")
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t = (datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a = self.__interpolation(t)
        return a
    def AddListInterOperating(self,value3):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if (value3 == "maxOT"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.maxoperatingtemperature)
            elif (value3 == "maxOP"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.maxoperatingpressure)
            elif (value3 == "minOT"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.minoperatingtemperature)
            elif (value3 == "minOP"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.minoperatingpressure)
            elif (value3 == "H2Spressure"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.h2spartialpressure)
            elif (value3 == "criticalTemp"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.criticalexposuretemperature)
            elif (value3 == "fluidHeight"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.fluidheight)
            elif (value3 == "fluidLeaveDike"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.fluidleavedikepercent)
            elif (value3 == "fluidOnsite"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.fluidleavedikeremainonsitepercent)
            elif (value3 == "fluidOffsite"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.fluidgooffsitepercent)
            elif (value3 == "naohConcent"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.naohconcentration)
            elif (value3 == "releasePercentToxic"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.releasefluidpercenttoxic)
            elif (value3 == "chlorideIon"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.chloride)
            elif (value3 == "co3"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.co3concentration)
            elif (value3 == "h2sContent"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.h2sinwater)
            elif (value3 == "PHWater"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.waterph)
            elif (value3 == "flowrate"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.flowrate)
            elif (value3 == "h2sinwater"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.h2sinwater)
            elif (value3 == "liquidlevel"):
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.liquidlevel)
            else:
                print("AddListInterEquipment")
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t = (datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a = self.__interpolation(t)
        return a
    def AddListInter(self,value1):
        assm = models.RwAssessment.objects.filter(componentid=self.componentID)
        tmin = assm[0].create
        datatmin = tmin.year * 365 + tmin.month * 30 + tmin.day
        checkdate = -1
        for ass in assm:
            date = ass.create
            if ((date.year * 365 + date.month * 30 + date.day) - datatmin != checkdate):
                self.X.append((date.year * 365 + date.month * 30 + date.day) - datatmin)
            if(value1== "minTemp"):
                Equiment = models.RwEquipment.objects.get(id=ass.id)
                self.Y.append(Equiment.minreqtemperaturepressurisation)
            elif (value1 == "EquipmentVolumn"):
                Equiment = models.RwEquipment.objects.get(id=ass.id)
                self.Y.append(Equiment.volume)
            elif (value1 == "distance"):
                # print(ass.id)
                Equiment = models.RwEquipment.objects.get(id=ass.id)
                self.Y.append(Equiment.distancetogroundwater)
            elif value1 == "NorminalDiameter":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.nominaldiameter)
            elif value1== "NorminalThickness":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.nominalthickness)
            elif value1 == "CurrentThickness":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.currentthickness)
            elif value1 == "MinReqThickness":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.minreqthickness)
            elif value1 == "CurrentCorrosionRate":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.currentcorrosionrate)
            elif value1 == "DeltaFATT":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.deltafatt)
            elif value1 == "weldjointeff":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.weldjointefficiency)
            elif value1 == "allowablestresss":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.allowablestress)
            elif value1 == "structuralthickness":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.structuralthickness)
            elif value1 == "compvolume":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.componentvolume)
            elif value1 == "shellHieght":
                Component = models.RwComponent.objects.get(id=ass.id)
                self.Y.append(Component.shellheight)
            elif value1 == "ChlorideIon":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.chloride)
            elif value1 == "CO3":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.co3concentration)
            elif value1 == "H2SInWater":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.h2sinwater)
            elif value1 == "maxOP":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.maxoperatingpressure)
            elif value1 == "maxOT":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.maxoperatingtemperature)
            elif value1 == "minOP":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.minoperatingpressure)
            elif value1 == "minOT":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.minoperatingtemperature)
            elif value1 == "CriticalTemp":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.criticalexposuretemperature)
            elif value1 == "NaOHConcentration":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.naohconcentration)
            elif value1 == "ReleasePercentToxic":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.releasefluidpercenttoxic)
            elif value1 == "PHWater":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.waterph)
            elif value1 == "OpHydroPressure":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.h2spartialpressure)
            elif value1 == "flowrate":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.flowrate)
            elif value1 == "fluidHeight":
                stream = models.RwStream.objects.get(id=ass.id)
                self.Y.append(stream.fluidheight)
            elif value1 == "OP1":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.minus12tominus8)
            elif value1 == "OP2":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.minus8toplus6)
            elif value1 == "OP3":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus6toplus32)
            elif value1 == "OP4":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus32toplus71)
            elif value1 == "OP5":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus71toplus107)
            elif value1 == "OP6":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus107toplus121)
            elif value1 == "OP7":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus121toplus135)
            elif value1 == "OP8":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus135toplus162)
            elif value1 == "OP9":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.plus162toplus176)
            elif value1 == "OP10":
                excor = models.RwExtcorTemperature.objects.get(id=ass.id)
                self.Y.append(excor.morethanplus176)
            elif value1 == "CladdingCorrosionRate":
                coating = models.RwCoating.objects.get(id=ass.id)
                self.Y.append(coating.claddingcorrosionrate)
            elif value1 == "claddingthickness":
                coating = models.RwCoating.objects.get(id=ass.id)
                self.Y.append(coating.claddingthickness)
            elif value1 == "DesignPressure":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.designpressure)
            elif value1 == "MaxDesignTemp":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.designtemperature)
            elif value1 == "MinDesignTemp":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.mindesigntemperature)
            elif value1 == "SigmaPhase":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.sigmaphase)
            elif value1 == "tempRef":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.referencetemperature)
            elif value1 == "CarbonAlloySteel":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.carbonlowalloy)
            elif value1 == "MaterialCostFactor":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.costfactor)
            elif value1 == "yieldstrength":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.yieldstrength)
            elif value1 == "tensilestrength":
                meterial = models.RwMaterial.objects.get(id=ass.id)
                self.Y.append(meterial.tensilestrength)
            checkdate = (date.year * 365 + date.month * 30 + date.day) - datatmin
        self.n = len(self.X)
        datenow = datetime.datetime.now()
        t=(datenow.year * 365 + datenow.month * 30 + datenow.day) - datatmin
        a=  self.__interpolation(t)
        return a
    def __interpolation(self, t):
        try:
            # print("go go")
            c = [0 for _ in range(self.n)]
            w = [0 for _ in range(self.n)]
            for i in range (0, self.n):
                w[i]=self.Y[i]
                for j in reversed(range(i)):
                    #print(j)
                    w[j] = (w[j + 1] - w[j]) / (self.X[i] - self.X[j])
                c[i]=w[0]
            s = c[self.n-1]
            for i in reversed(range(self.n-1)):
                s = s * (t -self.X[i])+c[i]
            return s
        except Exception as e:
            print("error __interpolation",e )
            return 0

if __name__=="__main__":
        try:
            # obj = Newton(27, "DeltaFATT")
            # obj.calculate()
            # print(obj.calculate())
            obj = Newton(206,"fluidHeight")
            # obj.calculate()
            print("gia tri",obj.calculate())
            # print(math.log10(65))
        except Exception as e:
            print("error in main interpolation",e)
            traceback.print_exc()
            sys.exit(1)

# from django.core.mail import EmailMessage
# Email = EmailMessage("aa", "aa", to=["doanhtuan14111997@gmail.com"])
# Email.send()

# DFm =models.DMItems.objects.get(dmitemid=1)
# print(DFm.dmdescription)





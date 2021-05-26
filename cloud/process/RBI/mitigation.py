import os,sys
from cloud import models
from cloud.process.RBI import FinancialCOF,Detail_DM_CAL,mitigationCoF,CA_Flammable,ToxicConsequenceArea
from cloud.process.RBI import fastCalulate as ReCalculate
from cloud.process.WebUI import roundData
def ShowThining(proposalID):
    try:
        data = []
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # print("check low", rwcomponent.confidencecorrosionrate)
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        damageMachinsm=models.RwDamageMechanism.objects.filter(id_dm=proposalID)[0]
        # damageMachinsm = models.RwDamageMechanism.objects.get(id_dm=proposalID)
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
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname

        obj['AllowableStress'] = rwcomponent.allowablestress
        obj['MinimunRequiredThickness'] = rwcomponent.minreqthickness
        obj['WeltJointEfficiency'] = rwcomponent.weldjointefficiency
        # print('WeltJointEfficiency'+str(obj['WeltJointEfficiency']))
        obj['CorrosionRate'] = rwcomponent.currentcorrosionrate
        obj['Diameter'] = rwcomponent.nominaldiameter
        obj['NominalThickness'] = rwcomponent.nominalthickness
        obj['CurentThickness'] = rwcomponent.currentthickness
        obj['ChemicalInjection'] = rwcomponent.chemicalinjection
        obj['HighlyEffectiveInspectionforChemicalInjection'] = rwcomponent.highlyinjectioninsp
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['deadLegs'] = rwequipment.containsdeadlegs
        obj['InternalCladding'] = rwcoat.internalcladding
        obj['CladdingThickness'] = rwcoat.claddingthickness
        obj['CladdingCorrosionRate'] = rwcoat.claddingcorrosionrate
        obj['confidencecorrosionrate'] = rwcomponent.confidencecorrosionrate
        obj['YeildStrength'] = rwmaterial.yieldstrength
        obj['TensileStrength'] = rwmaterial.tensilestrength
        obj['DesignPressure'] = rwmaterial.designpressure
        obj['Onlinemonitoring'] = rwequipment.onlinemonitoring
        obj['HighEffectiveDeadlegs'] = rwequipment.highlydeadleginsp
        obj['LastInspectionDate'] = damageMachinsm.lastinspdate.strftime('%Y-%m-%d')
        obj['NumberofInspection'] = damageMachinsm.numberofinspections

        obj['shapeFactor'] = comptype.shapefactor
        obj['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename

        thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                     obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                     rwmaterial.corrosionallowance, bool(rwcomponent.releasepreventionbarrier),
                                     obj['CladdingThickness'],
                                     obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                     0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                     bool(obj['deadLegs']), rwequipment.tankismaintained,
                                     rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                     obj['WeltJointEfficiency'], obj['AllowableStress'], obj['TensileStrength'],
                                     obj['YeildStrength'], rwcomponent.structuralthickness,
                                     rwcomponent.minstructuralthickness, obj['DesignPressure'], obj['shapeFactor'],
                                     obj['confidencecorrosionrate'], EquipmentType, rwassessment.assessmentdate,
                                     rwassessment.commisstiondate, ComponentNumber, APIComponentType)

        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        dataNominalThicknessX = []
        dataNominalThicknessY0 = []
        dataNominalThicknessY1 = []
        dataNominalThicknessY2 = []
        #
        dataCurentThicknessX = []
        dataCurentThicknessY0 = []
        dataCurentThicknessY1 = []
        dataCurentThicknessY2 = []
        #
        dataCorrosionRateX = []
        dataCorrosionRateY0 = []
        dataCorrosionRateY1 = []
        dataCorrosionRateY2 = []
        # Minimum Required Thickness
        dataMinimunRequiredThicknessX = []
        dataMinimunRequiredThicknessY0 = []
        dataMinimunRequiredThicknessY1 = []
        dataMinimunRequiredThicknessY2 = []
        #Nominal thickness
        #Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename

        # Df_CUI
        objCui={}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename

        # DF_BRITTLE
        objBri = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objBri['ComponentNumber'] = ComponentNumber
        objBri['EquipmentNumber'] = EquipmentName
        objBri['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objBri['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objBri['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objBri['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objBri['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objBri['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objBri['PWHT'] = bool(rwequipment.pwht)
        objBri['REF_TEMP'] = rwmaterial.referencetemperature
        objBri['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness
        objBri['FABRICATED_STEEL'] = bool(rwcomponent.fabricatedsteel)
        objBri['EQUIPMENT_SATISFIED'] = bool(rwcomponent.equipmentsatisfied)
        objBri['NOMINAL_OPERATING_CONDITIONS'] = bool(rwcomponent.nominaloperatingconditions)
        objBri['CET_THE_MAWP'] = bool(rwcomponent.cetgreaterorequal)
        objBri['CYCLIC_SERVICE'] = bool(rwcomponent.cyclicservice)
        objBri['PresenceCyanides'] = bool(rwstream.cyanide)
        objBri['EQUIPMENT_CIRCUIT_SHOCK'] = bool(rwcomponent.equipmentcircuitshock)
        objBri['NomalThick'] = rwcomponent.nominalthickness
        if objBri['NomalThick'] <= 12.7:
            objBri['equal_127'] = True
        else:
            objBri['equal_127'] = False
        if objBri['NomalThick'] <= 50.8:
            objBri['equal_508'] = True
        else:
            objBri['equal_508'] = False
        objBri['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objBri['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        objBri['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        # BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
        #                                    objBri['CRITICAL_TEMP'],
        #                                    objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
        #                                    objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
        #                                    objBri['NOMINAL_OPERATING_CONDITIONS'],
        #                                    objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
        #                                    objBri['EQUIPMENT_CIRCUIT_SHOCK'], objBri['NomalThick'],
        #                                    objBri['CARBON_ALLOY'],
        #                                    objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
        #                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
        #                                    ComponentNumber)
        for i in range(20,0,-2):
            if (obj['NominalThickness']-i)>0:
                dataNominalThicknessX.append(str(obj['NominalThickness']-i));
                xx=obj['NominalThickness']-i;
                print(obj['CladdingThickness'])
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], xx, obj['CurentThickness'],
                                             obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingThickness'],
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber,
                                             APIComponentType)
                EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                         objExCor['EXTERN_COAT_QUALITY'],
                                                                         objExCor['EXTERNAL_EVIRONMENT'],
                                                                         objExCor['CUI_PERCENT_2'],
                                                                         objExCor['CUI_PERCENT_3'],
                                                                         objExCor['CUI_PERCENT_4'],
                                                                         objExCor['CUI_PERCENT_5'],
                                                                         objExCor['CUI_PERCENT_6'],
                                                                         objExCor['SUPPORT_COATING'],
                                                                         objExCor['INTERFACE_SOIL_WATER'],
                                                                         objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                         objExCor['CARBON_ALLOY'],
                                                                         objExCor['MAX_OP_TEMP'],
                                                                         objExCor['MIN_OP_TEMP'],
                                                                         objExCor['EXTERNAL_INSP_EFF'],
                                                                         objExCor['EXTERNAL_INSP_NUM'],
                                                                         objExCor['NoINSP_EXTERNAL'],
                                                                         objExCor['APIComponentType'],
                                                                         xx,
                                                                         objExCor['CurrentThick'],
                                                                         objExCor['WeldJointEffciency'],
                                                                         objExCor['YieldStrengthDesignTemp'],
                                                                         objExCor['TensileStrengthDesignTemp'],
                                                                         objExCor['ShapeFactor'],
                                                                         objExCor[
                                                                             'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                         objExCor['CR_Confidents_Level'],
                                                                         objExCor['AllowableStress'],
                                                                         objExCor['MinThickReq'],
                                                                         objExCor['StructuralThickness'],
                                                                         objExCor['Pressure'],
                                                                         objExCor['Diametter'],
                                                                         rwassessment.assessmentdate,
                                                                         COMPONENT_INSTALL_DATE,
                                                                         ComponentNumber)
                CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                            objCui['CUI_PERCENT_3'],
                                            objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                            objCui['CUI_PERCENT_6'],
                                            objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                            objCui['CUI_PERCENT_9'],
                                            objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                            objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                            objCui['INTERFACE_SOIL_WATER'],
                                            objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                            , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                            objCui['MIN_OP_TEMP'],
                                            objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                            objCui['APIComponentType']
                                            , xx, objCui['CurrentThick'],
                                            objCui['CR_Confidents_Level'],
                                            objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                            objCui['WeldJointEffciency'],
                                            objCui['YieldStrengthDesignTemp'],
                                            objCui['TensileStrengthDesignTemp'],
                                            objCui['AllowableStress'], objCui['MinThickReq'],
                                            objCui['StructuralThickness'],
                                            objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                            objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                            rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                            ComponentNumber)
                BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
                                                   objBri['CRITICAL_TEMP'],
                                                   objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
                                                   objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
                                                   objBri['NOMINAL_OPERATING_CONDITIONS'],
                                                   objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
                                                   objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
                                                   objBri['CARBON_ALLOY'],
                                                   objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)
                thin0=thin.DF_THINNING_API(0)
                dataPoFTemp=dataPoF

                dataPoFTemp['thin']=thin0
                dataPoFTemp['external_corrosion']=EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
                dataPoFTemp['cui']=CUIF.DF_CUI_API(0)
                dataPoFTemp['brittle']=BRITTLE.DF_BRITTLE_API(0)
                dataNominalThicknessY0.append(thin0)
                # dataNominalThicknessY1.append(thin.DF_THINNING_API(36))
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataNominalThicknessY1.append(temp['PoF'])
                dataNominalThicknessY2.append(temp['damageTotal'] * dataCoF)
                # print(ReCalculate.calculatePoF(proposalID,dataPoF))

        for i in range(0, 20, 2):
            dataNominalThicknessX.append(str(obj['NominalThickness'] + i));
            xx = obj['NominalThickness'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], xx, obj['CurentThickness'],
                                         obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                         obj['CladdingThickness'],
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber,APIComponentType)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     objExCor['MAX_OP_TEMP'],
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     xx,
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , xx, objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
                                               objBri['CRITICAL_TEMP'],
                                               objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
                                               objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
                                               objBri['NOMINAL_OPERATING_CONDITIONS'],
                                               objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
                                               objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
                                               objBri['CARBON_ALLOY'],
                                               objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataNominalThicknessY0.append(thin0)
            # dataNominalThicknessY1.append(thin.DF_THINNING_API(36))
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataNominalThicknessY1.append(temp['PoF'])
            dataNominalThicknessY2.append(temp['damageTotal'] * dataCoF)

        #Minimun Measured Thickness


        for i in range(20,0,-2):
            if (obj['CurentThickness'] - i) > 0:
                dataCurentThicknessX.append(str(obj['CurentThickness'] - i));
                xx = obj['CurentThickness'] - i;
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], xx,
                                             obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                             obj['CladdingThickness'],
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber,
                                             APIComponentType)
                EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                         objExCor['EXTERN_COAT_QUALITY'],
                                                                         objExCor['EXTERNAL_EVIRONMENT'],
                                                                         objExCor['CUI_PERCENT_2'],
                                                                         objExCor['CUI_PERCENT_3'],
                                                                         objExCor['CUI_PERCENT_4'],
                                                                         objExCor['CUI_PERCENT_5'],
                                                                         objExCor['CUI_PERCENT_6'],
                                                                         objExCor['SUPPORT_COATING'],
                                                                         objExCor['INTERFACE_SOIL_WATER'],
                                                                         objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                         objExCor['CARBON_ALLOY'],
                                                                         objExCor['MAX_OP_TEMP'],
                                                                         objExCor['MIN_OP_TEMP'],
                                                                         objExCor['EXTERNAL_INSP_EFF'],
                                                                         objExCor['EXTERNAL_INSP_NUM'],
                                                                         objExCor['NoINSP_EXTERNAL'],
                                                                         objExCor['APIComponentType'],
                                                                         objExCor['NomalThick'],
                                                                         xx,
                                                                         objExCor['WeldJointEffciency'],
                                                                         objExCor['YieldStrengthDesignTemp'],
                                                                         objExCor['TensileStrengthDesignTemp'],
                                                                         objExCor['ShapeFactor'],
                                                                         objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                         objExCor['CR_Confidents_Level'],
                                                                         objExCor['AllowableStress'],
                                                                         objExCor['MinThickReq'],
                                                                         objExCor['StructuralThickness'],
                                                                         objExCor['Pressure'],
                                                                         objExCor['Diametter'],
                                                                         rwassessment.assessmentdate,
                                                                         COMPONENT_INSTALL_DATE,
                                                                         ComponentNumber)
                CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                            objCui['CUI_PERCENT_3'],
                                            objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                            objCui['CUI_PERCENT_6'],
                                            objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                            objCui['CUI_PERCENT_9'],
                                            objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                            objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                            objCui['INTERFACE_SOIL_WATER'],
                                            objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                            , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                            objCui['MIN_OP_TEMP'],
                                            objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                            objCui['APIComponentType']
                                            , objCui['NomalThick'], xx,
                                            objCui['CR_Confidents_Level'],
                                            objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                            objCui['WeldJointEffciency'],
                                            objCui['YieldStrengthDesignTemp'],
                                            objCui['TensileStrengthDesignTemp'],
                                            objCui['AllowableStress'], objCui['MinThickReq'],
                                            objCui['StructuralThickness'],
                                            objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                            objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                            rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                            ComponentNumber)
                # dataCurentThicknessY0.append(thin.DF_THINNING_API(0))
                # dataCurentThicknessY1.append(thin.DF_THINNING_API(36))
                # dataCurentThicknessY2.append(thin.DF_THINNING_API(72))
                thin0 = thin.DF_THINNING_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['thin'] = thin0
                dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
                dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

                dataCurentThicknessY0.append(thin0)
                # dataNominalThicknessY1.append(thin.DF_THINNING_API(36))
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataCurentThicknessY1.append(temp['PoF'])
                dataCurentThicknessY2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            dataCurentThicknessX.append(str(obj['CurentThickness'] + i));
            xx = obj['CurentThickness'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], xx,
                                         obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                         obj['CladdingThickness'],
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber,
                                         APIComponentType)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     objExCor['MAX_OP_TEMP'],
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     xx,
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], xx,
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

            dataCurentThicknessY0.append(thin0)

            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataCurentThicknessY1.append(temp['PoF'])
            dataCurentThicknessY2.append(temp['damageTotal'] * dataCoF)
            # dataCurentThicknessY0.append(thin.DF_THINNING_API(0))
            # dataCurentThicknessY1.append(thin.DF_THINNING_API(36))
            # dataCurentThicknessY2.append(thin.DF_THINNING_API(72))
        #Current Corrosion Rate
        for i in range(20,0,-2):
            if (obj['CorrosionRate'] - i) > 0:
                dataCorrosionRateX.append(str(obj['CorrosionRate'] - i));
                xx = obj['CorrosionRate'] - i;
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                             obj['MinimunRequiredThickness'], xx,
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingThickness'],
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber,
                                             APIComponentType)
                thin0 = thin.DF_THINNING_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['thin'] = thin0
                dataCorrosionRateY0.append(thin0)

                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataCorrosionRateY1.append(temp['PoF'])
                dataCorrosionRateY2.append(temp['damageTotal'] * dataCoF)
                # dataCorrosionRateY0.append(thin.DF_THINNING_API(0))
                # dataCorrosionRateY1.append(thin.DF_THINNING_API(36))
                # dataCorrosionRateY2.append(thin.DF_THINNING_API(72))
        for i in range(0, 20, 2):
            dataCorrosionRateX.append(str(obj['CorrosionRate'] + i));
            xx = obj['CorrosionRate'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                         obj['MinimunRequiredThickness'], xx,
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingThickness'],
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber,
                                         APIComponentType)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataCorrosionRateY0.append(thin0)

            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataCorrosionRateY1.append(temp['PoF'])
            dataCorrosionRateY2.append(temp['damageTotal'] * dataCoF)


        # Minimum Required Thickness
        for i in range(20,0,-2):
            if (obj['MinimunRequiredThickness'] - i) > 0:
                dataMinimunRequiredThicknessX.append(str(obj['MinimunRequiredThickness'] - i));
                xx = obj['MinimunRequiredThickness'] - i;
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                             xx, obj['CorrosionRate'],
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingThickness'],
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber,
                                             APIComponentType)
                EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                         objExCor['EXTERN_COAT_QUALITY'],
                                                                         objExCor['EXTERNAL_EVIRONMENT'],
                                                                         objExCor['CUI_PERCENT_2'],
                                                                         objExCor['CUI_PERCENT_3'],
                                                                         objExCor['CUI_PERCENT_4'],
                                                                         objExCor['CUI_PERCENT_5'],
                                                                         objExCor['CUI_PERCENT_6'],
                                                                         objExCor['SUPPORT_COATING'],
                                                                         objExCor['INTERFACE_SOIL_WATER'],
                                                                         objExCor[
                                                                             'EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                         objExCor['CARBON_ALLOY'],
                                                                         objExCor['MAX_OP_TEMP'],
                                                                         objExCor['MIN_OP_TEMP'],
                                                                         objExCor['EXTERNAL_INSP_EFF'],
                                                                         objExCor['EXTERNAL_INSP_NUM'],
                                                                         objExCor['NoINSP_EXTERNAL'],
                                                                         objExCor['APIComponentType'],
                                                                         objExCor['NomalThick'],
                                                                         objExCor['CurrentThick'],
                                                                         objExCor['WeldJointEffciency'],
                                                                         objExCor['YieldStrengthDesignTemp'],
                                                                         objExCor['TensileStrengthDesignTemp'],
                                                                         objExCor['ShapeFactor'],
                                                                         objExCor[
                                                                             'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                         objExCor['CR_Confidents_Level'],
                                                                         objExCor['AllowableStress'],
                                                                         xx,
                                                                         objExCor['StructuralThickness'],
                                                                         objExCor['Pressure'],
                                                                         objExCor['Diametter'],
                                                                         rwassessment.assessmentdate,
                                                                         COMPONENT_INSTALL_DATE,
                                                                         ComponentNumber)
                CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                            objCui['CUI_PERCENT_3'],
                                            objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                            objCui['CUI_PERCENT_6'],
                                            objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                            objCui['CUI_PERCENT_9'],
                                            objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                            objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                            objCui['INTERFACE_SOIL_WATER'],
                                            objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                            , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                            objCui['MIN_OP_TEMP'],
                                            objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                            objCui['APIComponentType']
                                            , objCui['NomalThick'], objExCor['CurrentThick'],
                                            objCui['CR_Confidents_Level'],
                                            objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                            objCui['WeldJointEffciency'],
                                            objCui['YieldStrengthDesignTemp'],
                                            objCui['TensileStrengthDesignTemp'],
                                            objCui['AllowableStress'], xx,
                                            objCui['StructuralThickness'],
                                            objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                            objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                            rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                            ComponentNumber)
                thin0 = thin.DF_THINNING_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['thin'] = thin0
                dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
                dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

                dataMinimunRequiredThicknessY0.append(thin0)

                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataMinimunRequiredThicknessY1.append(temp['PoF'])
                dataMinimunRequiredThicknessY2.append(temp['damageTotal'] * dataCoF)
                # dataMinimunRequiredThicknessY0.append(thin.DF_THINNING_API(0))
                # dataMinimunRequiredThicknessY1.append(thin.DF_THINNING_API(36))
                # dataMinimunRequiredThicknessY2.append(thin.DF_THINNING_API(72))
        for i in range(0, 20, 2):
            dataMinimunRequiredThicknessX.append(str(obj['MinimunRequiredThickness'] + i));
            xx = obj['MinimunRequiredThickness'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                         xx, obj['CorrosionRate'],
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingThickness'],
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber,
                                         APIComponentType)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor[
                                                                         'EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     objExCor['MAX_OP_TEMP'],
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     xx,
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objExCor['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], xx,
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

            dataMinimunRequiredThicknessY0.append(thin0)

            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMinimunRequiredThicknessY1.append(temp['PoF'])
            dataMinimunRequiredThicknessY2.append(temp['damageTotal'] * dataCoF)
            # dataMinimunRequiredThicknessY0.append(thin.DF_THINNING_API(0))
            # dataMinimunRequiredThicknessY1.append(thin.DF_THINNING_API(36))
            # dataMinimunRequiredThicknessY2.append(thin.DF_THINNING_API(72))
        res_obj={}
        res_obj['dataNominalThicknessX']=dataNominalThicknessX
        res_obj['dataNominalThicknessY0']=dataNominalThicknessY0
        res_obj['dataNominalThicknessY1']=dataNominalThicknessY1
        res_obj['dataNominalThicknessY2']=dataNominalThicknessY2
        res_obj['dataCurentThicknessX']= dataCurentThicknessX
        res_obj['dataCurentThicknessY0']= dataCurentThicknessY0
        res_obj['dataCurentThicknessY1']= dataCurentThicknessY1
        res_obj['dataCurentThicknessY2']= dataCurentThicknessY2
        res_obj['dataCorrosionRateX']= dataCorrosionRateX
        res_obj['dataCorrosionRateY0']= dataCorrosionRateY0
        res_obj['dataCorrosionRateY1']= dataCorrosionRateY1
        res_obj['dataCorrosionRateY2']= dataCorrosionRateY2
        res_obj['dataMinimunRequiredThicknessX']= dataMinimunRequiredThicknessX
        res_obj['dataMinimunRequiredThicknessY0']= dataMinimunRequiredThicknessY0
        res_obj['dataMinimunRequiredThicknessY1']= dataMinimunRequiredThicknessY1
        res_obj['dataMinimunRequiredThicknessY2']= dataMinimunRequiredThicknessY2
        return res_obj
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def showAlkaline(proposalID):
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

        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        CRACK_PRESENT = bool(rwcomponent.crackspresent)
        obj['CRACK_PRESENT'] = CRACK_PRESENT

        PWHT = bool(rwequipment.pwht)
        # PWHT=bool(1)
        CO3_CONTENT=rwstream.co3concentration
        PH = rwstream.waterph
        CARBON_ALLOY = bool(rwmaterial.carbonlowalloy)
        obj['CARBON_ALLOY']=bool(rwmaterial.carbonlowalloy)
        obj['PWHT'] = PWHT
        obj['co3'] = CO3_CONTENT
        obj['ph']=PH
        AQUEOUS_OPERATOR = bool(rwstream.aqueousoperation)
        obj['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        Alkaline=Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'],obj['PWHT'],obj['co3'],obj['ph'],obj['CARBON_ALLOY'],obj['AQUEOUS_OPERATOR'],'E',0, rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber)
        obj['ALKALINE_INSP_EFF'] = Alkaline.CACBONATE_INSP_EFF
        obj['ALKALINE_INSP_NUM'] = Alkaline.CACBONATE_INSP_NUM


        obj['Susceptibility']=Alkaline.GET_SUSCEPTIBILITY_CARBONATE()

        obj['SVI']=Alkaline.SVI_CARBONATE()
        obj['age1']=Alkaline.GET_AGE()
        obj['age2']=Alkaline.GET_AGE()+3
        obj['age3']=Alkaline.GET_AGE()+6
        obj['base1']=Alkaline.DFB_CACBONATE_API(0)
        obj['base2']=Alkaline.DFB_CACBONATE_API(3)
        obj['base3']=Alkaline.DFB_CACBONATE_API(6)
        obj['CACBONATE1'] = Alkaline.DF_CACBONATE_API(0)
        obj['CACBONATE2'] = Alkaline.DF_CACBONATE_API(3)
        obj['CACBONATE3'] = Alkaline.DF_CACBONATE_API(6)
        obj2={}
        obj2['PWHT']=True
        obj2['CRACK_PRESENT']=False
        obj2['ph'] =4
        obj2['CARBON_ALLOY']=True
        obj2['AQUEOUS_OPERATOR']=True
        Alkaline2=Detail_DM_CAL.Df_Cacbonate(False,bool(1),CO3_CONTENT,obj2['ph'],CARBON_ALLOY,AQUEOUS_OPERATOR,'E',0, rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber)
        obj2['ALKALINE_INSP_EFF'] = Alkaline2.CACBONATE_INSP_EFF
        obj2['ALKALINE_INSP_NUM'] = Alkaline2.CACBONATE_INSP_NUM
        obj2['co3'] = Alkaline2.CO3_CONTENT
        obj2['ph'] = Alkaline2.PH
        obj2['Susceptibility'] = Alkaline2.GET_SUSCEPTIBILITY_CARBONATE()
        obj2['PWHT'] = PWHT
        obj2['SVI'] = Alkaline2.SVI_CARBONATE()
        obj2['age1'] = Alkaline2.GET_AGE()
        obj2['age2'] = Alkaline2.GET_AGE() + 3
        obj2['age3'] = Alkaline2.GET_AGE() + 6
        obj2['base1'] = Alkaline2.DFB_CACBONATE_API(0)
        obj2['base2'] = Alkaline2.DFB_CACBONATE_API(3)
        obj2['base3'] = Alkaline2.DFB_CACBONATE_API(6)
        obj2['CACBONATE1'] = Alkaline2.DF_CACBONATE_API(0)
        obj2['CACBONATE2'] = Alkaline2.DF_CACBONATE_API(3)
        obj2['CACBONATE3'] = Alkaline2.DF_CACBONATE_API(6)
        dataCO3X = []
        dataCO3Y0 = []
        dataCO3Y1 = []
        dataCO3Y2 = []
        dataphX = []
        dataphY0 = []
        dataphY1 = []
        dataphY2 = []
        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        objsulphide = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objsulphide['ComponentNumber'] = ComponentNumber
        objsulphide['EquipmentNumber'] = EquipmentName
        objsulphide['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objsulphide['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objsulphide['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objsulphide['PH'] = rwstream.waterph
        objsulphide['H2SContent'] = rwstream.h2sinwater
        objsulphide['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objsulphide['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objsulphide['PWHT'] = bool(rwequipment.pwht)
        objsulphide['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        objsulphide['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objsulphide['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objsulphide['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)
        #
        objHicsohic_H2s = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHicsohic_H2s['ComponentNumber'] = ComponentNumber
        objHicsohic_H2s['EquipmentNumber'] = EquipmentName
        objHicsohic_H2s['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHicsohic_H2s['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHicsohic_H2s['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHicsohic_H2s['PH'] = rwstream.waterph
        objHicsohic_H2s['H2SContent'] = rwstream.h2sinwater
        objHicsohic_H2s['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objHicsohic_H2s['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHicsohic_H2s['PWHT'] = bool(rwequipment.pwht)

        objHicsohic_H2s['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        objHicsohic_H2s['OnlineMonitoring'] = rwequipment.onlinemonitoring
        objHicsohic_H2s['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHicsohic_H2s['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)


        #
        #
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP']=rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)




        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        #     thay doi obj['CO3']
        for i in range(20, 0, -2):
            xx = obj['co3'] - i
            if xx>=0:
                dataCO3X.append(str(xx))

                Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], xx, obj['ph'],
                                                      obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                      rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                      ComponentNumber)
                Alkaline0 = Alkaline.DF_CACBONATE_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['cacbonat'] = Alkaline0
                dataCO3Y0.append(Alkaline0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataCO3Y1.append(temp['PoF'])
                dataCO3Y2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            xx = obj['co3'] + i;
            dataCO3X.append(str(xx));

            Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], xx, obj['ph'],
                                                  obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                  rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                  ComponentNumber)
            Alkaline0 = Alkaline.DF_CACBONATE_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['cacbonat'] = Alkaline0
            dataCO3Y0.append(Alkaline0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataCO3Y1.append(temp['PoF'])
            dataCO3Y2.append(temp['damageTotal'] * dataCoF)
            #     thay doi obj['ph']
        for i in range(20, 0, -2):
            xx = obj['ph'] - i
            if xx >= 0:
                dataphX.append(str(xx))

                Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], obj['co3'],xx ,
                                                      obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                      rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                      ComponentNumber)
                sulphide = Detail_DM_CAL.Df_Sulphide(xx, objsulphide['H2SContent'],
                                                     objsulphide['PRESENT_CYANIDE'],
                                                     objsulphide['CRACK_PRESENT'], objsulphide['PWHT'],
                                                     objsulphide['BRINNEL_HARDNESS'],
                                                     objsulphide['CARBON_ALLOY'],
                                                     objsulphide['AQUEOUS_OPERATOR'],
                                                     objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                                     rwassessment.assessmentdate,
                                                     COMPONENT_INSTALL_DATE, ComponentNumber)
                Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(xx,
                                                             objHicsohic_H2s['H2SContent'],
                                                             objHicsohic_H2s['PRESENT_CYANIDE'],
                                                             objHicsohic_H2s['CRACK_PRESENT'],
                                                             objHicsohic_H2s['PWHT'],
                                                             objHicsohic_H2s['SULFUR_CONTENT'],
                                                             objHicsohic_H2s['OnlineMonitoring'],
                                                             objHicsohic_H2s['CARBON_ALLOY'],
                                                             objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                             objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                             0, rwassessment.assessmentdate,
                                                             COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
                CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'],
                                               objCLSCC['MAX_OP_TEMP'], objCLSCC['MIN_OP_TEMP'],
                                               objCLSCC['CHLORIDE_ION_CONTENT'],
                                               objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                               objCLSCC['AUSTENITIC_STEEL']
                                               , 'E', 0,
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
                Alkaline0 = Alkaline.DF_CACBONATE_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['cacbonat'] = Alkaline0
                dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
                dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
                dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
                dataphY0.append(Alkaline0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataphY1.append(temp['PoF'])
                dataphY2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            xx = obj['ph'] + i;
            dataphX.append(str(xx));

            Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], obj['co3'], xx,
                                                  obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                  rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                  ComponentNumber)
            sulphide = Detail_DM_CAL.Df_Sulphide(xx, objsulphide['H2SContent'],
                                                 objsulphide['PRESENT_CYANIDE'],
                                                 objsulphide['CRACK_PRESENT'], objsulphide['PWHT'],
                                                 objsulphide['BRINNEL_HARDNESS'],
                                                 objsulphide['CARBON_ALLOY'],
                                                 objsulphide['AQUEOUS_OPERATOR'],
                                                 objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                                 rwassessment.assessmentdate,
                                                 COMPONENT_INSTALL_DATE, ComponentNumber)
            Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(xx,
                                                         objHicsohic_H2s['H2SContent'],
                                                         objHicsohic_H2s['PRESENT_CYANIDE'],
                                                         objHicsohic_H2s['CRACK_PRESENT'],
                                                         objHicsohic_H2s['PWHT'],
                                                         objHicsohic_H2s['SULFUR_CONTENT'],
                                                         objHicsohic_H2s['OnlineMonitoring'],
                                                         objHicsohic_H2s['CARBON_ALLOY'],
                                                         objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                         objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                         0, rwassessment.assessmentdate,
                                                         COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'],
                                           objCLSCC['MAX_OP_TEMP'], objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)
            Alkaline0 = Alkaline.DF_CACBONATE_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['cacbonat'] = Alkaline0
            dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
            dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataphY0.append(Alkaline0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataphY1.append(temp['PoF'])
            dataphY2.append(temp['damageTotal'] * dataCoF)
        obj_res={}
        obj_res['dataCO3X']=dataCO3X
        obj_res['dataCO3Y0']=dataCO3Y0
        obj_res['dataCO3Y1']=dataCO3Y1
        obj_res['dataCO3Y2']=dataCO3Y2
        obj_res['dataphX']=dataphX
        obj_res['dataphY0']=dataphY0
        obj_res['dataphY1']=dataphY1
        obj_res['dataphY2']=dataphY2

        return obj_res
    except Exception as e:
        print(e)
def showCaustic(proposalID):

    try:
        obj={}
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
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT']=bool(rwcomponent.crackspresent)
        obj['HEAT_TREATMENT']=rwmaterial.heattreatment
        obj['NaOHConcentration']=rwstream.naohconcentration
        obj['HEAT_TRACE']=bool(rwequipment.heattraced)
        obj['STEAM_OUT']=bool(rwequipment.steamoutwaterflush)
        obj['MAX_OP_TEMP']=rwstream.maxoperatingtemperature
        obj['CARBON_ALLOY']=bool(rwmaterial.carbonlowalloy)
        obj['PWHT']=bool(rwequipment.pwht)

        caustic=Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'],obj['HEAT_TREATMENT'],obj['NaOHConcentration'],obj['HEAT_TRACE'], obj['STEAM_OUT'],obj['MAX_OP_TEMP'],obj['CARBON_ALLOY'],'E', 0,0,obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber)
        obj['CAUSTIC_INSP_EFF'] = caustic.CAUSTIC_INSP_EFF
        obj['CACBONATE_INSP_NUM'] = caustic.CACBONATE_INSP_NUM
        obj['CAUSTIC_INSP_NUM'] = caustic.CAUSTIC_INSP_NUM
        obj['plotinArea']=caustic.plotinArea
        obj['Susceptibility']=caustic.getSusceptibility_Caustic
        obj['SVI']=caustic.SVI_CAUSTIC
        obj['age1']=caustic.GET_AGE()
        obj['age2']=caustic.GET_AGE()+3
        obj['age3']=caustic.GET_AGE()+6
        obj['base1']=caustic.DFB_CAUSTIC_API(0)
        obj['base2']=caustic.DFB_CAUSTIC_API(3)
        obj['base3']=caustic.DFB_CAUSTIC_API(6)
        obj['caustic1']=caustic.DF_CAUSTIC_API(0)
        obj['caustic2']=caustic.DF_CAUSTIC_API(3)
        obj['caustic3']=caustic.DF_CAUSTIC_API(6)
        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        dataMAX_OP_TEMPX = []
        dataMAX_OP_TEMPY0 = []
        dataMAX_OP_TEMPY1 = []
        dataMAX_OP_TEMPY2 = []
        #
        objHIC_SOHIC_HF = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHIC_SOHIC_HF['ComponentNumber'] = ComponentNumber
        objHIC_SOHIC_HF['EquipmentNumber'] = EquipmentName
        objHIC_SOHIC_HF['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHIC_SOHIC_HF['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHIC_SOHIC_HF['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHIC_SOHIC_HF['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHIC_SOHIC_HF['HF_PRESENT'] = bool(rwstream.hydrofluoric)
        objHIC_SOHIC_HF['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHIC_SOHIC_HF['PWHT'] = bool(rwequipment.pwht)
        objHIC_SOHIC_HF['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        objHIC_SOHIC_HF['OnlineMonitoring'] = rwequipment.onlinemonitoring
        #
        objHSCHF = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHSCHF['ComponentNumber'] = ComponentNumber
        objHSCHF['EquipmentNumber'] = EquipmentName
        objHSCHF['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHSCHF['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHSCHF['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHSCHF['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHSCHF['HF_PRESENT'] = bool(rwstream.hydrofluoric)
        objHSCHF['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHSCHF['PWHT'] = bool(rwequipment.pwht)
        objHSCHF['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        #
        objAlkaline = {}
        objAlkaline['ComponentNumber'] = ComponentNumber
        objAlkaline['EquipmentNumber'] = EquipmentName
        objAlkaline['Assessment'] = rwassessment.proposalname
        objAlkaline['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objAlkaline['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
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
        objAlkaline['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objAlkaline['PWHT'] = PWHT
        objAlkaline['co3'] = CO3_CONTENT
        objAlkaline['ph'] = PH
        objAlkaline['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        #
        objsulphide = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objsulphide['ComponentNumber'] = ComponentNumber
        objsulphide['EquipmentNumber'] = EquipmentName
        objsulphide['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objsulphide['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objsulphide['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objsulphide['PH'] = rwstream.waterph
        objsulphide['H2SContent'] = rwstream.h2sinwater
        objsulphide['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objsulphide['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objsulphide['PWHT'] = bool(rwequipment.pwht)
        objsulphide['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        objsulphide['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objsulphide['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objsulphide['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)
        #
        objHicsohic_H2s = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHicsohic_H2s['ComponentNumber'] = ComponentNumber
        objHicsohic_H2s['EquipmentNumber'] = EquipmentName
        objHicsohic_H2s['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHicsohic_H2s['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHicsohic_H2s['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHicsohic_H2s['PH'] = rwstream.waterph
        objHicsohic_H2s['H2SContent'] = rwstream.h2sinwater
        objHicsohic_H2s['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objHicsohic_H2s['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHicsohic_H2s['PWHT'] = bool(rwequipment.pwht)

        objHicsohic_H2s['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        objHicsohic_H2s['OnlineMonitoring'] = rwequipment.onlinemonitoring
        objHicsohic_H2s['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHicsohic_H2s['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)

        # PASCC-PTA
        objPASCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objPASCC['ComponentNumber'] = ComponentNumber
        objPASCC['EquipmentNumber'] = EquipmentName
        objPASCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objPASCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objPASCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objPASCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objPASCC['ExposedSH2OOperation'] = bool(rwequipment.presencesulphideso2)
        objPASCC['ExposedSH2OShutdown'] = bool(rwequipment.presencesulphideso2shutdown)
        objPASCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objPASCC['ThermalHistory'] = rwequipment.thermalhistory
        objPASCC['PTAMaterial'] = rwmaterial.ptamaterialcode
        objPASCC['DOWNTIME_PROTECTED'] = bool(rwequipment.downtimeprotectionused)
        objPASCC['PTA_SUSCEP'] = bool(rwmaterial.ispta)
        objPASCC['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objPASCC['NICKEL_ALLOY'] = bool(rwmaterial.nickelbased)
        objPASCC['EXPOSED_SULFUR'] = bool(rwstream.exposedtosulphur)
        # Df_CLSCC
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        # Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = API_COMPONENT_TYPE_NAME = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # Df_CUI
        objCui = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # EXTERNAL CLSCC
        objEXTERN_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objEXTERN_CLSCC['ComponentNumber'] = ComponentNumber
        objEXTERN_CLSCC['EquipmentNumber'] = EquipmentName
        objEXTERN_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objEXTERN_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objEXTERN_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objEXTERN_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objEXTERN_CLSCC['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # CUI_CLSCC
        objCUI_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCUI_CLSCC['ComponentNumber'] = ComponentNumber
        objCUI_CLSCC['EquipmentNumber'] = EquipmentName
        objCUI_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        objCUI_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCUI_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCUI_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCUI_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCUI_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCUI_CLSCC['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCUI_CLSCC['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCUI_CLSCC['INSULATION_CHLORIDE'] = bool(rwcoat.insulationcontainschloride)
        objCUI_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objCUI_CLSCC['EXTERNAL_INSULATION'] = bool(rwcoat.externalinsulation)

        objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCUI_CLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCUI_CLSCC['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        # HTHA
        objHTHA = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHTHA['ComponentNumber'] = ComponentNumber
        objHTHA['EquipmentNumber'] = EquipmentName
        objHTHA['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHTHA['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHTHA['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHTHA['HTHA_PRESSURE'] = rwstream.h2spartialpressure * 0.006895
        objHTHA['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objHTHA['HTHADamageObserved'] = rwcomponent.hthadamage
        objHTHA['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objHTHA['MATERIAL_SUSCEP_HTHA'] = bool(rwmaterial.ishtha)
        objHTHA['HTHA_MATERIAL'] = rwmaterial.hthamaterialcode
        objHTHA['Hydrogen'] = rwstream.hydrogen
        # TEMP_EMBRITTLE
        objTEMP_EMBRITTLE = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objTEMP_EMBRITTLE['ComponentNumber'] = ComponentNumber
        objTEMP_EMBRITTLE['EquipmentNumber'] = EquipmentName
        objTEMP_EMBRITTLE['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objTEMP_EMBRITTLE['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['TEMPER_SUSCEP'] = bool(rwmaterial.temper)
        objTEMP_EMBRITTLE['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objTEMP_EMBRITTLE['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objTEMP_EMBRITTLE['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objTEMP_EMBRITTLE['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objTEMP_EMBRITTLE['REF_TEMP'] = rwmaterial.referencetemperature
        objTEMP_EMBRITTLE['DELTA_FATT'] = rwcomponent.deltafatt
        objTEMP_EMBRITTLE['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objTEMP_EMBRITTLE['PWHT'] = bool(rwequipment.pwht)
        objTEMP_EMBRITTLE['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness

        objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Df_885
        obj885 = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj885['ComponentNumber'] = ComponentNumber
        obj885['EquipmentNumber'] = EquipmentName
        obj885['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        obj885['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj885['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj885['CHROMIUM_12'] = bool(rwmaterial.chromemoreequal12)
        obj885['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj885['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj885['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj885['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj885['REF_TEMP'] = rwmaterial.referencetemperature
        obj885['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj885['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # dfSigma
        objSigma = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objSigma['ComponentNumber'] = ComponentNumber
        objSigma['EquipmentNumber'] = EquipmentName
        objSigma['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objSigma['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objSigma['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objSigma['MIN_TEM'] = rwstream.minoperatingtemperature
        objSigma['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objSigma['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objSigma['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        objSigma['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objSigma['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation

        objSigma['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objSigma['PERCENT_SIGMA'] = rwmaterial.sigmaphase
        # chua thay su dung MIN_DESIGN_TEMP
        objSigma['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Amine
        objAmine = {}
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
        objAmine['ComponentNumber'] = ComponentNumber
        objAmine['EquipmentName'] = EquipmentName
        objAmine['Assessment'] = rwassessment.proposalname

        objAmine['AMINE_EXPOSED'] = bool(rwstream.exposedtogasamine)
        objAmine['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objAmine['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objAmine['AMINE_SOLUTION'] = rwstream.aminesolution

        objAmine['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objAmine['HEAT_TRACE'] = bool(rwequipment.heattraced)
        objAmine['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)

        objAmine['AMINE_INSP_EFF'] = 'E'
        objAmine['AMINE_INSP_NUM'] = 0
        objAmine['PWHT'] = bool(rwequipment.pwht)
        objAmine['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objAmine['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objAmine['ComponentNumber'] = str(comp.componentnumber)
        # MAX_OP_TEMP
        for i in range(20, 0, -2):
            xx = obj['MAX_OP_TEMP'] - i;
            dataMAX_OP_TEMPX.append(str(xx));

            anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'], objAmine['CRACK_PRESENT'],
                                           objAmine['AMINE_SOLUTION'], xx, objAmine['HEAT_TRACE'],
                                           objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'], objAmine['AMINE_INSP_NUM'],
                                           objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           objAmine['ComponentNumber'])

            PASCC = Detail_DM_CAL.Df_PTA(objPASCC['CRACK_PRESENT'], objPASCC['ExposedSH2OOperation'],
                                         objPASCC['ExposedSH2OShutdown'],
                                         xx, objPASCC['ThermalHistory'],
                                         objPASCC['PTAMaterial'],
                                         objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                         objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                         objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)

            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)

            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)

            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)

            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'],
                                             objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)

            caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                               obj['NaOHConcentration'],
                                               obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                               xx,
                                               obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            caustic0 = caustic.DF_CAUSTIC_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic0
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(caustic0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)
        #     MAX_OP_TEMP
        for i in range(0, 20, 2):
            xx = obj['MAX_OP_TEMP'] + i;
            dataMAX_OP_TEMPX.append(str(xx));

            anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                           objAmine['CRACK_PRESENT'],
                                           objAmine['AMINE_SOLUTION'], xx, objAmine['HEAT_TRACE'],
                                           objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                           objAmine['AMINE_INSP_NUM'],
                                           objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           objAmine['ComponentNumber'])

            PASCC = Detail_DM_CAL.Df_PTA(objPASCC['CRACK_PRESENT'], objPASCC['ExposedSH2OOperation'],
                                         objPASCC['ExposedSH2OShutdown'],
                                         xx, objPASCC['ThermalHistory'],
                                         objPASCC['PTAMaterial'],
                                         objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                         objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                         objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)

            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)

            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)

            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)

            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'],
                                             objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)

            caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                               obj['NaOHConcentration'],
                                               obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                               xx,
                                               obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            caustic0 = caustic.DF_CAUSTIC_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic0
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(caustic0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)
        #     NaOHConcentration
        dataNaOHConcentrationX = []
        dataNaOHConcentrationY0 = []
        dataNaOHConcentrationY1 = []
        dataNaOHConcentrationY2 = []
        for i in range(20, 0, -2):
            xx = obj['NaOHConcentration'] - i;
            if xx>=0:
                dataNaOHConcentrationX.append(str(xx));
                caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                               xx,
                                               obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                                obj['MAX_OP_TEMP'],
                                               obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
                caustic0 = caustic.DF_CAUSTIC_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['caustic'] = caustic0
                dataNaOHConcentrationY0.append(caustic0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataNaOHConcentrationY1.append(temp['PoF'])
                dataNaOHConcentrationY2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            xx = obj['NaOHConcentration'] + i;
            if xx<=100:
                dataNaOHConcentrationX.append(str(xx));
                caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                               xx,
                                               obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                                obj['MAX_OP_TEMP'],
                                               obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
                caustic0 = caustic.DF_CAUSTIC_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['caustic'] = caustic0
                dataNaOHConcentrationY0.append(caustic0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataNaOHConcentrationY1.append(temp['PoF'])
                dataNaOHConcentrationY2.append(temp['damageTotal'] * dataCoF)
        #   CRACK_PRESENT
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       True,
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], objAmine['HEAT_TRACE'],
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])
        sulphide = Detail_DM_CAL.Df_Sulphide(objsulphide['PH'], objsulphide['H2SContent'],
                                             objsulphide['PRESENT_CYANIDE'],
                                             True, objsulphide['PWHT'],
                                             objsulphide['BRINNEL_HARDNESS'],
                                             objsulphide['CARBON_ALLOY'],
                                             objsulphide['AQUEOUS_OPERATOR'],
                                             objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                             rwassessment.assessmentdate,
                                             COMPONENT_INSTALL_DATE, ComponentNumber)
        Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(objHicsohic_H2s['PH'],
                                                     objHicsohic_H2s['H2SContent'],
                                                     objHicsohic_H2s['PRESENT_CYANIDE'],
                                                     True,
                                                     objHicsohic_H2s['PWHT'],
                                                     objHicsohic_H2s['SULFUR_CONTENT'],
                                                     objHicsohic_H2s['OnlineMonitoring'],
                                                     objHicsohic_H2s['CARBON_ALLOY'],
                                                     objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                     objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                     0, rwassessment.assessmentdate,
                                                     COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        Alkaline = Detail_DM_CAL.Df_Cacbonate(True, objAlkaline['PWHT'], objAlkaline['co3'],
                                              objAlkaline['ph'],
                                              objAlkaline['CARBON_ALLOY'], objAlkaline['AQUEOUS_OPERATOR'], 'E', 0,
                                              rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                              ComponentNumber)
        PASCC = Detail_DM_CAL.Df_PTA(True, objPASCC['ExposedSH2OOperation'],
                                     objPASCC['ExposedSH2OShutdown'],
                                     objPASCC['MAX_OP_TEMP'], objPASCC['ThermalHistory'],
                                     objPASCC['PTAMaterial'],
                                     objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                     objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                     objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        CLSCC = Detail_DM_CAL.Df_CLSCC(True, objCLSCC['ph'], objCLSCC['MAX_OP_TEMP'],
                                       objCLSCC['MIN_OP_TEMP'],
                                       objCLSCC['CHLORIDE_ION_CONTENT'],
                                       objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                       objCLSCC['AUSTENITIC_STEEL']
                                       , 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HSCHF = Detail_DM_CAL.Df_HSCHF(True, objHSCHF['HF_PRESENT'], objHSCHF['CARBON_ALLOY'],
                                       objHSCHF['PWHT'], objHSCHF['BRINNEL_HARDNESS'], 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HIC_SOHIC_HF = Detail_DM_CAL.Df_HIC_SOHIC_HF(True,
                                                     objHIC_SOHIC_HF['HF_PRESENT'], objHIC_SOHIC_HF['CARBON_ALLOY'],
                                                     objHIC_SOHIC_HF['PWHT'], objHIC_SOHIC_HF['SULFUR_CONTENT'],
                                                     objHIC_SOHIC_HF['OnlineMonitoring'], 'E', 0,
                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(True,
                                                     objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                     objEXTERN_CLSCC['MAX_OP_TEMP'],
                                                     'E', 0,
                                                     objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                     objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                     objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(True, objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                               objCUI_CLSCC['MAX_OP_TEMP'],
                                               objCUI_CLSCC['PIPING_COMPLEXITY'],
                                               objCUI_CLSCC['INSULATION_CONDITION'],
                                               objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                               objCUI_CLSCC['AUSTENITIC_STEEL'],
                                               objCUI_CLSCC['EXTERNAL_INSULATION'],
                                               objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                               objCUI_CLSCC['MIN_OP_TEMP'],
                                               objCUI_CLSCC['EXTERN_COAT_QUALITY'],
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
        caustic = Detail_DM_CAL.Df_Caustic(True, obj['HEAT_TREATMENT'],
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        dataCRACK_PRESENTX = []
        dataCRACK_PRESENTY0 = []
        dataCRACK_PRESENTY1 = []
        dataCRACK_PRESENTY2 = []
        dataCRACK_PRESENTX.append('True')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
        dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
        dataPoFTemp['cacbonat'] = Alkaline.DF_CACBONATE_API(0)
        dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
        dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
        dataPoFTemp['hschf'] = HSCHF.DF_HSCHF_API(0)
        dataPoFTemp['sohic'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(0)
        dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
        dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
        dataCRACK_PRESENTY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataCRACK_PRESENTY1.append(temp['PoF'])
        dataCRACK_PRESENTY2.append(temp['damageTotal'] * dataCoF)
        # false
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       False,
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], objAmine['HEAT_TRACE'],
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])
        sulphide = Detail_DM_CAL.Df_Sulphide(objsulphide['PH'], objsulphide['H2SContent'],
                                             objsulphide['PRESENT_CYANIDE'],
                                             False, objsulphide['PWHT'],
                                             objsulphide['BRINNEL_HARDNESS'],
                                             objsulphide['CARBON_ALLOY'],
                                             objsulphide['AQUEOUS_OPERATOR'],
                                             objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                             rwassessment.assessmentdate,
                                             COMPONENT_INSTALL_DATE, ComponentNumber)
        Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(objHicsohic_H2s['PH'],
                                                     objHicsohic_H2s['H2SContent'],
                                                     objHicsohic_H2s['PRESENT_CYANIDE'],
                                                     False,
                                                     objHicsohic_H2s['PWHT'],
                                                     objHicsohic_H2s['SULFUR_CONTENT'],
                                                     objHicsohic_H2s['OnlineMonitoring'],
                                                     objHicsohic_H2s['CARBON_ALLOY'],
                                                     objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                     objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                     0, rwassessment.assessmentdate,
                                                     COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        Alkaline = Detail_DM_CAL.Df_Cacbonate(False, objAlkaline['PWHT'], objAlkaline['co3'],
                                              objAlkaline['ph'],
                                              objAlkaline['CARBON_ALLOY'], objAlkaline['AQUEOUS_OPERATOR'], 'E', 0,
                                              rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                              ComponentNumber)
        PASCC = Detail_DM_CAL.Df_PTA(False, objPASCC['ExposedSH2OOperation'],
                                     objPASCC['ExposedSH2OShutdown'],
                                     objPASCC['MAX_OP_TEMP'], objPASCC['ThermalHistory'],
                                     objPASCC['PTAMaterial'],
                                     objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                     objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                     objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        CLSCC = Detail_DM_CAL.Df_CLSCC(False, objCLSCC['ph'], objCLSCC['MAX_OP_TEMP'],
                                       objCLSCC['MIN_OP_TEMP'],
                                       objCLSCC['CHLORIDE_ION_CONTENT'],
                                       objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                       objCLSCC['AUSTENITIC_STEEL']
                                       , 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HSCHF = Detail_DM_CAL.Df_HSCHF(False, objHSCHF['HF_PRESENT'], objHSCHF['CARBON_ALLOY'],
                                       objHSCHF['PWHT'], objHSCHF['BRINNEL_HARDNESS'], 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HIC_SOHIC_HF = Detail_DM_CAL.Df_HIC_SOHIC_HF(False,
                                                     objHIC_SOHIC_HF['HF_PRESENT'], objHIC_SOHIC_HF['CARBON_ALLOY'],
                                                     objHIC_SOHIC_HF['PWHT'], objHIC_SOHIC_HF['SULFUR_CONTENT'],
                                                     objHIC_SOHIC_HF['OnlineMonitoring'], 'E', 0,
                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(False,
                                                     objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                     objEXTERN_CLSCC['MAX_OP_TEMP'],
                                                     'E', 0,
                                                     objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                     objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                     objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(False, objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                               objCUI_CLSCC['MAX_OP_TEMP'],
                                               objCUI_CLSCC['PIPING_COMPLEXITY'],
                                               objCUI_CLSCC['INSULATION_CONDITION'],
                                               objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                               objCUI_CLSCC['AUSTENITIC_STEEL'],
                                               objCUI_CLSCC['EXTERNAL_INSULATION'],
                                               objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                               objCUI_CLSCC['MIN_OP_TEMP'],
                                               objCUI_CLSCC['EXTERN_COAT_QUALITY'],
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
        caustic = Detail_DM_CAL.Df_Caustic(False, obj['HEAT_TREATMENT'],
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        dataCRACK_PRESENTX.append('False')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
        dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
        dataPoFTemp['cacbonat'] = Alkaline.DF_CACBONATE_API(0)
        dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
        dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
        dataPoFTemp['hschf'] = HSCHF.DF_HSCHF_API(0)
        dataPoFTemp['sohic'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(0)
        dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
        dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
        dataCRACK_PRESENTY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataCRACK_PRESENTY1.append(temp['PoF'])
        dataCRACK_PRESENTY2.append(temp['damageTotal'] * dataCoF)
        # HEAT_TRACE

        caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], True,
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       obj['CRACK_PRESENT'],
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], True,
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])
        dataHEAT_TRACEX = []
        dataHEAT_TRACEY0 = []
        dataHEAT_TRACEY1 = []
        dataHEAT_TRACEY2 = []
        dataHEAT_TRACEX.append('True')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataHEAT_TRACEY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataHEAT_TRACEY1.append(temp['PoF'])
        dataHEAT_TRACEY2.append(temp['damageTotal'] * dataCoF)
        #
        caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], False,
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       obj['CRACK_PRESENT'],
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], False,
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])

        dataHEAT_TRACEX.append('False')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataHEAT_TRACEY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataHEAT_TRACEY1.append(temp['PoF'])
        dataHEAT_TRACEY2.append(temp['damageTotal'] * dataCoF)
        obj_res={}
        obj_res['dataMAX_OP_TEMPX']= dataMAX_OP_TEMPX
        obj_res['dataMAX_OP_TEMPY0']= dataMAX_OP_TEMPY0
        obj_res['dataMAX_OP_TEMPY1']= dataMAX_OP_TEMPY1
        obj_res['dataMAX_OP_TEMPY2']= dataMAX_OP_TEMPY2
        obj_res['dataNaOHConcentrationX']=dataNaOHConcentrationX
        obj_res['dataNaOHConcentrationY0']=dataNaOHConcentrationY0
        obj_res['dataNaOHConcentrationY1']=dataNaOHConcentrationY1
        obj_res['dataNaOHConcentrationY2']=dataNaOHConcentrationY2
        obj_res['dataCRACK_PRESENTX']=dataCRACK_PRESENTX
        obj_res['dataCRACK_PRESENTY0']=dataCRACK_PRESENTY0
        obj_res['dataCRACK_PRESENTY1']=dataCRACK_PRESENTY1
        obj_res['dataCRACK_PRESENTY2']=dataCRACK_PRESENTY2
        obj_res['dataHEAT_TRACEX']=dataHEAT_TRACEX
        obj_res['dataHEAT_TRACEY0']=dataHEAT_TRACEY0
        obj_res['dataHEAT_TRACEY1']=dataHEAT_TRACEY1
        obj_res['dataHEAT_TRACEY2']=dataHEAT_TRACEY2
        return obj_res
    except Exception as e:
        print(e)
def showPASCC(proposalID):

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
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['ExposedSH2OOperation'] = bool(rwequipment.presencesulphideso2)
        obj['ExposedSH2OShutdown'] = bool(rwequipment.presencesulphideso2shutdown)
        obj['MAX_OP_TEMP'] =rwstream.maxoperatingtemperature
        obj['ThermalHistory'] =rwequipment.thermalhistory
        obj['PTAMaterial'] =rwmaterial.ptamaterialcode
        obj['DOWNTIME_PROTECTED'] =bool(rwequipment.downtimeprotectionused)
        obj['PTA_SUSCEP'] =bool(rwmaterial.ispta)
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['NICKEL_ALLOY'] =bool(rwmaterial.nickelbased)
        obj['EXPOSED_SULFUR'] =bool(rwstream.exposedtosulphur)

        PASCC = Detail_DM_CAL.Df_PTA(obj['CRACK_PRESENT'], obj['ExposedSH2OOperation'], obj['ExposedSH2OShutdown'],
                                                     obj['MAX_OP_TEMP'], obj['ThermalHistory'], obj['PTAMaterial'],
                                                     obj['DOWNTIME_PROTECTED'],  obj['PTA_SUSCEP'],
                                                     obj['CARBON_ALLOY'], obj['NICKEL_ALLOY'],obj['EXPOSED_SULFUR'], 'E', 0,
                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        obj['PTA_INSP_EFF'] = PASCC.PTA_INSP_EFF
        obj['PTA_INSP_NUM'] = PASCC.PTA_INSP_NUM
        obj['Susceptibility']=PASCC.GET_SUSCEPTIBILITY_PTA()
        obj['SVI']=PASCC.SVI_PTA
        obj['age1']=PASCC.GET_AGE()
        obj['age2']=PASCC.GET_AGE()+3
        obj['age3']=PASCC.GET_AGE()+6
        obj['base1']=PASCC.DFB_PTA_API(0)
        obj['base2']=PASCC.DFB_PTA_API(3)
        obj['base3']=PASCC.DFB_PTA_API(6)
        obj['PASCC1']=PASCC.DF_PTA_API(0)
        obj['PASCC2']=PASCC.DF_PTA_API(3)
        obj['PASCC3']=PASCC.DF_PTA_API(6)

        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        dataMAX_OP_TEMPX = []
        dataMAX_OP_TEMPY0 = []
        dataMAX_OP_TEMPY1 = []
        dataMAX_OP_TEMPY2 = []
        # amine
        objAmine = {}
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
        objAmine['ComponentNumber'] = ComponentNumber
        objAmine['EquipmentName'] = EquipmentName
        objAmine['Assessment'] = rwassessment.proposalname

        objAmine['AMINE_EXPOSED'] = bool(rwstream.exposedtogasamine)
        objAmine['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objAmine['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objAmine['AMINE_SOLUTION'] = rwstream.aminesolution

        objAmine['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objAmine['HEAT_TRACE'] = bool(rwequipment.heattraced)
        objAmine['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)

        objAmine['AMINE_INSP_EFF'] = 'E'
        objAmine['AMINE_INSP_NUM'] = 0
        objAmine['PWHT'] = bool(rwequipment.pwht)
        objAmine['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objAmine['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objAmine['ComponentNumber'] = str(comp.componentnumber)
        # Df_CLSCC
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        # Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = API_COMPONENT_TYPE_NAME = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # Df_CUI
        objCui = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # EXTERNAL CLSCC
        objEXTERN_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objEXTERN_CLSCC['ComponentNumber'] = ComponentNumber
        objEXTERN_CLSCC['EquipmentNumber'] = EquipmentName
        objEXTERN_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objEXTERN_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objEXTERN_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objEXTERN_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objEXTERN_CLSCC['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # CUI_CLSCC
        objCUI_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCUI_CLSCC['ComponentNumber'] = ComponentNumber
        objCUI_CLSCC['EquipmentNumber'] = EquipmentName
        objCUI_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        objCUI_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCUI_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCUI_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCUI_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCUI_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCUI_CLSCC['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCUI_CLSCC['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCUI_CLSCC['INSULATION_CHLORIDE'] = bool(rwcoat.insulationcontainschloride)
        objCUI_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objCUI_CLSCC['EXTERNAL_INSULATION'] = bool(rwcoat.externalinsulation)

        objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCUI_CLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCUI_CLSCC['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        # HTHA
        objHTHA = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHTHA['ComponentNumber'] = ComponentNumber
        objHTHA['EquipmentNumber'] = EquipmentName
        objHTHA['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHTHA['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHTHA['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHTHA['HTHA_PRESSURE'] = rwstream.h2spartialpressure * 0.006895
        objHTHA['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objHTHA['HTHADamageObserved'] = rwcomponent.hthadamage
        objHTHA['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objHTHA['MATERIAL_SUSCEP_HTHA'] = bool(rwmaterial.ishtha)
        objHTHA['HTHA_MATERIAL'] = rwmaterial.hthamaterialcode
        objHTHA['Hydrogen'] = rwstream.hydrogen
        # TEMP_EMBRITTLE
        objTEMP_EMBRITTLE = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objTEMP_EMBRITTLE['ComponentNumber'] = ComponentNumber
        objTEMP_EMBRITTLE['EquipmentNumber'] = EquipmentName
        objTEMP_EMBRITTLE['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objTEMP_EMBRITTLE['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['TEMPER_SUSCEP'] = bool(rwmaterial.temper)
        objTEMP_EMBRITTLE['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objTEMP_EMBRITTLE['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objTEMP_EMBRITTLE['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objTEMP_EMBRITTLE['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objTEMP_EMBRITTLE['REF_TEMP'] = rwmaterial.referencetemperature
        objTEMP_EMBRITTLE['DELTA_FATT'] = rwcomponent.deltafatt
        objTEMP_EMBRITTLE['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objTEMP_EMBRITTLE['PWHT'] = bool(rwequipment.pwht)
        objTEMP_EMBRITTLE['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness

        objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Df_885
        obj885 = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj885['ComponentNumber'] = ComponentNumber
        obj885['EquipmentNumber'] = EquipmentName
        obj885['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        obj885['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj885['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj885['CHROMIUM_12'] = bool(rwmaterial.chromemoreequal12)
        obj885['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj885['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj885['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj885['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj885['REF_TEMP'] = rwmaterial.referencetemperature
        obj885['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj885['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # dfSigma
        objSigma = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objSigma['ComponentNumber'] = ComponentNumber
        objSigma['EquipmentNumber'] = EquipmentName
        objSigma['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objSigma['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objSigma['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objSigma['MIN_TEM'] = rwstream.minoperatingtemperature
        objSigma['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objSigma['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objSigma['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        objSigma['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objSigma['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation

        objSigma['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objSigma['PERCENT_SIGMA'] = rwmaterial.sigmaphase
        # chua thay su dung MIN_DESIGN_TEMP
        objSigma['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # caustic
        objcaustic = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objcaustic['ComponentNumber'] = ComponentNumber
        objcaustic['EquipmentNumber'] = EquipmentName
        objcaustic['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objcaustic['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objcaustic['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objcaustic['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objcaustic['HEAT_TREATMENT'] = rwmaterial.heattreatment
        objcaustic['NaOHConcentration'] = rwstream.naohconcentration
        objcaustic['HEAT_TRACE'] = bool(rwequipment.heattraced)
        objcaustic['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)
        objcaustic['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objcaustic['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objcaustic['PWHT'] = bool(rwequipment.pwht)

        for i in range(20, 0, -2):
            xx = obj['MAX_OP_TEMP'] - i;
            dataMAX_OP_TEMPX.append(str(xx));

            anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                           objAmine['CRACK_PRESENT'],
                                           objAmine['AMINE_SOLUTION'], xx, objAmine['HEAT_TRACE'],
                                           objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                           objAmine['AMINE_INSP_NUM'],
                                           objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           objAmine['ComponentNumber'])

            PASCC = Detail_DM_CAL.Df_PTA(obj['CRACK_PRESENT'], obj['ExposedSH2OOperation'],
                                         obj['ExposedSH2OShutdown'],
                                         xx, obj['ThermalHistory'],
                                         obj['PTAMaterial'],
                                         obj['DOWNTIME_PROTECTED'], obj['PTA_SUSCEP'],
                                         obj['CARBON_ALLOY'], obj['NICKEL_ALLOY'],
                                         obj['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)

            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)

            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)

            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)

            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'],
                                             objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)

            caustic = Detail_DM_CAL.Df_Caustic(objcaustic['CRACK_PRESENT'], objcaustic['HEAT_TREATMENT'],
                                               objcaustic['NaOHConcentration'],
                                               objcaustic['HEAT_TRACE'], objcaustic['STEAM_OUT'],
                                               xx,
                                               objcaustic['CARBON_ALLOY'], 'E', 0, 0, objcaustic['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            # BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
            #                                    objBri['CRITICAL_TEMP'],
            #                                    objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
            #                                    objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
            #                                    objBri['NOMINAL_OPERATING_CONDITIONS'],
            #                                    objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
            #                                    objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
            #                                    objBri['CARBON_ALLOY'],
            #                                    objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
            #                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
            #                                    ComponentNumber)

            PASCC0 = PASCC.DF_PTA_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
            dataPoFTemp['pta'] = PASCC0
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic.DF_CAUSTIC_API(0)
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(PASCC0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)

        for i in range(0, 20, 2):
            xx = obj['MAX_OP_TEMP'] + i;
            dataMAX_OP_TEMPX.append(str(xx));
            anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                           objAmine['CRACK_PRESENT'],
                                           objAmine['AMINE_SOLUTION'], xx, objAmine['HEAT_TRACE'],
                                           objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                           objAmine['AMINE_INSP_NUM'],
                                           objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           objAmine['ComponentNumber'])
            PASCC = Detail_DM_CAL.Df_PTA(obj['CRACK_PRESENT'], obj['ExposedSH2OOperation'],
                                         obj['ExposedSH2OShutdown'],
                                         xx, obj['ThermalHistory'],
                                         obj['PTAMaterial'],
                                         obj['DOWNTIME_PROTECTED'], obj['PTA_SUSCEP'],
                                         obj['CARBON_ALLOY'], obj['NICKEL_ALLOY'],
                                         obj['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)
            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'],
                                             objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)
            caustic = Detail_DM_CAL.Df_Caustic(objcaustic['CRACK_PRESENT'], objcaustic['HEAT_TREATMENT'],
                                               objcaustic['NaOHConcentration'],
                                               objcaustic['HEAT_TRACE'], objcaustic['STEAM_OUT'],
                                               xx,
                                               objcaustic['CARBON_ALLOY'], 'E', 0, 0, objcaustic['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            # BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
            #                                    objBri['CRITICAL_TEMP'],
            #                                    objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
            #                                    objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
            #                                    objBri['NOMINAL_OPERATING_CONDITIONS'],
            #                                    objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
            #                                    objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
            #                                    objBri['CARBON_ALLOY'],
            #                                    objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
            #                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
            #                                    ComponentNumber)
            PASCC0 = PASCC.DF_PTA_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
            dataPoFTemp['pta'] = PASCC0
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic.DF_CAUSTIC_API(0)
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(PASCC0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)
            obj_res={}
            obj_res['dataMAX_OP_TEMPX']=dataMAX_OP_TEMPX
            obj_res['dataMAX_OP_TEMPY0']=dataMAX_OP_TEMPY0
            obj_res['dataMAX_OP_TEMPY1']=dataMAX_OP_TEMPY1
            obj_res['dataMAX_OP_TEMPY2']=dataMAX_OP_TEMPY2
            return obj_res
    except Exception as e:
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def showAnime(proposalID):

    try:
        obj={}
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


        obj['AMINE_INSP_EFF']='E'
        obj['AMINE_INSP_NUM']=0
        obj['PWHT'] = bool(rwequipment.pwht)
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['ComponentNumber'] = str(comp.componentnumber)
        obj2 = {}
        obj2['HEAT_TRACE'] = False
        obj2['STEAM_OUT'] = False
        obj2['MAX_OP_TEMP'] = 30
        anime=Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'],obj['CARBON_ALLOY'],obj['CRACK_PRESENT'],obj['AMINE_SOLUTION'],obj['MAX_OP_TEMP'],obj['HEAT_TRACE'],obj['STEAM_OUT'],obj['AMINE_INSP_EFF'],obj['AMINE_INSP_NUM'],obj['PWHT'],rwassessment.assessmentdate,COMPONENT_INSTALL_DATE,obj['ComponentNumber'])
        obj['Susceptibility'] = anime.getSusceptibility_Amine()
        obj['Severity'] = anime.SVI_AMINE()
        obj['age1'] = anime.GET_AGE()
        obj['age2'] = anime.GET_AGE()+3
        obj['age3'] = anime.GET_AGE()+6
        obj['base1']=anime.DFB_AMINE_API(0)
        obj['base2']=anime.DFB_AMINE_API(3)
        obj['base3']=anime.DFB_AMINE_API(6)
        obj['amine1'] = anime.DF_AMINE_API(0)
        obj['amine2'] = anime.DF_AMINE_API(3)
        obj['amine3'] = anime.DF_AMINE_API(6)
        animeTem=Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'],obj['CARBON_ALLOY'],obj['CRACK_PRESENT'],obj['AMINE_SOLUTION'],obj2['MAX_OP_TEMP'],obj2['HEAT_TRACE'],obj2['STEAM_OUT'],obj['AMINE_INSP_EFF'],obj['AMINE_INSP_NUM'],obj['PWHT'],rwassessment.assessmentdate,COMPONENT_INSTALL_DATE,obj['ComponentNumber'])
        obj2['Susceptibility'] = animeTem.getSusceptibility_Amine()
        obj2['Severity'] = animeTem.SVI_AMINE()
        obj2['age1'] = animeTem.GET_AGE()
        obj2['age2'] = animeTem.GET_AGE() + 3
        obj2['age3'] = animeTem.GET_AGE() + 6
        obj2['base1'] = animeTem.DFB_AMINE_API(0)
        obj2['base2'] = animeTem.DFB_AMINE_API(3)
        obj2['base3'] = animeTem.DFB_AMINE_API(6)
        obj2['amine1'] = animeTem.DF_AMINE_API(0)
        obj2['amine2'] = animeTem.DF_AMINE_API(3)
        obj2['amine3'] = animeTem.DF_AMINE_API(6)


        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        dataMAX_OP_TEMPX = []
        dataMAX_OP_TEMPY0 = []
        dataMAX_OP_TEMPY1 = []
        dataMAX_OP_TEMPY2 = []
        dataAMINE_SOLUTIONX = []
        dataAMINE_SOLUTIONY0 = []
        dataAMINE_SOLUTIONY1 = []
        dataAMINE_SOLUTIONY2 = []
        # PASCC-PTA
        objPASCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objPASCC['ComponentNumber'] = ComponentNumber
        objPASCC['EquipmentNumber'] = EquipmentName
        objPASCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objPASCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objPASCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objPASCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objPASCC['ExposedSH2OOperation'] = bool(rwequipment.presencesulphideso2)
        objPASCC['ExposedSH2OShutdown'] = bool(rwequipment.presencesulphideso2shutdown)
        objPASCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objPASCC['ThermalHistory'] = rwequipment.thermalhistory
        objPASCC['PTAMaterial'] = rwmaterial.ptamaterialcode
        objPASCC['DOWNTIME_PROTECTED'] = bool(rwequipment.downtimeprotectionused)
        objPASCC['PTA_SUSCEP'] = bool(rwmaterial.ispta)
        objPASCC['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objPASCC['NICKEL_ALLOY'] = bool(rwmaterial.nickelbased)
        objPASCC['EXPOSED_SULFUR'] = bool(rwstream.exposedtosulphur)
        # Df_CLSCC
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        # Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = API_COMPONENT_TYPE_NAME = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # Df_CUI
        objCui = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # EXTERNAL CLSCC
        objEXTERN_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objEXTERN_CLSCC['ComponentNumber'] = ComponentNumber
        objEXTERN_CLSCC['EquipmentNumber'] = EquipmentName
        objEXTERN_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objEXTERN_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objEXTERN_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objEXTERN_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objEXTERN_CLSCC['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # CUI_CLSCC
        objCUI_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCUI_CLSCC['ComponentNumber'] = ComponentNumber
        objCUI_CLSCC['EquipmentNumber'] = EquipmentName
        objCUI_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        objCUI_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCUI_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCUI_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCUI_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCUI_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCUI_CLSCC['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCUI_CLSCC['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCUI_CLSCC['INSULATION_CHLORIDE'] = bool(rwcoat.insulationcontainschloride)
        objCUI_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objCUI_CLSCC['EXTERNAL_INSULATION'] = bool(rwcoat.externalinsulation)

        objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCUI_CLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCUI_CLSCC['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        # HTHA
        objHTHA = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHTHA['ComponentNumber'] = ComponentNumber
        objHTHA['EquipmentNumber'] = EquipmentName
        objHTHA['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHTHA['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHTHA['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHTHA['HTHA_PRESSURE'] = rwstream.h2spartialpressure * 0.006895
        objHTHA['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objHTHA['HTHADamageObserved'] = rwcomponent.hthadamage
        objHTHA['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objHTHA['MATERIAL_SUSCEP_HTHA'] = bool(rwmaterial.ishtha)
        objHTHA['HTHA_MATERIAL'] = rwmaterial.hthamaterialcode
        objHTHA['Hydrogen'] = rwstream.hydrogen
        # TEMP_EMBRITTLE
        objTEMP_EMBRITTLE = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objTEMP_EMBRITTLE['ComponentNumber'] = ComponentNumber
        objTEMP_EMBRITTLE['EquipmentNumber'] = EquipmentName
        objTEMP_EMBRITTLE['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objTEMP_EMBRITTLE['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['TEMPER_SUSCEP'] = bool(rwmaterial.temper)
        objTEMP_EMBRITTLE['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objTEMP_EMBRITTLE['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objTEMP_EMBRITTLE['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objTEMP_EMBRITTLE['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objTEMP_EMBRITTLE['REF_TEMP'] = rwmaterial.referencetemperature
        objTEMP_EMBRITTLE['DELTA_FATT'] = rwcomponent.deltafatt
        objTEMP_EMBRITTLE['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objTEMP_EMBRITTLE['PWHT'] = bool(rwequipment.pwht)
        objTEMP_EMBRITTLE['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness

        objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Df_885
        obj885 = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj885['ComponentNumber'] = ComponentNumber
        obj885['EquipmentNumber'] = EquipmentName
        obj885['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        obj885['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj885['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj885['CHROMIUM_12'] = bool(rwmaterial.chromemoreequal12)
        obj885['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj885['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj885['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj885['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj885['REF_TEMP'] = rwmaterial.referencetemperature
        obj885['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj885['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # dfSigma
        objSigma = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objSigma['ComponentNumber'] = ComponentNumber
        objSigma['EquipmentNumber'] = EquipmentName
        objSigma['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objSigma['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objSigma['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objSigma['MIN_TEM'] = rwstream.minoperatingtemperature
        objSigma['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objSigma['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objSigma['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        objSigma['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objSigma['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation

        objSigma['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objSigma['PERCENT_SIGMA'] = rwmaterial.sigmaphase
        # chua thay su dung MIN_DESIGN_TEMP
        objSigma['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # caustic
        objcaustic = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objcaustic['ComponentNumber'] = ComponentNumber
        objcaustic['EquipmentNumber'] = EquipmentName
        objcaustic['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objcaustic['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objcaustic['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objcaustic['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objcaustic['HEAT_TREATMENT'] = rwmaterial.heattreatment
        objcaustic['NaOHConcentration'] = rwstream.naohconcentration
        objcaustic['HEAT_TRACE'] = bool(rwequipment.heattraced)
        objcaustic['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)
        objcaustic['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objcaustic['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objcaustic['PWHT'] = bool(rwequipment.pwht)





        for i in range(20,0,-2):
            xx=obj['MAX_OP_TEMP']-i;
            dataMAX_OP_TEMPX.append(str(xx));

            anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                           obj['AMINE_SOLUTION'], xx, obj['HEAT_TRACE'],
                                           obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                           obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           obj['ComponentNumber'])

            PASCC = Detail_DM_CAL.Df_PTA(objPASCC['CRACK_PRESENT'], objPASCC['ExposedSH2OOperation'],
                                         objPASCC['ExposedSH2OShutdown'],
                                         xx, objPASCC['ThermalHistory'],
                                         objPASCC['PTAMaterial'],
                                         objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                         objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                         objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)

            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)

            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)

            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'], objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'], objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'], objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'], objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'], objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)

            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'], objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'], objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)

            caustic = Detail_DM_CAL.Df_Caustic(objcaustic['CRACK_PRESENT'], objcaustic['HEAT_TREATMENT'],
                                               objcaustic['NaOHConcentration'],
                                               objcaustic['HEAT_TRACE'], objcaustic['STEAM_OUT'],
                                               xx,
                                               objcaustic['CARBON_ALLOY'], 'E', 0, 0, objcaustic['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            # BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
            #                                    objBri['CRITICAL_TEMP'],
            #                                    objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
            #                                    objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
            #                                    objBri['NOMINAL_OPERATING_CONDITIONS'],
            #                                    objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
            #                                    objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
            #                                    objBri['CARBON_ALLOY'],
            #                                    objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
            #                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
            #                                    ComponentNumber)

            amine0 = anime.DF_AMINE_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = amine0
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic.DF_CAUSTIC_API(0)
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(amine0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)

        for i in range(0, 20, 2):
            xx = obj['MAX_OP_TEMP'] + i;
            dataMAX_OP_TEMPX.append(str(xx));
            anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                           obj['AMINE_SOLUTION'], xx, obj['HEAT_TRACE'],
                                           obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                           obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           obj['ComponentNumber'])
            PASCC = Detail_DM_CAL.Df_PTA(objPASCC['CRACK_PRESENT'], objPASCC['ExposedSH2OOperation'],
                                         objPASCC['ExposedSH2OShutdown'],
                                         xx, objPASCC['ThermalHistory'],
                                         objPASCC['PTAMaterial'],
                                         objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                         objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                         objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)
            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)
            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'], objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)
            caustic = Detail_DM_CAL.Df_Caustic(objcaustic['CRACK_PRESENT'], objcaustic['HEAT_TREATMENT'],
                                               objcaustic['NaOHConcentration'],
                                               objcaustic['HEAT_TRACE'], objcaustic['STEAM_OUT'],
                                               xx,
                                               objcaustic['CARBON_ALLOY'], 'E', 0, 0, objcaustic['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            # BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
            #                                    objBri['CRITICAL_TEMP'],
            #                                    objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
            #                                    objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
            #                                    objBri['NOMINAL_OPERATING_CONDITIONS'],
            #                                    objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
            #                                    objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
            #                                    objBri['CARBON_ALLOY'],
            #                                    objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
            #                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
            #                                    ComponentNumber)
            amine0 = anime.DF_AMINE_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = amine0
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic.DF_CAUSTIC_API(0)
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(amine0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)
        # AMINE_SOLUTION
        xx = 'Diethanolamine DEA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Diglycolamine DGA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Disopropanolamine DIPA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Methyldiethanolamine MDEA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Monoethanolamine MEA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Sulfinol'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        # AMINE_EXPOSED
        dataAMINE_EXPOSEDX = []
        dataAMINE_EXPOSEDY0 = []
        dataAMINE_EXPOSEDY1 = []
        dataAMINE_EXPOSEDY2 = []
        xx = 'True'
        dataAMINE_EXPOSEDX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(True, obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       obj['AMINE_SOLUTION'], obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'], obj['PWHT'],
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_EXPOSEDY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_EXPOSEDY1.append(temp['PoF'])
        dataAMINE_EXPOSEDY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'False'


        dataAMINE_EXPOSEDX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(False, obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       obj['AMINE_SOLUTION'], obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'], obj['PWHT'],
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_EXPOSEDY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_EXPOSEDY1.append(temp['PoF'])
        dataAMINE_EXPOSEDY2.append(temp['damageTotal'] * dataCoF)
        obj_res={}
        obj_res['dataMAX_OP_TEMPX']=dataMAX_OP_TEMPX
        obj_res['dataMAX_OP_TEMPY0']=dataMAX_OP_TEMPY0
        obj_res['dataMAX_OP_TEMPY1']=dataMAX_OP_TEMPY1
        obj_res['dataMAX_OP_TEMPY2']=dataMAX_OP_TEMPY2
        obj_res['dataAMINE_SOLUTIONX']=dataAMINE_SOLUTIONX
        obj_res['dataAMINE_SOLUTIONY0']=dataAMINE_SOLUTIONY0
        obj_res['dataAMINE_SOLUTIONY1']=dataAMINE_SOLUTIONY1
        obj_res['dataAMINE_SOLUTIONY2']=dataAMINE_SOLUTIONY2
        obj_res['dataAMINE_EXPOSEDX']=dataAMINE_SOLUTIONX
        obj_res['dataAMINE_EXPOSEDY0']=dataAMINE_SOLUTIONY0
        obj_res['dataAMINE_EXPOSEDY1']=dataAMINE_SOLUTIONY1
        obj_res['dataAMINE_EXPOSEDY2']=dataAMINE_SOLUTIONY2
        return obj_res
    except Exception as e:
        print(e)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def AllDamageFactor(proposalID):
    try:
        data = []
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        # print("check low", rwcomponent.confidencecorrosionrate)
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        damageMachinsm=models.RwDamageMechanism.objects.filter(id_dm=proposalID)[0]
        # damageMachinsm = models.RwDamageMechanism.objects.get(id_dm=proposalID)
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
        obj['ComponentNumber'] = ComponentNumber
        obj['EquipmentNumber'] = EquipmentName
        obj['Assessment'] = rwassessment.proposalname

        obj['AllowableStress'] = rwcomponent.allowablestress
        obj['MinimunRequiredThickness'] = rwcomponent.minreqthickness
        obj['WeltJointEfficiency'] = rwcomponent.weldjointefficiency
        # print('WeltJointEfficiency'+str(obj['WeltJointEfficiency']))
        obj['CorrosionRate'] = rwcomponent.currentcorrosionrate
        obj['Diameter'] = rwcomponent.nominaldiameter
        obj['NominalThickness'] = rwcomponent.nominalthickness
        obj['CurentThickness'] = rwcomponent.currentthickness
        obj['ChemicalInjection'] = rwcomponent.chemicalinjection
        obj['HighlyEffectiveInspectionforChemicalInjection'] = rwcomponent.highlyinjectioninsp
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['deadLegs'] = rwequipment.containsdeadlegs
        obj['InternalCladding'] = rwcoat.internalcladding
        obj['CladdingThickness'] = rwcoat.claddingthickness
        obj['CladdingCorrosionRate'] = rwcoat.claddingcorrosionrate
        obj['confidencecorrosionrate'] = rwcomponent.confidencecorrosionrate
        obj['YeildStrength'] = rwmaterial.yieldstrength
        obj['TensileStrength'] = rwmaterial.tensilestrength
        obj['DesignPressure'] = rwmaterial.designpressure
        obj['Onlinemonitoring'] = rwequipment.onlinemonitoring
        obj['HighEffectiveDeadlegs'] = rwequipment.highlydeadleginsp
        obj['LastInspectionDate'] = damageMachinsm.lastinspdate.strftime('%Y-%m-%d')
        obj['NumberofInspection'] = damageMachinsm.numberofinspections

        obj['shapeFactor'] = comptype.shapefactor
        obj['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename

        thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                     obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                     rwmaterial.corrosionallowance, bool(rwcomponent.releasepreventionbarrier),
                                     obj['CladdingThickness'],
                                     obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                     0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                     bool(obj['deadLegs']), rwequipment.tankismaintained,
                                     rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                     obj['WeltJointEfficiency'], obj['AllowableStress'], obj['TensileStrength'],
                                     obj['YeildStrength'], rwcomponent.structuralthickness,
                                     rwcomponent.minstructuralthickness, obj['DesignPressure'], obj['shapeFactor'],
                                     obj['confidencecorrosionrate'], EquipmentType, rwassessment.assessmentdate,
                                     rwassessment.commisstiondate, ComponentNumber, APIComponentType)

        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        dataNominalThicknessX = []
        dataNominalThicknessY0 = []
        dataNominalThicknessY1 = []
        dataNominalThicknessY2 = []
        #
        dataCurentThicknessX = []
        dataCurentThicknessY0 = []
        dataCurentThicknessY1 = []
        dataCurentThicknessY2 = []
        #
        dataCorrosionRateX = []
        dataCorrosionRateY0 = []
        dataCorrosionRateY1 = []
        dataCorrosionRateY2 = []
        # Minimum Required Thickness
        dataMinimunRequiredThicknessX = []
        dataMinimunRequiredThicknessY0 = []
        dataMinimunRequiredThicknessY1 = []
        dataMinimunRequiredThicknessY2 = []
        #Nominal thickness
        #Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename

        # Df_CUI
        objCui={}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename

        # DF_BRITTLE
        objBri = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objBri['ComponentNumber'] = ComponentNumber
        objBri['EquipmentNumber'] = EquipmentName
        objBri['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objBri['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objBri['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objBri['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objBri['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objBri['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objBri['PWHT'] = bool(rwequipment.pwht)
        objBri['REF_TEMP'] = rwmaterial.referencetemperature
        objBri['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness
        objBri['FABRICATED_STEEL'] = bool(rwcomponent.fabricatedsteel)
        objBri['EQUIPMENT_SATISFIED'] = bool(rwcomponent.equipmentsatisfied)
        objBri['NOMINAL_OPERATING_CONDITIONS'] = bool(rwcomponent.nominaloperatingconditions)
        objBri['CET_THE_MAWP'] = bool(rwcomponent.cetgreaterorequal)
        objBri['CYCLIC_SERVICE'] = bool(rwcomponent.cyclicservice)
        objBri['PresenceCyanides'] = bool(rwstream.cyanide)
        objBri['EQUIPMENT_CIRCUIT_SHOCK'] = bool(rwcomponent.equipmentcircuitshock)
        objBri['NomalThick'] = rwcomponent.nominalthickness
        if objBri['NomalThick'] <= 12.7:
            objBri['equal_127'] = True
        else:
            objBri['equal_127'] = False
        if objBri['NomalThick'] <= 50.8:
            objBri['equal_508'] = True
        else:
            objBri['equal_508'] = False
        objBri['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objBri['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        objBri['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        # BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
        #                                    objBri['CRITICAL_TEMP'],
        #                                    objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
        #                                    objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
        #                                    objBri['NOMINAL_OPERATING_CONDITIONS'],
        #                                    objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
        #                                    objBri['EQUIPMENT_CIRCUIT_SHOCK'], objBri['NomalThick'],
        #                                    objBri['CARBON_ALLOY'],
        #                                    objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
        #                                    rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
        #                                    ComponentNumber)
        for i in range(20,0,-2):
            if (obj['NominalThickness']-i)>0:
                dataNominalThicknessX.append(str(obj['NominalThickness']-i));
                xx=obj['NominalThickness']-i;
                print(obj['CladdingThickness'])
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], xx, obj['CurentThickness'],
                                             obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingThickness'],
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber,
                                             APIComponentType)
                EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                         objExCor['EXTERN_COAT_QUALITY'],
                                                                         objExCor['EXTERNAL_EVIRONMENT'],
                                                                         objExCor['CUI_PERCENT_2'],
                                                                         objExCor['CUI_PERCENT_3'],
                                                                         objExCor['CUI_PERCENT_4'],
                                                                         objExCor['CUI_PERCENT_5'],
                                                                         objExCor['CUI_PERCENT_6'],
                                                                         objExCor['SUPPORT_COATING'],
                                                                         objExCor['INTERFACE_SOIL_WATER'],
                                                                         objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                         objExCor['CARBON_ALLOY'],
                                                                         objExCor['MAX_OP_TEMP'],
                                                                         objExCor['MIN_OP_TEMP'],
                                                                         objExCor['EXTERNAL_INSP_EFF'],
                                                                         objExCor['EXTERNAL_INSP_NUM'],
                                                                         objExCor['NoINSP_EXTERNAL'],
                                                                         objExCor['APIComponentType'],
                                                                         xx,
                                                                         objExCor['CurrentThick'],
                                                                         objExCor['WeldJointEffciency'],
                                                                         objExCor['YieldStrengthDesignTemp'],
                                                                         objExCor['TensileStrengthDesignTemp'],
                                                                         objExCor['ShapeFactor'],
                                                                         objExCor[
                                                                             'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                         objExCor['CR_Confidents_Level'],
                                                                         objExCor['AllowableStress'],
                                                                         objExCor['MinThickReq'],
                                                                         objExCor['StructuralThickness'],
                                                                         objExCor['Pressure'],
                                                                         objExCor['Diametter'],
                                                                         rwassessment.assessmentdate,
                                                                         COMPONENT_INSTALL_DATE,
                                                                         ComponentNumber)
                CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                            objCui['CUI_PERCENT_3'],
                                            objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                            objCui['CUI_PERCENT_6'],
                                            objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                            objCui['CUI_PERCENT_9'],
                                            objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                            objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                            objCui['INTERFACE_SOIL_WATER'],
                                            objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                            , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                            objCui['MIN_OP_TEMP'],
                                            objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                            objCui['APIComponentType']
                                            , xx, objCui['CurrentThick'],
                                            objCui['CR_Confidents_Level'],
                                            objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                            objCui['WeldJointEffciency'],
                                            objCui['YieldStrengthDesignTemp'],
                                            objCui['TensileStrengthDesignTemp'],
                                            objCui['AllowableStress'], objCui['MinThickReq'],
                                            objCui['StructuralThickness'],
                                            objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                            objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                            rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                            ComponentNumber)
                BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
                                                   objBri['CRITICAL_TEMP'],
                                                   objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
                                                   objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
                                                   objBri['NOMINAL_OPERATING_CONDITIONS'],
                                                   objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
                                                   objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
                                                   objBri['CARBON_ALLOY'],
                                                   objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)
                thin0=thin.DF_THINNING_API(0)
                dataPoFTemp=dataPoF

                dataPoFTemp['thin']=thin0
                dataPoFTemp['external_corrosion']=EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
                dataPoFTemp['cui']=CUIF.DF_CUI_API(0)
                dataPoFTemp['brittle']=BRITTLE.DF_BRITTLE_API(0)
                dataNominalThicknessY0.append(thin0)
                # dataNominalThicknessY1.append(thin.DF_THINNING_API(36))
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataNominalThicknessY1.append(temp['PoF'])
                dataNominalThicknessY2.append(temp['damageTotal'] * dataCoF)
                # print(ReCalculate.calculatePoF(proposalID,dataPoF))

        for i in range(0, 20, 2):
            dataNominalThicknessX.append(str(obj['NominalThickness'] + i));
            xx = obj['NominalThickness'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], xx, obj['CurentThickness'],
                                         obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                         obj['CladdingThickness'],
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber,APIComponentType)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     objExCor['MAX_OP_TEMP'],
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     xx,
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , xx, objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            BRITTLE = Detail_DM_CAL.DF_BRITTLE(objBri['PRESSSURE_CONTROL'], objBri['MIN_TEMP_PRESSURE'],
                                               objBri['CRITICAL_TEMP'],
                                               objBri['PWHT'], objBri['REF_TEMP'], objBri['BRITTLE_THICK'],
                                               objBri['FABRICATED_STEEL'], objBri['EQUIPMENT_SATISFIED'],
                                               objBri['NOMINAL_OPERATING_CONDITIONS'],
                                               objBri['CET_THE_MAWP'], objBri['CYCLIC_SERVICE'],
                                               objBri['EQUIPMENT_CIRCUIT_SHOCK'], xx,
                                               objBri['CARBON_ALLOY'],
                                               objBri['MIN_DESIGN_TEMP'], objBri['MAX_OP_TEMP'],
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataNominalThicknessY0.append(thin0)
            # dataNominalThicknessY1.append(thin.DF_THINNING_API(36))
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataNominalThicknessY1.append(temp['PoF'])
            dataNominalThicknessY2.append(temp['damageTotal'] * dataCoF)

        #Minimun Measured Thickness


        for i in range(20,0,-2):
            if (obj['CurentThickness'] - i) > 0:
                dataCurentThicknessX.append(str(obj['CurentThickness'] - i));
                xx = obj['CurentThickness'] - i;
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], xx,
                                             obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                             obj['CladdingThickness'],
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber,
                                             APIComponentType)
                EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                         objExCor['EXTERN_COAT_QUALITY'],
                                                                         objExCor['EXTERNAL_EVIRONMENT'],
                                                                         objExCor['CUI_PERCENT_2'],
                                                                         objExCor['CUI_PERCENT_3'],
                                                                         objExCor['CUI_PERCENT_4'],
                                                                         objExCor['CUI_PERCENT_5'],
                                                                         objExCor['CUI_PERCENT_6'],
                                                                         objExCor['SUPPORT_COATING'],
                                                                         objExCor['INTERFACE_SOIL_WATER'],
                                                                         objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                         objExCor['CARBON_ALLOY'],
                                                                         objExCor['MAX_OP_TEMP'],
                                                                         objExCor['MIN_OP_TEMP'],
                                                                         objExCor['EXTERNAL_INSP_EFF'],
                                                                         objExCor['EXTERNAL_INSP_NUM'],
                                                                         objExCor['NoINSP_EXTERNAL'],
                                                                         objExCor['APIComponentType'],
                                                                         objExCor['NomalThick'],
                                                                         xx,
                                                                         objExCor['WeldJointEffciency'],
                                                                         objExCor['YieldStrengthDesignTemp'],
                                                                         objExCor['TensileStrengthDesignTemp'],
                                                                         objExCor['ShapeFactor'],
                                                                         objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                         objExCor['CR_Confidents_Level'],
                                                                         objExCor['AllowableStress'],
                                                                         objExCor['MinThickReq'],
                                                                         objExCor['StructuralThickness'],
                                                                         objExCor['Pressure'],
                                                                         objExCor['Diametter'],
                                                                         rwassessment.assessmentdate,
                                                                         COMPONENT_INSTALL_DATE,
                                                                         ComponentNumber)
                CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                            objCui['CUI_PERCENT_3'],
                                            objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                            objCui['CUI_PERCENT_6'],
                                            objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                            objCui['CUI_PERCENT_9'],
                                            objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                            objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                            objCui['INTERFACE_SOIL_WATER'],
                                            objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                            , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                            objCui['MIN_OP_TEMP'],
                                            objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                            objCui['APIComponentType']
                                            , objCui['NomalThick'], xx,
                                            objCui['CR_Confidents_Level'],
                                            objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                            objCui['WeldJointEffciency'],
                                            objCui['YieldStrengthDesignTemp'],
                                            objCui['TensileStrengthDesignTemp'],
                                            objCui['AllowableStress'], objCui['MinThickReq'],
                                            objCui['StructuralThickness'],
                                            objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                            objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                            rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                            ComponentNumber)
                # dataCurentThicknessY0.append(thin.DF_THINNING_API(0))
                # dataCurentThicknessY1.append(thin.DF_THINNING_API(36))
                # dataCurentThicknessY2.append(thin.DF_THINNING_API(72))
                thin0 = thin.DF_THINNING_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['thin'] = thin0
                dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
                dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

                dataCurentThicknessY0.append(thin0)
                # dataNominalThicknessY1.append(thin.DF_THINNING_API(36))
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataCurentThicknessY1.append(temp['PoF'])
                dataCurentThicknessY2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            dataCurentThicknessX.append(str(obj['CurentThickness'] + i));
            xx = obj['CurentThickness'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], xx,
                                         obj['MinimunRequiredThickness'], obj['CorrosionRate'],
                                         obj['CladdingThickness'],
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber,
                                         APIComponentType)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     objExCor['MAX_OP_TEMP'],
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     xx,
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], xx,
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

            dataCurentThicknessY0.append(thin0)

            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataCurentThicknessY1.append(temp['PoF'])
            dataCurentThicknessY2.append(temp['damageTotal'] * dataCoF)
            # dataCurentThicknessY0.append(thin.DF_THINNING_API(0))
            # dataCurentThicknessY1.append(thin.DF_THINNING_API(36))
            # dataCurentThicknessY2.append(thin.DF_THINNING_API(72))
        #Current Corrosion Rate
        for i in range(20,0,-2):
            if (obj['CorrosionRate'] - i) > 0:
                dataCorrosionRateX.append(str(obj['CorrosionRate'] - i));
                xx = obj['CorrosionRate'] - i;
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                             obj['MinimunRequiredThickness'], xx,
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingThickness'],
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber,
                                             APIComponentType)
                thin0 = thin.DF_THINNING_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['thin'] = thin0
                dataCorrosionRateY0.append(thin0)

                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataCorrosionRateY1.append(temp['PoF'])
                dataCorrosionRateY2.append(temp['damageTotal'] * dataCoF)
                # dataCorrosionRateY0.append(thin.DF_THINNING_API(0))
                # dataCorrosionRateY1.append(thin.DF_THINNING_API(36))
                # dataCorrosionRateY2.append(thin.DF_THINNING_API(72))
        for i in range(0, 20, 2):
            dataCorrosionRateX.append(str(obj['CorrosionRate'] + i));
            xx = obj['CorrosionRate'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                         obj['MinimunRequiredThickness'], xx,
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingThickness'],
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber,
                                         APIComponentType)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataCorrosionRateY0.append(thin0)

            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataCorrosionRateY1.append(temp['PoF'])
            dataCorrosionRateY2.append(temp['damageTotal'] * dataCoF)


        # Minimum Required Thickness
        for i in range(20,0,-2):
            if (obj['MinimunRequiredThickness'] - i) > 0:
                dataMinimunRequiredThicknessX.append(str(obj['MinimunRequiredThickness'] - i));
                xx = obj['MinimunRequiredThickness'] - i;
                thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                             xx, obj['CorrosionRate'],
                                             rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                             obj['CladdingThickness'],
                                             obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                             0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                             bool(obj['deadLegs']), rwequipment.tankismaintained,
                                             rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                             obj['WeltJointEfficiency'], obj['AllowableStress'],
                                             obj['TensileStrength'],
                                             obj['YeildStrength'], rwcomponent.structuralthickness,
                                             rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                             obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber,
                                             APIComponentType)
                EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                         objExCor['EXTERN_COAT_QUALITY'],
                                                                         objExCor['EXTERNAL_EVIRONMENT'],
                                                                         objExCor['CUI_PERCENT_2'],
                                                                         objExCor['CUI_PERCENT_3'],
                                                                         objExCor['CUI_PERCENT_4'],
                                                                         objExCor['CUI_PERCENT_5'],
                                                                         objExCor['CUI_PERCENT_6'],
                                                                         objExCor['SUPPORT_COATING'],
                                                                         objExCor['INTERFACE_SOIL_WATER'],
                                                                         objExCor[
                                                                             'EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                         objExCor['CARBON_ALLOY'],
                                                                         objExCor['MAX_OP_TEMP'],
                                                                         objExCor['MIN_OP_TEMP'],
                                                                         objExCor['EXTERNAL_INSP_EFF'],
                                                                         objExCor['EXTERNAL_INSP_NUM'],
                                                                         objExCor['NoINSP_EXTERNAL'],
                                                                         objExCor['APIComponentType'],
                                                                         objExCor['NomalThick'],
                                                                         objExCor['CurrentThick'],
                                                                         objExCor['WeldJointEffciency'],
                                                                         objExCor['YieldStrengthDesignTemp'],
                                                                         objExCor['TensileStrengthDesignTemp'],
                                                                         objExCor['ShapeFactor'],
                                                                         objExCor[
                                                                             'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                         objExCor['CR_Confidents_Level'],
                                                                         objExCor['AllowableStress'],
                                                                         xx,
                                                                         objExCor['StructuralThickness'],
                                                                         objExCor['Pressure'],
                                                                         objExCor['Diametter'],
                                                                         rwassessment.assessmentdate,
                                                                         COMPONENT_INSTALL_DATE,
                                                                         ComponentNumber)
                CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                            objCui['CUI_PERCENT_3'],
                                            objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                            objCui['CUI_PERCENT_6'],
                                            objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                            objCui['CUI_PERCENT_9'],
                                            objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                            objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                            objCui['INTERFACE_SOIL_WATER'],
                                            objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                            , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                            objCui['MIN_OP_TEMP'],
                                            objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                            objCui['APIComponentType']
                                            , objCui['NomalThick'], objExCor['CurrentThick'],
                                            objCui['CR_Confidents_Level'],
                                            objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                            objCui['WeldJointEffciency'],
                                            objCui['YieldStrengthDesignTemp'],
                                            objCui['TensileStrengthDesignTemp'],
                                            objCui['AllowableStress'], xx,
                                            objCui['StructuralThickness'],
                                            objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                            objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                            rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                            ComponentNumber)
                thin0 = thin.DF_THINNING_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['thin'] = thin0
                dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
                dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

                dataMinimunRequiredThicknessY0.append(thin0)

                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataMinimunRequiredThicknessY1.append(temp['PoF'])
                dataMinimunRequiredThicknessY2.append(temp['damageTotal'] * dataCoF)
                # dataMinimunRequiredThicknessY0.append(thin.DF_THINNING_API(0))
                # dataMinimunRequiredThicknessY1.append(thin.DF_THINNING_API(36))
                # dataMinimunRequiredThicknessY2.append(thin.DF_THINNING_API(72))
        for i in range(0, 20, 2):
            dataMinimunRequiredThicknessX.append(str(obj['MinimunRequiredThickness'] + i));
            xx = obj['MinimunRequiredThickness'] + i;
            thin = Detail_DM_CAL.Df_Thin(obj['Diameter'], obj['NominalThickness'], obj['CurentThickness'],
                                         xx, obj['CorrosionRate'],
                                         rwmaterial.corrosionallowance,bool(rwcomponent.releasepreventionbarrier),
                                         obj['CladdingThickness'],
                                         obj['CladdingCorrosionRate'], bool(obj['InternalCladding']),
                                         0, "E", obj['Onlinemonitoring'], obj['HighEffectiveDeadlegs'],
                                         bool(obj['deadLegs']), rwequipment.tankismaintained,
                                         rwequipment.adjustmentsettle, rwequipment.componentiswelded,
                                         obj['WeltJointEfficiency'], obj['AllowableStress'],
                                         obj['TensileStrength'],
                                         obj['YeildStrength'], rwcomponent.structuralthickness,
                                         rwcomponent.minstructuralthickness, obj['DesignPressure'],
                                         obj['shapeFactor'], obj['confidencecorrosionrate'], EquipmentType,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber,
                                         APIComponentType)
            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor[
                                                                         'EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     objExCor['MAX_OP_TEMP'],
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     xx,
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)
            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], objCui['MAX_OP_TEMP'],
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objExCor['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], xx,
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)
            thin0 = thin.DF_THINNING_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['thin'] = thin0
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)

            dataMinimunRequiredThicknessY0.append(thin0)

            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMinimunRequiredThicknessY1.append(temp['PoF'])
            dataMinimunRequiredThicknessY2.append(temp['damageTotal'] * dataCoF)
            # dataMinimunRequiredThicknessY0.append(thin.DF_THINNING_API(0))
            # dataMinimunRequiredThicknessY1.append(thin.DF_THINNING_API(36))
            # dataMinimunRequiredThicknessY2.append(thin.DF_THINNING_API(72))


        # gop Alkaline
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

        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
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
        obj['PWHT'] = PWHT
        obj['co3'] = CO3_CONTENT
        obj['ph'] = PH
        AQUEOUS_OPERATOR = bool(rwstream.aqueousoperation)
        obj['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], obj['co3'], obj['ph'],
                                              obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                              rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, ComponentNumber)
        dataCO3X = []
        dataCO3Y0 = []
        dataCO3Y1 = []
        dataCO3Y2 = []
        dataphX = []
        dataphY0 = []
        dataphY1 = []
        dataphY2 = []
        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        objsulphide = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objsulphide['ComponentNumber'] = ComponentNumber
        objsulphide['EquipmentNumber'] = EquipmentName
        objsulphide['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objsulphide['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objsulphide['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objsulphide['PH'] = rwstream.waterph
        objsulphide['H2SContent'] = rwstream.h2sinwater
        objsulphide['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objsulphide['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objsulphide['PWHT'] = bool(rwequipment.pwht)
        objsulphide['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        objsulphide['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objsulphide['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objsulphide['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)
        #
        objHicsohic_H2s = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHicsohic_H2s['ComponentNumber'] = ComponentNumber
        objHicsohic_H2s['EquipmentNumber'] = EquipmentName
        objHicsohic_H2s['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHicsohic_H2s['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHicsohic_H2s['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHicsohic_H2s['PH'] = rwstream.waterph
        objHicsohic_H2s['H2SContent'] = rwstream.h2sinwater
        objHicsohic_H2s['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objHicsohic_H2s['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHicsohic_H2s['PWHT'] = bool(rwequipment.pwht)

        objHicsohic_H2s['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        objHicsohic_H2s['OnlineMonitoring'] = rwequipment.onlinemonitoring
        objHicsohic_H2s['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHicsohic_H2s['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)

        #
        #
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)

        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        # thay doi obj['CO3']
        for i in range(20, 0, -2):
            xx = obj['co3'] - i
            if xx >= 0:
                dataCO3X.append(str(xx))

                Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], xx, obj['ph'],
                                                      obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                      rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                      ComponentNumber)
                Alkaline0 = Alkaline.DF_CACBONATE_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['cacbonat'] = Alkaline0
                dataCO3Y0.append(Alkaline0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataCO3Y1.append(temp['PoF'])
                dataCO3Y2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            xx = obj['co3'] + i;
            dataCO3X.append(str(xx));

            Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], xx, obj['ph'],
                                                  obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                  rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                  ComponentNumber)
            Alkaline0 = Alkaline.DF_CACBONATE_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['cacbonat'] = Alkaline0
            dataCO3Y0.append(Alkaline0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataCO3Y1.append(temp['PoF'])
            dataCO3Y2.append(temp['damageTotal'] * dataCoF)
            #     thay doi obj['ph']
        for i in range(20, 0, -2):
            xx = obj['ph'] - i
            if xx >= 0:
                dataphX.append(str(xx))

                Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], obj['co3'], xx,
                                                      obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                      rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                      ComponentNumber)
                sulphide = Detail_DM_CAL.Df_Sulphide(xx, objsulphide['H2SContent'],
                                                     objsulphide['PRESENT_CYANIDE'],
                                                     objsulphide['CRACK_PRESENT'], objsulphide['PWHT'],
                                                     objsulphide['BRINNEL_HARDNESS'],
                                                     objsulphide['CARBON_ALLOY'],
                                                     objsulphide['AQUEOUS_OPERATOR'],
                                                     objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                                     rwassessment.assessmentdate,
                                                     COMPONENT_INSTALL_DATE, ComponentNumber)
                Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(xx,
                                                             objHicsohic_H2s['H2SContent'],
                                                             objHicsohic_H2s['PRESENT_CYANIDE'],
                                                             objHicsohic_H2s['CRACK_PRESENT'],
                                                             objHicsohic_H2s['PWHT'],
                                                             objHicsohic_H2s['SULFUR_CONTENT'],
                                                             objHicsohic_H2s['OnlineMonitoring'],
                                                             objHicsohic_H2s['CARBON_ALLOY'],
                                                             objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                             objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                             0, rwassessment.assessmentdate,
                                                             COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
                CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'],
                                               objCLSCC['MAX_OP_TEMP'], objCLSCC['MIN_OP_TEMP'],
                                               objCLSCC['CHLORIDE_ION_CONTENT'],
                                               objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                               objCLSCC['AUSTENITIC_STEEL']
                                               , 'E', 0,
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
                Alkaline0 = Alkaline.DF_CACBONATE_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['cacbonat'] = Alkaline0
                dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
                dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
                dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
                dataphY0.append(Alkaline0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataphY1.append(temp['PoF'])
                dataphY2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            xx = obj['ph'] + i;
            dataphX.append(str(xx));

            Alkaline = Detail_DM_CAL.Df_Cacbonate(obj['CRACK_PRESENT'], obj['PWHT'], obj['co3'], xx,
                                                  obj['CARBON_ALLOY'], obj['AQUEOUS_OPERATOR'], 'E', 0,
                                                  rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                  ComponentNumber)
            sulphide = Detail_DM_CAL.Df_Sulphide(xx, objsulphide['H2SContent'],
                                                 objsulphide['PRESENT_CYANIDE'],
                                                 objsulphide['CRACK_PRESENT'], objsulphide['PWHT'],
                                                 objsulphide['BRINNEL_HARDNESS'],
                                                 objsulphide['CARBON_ALLOY'],
                                                 objsulphide['AQUEOUS_OPERATOR'],
                                                 objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                                 rwassessment.assessmentdate,
                                                 COMPONENT_INSTALL_DATE, ComponentNumber)
            Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(xx,
                                                         objHicsohic_H2s['H2SContent'],
                                                         objHicsohic_H2s['PRESENT_CYANIDE'],
                                                         objHicsohic_H2s['CRACK_PRESENT'],
                                                         objHicsohic_H2s['PWHT'],
                                                         objHicsohic_H2s['SULFUR_CONTENT'],
                                                         objHicsohic_H2s['OnlineMonitoring'],
                                                         objHicsohic_H2s['CARBON_ALLOY'],
                                                         objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                         objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                         0, rwassessment.assessmentdate,
                                                         COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'],
                                           objCLSCC['MAX_OP_TEMP'], objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)
            Alkaline0 = Alkaline.DF_CACBONATE_API(0)
            dataPoFTemp = dataPoF
            dataPoFTemp['cacbonat'] = Alkaline0
            dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
            dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataphY0.append(Alkaline0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataphY1.append(temp['PoF'])
            dataphY2.append(temp['damageTotal'] * dataCoF)
        # showCaustic
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
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        obj['HEAT_TREATMENT'] = rwmaterial.heattreatment
        obj['NaOHConcentration'] = rwstream.naohconcentration
        obj['HEAT_TRACE'] = bool(rwequipment.heattraced)
        obj['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)
        obj['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        obj['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        obj['PWHT'] = bool(rwequipment.pwht)

        caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'], obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'], obj['MAX_OP_TEMP'], obj['CARBON_ALLOY'],
                                           'E', 0, 0, obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)
        obj['CAUSTIC_INSP_EFF'] = caustic.CAUSTIC_INSP_EFF
        obj['CACBONATE_INSP_NUM'] = caustic.CACBONATE_INSP_NUM
        obj['CAUSTIC_INSP_NUM'] = caustic.CAUSTIC_INSP_NUM
        obj['plotinArea'] = caustic.plotinArea
        obj['Susceptibility'] = caustic.getSusceptibility_Caustic
        obj['SVI'] = caustic.SVI_CAUSTIC
        obj['age1'] = caustic.GET_AGE()
        obj['age2'] = caustic.GET_AGE() + 3
        obj['age3'] = caustic.GET_AGE() + 6
        obj['base1'] = caustic.DFB_CAUSTIC_API(0)
        obj['base2'] = caustic.DFB_CAUSTIC_API(3)
        obj['base3'] = caustic.DFB_CAUSTIC_API(6)
        obj['caustic1'] = caustic.DF_CAUSTIC_API(0)
        obj['caustic2'] = caustic.DF_CAUSTIC_API(3)
        obj['caustic3'] = caustic.DF_CAUSTIC_API(6)
        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)
        dataMAX_OP_TEMPX = []
        dataMAX_OP_TEMPY0 = []
        dataMAX_OP_TEMPY1 = []
        dataMAX_OP_TEMPY2 = []
        #
        objHIC_SOHIC_HF = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHIC_SOHIC_HF['ComponentNumber'] = ComponentNumber
        objHIC_SOHIC_HF['EquipmentNumber'] = EquipmentName
        objHIC_SOHIC_HF['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHIC_SOHIC_HF['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHIC_SOHIC_HF['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHIC_SOHIC_HF['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHIC_SOHIC_HF['HF_PRESENT'] = bool(rwstream.hydrofluoric)
        objHIC_SOHIC_HF['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHIC_SOHIC_HF['PWHT'] = bool(rwequipment.pwht)
        objHIC_SOHIC_HF['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        objHIC_SOHIC_HF['OnlineMonitoring'] = rwequipment.onlinemonitoring
        #
        objHSCHF = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHSCHF['ComponentNumber'] = ComponentNumber
        objHSCHF['EquipmentNumber'] = EquipmentName
        objHSCHF['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHSCHF['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHSCHF['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHSCHF['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHSCHF['HF_PRESENT'] = bool(rwstream.hydrofluoric)
        objHSCHF['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHSCHF['PWHT'] = bool(rwequipment.pwht)
        objHSCHF['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        #
        objAlkaline = {}
        objAlkaline['ComponentNumber'] = ComponentNumber
        objAlkaline['EquipmentNumber'] = EquipmentName
        objAlkaline['Assessment'] = rwassessment.proposalname
        objAlkaline['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objAlkaline['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
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
        objAlkaline['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objAlkaline['PWHT'] = PWHT
        objAlkaline['co3'] = CO3_CONTENT
        objAlkaline['ph'] = PH
        objAlkaline['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        #
        objsulphide = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objsulphide['ComponentNumber'] = ComponentNumber
        objsulphide['EquipmentNumber'] = EquipmentName
        objsulphide['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objsulphide['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objsulphide['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objsulphide['PH'] = rwstream.waterph
        objsulphide['H2SContent'] = rwstream.h2sinwater
        objsulphide['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objsulphide['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objsulphide['PWHT'] = bool(rwequipment.pwht)
        objsulphide['BRINNEL_HARDNESS'] = rwcomponent.brinnelhardness
        objsulphide['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objsulphide['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objsulphide['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)
        #
        objHicsohic_H2s = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHicsohic_H2s['ComponentNumber'] = ComponentNumber
        objHicsohic_H2s['EquipmentNumber'] = EquipmentName
        objHicsohic_H2s['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHicsohic_H2s['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHicsohic_H2s['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHicsohic_H2s['PH'] = rwstream.waterph
        objHicsohic_H2s['H2SContent'] = rwstream.h2sinwater
        objHicsohic_H2s['PRESENT_CYANIDE'] = bool(rwstream.cyanide)
        objHicsohic_H2s['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objHicsohic_H2s['PWHT'] = bool(rwequipment.pwht)

        objHicsohic_H2s['SULFUR_CONTENT'] = rwmaterial.sulfurcontent
        objHicsohic_H2s['OnlineMonitoring'] = rwequipment.onlinemonitoring
        objHicsohic_H2s['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objHicsohic_H2s['AQUEOUS_OPERATOR'] = bool(rwstream.aqueousoperation)
        objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'] = bool(rwstream.h2s)

        # PASCC-PTA
        objPASCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objPASCC['ComponentNumber'] = ComponentNumber
        objPASCC['EquipmentNumber'] = EquipmentName
        objPASCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objPASCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objPASCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objPASCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objPASCC['ExposedSH2OOperation'] = bool(rwequipment.presencesulphideso2)
        objPASCC['ExposedSH2OShutdown'] = bool(rwequipment.presencesulphideso2shutdown)
        objPASCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objPASCC['ThermalHistory'] = rwequipment.thermalhistory
        objPASCC['PTAMaterial'] = rwmaterial.ptamaterialcode
        objPASCC['DOWNTIME_PROTECTED'] = bool(rwequipment.downtimeprotectionused)
        objPASCC['PTA_SUSCEP'] = bool(rwmaterial.ispta)
        objPASCC['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objPASCC['NICKEL_ALLOY'] = bool(rwmaterial.nickelbased)
        objPASCC['EXPOSED_SULFUR'] = bool(rwstream.exposedtosulphur)
        # Df_CLSCC
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        # Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = API_COMPONENT_TYPE_NAME = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # Df_CUI
        objCui = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # EXTERNAL CLSCC
        objEXTERN_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objEXTERN_CLSCC['ComponentNumber'] = ComponentNumber
        objEXTERN_CLSCC['EquipmentNumber'] = EquipmentName
        objEXTERN_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objEXTERN_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objEXTERN_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objEXTERN_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objEXTERN_CLSCC['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # CUI_CLSCC
        objCUI_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCUI_CLSCC['ComponentNumber'] = ComponentNumber
        objCUI_CLSCC['EquipmentNumber'] = EquipmentName
        objCUI_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        objCUI_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCUI_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCUI_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCUI_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCUI_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCUI_CLSCC['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCUI_CLSCC['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCUI_CLSCC['INSULATION_CHLORIDE'] = bool(rwcoat.insulationcontainschloride)
        objCUI_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objCUI_CLSCC['EXTERNAL_INSULATION'] = bool(rwcoat.externalinsulation)

        objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCUI_CLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCUI_CLSCC['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        # HTHA
        objHTHA = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHTHA['ComponentNumber'] = ComponentNumber
        objHTHA['EquipmentNumber'] = EquipmentName
        objHTHA['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHTHA['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHTHA['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHTHA['HTHA_PRESSURE'] = rwstream.h2spartialpressure * 0.006895
        objHTHA['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objHTHA['HTHADamageObserved'] = rwcomponent.hthadamage
        objHTHA['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objHTHA['MATERIAL_SUSCEP_HTHA'] = bool(rwmaterial.ishtha)
        objHTHA['HTHA_MATERIAL'] = rwmaterial.hthamaterialcode
        objHTHA['Hydrogen'] = rwstream.hydrogen
        # TEMP_EMBRITTLE
        objTEMP_EMBRITTLE = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objTEMP_EMBRITTLE['ComponentNumber'] = ComponentNumber
        objTEMP_EMBRITTLE['EquipmentNumber'] = EquipmentName
        objTEMP_EMBRITTLE['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objTEMP_EMBRITTLE['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['TEMPER_SUSCEP'] = bool(rwmaterial.temper)
        objTEMP_EMBRITTLE['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objTEMP_EMBRITTLE['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objTEMP_EMBRITTLE['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objTEMP_EMBRITTLE['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objTEMP_EMBRITTLE['REF_TEMP'] = rwmaterial.referencetemperature
        objTEMP_EMBRITTLE['DELTA_FATT'] = rwcomponent.deltafatt
        objTEMP_EMBRITTLE['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objTEMP_EMBRITTLE['PWHT'] = bool(rwequipment.pwht)
        objTEMP_EMBRITTLE['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness

        objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Df_885
        obj885 = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj885['ComponentNumber'] = ComponentNumber
        obj885['EquipmentNumber'] = EquipmentName
        obj885['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        obj885['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj885['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj885['CHROMIUM_12'] = bool(rwmaterial.chromemoreequal12)
        obj885['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj885['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj885['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj885['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj885['REF_TEMP'] = rwmaterial.referencetemperature
        obj885['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj885['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # dfSigma
        objSigma = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objSigma['ComponentNumber'] = ComponentNumber
        objSigma['EquipmentNumber'] = EquipmentName
        objSigma['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objSigma['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objSigma['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objSigma['MIN_TEM'] = rwstream.minoperatingtemperature
        objSigma['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objSigma['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objSigma['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        objSigma['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objSigma['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation

        objSigma['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objSigma['PERCENT_SIGMA'] = rwmaterial.sigmaphase
        # chua thay su dung MIN_DESIGN_TEMP
        objSigma['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Amine
        objAmine = {}
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
        objAmine['ComponentNumber'] = ComponentNumber
        objAmine['EquipmentName'] = EquipmentName
        objAmine['Assessment'] = rwassessment.proposalname

        objAmine['AMINE_EXPOSED'] = bool(rwstream.exposedtogasamine)
        objAmine['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objAmine['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objAmine['AMINE_SOLUTION'] = rwstream.aminesolution

        objAmine['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objAmine['HEAT_TRACE'] = bool(rwequipment.heattraced)
        objAmine['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)

        objAmine['AMINE_INSP_EFF'] = 'E'
        objAmine['AMINE_INSP_NUM'] = 0
        objAmine['PWHT'] = bool(rwequipment.pwht)
        objAmine['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objAmine['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objAmine['ComponentNumber'] = str(comp.componentnumber)
        # MAX_OP_TEMP
        for i in range(20, 0, -2):
            xx = obj['MAX_OP_TEMP'] - i;
            dataMAX_OP_TEMPX.append(str(xx));

            anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                           objAmine['CRACK_PRESENT'],
                                           objAmine['AMINE_SOLUTION'], xx, objAmine['HEAT_TRACE'],
                                           objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                           objAmine['AMINE_INSP_NUM'],
                                           objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           objAmine['ComponentNumber'])

            PASCC = Detail_DM_CAL.Df_PTA(objPASCC['CRACK_PRESENT'], objPASCC['ExposedSH2OOperation'],
                                         objPASCC['ExposedSH2OShutdown'],
                                         xx, objPASCC['ThermalHistory'],
                                         objPASCC['PTAMaterial'],
                                         objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                         objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                         objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)

            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)

            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)

            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)

            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'],
                                             objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)

            caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                               obj['NaOHConcentration'],
                                               obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                               xx,
                                               obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            caustic0 = caustic.DF_CAUSTIC_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic0
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(caustic0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)
        # MAX_OP_TEMP
        for i in range(0, 20, 2):
            xx = obj['MAX_OP_TEMP'] + i;
            dataMAX_OP_TEMPX.append(str(xx));

            anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                           objAmine['CRACK_PRESENT'],
                                           objAmine['AMINE_SOLUTION'], xx, objAmine['HEAT_TRACE'],
                                           objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                           objAmine['AMINE_INSP_NUM'],
                                           objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           objAmine['ComponentNumber'])

            PASCC = Detail_DM_CAL.Df_PTA(objPASCC['CRACK_PRESENT'], objPASCC['ExposedSH2OOperation'],
                                         objPASCC['ExposedSH2OShutdown'],
                                         xx, objPASCC['ThermalHistory'],
                                         objPASCC['PTAMaterial'],
                                         objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                         objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                         objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            CLSCC = Detail_DM_CAL.Df_CLSCC(objCLSCC['CRACK_PRESENT'], objCLSCC['ph'], xx,
                                           objCLSCC['MIN_OP_TEMP'],
                                           objCLSCC['CHLORIDE_ION_CONTENT'],
                                           objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                           objCLSCC['AUSTENITIC_STEEL']
                                           , 'E', 0,
                                           rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                           ComponentNumber)

            EXTERNAL_CORROSION = Detail_DM_CAL.Df_EXTERNAL_CORROSION(COMPONENT_INSTALL_DATE,
                                                                     objExCor['EXTERN_COAT_QUALITY'],
                                                                     objExCor['EXTERNAL_EVIRONMENT'],
                                                                     objExCor['CUI_PERCENT_2'],
                                                                     objExCor['CUI_PERCENT_3'],
                                                                     objExCor['CUI_PERCENT_4'],
                                                                     objExCor['CUI_PERCENT_5'],
                                                                     objExCor['CUI_PERCENT_6'],
                                                                     objExCor['SUPPORT_COATING'],
                                                                     objExCor['INTERFACE_SOIL_WATER'],
                                                                     objExCor['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                                     objExCor['CARBON_ALLOY'],
                                                                     xx,
                                                                     objExCor['MIN_OP_TEMP'],
                                                                     objExCor['EXTERNAL_INSP_EFF'],
                                                                     objExCor['EXTERNAL_INSP_NUM'],
                                                                     objExCor['NoINSP_EXTERNAL'],
                                                                     objExCor['APIComponentType'],
                                                                     objExCor['NomalThick'],
                                                                     objExCor['CurrentThick'],
                                                                     objExCor['WeldJointEffciency'],
                                                                     objExCor['YieldStrengthDesignTemp'],
                                                                     objExCor['TensileStrengthDesignTemp'],
                                                                     objExCor['ShapeFactor'],
                                                                     objExCor[
                                                                         'MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                                                     objExCor['CR_Confidents_Level'],
                                                                     objExCor['AllowableStress'],
                                                                     objExCor['MinThickReq'],
                                                                     objExCor['StructuralThickness'],
                                                                     objExCor['Pressure'],
                                                                     objExCor['Diametter'],
                                                                     rwassessment.assessmentdate,
                                                                     COMPONENT_INSTALL_DATE,
                                                                     ComponentNumber)

            CUIF = Detail_DM_CAL.Df_CUI(objCui['EXTERNAL_EVIRONMENT'], objCui['CUI_PERCENT_2'],
                                        objCui['CUI_PERCENT_3'],
                                        objCui['CUI_PERCENT_4'], objCui['CUI_PERCENT_5'],
                                        objCui['CUI_PERCENT_6'],
                                        objCui['CUI_PERCENT_7'], objCui['CUI_PERCENT_8'],
                                        objCui['CUI_PERCENT_9'],
                                        objCui['INSULATION_TYPE'], objCui['PIPING_COMPLEXITY'],
                                        objCui['INSULATION_CONDITION'], objCui['SUPPORT_COATING'],
                                        objCui['INTERFACE_SOIL_WATER'],
                                        objCui['EXTERNAL_EXPOSED_FLUID_MIST']
                                        , objCui['CARBON_ALLOY'], xx,
                                        objCui['MIN_OP_TEMP'],
                                        objCui['CUI_INSP_EFF'], objCui['CUI_INSP_NUM'],
                                        objCui['APIComponentType']
                                        , objCui['NomalThick'], objCui['CurrentThick'],
                                        objCui['CR_Confidents_Level'],
                                        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'],
                                        objCui['WeldJointEffciency'],
                                        objCui['YieldStrengthDesignTemp'],
                                        objCui['TensileStrengthDesignTemp'],
                                        objCui['AllowableStress'], objCui['MinThickReq'],
                                        objCui['StructuralThickness'],
                                        objCui['Pressure'], objCui['Diametter'], objCui['ShapeFactor'],
                                        objCui['COMPONENT_INSTALL_DATE'], objCui['EXTERN_COAT_QUALITY'],
                                        rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                        ComponentNumber)

            EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(objEXTERN_CLSCC['CRACK_PRESENT'],
                                                         objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                         xx,
                                                         'E', 0,
                                                         objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                         objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                         objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                         ComponentNumber)
            CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(objCUI_CLSCC['CRACK_PRESENT'],
                                                   objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                                   xx,
                                                   objCUI_CLSCC['PIPING_COMPLEXITY'],
                                                   objCUI_CLSCC['INSULATION_CONDITION'],
                                                   objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                                   objCUI_CLSCC['AUSTENITIC_STEEL'],
                                                   objCUI_CLSCC['EXTERNAL_INSULATION'],
                                                   objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                   objCUI_CLSCC['MIN_OP_TEMP'],
                                                   objCUI_CLSCC['EXTERN_COAT_QUALITY'],

                                                   rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                   ComponentNumber)

            HTHA = Detail_DM_CAL.DF_HTHA(objHTHA['HTHA_PRESSURE'], objHTHA['CRITICAL_TEMP'],
                                         objHTHA['HTHADamageObserved'],
                                         xx, objHTHA['MATERIAL_SUSCEP_HTHA'], objHTHA['HTHA_MATERIAL'],
                                         objHTHA['Hydrogen'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            TEMP_EMBRITTLE = Detail_DM_CAL.Df_TEMP_EMBRITTLE(objTEMP_EMBRITTLE['TEMPER_SUSCEP'],
                                                             objTEMP_EMBRITTLE['CARBON_ALLOY'],
                                                             xx,
                                                             objTEMP_EMBRITTLE['MIN_OP_TEMP'],
                                                             objTEMP_EMBRITTLE['PRESSSURE_CONTROL'],
                                                             objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'],
                                                             objTEMP_EMBRITTLE['REF_TEMP'],
                                                             objTEMP_EMBRITTLE['DELTA_FATT'],
                                                             objTEMP_EMBRITTLE['CRITICAL_TEMP'],
                                                             objTEMP_EMBRITTLE['PWHT'],
                                                             objTEMP_EMBRITTLE['BRITTLE_THICK'],
                                                             objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'],
                                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                             ComponentNumber)
            df885 = Detail_DM_CAL.Df_885(obj885['CHROMIUM_12'], obj885['MIN_OP_TEMP'], xx,
                                         obj885['PRESSSURE_CONTROL'], obj885['MIN_TEMP_PRESSURE'],
                                         obj885['REF_TEMP'],
                                         obj885['CRITICAL_TEMP'], obj885['MIN_DESIGN_TEMP'],
                                         rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                         ComponentNumber)

            dfSigma = Detail_DM_CAL.Df_SIGMA(objSigma['MIN_TEM'], objSigma['AUSTENITIC_STEEL'],
                                             objSigma['MIN_OP_TEMP'],
                                             xx,
                                             objSigma['PRESSSURE_CONTROL'], objSigma['MIN_TEMP_PRESSURE'],
                                             objSigma['CRITICAL_TEMP'],
                                             objSigma['PERCENT_SIGMA'],
                                             rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                             ComponentNumber)

            caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                               obj['NaOHConcentration'],
                                               obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                               xx,
                                               obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                               rwassessment.assessmentdate,
                                               COMPONENT_INSTALL_DATE, ComponentNumber)
            caustic0 = caustic.DF_CAUSTIC_API(0)
            dataPoFTemp = dataPoF

            dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
            dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
            dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
            dataPoFTemp['external_corrosion'] = EXTERNAL_CORROSION.DF_EXTERNAL_CORROSION_API(0)
            dataPoFTemp['cui'] = CUIF.DF_CUI_API(0)
            dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
            dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
            dataPoFTemp['htha'] = HTHA.DF_HTHA_API(0)
            dataPoFTemp['embrittle'] = TEMP_EMBRITTLE.DF_TEMP_EMBRITTLE_API(0)
            dataPoFTemp['885'] = df885.DF_885_API(0)
            dataPoFTemp['sigma'] = dfSigma.DF_SIGMA_API(0)
            dataPoFTemp['caustic'] = caustic0
            # dataPoFTemp['brittle'] = BRITTLE.DF_BRITTLE_API(0)
            dataMAX_OP_TEMPY0.append(caustic0)
            temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
            dataMAX_OP_TEMPY1.append(temp['PoF'])
            dataMAX_OP_TEMPY2.append(temp['damageTotal'] * dataCoF)
        # NaOHConcentration
        dataNaOHConcentrationX = []
        dataNaOHConcentrationY0 = []
        dataNaOHConcentrationY1 = []
        dataNaOHConcentrationY2 = []
        for i in range(20, 0, -2):
            xx = obj['NaOHConcentration'] - i;
            if xx >= 0:
                dataNaOHConcentrationX.append(str(xx));
                caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                                   xx,
                                                   obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                                   obj['MAX_OP_TEMP'],
                                                   obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                                   rwassessment.assessmentdate,
                                                   COMPONENT_INSTALL_DATE, ComponentNumber)
                caustic0 = caustic.DF_CAUSTIC_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['caustic'] = caustic0
                dataNaOHConcentrationY0.append(caustic0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataNaOHConcentrationY1.append(temp['PoF'])
                dataNaOHConcentrationY2.append(temp['damageTotal'] * dataCoF)
        for i in range(0, 20, 2):
            xx = obj['NaOHConcentration'] + i;
            if xx <= 100:
                dataNaOHConcentrationX.append(str(xx));
                caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], obj['HEAT_TREATMENT'],
                                                   xx,
                                                   obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                                   obj['MAX_OP_TEMP'],
                                                   obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                                   rwassessment.assessmentdate,
                                                   COMPONENT_INSTALL_DATE, ComponentNumber)
                caustic0 = caustic.DF_CAUSTIC_API(0)
                dataPoFTemp = dataPoF
                dataPoFTemp['caustic'] = caustic0
                dataNaOHConcentrationY0.append(caustic0)
                temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
                dataNaOHConcentrationY1.append(temp['PoF'])
                dataNaOHConcentrationY2.append(temp['damageTotal'] * dataCoF)
        # CRACK_PRESENT
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       True,
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], objAmine['HEAT_TRACE'],
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])
        sulphide = Detail_DM_CAL.Df_Sulphide(objsulphide['PH'], objsulphide['H2SContent'],
                                             objsulphide['PRESENT_CYANIDE'],
                                             True, objsulphide['PWHT'],
                                             objsulphide['BRINNEL_HARDNESS'],
                                             objsulphide['CARBON_ALLOY'],
                                             objsulphide['AQUEOUS_OPERATOR'],
                                             objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                             rwassessment.assessmentdate,
                                             COMPONENT_INSTALL_DATE, ComponentNumber)
        Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(objHicsohic_H2s['PH'],
                                                     objHicsohic_H2s['H2SContent'],
                                                     objHicsohic_H2s['PRESENT_CYANIDE'],
                                                     True,
                                                     objHicsohic_H2s['PWHT'],
                                                     objHicsohic_H2s['SULFUR_CONTENT'],
                                                     objHicsohic_H2s['OnlineMonitoring'],
                                                     objHicsohic_H2s['CARBON_ALLOY'],
                                                     objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                     objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                     0, rwassessment.assessmentdate,
                                                     COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        Alkaline = Detail_DM_CAL.Df_Cacbonate(True, objAlkaline['PWHT'], objAlkaline['co3'],
                                              objAlkaline['ph'],
                                              objAlkaline['CARBON_ALLOY'], objAlkaline['AQUEOUS_OPERATOR'], 'E', 0,
                                              rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                              ComponentNumber)
        PASCC = Detail_DM_CAL.Df_PTA(True, objPASCC['ExposedSH2OOperation'],
                                     objPASCC['ExposedSH2OShutdown'],
                                     objPASCC['MAX_OP_TEMP'], objPASCC['ThermalHistory'],
                                     objPASCC['PTAMaterial'],
                                     objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                     objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                     objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        CLSCC = Detail_DM_CAL.Df_CLSCC(True, objCLSCC['ph'], objCLSCC['MAX_OP_TEMP'],
                                       objCLSCC['MIN_OP_TEMP'],
                                       objCLSCC['CHLORIDE_ION_CONTENT'],
                                       objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                       objCLSCC['AUSTENITIC_STEEL']
                                       , 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HSCHF = Detail_DM_CAL.Df_HSCHF(True, objHSCHF['HF_PRESENT'], objHSCHF['CARBON_ALLOY'],
                                       objHSCHF['PWHT'], objHSCHF['BRINNEL_HARDNESS'], 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HIC_SOHIC_HF = Detail_DM_CAL.Df_HIC_SOHIC_HF(True,
                                                     objHIC_SOHIC_HF['HF_PRESENT'], objHIC_SOHIC_HF['CARBON_ALLOY'],
                                                     objHIC_SOHIC_HF['PWHT'], objHIC_SOHIC_HF['SULFUR_CONTENT'],
                                                     objHIC_SOHIC_HF['OnlineMonitoring'], 'E', 0,
                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(True,
                                                     objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                     objEXTERN_CLSCC['MAX_OP_TEMP'],
                                                     'E', 0,
                                                     objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                     objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                     objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(True, objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                               objCUI_CLSCC['MAX_OP_TEMP'],
                                               objCUI_CLSCC['PIPING_COMPLEXITY'],
                                               objCUI_CLSCC['INSULATION_CONDITION'],
                                               objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                               objCUI_CLSCC['AUSTENITIC_STEEL'],
                                               objCUI_CLSCC['EXTERNAL_INSULATION'],
                                               objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                               objCUI_CLSCC['MIN_OP_TEMP'],
                                               objCUI_CLSCC['EXTERN_COAT_QUALITY'],
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
        caustic = Detail_DM_CAL.Df_Caustic(True, obj['HEAT_TREATMENT'],
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        dataCRACK_PRESENTX = []
        dataCRACK_PRESENTY0 = []
        dataCRACK_PRESENTY1 = []
        dataCRACK_PRESENTY2 = []
        dataCRACK_PRESENTX.append('True')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
        dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
        dataPoFTemp['cacbonat'] = Alkaline.DF_CACBONATE_API(0)
        dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
        dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
        dataPoFTemp['hschf'] = HSCHF.DF_HSCHF_API(0)
        dataPoFTemp['sohic'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(0)
        dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
        dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
        dataCRACK_PRESENTY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataCRACK_PRESENTY1.append(temp['PoF'])
        dataCRACK_PRESENTY2.append(temp['damageTotal'] * dataCoF)
        # false
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       False,
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], objAmine['HEAT_TRACE'],
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])
        sulphide = Detail_DM_CAL.Df_Sulphide(objsulphide['PH'], objsulphide['H2SContent'],
                                             objsulphide['PRESENT_CYANIDE'],
                                             False, objsulphide['PWHT'],
                                             objsulphide['BRINNEL_HARDNESS'],
                                             objsulphide['CARBON_ALLOY'],
                                             objsulphide['AQUEOUS_OPERATOR'],
                                             objsulphide['ENVIRONMENT_H2S_CONTENT'], 'E', 0,
                                             rwassessment.assessmentdate,
                                             COMPONENT_INSTALL_DATE, ComponentNumber)
        Hicsohic_H2s = Detail_DM_CAL.Df_Hicsohic_H2s(objHicsohic_H2s['PH'],
                                                     objHicsohic_H2s['H2SContent'],
                                                     objHicsohic_H2s['PRESENT_CYANIDE'],
                                                     False,
                                                     objHicsohic_H2s['PWHT'],
                                                     objHicsohic_H2s['SULFUR_CONTENT'],
                                                     objHicsohic_H2s['OnlineMonitoring'],
                                                     objHicsohic_H2s['CARBON_ALLOY'],
                                                     objHicsohic_H2s['AQUEOUS_OPERATOR'],
                                                     objHicsohic_H2s['ENVIRONMENT_H2S_CONTENT'], 'E',
                                                     0, rwassessment.assessmentdate,
                                                     COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        Alkaline = Detail_DM_CAL.Df_Cacbonate(False, objAlkaline['PWHT'], objAlkaline['co3'],
                                              objAlkaline['ph'],
                                              objAlkaline['CARBON_ALLOY'], objAlkaline['AQUEOUS_OPERATOR'], 'E', 0,
                                              rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                              ComponentNumber)
        PASCC = Detail_DM_CAL.Df_PTA(False, objPASCC['ExposedSH2OOperation'],
                                     objPASCC['ExposedSH2OShutdown'],
                                     objPASCC['MAX_OP_TEMP'], objPASCC['ThermalHistory'],
                                     objPASCC['PTAMaterial'],
                                     objPASCC['DOWNTIME_PROTECTED'], objPASCC['PTA_SUSCEP'],
                                     objPASCC['CARBON_ALLOY'], objPASCC['NICKEL_ALLOY'],
                                     objPASCC['EXPOSED_SULFUR'], 'E', 0,
                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                     ComponentNumber)
        CLSCC = Detail_DM_CAL.Df_CLSCC(False, objCLSCC['ph'], objCLSCC['MAX_OP_TEMP'],
                                       objCLSCC['MIN_OP_TEMP'],
                                       objCLSCC['CHLORIDE_ION_CONTENT'],
                                       objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'],
                                       objCLSCC['AUSTENITIC_STEEL']
                                       , 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HSCHF = Detail_DM_CAL.Df_HSCHF(False, objHSCHF['HF_PRESENT'], objHSCHF['CARBON_ALLOY'],
                                       objHSCHF['PWHT'], objHSCHF['BRINNEL_HARDNESS'], 'E', 0,
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       ComponentNumber)
        HIC_SOHIC_HF = Detail_DM_CAL.Df_HIC_SOHIC_HF(False,
                                                     objHIC_SOHIC_HF['HF_PRESENT'], objHIC_SOHIC_HF['CARBON_ALLOY'],
                                                     objHIC_SOHIC_HF['PWHT'], objHIC_SOHIC_HF['SULFUR_CONTENT'],
                                                     objHIC_SOHIC_HF['OnlineMonitoring'], 'E', 0,
                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        EXTERN_CLSCC = Detail_DM_CAL.Df_EXTERN_CLSCC(False,
                                                     objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'],
                                                     objEXTERN_CLSCC['MAX_OP_TEMP'],
                                                     'E', 0,
                                                     objEXTERN_CLSCC['AUSTENITIC_STEEL'],
                                                     objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                                     objEXTERN_CLSCC['MIN_DESIGN_TEMP'],

                                                     rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                                     ComponentNumber)
        CUI_CLSCC = Detail_DM_CAL.Df_CUI_CLSCC(False, objCUI_CLSCC['EXTERNAL_EVIRONMENT'],
                                               objCUI_CLSCC['MAX_OP_TEMP'],
                                               objCUI_CLSCC['PIPING_COMPLEXITY'],
                                               objCUI_CLSCC['INSULATION_CONDITION'],
                                               objCUI_CLSCC['INSULATION_CHLORIDE'], 'E', 0,
                                               objCUI_CLSCC['AUSTENITIC_STEEL'],
                                               objCUI_CLSCC['EXTERNAL_INSULATION'],
                                               objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'],
                                               objCUI_CLSCC['MIN_OP_TEMP'],
                                               objCUI_CLSCC['EXTERN_COAT_QUALITY'],
                                               rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                               ComponentNumber)
        caustic = Detail_DM_CAL.Df_Caustic(False, obj['HEAT_TREATMENT'],
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        dataCRACK_PRESENTX.append('False')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataPoFTemp['sulphide'] = sulphide.DF_SULPHIDE_API(0)
        dataPoFTemp['hicsohic_h2s'] = Hicsohic_H2s.DF_HICSOHIC_H2S_API(0)
        dataPoFTemp['cacbonat'] = Alkaline.DF_CACBONATE_API(0)
        dataPoFTemp['pta'] = PASCC.DF_PTA_API(0)
        dataPoFTemp['clscc'] = CLSCC.DF_CLSCC_API(0)
        dataPoFTemp['hschf'] = HSCHF.DF_HSCHF_API(0)
        dataPoFTemp['sohic'] = HIC_SOHIC_HF.DF_HIC_SOHIC_HF_API(0)
        dataPoFTemp['extern_clscc'] = EXTERN_CLSCC.DF_EXTERN_CLSCC_API(0)
        dataPoFTemp['cui_clscc'] = CUI_CLSCC.DF_CUI_CLSCC_API(0)
        dataCRACK_PRESENTY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataCRACK_PRESENTY1.append(temp['PoF'])
        dataCRACK_PRESENTY2.append(temp['damageTotal'] * dataCoF)
        # HEAT_TRACE

        caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], True,
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       obj['CRACK_PRESENT'],
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], True,
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])
        dataHEAT_TRACEX = []
        dataHEAT_TRACEY0 = []
        dataHEAT_TRACEY1 = []
        dataHEAT_TRACEY2 = []
        dataHEAT_TRACEX.append('True')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataHEAT_TRACEY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataHEAT_TRACEY1.append(temp['PoF'])
        dataHEAT_TRACEY2.append(temp['damageTotal'] * dataCoF)
        #
        caustic = Detail_DM_CAL.Df_Caustic(obj['CRACK_PRESENT'], False,
                                           obj['NaOHConcentration'],
                                           obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                           obj['MAX_OP_TEMP'],
                                           obj['CARBON_ALLOY'], 'E', 0, 0, obj['PWHT'],
                                           rwassessment.assessmentdate,
                                           COMPONENT_INSTALL_DATE, ComponentNumber)
        anime = Detail_DM_CAL.Df_Amine(objAmine['AMINE_EXPOSED'], objAmine['CARBON_ALLOY'],
                                       obj['CRACK_PRESENT'],
                                       objAmine['AMINE_SOLUTION'], objAmine['MAX_OP_TEMP'], False,
                                       objAmine['STEAM_OUT'], objAmine['AMINE_INSP_EFF'],
                                       objAmine['AMINE_INSP_NUM'],
                                       objAmine['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       objAmine['ComponentNumber'])

        dataHEAT_TRACEX.append('False')
        caustic0 = caustic.DF_CAUSTIC_API(0)
        dataPoFTemp = dataPoF
        dataPoFTemp['caustic'] = caustic0
        dataPoFTemp['amine'] = anime.DF_AMINE_API(0)
        dataHEAT_TRACEY0.append(caustic0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataHEAT_TRACEY1.append(temp['PoF'])
        dataHEAT_TRACEY2.append(temp['damageTotal'] * dataCoF)

        # showAnime
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
        obj['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj['ComponentNumber'] = str(comp.componentnumber)
        obj2 = {}
        obj2['HEAT_TRACE'] = False
        obj2['STEAM_OUT'] = False
        obj2['MAX_OP_TEMP'] = 30
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       obj['AMINE_SOLUTION'], obj['MAX_OP_TEMP'], obj['HEAT_TRACE'], obj['STEAM_OUT'],
                                       obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'], obj['PWHT'],
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, obj['ComponentNumber'])
        obj['Susceptibility'] = anime.getSusceptibility_Amine()
        obj['Severity'] = anime.SVI_AMINE()
        obj['age1'] = anime.GET_AGE()
        obj['age2'] = anime.GET_AGE() + 3
        obj['age3'] = anime.GET_AGE() + 6
        obj['base1'] = anime.DFB_AMINE_API(0)
        obj['base2'] = anime.DFB_AMINE_API(3)
        obj['base3'] = anime.DFB_AMINE_API(6)
        obj['amine1'] = anime.DF_AMINE_API(0)
        obj['amine2'] = anime.DF_AMINE_API(3)
        obj['amine3'] = anime.DF_AMINE_API(6)
        animeTem = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                          obj['AMINE_SOLUTION'], obj2['MAX_OP_TEMP'], obj2['HEAT_TRACE'],
                                          obj2['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'], obj['PWHT'],
                                          rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, obj['ComponentNumber'])
        obj2['Susceptibility'] = animeTem.getSusceptibility_Amine()
        obj2['Severity'] = animeTem.SVI_AMINE()
        obj2['age1'] = animeTem.GET_AGE()
        obj2['age2'] = animeTem.GET_AGE() + 3
        obj2['age3'] = animeTem.GET_AGE() + 6
        obj2['base1'] = animeTem.DFB_AMINE_API(0)
        obj2['base2'] = animeTem.DFB_AMINE_API(3)
        obj2['base3'] = animeTem.DFB_AMINE_API(6)
        obj2['amine1'] = animeTem.DF_AMINE_API(0)
        obj2['amine2'] = animeTem.DF_AMINE_API(3)
        obj2['amine3'] = animeTem.DF_AMINE_API(6)

        EquipmentType = models.EquipmentType.objects.get(
            equipmenttypeid=models.EquipmentMaster.objects.get(
                equipmentid=comp.equipmentid_id).equipmenttypeid_id).equipmenttypename
        if (EquipmentType == 'Tank'):
            dataCoF = models.RwCaTank.objects.get(id=proposalID).consequence
            dataPoF = ReCalculate.calculateHelpTank(proposalID)
        else:
            dataCoF = models.RwFullFcof.objects.get(id=proposalID).fcofvalue
            dataPoF = ReCalculate.calculateHelpNormal(proposalID)

        dataAMINE_SOLUTIONX = []
        dataAMINE_SOLUTIONY0 = []
        dataAMINE_SOLUTIONY1 = []
        dataAMINE_SOLUTIONY2 = []
        # PASCC-PTA
        objPASCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objPASCC['ComponentNumber'] = ComponentNumber
        objPASCC['EquipmentNumber'] = EquipmentName
        objPASCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objPASCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objPASCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objPASCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objPASCC['ExposedSH2OOperation'] = bool(rwequipment.presencesulphideso2)
        objPASCC['ExposedSH2OShutdown'] = bool(rwequipment.presencesulphideso2shutdown)
        objPASCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objPASCC['ThermalHistory'] = rwequipment.thermalhistory
        objPASCC['PTAMaterial'] = rwmaterial.ptamaterialcode
        objPASCC['DOWNTIME_PROTECTED'] = bool(rwequipment.downtimeprotectionused)
        objPASCC['PTA_SUSCEP'] = bool(rwmaterial.ispta)
        objPASCC['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objPASCC['NICKEL_ALLOY'] = bool(rwmaterial.nickelbased)
        objPASCC['EXPOSED_SULFUR'] = bool(rwstream.exposedtosulphur)
        # Df_CLSCC
        objCLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCLSCC['ComponentNumber'] = ComponentNumber
        objCLSCC['EquipmentNumber'] = EquipmentName
        objCLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objCLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCLSCC['ph'] = rwstream.waterph
        objCLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCLSCC['CHLORIDE_ION_CONTENT'] = rwstream.chloride
        objCLSCC['INTERNAL_EXPOSED_FLUID_MIST'] = bool(rwstream.materialexposedtoclint)
        objCLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        # Df_EXTERNAL_CORROSION
        objExCor = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objExCor['ComponentNumber'] = ComponentNumber
        objExCor['EquipmentNumber'] = EquipmentName
        objExCor['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        objExCor['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objExCor['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objExCor['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objExCor['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objExCor['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objExCor['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objExCor['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objExCor['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objExCor['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objExCor['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objExCor['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objExCor['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objExCor['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objExCor['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objExCor['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objExCor['EXTERNAL_INSP_EFF'] = 'E'
        objExCor['EXTERNAL_INSP_NUM'] = 0
        objExCor['NoINSP_EXTERNAL'] = 0
        objExCor['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objExCor['NomalThick'] = rwcomponent.nominalthickness
        objExCor['CurrentThick'] = rwcomponent.currentthickness
        objExCor['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objExCor['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objExCor['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objExCor['ShapeFactor'] = comptype.shapefactor
        objExCor['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objExCor['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objExCor['AllowableStress'] = rwcomponent.allowablestress
        objExCor['MinThickReq'] = rwcomponent.minreqthickness
        objExCor['StructuralThickness'] = rwcomponent.structuralthickness
        objExCor['Pressure'] = rwmaterial.designpressure
        objExCor['Diametter'] = rwcomponent.nominaldiameter
        objExCor['shape'] = API_COMPONENT_TYPE_NAME = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # Df_CUI
        objCui = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCui['ComponentNumber'] = ComponentNumber
        objCui['EquipmentNumber'] = EquipmentName
        objCui['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        comptype = models.ComponentType.objects.get(componenttypeid=comp.componenttypeid_id)
        rwexcor = models.RwExtcorTemperature.objects.get(id=proposalID)
        objCui['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCui['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCui['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCui['CUI_PERCENT_2'] = rwexcor.minus8toplus6
        objCui['CUI_PERCENT_3'] = rwexcor.plus6toplus32
        objCui['CUI_PERCENT_4'] = rwexcor.plus32toplus71
        objCui['CUI_PERCENT_5'] = rwexcor.plus71toplus107
        objCui['CUI_PERCENT_6'] = rwexcor.plus107toplus121
        objCui['CUI_PERCENT_7'] = rwexcor.plus121toplus135
        objCui['CUI_PERCENT_8'] = rwexcor.plus135toplus162
        objCui['CUI_PERCENT_9'] = rwexcor.plus162toplus176
        objCui['INSULATION_TYPE'] = rwcoat.externalinsulationtype
        objCui['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCui['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCui['SUPPORT_COATING'] = bool(rwcoat.supportconfignotallowcoatingmaint)
        objCui['INTERFACE_SOIL_WATER'] = bool(rwequipment.interfacesoilwater)
        objCui['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCui['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objCui['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCui['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCui['CUI_INSP_EFF'] = 'E'
        objCui['CUI_INSP_NUM'] = 0
        objCui['APIComponentType'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        objCui['NomalThick'] = rwcomponent.nominalthickness
        objCui['CurrentThick'] = rwcomponent.currentthickness
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        # chua thay dung
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['CR_Confidents_Level'] = rwcomponent.confidencecorrosionrate
        objCui['MINIUM_STRUCTURAL_THICKNESS_GOVERS'] = rwcomponent.minstructuralthickness
        objCui['WeldJointEffciency'] = rwcomponent.weldjointefficiency
        objCui['YieldStrengthDesignTemp'] = rwmaterial.yieldstrength
        objCui['TensileStrengthDesignTemp'] = rwmaterial.tensilestrength
        objCui['AllowableStress'] = rwcomponent.allowablestress
        objCui['MinThickReq'] = rwcomponent.minreqthickness
        objCui['StructuralThickness'] = rwcomponent.structuralthickness
        objCui['Pressure'] = rwmaterial.designpressure
        objCui['Diametter'] = rwcomponent.nominaldiameter
        objCui['ShapeFactor'] = comptype.shapefactor
        objCui['COMPONENT_INSTALL_DATE'] = COMPONENT_INSTALL_DATE
        objCui['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        objCui['shape'] = models.ApiComponentType.objects.get(
            apicomponenttypeid=comp.apicomponenttypeid).apicomponenttypename
        # EXTERNAL CLSCC
        objEXTERN_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objEXTERN_CLSCC['ComponentNumber'] = ComponentNumber
        objEXTERN_CLSCC['EquipmentNumber'] = EquipmentName
        objEXTERN_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objEXTERN_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objEXTERN_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objEXTERN_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objEXTERN_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objEXTERN_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objEXTERN_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objEXTERN_CLSCC['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # CUI_CLSCC
        objCUI_CLSCC = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objCUI_CLSCC['ComponentNumber'] = ComponentNumber
        objCUI_CLSCC['EquipmentNumber'] = EquipmentName
        objCUI_CLSCC['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        rwcoat = models.RwCoating.objects.get(id=proposalID)
        objCUI_CLSCC['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objCUI_CLSCC['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objCUI_CLSCC['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objCUI_CLSCC['EXTERNAL_EVIRONMENT'] = rwequipment.externalenvironment
        objCUI_CLSCC['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objCUI_CLSCC['PIPING_COMPLEXITY'] = rwcomponent.complexityprotrusion
        objCUI_CLSCC['INSULATION_CONDITION'] = rwcoat.insulationcondition
        objCUI_CLSCC['INSULATION_CHLORIDE'] = bool(rwcoat.insulationcontainschloride)
        objCUI_CLSCC['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objCUI_CLSCC['EXTERNAL_INSULATION'] = bool(rwcoat.externalinsulation)

        objCUI_CLSCC['EXTERNAL_EXPOSED_FLUID_MIST'] = bool(rwequipment.materialexposedtoclext)
        objCUI_CLSCC['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objCUI_CLSCC['EXTERN_COAT_QUALITY'] = rwcoat.externalcoatingquality
        # HTHA
        objHTHA = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objHTHA['ComponentNumber'] = ComponentNumber
        objHTHA['EquipmentNumber'] = EquipmentName
        objHTHA['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objHTHA['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objHTHA['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objHTHA['HTHA_PRESSURE'] = rwstream.h2spartialpressure * 0.006895
        objHTHA['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objHTHA['HTHADamageObserved'] = rwcomponent.hthadamage
        objHTHA['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objHTHA['MATERIAL_SUSCEP_HTHA'] = bool(rwmaterial.ishtha)
        objHTHA['HTHA_MATERIAL'] = rwmaterial.hthamaterialcode
        objHTHA['Hydrogen'] = rwstream.hydrogen
        # TEMP_EMBRITTLE
        objTEMP_EMBRITTLE = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objTEMP_EMBRITTLE['ComponentNumber'] = ComponentNumber
        objTEMP_EMBRITTLE['EquipmentNumber'] = EquipmentName
        objTEMP_EMBRITTLE['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objTEMP_EMBRITTLE['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objTEMP_EMBRITTLE['TEMPER_SUSCEP'] = bool(rwmaterial.temper)
        objTEMP_EMBRITTLE['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objTEMP_EMBRITTLE['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objTEMP_EMBRITTLE['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objTEMP_EMBRITTLE['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objTEMP_EMBRITTLE['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        objTEMP_EMBRITTLE['REF_TEMP'] = rwmaterial.referencetemperature
        objTEMP_EMBRITTLE['DELTA_FATT'] = rwcomponent.deltafatt
        objTEMP_EMBRITTLE['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objTEMP_EMBRITTLE['PWHT'] = bool(rwequipment.pwht)
        objTEMP_EMBRITTLE['BRITTLE_THICK'] = rwcomponent.brittlefracturethickness

        objTEMP_EMBRITTLE['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # Df_885
        obj885 = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        obj885['ComponentNumber'] = ComponentNumber
        obj885['EquipmentNumber'] = EquipmentName
        obj885['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        obj885['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        obj885['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        obj885['CHROMIUM_12'] = bool(rwmaterial.chromemoreequal12)
        obj885['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        obj885['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        obj885['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        obj885['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation
        obj885['REF_TEMP'] = rwmaterial.referencetemperature
        obj885['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        obj885['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # dfSigma
        objSigma = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objSigma['ComponentNumber'] = ComponentNumber
        objSigma['EquipmentNumber'] = EquipmentName
        objSigma['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objSigma['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objSigma['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objSigma['MIN_TEM'] = rwstream.minoperatingtemperature
        objSigma['AUSTENITIC_STEEL'] = bool(rwmaterial.austenitic)
        objSigma['MIN_OP_TEMP'] = rwstream.minoperatingtemperature
        objSigma['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature

        objSigma['PRESSSURE_CONTROL'] = bool(rwequipment.pressurisationcontrolled)
        objSigma['MIN_TEMP_PRESSURE'] = rwequipment.minreqtemperaturepressurisation

        objSigma['CRITICAL_TEMP'] = rwstream.criticalexposuretemperature
        objSigma['PERCENT_SIGMA'] = rwmaterial.sigmaphase
        # chua thay su dung MIN_DESIGN_TEMP
        objSigma['MIN_DESIGN_TEMP'] = rwmaterial.mindesigntemperature
        # caustic
        objcaustic = {}
        rwassessment = models.RwAssessment.objects.get(id=proposalID)
        comp = models.ComponentMaster.objects.get(componentid=rwassessment.componentid_id)
        COMPONENT_INSTALL_DATE = models.EquipmentMaster.objects.get(
            equipmentid=comp.equipmentid_id).commissiondate
        ComponentNumber = str(comp.componentnumber)
        EquipmentName = models.EquipmentMaster.objects.get(equipmentid=comp.equipmentid_id).equipmentnumber
        objcaustic['ComponentNumber'] = ComponentNumber
        objcaustic['EquipmentNumber'] = EquipmentName
        objcaustic['Assessment'] = rwassessment.proposalname
        rwequipment = models.RwEquipment.objects.get(id=proposalID)
        rwstream = models.RwStream.objects.get(id=proposalID)
        rwmaterial = models.RwMaterial.objects.get(id=proposalID)
        rwcomponent = models.RwComponent.objects.get(id=proposalID)
        objcaustic['assessmentDate'] = rwassessment.assessmentdate.strftime('%Y-%m-%d')
        objcaustic['CommissionDate'] = COMPONENT_INSTALL_DATE.strftime('%Y-%m-%d')
        objcaustic['CRACK_PRESENT'] = bool(rwcomponent.crackspresent)
        objcaustic['HEAT_TREATMENT'] = rwmaterial.heattreatment
        objcaustic['NaOHConcentration'] = rwstream.naohconcentration
        objcaustic['HEAT_TRACE'] = bool(rwequipment.heattraced)
        objcaustic['STEAM_OUT'] = bool(rwequipment.steamoutwaterflush)
        objcaustic['MAX_OP_TEMP'] = rwstream.maxoperatingtemperature
        objcaustic['CARBON_ALLOY'] = bool(rwmaterial.carbonlowalloy)
        objcaustic['PWHT'] = bool(rwequipment.pwht)
        # AMINE_SOLUTION
        xx = 'Diethanolamine DEA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Diglycolamine DGA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Disopropanolamine DIPA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Methyldiethanolamine MDEA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Monoethanolamine MEA'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'Sulfinol'
        dataAMINE_SOLUTIONX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(obj['AMINE_EXPOSED'], obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       xx, obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'],
                                       obj['PWHT'], rwassessment.assessmentdate, COMPONENT_INSTALL_DATE,
                                       obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_SOLUTIONY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_SOLUTIONY1.append(temp['PoF'])
        dataAMINE_SOLUTIONY2.append(temp['damageTotal'] * dataCoF)
        # AMINE_EXPOSED
        dataAMINE_EXPOSEDX = []
        dataAMINE_EXPOSEDY0 = []
        dataAMINE_EXPOSEDY1 = []
        dataAMINE_EXPOSEDY2 = []
        xx = 'True'
        dataAMINE_EXPOSEDX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(True, obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       obj['AMINE_SOLUTION'], obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'], obj['PWHT'],
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_EXPOSEDY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_EXPOSEDY1.append(temp['PoF'])
        dataAMINE_EXPOSEDY2.append(temp['damageTotal'] * dataCoF)
        #
        xx = 'False'

        dataAMINE_EXPOSEDX.append(xx)
        anime = Detail_DM_CAL.Df_Amine(False, obj['CARBON_ALLOY'], obj['CRACK_PRESENT'],
                                       obj['AMINE_SOLUTION'], obj['MAX_OP_TEMP'], obj['HEAT_TRACE'],
                                       obj['STEAM_OUT'], obj['AMINE_INSP_EFF'], obj['AMINE_INSP_NUM'], obj['PWHT'],
                                       rwassessment.assessmentdate, COMPONENT_INSTALL_DATE, obj['ComponentNumber'])
        amine0 = anime.DF_AMINE_API(0)
        dataPoFTemp['amine'] = amine0
        dataPoFTemp = dataPoF
        dataAMINE_EXPOSEDY0.append(amine0)
        temp = ReCalculate.calculatePoF(proposalID, dataPoFTemp)
        dataAMINE_EXPOSEDY1.append(temp['PoF'])
        dataAMINE_EXPOSEDY2.append(temp['damageTotal'] * dataCoF)
        res_obj={}
        res_obj['dataNominalThicknessX']=dataNominalThicknessX
        res_obj['dataNominalThicknessY0']=dataNominalThicknessY0
        res_obj['dataNominalThicknessY1']=dataNominalThicknessY1
        res_obj['dataNominalThicknessY2']=dataNominalThicknessY2
        res_obj['dataCurentThicknessX']= dataCurentThicknessX
        res_obj['dataCurentThicknessY0']= dataCurentThicknessY0
        res_obj['dataCurentThicknessY1']= dataCurentThicknessY1
        res_obj['dataCurentThicknessY2']= dataCurentThicknessY2
        res_obj['dataCorrosionRateX']= dataCorrosionRateX
        res_obj['dataCorrosionRateY0']= dataCorrosionRateY0
        res_obj['dataCorrosionRateY1']= dataCorrosionRateY1
        res_obj['dataCorrosionRateY2']= dataCorrosionRateY2
        res_obj['dataMinimunRequiredThicknessX']= dataMinimunRequiredThicknessX
        res_obj['dataMinimunRequiredThicknessY0']= dataMinimunRequiredThicknessY0
        res_obj['dataMinimunRequiredThicknessY1']= dataMinimunRequiredThicknessY1
        res_obj['dataMinimunRequiredThicknessY2']= dataMinimunRequiredThicknessY2
        res_obj['dataCO3X'] = dataCO3X
        res_obj['dataCO3Y0'] = dataCO3Y0
        res_obj['dataCO3Y1'] = dataCO3Y1
        res_obj['dataCO3Y2'] = dataCO3Y2
        res_obj['dataphX'] = dataphX
        res_obj['dataphY0'] = dataphY0
        res_obj['dataphY1'] = dataphY1
        res_obj['dataphY2'] = dataphY2

        res_obj['dataMAX_OP_TEMPX'] = dataMAX_OP_TEMPX
        res_obj['dataMAX_OP_TEMPY0'] = dataMAX_OP_TEMPY0
        res_obj['dataMAX_OP_TEMPY1'] = dataMAX_OP_TEMPY1
        res_obj['dataMAX_OP_TEMPY2'] = dataMAX_OP_TEMPY2
        res_obj['dataNaOHConcentrationX'] = dataNaOHConcentrationX
        res_obj['dataNaOHConcentrationY0'] = dataNaOHConcentrationY0
        res_obj['dataNaOHConcentrationY1'] = dataNaOHConcentrationY1
        res_obj['dataNaOHConcentrationY2'] = dataNaOHConcentrationY2
        res_obj['dataCRACK_PRESENTX'] = dataCRACK_PRESENTX
        res_obj['dataCRACK_PRESENTY0'] = dataCRACK_PRESENTY0
        res_obj['dataCRACK_PRESENTY1'] = dataCRACK_PRESENTY1
        res_obj['dataCRACK_PRESENTY2'] = dataCRACK_PRESENTY2
        res_obj['dataHEAT_TRACEX'] = dataHEAT_TRACEX
        res_obj['dataHEAT_TRACEY0'] = dataHEAT_TRACEY0
        res_obj['dataHEAT_TRACEY1'] = dataHEAT_TRACEY1
        res_obj['dataHEAT_TRACEY2'] = dataHEAT_TRACEY2

        res_obj['dataAMINE_SOLUTIONX'] = dataAMINE_SOLUTIONX
        res_obj['dataAMINE_SOLUTIONY0'] = dataAMINE_SOLUTIONY0
        res_obj['dataAMINE_SOLUTIONY1'] = dataAMINE_SOLUTIONY1
        res_obj['dataAMINE_SOLUTIONY2'] = dataAMINE_SOLUTIONY2
        res_obj['dataAMINE_EXPOSEDX'] = dataAMINE_SOLUTIONX
        res_obj['dataAMINE_EXPOSEDY0'] = dataAMINE_SOLUTIONY0
        res_obj['dataAMINE_EXPOSEDY1'] = dataAMINE_SOLUTIONY1
        res_obj['dataAMINE_EXPOSEDY2'] = dataAMINE_SOLUTIONY2

        return res_obj
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
# Financial
def FinancialNomalCoF(proposalID):
    rwAss = models.RwAssessment.objects.get(id=proposalID)
    component = models.ComponentMaster.objects.get(componentid=rwAss.componentid_id)
    inputCa = models.RwInputCaLevel1.objects.get(id=proposalID)
    rwstream = models.RwStream.objects.get(id=proposalID)
    material = models.RwMaterial.objects.get(id=proposalID)
    rwinputca = models.RwInputCaLevel1.objects.get(id=proposalID)
    model_fluid=inputCa.api_fluid
    toxic_fluid = inputCa.toxic_fluid
    toxic_fluid_percentage=inputCa.toxic_percent
    api_com_type=models.ApiComponentType.objects.get(
                apicomponenttypeid=component.apicomponenttypeid).apicomponenttypename
    phase_fluid_storage=rwstream.storagephase

    MATERIAL_COST=material.costfactor
    max_operating_pressure=rwstream.maxoperatingpressure * 1000
    caflammable = CA_Flammable.CA_Flammable(model_fluid, phase_fluid_storage,
                                            inputCa.mitigation_system, proposalID,
                                            rwstream.maxoperatingtemperature,
                                            api_com_type, toxic_fluid_percentage,
                                            toxic_fluid)
    catoxic = ToxicConsequenceArea.CA_Toxic(proposalID, inputCa.toxic_fluid, caflammable.ReleasePhase(),
                                            toxic_fluid_percentage, api_com_type,
                                            model_fluid, max_operating_pressure)
    CA_cmd= max(caflammable.CA_Flam_Cmd(), caflammable.CA_Flam_Cmd_toxic())
    CA_inj=max(caflammable.CA_Flam_inj(), caflammable.CA_Flam_inj_toxic(), catoxic.CA_toxic_inj(),
                                 catoxic.CA_toxic_inj2(), catoxic.NoneCA_leck())
    process_unit = rwinputca.process_unit
    outage_multiplier = rwinputca.outage_multiplier
    production_cost = rwinputca.production_cost
    personal_density = rwinputca.personal_density
    injure_cost = rwinputca.injure_cost
    evironment_cost = rwinputca.evironment_cost

    POF = models.RwFullPof.objects.get(id=proposalID).pofap1
    #  process unit change
    data_PROCESS_UNIT_X = []
    data_PROCESS_UNIT_Y0=[]
    data_PROCESS_UNIT_Y1=[]
    for i in range(20, 0, -2):
        if process_unit-i>0:
            data_PROCESS_UNIT_X.append(process_unit-i)
            fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                        toxic_fluid_percentage, api_com_type,
                                        MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                        rwinputca.mitigation_system,
                                        rwstream.maxoperatingtemperature,max_operating_pressure,
                                         process_unit-i,outage_multiplier,production_cost,
                                         personal_density,injure_cost,evironment_cost)
            if fullcof.FC_total()==0:
                financial_CoF=100000000

            else:
                financial_CoF=(roundData.roundFC(fullcof.FC_total()))
            data_PROCESS_UNIT_Y0.append(financial_CoF)
            data_PROCESS_UNIT_Y1.append(financial_CoF*POF)
    for i in range(0, 20, 2):
        data_PROCESS_UNIT_X.append(process_unit+i)
        fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                             toxic_fluid_percentage, api_com_type,
                                             MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                             rwinputca.mitigation_system,
                                             rwstream.maxoperatingtemperature,max_operating_pressure,
                                             process_unit + i, outage_multiplier, production_cost,
                                             personal_density, injure_cost, evironment_cost)
        if fullcof.FC_total() == 0:
            financial_CoF = 100000000

        else:
            financial_CoF = (roundData.roundFC(fullcof.FC_total()))
        data_PROCESS_UNIT_Y0.append(financial_CoF)
        data_PROCESS_UNIT_Y1.append(financial_CoF * POF)
    # equipment outage multiplier change
    data_OUTAGE_MULTIPLIER_X = []
    data_OUTAGE_MULTIPLIER_Y0 = []
    data_OUTAGE_MULTIPLIER_Y1 = []
    for i in range(20, 0, -2):
        if outage_multiplier - i > 0:
            data_OUTAGE_MULTIPLIER_X.append(outage_multiplier - i)
            fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                                 toxic_fluid_percentage, api_com_type,
                                                 MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                 rwinputca.mitigation_system,
                                                 rwstream.maxoperatingtemperature, max_operating_pressure,
                                                 process_unit, outage_multiplier-i, production_cost,
                                                 personal_density, injure_cost, evironment_cost)
            if fullcof.FC_total() == 0:
                financial_CoF = 100000000

            else:
                financial_CoF = (roundData.roundFC(fullcof.FC_total()))
            data_OUTAGE_MULTIPLIER_Y0.append(financial_CoF)
            data_OUTAGE_MULTIPLIER_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_OUTAGE_MULTIPLIER_X.append(outage_multiplier + i)
        fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                             toxic_fluid_percentage, api_com_type,
                                             MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                             rwinputca.mitigation_system,
                                             rwstream.maxoperatingtemperature, max_operating_pressure,
                                             process_unit, outage_multiplier+i, production_cost,
                                             personal_density, injure_cost, evironment_cost)
        if fullcof.FC_total() == 0:
            financial_CoF = 100000000

        else:
            financial_CoF = (roundData.roundFC(fullcof.FC_total()))
        data_OUTAGE_MULTIPLIER_Y0.append(financial_CoF)
        data_OUTAGE_MULTIPLIER_Y1.append(financial_CoF * POF)
    # loss of prodution cost change
    data_PRODUCTION_COST_X = []
    data_PRODUCTION_COST_Y0 = []
    data_PRODUCTION_COST_Y1 = []
    for i in range(20, 0, -2):
        if production_cost - i > 0:
            data_PRODUCTION_COST_X.append(production_cost - i)
            fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                                 toxic_fluid_percentage, api_com_type,
                                                 MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                 rwinputca.mitigation_system,
                                                 rwstream.maxoperatingtemperature, max_operating_pressure,
                                                 process_unit, outage_multiplier, production_cost-i,
                                                 personal_density, injure_cost, evironment_cost)
            if fullcof.FC_total() == 0:
                financial_CoF = 100000000

            else:
                financial_CoF = (roundData.roundFC(fullcof.FC_total()))
            data_PRODUCTION_COST_Y0.append(financial_CoF)
            data_PRODUCTION_COST_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_PRODUCTION_COST_X.append(production_cost + i)
        fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                             toxic_fluid_percentage, api_com_type,
                                             MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                             rwinputca.mitigation_system,
                                             rwstream.maxoperatingtemperature, max_operating_pressure,
                                             process_unit, outage_multiplier, production_cost+i,
                                             personal_density, injure_cost, evironment_cost)
        if fullcof.FC_total() == 0:
            financial_CoF = 100000000

        else:
            financial_CoF = (roundData.roundFC(fullcof.FC_total()))
        data_PRODUCTION_COST_Y0.append(financial_CoF)
        data_PRODUCTION_COST_Y1.append(financial_CoF * POF)
    # the unit population density change
    data_PERONAL_DENSITY_X = []
    data_PERONAL_DENSITY_Y0 = []
    data_PERONAL_DENSITY_Y1 = []
    for i in range(20, 0, -2):
        if personal_density - i > 0:
            data_PERONAL_DENSITY_X.append(personal_density - i)
            fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                                 toxic_fluid_percentage, api_com_type,
                                                 MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                 rwinputca.mitigation_system,
                                                 rwstream.maxoperatingtemperature, max_operating_pressure,
                                                 process_unit, outage_multiplier , production_cost,
                                                 personal_density-i, injure_cost, evironment_cost)
            if fullcof.FC_total() == 0:
                financial_CoF = 100000000

            else:
                financial_CoF = (roundData.roundFC(fullcof.FC_total()))
            data_PERONAL_DENSITY_Y0.append(financial_CoF)
            data_PERONAL_DENSITY_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_PERONAL_DENSITY_X.append(personal_density + i)
        fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                             toxic_fluid_percentage, api_com_type,
                                             MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                             rwinputca.mitigation_system,
                                             rwstream.maxoperatingtemperature, max_operating_pressure,
                                             process_unit, outage_multiplier, production_cost,
                                             personal_density+i, injure_cost, evironment_cost)
        if fullcof.FC_total() == 0:
            financial_CoF = 100000000

        else:
            financial_CoF = (roundData.roundFC(fullcof.FC_total()))
        data_PERONAL_DENSITY_Y0.append(financial_CoF)
        data_PERONAL_DENSITY_Y1.append(financial_CoF * POF)
    # the cost associated change
    data_INJURE_COST_X = []
    data_INJURE_COST_Y0 = []
    data_INJURE_COST_Y1 = []
    for i in range(20, 0, -2):
        if injure_cost - i > 0:
            data_INJURE_COST_X.append(injure_cost - i)
            fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                                 toxic_fluid_percentage, api_com_type,
                                                 MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                 rwinputca.mitigation_system,
                                                 rwstream.maxoperatingtemperature, max_operating_pressure,
                                                 process_unit, outage_multiplier, production_cost,
                                                 personal_density, injure_cost-i, evironment_cost)
            if fullcof.FC_total() == 0:
                financial_CoF = 100000000

            else:
                financial_CoF = (roundData.roundFC(fullcof.FC_total()))
            data_INJURE_COST_Y0.append(financial_CoF)
            data_INJURE_COST_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_INJURE_COST_X.append(injure_cost + i)
        fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                             toxic_fluid_percentage, api_com_type,
                                             MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                             rwinputca.mitigation_system,
                                             rwstream.maxoperatingtemperature, max_operating_pressure,
                                             process_unit, outage_multiplier, production_cost,
                                             personal_density, injure_cost+i, evironment_cost)
        if fullcof.FC_total() == 0:
            financial_CoF = 100000000

        else:
            financial_CoF = (roundData.roundFC(fullcof.FC_total()))
        data_INJURE_COST_Y0.append(financial_CoF)
        data_INJURE_COST_Y1.append(financial_CoF * POF)
    # enviromental clean up change
    data_EVIRONMENT_COST_X = []
    data_EVIRONMENT_COST_Y0 = []
    data_EVIRONMENT_COST_Y1 = []
    for i in range(20, 0, -2):
        if evironment_cost - i > 0:
            data_EVIRONMENT_COST_X.append(evironment_cost - i)
            fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                                 toxic_fluid_percentage, api_com_type,
                                                 MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                                 rwinputca.mitigation_system,
                                                 rwstream.maxoperatingtemperature, max_operating_pressure,
                                                 process_unit, outage_multiplier, production_cost,
                                                 personal_density, injure_cost, evironment_cost-i)
            if fullcof.FC_total() == 0:
                financial_CoF = 100000000

            else:
                financial_CoF = (roundData.roundFC(fullcof.FC_total()))
            data_EVIRONMENT_COST_Y0.append(financial_CoF)
            data_EVIRONMENT_COST_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_EVIRONMENT_COST_X.append(evironment_cost + i)
        fullcof = mitigationCoF.FinancialNomalCOF(proposalID, model_fluid, toxic_fluid,
                                             toxic_fluid_percentage, api_com_type,
                                             MATERIAL_COST, CA_cmd, CA_inj, phase_fluid_storage,
                                             rwinputca.mitigation_system,
                                             rwstream.maxoperatingtemperature, max_operating_pressure,
                                             process_unit, outage_multiplier, production_cost,
                                             personal_density, injure_cost , evironment_cost+i)
        if fullcof.FC_total() == 0:
            financial_CoF = 100000000

        else:
            financial_CoF = (roundData.roundFC(fullcof.FC_total()))
        data_EVIRONMENT_COST_Y0.append(financial_CoF)
        data_EVIRONMENT_COST_Y1.append(financial_CoF * POF)
    obj_res = {}
    obj_res['data_PROCESS_UNIT_X'] = data_PROCESS_UNIT_X
    obj_res['data_PROCESS_UNIT_Y0'] = data_PROCESS_UNIT_Y0
    obj_res['data_PROCESS_UNIT_Y1'] = data_PROCESS_UNIT_Y1
    obj_res['data_OUTAGE_MULTIPLIER_X'] = data_OUTAGE_MULTIPLIER_X
    obj_res['data_OUTAGE_MULTIPLIER_Y0'] = data_OUTAGE_MULTIPLIER_Y0
    obj_res['data_OUTAGE_MULTIPLIER_Y1'] = data_OUTAGE_MULTIPLIER_Y1
    obj_res['data_PRODUCTION_COST_X'] = data_PRODUCTION_COST_X
    obj_res['data_PRODUCTION_COST_Y0'] = data_PRODUCTION_COST_Y0
    obj_res['data_PRODUCTION_COST_Y1'] = data_PRODUCTION_COST_Y1
    obj_res['data_PERONAL_DENSITY_X'] = data_PERONAL_DENSITY_X
    obj_res['data_PERONAL_DENSITY_Y0'] = data_PERONAL_DENSITY_Y0
    obj_res['data_PERONAL_DENSITY_Y1'] = data_PERONAL_DENSITY_Y1
    obj_res['data_INJURE_COST_X'] = data_INJURE_COST_X
    obj_res['data_INJURE_COST_Y0'] = data_INJURE_COST_Y0
    obj_res['data_INJURE_COST_Y1'] = data_INJURE_COST_Y1
    obj_res['data_EVIRONMENT_COST_X'] = data_EVIRONMENT_COST_X
    obj_res['data_EVIRONMENT_COST_Y0'] = data_EVIRONMENT_COST_Y0
    obj_res['data_EVIRONMENT_COST_Y1'] = data_EVIRONMENT_COST_Y1

    return obj_res
def FinancialShellCoF(proposalID):
    rwFullCofTank = models.RWFullCofTank.objects.filter(id=proposalID)
    if rwFullCofTank.count() == 0:
        EQUIP_COST = 0
        EQUIP_OUTAGE_MULTIPLIER = 0
        PROD_COST = 0
        POP_DENS = 0
        INJ_COST = 0
    else:
        rwFullCofTank = models.RWFullCofTank.objects.get(id=proposalID)
        EQUIP_COST = rwFullCofTank.equipcost
        EQUIP_OUTAGE_MULTIPLIER = rwFullCofTank.equipoutagemultiplier
        PROD_COST = rwFullCofTank.prodcost
        POP_DENS = rwFullCofTank.popdens
        INJ_COST = rwFullCofTank.injcost
    POF = models.RwFullPof.objects.get(id=proposalID).pofap1

    #  process unit change
    data_PROCESS_UNIT_X = []
    data_PROCESS_UNIT_Y0 = []
    data_PROCESS_UNIT_Y1 = []
    for i in range(20, 0, -2):
        if EQUIP_COST - i > 0:
            data_PROCESS_UNIT_X.append(EQUIP_COST - i)
            financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST-i, EQUIP_OUTAGE_MULTIPLIER, PROD_COST, POP_DENS, INJ_COST)
            data_PROCESS_UNIT_Y0.append(financial_CoF)

            data_PROCESS_UNIT_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_PROCESS_UNIT_X.append(EQUIP_COST+i)
        financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST+i, EQUIP_OUTAGE_MULTIPLIER, PROD_COST,
                                                        POP_DENS, INJ_COST)
        data_PROCESS_UNIT_Y0.append(financial_CoF)
        data_PROCESS_UNIT_Y1.append(financial_CoF * POF)
    # equipment outage multiplier change
    data_OUTAGE_MULTIPLIER_X = []
    data_OUTAGE_MULTIPLIER_Y0 = []
    data_OUTAGE_MULTIPLIER_Y1 = []
    for i in range(20, 0, -2):
        if EQUIP_OUTAGE_MULTIPLIER - i > 0:
            data_OUTAGE_MULTIPLIER_X.append(EQUIP_OUTAGE_MULTIPLIER - i)
            financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER-i, PROD_COST, POP_DENS, INJ_COST)

            data_OUTAGE_MULTIPLIER_Y0.append(financial_CoF)
            data_OUTAGE_MULTIPLIER_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_OUTAGE_MULTIPLIER_X.append(EQUIP_OUTAGE_MULTIPLIER + i)
        financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER + i, PROD_COST,
                                                        POP_DENS, INJ_COST)
        data_OUTAGE_MULTIPLIER_Y0.append(financial_CoF)
        data_OUTAGE_MULTIPLIER_Y1.append(financial_CoF * POF)
    # loss of prodution cost change
    data_PRODUCTION_COST_X = []
    data_PRODUCTION_COST_Y0 = []
    data_PRODUCTION_COST_Y1 = []
    for i in range(20, 0, -2):
        if PROD_COST - i > 0:
            data_PRODUCTION_COST_X.append(PROD_COST - i)
            financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER, PROD_COST-i, POP_DENS, INJ_COST)
            data_PRODUCTION_COST_Y0.append(financial_CoF)
            data_PRODUCTION_COST_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_PRODUCTION_COST_X.append(PROD_COST + i)
        financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER, PROD_COST + i,
                                                        POP_DENS, INJ_COST)
        data_PRODUCTION_COST_Y0.append(financial_CoF)
        data_PRODUCTION_COST_Y1.append(financial_CoF * POF)
    # the unit population density change
    data_PERONAL_DENSITY_X = []
    data_PERONAL_DENSITY_Y0 = []
    data_PERONAL_DENSITY_Y1 = []
    for i in range(20, 0, -2):
        if POP_DENS - i > 0:
            data_PERONAL_DENSITY_X.append(POP_DENS - i)
            financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER, PROD_COST, POP_DENS-i, INJ_COST)
            data_PERONAL_DENSITY_Y0.append(financial_CoF)
            data_PERONAL_DENSITY_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_PERONAL_DENSITY_X.append(POP_DENS + i)
        financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER, PROD_COST,
                                                        POP_DENS+i, INJ_COST)
        data_PERONAL_DENSITY_Y0.append(financial_CoF)
        data_PERONAL_DENSITY_Y1.append(financial_CoF * POF)
    # the cost associated change
    data_INJURE_COST_X = []
    data_INJURE_COST_Y0 = []
    data_INJURE_COST_Y1 = []
    for i in range(20, 0, -2):
        if INJ_COST - i > 0:
            data_INJURE_COST_X.append(INJ_COST - i)
            financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER, PROD_COST, POP_DENS, INJ_COST-i)

            data_INJURE_COST_Y0.append(financial_CoF)
            data_INJURE_COST_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_INJURE_COST_X.append(INJ_COST + i)
        financial_CoF = mitigationCoF.FinancialShellCOF(proposalID, EQUIP_COST, EQUIP_OUTAGE_MULTIPLIER, PROD_COST,
                                                        POP_DENS, INJ_COST + i)


        data_INJURE_COST_Y0.append(financial_CoF)
        data_INJURE_COST_Y1.append(financial_CoF * POF)
    obj_res = {}
    obj_res['data_PROCESS_UNIT_X'] = data_PROCESS_UNIT_X
    obj_res['data_PROCESS_UNIT_Y0'] = data_PROCESS_UNIT_Y0
    obj_res['data_PROCESS_UNIT_Y1'] = data_PROCESS_UNIT_Y1
    obj_res['data_OUTAGE_MULTIPLIER_X'] = data_OUTAGE_MULTIPLIER_X
    obj_res['data_OUTAGE_MULTIPLIER_Y0'] = data_OUTAGE_MULTIPLIER_Y0
    obj_res['data_OUTAGE_MULTIPLIER_Y1'] = data_OUTAGE_MULTIPLIER_Y1
    obj_res['data_PRODUCTION_COST_X'] = data_PRODUCTION_COST_X
    obj_res['data_PRODUCTION_COST_Y0'] = data_PRODUCTION_COST_Y0
    obj_res['data_PRODUCTION_COST_Y1'] = data_PRODUCTION_COST_Y1
    obj_res['data_PERONAL_DENSITY_X'] = data_PERONAL_DENSITY_X
    obj_res['data_PERONAL_DENSITY_Y0'] = data_PERONAL_DENSITY_Y0
    obj_res['data_PERONAL_DENSITY_Y1'] = data_PERONAL_DENSITY_Y1
    obj_res['data_INJURE_COST_X'] = data_INJURE_COST_X
    obj_res['data_INJURE_COST_Y0'] = data_INJURE_COST_Y0
    obj_res['data_INJURE_COST_Y1'] = data_INJURE_COST_Y1
    return obj_res
def FinancialTankBottomCoF(proposalID):
    POF = models.RwFullPof.objects.get(id=proposalID).pofap1
    rwinputca = models.RwInputCaTank.objects.get(id=proposalID)
    rwcomponent = models.RwComponent.objects.get(id=proposalID)
    #  process unit change
    data_COST_LOSS_X = []
    data_COST_LOSS_Y0 = []
    data_COST_LOSS_Y1 = []
    data_Nominal_Diameter_X = []
    data_Nominal_Diameter_Y0 = []
    data_Nominal_Diameter_Y1 = []
    productioncost = rwinputca.productioncost
    TANK_DIAMETER = rwcomponent.nominaldiameter
    # productioncost change
    for i in range(20, 0, -2):
        if productioncost - i > 0:
            data_COST_LOSS_X.append(productioncost - i)
            financial_CoF = mitigationCoF.FinancialTankBottomCoF(proposalID,productioncost - i,TANK_DIAMETER)
            data_COST_LOSS_Y0.append(financial_CoF)
            data_COST_LOSS_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_COST_LOSS_X.append(productioncost + i)
        financial_CoF = mitigationCoF.FinancialTankBottomCoF(proposalID, productioncost + i,TANK_DIAMETER)
        data_COST_LOSS_Y0.append(financial_CoF)
        data_COST_LOSS_Y1.append(financial_CoF * POF)
    # TANK_DIAMETER change
    for i in range(20, 0, -2):
        if TANK_DIAMETER - i > 0:
            data_Nominal_Diameter_X.append(TANK_DIAMETER - i)
            financial_CoF = mitigationCoF.FinancialTankBottomCoF(proposalID,productioncost,TANK_DIAMETER-i)
            data_Nominal_Diameter_Y0.append(financial_CoF)
            data_Nominal_Diameter_Y1.append(financial_CoF * POF)
    for i in range(0, 20, 2):
        data_Nominal_Diameter_X.append(TANK_DIAMETER + i)
        financial_CoF = mitigationCoF.FinancialTankBottomCoF(proposalID, productioncost,TANK_DIAMETER+i)
        data_Nominal_Diameter_Y0.append(financial_CoF)
        data_Nominal_Diameter_Y1.append(financial_CoF * POF)
    obj_res = {}
    obj_res['data_COST_LOSS_X'] = data_COST_LOSS_X
    obj_res['data_COST_LOSS_Y0'] = data_COST_LOSS_Y0
    obj_res['data_COST_LOSS_Y1'] = data_COST_LOSS_Y1
    obj_res['data_Nominal_Diameter_X'] = data_Nominal_Diameter_X
    obj_res['data_Nominal_Diameter_Y0'] = data_Nominal_Diameter_Y0
    obj_res['data_Nominal_Diameter_Y1'] = data_Nominal_Diameter_Y1
    return obj_res
# def Save_DB_All(proposalID):
#     obj=AllDamageFactor(proposalID)
#     if len(obj['dataNominalThicknessX'])<20:
#         n=20-len(obj['dataNominalThicknessX'])
#         for x in range(n):
#             obj['dataNominalThicknessX'].append(-1)
#     models.mitigationNominalThickness(id=proposalID,x0=obj['dataNominalThicknessX'][0],x1=obj['dataNominalThicknessX'][1],x=obj['dataNominalThicknessX'][0]
#                                       , x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0]
#                                       , x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0]
#                                       , x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0],
#     , x0 = obj['dataNominalThicknessX'][0],x0=obj['dataNominalThicknessX'][0])




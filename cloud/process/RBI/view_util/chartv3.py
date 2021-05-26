from cloud import models
from cloud.process.WebUI import date2Str


def ChartV3(proposalID, rwAssessment): 
    proposalname = rwAssessment.proposalname 
    check = 0
    dataPresent = []
    Target = []
    dataOld = []
    dataLabel = []
    rwFullpof = models.RwFullPof.objects.get(id=proposalID)
    rwFullcof = models.RwFullFcof.objects.get(id=proposalID)
    risk = rwFullpof.pofap1 * rwFullcof.fcofvalue
    chart = models.RwDataChart.objects.get(id=proposalID)
    print('id'+str(proposalID))
    component = models.ComponentMaster.objects.get(componentid=rwAssessment.componentid_id)

    risktarget=component.risktarget
    equip = models.EquipmentMaster.objects.get(equipmentid=component.equipmentid_id)
    if component.componenttypeid_id == 12 or component.componenttypeid_id == 13 or component.componenttypeid_id == 14 or component.componenttypeid_id == 15:
        isTank = 1
    else:
        isTank = 0
    if component.componenttypeid_id == 13:
        isShell = 1
    else:
        isShell = 0
    print("có 1 proposal")
    assessmentDate = rwAssessment.assessmentdate
    # if risk < chart.riskage1:
    dataChart = [risk, chart.riskage1, chart.riskage2, chart.riskage3, chart.riskage4, chart.riskage5,
                    chart.riskage6,chart.riskage7, chart.riskage8, chart.riskage9, chart.riskage10,
                    chart.riskage11,chart.riskage12, chart.riskage13, chart.riskage14, chart.riskage15,
                chart.riskage16,chart.riskage17,chart.riskage18,chart.riskage19,chart.riskage20,
                    chart.riskage21,chart.riskage22,chart.riskage23,chart.riskage24,chart.riskage25,chart.riskage26,chart.riskage27]
    print('datachart')
    print(dataChart)
    # dataLabel = [date2Str.date2strCC(assessmentDate)]
    listTime=[]
    listPeriod=[]
    time=[]
    periodtime=-12
    year=0
    print(chart.risktarget)
    while (year<17.0):
        dataLabel.append(date2Str.date2strCC(date2Str.dateFuture(assessmentDate, year)))
        periodtime=periodtime+12
        listPeriod.append(periodtime)
        time.append(date2Str.date2strCC(date2Str.dateFuture(assessmentDate, year)))
        if year==int(chart.risktarget):
            day = 1
            month=1
            while month<12:
                dataLabel.append(date2Str.date2strCC(date2Str.dateFuturebyMonth(assessmentDate, year,month, 0)))
                month+=1
                time.append(date2Str.date2strCC(date2Str.dateFuturebyMonth(assessmentDate, year,month, 0)))
                periodtime =periodtime+ 1
                listPeriod.append(periodtime)
        year += 1
    # print(len(dataLabel))
    # print(len(dataChart))
    dataChartPoF=models.RwDataChartPoF.objects.get(id=proposalID)
    dataChartDMFactor=models.RwDataDMFactor.objects.get(id=proposalID)
    listPoF=[models.RwFullPof.objects.get(id=proposalID).pofap1,dataChartPoF.riskage1, dataChartPoF.riskage2, dataChartPoF.riskage3, dataChartPoF.riskage4, dataChartPoF.riskage5,
                dataChartPoF.riskage6,dataChartPoF.riskage7, dataChartPoF.riskage8, dataChartPoF.riskage9, dataChartPoF.riskage10,
                dataChartPoF.riskage11,dataChartPoF.riskage12, dataChartPoF.riskage13, dataChartPoF.riskage14, dataChartPoF.riskage15,
                dataChartPoF.riskage16,dataChartPoF.riskage17,dataChartPoF.riskage18,dataChartPoF.riskage19,dataChartPoF.riskage20,
                dataChartPoF.riskage21,dataChartPoF.riskage22,dataChartPoF.riskage23,dataChartPoF.riskage24,dataChartPoF.riskage25,
                dataChartPoF.riskage26,dataChartPoF.riskage27]
    listDMFactor = [models.RwFullPof.objects.get(id=proposalID).totaldfap1, dataChartDMFactor.riskage1, dataChartDMFactor.riskage2,
                    dataChartDMFactor.riskage3, dataChartDMFactor.riskage4, dataChartDMFactor.riskage5,
                    dataChartDMFactor.riskage6, dataChartDMFactor.riskage7, dataChartDMFactor.riskage8, dataChartDMFactor.riskage9,
                    dataChartDMFactor.riskage10,
                    dataChartDMFactor.riskage11, dataChartDMFactor.riskage12, dataChartDMFactor.riskage13, dataChartDMFactor.riskage14,
                    dataChartDMFactor.riskage15,
                    dataChartDMFactor.riskage16, dataChartDMFactor.riskage17, dataChartDMFactor.riskage18, dataChartDMFactor.riskage19,
                    dataChartDMFactor.riskage20,
                    dataChartDMFactor.riskage21, dataChartDMFactor.riskage22, dataChartDMFactor.riskage23, dataChartDMFactor.riskage24,
                    dataChartDMFactor.riskage25,
                    dataChartDMFactor.riskage26, dataChartDMFactor.riskage27]

    for a in range(0, 28):
        obj={}
        obj['x'] = time[a]
        obj['y'] = dataChart[a]
        obj['index'] = a + 1
        obj['pof'] = listPoF[a]
        obj['dm'] = listDMFactor[a]
        obj['period']=listPeriod[a]
        listTime.append(obj)
    for a in range(0, 28):
        obj={}
        obj['x'] = dataLabel[a]
        obj['y'] = dataChart[a]
        dataPresent.append(obj)
    print('dataPresent1')
    print(dataPresent) 
    print('risktarget')
    print(risktarget)
    dataTarget = [risktarget,risktarget,risktarget,risktarget,risktarget,risktarget,risktarget,
                    risktarget,risktarget,risktarget,risktarget,risktarget,risktarget,risktarget,
                    risktarget,risktarget,risktarget,risktarget,risktarget,risktarget,risktarget,
                    risktarget,risktarget,risktarget,risktarget,risktarget]

    for a in range(0, len(dataLabel)):
        obj={}
        obj['x'] = dataPresent[a]['x']
        obj['y'] = risktarget
        obj['index'] = a + 1
        Target.append(obj)
    # print(Target)
    return isTank, isShell, rwAssessment.componentid_id, dataLabel,check, dataOld, dataPresent, Target, proposalname, listTime
    
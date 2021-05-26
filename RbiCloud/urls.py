"""RbiCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cloud import views
from django.conf.urls import handler404
from django.conf.urls import handler500
import django.views.static
from RbiCloud import settings

urlpatterns = [
    # path('static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    ########################## Base ################################
    path('admin/', admin.site.urls),
    path('', views.signin, name='home'),
    path('Password/',views.Password,name='password'),
    path('Reset_Password/<int:userid>/',views.RsPassword,name='reset'),
    path('basecitizen/',views.Base_citizen,name='basecitizen'),
    path('basemanagement/', views.base_manager, name= 'basemanager'),
    path('basebusiness/',views.base_business,name='basebusiness'),
    path('business/', views.business_home, name='business'),
    path('equipment/', views.base_equipment, name='equipment'),
    path('component/', views.base_component, name='componentmanagement/'),
    path('proposal/', views.base_proposal, name='prosal'),
    path('risksummary/', views.base_risksummary, name='risk'),
    path('designcode/', views.base_designcode, name='designcode'),
    path('manufacture/', views.base_manufacture, name= 'manufacture'),
    path('basereport/', views.base_report,name='basereport'), #Dat sua
    ########################## Facility UI################################
    path('damage/thining/<int:proposalID>/', views.ShowThining, name='thining'),
    path('damage/lining/<int:proposalID>/', views.showLining, name='lining'),
    path('damage/chooseThining/<int:proposalID>/', views.chooseThining, name='choseThining'),
    path('damage/chooseGoverningBrittle/<int:proposalID>/', views.chooseGoverningBrittle,
         name='chooseGoverningBrittle'),
    path('damage/chooseGoverningExternal/<int:proposalID>/', views.chooseGoverningExternal,
         name='chooseGoverningExternal'),
    path('damage/extCLSCC/<int:proposalID>/', views.ShowextCLSCC, name='extCLSCC'),
    path('damage/cuiCLSCC/<int:proposalID>/', views.ShowCUI_CLSCC, name='CUI_CLSCC'),
    path('damage/EXTERNAL_CORROSION/<int:proposalID>/', views.ShowEXTERNAL_CORROSION, name='EXTERNAL_CORROSION'),
    path('damage/CUIF/<int:proposalID>/', views.ShowCUIF, name='CUIF'),
    path('damage/HTHA/<int:proposalID>/', views.ShowHTHA, name='HTHA'),
    path('damage/BRITTLE/<int:proposalID>/', views.ShowBRITTLE, name='BRITTLE'),
    path('damage/TEMP_EMBRITTLE/<int:proposalID>/', views.ShowTEMP_EMBRITTLE, name='TEMP_EMBRITTLE'),
    path('damage/885/<int:proposalID>/', views.Show885, name='885'),
    path('damage/SIGMA/<int:proposalID>/', views.ShowSIGMA, name='SIGMA'),
    path('damage/PIPE/<int:proposalID>/', views.ShowPIPE, name='PIPE'),
    path('damage/anime/<int:proposalID>/<int:const>/', views.showAnime, name='anime'),
    path('damage/alkaline/<int:proposalID>/<int:const>/', views.showAlkaline, name='alkaline'),
    path('damage/caustic/<int:proposalID>/<int:const>/', views.showCaustic, name='caustic'),
    path('damage/sulphide/<int:proposalID>/<int:const>/', views.showSulphide, name='sulphide'),
    path('damage/hicsohich2s/<int:proposalID>/<int:const>/', views.showHicsohicH2s, name='hicsohich2s'),
    path('damage/PASCC/<int:proposalID>/<int:const>/', views.showPASCC, name='PASCC'),
    path('damage/CLSCC/<int:proposalID>/<int:const>/', views.showCLSCC, name='CLSCC'),
    path('damage/HSCHF/<int:proposalID>/<int:const>/', views.showHSCHF, name='HSCHF'),
    path('damage/HICSOHICHF/<int:proposalID>/<int:const>/', views.showHICSOHICHF, name='HICSOHICHF'),
    path('damage/chooseGoverningStressCorrosionCracking/<int:proposalID>/', views.ShowGoverningStressCorrosionCracking,
         name='GoverningStressCorrosionCracking'),
    # path('inspection/plan/<int:siteID>/', views.MainInpsectionPlan, name='inspectionPlan'),
    path('inspection/plan/<str:siteID>/', views.MainInpsectionPlan, name='inspectionPlan'),
    path('inspection/plan/<int:siteID>/<int:planID>/damageMechanism', views.DamamgeMechanism, name='damageMechanism'),
    # path('inspection/plan/<int:siteID>/InpsectionPlan<str:name>/InpsectionPlan<str:date>/', views.MainInpsectionPlan,name='inspectionPlan'),
    path('inspection/plan/<str:siteID>/InpsectionPlan<str:name>/InpsectionPlan<str:date>/', views.MainInpsectionPlan,name='inspectionPlan'),
    path('add/<int:siteID>/<int:facilityID>/<int:equipID>/<str:name>/<str:date>/plan/', views.AdddInssepctionPlan,name='addInspectionPlan'),
    path('scheduled/<int:siteID>/<str:name>/<str:date>/plan/', views.Scheduled,name='scheduled'),
    path('edit/<int:siteID>/<int:facilityID>/<int:equipID>/<str:name>/<str:date>/plan/', views.EditInspectionPlan,name='editInspectionPlan'),
    path('create/<int:siteID>/plan/', views.CreateInspectionPlan, name='createInspectionPlan'),
    # path('facilities/display/<int:siteID>/', views.ListFacilities, name='facilitiesDisplay'),
    path('facilities/display/<str:siteID>/', views.ListFacilities, name='facilitiesDisplay'),
    # path('facilities/setting/<int:siteID>/', views.settingAccount, name='settingAccount'),
    path('facilities/setting/<str:siteID>/', views.settingAccount, name='settingAccount'),
    # path('user/setting-notification/<int:siteID>/', views.settingNotification, name='settingNotification'),
    path('user/setting-notification/<str:siteID>/', views.settingNotification, name='settingNotification'),
    path('facilities/auto/<int:siteID>/Re-verification/setup/Fatories', views.AutoReVerificationSite, name='Re-verificationSite'),

    # path('facilities/display/sample-test/<int:siteID>/', views.TestSample, name='testsample'),
    path('facilities/display/sample-test/<str:siteID>/', views.TestSample, name='testsample'),
    path('facilities/display/sample-test/risk-analysis/<int:siteID>/<int:proposalID>/', views.InputdataFactory, name='inputdataTestSample'),
    path('sample-test/detail/risk-analysis/<int:siteID>/<int:proposalID>/', views.RiskAnalaysisTestSample, name='riskTestSample'),
    path('facilities/<int:siteID>/new/', views.NewFacilities, name='facilitiesNew'),
    path('facilities/<int:facilityID>/edit/', views.EditFacilities, name= 'facilitiesEdit'),
    path('designcode/display/<int:facilityID>/', views.ListDesignCode, name='designcodeDisplay'),
    path('designcode/display/<str:facilityID>/', views.ListDesignCode, name='designcodeDisplay'),
    path('designcode/<int:siteID>/new/', views.NewDesignCode, name='designcodeNew'),
    path('designcode/<int:designcodeID>/edit/', views.EditDesignCode, name='designcodeEdit'),
    # path('manufacture/display/<int:facilityID>/', views.ListManufacture, name='manufactureDisplay'),
    path('manufacture/display/<str:facilityID>/', views.ListManufacture, name='manufactureDisplay'),
    path('manufacture/<int:siteID>/new/', views.NewManufacture , name='manufactureNew'),
    path('manufacture/<int:manufactureID>/edit/', views.EditManufacture, name='manufactureEdit'),
    path('equipment/display/<int:facilityID>/', views.ListEquipment, name='equipmentDisplay'),
    path('equipment/<int:facilityID>/new/', views.NewEquipment, name='equipmentNew'),
    path('equipment/<int:equipmentID>/edit/', views.EditEquipment, name='equipmentEdit'),
    path('component/display/<int:equipmentID>/', views.ListComponent, name='componentDisplay'),
    path('component/<int:equipmentID>/new/', views.NewComponent , name='componentNew'),
    path('component/<int:componentID>/edit/', views.EditComponent, name='componentEdit'),
    path('proposal/display/<int:componentID>/', views.ListProposal, name='proposalDisplay'),
    path('proposal/importScada/<int:proposalID>/', views.ImportScada, name='importScada'),
    path('proposal/<int:componentID>/new/', views.NewProposal, name='proposalNew'),
    path('tank/<int:componentID>/new/', views.NewTank , name='tankNew'),
    path('proposal/<int:proposalID>/edit/', views.EditProposal, name='prosalEdit'),
    path('tank/<int:proposalID>/edit/', views.EditTank, name='tankEdit'),
    path('proposal/<int:proposalID>/risk-matrix/', views.RiskMatrix, name='riskMatrix'),
    path('proposal/<int:proposalID>/damage-factor/', views.FullyDamageFactor, name='damgeFactor'),
    path('proposal/<int:proposalID>/corrosion-control/', views.CorrosionControl, name='corrosionCotrol'),
    path('proposal/<int:proposalID>/chart/', views.RiskChart, name='riskChart'),
    path('proposal/<int:proposalID>/chartv2/', views.RiskchartV3, name='riskChartv2'),
    path('proposal/<int:proposalID>/fully-consequence/',views.FullyConsequence, name='fullyConsequence'),
    path('propasal/<int:proposalID>/areaBased-CoF/',views.AreaBasedCoF, name='areaBasedCoF'),
    path('proposal/comparision/<int:BenchMarkID>/<int:proposalID>/chart/', views.CompareBechMark, name='testBenchMark'),
    path('export/<int:index>/<str:type>/', views.ExportExcel, name='exportData'),
    # path('site/<int:siteID>/upload/InspectionHistory/', views.uploadInspPlan, name='upload'),
    path('site/<str:siteID>/upload/InspectionHistory/', views.uploadInspPlan, name='upload'),
    # path('site/<int:siteID>/<str:filename>upload/InspectionHistory/', views.uploadInspPlan, name='upload'),
    path('site/<str:siteID>/<str:filename>upload/InspectionHistory/', views.uploadInspPlan, name='upload'),
    # path('site/<int:siteID>/upload/Plan/', views.upload, name='uploadPlan'),
    path('site/<str:siteID>/upload/Plan/', views.upload, name='uploadPlan'),
    path('site/<int:siteID>/success/', views.successUpload, name='successUpload'),
    # path('site/<int:siteID>/<int:id>upload/Plan/', views.upload, name='uploadPlan'),#Cuong bo sung 14/9/2020
    path('site/<str:siteID>/<int:id>upload/Plan/', views.upload, name='uploadPlan'),#Cuong bo sung 14/9/2020
    # path('site/<int:siteID>/manage-files/', views.ManageFile, name='manageFile'),#Cuong bo sung 14/9/2020
    path('site/<str:siteID>/manage-files/', views.ManageFile, name='manageFile'),#Cuong bo sung 14/9/2020
    path('ManagmentSystems/<int:facilityID>/', views.ManagementSystems, name='managmentsystems'),
    # path('site/<int:siteID>/upload/DCS-SCADA/', views.uploadSCADA, name='uploadScada'),
    ########################## forum ################################
    path('forum/',views.base_forum,name='forum'),
    path('forum/post/<int:postID>',views.posts_forum,name='posts'),
    path('logout',views.logout,name='logout'),
    ########################## Messages ################################
    path('messagesinbox/', views.MessagesInbox, name='messagesInbox'),
    path('messagessent/', views.Email_Message_sent, name='messagesSent'),
    path('messagesinbox/<int:IDEmail>/seen/', views.MessagesInbox_seen, name='messagesIbox_seen'),
    path('messagessent/<int:IDEmail>/seen/', views.MessagesSent_Seen, name='messagesSent_seen'),
    ########################## Help ################################
    path('help/',views.Help, name='help'),
    path('help/UserManual/Citizen',views.Help_Usermanual_Citizen,name='helpUserManualCtizen'),
    path('help/UserManual/Business',views.Help_Usermanual_Business,name='helpUserManualBusiness'),
    path('help/UserManual/Manager',views.Help_Usermanual_Manager,name='helpUserManualManager'),
    path('help/AccountManagement/LoginPasswork',views.Help_AccountManagement_LoginPass,name='LoginPasswork'),
    path('help/AccountManagement/PersonalInfor',views.Help_AccountManagement_PerInfo,name='perinfor'),
    path('help/AccountManagement/AccessDownload',views.Help_AccountManagement_AccessDownload,name='accdownload'),
    path('help/AccountManagement/notification',views.Help_AccountManagement_Notification,name='notification'),
    path('help/PrivateSafe/',views.Private_Safe,name='PrivateSafe'),
    path('help/PoliciesReports/',views.Policies_Reports,name='PoliciesReports'),
    ########################## Dang ki tai khoan ################################
    path('AccountCitizen/', views.AccountCitizen, name='accountcitizen'),
    path('AccountBusiness/',views.AccountBusiness, name='accountbusiness'),
    path('AccountManagement',views.AccountManagement,name='accountmanagement'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    ########################## Manager UI################################
    path('management/<int:siteID>/Admin/',views.Admin, name= 'admin1'),
    path('management/<int:siteID>/RegisterAccount/',views.RegisterAccount,name ='registerAccount'),
    path('management/<int:siteID>/', views.ManagerHome, name= 'manager'),
    path('importExcel/<str:url_file>/', views.ImportExcel, name= 'importexcel'),
    # Cuong bo sung 12/8/2020 => thiet ke giao dien hang mmuc co quan quan li
    path('mitigation/<int:siteID>/Home/', views.Mitigation, name= 'mitigation'),
    path('mitigation/<int:siteID>/<int:proposalID>/damage-mechanism/', views.MitigationDetail, name= 'damageDetailmitigation'),
    # Cuong bo sung mitigationSite cho hạng mục nhà máy 28/9/2020
    # path('mitigationSite/<int:siteID>/', views.MitigationSite, name= 'mitigationSite'),
    path('mitigationSite/<str:siteID>/', views.MitigationSite, name= 'mitigationSite'),
    path('mitigation-detail/<int:x1>/<int:x2>/', views.MitigationDetailV2, name= 'mitigationdetail'),
    path('management/<int:siteID>/Home/', views.ManagerHomeDetail, name= 'managerhomedetail'),
    path('admin/<int:siteID>/Home/', views.AdminDetail, name= 'admindetail'),
    # path('facilities/<int:siteID>/Home/', views.HomeFacility, name='homefacility'),
    path('facilities/<str:siteID>/Home/', views.HomeFacility, name='homefacility'),
    path('management/<int:siteID>/CalculateFunction/', views.CalculateFunctionManager, name= 'calculatefunctionmanager'),
    path('management/<int:siteID>/ToolManager/', views.ToolManager, name= 'toolmanager'),
    path('manufactureMana/display/<int:siteID>/', views.ListManufactureMana, name='manufactureDisplayMana'),
    path('designcodeMana/display/<int:siteID>/', views.ListDesignCodeMana, name='designcodeDisplayMana'),
    path('facilitiesMana/display/<int:siteID>/', views.ListFacilitiesMana, name='facilitiesDisplayMana'),
    path('equipmentMana/display/<int:facilityID>/', views.ListEquipmentMana, name='equipmentDisplayMana'),
    path('componentMana/display/<int:equipmentID>/', views.ListComponentMana, name='componentDisplayMana'),
    path('proposalMana/display/<int:componentID>/', views.ListProposalMana, name='proposalDisplayMana'),
    path('proposalMana/<int:proposalID>/data/', views.Inputdata, name='inputdata'),
    path('proposalMana/<int:proposalID>/damage-factor/', views.FullyDamageFactorMana, name='damgeFactorMana'),
    path('proposalMana/<int:proposalID>/chart/', views.RiskChartMana, name='riskChartMana'),
    path('proposalMana/<int:proposalID>/risk-matrix/', views.RiskMatrixMana, name='riskMatrixMana'),
    path('proposalMana/<int:proposalID>/fully-consequence/',views.FullyConsequenceMana, name='fullyConsequenceMana'),
#testCuong
    path('proposal/<int:proposalID>/corrisionRate/', views.CorrisionRate, name='corrision'),
    path('proposal/<int:proposalID>/caculated/', views.CaculateCorrision, name='Caculate'),
    ############# Verification #############
    path('verification/<int:faciid>',views.VerificationHome,name='VerificationHome'),
    path('verification/<int:verifiID>/Check',views.VerificationCheck,name='VerificationCheck'),
    path('verificationFaci',views.VerificationNumberFacilities,name='VerificationFaci'),
    ######################### Citizen UI ##############################
    path('citizen/', views.citizen_home, name= 'citizenHome'),
    path('facilityCitizen/display/<int:siteID>/',views.ListfacilityCitizen, name='facilityCitizen'),
    path('ListProposalCitizen/display/<int:facilityID>/<int:siteID>/',views.ListProposalCitizen, name='ListProposalCitizen'),
    path('proposalCitizen/<int:proposalID>/risk-matrix/', views.RiskMatrixCitizen, name='riskMatrixCitizen'),
    path('proposalCitizen/<int:proposalID>/damage-factor/', views.FullyDamageFactorCitizen, name='damgeFactorCitizen'),
    path('proposalCitizen/<int:proposalID>/chart/', views.RiskChartCitizen, name='riskChartCitizen'),
    path('proposalCitizen/<int:proposalID>/fully-consequence/',views.FullyConsequenceCitizen, name='fullyConsequenceCitizen'),
    #############connect thingsboard _____ sensor, gateway #############
    path('newsensor/<int:componentID>/', views.NewSensor, name='newsensor'),
    path('scada/<int:componentID>/', views.NewScada, name='scada'),
    path('sensor/<int:componentID>/chart/', views.DataChart, name='sensorchart'),
    path('sensor/<int:componentID>/setting/', views.Setting, name='setting'),
    # Datdz
    path('report/', views.ReportMana, name='reportmana'),
    path('reportfac/<int:siteID>/', views.ReportFacilities, name='reportfacilities'),
    path('reportequip/<int:facilityID>/', views.ReportEquipment, name='reportequipment'),
    path('reportcomp/<int:equipmentID>/', views.ReportComponent, name='reportcomponent'),
    path('reportproposal/<int:componentID>/', views.ReportProposal, name='reportproposal'),
    path('propasal/<int:proposalID>/areaBased-CoF-shell/',views.AreaBasedCoFShell, name='AreaBasedCoFShell'),
    path('help/UseSoftware', views.Help_UseSoftware, name='helpUseSoftware'),
    path('proposal/noviewexcel/', views.ExcelEmpty, name='excelempty'),
    path('proposal/viewexcel/<int:index>/<str:type>/', views.ViewExeclProposal, name='viewexcelproposal'),
    path('databasereport/',views.DatabaseReport, name='databasereport'),
    path('rbitracking/',views.RBITracking, name='rbitracking'),
    path('verification/<int:verifiID>/Delete',views.Verificationdelete,name='Verificationdelete'),
    path('fullyConsequencelv2/<int:proposalID>/', views.FullyConsequencelv2, name='fullyConsequencelv2'),
    path('<int:siteID>/requesthistory/',views.Viewhistoryrequest, name='historyrequest'),
    path('proposaldetail/<int:faciid>/<int:reportid>', views.proposal_detail, name='proposaldetail'),
    
    # path('proposal/chart/<int:componentID>/', views.ListProposal, name='proposalChart'),
    path('proposal/chart', views.testva, name="testva" )
]
handler500 = 'cloud.views.handler404'
handler404 = 'cloud.views.handler404'

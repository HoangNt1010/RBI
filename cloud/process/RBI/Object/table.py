import numpy as np 

class ConversionFactorCOF:
    _C1 = 31623.0
    _C10 = 9.744
    _C11 = 0.145
    _C12 = 1.8
    _C13 = 6.29
    _C14 = 1.0
    _C15 = 4.685
    _C16 = 30.89
    _C17 = 0.001481
    _C18 = 0.005
    _C19 = 1.085
    _C2 = 1000.0
    _C20 = 1.013
    _C21 = 5328.0
    _C22 = 5.8
    _C23 = 0.45
    _C24 = 2.6
    _C25 = 0.0296
    _C26 = 100.0
    _C27 = 1.0
    _C28 = 1000.0
    _C29 = 0.0004303
    _C3 = 4536.0
    _C30 = 9.76E-08
    _C31 = 864.0
    _C32 = 0.543
    _C33 = 0.0815
    _C34 = 86.4
    _C35 = 2.382
    _C36 = 30.5
    _C37 = 1.408E-08
    _C38 = 1.1341
    _C39 = 3.9365
    _C4 = 2.205
    _C40 = 5.9352
    _C5 = 25.2
    _C6 = 55.6
    _C7 = 1.0
    _C8 = 0.0929
    _C9 = 0.123


class FluidPhase:
    Gas = "Gas"
    Liquid = "Liquid"
    Powder = "Powder"


class TBL52:
    def __init__(self, fluid):
        self.fluid = fluid
        self.C1_To_C2 = (23.0, 250.512, 148.0, 831.0, FluidPhase.Gas,
                         1, 12.3, 0.115, -2.87E-05, -1.3E-09, 0.0, 0.0)
        self.C3_To_C4 = (51.0, 538.379, 252.0, 642.0, FluidPhase.Gas,
                         1, 2.632, 0.3188, -13500.0, 1.47E-08, 0.0, 0.0)
        self.C5 = (72.0, 625.199, 309.0, 557.0, FluidPhase.Liquid,
                   1, -3.626, 0.4873, -0.00026, 5.3E-08, 0.0, 0.0)
        self.C6_To_C8 = (100.0, 684.018, 372.0, 496.0, FluidPhase.Liquid,
                         1, -5.146, 0.676, -0.000365, 7.66E-08, 0.0, 0.0)
        self.C9_To_C12 = (149.0, 734.012, 457.0, 481.0,
                          FluidPhase.Liquid, 1, -8.5, 1.01, -0.000556, 1.18E-07, 0.0, 0.0)
        self.C13_To_C16 = [205.0, 764.527, 534.0, 475.0,
                           FluidPhase.Liquid, 1, -11.7, 1.39, -0.000772, 1.67E-07, 0.0, 0.0]
        self.C17_To_C25 = [280.0, 775.019, 617.0, 475.0,
                           FluidPhase.Liquid, 1, -22.4, 1.94, -0.00112, -2.53E-07, 0.0, 0.0]
        self.C25_And_Above = [422.0, 900.026, 800.0, 475.0,
                              FluidPhase.Liquid, 1, -22.4, 1.94, -0.00112, -2.53E-07, 0.0, 0.0]
        self.Water = [18.0, 997.947, 373.0, False, FluidPhase.Liquid,
                      3, 276000.0, -2090.0, 8.125, -0.0141, 9.37E-06, 0.0]
        self.Steam = [18.0, 997.947, 373.0, False, FluidPhase.Gas,
                      3, 33400.0, 26800.0, 2610.0, 8900.0, 1170.0, 0.0]
        self.Acid = [18.0, 997.947, 373.0, False, FluidPhase.Liquid,
                     3, 276000.0, -2090.0, 8.125, -0.0141, 9.37E-06, 0.0]
        self.Caustic = [18.0, 997.947, 373.0, False, FluidPhase.Liquid,
                        3, 276000.0, -2090.0, 8.125, -0.0141, 9.37E-06, 0.0]
        self.H2 = [2.0, 71.01, 20.0, 673.0, FluidPhase.Gas,
                   1, 27.1, 0.00927, -1.38E-05, 7.65E-09, 0.0, 0.0]
        self.H2S = [34.0, 993.029, 214.0, 533.0, FluidPhase.Gas,
                    1, 31.9, 0.00144, 2.43E-05, -1.18E-08, 0.0, 0.0]
        self.HFAcid = [20.0, 967.031, 293.0, 18033.0, FluidPhase.Gas,
                       1, 29.1, 0.000661, -2.03E-06, 2.5E-09, 0.0, 0.0]
        self.CO = [28.0, 800.92, 82.0, 882.0, FluidPhase.Gas,
                   2, 29100.0, 8770.0, 3090.0, 8460.0, 1540.0, 0.0]
        self.DEE = [74.0, 720.828, 308.0, 433.0, FluidPhase.Liquid,
                    2, 86200.0, 255000.0, 1540.0, 144000.0, -689.0, 0.0]
        self.HCL = [36.0, 1185.362, 188.0, False,
                    FluidPhase.Gas, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.4]
        self.NitricAcid = [63.0, 1521.749, 394.0, False,
                           FluidPhase.Liquid, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5]
        self.AlCl3 = [133.5, 2434.798, 467.0, 831.0, FluidPhase.Powder,
                      1, 43400.0, 39700.0, 417.0, 24000.0, 0.0, 0.0]
        self.NO2 = [90.0, 929.068, 408.0, False,
                    FluidPhase.Liquid, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5]
        self.Phosgene = [99.0, 1377.583, 356.0, False,
                         FluidPhase.Liquid, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5]
        self.TDI = [174.0, 1217.399, 524.0, 893.0,
                    FluidPhase.Liquid, 4, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5]
        self.Methanol = [32.0, 800.92, 338.0, 737.0, FluidPhase.Liquid,
                         2, 39300.0, 87900.0, 1920.0, 53700.0, 897.0, 0.0]
        self.PO = [58.0, 832.957, 307.0, 722.0, FluidPhase.Liquid,
                   2, 49500.0, 174000.0, 1560.0, 115000.0, 702.0, 0.0]
        self.Styrene = [104.0, 683.986, 418.0, 763.0, FluidPhase.Liquid,
                        2, 89300.0, 215000.0, 772.0, 99900.0, 2440.0, 0.0]
        self.EE = [132.0, 977.123, 429.0, 652.0, FluidPhase.Liquid,
                   2, 106000.0, 240000.0, 659.0, 150000.0, 1970.0, 0.0]
        self.EEA = [90.0, 929.068, 408.0, 508.0, FluidPhase.Liquid,
                    2, 32500.0, 300000.0, 1170.0, 208000.0, 473.0, 0.0]
        self.EG = [62.0, 1105.27, 470.0, 669.0, FluidPhase.Liquid,
                   2, 63000.0, 146000.0, 1670.0, 97300.0, 774.0, 0.0]
        self.EO = [44.0, 881.013, 284.0, 702.0, FluidPhase.Gas,
                   2, 33500.0, 121000.0, 1610.0, 82400.0, 737.0, 0.0]
        self.Pyrophoric = [149.0, 734.012, 457.0, 274.0,
                           FluidPhase.Liquid, 1, -8.5, 1.01, -0.000556, 1.18E-07, 0.0, 0.0]
        self.Ammonia = [17.0, 681.9, 240.0, 924.0,
                        FluidPhase.Gas, 6, 0.0, 0.0, 0.0, 0.0, 0.0, 1.32]
        self.Chlorine = [71.0, 1562.5, 239.0, False,
                         FluidPhase.Gas, 7, 0.0, 0.0, 0.0, 0.0, 0.0, 1.33]

    def get_data(self):
        if (self.fluid == "Caustic"):
            return self.Caustic
        elif (self.fluid == "Acid"):
            return self.Acid
        elif (self.fluid == "AlCl3"):
            return self.AlCl3
        elif (self.fluid == "C1-C2"):
            return self.C1_To_C2
        elif (self.fluid == "C13-C16"):
            return self.C13_To_C16
        elif (self.fluid == "C17-C25"):
            return self.C17_To_C25
        elif (self.fluid == "C25+"):
            return self.C25_And_Above
        elif (self.fluid == "C3-C4"):
            return self.C3_To_C4
        elif (self.fluid == "C5"):
            return self.C5
        elif (self.fluid == "C6-C8"):
            return self.C6_To_C8
        elif (self.fluid == "C9-C12"):
            return self.C9_To_C12
        elif (self.fluid == "CO"):
            return self.CO
        elif (self.fluid == "DEE"):
            return self.DEE
        elif (self.fluid == "EE"):
            return self.EE
        elif (self.fluid == "EEA"):
            return self.EEA
        elif (self.fluid == "EG"):
            return self.EG
        elif (self.fluid == "EO"):
            return self.EO
        elif (self.fluid == "H2"):
            return self.H2
        elif (self.fluid == "H2S"):
            return self.H2S
        elif (self.fluid == "HCl"):
            return self.HCL
        elif (self.fluid == "HF"):
            return self.HFAcid
        elif (self.fluid == "Methanol"):
            return self.Methanol
        elif (self.fluid == "Nitric Acid"):
            return self.NitricAcid
        elif (self.fluid == "NO2"):
            return self.NO2
        elif (self.fluid == "PO"):
            return self.PO
        elif (self.fluid == "Pyrophoric"):
            return self.Pyrophoric
        elif (self.fluid == "Steam"):
            return self.Steam
        elif (self.fluid == "Styrene"):
            return self.Styrene
        elif (self.fluid == "TDI"):
            return self.TDI
        elif (self.fluid == "Water"):
            return self.Water
        elif (self.fluid == "Ammonia"):
            return self.Ammonia
        elif (self.fluid == "Chlorine"):
            return self.Chlorine
        else:
            return 0


class TBL74:
    def __init__(self, svi, field):
        self.svi = svi
        self.field = field
        self.TableA = np.array
        self.TableB = np.array
        self.TableC = np.array
        self.TableD = np.array
        self.TableA = np.append(
            self.TableA, [1.0,  [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableA = np.append(
            self.TableA, [10.0,  [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableA = np.append(
            self.TableA, [50.0, [3.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableA = np.append(
            self.TableA, [100.0, [5.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableA = np.append(
            self.TableA, [500.0, [25.0, 5.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableA = np.append(
            self.TableA, [1000.0, [50.0, 10.0, 2.0, 1.0, 1.0, 1.0]])
        self.TableA = np.append(
            self.TableA, [5000.0, [250.0, 50.0, 10.0, 2.0, 1.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [1.0, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [10.0, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [50.0, [5.0, 2.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [100.0, [10.0, 4.0, 2.0, 1.0, 1.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [500.0, [50.0, 20.0, 8.0, 2.0, 1.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [1000.0, [100.0, 40.0, 16.0, 5.0, 2.0, 1.0]])
        self.TableB = np.append(
            self.TableB, [5000.0, [500.0, 250.0, 80.0, 25.0, 5.0, 2.0]])
        self.TableC = np.append(
            self.TableC, [1.0, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableC = np.append(
            self.TableC, [10.0, [3.0, 2.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableC = np.append(
            self.TableC, [50.0, [17.0, 10.0, 5.0, 2.0, 1.0, 1.0]])
        self.TableC = np.append(
            self.TableC, [100.0, [33.0, 20.0, 10.0, 5.0, 2.0, 1.0]])
        self.TableC = np.append(
            self.TableC, [500.0, [170.0, 100.0, 50.0, 25.0, 10.0, 5.0]])
        self.TableC = np.append(
            self.TableC, [1000.0, [330.0, 200.0, 100.0, 50.0, 25.0, 10.0]])
        self.TableC = np.append(
            self.TableC, [5000.0, [1670.0, 1000.0, 500.0, 250.0, 125.0, 50.0]])
        self.TableD = np.append(
            self.TableD, [1.0, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        self.TableD = np.append(
            self.TableD, [10.0, [8.0, 6.0, 4.0, 2.0, 1.0, 1.0]])
        self.TableD = np.append(
            self.TableD, [50.0, [40.0, 30.0, 20.0, 10.0, 5.0, 1.0]])
        self.TableD = np.append(
            self.TableD, [100.0, [80.0, 60.0, 40.0, 20.0, 10.0, 5.0]])
        self.TableD = np.append(
            self.TableD, [500.0, [400.0, 300.0, 200.0, 100.0, 50.0, 25.0]])
        self.TableD = np.append(
            self.TableD, [1000.0, [800.0, 600.0, 400.0, 200.0, 100.0, 50.0]])
        self.TableD = np.append(
            self.TableD, [5000.0, [4000.0, 3000.0, 2000.0, 1000.0, 500.0, 250.0]])

    def getdata():
        return Table7_4.TableA[1][0]

    def GET_TBL_74(self):
        if self.field == "E":
            return self.svi
        elif self.field == "1D":
            return ((self.TableD[(np.where(self.TableD == self.svi))[0] + 1][0])[0])
        elif self.field == "1C":
            return ((self.TableC[(np.where(self.TableD == self.svi))[0] + 1][0])[0])
        elif self.field == "1B":
            return ((self.TableB[(np.where(self.TableD == self.svi))[0] + 1][0])[0])
        elif self.field == "1A":
            return ((self.TableA[(np.where(self.TableD == self.svi))[0] + 1][0])[0])
        elif self.field == "2D":
            return ((self.TableD[(np.where(self.TableD == self.svi))[0] + 1][0])[1])
        elif self.field == "2C":
            return ((self.TableC[(np.where(self.TableD == self.svi))[0] + 1][0])[1])
        elif self.field == "2B":
            return ((self.TableB[(np.where(self.TableD == self.svi))[0] + 1][0])[1])
        elif self.field == "2A":
            return ((self.TableA[(np.where(self.TableD == self.svi))[0] + 1][0])[1])
        elif self.field == "3D":
            return ((self.TableD[(np.where(self.TableD == self.svi))[0] + 1][0])[2])
        elif self.field == "3C":
            return ((self.TableC[(np.where(self.TableD == self.svi))[0] + 1][0])[2])
        elif self.field == "3B":
            return ((self.TableB[(np.where(self.TableD == self.svi))[0] + 1][0])[2])
        elif self.field == "3A":
            return ((self.TableA[(np.where(self.TableD == self.svi))[0] + 1][0])[2])
        elif self.field == "4D":
            return ((self.TableD[(np.where(self.TableD == self.svi))[0] + 1][0])[3])
        elif self.field == "4C":
            return ((self.TableC[(np.where(self.TableD == self.svi))[0] + 1][0])[3])
        elif self.field == "4B":
            return ((self.TableB[(np.where(self.TableD == self.svi))[0] + 1][0])[3])
        elif self.field == "4A":
            return ((self.TableA[(np.where(self.TableD == self.svi))[0] + 1][0])[3])
        elif self.field == "5D":
            return ((self.TableD[(np.where(self.TableD == self.svi))[0] + 1][0])[4])
        elif self.field == "5C":
            return ((self.TableC[(np.where(self.TableD == self.svi))[0] + 1][0])[4])
        elif self.field == "5B":
            return ((self.TableB[(np.where(self.TableD == self.svi))[0] + 1][0])[4])
        elif self.field == "5A":
            return ((self.TableA[(np.where(self.TableD == self.svi))[0] + 1][0])[4])
        elif self.field == "6D":
            return ((self.TableD[(np.where(self.TableD == self.svi))[0] + 1][0])[5])
        elif self.field == "6C":
            return ((self.TableC[(np.where(self.TableD == self.svi))[0] + 1][0])[5])
        elif self.field == "6B":
            return ((self.TableB[(np.where(self.TableD == self.svi))[0] + 1][0])[5])
        else:
            return ((self.TableA[(np.where(self.TableD == self.svi))[0] + 1][0])[5])


class Table7_4:
    TableA = {1.0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              10.0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              50.0: [3.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              100.0: [5.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              500.0: [25.0, 5.0, 1.0, 1.0, 1.0, 1.0],
              1000.0: [50.0, 10.0, 2.0, 1.0, 1.0, 1.0],
              5000.0: [250.0, 50.0, 10.0, 2.0, 1.0, 1.0]}
    TableB = {1.0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              10.0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              50.0: [5.0, 2.0, 1.0, 1.0, 1.0, 1.0],
              100.0: [10.0, 4.0, 2.0, 1.0, 1.0, 1.0],
              500.0: [50.0, 20.0, 8.0, 2.0, 1.0, 1.0],
              1000.0: [100.0, 40.0, 16.0, 5.0, 2.0, 1.0],
              5000.0: [500.0, 250.0, 80.0, 25.0, 5.0, 2.0]}
    TableC = {1.0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              10.0: [3.0, 2.0, 1.0, 1.0, 1.0, 1.0],
              50.0: [17.0, 10.0, 5.0, 2.0, 1.0, 1.0],
              100.0: [33.0, 20.0, 10.0, 5.0, 2.0, 1.0],
              500.0: [170.0, 100.0, 50.0, 25.0, 10.0, 5.0],
              1000.0: [330.0, 200.0, 100.0, 50.0, 25.0, 10.0],
              5000.0: [1670.0, 1000.0, 500.0, 250.0, 125.0, 50.0]}
    TableD = {1.0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
              10.0: [8.0, 6.0, 4.0, 2.0, 1.0, 1.0],
              50.0: [40.0, 30.0, 20.0, 10.0, 5.0, 1.0],
              100.0: [80.0, 60.0, 40.0, 20.0, 10.0, 5.0],
              500.0: [400.0, 300.0, 200.0, 100.0, 50.0, 25.0],
              1000.0: [800.0, 600.0, 400.0, 200.0, 100.0, 50.0],
              5000.0: [4000.0, 3000.0, 2000.0, 1000.0, 500.0, 250.0]}


class getDataFromTable:
    def TBL7_4(svi, field):
        if field == "E":
            return svi
        elif field == "1D":
            return Table7_4.TableD[svi][0]
        elif field == "1C":
            return Table7_4.TableC[svi][0]
        elif field == "1B":
            return Table7_4.TableB[svi][0]
        elif field == "1A":
            return Table7_4.TableA[svi][0]
        elif field == "2D":
            return Table7_4.TableD[svi][1]
        elif field == "2C":
            return Table7_4.TableC[svi][1]
        elif field == "2B":
            return Table7_4.TableB[svi][1]
        elif field == "2A":
            return Table7_4.TableA[svi][1]
        elif field == "3D":
            return Table7_4.TableD[svi][2]
        elif field == "3C":
            return Table7_4.TableC[svi][2]
        elif field == "3B":
            return Table7_4.TableB[svi][2]
        elif field == "3A":
            return Table7_4.TableA[svi][2]
        elif field == "4D":
            return Table7_4.TableD[svi][3]
        elif field == "4C":
            return Table7_4.TableC[svi][3]
        elif field == "4B":
            return Table7_4.TableB[svi][3]
        elif field == "4A":
            return Table7_4.TableA[svi][3]
        elif field == "5D":
            return Table7_4.TableD[svi][4]
        elif field == "5C":
            return Table7_4.TableC[svi][4]
        elif field == "5B":
            return Table7_4.TableB[svi][4]
        elif field == "5A":
            return Table7_4.TableA[svi][4]
        elif field == "6D":
            return Table7_4.TableD[svi][5]
        elif field == "6C":
            return Table7_4.TableC[svi][5]
        elif field == "6B":
            return Table7_4.TableB[svi][5]
        else:
            return Table7_4.TableA[svi][5]
# tuan


class Table204:
    TableNoInspection = {'Damage': [0.0],
                         'High': [2000.0],
                         'Low': [20.0],
                         'Medium': [200.0],
                         'Not': [1.0]}
    TableB = {'Damage': [2000.0, 2000.0],
              'High': [800.0, 400.0],
              'Low': [8.0, 4.0],
              'Medium': [80.0, 40.0],
              'Not': [1.0, 1.0]}
    TableC = {'Damage': [2000.0, 2000.0],
              'High': [1200.0, 800.0],
              'Low': [12.0, 8.0],
              'Medium': [120.0, 80],
              'Not': [1.0, 1.0]}
    TableD = {'Damage': [2000.0, 2000.0],
              'High': [1800.0, 1600.0],
              'Low': [18.0, 16.0],
              'Medium': [180.0, 160.0],
              'Not': [1.0, 1.0]}


class Table58:
    def __init__(self, fluid):
        self.fluid = fluid
        self.Aromatics = (64.14, 0.963, 353.5, 0.883, 1344, 0.937, 487.7,
                          0.268, 18.08, 0.686, 0.14, 0.935, 512.6, 0.713, 1.404, 0.935)
        self.C1_To_C2 = (8.669, 0.98, 8.669, 0.98, 55.13, 0.95, 55.13,
                         0.95, 6.469, 0.67, 6.469, 0.67, 163.7, 0.62, 163.7, 0.62)
        self.C13_To_C16 = (0, 0, 12.11, 0.9, 0, 0, 196.7,
                           0.92, 0, 0, 0.086, 0.88, 0, 0, 1.714, 0.88)
        self.C17_To_C25 = (0, 0, 3.785, 0.9, 0, 0, 165.5,
                           0.92, 0, 0, 0.021, 0.91, 0, 0, 1.068, 0.91)
        self.C25_plus = (0, 0, 2.098, 0.91, 0, 0, 103, 0.9,
                         0, 0, 0.006, 0.99, 0, 0, 0.284, 0.99)
        self.C3_To_C4 = (10.13, 1, 0, 0, 64.23, 1, 0, 0,
                         4.59, 0.72, 0, 0, 79.94, 0.63, 0, 0)
        self.C5 = (5.115, 0.99, 100.6, 0.89, 62.41, 1, 0, 0,
                   2.214, 0.73, 0.271, 0.85, 41.38, 0.61, 0, 0)
        self.C6_To_C8 = (5.846, 0.98, 34.17, 0.89, 63.98, 1, 103.4,
                         0.95, 2.188, 0.66, 0.749, 0.78, 41.49, 0.61, 8.18, 0.55)
        self.C9_To_C12 = (2.419, 0.98, 24.6, 0.9, 76.98, 0.95, 110.3,
                          0.95, 1.111, 0.66, 0.559, 0.76, 42.28, 0.61, 0.848, 0.53)
        self.CO = (0.04, 1.752, 0.04, 1.752, 0, 0, 0, 0,
                   10.97, 0.667, 10.97, 0.667, 0, 0, 0, 0)
        self.DEE = (9.072, 1.134, 164.2, 1.106, 67.42, 1.033, 976,
                    0.649, 24.51, 0.667, 0.981, 0.919, 0, 0, 1.09, 0.919)
        self.EE = (2.595, 1.005, 35.45, 1, 0, 0, 0, 0,
                   6.119, 0.667, 14.79, 1, 0, 0, 0, 0)
        self.EEA = (0, 1.035, 23.96, 1, 0, 0, 0, 0,
                    1.261, 0.667, 14.13, 1, 0, 0, 0, 0)
        self.EG = (1.548, 0.973, 22.12, 1, 0, 0, 0, 0,
                   1.027, 0.667, 14.13, 1, 0, 0, 0, 0)
        self.EO = (6.712, 1.069, 6.712, 1.069, 0, 0, 0, 0,
                   21.46, 0.667, 21.46, 0.667, 0, 0, 0, 0)
        self.H2 = (13.13, 0.992, 13.13, 0.992, 86.02, 1, 86.02, 1,
                   9.605, 0.657, 9.605, 0.657, 216.5, 0.618, 216.5, 0.618)
        self.H2S = (6.554, 1, 6.554, 1, 38.11, 0.89, 38.11, 0.89,
                    22.63, 0.63, 22.63, 0.63, 53.72, 0.61, 53.72, 0.61)
        self.HF = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.Methanol = (0.005, 0.909, 340.4, 0.934, 0, 0, 0,
                         0, 4.425, 0.667, 0.363, 0.9, 0, 0, 0, 0)
        self.PO = (3.277, 1.114, 257, 0.96, 0, 0, 0, 0,
                   10.32, 0.667, 0.629, 0.869, 0, 0, 0, 0)
        self.Pyrophoric = (2.419, 0.98, 24.6, 0.9, 76.98, 0.95, 110.3,
                           0.95, 1.111, 0.66, 0.559, 0.76, 42.28, 0.61, 0.848, 0.53)
        self.Styrene = (3.952, 1.097, 21.1, 1, 80.11, 1.055, 0,
                        0, 1.804, 0.667, 14.36, 1, 83.68, 0.713, 143.6, 1)

    def get_data(self):
        if (self.fluid == "Aromatics"):
            return self.Aromatics
        if (self.fluid == "C1-C2"):
            return self.C1_To_C2
        if (self.fluid == "C13-C16"):
            return self.C13_To_C16
        if (self.fluid == "C17-C25"):
            return self.C17_To_C25
        if (self.fluid == "C25+"):
            return self.C25_plus
        if (self.fluid == "C3-C4"):
            return self.C3_To_C4
        if (self.fluid == "C5"):
            return self.C5
        if (self.fluid == "C6-C8"):
            return self.C6_To_C8
        if (self.fluid == "C9-C12"):
            return self.C9_To_C12
        if (self.fluid == "CO"):
            return self.CO
        if (self.fluid == "DEE"):
            return self.DEE
        if (self.fluid == "EE"):
            return self.EE
        if (self.fluid == "EEA"):
            return self.EEA
        if (self.fluid == "EG"):
            return self.EG
        if (self.fluid == "EO"):
            return self.EO
        if (self.fluid == "H2"):
            return self.H2
        if (self.fluid == "H2S"):
            return self.H2S
        if (self.fluid == "HF"):
            return self.HF
        if (self.fluid == "Methanol"):
            return self.Methanol
        if (self.fluid == "PO"):
            return self.PO
        if (self.fluid == "Pyrophoric"):
            return self.Pyrophoric
        if (self.fluid == "Styrene"):
            return self.Styrene


class Table59:
    def __init__(self, fluid):
        self.fluid = fluid
        self.Aromatics = (12.76, 0.963, 66.01, 0.883, 261.9, 0.937, 56.0,
                          0.268, 2.889, 0.686, 0.027, 0.935, 83.68, 0.713, 0.273, 0.935)
        self.C1_To_C2 = (21.83, 0.96, 21.83, 0.96, 143.2, 0.92, 142.2,
                         0.92, 12.46, 0.67, 12.46, 0.67, 473.9, 0.63, 473.9, 0.63)
        self.C13_To_C16 = (0.0, 0.0, 34.36, 0.89, 0.0, 0.0, 539.4,
                           0.9, 0.0, 0.0, 0.242, 0.88, 0.0, 0.0, 4.843, 0.88)
        self.C17_To_C25 = (0.0, 0.0, 10.7, 0.89, 0.0, 0.0, 458,
                           0.9, 0.0, 0.0, 0.061, 0.91, 0.0, 0.0, 3.052, 0.9)
        self.C25_plus = (0.0, 0.0, 6.196, 0.89, 0.0, 0.0, 303.6,
                         0.9, 0.0, 0.0, 0.016, 0.99, 0.0, 0.0, 0.833, 0.99)
        self.C3_To_C4 = (25.64, 1.0, 25.64, 1.0, 171.4, 1.0, 171.4,
                         1.0, 9.702, 0.75, 9.702, 0.75, 270.4, 0.63, 270.4, 0.63)
        self.C5 = (12.71, 1.0, 290.1, 0.89, 166.1, 1.0, 0.0, 0.0,
                   4.82, 0.76, 0.79, 0.85, 146.7, 0.63, 0.0, 0.0)
        self.C6_To_C8 = (3.49, 0.96, 96.88, 0.89, 169.7, 1.0, 252.8,
                         0.92, 4.216, 0.67, 2.186, 0.78, 147.2, 0.63, 31.89, 0.54)
        self.C9_To_C12 = (5.755, 0.96, 70.03, 0.89, 188.6, 0.92, 269.4,
                          0.92, 2.035, 0.66, 1.609, 0.76, 151, 0.63, 2.847, 0.54)
        self.CO = (5.491, 0.991, 5.491, 0.991, 0.0, 0.0, 0.0, 0.0,
                   16.91, 0.692, 16.91, 0.692, 0.0, 0.0, 0.0, 0.0)
        self.DEE = (26.76, 1.025, 236.7, 1.219, 241.5, 0.997, 488.9,
                    0.864, 31.71, 0.682, 8.333, 0.814, 128.3, 0.657, 9.258, 0.814)
        self.EE = (7.107, 0.969, 8.142, 0.8, 0.0, 0.0, 0.0, 0.0,
                   25.36, 0.66, 0.029, 0.927, 0.0, 0.0, 0.0, 0.0)
        self.EEA = (0.0, 0.946, 79.66, 0.835, 0.0, 0.0, 0.0, 0.0,
                    1.825, 0.687, 0.03, 0.924, 0.0, 0.0, 0.0, 0.0)
        self.EG = (5.042, 0.947, 59.96, 0.869, 0.0, 0.0, 0.0, 0.0,
                   1.435, 0.687, 0.027, 0.922, 0.0, 0.0, 0.0, 0.0)
        self.EO = (11, 1.105, 11, 1.105, 0.0, 0.0, 0.0, 0.0,
                   34.7, 0.665, 34.7, 0.665, 0.0, 0.0, 0.0, 0.0)
        self.H2 = (32.05, 0.933, 0.0, 0.0, 228.8, 1.0, 0.0, 0.0,
                   18.43, 0.652, 0.0, 0.0, 636.5, 0.621, 0.0, 0.0)
        self.H2S = (10.65, 1.0, 0.0, 0.0, 73.25, 0.94, 0.0, 0.0,
                    41.43, 0.63, 0.0, 0.0, 191.5, 0.63, 0.0, 0.0)
        self.HF = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.Methanol = (0.0, 1.008, 849.9, 0.902, 0.0, 0.0, 0.0,
                         0.0, 6.035, 6.88, 1.157, 0.871, 0.0, 0.0, 0.0, 0.0)
        self.PO = (8.239, 1.047, 352.8, 0.84, 0.0, 0.0, 0.0, 0.0,
                   13.33, 0.682, 2.732, 0.83, 0.0, 0.0, 0.0, 0.0)
        self.Pyrophoric = (5.755, 0.96, 70.03, 0.89, 188.6, 0.92, 269.4,
                           0.92, 2.035, 0.66, 1.609, 0.76, 151, 0.63, 2.847, 0.54)
        self.Styrene = (12.76, 0.963, 66.01, 0.883, 261.9, 0.937, 56,
                        0.268, 2.889, 0.686, 0.027, 0.935, 83.68, 0.713, 0.273, 0.935)

    def get_data(self):
        if (self.fluid == "Aromatics"):
            return self.Aromatics
        if (self.fluid == "C1-C2"):
            return self.C1_To_C2
        if (self.fluid == "C13-C16"):
            return self.C13_To_C16
        if (self.fluid == "C17-C25"):
            return self.C17_To_C25
        if (self.fluid == "C25+"):
            return self.C25_plus
        if (self.fluid == "C3-C4"):
            return self.C3_To_C4
        if (self.fluid == "C5"):
            return self.C5
        if (self.fluid == "C6-C8"):
            return self.C6_To_C8
        if (self.fluid == "C9-C12"):
            return self.C9_To_C12
        if (self.fluid == "CO"):
            return self.CO
        if (self.fluid == "DEE"):
            return self.DEE
        if (self.fluid == "EE"):
            return self.EE
        if (self.fluid == "EEA"):
            return self.EEA
        if (self.fluid == "EG"):
            return self.EG
        if (self.fluid == "EO"):
            return self.EO
        if (self.fluid == "H2"):
            return self.H2
        if (self.fluid == "H2S"):
            return self.H2S
        if (self.fluid == "HF"):
            return self.HF
        if (self.fluid == "Methanol"):
            return self.Methanol
        if (self.fluid == "PO"):
            return self.PO
        if (self.fluid == "Pyrophoric"):
            return self.Pyrophoric
        if (self.fluid == "Styrene"):
            return self.Styrene


class Table71:
    def __init__(self, fluid):
        self.fluid = fluid
        self.Crude_Oil = ('C17_To_C25', 280.0, 775.019, 0.0369)
        self.Fuel_Oil = ('C17_To_C25', 280.0, 775.019, 0.0369)
        self.Gasonline = ('C6_To_C8', 100.0, 684.018, 0.00401)
        self.Heavy_Crude_Oil = ('C25_plus', 422.0, 900.026, 0.046)
        self.Heavy_Diesel_Oil = ('C13_To_C16', 205.0, 764.527, 0.00246)
        self.Heavy_Fuel_Oil = ('C25_plus', 422.0, 900.026, 0.046)
        self.Light_Diesel_Oil = ('C9_To_C12', 149.0, 734.011, 0.00104)

    def get_data(self):
        if (self.fluid == "Crude Oil"):
            return self.Crude_Oil
        if (self.fluid == "Fuel Oil"):
            return self.Fuel_Oil
        if (self.fluid == "Gason line"):
            return self.Gasonline
        if (self.fluid == "Heavy Crude Oil"):
            return self.Heavy_Crude_Oil
        if (self.fluid == "Heavy Diesel Oil"):
            return self.Heavy_Diesel_Oil
        if (self.fluid == "Heavy Fuel Oil"):
            return self.Heavy_Fuel_Oil
        if (self.fluid == "Light Diesel Oil"):
            return self.Light_Diesel_Oil


class Table64:
    Table_Years_Since_Last_Inspection = {
        1.0: [0.3, 0.5, 9.0, 3.0, 0.01, 1.0],
        2.0: [0.5, 1.0, 40.0, 4.0, 0.03, 1.0],
        3.0: [0.7, 2.0, 146.0, 6.0, 0.05, 1.0],
        4.0: [1.0, 4.0, 428.0, 7.0, 0.15, 1.0],
        5.0: [1.0, 9.0, 1017.0, 9.0, 1.0, 1.0],
        6.0: [2.0, 16.0, 1978.0, 11.0, 1.0, 1.0],
        7.0: [3.0, 30.0, 3000.0, 13.0, 1.0, 2.0],
        8.0: [4.0, 53.0, 3000.0, 16.0, 1.0, 3.0],
        9.0: [6.0, 89.0, 3000.0, 20.0, 2.0, 7.0],
        10.0: [9.0, 146.0, 3000.0, 25.0, 3.0, 13.0],
        11.0: [12.0, 230.0, 3000.0, 30.0, 4.0, 26.0],
        12.0: [16.0, 351.0, 3000.0, 36.0, 5.0, 47.0],
        13.0: [22.0, 518.0, 3000.0, 44.0, 7.0, 82.0],
        14.0: [30.0, 738.0, 3000.0, 53.0, 9.0, 139.0],
        15.0: [40.0, 1017.0, 3000.0, 63.0, 11.0, 228.0],
        16.0: [53.0, 1358.0, 3000.0, 75.0, 15.0, 359.0],
        17.0: [69.0, 1758.0, 3000.0, 89.0, 19.0, 548.0],
        18.0: [89.0, 2209.0, 3000.0, 105.0, 25.0, 808.0],
        19.0: [115.0, 2697.0, 3000.0, 124.0, 31.0, 1151.0],
        20.0: [146.0, 3000.0, 3000.0, 146.0, 40.0, 1587.0],
        21.0: [184.0, 3000.0, 3000.0, 170.0, 50.0, 2119.0],
        22.0: [230.0, 3000.0, 3000.0, 199.0, 63.0, 2743.0],
        23.0: [286.0, 3000.0, 3000.0, 230.0, 78.0, 3000.0],
        24.0: [351.0, 3000.0, 3000.0, 266.0, 97.0, 3000.0],
        25.0: [428.0, 3000.0, 3000.0, 306.0, 119.0, 3000.0]}


class Table65:
    Table_Year_In_Service = {
        1.0: [30, 1, 0.1],
        2.0: [89, 4, 0.13],
        3.0: [230, 16, 0.15],
        4.0: [518, 53, 0.17],
        5.0: [1017, 146, 0.2],
        6.0: [1758, 351, 1],
        7.0: [2697, 738, 4],
        8.0: [3000, 1358, 16],
        9.0: [3000, 2209, 53],
        10.0: [3000, 3000, 146],
        11.0: [3000, 3000, 351],
        12.0: [3000, 3000, 738],
        13.0: [3000, 3000, 1358],
        14.0: [3000, 3000, 2209],
        15.0: [3000, 3000, 3000],
        16.0: [3000, 3000, 3000],
        17.0: [3000, 3000, 3000],
        18.0: [3000, 3000, 3000],
        19.0: [3000, 3000, 3000],
        20.0: [3000, 3000, 3000],
        21.0: [3000, 3000, 3000],
        22.0: [3000, 3000, 3000],
        23.0: [3000, 3000, 3000],
        24.0: [3000, 3000, 3000],
        25.0: [3000, 3000, 3000]}


class Table213:
    Table_Component_Thickness = {
        0.25: [18, -20, -55, -55],
        0.3125: [18, -20, -55, -55],
        0.375: [18, -20, -55, -55],
        0.4375: [24.2, -14, -40.5, -55],
        0.5: [31.6, -6.9, -32.2, -55],
        0.5625: [38.2, -0.6, -27.2, -51],
        0.625: [44, 5.2, -22.8, -47.5],
        0.6875: [49.2, 10.4, -18.7, -44.2],
        0.75: [53.9, 15.1, -15, -41.1],
        0.8125: [58.2, 19.5, -11.6, -38.1],
        0.875: [62.1, 23.5, -8.6, -35.3],
        0.9375: [65.6, 27.2, -5.7, -32.7],
        1.0: [68.9, 30.6, -3.1, -30.1],
        1.0625: [71.9, 33.8, -0.7, -27.8],
        1.125: [74.6, 36.7, 1.6, -25.5],
        1.1875: [77.2, 39.4, 3.7, -23.4],
        1.25: [79.6, 42, 5.8, -21.4],
        1.3125: [81.8, 44.4, 7.7, -19.5],
        1.375: [83.8, 46.6, 9.6, -17.6],
        1.4375: [85.8, 48.7, 11.4, -15.9],
        1.5: [87.6, 50.7, 13.1, -14.3],
        1.5625: [89.2, 52.5, 14.8, -12.7],
        1.625: [90.8, 54.3, 16.4, -11.2],
        1.6875: [92.3, 55.9, 17.9, -9.8],
        1.75: [93.7, 57.5, 19.4, -8.5],
        1.8125: [95.1, 58.9, 20.9, -7.2],
        1.875: [96.3, 60.3, 22.3, -5.9],
        1.9375: [97.5, 61.7, 23.7, -4.7],
        2.0: [98.6, 63, 25, -3.6],
        2.0625: [99.7, 64.2, 26.3, -2.5],
        2.125: [100.7, 65.3, 27.5, -1.4],
        2.1875: [101.7, 66.4, 28.7, -0.4],
        2.25: [102.6, 67.5, 29.9, 0.6],
        2.3125: [103.5, 68.5, 31, 1.6],
        2.375: [104.3, 69.5, 32.1, 2.5],
        2.4375: [105.1, 70.5, 33.2, 3.4],
        2.5: [105.8, 71.4, 34.3, 4.3],
        2.5625: [106.5, 72.3, 35.3, 5.2],
        2.625: [107.2, 73.2, 36.3, 6],
        2.6875: [107.9, 74, 37.2, 6.9],
        2.75: [108.5, 74.8, 38.2, 7.7],
        2.8125: [109.1, 75.6, 39.1, 8.5],
        2.875: [109.7, 76.4, 39.9, 9.3],
        2.9375: [110.2, 77.2, 40.8, 10.1],
        3.0: [110.8, 77.9, 41.7, 10.9],
        3.0625: [111.3, 78.7, 42.5, 11.7],
        3.125: [111.7, 79.4, 43.3, 12.4],
        3.1875: [112.2, 80.1, 44, 13.2],
        3.25: [112.6, 80.8, 44.8, 13.9],
        3.3125: [113.1, 81.5, 45.5, 14.7]}


class Table214:
    Table_Tmin_Tref = {
        -56.0: [4, 61, 579, 1436, 2336, 3160, 3883, 4509, 5000],
        -44.0: [3, 46, 474, 1239, 2080, 2873, 3581, 4203, 4746],
        -33.0: [2, 30, 350, 988, 1740, 2479, 3160, 3769, 4310],
        -22.0: [2, 16, 220, 697, 1317, 1969, 2596, 3176, 3703],
        -11.0: [1.2, 7, 109, 405, 850, 1366, 1897, 2415, 2903],
        0.0: [0.9, 3, 39, 175, 424, 759, 1142, 1545, 1950],
        11.0: [0.1, 1.3, 10, 49, 143, 296, 500, 741, 1008],
        22.0: [0, 0.7, 2, 9, 29, 69, 133, 224, 338],
        33.0: [0, 0, 1, 2, 4, 9, 19, 36, 60],
        44.0: [0, 0, 0, 0.8, 1.1, 2, 2, 4, 6],
        56.0: [0, 0, 0, 0, 0, 0, 0.9, 1.1, 1.2]}


class Table215:
    Table_Tmin_Tref = {
        -56.0: [0, 1.3, 9, 46, 133, 277, 472, 704, 962],
        -44.0: [0, 1.2, 7, 34, 102, 219, 382, 582, 810],
        -33.0: [0, 1.1, 5, 22, 68, 153, 277, 436, 623],
        -22.0: [0, 0.9, 3, 12, 38, 90, 171, 281, 416],
        -11.0: [0, 0.4, 2, 5, 17, 41, 83, 144, 224],
        0.0: [0, 0, 1.1, 2, 6, 14, 29, 53, 88],
        11.0: [0, 0, 0.6, 1.2, 2, 4, 7, 13, 23],
        22.0: [0, 0, 0, 0.5, 1.1, 1.3, 2, 3, 4],
        33.0: [0, 0, 0, 0, 0, 0.5, 0.9, 1.1, 1.3],
        44.0: [0, 0, 0, 0, 0, 0, 0, 0, 0.2],
        56.0: [0, 0, 0, 0, 0, 0, 0, 0, 0]}


class Table3b21:
    Table_conversionFactory = {
        1.0: [31623, 12],
        2.0: [1000, 1],
        3.0: [4536, 10000],
        4.0: [2.205, 1],
        5.0: [25.2, 55.6],
        6.0: [55.6, 100],
        7.0: [1, 10.763],
        8.0: [0.0929, 1],
        9.0: [0.123, 0.6],
        10.0: [9.744, 63.32],
        11.0: [0.145, 1],
        12.0: [1.8, 1],
        13.0: [6.29, 0.178],
        14.0: [1, 3600],
        15.0: [4.685, 1],
        16.0: [30.89, 70],
        17.0: [0.001481, 0.00723],
        18.0: [0.005, 0.0164],
        19.0: [1.085, 1.015],
        20.0: [1.013, 0.147],
        21.0: [5328, 9590],
        22.0: [5.8, 14.62],
        23.0: [0.45, 0.346],
        24.0: [2.6, 2.279],
        25.0: [0.0296, 0.0438],
        26.0: [100, 14.5],
        27.0: [1, 0.3967],
        28.0: [1000, 6895],
        29.0: [0.00043, 0.000185],
        30.0: [0.0000000976, 0.000000643],
        31.0: [864, 7200],
        32.0: [0.543, 107],
        33.0: [0.0815, 16.03],
        34.0: [86.4, 183000],
        35.0: [2.382, 0.0259],
        36.0: [30.5, 100],
        37.0: [0.00000001408, 0.00006995],
        38.0: [1.1341, 403.95],
        39.0: [3.9365, 7.2622],
        40.0: [5.9352, 5.0489],
        41.0: [32, 0]}


class Table511:
    Table_art = {
        0.00: [0, 1, 0, 0, 0, 0],
        0.05: [4, 1, 1, 1, 0, 0],
        0.01: [14, 1, 3, 1, 1, 1],
        0.15: [32, 1, 8, 2, 1, 1],
        0.20: [56, 1, 18, 6, 2, 1],
        0.25: [87, 1, 32, 11, 4, 3],
        0.30: [125, 1, 53, 21, 9, 6],
        0.35: [170, 1, 80, 36, 16, 12],
        0.40: [222, 1, 115, 57, 29, 21],
        0.45: [281, 1, 158, 86, 47, 36],
        0.50: [347, 1, 211, 124, 73, 58],
        0.55: [420, 1, 273, 173, 109, 89],
        0.60: [500, 1, 346, 234, 158, 133],
        0.65: [587, 1, 430, 309, 222, 192],
        0.70: [681, 1, 527, 401, 305, 270],
        0.75: [782, 1, 635, 510, 409, 370],
        0.80: [890, 1, 757, 638, 538, 498],
        0.85: [1005, 1, 893, 789, 698, 658],
        0.90: [1128, 1, 1044, 963, 888, 856],
        0.95: [1255, 1, 1209, 1163, 1118, 1098],
        1.00: [1390, 1, 1390, 1390, 1390, 1390]}


class Table512:
    Table_art = {
        0.05: [4, 1, 1, 0.5, 0.4, 0.4],
        0.10: [14, 1, 3, 1, 0.7, 0.7],
        0.15: [32, 1, 8, 2, 1, 1],
        0.20: [56, 1, 18, 6, 2, 1],
        0.25: [87, 1, 32, 11, 4, 3],
        0.30: [125, 1, 53, 21, 9, 6],
        0.35: [170, 1, 80, 36, 16, 12],
        0.40: [222, 1, 115, 57, 29, 21],
        0.45: [281, 1, 158, 86, 47, 36],
        0.50: [347, 1, 211, 124, 73, 58],
        0.55: [420, 1, 273, 173, 109, 89],
        0.60: [500, 1, 346, 234, 158, 133],
        0.65: [587, 1, 430, 309, 222, 192],
        0.70: [681, 1, 527, 401, 305, 270],
        0.75: [782, 1, 635, 510, 409, 370],
        0.80: [890, 1, 757, 638, 538, 498],
        0.85: [1005, 1, 893, 789, 696, 658],
        0.90: [1126, 1, 1044, 963, 888, 856],
        0.95: [1255, 1, 1209, 1163, 1118, 1098],
        1.00: [1390, 1, 1390, 1390, 1390, 1390],
        0.00: [0.1, 1, 0.1, 0.1, 0.1, 0.1]}

def locat(DamageFactor, FinancialCost):
    data = {}
    data['x'] = 0
    data['y'] = 500

    if FinancialCost <= 10000:
        data['x'] = int(round(100+0.01 * FinancialCost,0))
    elif FinancialCost <= 100000:
        data['x'] = int(round(200 + 0.001 * FinancialCost,0))
    elif FinancialCost <= 1000000:
        data['x'] = int(round(300 + 0.0001 * FinancialCost,0))
    elif FinancialCost <= 10000000:
        data['x'] = int(round(400 + 0.00001 * FinancialCost,0))
    elif FinancialCost <= 1000000000:
        data['x'] = int(round(500 + 0.000001 * FinancialCost,0))
    else:
        data['x'] = 600

    if DamageFactor <= 2:
        data['y'] = int(round(500 - 50* DamageFactor,0))
    elif DamageFactor <= 20:
        data['y'] = int(round(400 - (100 * DamageFactor)/20,0))
    elif DamageFactor <= 100:
        data['y'] = int(round(300 - DamageFactor*1.25,0))
    elif DamageFactor <= 1000:
        data['y'] = int(round(200 - 0.1*DamageFactor,0))
    elif DamageFactor <= 10000:
        data['y'] = int(round(100- 0.01*DamageFactor,0))
    else:
        data['y'] = 0
    return data
def locatData(DamageFactor, FinancialCost):
    data = {}
    data['x'] = 0
    data['y'] = 400

    if FinancialCost <= 10000:
        data['x'] = int(round(100+0.01 * FinancialCost,0))
    elif FinancialCost <= 100000:
        data['x'] = int(round(180 + 0.001 * FinancialCost,0))
    elif FinancialCost <= 1000000:
        data['x'] = int(round(260 + 0.0001 * FinancialCost,0))
    elif FinancialCost <= 10000000:
        data['x'] = int(round(340 + 0.00001 * FinancialCost,0))
    elif FinancialCost <= 1000000000:
        data['x'] = int(round(400 + 0.000001 * FinancialCost,0))
    else:
        data['x'] = 500

    if DamageFactor <= 2:
        data['y'] = int(round(480 - 50* DamageFactor,0))
    elif DamageFactor <= 20:
        data['y'] = int(round(420 - (100 * DamageFactor)/20,0))
    elif DamageFactor <= 100:
        data['y'] = int(round(340 - DamageFactor*1.25,0))
    elif DamageFactor <= 1000:
        data['y'] = int(round(260 - 0.1*DamageFactor,0))
    elif DamageFactor <= 10000:
        data['y'] = int(round(180- 0.01*DamageFactor,0))
    else:
        data['y'] = 100
    return data
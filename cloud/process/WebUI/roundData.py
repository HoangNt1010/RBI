def roundDF(df):
    if df is None:
        return "N/A"
    else:
        return round(df, 5)
def roundPoF(pof):
    if pof is None:
        return "N/A"
    else:
        return round(pof,10)
def roundFC(fc):
    if fc is None:
        return "N/A"
    else:
        return round(fc,5)
def roundMoney(money):
    if money is None:
        return "N/A"
    else:
        return round(money,0)
def convertDF(df):
    if round(df,0)<= 2:
        return "1"
    elif round(df,0)>2 and round(df,0) <= 20:
        return "2"
    elif round(df,0)>20 and round(df,0) <= 150:
        return "3"
    elif round(df,0)>150 and round(df,0) <= 1000:
        return "4"
    else:
        return "5"
def roundMonth(month):
    return round(month,5)
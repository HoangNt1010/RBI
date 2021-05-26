import joblib
import numpy as np

'''
Tank Equipment
height = adjust height/ height
cof = adjust cof/ cof
leavedike, leavedikeremainonsite, gooffsite = 0-1
'''
def predictHeightFluid(leavedike, leavedikeremainonsite, gooffsite, cof):
    model = joblib.load('cloud/MLModelBackend/cof/fludiHeightTank.pkl')
    input = np.array([leavedike, leavedikeremainonsite, gooffsite, cof])
    result = model.predict([input])
    return result[0]/100

def predictLeaveDike(height, leavedikeremainonsite, gooffsite, cof):
    model = joblib.load('cloud/MLModelBackend/cof/rwstream_FluidLeaveDikePercent.pkl')
    input = np.array([height, leavedikeremainonsite, gooffsite, cof])
    result = model.predict([input])
    return result[0]

def predictLeaveDikeRemainOnSite(height, leavedike, gooffsite, cof):
    model = joblib.load('cloud/MLModelBackend/cof/rwstream_FluidLeaveDikereMainOnSitePercent.pkl')
    input = np.array([height, leavedike, gooffsite, cof])
    result = model.predict([input])
    return result[0]

def predictfGoOffSite(height, leavedike, leavedikeremainonsite, cof): 
    model = joblib.load('cloud/MLModelBackend/cof/rwstream_FluidGoOffSitePercent.pkl')
    input = np.array([height, leavedike, leavedikeremainonsite, cof])
    result = model.predict([input])
    return result[0]

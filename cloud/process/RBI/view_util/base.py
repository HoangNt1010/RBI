from django.db.models import Q
from itertools import count
from cloud import models


def GetStatus(request, proposalID):
    noti = models.ZNotification.objects.all().filter(id_user=request.session['id'])
    countnoti = noti.filter(state=0).count()
    count = models.Emailto.objects.filter(Q(Emailt=models.ZUser.objects.filter(id=request.session['id'])[0].email), Q(Is_see=0)).count()
    rwAssessment = models.RwAssessment.objects.get(id=proposalID) 
    return noti, countnoti, count, rwAssessment
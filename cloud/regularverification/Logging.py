import os,sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()

from django.utils import timezone
import pytz

import glob
import logging
import logging.handlers

# You'll need these imports in your own code
import multiprocessing

# Next two import lines for this demo only
from random import choice, random
import time
from django.http import Http404,HttpResponse
from cloud import models
from datetime import datetime
import threading
import time
import json
import requests

def Logging():
    try:
        zsensor = models.ZSensor.objects.all()
        print(zsensor.count())
        for a in zsensor:
            ACCESS_TOKEN = a.Token
            print(a.Token)
            headers = {
                'Content-Type': 'application/json',
                'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlbmwubGFiNDExQGdtYWlsLmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiNzlkYjhhZTAtNmEyNy0xMWU4LTk2NjUtMTMyMDYzOTIxYjExIiwiZmlyc3ROYW1lIjoibGFiIiwibGFzdE5hbWUiOiI0MTEiLCJlbmFibGVkIjp0cnVlLCJwcml2YWN5UG9saWN5QWNjZXB0ZWQiOnRydWUsImlzUHVibGljIjpmYWxzZSwidGVuYW50SWQiOiI3OWQ2MGNhMC02YTI3LTExZTgtOTY2NS0xMzIwNjM5MjFiMTEiLCJjdXN0b21lcklkIjoiMTM4MTQwMDAtMWRkMi0xMWIyLTgwODAtODA4MDgwODA4MDgwIiwiaXNzIjoidGhpbmdzYm9hcmQuaW8iLCJpYXQiOjE2MDkxNDE0MjUsImV4cCI6MTYxMDk0MTQyNX0.jlPZRnZD5OczsiQyQHIY6bsCVVGbnBO__S68A5sUdeq75MmJ1FbSSe_NqgDaX9pOOx4dzbnTe_dniG7PIK2Esg',
            }
            response = requests.get(
                'http://demo.thingsboard.io/api/plugins/telemetry/DEVICE/' + ACCESS_TOKEN + '/values/timeseries?keys=',
                headers=headers)
            # print(response.json())
            datajson = response.json()
            # string = str(
            #     'Humidity, ' + datajson['humidity'][0]['value'] + ', Flow rate, ' + datajson['flow_rate'][0][
            #         'value'] + ', Temperature, ' + datajson['temparature'][0][
            #         'value'] + ', Dust, ' + datajson['Dust'][0][
            #         'value'] + ', Equipment Volume, ' + datajson['equipment_volume'][0][
            #         'value'] + ', Max Operating Temperature, ' + datajson['max.operating_temperature'][0][
            #         'value'] + ', Distance to ground water, ' + datajson['distance_to_ground_water'][0][
            #         'value'] + ', Current Thickness, ' + datajson['current_thickness'][0][
            #         'value'] + ', Minimum Operating Temperature, ' + datajson['min.operating_temperature'][0][
            #         'value'] + ', Critical Exposure Temperature, ' +
            #     datajson['critical_exposure_temperature'][0]['value'] + ', pH of Water, ' +
            #     datajson['ph_of_water'][0]['value'] + ', Interface at Soil or Water, ' +
            #     datajson['interface_at_soil_or_water'][0][
            #         'value'] + ', Max Operating Pressure, ' + datajson['max.operating_pressure'][0][
            #         'value'] + ', Operating Hydrogen Partial Pressure, ' +
            #     datajson['operating_hydrogen_partial_pressure'][0]['value'] + ', Min Operating Pressure, ' +
            #     datajson['min.operating_pressure'][0][
            #         'value'] + ', Current Corrosion Rate, ' +
            #     datajson['current_corrosion-rate'][0]['value'] + ', Min.Required Thickness, ' +
            #     datajson['min.required_thickness'][0]['value'] + ', NaOH Concentration, ' +
            #     datajson['naoh_concentration'][0]['value'] + ', Fluid Height, ' + datajson['fluid_height'][0][
            #         'value'] + ', H2S Content in Water, ' + datajson['h2s_content_in_water'][0][
            #         'value'] + ', Presence of Crack, ' + datajson['presence_of_crack'][0][
            #         'value'] + ', Cladding Thickness, ' + datajson['cladding_thinkness'][0][
            #         'value'] + ', External Coating, ' + datajson['external_coating'][0][
            #         'value'] + ', Internal Coating, ' + datajson['internal_coating'][0][
            #         'value'] + ', Environment Contains H2S, ' + datajson['environment_contains_H2S'][0][
            #         'value'] + ', Steam, ' + datajson['steamed_out_prior_to_water_flushing'][0][
            #         'value'] + ', Exposeed to Acid, ' + datajson['exposed_to_acid_gas_treating_amine'][0][
            #         'value'] + ', Internal Cladding, ' + datajson['internal_cladding'][0]['value'])
            # print(string)
            print(datajson)
            LOG_FILENAME = 'logging_rotatingfile_RBI1.log'

            # Set up a specific logger with our desired output level
            # print(request.session['id'])
            # UserID = models.Sites.objects.filter(userID_id=request.session['id'])[0].userID_id
            # UserID = "user1"
            # print("check site")
            # print(UserID)
            # Name = models.ZUser.objects.get(id=UserID).username
            # Name = "Cuong"
            my_logger = logging.getLogger(ACCESS_TOKEN)
            my_logger.setLevel(logging.DEBUG)

            # Add the log message handler to the logger
            handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=52428800,
                                                           backupCount=5)  # 50 MB = 52 428 800 bytes
            f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
            handler.setFormatter(f)
            my_logger.addHandler(handler)
            # Mess = "cuong"
            # Log some messages
            # for i in range(10):
            my_logger.info('%s' % datajson)

            # See what files are created
            logfiles = glob.glob('%s*' % LOG_FILENAME)

            for filename in logfiles:
                print(filename)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def worker(arg):
    while not arg['stop']:
        logging.debug('Hi from myfunc')
        time.sleep(0.5)

def main():
    logging.basicConfig(level=logging.DEBUG,filename='runtime.log', format='%(relativeCreated)6d %(threadName)s %(message)s')
    info = {'stop': False}
    thread = threading.Thread(target=worker, args=(info,))
    thread.start()
    while True:
        try:
            logging.debug('Hello from main')
            time.sleep(0.75)
        except KeyboardInterrupt:
            info['stop'] = True
            break
    thread.join()

if __name__ == "__main__":
    main()

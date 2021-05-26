#!/usr/bin/env python
import os
import sys
import threading
from cloud.regularverification.regular import REGULAR
from cloud.regularverification import subscribe
from cloud.regularverification import subscribe_thingsboard
import time
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RbiCloud.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    execute_from_command_line(sys.argv)

def RegularVerification():
    # obj = REGULAR()
    # obj.regular_1()
    i=1
    while 1:
        print(i)
        i=i+1
        time.sleep(10)

if __name__ == "__main__":
    # t2 = threading.Thread(target=main)
    # t2.setDaemon(True)
    # t2.start()
    #
    # t1 = threading.Thread(target=RegularVerification)
    # t1.setDaemon(True)
    # t1.start()
    # t1.join()
    main()

    # t2 = threading.Thread(target=subscribe.SubDATA)
    # t2.setDaemon(True)
    # t2.start()
    # t3 = threading.Thread(target=subscribe_thingsboard.SubDATA)
    # t3.setDaemon(True)
    # t3.start()
    # t3.join()
    # t4 = threading.Thread(target=main)
    # t4.setDaemon(True)
    # t4.start()
    # subscribe_thingsboard.SubDATA()
    # t4.join()

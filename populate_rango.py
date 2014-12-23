import datetime
import os

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dancestudio.settings')
django.setup()


def populate():
    print 'hello populate'
    d1 =  datetime.datetime.strptime('2014-12-21', "%Y-%m-%d")
    d2 = datetime.datetime.strptime('2014-12-28', "%Y-%m-%d")
    
    e1 = datetime.datetime.strptime('2014-12-18', "%Y-%m-%d")
    e2 = datetime.datetime.strptime('2014-12-28', "%Y-%m-%d") 
    for x in range(0, 10):
        print x
        if (d1.date <= e1.date and d2.date > e1.date and d2.date <= e2.date):
                    print("Partial collapse left side")
                # CASE 2: if paramstartdate greater or equal to event startdate  
        elif (d1.date >= e1.date and d2.date <= e2 ):
                    print("Fully collapse or contain within event start-end period")
        elif(d1.date >= e1.date and  d2 .date>= e2.date):
                    print("Partially collapse right side")


# Start execution here!
if __name__ == '__main__':
    print "Starting sway population script..."
    populate()
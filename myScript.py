import datetime
from datetime import datetime as dt
from datetime import timedelta

script_version = "1.0.4"
last_mod_date = "26/04/2022"
pay_day = 5
ipo_day = 10
ipo_val = 533
expec_val = 1000

def getDelta(dtToday):
	year 	= dtToday.year
	mounth 	= dtToday.month
	next_pay_day = datetime.date(year, mounth, pay_day)
	if (dtToday.day < pay_day):		
		return (next_pay_day - dtToday.date()).days
	
	if (mounth == 12):
		year = year +1
		mounth = 1
	else:
		mounth = mounth +1
		
	next_pay_day = datetime.date(year, mounth, pay_day)
	return (next_pay_day - dtToday.date()).days

print("Script version is", script_version)
today = dt.today()  # get date today
print (today)
#today.year=2019
#today.mounth=12
#today.day=1
#today = datetime.date.fromisoformat('2019-12-04')

print("Today is", today.strftime("%d/%m/%Y"))
delta = getDelta(today)
print("Days before next pay:", delta)
print("Enter ammount:")
ammount = int(input())
leftOver = ammount - expec_val;
if (today.day < ipo_day):
   leftOver = leftOver - ipo_val	
print("Left ofer:", leftOver)
print (leftOver/delta)

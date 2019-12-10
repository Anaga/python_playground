import datetime

script_version = "1.0.2"
last_mod_date = "10/12/2019"
pay_day = 24
ipo_day = 10
ipo_val = 533
expec_val = 1500

print("script version is", script_version)
today = datetime.date.today()
#today = datetime.date.fromisoformat('2019-12-04')

print("Today is", today.strftime("%d/%m/%Y"))
next_mounth = today.month + 1;
year = today.year
if (next_mounth == 13):
    next_mounth = 1
    year = today.year +1

next_month_begin = datetime.date(year, next_mounth, 1)
delta = (next_month_begin - today).days
print("Days before next month:", delta)
print("Enter ammount:")
ammount = int(input())
print (ammount/delta)

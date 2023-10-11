"script to caclulate expected spends and availble day money"
import datetime
from datetime import datetime as dt

script_version = "1.0.15"
last_mod_date = "11/10/2023"

# Switch to new job - pay day is 5
pay_day = 4
expec_val = 3000

# 6271516 SEB laenukaitse kindlustuse maksekorraldus -45,89
# last change 10.05.2023: -46.91
# last change 10.08.2023: -49.09
# last change 11.09.2023: -50,62
# last change 11.09.2023: -45,83
ipo_insurense = {"day": 11, "ammount": 45.83}


# seb liising
# 102895391 Arve nr A22214516 tasumine -455,26
# last change 10.03.2023: -481.73
# last change 11.09.2023: -488.03
lising = {"day": 11, "ammount": 488.03}

# Lep. 2019009655/intress/L190006408 -220,43
# EURIBOR 2.316% 
# Now percent is 4.216%
# old percent ipo_intress = {"day": 10, "ammount": 220.43}
# last change 10.05.2023: -462.65
# 10.07.2023 - EURIBOR 3.605% 
#       Now percent is 5.505%
# last change 10.07.2023: -562.24
# 10.08.2023 - EURIBOR 3.9640% 
#       Now percent is 5.505%
# last change 10.08.2023: -621.36
# last change 11.09.2023: -640.54
# last change 11.10.2023: -579,79
ipo_intress = {"day": 11, "ammount": 579.79}

# Lep. 2019009655/põhiosa/L190006408 -312,03
# old ipo_pohiosa = {"day": 10, "ammount": 312.03}
# last change 10.05.2023: -235.22
# last change 10.07.2023: -236.54
# last change 10.08.2023: -177.42
# last change 11.09.2023: -158.24
# last change 11.10.2023: -218,99
ipo_pohiosa = {"day": 11, "ammount": 218.99}


# car insurense
# as LHV kindlustus
car_insurense = {"day": 16, "ammount": 43.46}

life_insurence = {"day": 18, "ammount": 200}   #

#expens_array = [ipo_insurense, ipo_intress, ipo_pohiosa, lising, life_insurence, car_insurense]
expens_array = [ipo_insurense, ipo_intress, ipo_pohiosa, lising, car_insurense]
#expens_array = [ipo_intress, ipo_pohiosa, lising, life_insurence]

def getDelta(dtToday, pay_day):
    "function to calculte days count between today and pay day"
    year = dtToday.year
    mounth = dtToday.month
    next_pay_day = datetime.date(year, mounth, pay_day)
    if (dtToday.day < pay_day):
        return (next_pay_day - dtToday.date()).days

    if (mounth == 12):
        year = year + 1
        mounth = 1
    else:
        mounth = mounth + 1

    next_pay_day = datetime.date(year, mounth, pay_day)
    return (next_pay_day - dtToday.date()).days


def future_spend(expens_array, pay_day, today):
    "function to calculate how much many will be spend on all expected expenses."
    future_spends = 0.0

    for exp in expens_array:
        cur_day = exp.get("day")
        first_half = cur_day < pay_day
        futurs_pay = cur_day > today

        if today < pay_day:  # first falf of mounth, expected expens is from today till pay_day
            if first_half and futurs_pay:
                future_spends += exp.get("ammount")

        if today >= pay_day:  # last falf of mounth, expected expens is from today till pay_day in next mounth
            if first_half or futurs_pay:
                future_spends += exp.get("ammount")

    return future_spends


print(F"Script version is {script_version}")
today = dt.today()  # get date today

date = today.strftime("%d/%m/%Y")
print(F"Today is {date}")

print("Enter ammount:")
ammount = int(input())

will_spend = future_spend(expens_array, pay_day, (today.day))
print(F"Will spend: {will_spend:.2f}")
leftOver = ammount - will_spend - expec_val

delta = getDelta(today, pay_day)
print(F"Days before next pay: {delta}")
print(F"Left over: {leftOver:.2f}")
print(F"You can spend {(leftOver/delta):.2f} per day")

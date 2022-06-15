import datetime
from datetime import datetime as dt
from datetime import timedelta

script_version = "1.0.6"
last_mod_date = "10/06/2022"

pay_day = 15

# 6271516 SEB laenukaitse kindlustuse maksekorraldus -45,89
ipo_insurense = {"day": 10, "ammount": 45.89, "is_paid": False}

# Lep. 2019009655/intress/L190006408 -220,43
ipo_intress = {"day": 10, "ammount": 220.43, "is_paid": False}

# Lep. 2019009655/põhiosa/L190006408 -312,03
ipo_pohiosa = {"day": 10, "ammount": 312.03, "is_paid": False}

# 102895391 Arve nr A22214516 tasumine -455,26
lising = {"day": 10, "ammount": 455.26, "is_paid": False}

life_insurence = {"day": 26, "ammount": 50, "is_paid": False}   #

expens_array = [ipo_insurense, ipo_intress,
                ipo_pohiosa, lising, life_insurence]


ipo_day = 10
ipo_val = 1000
expec_val = 1000

def getDelta(dtToday):
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
        cur_amm = exp.get("ammount")

        if today < pay_day:  # first falf of mounth, expected expens is from today till pay_day
            if cur_day >= today and cur_day < pay_day:
                future_spends += cur_amm

        if today == pay_day:  # salary day, expected expens is only today
            if cur_day == today:
                future_spends += cur_amm

        if today > pay_day:  # last falf of mounth, expected expens is from today till pay_day in next mounth
            if cur_day >= pay_day and cur_day > today:
                future_spends += cur_amm

    return future_spends


print(F"Script version is {script_version}")
today = dt.today()  # get date today
date = today.strftime("%d/%m/%Y")
print(F"Today is {date}")


print("Enter ammount:")
ammount = int(input())
will_spend = future_spend(expens_array, pay_day, today.day)
print(F"will spend: {will_spend}")
leftOver = ammount - will_spend - expec_val

delta = getDelta(today)
print(F"Days before next pay: {delta}")
print(F"Left over: {leftOver}")
print(leftOver/delta)

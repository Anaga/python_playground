"script to caclulate expected spends and availble day money"
import datetime
from datetime import datetime as dt

script_version = "1.0.7"
last_mod_date = "11/08/2022"

pay_day = 15
expec_val = 1500

# 6271516 SEB laenukaitse kindlustuse maksekorraldus -45,89
ipo_insurense = {"day": 10, "ammount": 45.89}

# Lep. 2019009655/intress/L190006408 -220,43
ipo_intress = {"day": 10, "ammount": 220.43}

# Lep. 2019009655/põhiosa/L190006408 -312,03
ipo_pohiosa = {"day": 10, "ammount": 312.03}

# 102895391 Arve nr A22214516 tasumine -455,26
lising = {"day": 10, "ammount": 455.26}

life_insurence = {"day": 26, "ammount": 50}   #

expens_array = [ipo_insurense, ipo_intress,
                ipo_pohiosa, lising, life_insurence]

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

will_spend = future_spend(expens_array, pay_day, today.day)
print(F"Will spend: {will_spend:.2f}")
leftOver = ammount - will_spend - expec_val

delta = getDelta(today, pay_day)
print(F"Days before next pay: {delta}")
print(F"Left over: {leftOver:.2f}")
print(F"You can spend {(leftOver/delta):.2f} per day")

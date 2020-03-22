import serial
import time

# version: 1.00
# date : 22.03.2020

NOM_VOLT  = 42.0
NOM_AMPER = 20.0
PER_CENT  = 0x6400

STATUS_QUERY_ACTUAL  = [0x75, 0x00, 0x47]
STATUS_QUERY_SETTING = [0x75, 0x00, 0x48]

REMOUTE_MODE_ACTIVATE   = [0xF1, 0x00, 0x36, 0x10, 0x10] 
REMOUTE_MODE_DEACTIVATE = [0xF1, 0x00, 0x36, 0x10, 0x00] 

POWER_OUTPUT_ON   = [0xF1, 0x00, 0x36, 0x01, 0x01] 
POWER_OUTPUT_OFF  = [0xF1, 0x00, 0x36, 0x01, 0x00] 

#12.05V = 0x1C, 0x95
SET_VOLTAGE_VAL = [0xF1, 0x00, 0x32, 0x1C, 0x95] 
#8.5V = 0x14, 0x40
#SET_VOLTAGE_VAL = [0xF1, 0x00, 0x32, 0x14, 0x40] 
SET_VOLTAGE = [0xF1, 0x00, 0x32] 

#1.33A= 0x06, 0xA8
SET_CURRENT_VAL = [0xF1, 0x00, 0x33, 0x06, 0xA8] 

def add_check_summ(bytes: list) -> list:
    summ = 0
    arr_head = list()
    arr_tail = list()
    for byte in bytes:
        summ+=byte
        arr_head.append(byte)
    b0 =(int) (summ / 256)
    b1 =(int) (summ % 256)
    arr_tail.append(b0)
    arr_tail.append(b1)
    arr = arr_head + arr_tail
    return (arr)
    
def get_real_value(two_byte_val: bytearray, NOM_val: float) -> float:
    percent_val = two_byte_val[0]*256 + two_byte_val[1]
    return ((NOM_val * percent_val)/PER_CENT)

def get_percent_value(real_val: float, NOM_val: float) -> list: 
    if real_val<0.0: return [0x00, 0x00] 
    if real_val>NOM_val: return [0x64, 0x00] 
    percent_val = (int)((PER_CENT * real_val) / NOM_val)
    b0 =(int) (percent_val / 256)
    b1 =(int) (percent_val % 256)
    arr = [b0, b1]
    return arr

def config_port(serial_obj, port_name: str):
    serial_obj.baudrate = 115200
    serial_obj.port = port_name
    serial_obj.parity = serial.PARITY_ODD
    serial_obj.stopbits = serial.STOPBITS_ONE 
    serial_obj.timeout = 0.25 # 1/4 sec after last char is recived
    return serial_obj

def show_status(serial_obj):
    bytes_data = bytearray(add_check_summ(STATUS_QUERY_ACTUAL))
    bytes_to_send = ' '.join(format(x, '02X') for x in bytes_data)
    print(bytes_to_send)
    serial_obj.write(bytes_data)
    res_data = serial_obj.read(11) 
    res = ' '.join(format(x, '02X') for x in res_data)
    print(res)
    if len(res_data) < 11: return ('EE FF', 0.0, 0.0)
    stat= res_data[3:5]
    vol = res_data[5:7]
    cur = res_data[7:9]
    
    status = ' '.join(format(x, '02X') for x in stat)
    act_val = get_real_value(vol, NOM_VOLT)
    act_cur = get_real_value(cur, NOM_AMPER)    
    print("Status: %s, %02.3fV, %02.3fA"%(status, act_val, act_cur))
    return (status, act_val, act_cur)
    
def set_remoute_mode(serial_obj, on_off: bool):
    command = []
    if (on_off) : command = REMOUTE_MODE_ACTIVATE
    else        : command = REMOUTE_MODE_DEACTIVATE
    bytes_data = bytearray(add_check_summ(command))
    serial_obj.write(bytes_data)
    res_data = ser.read(16) 
    res = ' '.join(format(x, '02X') for x in res_data)
    print(res)

def set_voltage(serial_obj, voltage: float):
    status = show_status(serial_obj)
    rem_mod = status[0][1]
    if (rem_mod == '0') : set_remoute_mode(serial_obj, True)
    command_head = list(SET_VOLTAGE)
    command_tail = list(get_percent_value(voltage, NOM_VOLT))
    command = command_head + command_tail
    bytes_data = bytearray(add_check_summ(command))
    serial_obj.write(bytes_data)
    res_data = ser.read(16) 
    res = ' '.join(format(x, '02X') for x in res_data)
    print(res)

def set_outut(serial_obj, on_off: bool):
    status = show_status(serial_obj)
    rem_mod = status[0][1]
    if (rem_mod == '0') : set_remoute_mode(serial_obj, True)
    command = []
    if (on_off) : command = POWER_OUTPUT_ON
    else        : command = POWER_OUTPUT_OFF
    bytes_data = bytearray(add_check_summ(command))
    serial_obj.write(bytes_data)
    res_data = ser.read(16) 
    res = ' '.join(format(x, '02X') for x in res_data)
    print(res)
    
ser = serial.Serial()    
ser = config_port(ser, 'COM6')

ser.open()
print(ser.is_open)

show_status(ser)

set_remoute_mode(ser, True)

set_voltage(ser, 12)
status = show_status(ser)
print(status)
set_outut(ser, True)
status = show_status(ser)
print(status)
time.sleep(30)
set_voltage(ser, 8.5)
status = show_status(ser)
print(status)
time.sleep(30)
show_status(ser)
set_outut(ser, False)
set_remoute_mode(ser, False)
show_status(ser)
ser.close()
print(ser.is_open)

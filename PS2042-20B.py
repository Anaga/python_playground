import serial
import time


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

def get_percent_value(real_val: float, NOM_val: float) -> bytearray: 
    if real_val<0.0: return bytearray(b'\x00\x00')
    if real_val>NOM_val: return bytearray(b'\x64\x00')
    percent_val = (int)((PER_CENT * real_val) / NOM_val)
    b0 =(int) (percent_val / 256)
    b1 =(int) (percent_val % 256)
    arr = (b0, b1)   
    return bytearray(arr)

def config_port(serial_obj, port_name: str):
    serial_obj.baudrate = 115200
    serial_obj.port = port_name
    serial_obj.parity = serial.PARITY_ODD
    serial_obj.stopbits = serial.STOPBITS_ONE 
    serial_obj.timeout = 0.25 # 1/4 sec after last char is recived
    return serial_obj

def show_status(serial_obj):
    bytes_data = bytearray(add_check_summ(STATUS_QUERY_ACTUAL))
    serial_obj.write(bytes_data)
    res_data = serial_obj.read(11) 
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


ser = serial.Serial()    
ser = config_port(ser, 'COM6')

print(ser)
ser.open()
print(ser.is_open)

show_status(ser)
bytes_data = bytearray(add_check_summ(REMOUTE_MODE_ACTIVATE))
ser.write(bytes_data)
res_data = ser.read(16) 
res = ' '.join(format(x, '02X') for x in res_data)
print(res)
show_status(ser)

bytes_data = bytearray(add_check_summ(SET_VOLTAGE_VAL))
ser.write(bytes_data)
res_data = ser.read(16) 
res = ' '.join(format(x, '02X') for x in res_data)
print(res)

show_status(ser)

bytes_data = bytearray(add_check_summ(POWER_OUTPUT_ON))
ser.write(bytes_data)
res_data = ser.read(16) 
res = ' '.join(format(x, '02X') for x in res_data)
print(res)
show_status(ser)
time.sleep(1)
show_status(ser)
time.sleep(1)
show_status(ser)
time.sleep(1)

bytes_data = bytearray(add_check_summ(REMOUTE_MODE_DEACTIVATE))
res_data = ser.read(16) 
res = ' '.join(format(x, '02X') for x in res_data)
print(res)
show_status(ser)

bytes_data = bytearray(add_check_summ(REMOUTE_MODE_ACTIVATE))
ser.write(bytes_data)
res_data = ser.read(16) 
res = ' '.join(format(x, '02X') for x in res_data)
print(res)
show_status(ser)
vol_8_5 = list(SET_VOLTAGE_VAL)
#8.5V = 0x14, 0x40
vol_8_5[3]=0x14
vol_8_5[4]=0x40

bytes_data = bytearray(add_check_summ(vol_8_5))
ser.write(bytes_data)
res_data = ser.read(16) 
res = ' '.join(format(x, '02X') for x in res_data)
print(res)

show_status(ser)
ser.close()
print(ser.is_open)

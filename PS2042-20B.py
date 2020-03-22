import serial

NOM_VOLT  = 42.0
NOM_AMPER = 20.0
PER_CENT  = 0x6400

STATUS_QUERY_ACTUAL  = [0x75, 0x00, 0x47, 0x00, 0xBC]
STATUS_QUERY_SETTING = [0x75, 0x00, 0x48, 0x00, 0xBD]

REMOUTE_MODE_ACTIVATE   = [0xF1, 0x00, 0x36, 0x10, 0x10, 0X01, 0X47] 
REMOUTE_MODE_DEACTIVATE = [0xF1, 0x00, 0x36, 0x10, 0x00, 0X01, 0X37] 

POWER_OUTPUT_ON   = [0xF1, 0x00, 0x36, 0x01, 0x01, 0X01, 0X29] 
POWER_OUTPUT_OFF  = [0xF1, 0x00, 0x36, 0x01, 0x00, 0X01, 0X28] 

#12.05V = 0x1C, 0x95
SET_VOLTAGE_VAL = [0xF1, 0x00, 0x32, 0x1C, 0x95, 0X01, 0XD4] 

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
    return serial_obj

ser = serial.Serial()
    
ser = config_port(ser, 'COM5')

vol_to_set = get_percent_value(8.052, NOM_VOLT)
res = ' '.join(format(x, '02X') for x in vol_to_set) 
vol_from_dev = get_real_value(vol_to_set, NOM_VOLT)

vol_to_set = get_percent_value(12, NOM_VOLT)
res = ' '.join(format(x, '02X') for x in vol_to_set) 
vol_from_dev = get_real_value(vol_to_set, NOM_VOLT)

vol_to_set = get_percent_value(0.052, NOM_VOLT)
res = ' '.join(format(x, '02X') for x in vol_to_set) 
vol_from_dev = get_real_value(vol_to_set, NOM_VOLT)

vol_to_set = get_percent_value(-8.052, NOM_VOLT)
res = ' '.join(format(x, '02X') for x in vol_to_set) 
vol_from_dev = get_real_value(vol_to_set, NOM_VOLT)
print(vol_from_dev)

vol_to_set = get_percent_value(88.052, NOM_VOLT)
res = ' '.join(format(x, '02X') for x in vol_to_set) 
vol_from_dev = get_real_value(vol_to_set, NOM_VOLT)
print(vol_from_dev)




print(ser)
ser.open()
print(ser.is_open)

req_data = [0x75, 0x00, 0x47, 0x00, 0xBC]
data = bytearray(req_data) 

data_len = ser.write(data)

res_data = ser.read(11) 
vol = res_data[5:7]

row_val = vol[0]*256 + vol[1]
act_val = get_real_value(vol, NOM_VOLT)
act_val = (42.0 * row_val)/25600.0

print("Actual %02.3fV "%act_val)

cur = res_data[7:9]
row_cur = cur[0]*256 + cur[1]
act_cur = (20.0 * row_cur)/25600.0

act_cur = get_real_value(cur, NOM_AMPER)
print("Actual %02.3fA "%act_cur)

res = ' '.join(format(x, '02X') for x in res_data) 
resp_data_list = res.split()
status  = resp_data_list[3:5]

print("Status: %s, %02.3fV, %02.3fA"%(status, act_val, act_cur))

ser.close()
print(ser.is_open)

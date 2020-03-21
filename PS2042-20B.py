import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM6'
ser.parity = serial.PARITY_ODD
ser.stopbits = serial.STOPBITS_ONE

print(ser)
ser.open()
print(ser.is_open)

req_data = [0x75, 0x00, 0x47, 0x00, 0xBC]
data = bytearray(req_data) 

data_len = ser.write(data)

res_data = ser.read(11) 
vol = res_data[5:7]
row_val = vol[0]*256 + vol[1]
act_val = (42.0 * row_val)/25600.0

print("Actual %02.3fV "%act_val)

cur = res_data[7:9]
row_cur = cur[0]*256 + cur[1]
act_cur = (20.0 * row_cur)/25600.0

print("Actual %02.3fA "%act_cur)

res = ' '.join(format(x, '02X') for x in res_data) 
resp_data_list = res.split()
status  = resp_data_list[3:5]

print("Status: %s, %02.3fV, %02.3fA"%(status, act_val, act_cur))

ser.close()
print(ser.is_open)

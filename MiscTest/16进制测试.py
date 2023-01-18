##16进制测试
addr = 0x80700000
addr_res = addr + 11
print('0x%x'%addr_res)
print([(1)+(0<<6)+(1<<4)+(1<<2)+(100<<8)])
print(bin((1)+(0<<6)+(1<<4)+(1<<2)+(100<<8)))

for i in range(128):
    data = 1<<i
    data1 = data & 0xFFFFFFFF
    data2 = (data>>32) & 0xFFFFFFFF
    data3 = (data>>64) & 0xFFFFFFFF
    data4 = (data>>96) & 0xFFFFFFFF
    print('0x%x'%data)
print(int(628/8)*8)
print(0b11&0b1)
print((0b11>>1)&0b1)


value = [0] * 4

for addr in range(1):
    m = int(addr/32)
    n = addr - m*32
    value[m] = value[m]+(1<<n)
print("0x%x"%value[0])
data1 = value[0] & 0xFFFFFFFF
data2 = value[1] & 0xFFFFFFFF
data3 = value[2] & 0xFFFFFFFF
data4 = value[3] & 0xFFFFFFFF
print("0x%x"%data1)
print("0x%x"%data2)
print("0x%x"%data3)
print("0x%x"%data4)
print(data1)
print(data2)
print(data3)
# print(data4)
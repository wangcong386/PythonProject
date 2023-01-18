ns2m  = 0.1498527 yes
ns2lsb = 256 yes
lsb2m = ns2m/256
lsb2ns = 1/256
m2lsb = 1/lsb2m
m2ns = 1/ns2m
lsb4mm2m = 4/1000
lsb4mm2ns = lsb4mm2m*m2ns
lsb4mm2lsb = lsb4mm2m*m2lsb
adcbit2ns = 32/256
ns2adcbit = 1/adcbit2ns
adcbit2lsb = adcbit2ns*ns2lsb
m2adcbit = m2ns*ns2adcbit
adcbitslope2ns = 32/128
ns2adcbitslope = 1/adcbitslope2ns
adcbitslope2lsb = adcbitslope2ns*ns2lsb
m2adcbitslope = m2ns*ns2adcbitslope

print(m2adcbitslope)
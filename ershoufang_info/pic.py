# -*- coding:utf-8 -*-

import csv
import numpy
import matplotlib.pyplot as plt


price, size = numpy.loadtxt('house.csv', delimiter='|', usecols=(1,2),unpack=True)

print price
print size

plt.figure()
plt.subplot(211)
#plt.title("price")
plt.title("/ 10000RMB")
plt.hist(price, bins=20)

plt.subplot(212)
#plt.title("area")
plt.xlabel("/ m**2")
plt.hist(size, bins=20)

plt.figure(2)
plt.title("price")
plt.plot(price)

plt.show()

price_mean = numpy.mean(price)
size_mean = numpy.mean(size)

print "平均价格为：", price_mean
print "平均面积为:", size_mean

price_var = numpy.var(price)
size_var = numpy.var(size)

print "价格方差为：", price_var
print "面积的方差为：", size_var

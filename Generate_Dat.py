from random import randint
import pandas as pd
import csv

def Strin (i):
	if i<10:
		return '0'+str(i)
	else:
		return str(i)

class Data:
	def Rand (self):
		pass
		'''self.PID
		self.Quant
		self'''
	def Generate(self):
		Pid = randint(100,999)
		Pid1 = randint(1,12)
		Prod = chr(Pid1+64)+str(Pid)
		Quant = randint(1,6)
		Day = randint(1,28)
		month = randint(1,12)
		Year = randint(2013,2017)
		Date = Strin(Day)+'/'+Strin(month)+'/'+Strin(Year)
		Price = randint(900,2100)
		Pin = randint(411012,411047)
		DTD = randint(3,11)
		print Prod+','+str(Quant)+','+Date+','+str(Price)+','+str(Pin)+','+str(DTD)
		File = open('CustomerData1.csv','a')
		DataWriter=csv.writer(File,delimiter=',')
	#print Entry1.get()
		DataWriter.writerow([Prod,str(Quant),Date,str(Price),str(Pin),str(DTD)])
		

ProductID = ['A808','B736','B893','B1101']
Address = ['411047','411020','411033','411012','411003']
D = Data()
for i in range(300):
	D.Generate()



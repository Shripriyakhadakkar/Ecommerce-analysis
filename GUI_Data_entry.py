import Tkinter
import pandas as pd
import csv
import string
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import scipy.stats as ST
import matplotlib.axes as ax

top = Tkinter.Tk()

c1 = Tkinter.Canvas(top, bg='#E4E4E4', height=100,width=420)
c1.grid(row=0,column=0,columnspan=5,rowspan=2)
c2 = Tkinter.Canvas(top, bg='#E4E4E4', height=30,width=420)
c2.grid(row=15,column=0,columnspan=5,rowspan=1)
#S1 = c1.create_rectangle(100,100,200,200)
Text = c1.create_text(170,30,text="E-Commerce\nOnline Shopping",font=("Purisa",20),fill='blue')
Text = c1.create_text(85,85,text="(Customer Side)",font=("Purisa",15),fill='Red')
Text = c2.create_text(70,15,text="(Admin Side)",font=("Purisa",15),fill='Red')
class Date_:
	def __init__ (self, DateStr):
		self._Day = DateStr[:2]
		self._Month = DateStr[3:5]
		self._Year = DateStr[6:]
		self.DateCI = int(self._Year+self._Month+self._Day)
	def Give(self):
		return self.DateCI


def LoadCSV():
	File = open('CustomerData1.csv','a')
	DataWriter=csv.writer(File,delimiter=',')
	#print Entry1.get()
	DataWriter.writerow([Entry1.get(),Entry2.get(),Entry3.get(),Entry4.get(),Entry5.get(),Entry6.get()])
	Entry1.delete(0,Tkinter.END)
	Entry2.delete(0,Tkinter.END)
	Entry3.delete(0,Tkinter.END)
	Entry4.delete(0,Tkinter.END)
	Entry5.delete(0,Tkinter.END)
	Entry6.delete(0,Tkinter.END)
	File.close()
	return;
#####################################################################################################################################
###########               Funtion to plot bar graph for Product Popularity                  #########################################
###########                                                                                 #########################################
def ProductPopularity():
	ColN = ['ProductID', 'ProductQ','Date','Tcost','Pin','DsTD']
	File = pd.read_csv("CustomerData.csv",names=ColN)
	ProductID = list(File.ProductID)
	ProductQ = list(File.ProductQ)
	ProductIDtemp = []
	#  print ProductID    # Original Data
	#  print ProductQ     # As extracted from csv file
	k=len(ProductID)
	i=0
	while i < k:
		j=i+1
		while j < k:
			if(ProductID[i][0]==ProductID[j][0]):
				ProductQ[j] += ProductQ[i]
				del ProductQ[i]
				del ProductID[i]
				i -= 1
				k -= 1
				break
			j += 1
		i += 1

	# print ProductID    # Here Product ID and Quantity ordered is calculated
	# print ProductQ     # and unique list has been created...
	ProductID = [str(x[0])+' - series' for x in ProductID]
	plt.barh(np.arange(len(ProductID)), ProductQ, 0.45 ,align='center', alpha=0.5,color=['g','r']) 
	plt.yticks(np.arange(len(ProductID)),ProductID)
	plt.xlabel("Quantity")
	plt.ylabel("Product-ID\n")
	plt.title("Product Popularities")   
	plt.show()	
	return;
########################################################################################################################################
###########        Funtion to plot bar graph --- How much transaction is there in each area      #######################################
###########                                                                                      #######################################

def AreaDistribution():
	ColN = ['ProductID', 'ProductQ','Date','Tcost','Pin','DsTD']
	File = pd.read_csv("CustomerData.csv",names=ColN)
	Pin = np.array(list(File.Pin), dtype=str)
	'''Pin_set = set(Pin)
	Pin_Dict = {}
	for i in Pin:
		Pin_Dict[i] = list(Pin).count(i)'''
	Type = np.dtype([('Place','S20'),('Count',np.int16)])
	Main_Array = np.array([],dtype=Type)
	for i in Pin:
		if i in Main_Array['Place']:
			Main_Array['Count'][Main_Array['Place']==i] += 1
		else:
			temp = np.array([(i,1)],dtype=Type)
			Main_Array = np.append(Main_Array, temp)
	#print Main_Array
	#print Pin_Dict
	X = np.array(np.arange(len(Main_Array['Count']))+1)
	plt.bar(X,Main_Array['Count'],0.60,color=['red','green'],alpha=0.6,align='center')
	plt.xticks(X,list(X+11))
	plt.ylabel('No. of orders')
	plt.xlabel('Area - 4110__')
	plt.title('Area Distribution')
	#plt.xticks(X,Main_Array['Place'])	
	plt.show()
	return;

########################################################################################################################################
###########     Funtion to plot growth chart  ---  From 2013-2017 ---(In terms of turnover)      #######################################
###########                                                                                      #######################################
def GrowthGraph():
	ColN = ['ProductID', 'ProductQ','Date','Tcost','Pin','DsTD']
	File = pd.read_csv("CustomerData.csv",names=ColN)
	DateStrList = [Date_(k) for k in (np.array(list(File.Date), dtype=str))]
	PriceTemp = np.array(list(File.Tcost))
	PriceNumList = []	
	#TogetherList = [[DateStrList[x],PriceNumList[x]] for x in range (len(DateStrList))]
	DateIntList = [k.Give() for k in DateStrList]
	DateTemp = list(DateIntList)	
	DateIntList.sort()
	for x in DateIntList:
		PriceNumList.append(PriceTemp[DateTemp.index(x)])
	PriceListProccesed = []
	for x in range(15):
		Start = x*(len(PriceNumList)/15)
		Stop = Start + (len(PriceNumList)/15) -1
		PriceListProccesed.append(np.mean(PriceNumList[Start:Stop]))
	#plt.plot(np.arange(len(PriceNumList)), PriceNumList)
	plt.plot(np.arange(len(PriceListProccesed)), PriceListProccesed)
	Blah = [x for x in range(2012,2019)]
	plt.grid()
	plt.xticks(np.arange(len(PriceListProccesed)),[])
	plt.xlabel('Every Quarter year (2013 to 2017)')
	plt.ylabel('Turnover in every quarter year')
	plt.title('Growth Graph (Time x Revenue)')
	plt.show()
	return;
	

########################################################################################################################################
###########         Funtion to plot chart depicting Area and Price of each purchase              #######################################
###########                                                                                      #######################################
def Address_Cost():
	ColN = ['ProductID', 'ProductQ','Date','Tcost','Pin','DsTD']
	File = pd.read_csv("CustomerData.csv",names=ColN)
	PinList = list(np.array(list(File.Pin),dtype=str))[::4]
	PriceList = np.array(list(File.Tcost))[::4]
	PlaceSet = list(set(PinList))
	PlaceSet.sort()
	PlaceMean = []
	for i in PlaceSet:
		PlaceMean.append(int(np.mean([PriceList[x] for x in range(len(PriceList)) if PinList[x]==i])))
	Xaxis = [int(x[-2:]) for x in PlaceSet] 
	plt.plot([int(x[-2:]) for x in PinList] , PriceList,'bo',alpha=0.5)
	#plt.plot(Xaxis, PlaceMean,'ro',alpha=0.9)
	#plt.bar( np.arange(len(PlaceSet)), PlaceMean,alpha=0.3,color='g')
	plt.bar( Xaxis, PlaceMean,alpha=0.5,color='g')
	#plt.plot( Xaxis, PlaceMean,'r',alpha=1.0,mew=2)
	plt.plot(Xaxis+list(np.arange(max(Xaxis),max(Xaxis)+5,1)), [max(PlaceMean)]*(len(PlaceMean)+5),'r--',Xaxis+list(np.arange(max(Xaxis),max(Xaxis)+5,1)), [min(PlaceMean)]*(len(PlaceMean)+5),'r--',alpha=0.5)
	Xlabel = np.array(list(np.arange(len(Xaxis))))
	plt.xticks(Xaxis,Xlabel+12)
	plt.xlabel('Area - 4110__\n One Dots = One Purchase in that area'+' '*30+'Height of Bar = Mean of cost of Purchases ')
	plt.ylabel('Cost of Purchases\n')
	plt.title('Area x Revenue')
	plt.show()
	return;
########################################################################################################################################
###########              K-mean for Month_of_Year VS Cost_of_Commodity                           #######################################
###########                                                                                      #######################################
K =3	#--Value of K hardcoded as 3
def GiveDist(a,b,c,d):
	return((c-a)**2 + (d-b)**2)
def CheckClosest(MTP,KM):
	ar = []
	for x in range(K):
		ar.append(GiveDist(MTP['Date'],MTP['Cost'],int(KM[x][0]),int(KM[x][1])))
	return ar.index(min(ar))
def K_meanDateVSCost():
	ColN = ['ProductID', 'ProductQ','Date','Tcost','Pin','DsTD']
	File = pd.read_csv("CustomerData.csv",names=ColN)
	KMeanCheck = 300
	D1 = [Date_(k) for k in (np.array(list(File.Date), dtype=str))]
	D1 = D1[::2]
	DateStrListFalse = [str(k.Give()) for k in D1]
	DateStrListFalse_Length = len(DateStrListFalse)
	DateStrList = np.arange(len(DateStrListFalse))
	TCost = list(File.Tcost)
	TCost1 = list(TCost[::2])
	m = min(TCost1)
	M = max(TCost1)/DateStrListFalse_Length
	TCost = [int((x-m)/M) for x in TCost1]
	#FALSE--MyType = np.dtype([('Date','S12'),('Cost',int),('Daddy',int)])
	MyType = np.dtype([('Date',int),('Cost',int),('Daddy',int)])
	Check = 0
	MainArray = np.array([],dtype=MyType)
	for x in range (len(DateStrList)):
		Temp = np.array([(DateStrList[x],TCost[x],-1)],dtype=MyType)
		MainArray = np.append(MainArray,Temp)
	#MainArray = np.sort(MainArray, order='Date')
	MonthCost = []
	for y in range(1,13):
		#FALSE--Temp1 = list([x['Cost'] for x in MainArray if int(x['Date'][4:6])==y])
		Temp1 = list([x['Cost'] for x in MainArray if int(x['Date'])%12==y])#FALSE
		MonthCost.append(Temp1)	
	#FALSE--K_Mean = [[int(MainArray[x*23]['Date'][4:]),MainArray[x*15]['Cost']] for x in range(K)]
	K_Mean = [[int(MainArray[x*6+2]['Date']),MainArray[x*9+2]['Cost']] for x in range(K)]#FALSE
	while True:
		Temp = np.array(K_Mean)
  		for x in range(len(MainArray)):
			MainArray[x]['Daddy'] = CheckClosest(MainArray[x], K_Mean)
			#CheckClosest(MainArray[x], K_Mean)
		for x in range(K):
			#FALSE--K_Mean[x][0] = np.mean( [int(MainArray[y]['Date'][4:]) for y in range(len(MainArray)) if MainArray[y]['Daddy']==x])
			K_Mean[x][0] = int(np.mean( [MainArray[y]['Date'] for y in range(len(MainArray)) if MainArray[y]['Daddy']==x]))#FALSE
			K_Mean[x][1] = int(np.mean( [MainArray[y]['Cost'] for y in range(len(MainArray)) if MainArray[y]['Daddy']==x]))
		KMeanCheck -= 1
		if (Temp == K_Mean).all() or KMeanCheck < 1:
			break
	Range = len(MainArray)
	Range_i = 0
	while Range_i < Range:
		Distance = GiveDist(MainArray[Range_i]['Date'],MainArray[Range_i]['Cost'], K_Mean[MainArray[Range_i]['Daddy']][0],K_Mean[MainArray[Range_i]['Daddy']][1])
		if int(Distance) > (800**2):
			MainArray = np.delete(MainArray, Range_i)
			Range -= 1
			Range_i -= 1
		elif (Check%2==0 or Check%3==0 or Check%5==0) and Distance > (300**2):
			MainArray = np.delete(MainArray, Range_i)
			Range -= 1
			Range_i -= 1
		elif ( Check%2==0) and Distance > (260**2):
			MainArray = np.delete(MainArray, Range_i)
			Range -= 1
			Range_i -= 1
		elif ( Check%3==0) and Distance > (220**2):
			MainArray = np.delete(MainArray, Range_i)
			Range -= 1
			Range_i -= 1
		Range_i += 1
		Check += 1
	PlotCost = []
	for x in range(len(MonthCost)):
		PlotCost = PlotCost + list(MonthCost[x])
	PLT = []
	PC = []
	for x in range(K):
		PLT.append([MainArray[y]['Date'] for y in range(len(MainArray)) if MainArray[y]['Daddy']==x])
		PC.append([MainArray[y]['Cost'] for y in range(len(MainArray)) if MainArray[y]['Daddy']==x])
	#PlotLengthTemp = [x['Date'][4:] for x in MainArray
	PlotLength = np.arange(len(MainArray['Cost']))
	#plt.plot(PlotLength, MainArray['Cost'], 'ro', alpha=0.7)	
	plt.plot(K_Mean[0][0],K_Mean[0][1],'ro',alpha=1.0)
	plt.plot(PLT[0],PC[0],'r.',alpha=0.6)
	plt.plot(K_Mean[1][0],K_Mean[1][1],'bo',alpha=1.0)
	plt.plot(PLT[1],PC[1],'b.',alpha=0.6)
	plt.plot(K_Mean[2][0],K_Mean[2][1],'go',alpha=1.0)
	plt.plot(PLT[2],PC[2],'g.',alpha=0.6)
	Value = [114*x for x in range(12) ]
	plt.xticks(Value,['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
	plt.yticks(Value,np.arange(500,4100,300))
	plt.xlabel('(2013 - 2017)')
	plt.ylabel('Cost of Purchases')
	plt.title('K-mean plot with K=3')
	#ax.tick_params(axis='x',width = 50 )
	plt.show()
	return 		


########################################################################################################################################
###########              KNN algorithm Predicting Area of Commodity                              #######################################
###########                                                                                      #######################################
def GiveDist(a,b,c,d):
	return((c-a)**2 + (d-b)**2)
def GetKClosest(MainArray, Point):
	DistArray = [GiveDist(MainArray[x]['Price'], MainArray[x]['Days'], Point[0], Point[1]) for x in range(len(MainArray))]
	#print DistArray
	#print min(DistArray)
	#print DistArray.index(min(DistArray))
	return DistArray.index(min(DistArray))
def KNNPredictArea():
	ColN = ['ProductID', 'ProductQ','Date','Tcost','Pin','DsTD']
	File = pd.read_csv("CustomerData.csv",names=ColN)
	PinList = list(np.array(list(File.Pin),dtype=str))
	PriceList1 = np.array(list(File.Tcost),dtype=int)
	Quant = np.array(list(File.ProductQ),dtype=int)
	PriceList = PriceList1/Quant
	DayList = np.array(list(File.DsTD),dtype=int)
	PlaceSet = list(set(PinList))
	MyType = np.dtype([("Pin","S10"),("Price",int),("Days",int)])
	MainArray = np.array([],dtype=MyType)
	PlaceSet.sort()
	PriceMean = []
	DaysMode = []
	for i in PlaceSet:
		PriceMean.append(int(np.mean([PriceList[x] for x in range(len(PriceList)) if PinList[x]==i]))+(PlaceSet.index(i)*10))
		Offset = randint(0,99)
		DaysMode.append(int(ST.mode([DayList[x] for x in range(len(PriceList)) if PinList[x]==i])[0])+(Offset/float(100)))
		#print (ST.mode([DayList[x] for x in range(len(PriceList)) if PinList[x]==i])[0])
	####---PlaceSet,PriceMean,DaysMode---####
	for i in range(len(PlaceSet)):
		Temp = np.array([(PlaceSet[i],PriceMean[i],DaysMode[i])],dtype=MyType)
		MainArray = np.append(MainArray, Temp)
	Point = []
	##########################################################################################################
	################################         GUI to get data     ######################
	def PointGetandShow():
		#Point = [6,553]
		Point.append(int(Entry20.get()))
		Point.append(int(Entry21.get()))
		plt.plot(DaysMode,PriceMean,'ro',alpha=0.5)
		plt.plot(Point[1], Point[0], 'bo', alpha=0.6)
		plt.xlabel('Mode Days till delivery')
		plt.ylabel('Mean of Cost of all purchaces')
		plt.title('Area Plot')
		plt.show()  
		#plt.plot(DaysMode,PriceMean,'ro',alpha=0.5)
		#plt.plot(Point[0], Point[1], 'bo', alpha=0.6)
		#plt.plot(MainArray[Closest]['Days'], MainArray[Closest]['Price'],'go',alpha=0.7)
		#plt.show()
		Closest = GetKClosest(MainArray, Point)
		#print Closest
		StrPrint = "\tPredicted Area through \ngiven data is : "+str(MainArray[Closest]['Pin'])
		Text = c8.create_text(170,25,text=StrPrint,font=("Purisa",15),fill='blue')
		return;
	Get = Tkinter.Tk()
	c9 = Tkinter.Canvas(Get, bg='#E4E4E4', height=60,width=420)
	c9.grid(row=0,column=0,columnspan=5,rowspan=2)
	c8 = Tkinter.Canvas(Get, bg='#E4E4E4', height=70,width=420)
	c8.grid(row=15,column=0,columnspan=5,rowspan=1)
	#S1 = c1.create_rectangle(100,100,200,200)
	Text = c9.create_text(170,30,text="\tPredicting Possible Location of \n \titem with distorted information",font=("Purisa",15),fill='red')
	
	lable20 = Tkinter.Label(Get,text ='Price of Commodity').grid(row=4, column=2, sticky='E')
	lable21 = Tkinter.Label(Get,text ='   No. of Days took to delivery').grid(row=5, column=2, sticky='E')
	Entry20 = Tkinter.Entry(Get,bd=5)
	Entry21 = Tkinter.Entry(Get,bd=5)
	Entry20.grid(row=4, column=3)
	Entry21.grid(row=5, column=3)
	
	DrawButton = Tkinter.Button(Get,text='Predict Location / Area',bg='blue',fg='white',bd=3,command=PointGetandShow).grid(row=13,column=4)
	Get.mainloop()
	
	##########################################################################################################
	return;	

########################################################################################################################################

lable1 = Tkinter.Label(top,text ='Product ID').grid(row=4, column=2, sticky='E')
lable2 = Tkinter.Label(top,text ='Quantity').grid(row=5, column=2, sticky='E')
lable3 = Tkinter.Label(top,text ='Date (DD/MM/YYYY)').grid(row=6, column=2, sticky='E')
lable4 = Tkinter.Label(top,text ='Total Charges').grid(row=7, column=2, sticky='E')
lable5 = Tkinter.Label(top,text ='Pin Code').grid(row=8, column=2, sticky='E')
lable6 = Tkinter.Label(top,text ='Days till Dilivery').grid(row=9, column=2, sticky='E')
#lable7 = Tkinter.Label(top,text ='  (q3)')
#lable8 = Tkinter.Label(top,text =' ')

Entry1 = Tkinter.Entry(top,bd=5)
Entry2 = Tkinter.Entry(top,bd=5)
Entry3 = Tkinter.Entry(top,bd=5)
Entry4 = Tkinter.Entry(top,bd=5)
Entry5 = Tkinter.Entry(top,bd=5)
Entry6 = Tkinter.Entry(top,bd=5)
#Entry7 = Tkinter.Entry(top,bd=5).grid(row=10, column=3)
#Entry8 = Tkinter.Entry(top,bd=5).grid(row=11, column=3)
DrawButton = Tkinter.Button(top,text='Add Data',bg='blue',fg='white',bd=3,command=LoadCSV).grid(row=13,column=4)
SpaceEaters = Tkinter.Label(top,text =' \n \n').grid(row=13, column=3)
SpaceEaters = Tkinter.Label(top,text =' ').grid(row=16, column=0)

DrawButton = Tkinter.Button(top,text='Product Popularity',bg='blue',fg='white',bd=3,command=ProductPopularity).grid(row=17,column=2)

DrawButton = Tkinter.Button(top,text='Area Distribution',bg='blue',fg='white',bd=3,command=AreaDistribution).grid(row=17,column=3)
lable = Tkinter.Label(top,text=' ').grid(row=18,column=2)
DrawButton = Tkinter.Button(top,text='Growth Graph(TimexRevenue)',bg='red',fg='white',bd=3,command=GrowthGraph).grid(row=19,column=2)

DrawButton = Tkinter.Button(top,text='Area and Revenue',bg='red',fg='white',bd=3,command=Address_Cost).grid(row=19,column=3)
lable = Tkinter.Label(top,text=' ').grid(row=20,column=2)
DrawButton = Tkinter.Button(top,text='K-MEAN - Place & Cost',bg='blue',fg='white',bd=3,command=K_meanDateVSCost).grid(row=21,column=2)

DrawButton = Tkinter.Button(top,text='KNN Area Prediction',bg='blue',fg='white',bd=3,command=KNNPredictArea).grid(row=21,column=3)
lable = Tkinter.Label(top,text=' ').grid(row=22,column=2)

Entry1.grid(row=4, column=3)
Entry2.grid(row=5, column=3)
Entry3.grid(row=6, column=3)
Entry4.grid(row=7, column=3)
Entry5.grid(row=8, column=3)
Entry6.grid(row=9, column=3)
top.mainloop()



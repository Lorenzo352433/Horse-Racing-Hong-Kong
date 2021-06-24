import pandas as pd
import os 
import numpy as np 
import csv
print ("Please input raceday")
racedate = input()
racedate = str(racedate)
print("Please input racenumber")
racenumber = input()
racenumber = str(racenumber)




#Set up new CSV

#Searching
def horsesearch():
	for row in database:
		for noofhorses in range(0,noofhorse):
			horse=brandno[noofhorses]
			if horse in row[3]:
				horse1=row
				with open(racedate+racenumber+"racecard.csv","a") as racecard:
					writer = csv.writer(racecard)
					writer.writerows(row+[" "] for r in horse1)
				df = pd.read_csv(racedate+racenumber+"racecard.csv")
				df.drop_duplicates(inplace=True)
				df.to_csv(racedate+racenumber+"racecard.csv", index=False)
				print(horse1)
				
				
			

			


os.chdir("/Users/Lorenzo/Documents/Investment/Racing/Racecard/" + racedate) #Go to the racecard file
	

data = pd.read_csv(racedate+racenumber+".csv")
brandno=data.number	
print(brandno)
noofhorse=len(brandno)
noofhorse=int(noofhorse)
print(noofhorse)

#Go to database
os.chdir("/Users/Lorenzo/Documents/Investment/Racing/Records")
database = csv.reader(open("Data20192021.csv" , "r"))

os.chdir("/Users/Lorenzo/Documents/Investment/Racing/Racecard/" + racedate)
filename = racedate+racenumber+"racecard.csv"
headers = 'race_id,place,horse_num,horse_id,jockey,trainer,actual_weight,horse_weight,draw,lbw,finish_time,win_odds,class,distance,location,going,course,1st_sectional_place,2nd_sectional_place,3rd_sectional_place,4th_sectional_place,5th_sectional_place,6th_sectional_place,1st_sectional_time,2nd_sectional_time,3rd_sectional_time,4th_sectional_time,5th_sectional_time,6th_sectional_time,finish_time,1st_section_MPS,2nd_section_MPS,3rd_section MPS,4th_section_MPS,5th_section_MPS,6th_section_MPS,AP,EP,SP,Total_Energy,E%,FX'
f = open(filename,"w")
f.write(headers)
	
horsesearch()







	
		





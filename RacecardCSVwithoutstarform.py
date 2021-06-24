import requests
from bs4 import BeautifulSoup as BS4
import time
import os
timestr = time.strftime("%y%m%d")
print("Please enter the race date")
racedate = input()
print("Please input number of races on the next meeting.")
path = "/Users/Lorenzo/Documents/Investment/Racing/Racecard/"+racedate
os.mkdir(path)
os.chdir(path)
racenumber = input()
racenumber=int(racenumber)
for racenumbers in range(1,racenumber+1):

	URL = 'https://www.scmp.com/sport/racing/racecard/'+str(racenumbers)
	page = requests.get(URL)
	soup = BS4(page.content, 'html.parser')
	detailcontainer = soup.findAll("div",{"class":"details"})
	race = detailcontainer[0].h1
	racename = race
	race = detailcontainer[0].h1.span.decompose()
	race = detailcontainer[0].h1.text
	racedetail = detailcontainer[0].p.text
	noofrace = str(race)
	numberofrace= len(race)
	
	if racenumbers <10:
		race = race[0:6]
		print(race)
		raceno = int(race[5])
	else:
		race = race[0:7]
		raceno = int(race[5:7])
	if raceno < 10:
		race = race.replace(' ', '0')
		race = race[4:6]
	else:
		race = race[5:7]
	date = detailcontainer[0].h2.text
	print (str(date) + str(racename))

	filename = racedate+race+".csv"

	total = soup.findAll("tbody")
	total = total[0]
	bodies = total.findAll("tr")


	headers = 'number,brandno,engname,lastsixrun,draw,age,weight,rating,trainer,jockey,priority,overnight,odds,placeodds\n'
	f = open(filename, "w")
	f.write(headers)

	for body in bodies:
		
		#Horse Number
		numbercontainer = body.findAll("td",{"class":"horse_number"}) 
		number = numbercontainer[0].text 
		print("Horse number" + str(number)) 

		#Horse Name and Brand Number
		namecontainer = body.findAll("td",{"class":"horse_name"})
		brandno = namecontainer[0].a.span.text
		brandno = brandno[2:6]
		engname = namecontainer[0].a.text
		print("brand number" + brandno)
		print("english name" + engname)

		#Last Six Runs
		lastsixruncontainer = body.findAll("td",{"class":"last_six_run"})
		lastsixrun = lastsixruncontainer[0].text
		print("last six run" + lastsixrun)

		#Draw
		drawcontainer = body.findAll("td")
		draw = drawcontainer[12].text
		print("Draw" + draw)

		#Age
		agecontainer = body.findAll("td")
		age = agecontainer[8].text
		print("Age" + age)

		#Weight 
		weightcontainer = body.findAll("td")
		weight = weightcontainer[9].text
		print("Weight" + weight)

		#Rating
		ratingcontainer = body.findAll("td")
		rating = agecontainer[10].text
		print("Age" + age)

		#Trainer 
		trainercontainer = body.findAll("td",{"class":"trainer_name"})
		trainer = trainercontainer[0].text
		print("Trainer" + trainer)

		#Jockey
		jockeycontainer = body.findAll("td",{"class":"jockey_name"})
		jockey = jockeycontainer[0].text
		print ("Jockey" + jockey)

		#Priority
		prioritcontainer = body.findAll("td")
		priority = prioritcontainer[4].text
		print("Priority" + priority)

		#Overnight Odds
		overnightcontainer =body.findAll("td",{"class":"overnight_win_odds"})
		overnight = overnightcontainer[0].text
		print("Overnight Win Odds" + overnight)

		#Today Odds
		oddscontainer =body.findAll("td",{"class":"win_odds"})
		odds = oddscontainer[0].text
		print("Win Odds" + odds)

		#Place
		placeoddscontainer = body.findAll("td")
		placeodds = placeoddscontainer[15].text
		print("Place Odds" + placeodds)

		f.write(number + "," + brandno + "," + engname + "," + lastsixrun + "," + draw + "," + age + "," + weight + "," + rating + "," + trainer + "," + jockey + "," + priority + "," + overnight + "," + odds + "," + placeodds + "," + "\n")





	





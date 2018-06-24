from bs4 import BeautifulSoup
import requests
import re
import csv

 


def checking(val):
	if val == None:
		return " "
	else:
		return val


html_page = requests.get("https://ballotpedia.org/List_of_current_city_council_officials_of_the_top_100_cities_in_the_United_States")
 
soup = BeautifulSoup(html_page.text, 'lxml')
all_arr = []
city_name = []

cities = soup.find_all('span', attrs={'class': "mw-headline"})
for each_city in cities:
	city_name.append(each_city.get('id'))
city_name = city_name[:-6]

for imdone in city_name:


	# city_name = ['New_York_City', 'Los_Angeles','Chicago','Houston','Philadelphia','Phoenix','San_Antonio','San_Diego']
	ny = soup.find('span',id=imdone)
	table = ny.parent.find_next_sibling().find_all('a')

	people_name = []
	people_web = []
	for name in table:
		x = (name.get('title'))
		y = "https://ballotpedia.org/" +x.replace(" ", "_")
		# people_name.append(x)
		people_web.append(y)


	# print(people_name)
	# print(people_web)


	# ----------------------------------------------------------------
	temp_arr = []
	for sites in people_web:
		people_sites = requests.get(sites)

		soup2 = BeautifulSoup(people_sites.text, 'lxml')
		getname = soup2.find('div', attrs={'class':'widget-row value-only Democratic Party'})
		if(getname==None):
			temp_arr = ["","","","",""]
		else:
			nextone = checking(getname.find_next_sibling())
			tenure = checking(nextone.find_next_sibling().find_next_sibling().find_next_sibling())
			end = checking(tenure.find_next_sibling().find_next_sibling())
			year_posi = checking(end.find_next_sibling().find_next_sibling())
			party = checking(year_posi.find_next_sibling())

			temp_arr.append(getname.text.strip())
			temp_arr.append(tenure.text.strip())
			temp_arr.append(end.text.strip())
			temp_arr.append(year_posi.text.strip())
			temp_arr.append(party.text.strip())


		social = soup2.find('span',id='External_links')
		next_ = social.parent.find_next_sibling().find_next_sibling().find('ul')
		if(next_ != None):


			face = next_.find('a',text='Facebook')
			if(face!=None):
				temp_arr.append(face['href'])
			else:
				temp_arr.append("no facebook")

			twit = (next_.find('a',text='Twitter'))
			if(twit !=None):

				temp_arr.append(twit['href'])
			else:
				temp_arr.append("no twitter")
		else:
			temp_arr.append("no facebook")
			temp_arr.append("no twitter")
	

		# all_arr.append(temp_arr)


		with open('Workbook1.csv', 'a') as csvfile:
		    fieldnames = ['name', 'Tenure','Term ends','Year in position','party','faceb','twitt']
		    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		    writer.writeheader()
		    writer.writerow({'name' : temp_arr[0], 'Tenure' : temp_arr[1],'Term ends': temp_arr[2],'Year in position':temp_arr[3],'party':temp_arr[4],'faceb':temp_arr[5],'twitt':temp_arr[6]})
		temp_arr = []


# print(all_arr)




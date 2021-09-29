from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# from rasa_core_sdk.events import AllSlotsReset
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import Restarted
import pandas as pd
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class ActionRestarted(Action): 	
	def name(self):
		return 'action_restart'
	def run(self, dispatcher, tracker, domain):
		return[Restarted()] 

class ActionSlotReset(Action): 
	def name(self): 
		return 'action_slot_reset' 
	def run(self, dispatcher, tracker, domain): 
		return[AllSlotsReset()]


ZomatoData = pd.read_csv('zomato.csv',encoding='latin1')
ZomatoData = ZomatoData.dropna()
ZomatoData = ZomatoData.drop_duplicates().reset_index(drop=True)
WeOperate = ['New Delhi', 'Gurgaon', 'Noida', 'Faridabad', 'Allahabad', 'Bhubaneshwar', 'Mangalore', 'Mumbai', 'Ranchi', 'Patna', 'Mysore', 'Aurangabad', 'Amritsar', 'Puducherry', 'Varanasi', 'Nagpur', 'Vadodara', 'Dehradun', 'Vizag', 'Agra', 'Ludhiana', 'Kanpur', 'Lucknow', 'Surat', 'Kochi', 'Indore', 'Ahmedabad', 'Coimbatore', 'Chennai', 'Guwahati', 'Jaipur', 'Hyderabad', 'Bangalore', 'Nashik', 'Pune', 'Kolkata', 'Bhopal', 'Goa', 'Chandigarh', 'Ghaziabad', 'Ooty', 'Gangtok', 'Shimla']

# def restaurant_search(City,Cuisine,budget):
def restaurant_search(City,Cuisine):
	# cost_for_two = 0
	# priceMin=0
	# priceMax=1000000
	# if(budget=="<300"):
	# 	priceMax=299
	# elif(budget=="300-700"):
	# 	priceMin=300
	# 	priceMax=699
	# else:
	# 	priceMin=700
	# cost_for_two = ZomatoData['Average Cost for two']
	# if(cost_for_two>=priceMin & cost_for_two<=priceMax):
	TEMP = ZomatoData[(ZomatoData['Cuisines'].apply(lambda x: str(Cuisine).lower() in str(x).lower())) & (ZomatoData['City'].apply(lambda x: str(City).lower() in str(x).lower()))]	
	return TEMP[['Restaurant Name','Address','Average Cost for two','Aggregate rating']]
	
def validate_location(location):
	if location.title() in WeOperate:
		return True
	else:
		return False

MY_ADDRESS = 'rashika.khandelwal554@gmail.com'
PASSWORD = '$rashi554'

def send_email(name,user_domain,response):
	# set up the SMTP server
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)

	#For each contact, send the email:
    # for name, email in zip(names, emails):
	# create a message
	msg = MIMEMultipart()
	# add in the actual person name to the message template
	message = "Hello, "+name+"\n"+response
	
	# Prints out the message body for our sake
	print(message)
	# setup the parameters of the message
	msg['From']=MY_ADDRESS
	msg['To']=user_domain
	msg['Subject']="Foodie"
	
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))
	
	# send the message via the server set up earlier.
	s.send_message(msg)
	del msg
	
	# Terminate the SMTP session and close the connection
	s.quit()


class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_search_restaurants'

	def run(self, dispatcher, tracker, domain):
		#config={ "user_key":"f4924dc9ad672ee8c4f8c84743301af5"}
		print('testing')
		found_restaurants=True
		price_max = 1000000
		price_min = 0
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		results = restaurant_search(City=loc,Cuisine=cuisine)
		# results = restaurant_search(City=loc,Cuisine=cuisine,budget=budget)
		response=""
		#print(F'hello {loc}')
		if results.shape[0] == 0:
			response= "no results"
			dispatcher.utter_message("Sorry, We couldn't find any "+str(cuisine)+" restaurants in "+str(loc)+".")
			found_restaurants=False
		else:
			df=pd.DataFrame(data=results,columns=['Restaurant Name','Address','Average Cost for two','Aggregate rating'])
			df=df.rename(columns={'Restaurant Name':'Name'})
			df=df.rename(columns={'Aggregate rating':'Rating'})
			df=df.rename(columns={'Average Cost for two':'Avg_Cost_for_Two'})
			if budget == '<300':
				price_max = 299
			elif budget == '300-700':
				price_min = 300
				price_max = 699
			else:
				price_min = 700
			df = df[(df['Avg_Cost_for_Two'] >= price_min) & (df['Avg_Cost_for_Two'] <= price_max)]
			df = df.sort_values(by=['Rating'], ascending=False)
			if(len(df.Name)>=5): 
				response="Top 5 "+str(cuisine)+" restaurants near "+str(loc)+" are: \n"
				# for i in range(5):
				# 	response+=df.Name[i]+" in "+df.Address[i]+" has been rated "+str(df.Rating[i])+". Average Cost for Two is Rs. "+str(df.Avg_Cost_for_Two[i])+". \n"
				for restaurant in df.iloc[:5].iterrows():
					restaurant = restaurant[1]
					response = response + F"Found {restaurant['Name']} in {restaurant['Address']} rated {restaurant['Rating']} with avg cost {restaurant['Avg_Cost_for_Two']} \n\n"
			elif(len(df.Name)>0 and len(df.Name)<5):  # Couldn't find 5 restaurants
				response="Sorry we could not find enough restaurants with given details \n"
				response+="Top "+str(len(df.Name))+" "+str(cuisine)+" restaurants near "+str(loc).rstrip()+" are: \n"
				# for i in range(len(df.Name)):
				for restaurant in df.iloc[:len(df.Name)].iterrows():
					restaurant = restaurant[1]
					response = response + F"Found {restaurant['Name']} in {restaurant['Address']} rated {restaurant['Rating']} with avg cost {restaurant['Avg_Cost_for_Two']} \n\n"
			else:
				response="Sorry, We couldn't find any restaurants matching your requirements."
				found_restaurants=False
		dispatcher.utter_message(response)
		return [SlotSet('found_restaurants',found_restaurants)]


class ActionSearchRestaurantsTopTen(Action):
	def name(self):
		return 'action_send_email'
		
	def run(self, dispatcher, tracker, domain):
		print('testing1')
		price_max = 1000000
		price_min = 0
		mail_status=False
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		user_domain = tracker.get_slot('email')
		found_restaurants = tracker.get_slot('found_restaurants')
		name = user_domain.split('@')[0]
		budget = tracker.get_slot('budget')
		results = restaurant_search(City=loc,Cuisine=cuisine)
		# results = restaurant_search(City=loc,Cuisine=cuisine,budget=budget)
		response=""
		#print(F'hello {loc}')
		if results.shape[0] == 0:
			response= "no results"
		else:
			df=pd.DataFrame(data=results,columns=['Restaurant Name','Address','Average Cost for two','Aggregate rating'])
			df=df.rename(columns={'Restaurant Name':'Name'})
			df=df.rename(columns={'Aggregate rating':'Rating'})
			df=df.rename(columns={'Average Cost for two':'Avg_Cost_for_Two'})
			if budget == '<300':
				price_max = 299
			elif budget == '300-700':
				price_min = 300
				price_max = 699
			else:
				price_min = 700
			df = df[(df['Avg_Cost_for_Two'] >= price_min) & (df['Avg_Cost_for_Two'] <= price_max)]
			df=df.sort_values(by=['Rating'], ascending=False)
			if(found_restaurants==True):
				if(len(df.Name)>=10): 
					response="Top 10 "+str(cuisine)+" restaurants near "+str(loc)+" are: \n"
					# for i in range(10):
					# 	response+=df.Name[i]+" in "+df.Address[i]+" has been rated "+str(df.Rating[i])+". Average Cost for Two is Rs. "+str(df.Avg_Cost_for_Two[i])+". \n"
					for restaurant in df.iloc[:10].iterrows():
						restaurant = restaurant[1]
						response = response + F"Found {restaurant['Name']} in {restaurant['Address']} rated {restaurant['Rating']} with avg cost {restaurant['Avg_Cost_for_Two']} \n\n"
					mail_status=True
					send_email(name,user_domain,response)
				elif(len(df.Name)>0 and len(df.Name)<10):  # Couldn't find 10 restaurants
					response="All "+str(cuisine)+" restaurants near "+str(loc).rstrip()+" are: \n"
					for restaurant in df.iloc[:len(df.Name)].iterrows():
						restaurant = restaurant[1]
						response = response + F"Found {restaurant['Name']} in {restaurant['Address']} rated {restaurant['Rating']} with avg cost {restaurant['Avg_Cost_for_Two']} \n\n"
					mail_status=True
					send_email(name,user_domain,response)
				dispatcher.utter_message("Mail Sent!")
			else:
				mail_status=False
				dispatcher.utter_message("Sorry.No restaurants found")
		return [SlotSet('mail_sent',mail_status)]


class ActionCheckLocation(Action):
	def name(self):
		return 'action_check_location'

	def run(self, dispatcher, tracker, domain):
		print('testing2')
		location = tracker.get_slot('location')
		res = validate_location(location)
		print('testing 2 ran successfully')
		return [SlotSet('check_resp',res)]		














	# return [SlotSet('location',loc)]
	 # except:
    #   dispatcher.utter_message("Sorry, We couldn't find any "+str(cuisine)+" restaurants in "+str(loc)+".")
    #   found_restaurants=False
			# for restaurant in restaurant_search(loc,cuisine).iloc[:5].iterrows():
			# 	restaurant = restaurant[1]
			# 	response = response + F"Found {restaurant['Restaurant Name']} in {restaurant['Address']} rated {restaurant['Aggregate rating']} with avg cost {restaurant['Average Cost for two']} \n\n"
				

# class ActionSendMail(Action):
# 	def name(self):
# 		return 'action_send_mail'

# 	def run(self, dispatcher, tracker, domain):
# 		loc = tracker.get_slot('location')
#         cuisine = tracker.get_slot('cuisine')
# 		user_domain = tracker.get_slot('mail_id')
# 		found_restaurants = tracker.get_slot('found_restaurants')
# 		name = user_domain.split('@')[0]
# 		send_mail(name,user_domain,response)
# 		return [SlotSet('mail_id',MailID)]










    # else:
    #   r_data=[]
    #   for i,r in enumerate(d["restaurants"]):
    #     r_l=[]
    #     cost_for_two=int(r['restaurant']['average_cost_for_two'])
    #     if(cost_for_two>=priceMin and cost_for_two<=priceMax):
    #       r_l.append(r['restaurant']['id'])
    #       r_l.append(r['restaurant']['name'])
    #       r_l.append(float(r['restaurant']['user_rating']['aggregate_rating']))
    #       r_l.append(cost_for_two)
    #       r_l.append(r['restaurant']['location']['address'])
    #       r_data.append(r_l)
    #   df=pd.DataFrame(data=r_data,columns=["ID","Name","Rating","Avg_Cost_for_Two","Address"])
    #   df.set_index('ID', inplace=True)
    #   df=df.sort_values('Rating',ascending=False)
    #   if(found_restaurants==True):
    #     if(len(df.Name)>=10): 
    #       response="Top 10 "+str(cuisine)+" restaurants near "+str(loc)+" are: \n"
    #       for i in range(10):
    #         response+=str(i+1)+" "+df.Name[i]+" in "+df.Address[i]+" has been rated "+str(df.Rating[i])+". Average Cost for Two is Rs. "+str(df.Avg_Cost_for_Two[i])+". \n"
    #       mail_status=True
    #       send_email(name,user_domain,response)
    #     elif(len(df.Name)>0 and len(df.Name)<10):  # Couldn't find 10 restaurants
    #       response="All "+str(cuisine)+" restaurants near "+str(loc).rstrip()+" are: \n"
    #       for i in range(len(df.Name)):
    #         response+=str(i+1)+" "+df.Name[i]+" in "+df.Address[i]+" has been rated "+str(df.Rating[i])+". Average Cost for Two is Rs. "+str(df.Avg_Cost_for_Two[i])+". \n"
    #       mail_status=True
    #       send_email(name,user_domain,response)
    #     dispatcher.utter_message("Mail Sent!")
    #   else:
    #     mail_status=False
    #     dispatcher.utter_message("Sorry.No restaurants found")
    # # dispatcher.utter_message(response)

         


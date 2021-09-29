<!-- ## complete path
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
    - slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - action_check_loc
    - slot{"check_resp": true}
    - utter_ask_price
    - slot{"price": ">300"}
    - action_search_restaurants
    - slot{"location": "delhi"}
    - utter_goodbye
    - export -->

## complete path
* greet
    - utter_greet
* restaurant_search{"location": "Pune"}
    - slot{"location": "Pune"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
    - slot{"cuisine": "North Indian"}
    - utter_ask_budget
* restaurant_search{"budget": ">700"}
    - slot{"budget": ">700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_ask_top_ten
* send_email{"more_info_desired": "Yes"}
    - slot{"more_info_desired": "Yes"}
    - utter_ask_email
* send_email{"email": "rashika.khandelwal554@gmail.com"}
    - slot{"email": "rashika.khandelwal554@gmail.com"}
    - action_send_email
    - slot{"mail_sent": true}
    - utter_goodbye
    - action_restart

## complete path basic
* greet
    - utter_greet
* restaurant_search{"location": "Faridabad"}
    - slot{"location": "Faridabad"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_ask_top_ten
* send_email{"more_info_desired": "Y"}
    - slot{"more_info_desired": true}
    - utter_ask_email
* send_email{"email": "rashika.khandelwal554@gmail.com"}
    - slot{"email": "rashika.khandelwal554@gmail.com"}
    - action_send_email
* exit
    - utter_goodbye
    - action_restart

## interactive_story_1
* greet
    - utter_greet
* restaurant_search{"location": "Chennai"}
    - slot{"location": "Chennai"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "Italian"}
    - slot{"cuisine": "Italian"}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_goodbye


## interactive_story_2
* greet{"greet": "yello"}
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "Agra"}
    - slot{"location": "Agra"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
    - slot{"cuisine": "North Indian"}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_goodbye

## interactive_story_3
* greet
    - utter_greet
* restaurant_search{"location": "Hyderabad"}
    - slot{"location": "Hyderabad"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_ask_top_ten
* send_email
    - utter_greet

## interactive_story_4
* greet
    - utter_greet
* restaurant_search{"cuisine": "American", "location": "Kochi"}
    - slot{"cuisine": "American"}
    - slot{"location": "Kochi"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_ask_top_ten
* send_email
    - utter_greet

## interactive_story_5
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "Chennai"}
    - slot{"location": "Chennai"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "South Indian"}
    - slot{"cuisine": "South Indian"}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": false}
    - utter_goodbye


## interactive_story_6
* greet
    - utter_greet
* restaurant_search{"cuisine": "American", "location": "Chennai"}
    - slot{"cuisine": "American"}
    - slot{"location": "Chennai"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_budget
* restaurant_search{"budget": ">700"}
    - slot{"budget": ">700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - action_send_email


## interactive_story_7
* greet
    - utter_greet
* restaurant_search{"cuisine": "Mexican", "location": "Delhi"}
    - slot{"cuisine": "Mexican"}
    - slot{"location": "Delhi"}
    - action_check_location
    - slot{"check_resp": false}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_ask_top_ten
* send_email
    - utter_ask_email
* send_email{"email": "rashika.khandelwal554@gmail.com"}
    - slot{"email": "rashika.khandelwal554@gmail.com"}
    - action_send_email
    - slot{"mail_sent": true}

## interactive_story_8
* greet
    - utter_greet
* restaurant_search{"cuisine": "chinese", "location": "Gurgaon"}
    - slot{"cuisine": "chinese"}
    - slot{"location": "Gurgaon"}
    - action_check_location
    - slot{"check_resp": true}
    - utter_ask_budget
* restaurant_search{"budget": "300-700"}
    - slot{"budget": "300-700"}
    - action_search_restaurants
    - slot{"found_restaurants": true}
    - utter_ask_top_ten
* send_email
    - utter_ask_email
* send_email{"email": "rashika.khandelwal225@gmail.com"}
    - slot{"email": "rashika.khandelwal225@gmail.com"}
    - action_send_email
    - slot{"mail_sent": true}
* goodbye
    - utter_goodbye
    - action_restart



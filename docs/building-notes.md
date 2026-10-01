# build notes

## step 1 - starting the project

i started tabletwo because picking a place to eat for date night usually takes way longer than it should. the idea is to build an app that helps narrow restaurants down based on stuff that actually matters like location, cuisine, price, ratings, and vibe.

## step 2 - first restaurant data

for now, i added a small hardcoded list of restaurants in python.

i did this first instead of connecting a real api because i wanted to understand the recommendation logic before adding more complicated stuff.

each restaurant is stored as a dictionary with fields like:
- name
- city
- cuisine
- price
- rating
- vibe

all of the restaurant dictionaries are stored inside a list called `restaurants`.


## step 3 - first filter function

i created a function called `find_restaurants(cuisine, max_price)`.

this function loops through the restaurant list and checks:
- if the cuisine matches
- if the restaurant is within the user's budget

if both conditions are true, it adds that restaurant to a new list called `matches`.

at the end, it returns the matching restaurants.

## what i learned

from this step i learned:
- how to store structured data in python using dictionaries
- how to group multiple items in a list
- how to loop through a list with a `for` loop
- how to write a function that filters data
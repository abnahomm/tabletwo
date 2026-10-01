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

## step 4 - adding scores

i changed the restaurant logic so it does not just say match or no match anymore.

each restaurant now gets points based on how well it fits what the user wants.

for example, matching the cuisine and vibe gives more points, while being within budget and having a high rating also adds points.

after that, the restaurants are sorted from highest score to lowest.

i did it this way because a place can still be a good option even if it does not match every single preference.

## what i learned

- how to make one function handle scoring
- how to pass values between functions
- how to sort data based on a score
- how recommendation systems can rank choices instead of only filtering them

## step 5 - getting preferences from the user

before this step, i had the preferences hardcoded into the program.

for example, i was manually telling it to look for italian food with a certain price and vibe.

i changed that so the program now asks the user what they want when it runs.

the user can enter:
- the type of food they want
- their maximum price level
- the kind of vibe they are looking for

those answers are then passed into the recommendation function and used to score the restaurants.

i did this because i wanted the program to start feeling more like an actual app instead of just testing fixed values in the code.

## what i learned

- how to collect user input in python
- how to store user answers in variables
- how to convert text input into a number
- how to pass user input into functions
- how user preferences can change the results the program returns
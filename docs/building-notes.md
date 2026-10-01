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

## step 6 - allowing more than one vibe

since a restaurant can fit more than one vibe.

for example, a place can be romantic, chill, and upscale at the same time.

i changed the restaurant data so each restaurant now stores a list of vibes instead of just one.

the program now checks if the vibe the user entered is inside that list.

this makes the recommendation system more flexible and closer to how i want the real app to work.

## what i learned

- how to store multiple values in a list
- how to check if something exists inside a list
- how changing the data structure can make the recommendation logic better

## step 7 - adjusting the recommendation weights

while testing the program, i noticed that choosing japanese food gave several restaurants the same score even though only one of them was actually japanese.

this happened because cuisine and vibe were worth the same amount of points.

i changed cuisine to be worth more because if someone asks for a specific type of food, that should matter more than a restaurant just having the right vibe.

this helped me understand that recommendation systems are not only about adding features. the weights you give each preference can completely change the results.

## what i learned

- how scoring weights affect recommendations
- why some preferences should matter more than others
- how testing different inputs can expose problems in the logic
- how recommendation systems need tuning to give useful results

## step 8 - explaining the score

i changed the program so it shows why each restaurant got its score instead of only showing the number.

now it can show reasons like:
- matches cuisine
- within budget
- matches vibe
- high rating

## what i learned

- how a function can return multiple values
- how to store reasons with each result
- how to make recommendations easier to understand

## step 9 - validating user input

i added input validation for the price level so the program does not crash if someone enters the wrong thing.

now it keeps asking until the user enters 1, 2, or 3.

## what i learned

- how to use try and except
- how to prevent bad input from crashing a program
- how to keep asking for input until it is valid

## step 10 - fixing price filtering

while testing, i noticed expensive restaurants could still rank high even when the user picked a low budget.

i changed the logic so restaurants above the selected price level are removed before scoring.

i also started thinking about how vibe searches should understand related words instead of requiring an exact match.

## what i learned

- some preferences should be filters instead of scores
- testing results can expose problems with recommendation logic
- user input needs to be flexible instead of relying on exact words
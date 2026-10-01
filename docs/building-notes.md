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

## step 11 - matching related vibes

i changed the vibe logic so users do not have to type the exact same word stored for a restaurant.

for example, typing "relaxed" can still match a restaurant tagged as "chill" or "casual" if those words are in the same vibe group.

## what i learned

- how to group related words
- how to loop through nested lists
- how to make user input more flexible

## step 12 - using real restaurant data

i connected tabletwo to the yelp api so i can search real restaurants instead of using only the sample ones i added myself.

right now the search sends a location and cuisine to yelp and gets restaurant names and ratings back.

## what i learned

- how to make an api request with python
- how to send search parameters
- how to read json data
- how to keep my api key outside of the code

## step 13 - connecting the api to the main program

i connected the yelp search function to the main tabletwo program.

the user can now enter a city and type of food, and those preferences are sent to yelp to find real restaurants.

i also changed the test code in `yelp_api.py` so it only runs when i test that file directly.

## what i learned

- how to import a function from another python file
- how different files in a project can work together
- how user input can be sent to an external api


## step 14 - converting yelp data

i converted the restaurant data from yelp into a simpler format that tabletwo can use.

i kept yelp's `$`, `$$`, and `$$$` format for displaying price, but i also created a numeric price level behind the scenes so the program can compare it with the user's budget.

## what i learned

- how to reshape api data
- how to store one value in different formats
- how to keep display data separate from logic

## step 15 - filtering real restaurants by price

i connected the user's budget to the real restaurant data from yelp.

the program now compares the selected price level with each restaurant and removes places that are over budget.

if yelp does not have a price listed, i keep the restaurant in the results for now instead of automatically removing it.

## what i learned

- how to filter api results
- how to compare real data with user input
- how to handle missing api data

## step 16 - ranking real restaurants

i added a score to the real yelp results so tabletwo can rank restaurants instead of just showing them in the order they come back from the api.

right now the score uses rating and how well the restaurant's price matches the user's budget.

## what i learned

- how to score real api data
- how to sort restaurants by score
- how to show why a restaurant ranked higher

## step 17 - adding vibe to real restaurants

i started connecting the vibe system to real yelp results.

i use restaurant categories like sports bars, lounges, cafes, and cocktail bars to estimate different vibes.

this is still a basic version, but it lets real restaurants start getting vibe points.

## what i learned

- how to turn api categories into my own data
- how to add custom tags to real restaurant results
- how to combine api data with my own recommendation logic

## step 18 - making vibe input more flexible

i changed the vibe system so the user can type more natural phrases instead of needing one exact word.

for example, phrases like "good for a first date" or "somewhere we can watch the game" can now match the right vibe group.

## what i learned

- how to search for words inside user input
- how to make text input more flexible
- how keyword matching can make recommendations feel more natural

## step 19 - showing restaurant details

i added the restaurant address and yelp link to the results so the recommendations are actually useful after a restaurant is found.

the app now shows the restaurant, rating, price, score, address, link, and why it matched.

## what i learned

- how to display more data from an api response
- how to organize results so they are easier to understand
- how the same api data can be used for both scoring and display

## step 20 - adding maps and tiktok links

i added google maps and tiktok search links for each restaurant.

the links are built using the restaurant name and location so the user can quickly check directions or look up videos without searching everything manually.

## what i learned

- how to build dynamic urls with python
- how to format text safely for a url
- how to connect recommendation results to other platforms

## step 21 - starting the web backend

i started turning tabletwo from a terminal program into a web app by setting up a fastapi backend.

i created basic endpoints and ran the backend on a local server to make sure the api was working.

## what i learned

- what a backend api does
- how to create api endpoints with fastapi
- how to run a local web server
- how a frontend will eventually communicate with python

## step 22 - creating a recommendation endpoint

i created a `/recommendations` api endpoint that accepts the user's location, cuisine, budget, and vibe.

the endpoint searches yelp for real restaurants, filters out places above the user's budget, and returns the results as json.

i also fixed an issue where the backend could not find my `.env` file and learned how the api key gets loaded into the project.

## what i learned

- how api endpoints can accept user inputs
- how query parameters work
- how to return json from fastapi
- how environment variables are loaded
- how to debug a 500 server error

## step 23 - adding scoring to the api

i moved the restaurant scoring logic into the `/recommendations` api endpoint.

the backend now filters by budget, scores restaurants using rating, price, and vibe, explains why each restaurant matched, and sorts the results from highest score to lowest.

## what i learned

- how to move program logic into an api endpoint
- how to score api results before returning them
- how to sort json results by recommendation score
- how the backend can handle most of the recommendation logic
# TableTwo Build Notes

## step 1 - defining the project

i decided to build TableTwo as a simple python restaurant recommendation project.

the goal is to help two people figure out where to eat by comparing both of their preferences.

instead of building a full website, i wanted the project to focus on the actual recommendation logic.

## what i learned

- how to define a smaller project scope
- how to focus on one clear problem
- how to keep a project simple but still useful


## step 2 - setting up the project structure

i simplified the project into a few python files.

the project structure is:

tabletwo/
- main.py
- recommender.py
- yelp_api.py
- requirements.txt
- .env
- .gitignore
- README.md

each file has one main job.

## what i learned

- how to organize a python project
- why separating code into different files makes it easier to understand
- how to keep a project from becoming too complicated


## step 3 - connecting to the yelp api

i created yelp_api.py to handle requests to the Yelp API.

the program sends a location and food preference to Yelp and gets back real restaurant data.

the restaurant data includes things like:

- restaurant name
- rating
- price
- categories
- restaurant id

## what i learned

- how to make an api request in python
- how to use the requests library
- how to read json data from an api response
- how to separate api code from the rest of the project


## step 4 - protecting the api key

i stored my Yelp API key in a .env file instead of putting it directly inside the python code.

the program loads the key using python-dotenv.

i also added .env to .gitignore so the key does not get uploaded to github.

## what i learned

- what environment variables are
- why api keys should not be hardcoded
- how .gitignore keeps private files out of github
- how python can load values from a .env file


## step 5 - getting two restaurant searches

the program searches Yelp twice.

one search uses person 1's food preference and the second search uses person 2's food preference.

for example:

person 1:
italian

person 2:
japanese

the program gets restaurant results for both searches.

## what i learned

- how to reuse the same function with different inputs
- how to work with multiple api responses
- how to pass values between python files


## step 6 - combining restaurant results

i created logic that combines both Yelp searches.

restaurants are stored using their Yelp restaurant id so the same restaurant does not get added twice.

if a restaurant appears in both searches, the program remembers that it matched both food preferences.

## what i learned

- how to remove duplicate data
- how dictionaries can be used to organize results
- how sets can store multiple matching preferences
- why restaurant ids are useful for identifying unique restaurants


## step 7 - filtering by budget

i added a maximum price input.

the user chooses:

1 = $
2 = $$
3 = $$$

restaurants that are more expensive than the selected budget are removed.

restaurants with no listed price are still allowed.

## what i learned

- how to filter a list of results
- how to use conditionals for user preferences
- how to convert Yelp's price symbols into a simple number


## step 8 - creating the recommendation score

i created a custom scoring system for each restaurant.

restaurants get points for things like:

- high rating
- matching the selected budget
- matching person 1's food
- matching person 2's food
- matching person 1's vibe
- matching person 2's vibe

the score is used to compare restaurants.

## what i learned

- how to create a simple recommendation algorithm
- how to turn different preferences into points
- how scoring can be used to compare multiple options


## step 9 - adding vibe matching

i added basic vibe categories like:

- romantic
- chill
- lively
- upscale
- casual

each vibe is connected to Yelp restaurant categories.

for example, wine bars can help match a romantic or upscale vibe.

## what i learned

- how to group related values
- how to compare restaurant categories to user preferences
- how simple rules can be used for recommendation logic


## step 10 - sorting the recommendations

after each restaurant gets a score, the results are sorted from highest score to lowest score.

the highest scoring restaurants appear first.

the program only prints the top results so the user is not overwhelmed with too many options.

## what i learned

- how to sort python lists
- how lambda functions can be used as a sorting key
- how ranking makes raw api data more useful


## step 11 - creating match labels

instead of showing users a confusing raw score, the program turns the score into a simple label.

examples:

- great match
- good match
- possible match

this makes the results easier to understand.

## what i learned

- how to turn internal program data into user-friendly output
- why raw scores can be confusing
- how small changes can improve usability


## step 12 - building the command line program

i created main.py to handle the user interaction.

the program asks for:

- location
- person 1 food preference
- person 1 vibe
- person 2 food preference
- person 2 vibe
- maximum budget

after the user enters everything, main.py calls the recommendation code and prints the results.

## what i learned

- how to collect input from a user
- how to call functions from another python file
- how to format terminal output
- how to keep input/output code separate from recommendation logic


## step 13 - validating budget input

i added validation so the budget has to be:

1
2
or
3

if the user enters something else, the program asks again instead of crashing.

## what i learned

- how to use try and except
- how to validate user input
- how to prevent basic program crashes


## step 14 - handling errors

i added basic error handling around the recommendation search.

if the Yelp request fails, the program prints an error instead of completely crashing.

## what i learned

- how exceptions work in python
- why api requests can fail
- how to make a program handle errors more safely


## step 15 - creating requirements.txt

i created requirements.txt with the external python packages the project needs.

the project currently uses:

- requests
- python-dotenv

this makes it easier for someone else to install everything needed to run the project.

## what i learned

- what requirements.txt is used for
- how python projects list dependencies
- how someone else can recreate the project environment


## step 16 - cleaning the project

i removed the old react, typescript, fastapi, css, and frontend code.

the project now focuses only on python, the Yelp API, and the recommendation algorithm.

this made the project easier to understand and easier to explain.

## what i learned

- more code does not always make a project better
- how to reduce project scope
- why simple projects can still demonstrate programming skills


## step 17 - final project flow

the final program works like this:

1. the user enters two people's preferences
2. main.py sends those preferences to recommender.py
3. recommender.py asks yelp_api.py for restaurant data
4. yelp_api.py sends requests to Yelp
5. recommender.py combines the results
6. restaurants over budget are removed
7. each restaurant gets a recommendation score
8. the restaurants are sorted
9. main.py prints the best matches

## what i learned

- how different python files work together
- how data moves through a program
- how an external api can be used inside a recommendation system
- how to build a complete program from input to output
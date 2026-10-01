# TableTwo

TableTwo is a Python restaurant recommendation tool made for couples who cannot decide where to eat.

The program uses the Yelp API to find real restaurants and ranks them based on both people's preferences.

## What it does

TableTwo asks for:

- location
- person 1 food preference
- person 1 vibe
- person 2 food preference
- person 2 vibe
- maximum price

It then:

1. searches Yelp for both food preferences
2. combines the restaurant results
3. removes restaurants over the selected budget
4. scores restaurants based on rating, food preferences, and vibe
5. sorts the results
6. prints the top recommendations

## Technologies

- Python
- Yelp API
- Requests
- python-dotenv

## Project Structure

```text
tabletwo/
├── main.py
├── recommender.py
├── yelp_api.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
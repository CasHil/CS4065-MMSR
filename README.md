# Musical search engine based on context and emotion

## Backend
Run `cd backend` to switch to the backend folder. The backend is built using Flask.

### Create virtual environment
`python -m venv venv`
### Activate virtual environment
`venv\Scripts\activate`
### Install dependencies
`pip install -r requirements.txt`
### Start backend
`python main.py`

## Frontend
Run `cd frontend` to switch to the frontend folder. The frontend is built using Svelte. It retrieves a list of recommended songs from the backend, which are then used as queries to the Spotify API. The result of these queries is displayed as the song results for the user's query.

### Install dependencies
`npm i`
### Start the frontend
`npm run dev -- --open`

## Design
The backend has around 2000 songs, a list of sentiment keywords, and a list of nouns. 
Before it's ready to accept queries it goes through the list of nouns and sentiment keywords, and calculates the min and max distance that occours in each list, to the music columns "loudness", and "tempo". It then uses that to normalize the data, so it can compare it with the songs ratings. 
A user then types in a query, and it extracts sentiment keywords and nouns from the users query, and calculates their distances to the "loudness" and "tempo" columns. After normalizing these, and taking the average, it recommends the three songs that have the smallest distance.

This is just a simple proof of concept to analyze the music, and give different results based on the queries. It relies on semantic relationships between words, that probably aren't very strong for the actual music.

# Musical search engine based on context and emotion

## Backend
Run `cd backend` to switch to the backend folder. The backend is built using Flask.

## Create venv
python -m venv venv
## activate venv
venv\Scripts\activate.bat
## download dependencies
pip install -r requirements.txt
## start backend
python main.py

## Frontend
Run `cd frontend`, `npm i`, `npm run dev -- --open` to start the frontend. The frontend is built using Svelte.


## Design
The backend has around 2000 songs, a list of sentiment keywords, and a list of nouns. 
Before it's ready to accept queries it goes through the list of nouns and sentiment keywords, and calculates the min and max distance that occours in each list, to the music columns "loudness", and "tempo". It then uses that to normalize the data, so it can compare it with the songs ratings. 
A user then types in a query, and it extracts sentiment keywords and nouns from the users query, and calculates their distances to the "loudness" and "tempo" columns. After normalizing these, and taking the average, it recommends the three songs that have the smallest distance.

This is just a simple POC to analyze the music, and give different results based on the queries. It relies on semantic relationships between words, that probably aren't very strong for the actual music.
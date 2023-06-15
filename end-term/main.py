import pandas as pd
import math
from collections import Counter
import re
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_distances
from flask import Flask, request

from gensim.models import Word2Vec
import gensim.downloader as api
model = api.load("glove-wiki-gigaword-50")
most_sim = (model.most_similar("glass"))
WORD = re.compile(r"\w+")

df = pd.read_csv('million_song_subset.csv', sep='###')
df.drop(['time_signature', 'duration'], axis=1)
pd.options.display.max_columns = 10
df.head()


data_scaled = pd.DataFrame(df, columns=['danceability', 'energy', 'loudness', 'tempo', 'time_signature', 'segment_loudness_avg'
                                                ])



subset_columns = ['loudness', 'tempo']#['danceability', 'energy', 'loudness', 'tempo']
song_subset = data_scaled[subset_columns]

columns = subset_columns#['dance', 'energy', 'loudness', 'tempo']

normalized_songs=(song_subset-song_subset.mean())/song_subset.std()
    

def get_cosine(vec1, vec2):
    try:
        return model.similarity(vec1, vec2)
    except KeyError:
        return "N/A"
    
def find_max_values(keywords, columns):
    feeling_dict = {}
    for column in columns:
        min = (99, "")
        max = (0, "")
        for keyword in keywords:
            distance = get_cosine(column, keyword)
            if distance != "N/A":
                distance = abs(distance)
                if min[0] > distance:
                    min = (distance, keyword)
                if max[0] < distance:
                    max = (distance, keyword)
            feeling_dict[column] = {"min": min[1], "max": max[1], "distance": max[0] - min[0]}
    return feeling_dict


sentiment_list = []

with open("./feelings.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        sentiment_list.append(row[0])
## this is the one dict with all of the feelings
sentiment_dict = find_max_values(sentiment_list, columns)

situation_list = []

with open("./nounlist.csv", "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        situation_list.append(row[0])

situation_dict = find_max_values(situation_list, columns)

def get_keyword_weights_normalized(keyword, distances, columns):
    weights = {}
    for column in columns:
        ## first we get the distance, then we need to convert it to a weight
        distance = distances[column]
        distance_to_min = abs(get_cosine(distance["min"], keyword))
        if distance["distance"] == 0.0:
            normalized_weight = 1.0
        else:
            normalized_weight = (distance["distance"] - distance_to_min) / distance["distance"]
        weights[column] = normalized_weight
    return weights

## recommends a song based a vector, and the distance to a songs vector
def recommend_songs(song_vector):
    song_vector = np.array(list(song_vector.values()))
    distances = cosine_distances(normalized_songs, [song_vector])
    ## find indicies of the rows with smallest distance
    min_distance_indices = np.argsort(distances, axis=0)[:10].flatten()
    ## retrieve rows
    rows_with_min_distances = df.loc[df.index[min_distance_indices]]
    ## extract songtitles
    song_titles = [song_title[2:-1] for song_title in rows_with_min_distances['song_title']]
    return song_titles

def is_words_valid(situation_keywords, sentiment_keywords):
    for sentiment_keyword in sentiment_keywords:
        if sentiment_keyword not in sentiment_list:
            raise ValueError("Invalid sentiment keyword: " + sentiment_keyword)
    for situation_keyword in situation_keywords:
        if situation_keyword not in situation_keywords:
            raise ValueError("Invalid situation keyword: " + situation_keyword)

    return (situation_keywords, sentiment_keywords)    

print("Welcome to the greatest song recommendation system in existence! I will be your guide on your journey to your musical discovery!")
print("At the moment, we only support select words, very sorry!")
print("\n")
print("                         ,' __ ``.._..''   `.")
print("                         `.`. ``-.___..-.    :")
print(" ,---..____________________>/          _,'_  |")
print(" `-:._,:_|_|_|_|_|_|_|_|_|_|.:SSt:.:|-|(/  |")
print("                        _.' )   ____  '-'    ;")
print("                       (    `-''  __``-'    /")
print("                        ``-....-''  ``-..-''")
print("\n")


app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def post_endpoint():
    data = request.get_json()
    situation_keywords = data.get('situation_keywords')
    sentiment_keywords = data.get('sentiment_keywords')
    weights_summed = {}
    try:
        is_words_valid(situation_keywords, sentiment_keywords)
    except ValueError as e:
        return str(e), 400
    ## initilaize
    for column in columns:
        weights_summed[column] = 0
    ## sum up
    for keyword in situation_keywords:
        keyword_weights = get_keyword_weights_normalized(keyword, situation_dict, columns)
        for key, weight in keyword_weights.items():
            weights_summed[key] += weight
    for keyword in sentiment_keywords:
        keyword_weights = get_keyword_weights_normalized(keyword, sentiment_dict, columns)
        for key, weight in keyword_weights.items():
            weights_summed[key] += weight
    ## normalize
    for weight in weights_summed:
        weights_summed[weight] = weights_summed[weight] / len(situation_keywords) + len(sentiment_keywords)
    if len(weights_summed) < 0:
        return "no valid song", 400
    data = {"songs": recommend_songs(weights_summed)}
    return data, 200
        

if __name__ == '__main__':
    app.run()
    
    
## run locally:

def prompt_user():
    situation_keywords = ["home", "car"]
    sentiment_keywords = ["happy", "sad"]
    situation_keywords = input("Input some keywords related to the situation comma seperated: ").split(",")
    sentiment_keywords = input("Input some keywords related to the sentiment/feelings comma seperated: ").split(",")
    for sentiment_keyword in sentiment_keywords:
        if sentiment_keyword not in sentiment_list:
            print("You used a sentiment keyword not in the list, please do try agian good sir")
            return [], []
    for situation_keyword in situation_keywords:
        if situation_keyword not in situation_keywords:
            print("You used a situation keyword not in the list, please do try agian good sir")
            return [], []
    return (situation_keywords, sentiment_keywords)

# while True:
#     situation_keywords, sentiment_keywords = prompt_user()
#     weights_summed = {}
#     if len(situation_keywords) + len(sentiment_keywords) > 0:
#         ## initilaize
#         for column in columns:
#             weights_summed[column] = 0
#         ## sum up
#         for keyword in situation_keywords:
#             keyword_weights = get_keyword_weights_normalized(keyword, situation_dict, columns)
#             for key, weight in keyword_weights.items():
#                 weights_summed[key] += weight
#         for keyword in sentiment_keywords:
#             keyword_weights = get_keyword_weights_normalized(keyword, sentiment_dict, columns)
#             for key, weight in keyword_weights.items():
#                 weights_summed[key] += weight
#         ## normalize
#         for weight in weights_summed:
#             weights_summed[weight] = weights_summed[weight] / len(situation_keywords) + len(sentiment_keywords)
#         if len(weights_summed) > 0:
#             song = recommend_song(weights_summed)
#             print(song)
            
    
    # Do something with the keywords
    # You can add your logic here to process or analyze the input keywords
    

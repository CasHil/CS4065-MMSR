from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('million_song_subset.csv', sep='###')
df.drop(['time_signature', 'duration'], axis=1)
pd.options.display.max_columns = 10
df.head()

df1 = df.drop(['duration', 'year', 'energy', 'danceability'], axis=1)

scaler = MinMaxScaler()
data_final = df1.drop(['song_id', 'song_title'], axis=1)
model = scaler.fit(data_final)
scaled_data = model.transform(data_final)

data_scaled = pd.DataFrame(scaled_data, columns=['loudness', 'tempo', 'time_signature', 'segment_loudness_avg',
                                                 'chroma1', 'chroma2', 'chroma3', 'chroma4', 'chroma5', 'chroma6',
                                                 'chroma7', 'chroma8', 'chroma9', 'chroma10', 'chroma11', 'chroma12',
                                                 'MFCC1', 'MFCC2', 'MFCC3', 'MFCC4', 'MFCC5', 'MFCC6', 'MFCC7', 'MFCC8',
                                                 'MFCC9', 'MFCC10', 'MFCC11', 'MFCC12'])
data_scaled.head()

kmeans = KMeans(n_clusters=10)
k_fit = kmeans.fit(data_scaled)

pd.options.display.max_columns = 13
predictions = k_fit.labels_
data_scaled['clusters'] = predictions
data_scaled.head(5)


pca = PCA(2)
pca_data = pd.DataFrame(pca.fit_transform(
    data_scaled.drop(['clusters'], axis=1)), columns=['PC1', 'PC2'])
pca_data['clusters'] = predictions

plt.figure(figsize=(10, 10))
sns.scatterplot(data=pca_data, x='PC1', y='PC2',
                hue='clusters', palette='Set2', alpha=0.9)
plt.title('Music Recommendation after PCA')
plt.show()

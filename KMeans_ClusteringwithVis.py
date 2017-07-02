import random
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import defaultdict
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.style.use('ggplot')
matplotlib.rc('font', **{
    'family': 'DejaVu Sans',
    'weight': 'normal'
})
plt.style.use('bmh')

df = pd.read_csv('tweets.csv')

hashtags_freq = defaultdict(int)
for index, tweet in df.iterrows():
    hashtags_freq[tweet.hashtag_id] += 1

for hashtag_id in hashtags_freq:
    if hashtags_freq[hashtag_id] < 10:
        hashtags_freq[hashtag_id] += random.random() * 5

# print hashtags_freq.items()

grouped = df.groupby('tweet_id', as_index=False).apply(lambda data: list(data.hashtag_id))

hashtags_count = len(hashtags_freq)

hashtags_groups = defaultdict(list)
for hashtag_id in hashtags_freq:
    for items in grouped:
        if hashtag_id in items:
            hashtags_groups[hashtag_id] += items

hashtags_centrality = defaultdict(int)
for hashtag_id in hashtags_groups:
    hashtags_centrality[hashtag_id] = (len(set(hashtags_groups[hashtag_id])) - 1) / (float(hashtags_count) - 1.0)
    hashtags_centrality[hashtag_id] += random.random() * 0.01

# print hashtags_centrality.items()

combined = [(hashtag_id, hashtags_freq[hashtag_id], hashtags_centrality[hashtag_id]) for hashtag_id in hashtags_freq]
df2 = pd.DataFrame(combined, columns=['hashtag_id', 'freq', 'centrality'])


#plt.figure(figsize=(17,6))
#plt.xlim([-10, 100])
#plt.ylim([0, 0.12])
#plt.xticks(np.arange(0, 100, 10))
#plt.title('Hashtags')
#plt.xlabel('hashtag frequency')
#plt.ylabel('hashtag degree centrality')
#plt.scatter(df2.freq, df2.centrality, s=100)

# hierarchical clustering ward method
Z2=hierarchy.ward(df2[['freq', 'centrality']])
plt.figure()
dn = hierarchy.dendrogram(Z2,orientation='top', labels=list(df['hashtag']),color_threshold='180,0')
plt.show()

# clustering kMeans
K = 3
model = KMeans(n_clusters=K)
model.fit(df2[['freq', 'centrality']])
# cluster result
df2['labels'] = model.labels_
df2.to_csv('metrics.csv')
#print df2


plt.figure(figsize=(17, 8))
plt.xlim([-10, 100])
plt.ylim([0, 0.12])
plt.xticks(np.arange(0, 100, 10))
plt.title('Hashtags')
plt.xlabel('hashtag frequency')
plt.ylabel('hashtag degree centrality')

for i in range(K):
    # select only data observations with cluster label == i
    ds = df2[df2['labels'] == i]

    # plot the data observations
    plt.plot(ds.freq, ds.centrality, '*', label='cluster {} - {} points'.format(i, len(ds)), ms=15)

    # plot the centroids
    lines = plt.plot(model.cluster_centers_[i, 0], model.cluster_centers_[i, 1], 'kx')
    plt.setp(lines, ms=15.0)
    plt.setp(lines, mew=2.0)

plt.legend(loc=2)
plt.show()
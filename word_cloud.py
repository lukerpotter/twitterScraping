from matplotlib import pyplot as plt
from wordcloud import WordCloud

search_term = "luke"

with open(f"clean_tweets_{search_term}.txt", 'r') as file:
    text = file.read()

word_cloud = WordCloud(collocations=False, background_color='white').generate(text)

plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()

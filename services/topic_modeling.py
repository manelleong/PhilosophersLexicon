from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import PCA

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

import json


def chunkify(text, length):
    tokenized_text = text.split(" ")
    loops = len(tokenized_text)//length

    chunks = [" ".join(tokenized_text[i*length:(i+1)*length]) for i in range(loops)]

    return chunks

# this version of chunkify returns the same number of chunks regardless of text length
def evenchunkify(text, chunk_count):
    tokenized_text = text.split(" ")
    
    words_per_chunk = len(tokenized_text) // chunk_count

    chunks = [" ".join(tokenized_text[i * words_per_chunk:(i + 1) * words_per_chunk]) for i in range(chunk_count)]

    return chunks

def makeGraph(selected_philosophers, selected_settings):
    stop_words = set(stopwords.words('english'))

    authors = []
    texts = []

    for philosopher in selected_philosophers:
        with open(f'data/{philosopher}/{philosopher}.txt') as file:
            text = file.read()
        
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in stop_words]
        text = " ".join(filtered_words)

        if len(selected_settings) > 2: # we are using even chunking
            chunks = evenchunkify(text, int(selected_settings[1]))
        else:
            chunks = chunkify(text, int(selected_settings[1]))

        texts.extend(chunks)

        for _ in range(len(chunks)):
            authors.append(philosopher)

    vectorizer = TfidfVectorizer(use_idf = False, max_features = int(selected_settings[0]))

    frequencies = vectorizer.fit_transform(texts)

    pca = PCA(n_components = 2)

    my_pca = pca.fit_transform(frequencies.toarray())
    frequencies.toarray().shape

    pc1 = my_pca[:,0]
    pc2 = my_pca[:,1]

    loadings = pca.components_
    vocabulary = vectorizer.get_feature_names_out()

    loadings_data = {"vocab" : [], "x" : [], "y" : []}

    for i, vocab in enumerate(vocabulary):
        loadings_data["vocab"].append(vocab)
        loadings_data["x"].append(loadings[0, i])
        loadings_data["y"].append(loadings[1, i])

    loadings_df = pd.DataFrame(loadings_data)

    data = {"authors" : authors, "pc1" : pc1, "pc2" : pc2}

    df = pd.DataFrame(data)

    fig = px.scatter(df, x='pc1', y = 'pc2', color = 'authors')

    fig.add_trace(go.Scatter(x = loadings_df["x"], y = loadings_data["y"], mode = "text", 
                         text = loadings_df["vocab"]))
    
    fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    legend_title_text = 'Legend'
    )

    fig.data[-1].name = 'Words'

    vocabulary = [f"'{word}'" for word in vocabulary]

    return fig, ", ".join(vocabulary)

def getWordData(selected_philosophers):
    output = ""
    for philosopher in selected_philosophers:
        with open(f'data/{philosopher}/{philosopher}.json', 'r') as file:
            json_object = json.load(file)

        output += f"{philosopher}: word count: {json_object['word_count']} unique word count: {json_object['unique_word_count']} top ten words: {json_object['top_ten']}\n"
        
    return output
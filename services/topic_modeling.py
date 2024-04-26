

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import PCA

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

def chunkify(text, length):
    tokenized_text = text.split(" ")
    loops = len(tokenized_text)//length

    chunks = [" ".join(tokenized_text[i*length:(i+1)*length]) for i in range(loops)]

    return chunks

def makeGraph(selected_philosophers):
    stop_words = set(stopwords.words('english'))

    authors = []
    texts = []

    for philosopher in selected_philosophers:
        with open(f'data/{philosopher}/{philosopher}.txt') as file:
            text = file.read()
        
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in stop_words]
        text = " ".join(filtered_words)

        chunks = chunkify(text, 1000)
        texts.extend(chunks)

        for _ in range(len(chunks)):
            authors.append(philosopher)

    vectorizer = TfidfVectorizer(use_idf = False, max_features = 30)

    frequencies = vectorizer.fit_transform(texts)

    pca = PCA(n_components = 2)

    my_pca = pca.fit_transform(frequencies.toarray())
    frequencies.toarray().shape

    pc1 = my_pca[:,0]
    pc2 = my_pca[:,1]

    loadings = pca.components_
    vocabulary = vectorizer.get_feature_names_out()

    print(vocabulary)

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
    
    return fig
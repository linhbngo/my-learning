from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
import zipfile


sentences = []
with zipfile.ZipFile("../../data/aristo-mini-corpus.zip", "r") as z:
    with z.open("Aristo-Mini-Corpus-Dec2016.txt") as file:
        for line in file:
          text_line = line.decode("utf-8").lower()
          line_words = re.findall(r"[a-zA-Z]+", text_line)
          sentences.append(line_words)  

# 2. Train a small Word2Vec model
# vector_size = 50 to be representative enough
# window = 5 to ensure that the sliding context window can avoid generic surrounding words
# min_count= 5 to remove low occurence words that can cause noise.
# sample=1e-3 to down-weight high frequency stop words. 
# epochs=10 to avoid overtrainning
model = Word2Vec(sentences, vector_size=10, window=3, min_count=1, seed=42, sample=1e-3, workers=4, epochs=10)

# 3. Extract the raw embedding vectors
eagle_vec = model.wv['eagle'].reshape(1, -1)
goose_vec = model.wv['goose'].reshape(1, -1)
duck_vec = model.wv['duck'].reshape(1, -1)
squirrel_vec = model.wv['squirrel'].reshape(1, -1)

# 4. Print the raw numeric vectors
print("=== RAW WORD EMBEDDINGS (4 Dimensions) ===")
print(f"Eagle vector:    {np.round(eagle_vec[0], 4)}")
print(f"Goose vector:    {np.round(goose_vec[0], 4)}")
print(f"Duck vector:     {np.round(duck_vec[0], 4)}")
print(f"Squirrel vector: {np.round(squirrel_vec[0], 4)}")
print("\n" + "="*40 + "\n")

# 5. Calculate Cosine Similarity (1.0 means identical direction, 0.0 means orthogonal/unrelated)
def get_similarity(vec1, vec2):
    return cosine_similarity(vec1, vec2)[0][0]

print("=== COSINE SIMILARITY SCORES ===")
print(f"Goose vs Duck:     {get_similarity(goose_vec, duck_vec):.4f}  (Very High - both are water birds)")
print(f"Eagle vs Goose:    {get_similarity(eagle_vec, goose_vec):.4f}  (Moderate/High - both are flying birds)")
print(f"Eagle vs Duck:     {get_similarity(eagle_vec, duck_vec):.4f}  (Moderate/High - both are flying birds)")
print("-" * 40)
print(f"Squirrel vs Duck:  {get_similarity(squirrel_vec, duck_vec):.4f} (Low - completely different context)")
print(f"Squirrel vs Goose: {get_similarity(squirrel_vec, goose_vec):.4f} (Low - completely different context)")
print(f"Squirrel vs Eagle: {get_similarity(squirrel_vec, eagle_vec):.4f} (Low - completely different context)")


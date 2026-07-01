from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
from datasets import load_dataset
import pickle
import os
import sys
from collections import Counter

CACHE_FILE = "../../data/wikitext_processed_words.pkl"


sentences = []

if os.path.exists(CACHE_FILE):
    print(f"Loading processed words from local cache: {CACHE_FILE}")
    with open(CACHE_FILE, "rb") as f:
        sentences = pickle.load(f)
else:
    dataset = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split = "train")
    for item in dataset:
        line = item["text"].strip()
        if not line:
            continue
        text_line = line.lower()
        line_words = re.findall(r"[a-z]+", text_line)
        if line_words:
            sentences.append(line_words)
    print(f"Saving processed words to local cache: {CACHE_FILE}")
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(sentences, f, protocol = pickle.HIGHEST_PROTOCOL)
# 2. Train a small Word2Vec model
# vector_size = 50 to be representative enough
# window = 5 to ensure that the sliding context window can avoid generic surrounding words
# min_count= 5 to remove low occurence words that can cause noise.
# sample=1e-3 to down-weight high frequency stop words. 
# epochs=10 to avoid overtrainning
#

if sys.platform == "darwin":
    sys.stderr = open(os.devnull,"w")

model = Word2Vec(sentences, vector_size=50, window=5, min_count=5, seed=42, sample=1e-3, workers=8, epochs=10)

if sys.platform == "darwin":
    sys.stderr.close()
    sys.stderr = sys.__stderr__

# 3. Extract the raw embedding vectors
#eagle_vec = model.wv['eagle'].reshape(1, -1)
#goose_vec = model.wv['goose'].reshape(1, -1)
#duck_vec = model.wv['duck'].reshape(1, -1)
#squirrel_vec = model.wv['squirrel'].reshape(1, -1)

eagle_vec = model.wv.get_vector('eagle', norm = True).reshape(1, -1)
goose_vec = model.wv.get_vector('goose', norm = True).reshape(1, -1)
duck_vec = model.wv.get_vector('duck', norm = True).reshape(1, -1)
squirrel_vec = model.wv.get_vector('squirrel', norm = True).reshape(1, -1)

# 5. Calculate Cosine Similarity (1.0 means identical direction, 0.0 means orthogonal/unrelated)
def get_similarity(vec1, vec2):
    return cosine_similarity(vec1, vec2)[0][0]

print("=== COSINE SIMILARITY SCORES ===")
print(f"Goose vs Duck:     {get_similarity(goose_vec, duck_vec):.4f}  (Expect very High - both are water birds)")
print(f"Eagle vs Goose:    {get_similarity(eagle_vec, goose_vec):.4f}  (Expect moderate/High - both are flying birds)")
print(f"Eagle vs Duck:     {get_similarity(eagle_vec, duck_vec):.4f}  (Expect moderate/High - both are flying birds)")
print("-" * 40)
print(f"Squirrel vs Duck:  {get_similarity(squirrel_vec, duck_vec):.4f} (Expect low - completely different context)")
print(f"Squirrel vs Goose: {get_similarity(squirrel_vec, goose_vec):.4f} (Expect low - completely different context)")
print(f"Squirrel vs Eagle: {get_similarity(squirrel_vec, eagle_vec):.4f} (Expect low - completely different context)")

print(f"Total processed lines/sentences: {len(sentences)}")
print(f"Example line: {sentences[0] if sentences else 'Empty'}")

# Count the frequencies to verify your animals exist here
flat_words = [word for line in sentences for word in line]
word_counts = Counter(flat_words)

targets = ["goose", "duck", "squirrel", "eagle"]
print("\n=== NEW ANIMAL COUNTS ===")
for animal in targets:
    print(f"{animal.capitalize()}: {word_counts[animal]} times")

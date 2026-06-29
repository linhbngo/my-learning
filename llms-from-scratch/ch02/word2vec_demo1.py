from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 1. Prepare dummy training data to give the model contextual clues
# Word2Vec learns meaning by seeing which words frequently share similar neighbors.
sentences = [
    ["the", "eagle", "flew", "high", "in", "the", "sky"],
    ["a", "wild", "goose", "flew", "over", "the", "lake"],
    ["the", "mallard", "duck", "flew", "and", "swam", "in", "the", "pond"],
    ["goose", "and", "duck", "are", "birds", "that", "fly"],
    ["eagle", "is", "a", "large", "bird", "of", "prey"],
    
    ["the", "furry", "squirrel", "climbed", "up", "the", "oak", "tree"],
    ["a", "squirrel", "gathers", "nuts", "and", "acorns", "on", "the", "ground"],
    ["the", "gray", "squirrel", "scampered", "forest", "tree"]
]

# 2. Train a small Word2Vec model
# vector_size=4 gives us small, readable 4-dimensional embedding vectors.
# min_count=1 ensures none of our specific words get filtered out.
model = Word2Vec(sentences, vector_size=4, window=3, min_count=1, seed=42, workers=1, epochs=500)

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


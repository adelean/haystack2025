import numpy as np
import json
from sklearn.cluster import KMeans

def bbq_quantize(vectors, n_clusters=256):
    """
    Perform BBQ quantization: quantize vectors into binary codes.
    Each vector is quantized into n_clusters binary codes.

    Parameters:
    - vectors: ndarray, input vectors of shape (num_samples, num_features)
    - n_clusters: int, number of clusters for quantization

    Returns:
    - binary_codes: ndarray, quantized binary vectors of shape (num_samples, n_clusters)
    """
    # Perform KMeans clustering for BBQ quantization
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(vectors)
    
    # Convert cluster centers to binary codes
    quantized_vectors = kmeans.predict(vectors)
    
    # Convert to binary codes (0 or 1)
    binary_codes = np.zeros((len(vectors), n_clusters), dtype=np.uint8)
    for i, quantized_vector in enumerate(quantized_vectors):
        binary_codes[i, quantized_vector] = 1
    
    return binary_codes


    

# Example: Loading your vectorized dataset (replace with your actual vector data)
# This is a placeholder for your actual vector data (e.g., embeddings from Sentence Transformers)
# vectors = np.array([your_data_here]) 

# Assuming your vectorized dataset is already in `vectors`, otherwise load it:
# vectors = np.load('your_vectors_file.npy')  # Example: loading pre-saved vectors

# Example dataset - Replace with your own vectorized data
vectors = np.random.rand(1000, 384)  # 1000 vectors of size 384, replace with your actual vectors

# Apply BBQ Quantization
bbq_quantized_vectors = bbq_quantize(vectors, 384)

# Prepare bulk index data for Elasticsearch
bulk_index_data_bbq = []
for idx, embed in enumerate(bbq_quantized_vectors):
    bulk_index_data_bbq.append({
        "index": {"_index": "demo_bqq_quantized", "_id": idx}
    })
    bulk_index_data_bbq.append({
        "vec": embed.tolist()  # The quantized binary code to be stored
    })

# Save to file for bulk indexing in Elasticsearch
with open('../output/bulk_bqq_quantized.json', 'w') as file:
    for entry in bulk_index_data_bbq:
        file.write(json.dumps(entry) + '\n')

print("BBQ Quantized data prepared and saved to 'bulk_bqq_quantized.json'")

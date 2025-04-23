import numpy as np
import json
from sklearn.cluster import KMeans

def pq_quantize(vectors, n_subvectors=8, n_clusters=256):
    """
    Perform Product Quantization (PQ) on the input vectors.

    Parameters:
    - vectors: ndarray of shape (n_samples, dim)
    - n_subvectors: int, number of subvectors to split each vector into
    - n_clusters: int, number of clusters per subvector

    Returns:
    - quantized_codes: ndarray of shape (n_samples, n_subvectors)
    """
    n_samples, dim = vectors.shape
    assert dim % n_subvectors == 0, "Vector dimension must be divisible by number of subvectors"
    
    subv_len = dim // n_subvectors
    quantized_codes = np.zeros((n_samples, n_subvectors), dtype=np.uint8)
    kmeans_models = []

    for i in range(n_subvectors):
        subvectors = vectors[:, i * subv_len:(i + 1) * subv_len]
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(subvectors)
        codes = kmeans.predict(subvectors)
        quantized_codes[:, i] = codes
        kmeans_models.append(kmeans)

    return quantized_codes





# Example: random vector dataset
vectors = np.random.rand(1000, 384)  # 1000 vectors of dimension 384

# PQ Quantization
pq_codes = pq_quantize(vectors, n_subvectors=8, n_clusters=256)

# Prepare bulk data for Elasticsearch
bulk_index_data_pq = []
for idx, code in enumerate(pq_codes):
    bulk_index_data_pq.append({
        "index": {"_index": "demo_pq_quantized", "_id": idx}
    })
    bulk_index_data_pq.append({
        "pq_code": code.tolist()
    })

# Save to file
with open('../output/bulk_pq_quantized.json', 'w') as file:
    for entry in bulk_index_data_pq:
        file.write(json.dumps(entry) + '\n')

print("PQ Quantized data saved to 'bulk_pq_quantized.json'")

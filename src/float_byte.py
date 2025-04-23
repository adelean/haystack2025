import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('../resources/demo_questions_1000.json', 'r') as file:
    bulk_data = json.load(file)

questions = [item['question'] for idx, item in enumerate(bulk_data) if idx % 2 != 0]

embeddings = model.encode(questions)

# Normalize the embeddings to [0, 1] for byte quantization
scaler = MinMaxScaler()
scaled_embeddings = scaler.fit_transform(embeddings)

# Convert scaled embeddings to byte (0-255 range)
byte_embeddings = np.round(scaled_embeddings * 255 - 128).astype(np.int8)

# Create bulk index payload for Elasticsearch (without quantization)
bulk_index_data_float = []
for idx, embed in enumerate(embeddings):
    bulk_index_data_float.append({
        "index": {"_index": "demo_float_hnsw", "_id": idx}
    })
    bulk_index_data_float.append({
        "vec": embed.tolist()
    })

# Create bulk index payload for Elasticsearch (with byte quantization)
bulk_index_data_byte = []
for idx, embed in enumerate(byte_embeddings):
    bulk_index_data_byte.append({
        "index": {"_index": "demo_byte_ext_hnsw", "_id": idx}
    })
    bulk_index_data_byte.append({
        "vec": embed.tolist()
    })

with open('../output/bulk_float_hnsw.json', 'w') as file:
    for entry in bulk_index_data_float:
        file.write(json.dumps(entry) + '\n')

with open('../output/bulk_byte_hnsw.json', 'w') as file:
    for entry in bulk_index_data_byte:
        file.write(json.dumps(entry) + '\n')


print("Files ready: 'bulk_float_hnsw.json' and 'bulk_byte_hnsw.json'")

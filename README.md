# Haystack 2025

## 🛠️ Setup Instructions

### 1. Fire up elasticsearch and kibana
Use the docker-compose file to start an instance of a single node elasticsearch and kibana v8.17.0
```
docker-compose up -d'
```

### 2. Create Index Mappings

First, create the index mappings in Elasticsearch.  
You can refer to the mapping definitions in the file:

```
/resources/index_mappings.json
```


---

### 3. Generate Bulk Insert Files

Run the following scripts to prepare JSON files for indexing:

#### 🔹 Float & Byte Vectors
```
python float_byte.py
```
This script generates JSON files with both float and byte vectors for bulk insert.

🔹 BBQ Quantization
```
python bbq_quantization.py
```
This script generates JSON bulk files for BBQ (Binary-based Quantization).

🔹 Product Quantization (PQ)
```
python pq_quantization.py
```
This script generates JSON bulk files for Product Quantization (PQ).

### 4. Insert Data into Elasticsearch
Once the JSON files are ready, use the script below to insert everything into Elasticsearch:

```
./bulk_insert_es.sh
```
### 5. Verify Index Sizes
After indexing, you can compare the storage sizes for each type of vector data by calling:

```
GET _cat/indices/*demo*?v&s=store.size:desc
```
This will return a list of all your *demo* indices, sorted by their size in descending order.

✅ Done! You now have an indexed vector dataset in various formats, ready for experimentation or benchmarking.

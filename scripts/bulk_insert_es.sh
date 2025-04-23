#!/bin/bash

echo "Uploading bulk_float_hnsw.json..."
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @../output/bulk_float_hnsw.json
echo "\nDone uploading bulk_float_hnsw.json"

echo "Uploading bulk_byte_hnsw.json..."
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @../output/bulk_byte_hnsw.json
echo "\nDone uploading bulk_byte_hnsw.json"

echo "Uploading bulk_bqq_quantized.json..."
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @../output/bulk_bqq_quantized.json
echo "\nDone uploading bulk_bqq_quantized.json"

echo "Uploading bulk_pq_quantized.json..."
curl -X POST "localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @../output/bulk_pq_quantized.json
echo "\nDone uploading bulk_pq_quantized.json"

echo "All files uploaded successfully."

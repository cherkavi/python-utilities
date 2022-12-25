# pip install elasticsearch==7.10.1

# Create an Elasticsearch client
es = Elasticsearch()

# Index a document with an ID of 1
es.index(index="my_index", doc_type="my_type", id=1, body={"name": "John Doe", "age": 34})

# Perform a search query
results = es.search(index="my_index", doc_type="my_type", body={"query": {"match": {"name": "John"}}})

# Print the results
print(results)

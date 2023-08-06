# Ananse

The ``Ananse`` package is a python implementation of the ``litsearchr`` R package  designed to partially automate search term selection and writing search strategies for systematic reviews. Read the documentation at [baasare.github.io/ananse](https://baasare.github.io/ananse/_build/html/index.html) and [ananse.readthedocs.io/](https://ananse.readthedocs.io/en/latest/)

## Setup
Ananse requires python 3.7 or higher


### Using pip

```bash
pip install ananse
```

### Directly from the repository

```bash
git clone https://github.com/baasare/ananse.git
python ananse/setup.py install
```

## Quick start        
### Writing your own script


```python
from ananse import Ananse
    
# Create an object of the package
review = Ananse()

# Import your naive search results from a directory 
imports = review.import_naive_results(path="./")

deduplication_columns =  ['title', 'abstract']

#de-duplicate the imported search results
data = review.deduplicate_dataframe(imports, deduplication_columns)

#extract keywords from article title and abstract as well as author and database tagged keywords
all_terms = review.extract_terms(data)

#create Document-Term Matrix, with columns as terms and rows as articles
dtm, term_columns = review.create_dtm(data.text, all_terms)

#create co-occurrence network using Document-Term Matrix
graph_network = review.create_network(dtm, term_columns)

#plot degree and rank distribution of the network
review.plot_degree_distribution(graph_network)
review.plot_rank_degree_distribution(graph_network)
review.plot_degree_histogram(graph_network)


#Determine cutoff for the relevant keywords
cutoff_strengths = review.find_cutoff(graph_network, "spline", "degree", degrees=2, knot_num=1, percent=0.8)

#reduce graph with only relevant keywords 
reduced_graph, nodes = review.reduce_graph(graph_network, "degree", cutoff_strengths)

#get suggested keywords and save to a csv file
suggested_keywords = review.get_keywords(reduced_graph, save_network=True )
for word in suggested_keywords:
   print(word)


```
### Using Ananse Test Script


```bash
python tests/ananse_test
```

## References

This is a python implementation of the R package as mentioned in paper [An automated approach to identifying search terms for systematic reviews using keyword co‐occurrence networks by Eliza M. Grames, Andrew N. Stillman  Morgan W. Tingley and Chris S. Elphick](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13268)
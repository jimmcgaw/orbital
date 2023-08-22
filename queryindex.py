#!/usr/bin/env python3

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

search_index = open_dir("apiserver/index")


with search_index.searcher() as searcher:
    parser = QueryParser("title", search_index.schema)
    my_query = parser.parse("interest")
    results = searcher.search(my_query)
    import pdb; pdb.set_trace()
    print(searcher.search(my_query))
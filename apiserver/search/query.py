import os

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.searching import Hit, Results


SEARCH_APP_PATH = os.path.dirname(__file__)
SEARCH_INDEX_PATH = os.path.join(SEARCH_APP_PATH, 'index')


class SearchIndex:
    def __init__(self):
        self.search_index = open_dir(SEARCH_INDEX_PATH)

    def query_index(self, search_text: str) -> list[dict]:
        results = []

        with self.search_index.searcher() as searcher:
            query_parser = QueryParser("title", self.search_index.schema)
            search_query = query_parser.parse(search_text)
            search_results = searcher.search(search_query)
            search_hit: Hit
            for search_hit in search_results:
                hit_dict = search_hit.fields()
                results.append({
                    "title": hit_dict["title"],
                    "description": hit_dict["description"],
                    "content": f"{hit_dict['content'][:100]}...",
                })
        return results

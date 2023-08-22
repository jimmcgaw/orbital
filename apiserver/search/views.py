import os
import time
from datetime import datetime

from django.http import HttpRequest, JsonResponse

from django.shortcuts import render

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.searching import Hit, Results


SEARCH_APP_PATH = os.path.dirname(__file__)
SEARCH_INDEX_PATH = os.path.join(SEARCH_APP_PATH, '../index')


search_index = open_dir(SEARCH_INDEX_PATH)


def _get_search_results(search_text: str) -> list[dict]:
    results = []
    with search_index.searcher() as searcher:
        query_parser = QueryParser("title", search_index.schema)
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



def query(request: HttpRequest) -> JsonResponse:
    start_time = time.time()
    search_text = request.GET.get('q', '')

    results: list[dict] = []
    if search_text:
        results.extend(
            _get_search_results(search_text)
        )

    response = {
        "timestamp": datetime.now(),
        "duration": f"{time.time() - start_time}s",
        "query": search_text,
        "results": results,
    }
    return JsonResponse(response, safe=False)
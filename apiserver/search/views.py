import time
from datetime import datetime

from django.http import HttpRequest, JsonResponse

# from django.shortcuts import render

from .query import SearchIndex


def query(request: HttpRequest) -> JsonResponse:
    start_time = time.time()
    search_text = request.GET.get('q', '')

    results: list[dict] = []
    if search_text:
        results.extend(
            SearchIndex().query_index(search_text)
        )

    response = {
        "timestamp": datetime.now(),
        "duration": f"{time.time() - start_time}s",
        "query": search_text,
        "results": results,
    }
    return JsonResponse(response, safe=False)
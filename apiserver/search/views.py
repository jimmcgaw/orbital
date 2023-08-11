import time
from datetime import datetime

from django.http import HttpRequest, JsonResponse

from django.shortcuts import render


def query(request: HttpRequest) -> JsonResponse:
    start_time = time.time()
    q = request.GET.get('q', '')
    response = {
        "timestamp": datetime.now(),
        "duration": f"{time.time() - start_time}s",
        "query": q,
        "results": [],
    }
    return JsonResponse(response, safe=False)
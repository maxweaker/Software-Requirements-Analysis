from django.http import JsonResponse
# Create your views here.
from django.core.cache import cache
def searchTest(request):
    if request.method == 'POST':
        pass
    return JsonResponse({"r":True})


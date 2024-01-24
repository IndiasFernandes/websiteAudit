from rest_framework.views import APIView  # import the APIView class from the rest_framework.views module. This is
# used to define API views.

from rest_framework.response import Response  # import the Response class from the rest_framework.response module.
# This is used to return a response from the API.

from rest_framework.decorators import api_view  # import the api_view decorator from the rest_framework.decorators
from report_generator.models import WebsiteReport
from report_generator.screenshot.takeScreenshot import take_screenshot
from .serializers import ItemSerializer

# module. This is used to define API views.

@api_view(['GET'])
def getData(request):
    items = WebsiteReport.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addItem(request):

    # add prints
    print(request.data)
    take_screenshot(request.data['url'])
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    else:
        return Response(serializer.errors, status=400)

from django.shortcuts import render

def form(request):
    return render(request, 'test.html')
#
#
# from .models import FormResponse
# from .serializers import FormResponseSerializer
#
#
# # Create your views here.
# # Views are the logic behind the API. They are responsible for processing the request and returning the response.
# # TODO: Define your views here
#
# class FormResponseView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = FormResponseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # Process data here and generate a report
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

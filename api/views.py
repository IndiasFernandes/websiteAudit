from rest_framework.views import APIView  # import the APIView class from the rest_framework.views module. This is
# used to define API views.

from rest_framework.response import Response  # import the Response class from the rest_framework.response module.
# This is used to return a response from the API.

from rest_framework.decorators import api_view  # import the api_view decorator from the rest_framework.decorators


# module. This is used to define API views.

@api_view(['GET'])
def getData(request):
    form = {'name': 'John Doe', 'email': 'john@mail.com', 'message': 'Hello World!', 'url': 'https://www.google.com'}
    return Response(form)
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

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FormResponse
from .serializers import FormResponseSerializer

# Create your views here.
# Views are the logic behind the API. They are responsible for processing the request and returning the response.
# TODO: Define your views here

class FormResponseView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FormResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Process data here and generate a report
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

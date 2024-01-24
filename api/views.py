from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from report_generator.models import WebsiteReport
from screenshot.takeScreenshot import take_screenshot, get_domain_from_url
from .serializers import ItemSerializer

# View para obter dados usando o Django Rest Framework
@api_view(['GET'])
def getData(request):
    items = WebsiteReport.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

# View para adicionar itens usando o Django Rest Framework
@api_view(['POST'])
def addItem(request):
    print(request.data)
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)

# View baseada em função para renderizar um formulário
def form(request):
    return render(request, 'test.html')

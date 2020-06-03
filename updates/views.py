from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from updates.models import Record
from updates.serializers import RecordSerializer


class MainPage(TemplateView):
    def get(self, request, **kwargs):
        
        latest_record = Record.objects.latest('timestamp')
        date = latest_record.date
        new_cases = latest_record.new_cases

        return render(
            request, 
            'index.html', 
            {
                'date': date,
                'new_cases': new_cases,
                'timestamp': latest_record.timestamp
            })


class RecordViewSet(viewsets.ModelViewSet):
    
    queryset = Record.objects.all().order_by('date')
    serializer_class = RecordSerializer
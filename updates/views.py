from django.shortcuts import render
from django.views.generic import TemplateView
from updates.models import Record
    

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

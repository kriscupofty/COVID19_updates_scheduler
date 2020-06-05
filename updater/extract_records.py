import tabula
import requests
import os.path
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from datetime import date, timedelta
from updates.models import Record
from django.conf import settings


holidays = [date(2020, 4, 10), date(2020, 4, 13), date(2020, 5, 18), 
                date(2020, 7, 1), date(2020, 8, 3), date(2020, 9, 7)]

def save_past_records(): 
    if len(Record.objects.all()) != 0:
        print("Database already populated")
        return

    # save today's case details csv
    df = pd.read_csv('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv')
    df.to_csv(os.path.join(settings.MEDIA_ROOT, 'case_details.csv'))  

    text = requests.get('http://www.bccdc.ca/health-info/diseases-conditions/covid-19/case-counts-press-statements').text
    names = re.findall(r'href="/Health-Info-Site/Documents/BC_Surveillance_(.*?).pdf"', text)

    urls = ['http://www.bccdc.ca/Health-Info-Site/Documents/BC_Surveillance_{}.pdf'.format(name) for name in names]
    urls.reverse()
    urls = urls[1:]

    sdate = date(2020, 3, 24)
    edate = date.today()
    print('today is ', edate)
    dates = [sdate + timedelta(days=i) for i in range((edate - sdate).days + 1)]

    new_cases = []
    url_iter = iter(urls)

    for d in dates:
        if d.weekday() < 5 and d not in holidays:
            try:
                url = next(url_iter)
                print('url: ', url)
            except:
                print('report for today yet to be released')
                new_cases.append('NA')
        else: 
            new_cases.append('Unavailable')
            print('data unavailable on a holiday')
            continue

        file_name = os.path.join(settings.MEDIA_ROOT, url.split('/')[-1]) 
        if not os.path.isfile(file_name):
            file = requests.get(url)
            open(file_name, 'wb').write(file.content)

        pages = 1
        if 'April_8' in file_name:
            area = (410, 38, 670.26, 569.379988861084)
        elif 'April_20' in file_name or 'April_21' in file_name:
            area = (360, 38, 670.26, 569.379988861084)
        elif dates.index(d) >= 48:
            area = (106, 40, 409, 571)
            pages = 2
        else:
            area = (395, 38, 670.26, 569.379988861084)

        try:
            df = tabula.read_pdf(file_name,
                                pages=pages, lattice=True, multiple_tables=False,
                                area=area)
            df = pd.DataFrame(df[0])
            df = df.replace({list(df.columns)[-1]: r'[^\d()\%//]'}, '', regex=True)

            new_cases_r = df[df.iloc[:, 0].astype(str).str.lower().str.contains("new cases")]
            if len(new_cases_r) == 0 and df.shape[1] > 1:
                new_cases_r = df[df.iloc[:, 1].astype(str).str.lower().str.contains("new cases")]

            if len(new_cases_r) == 0:
                df = tabula.read_pdf(file_name,
                                    pages=pages, lattice=True, multiple_tables=False,
                                    area=(380, 38, 670.26, 569.379988861084))
                df = pd.DataFrame(df[0])
                df = df.replace({list(df.columns)[-1]: r'[^\d()\%//]'}, '', regex=True)
                new_cases_r = df[df.iloc[:, 0].astype(str).str.lower().str.contains("new cases")]

            if len(new_cases_r) != 0:
                num = new_cases_r.iloc[0, -1]
                num = re.sub(r'\(.+?\)', '', num)
            else:
                num = 'NA'
            new_cases.append(num)
        except:
            new_cases.append('NA')
            print('Error parsing the pdf')

    for date_, num in zip(dates, new_cases):
        new_record = Record()
        new_record.date = date_
        new_record.new_cases = num

        new_record.save()
        print('Saving ', str(new_record))
    
    generate_new_cases_chart()
    print('Saved new chart')


def add_new_record():
    prev_total = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'case_details.csv')).shape[0]
    new_csv = pd.read_csv('http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv')
    new_total = new_csv.shape[0] 
    new_date = date.today()

    new_record = Record()
    new_record.date = new_date
    if new_date.weekday() < 5 and new_date not in holidays:
        new_record.new_cases = new_total - prev_total
    else:
        new_record.new_cases = 'Unavailable'

    new_record.save()
    print('Saving ', str(new_record))

    new_csv.to_csv(os.path.join(settings.MEDIA_ROOT, 'case_details.csv'))
    print('Saved new case_details.csv')

    generate_new_cases_chart()
    print('Saved new chart')


def generate_new_cases_chart():
    qs = Record.objects.all().order_by('date').values('date', 'new_cases')

    date_range = pd.date_range(start=qs[0]['date'], end=qs[len(qs)-1]['date'])

    df = pd.DataFrame(qs)
    df.date = pd.to_datetime(date_range)
    df = df.set_index('date')

    df.new_cases = pd.to_numeric(df.new_cases, errors='coerce')
    plt.bar(df.index, df.new_cases.values)
    plt.ylabel('number of new cases')
    plt.gcf().autofmt_xdate()
    plt.savefig(os.path.join(settings.MEDIA_ROOT, 'new_cases.png'), dpi=400)

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings
import os


download_path = os.path.join(settings.MEDIA_ROOT,'invoice.pdf')

def pdf(cont,path):
    template_render  = render_to_string(path, cont)
    html = HTML(string=template_render)
    html.write_pdf(target=download_path)

    fs = FileSystemStorage(settings.MEDIA_ROOT)
    with fs.open('invoice.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
    return response
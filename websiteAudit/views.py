from django.shortcuts import render
import os

from websiteAudit import settings


def display_stdout(request):
    log_file_path = os.path.join(settings.LOG_DIR, 'stdout.log')
    with open(log_file_path, 'r') as log_file:
        stdout_content = log_file.read()

    return render(request, 'stdout_display.html', {'stdout_content': stdout_content})




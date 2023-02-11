from django.shortcuts import render
from rest_framework.decorators import api_view
import sys
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from EmployeeApp.models import PitcherResume
from EmployeeApp.serializers import PitcherResumeSerializers
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django.shortcuts import redirect

import csv
import numpy as np



@api_view(['POST'])
@parser_classes((MultiPartParser, FileUploadParser))
def uploadResume(request):
    try:
        # pitcherResume = PitcherResume.objects.get(pitcher_id=request.data['id'])
        pitcherResume = PitcherResume()
        myFile = request.FILES['upload_resume']
        if myFile.size > settings.MAX_RESUME_UPLOAD_SIZE:
            return JsonResponse({'error': 1, 'path': '', 'message': 'Resume size is more than 5 MB.'})
        if myFile.size == 0:
            return JsonResponse({'error': 1, 'path': '', 'message': 'Resume size cannot be zero.'})
        fs = FileSystemStorage(location=settings.PITCHER_PROJECT_STORAGE, file_permissions_mode=0o644)
        # find out extension of file being uploaded
        fileName, extension = os.path.splitext(myFile.name)
        # check for valid Resume mime types
        if extension not in settings.ALLOWED_RESUME_TYPES:
            return JsonResponse({'error': 1,
                                    'path': '',
                                    'message': 'The format of resume that you are trying to upload, is not supported.'
                                    })
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        newFileName = str(now) + "_" + str(myFile)
        # save on disk
        fs.save(newFileName, myFile)
        # check if jobseeker has already resume uploaded
        if pitcherResume.pitcher_pdf_resume != "":
            # delete old Resume file if exists
            if fs.exists(pitcherResume.pitcher_pdf_resume):
                fs.delete(pitcherResume.pitcher_pdf_resume)
            # update pitcher with new file name
        pitcherResume.pitcher_pdf_resume = newFileName
        pitcherResume.save()
        uploaded_file_url = newFileName
        return JsonResponse({'error': 0, 'path': uploaded_file_url, 'message': 'CSV uploaded successfully.'})
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 1, 'path': '', 'message': 'Something went wrong. Please try again later.'})



@api_view(['GET'])
def csvfile(request):
    try:
        csv_file = PitcherResume.objects.all()
        serializer = PitcherResumeSerializers(csv_file, many=True)
        if csv_file:
            return JsonResponse({'error': 0, "attrs": serializer.data, 'message': "Data Found Successfully"})
        else:
            return JsonResponse({'error': 0, "attrs": '', 'message': "Data NotFound"})
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 1, 'path': '', 'message': 'Something went wrong. Please try again later.'})


@api_view(['GET'])
def read_csv(request,pk):
    requestedOperation = request.GET.get('operation', '')
    requestedColumnName = request.GET.get('column_name', '')
    
    try:
        csv_file = PitcherResume.objects.get(pitcher_id=pk)
        file_name = csv_file.pitcher_pdf_resume
        file_path = settings.PITCHER_PROJECT_STORAGE
        with open(file_path + '/' +file_name) as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            csv_file = csv.reader(file, dialect, quotechar='"')
            csv_file_list = []
            file.seek(0)
            firstline = True
            for row in csv_file:
                print(row,"pppppppppppp")
                if firstline:    #skip first line
                    firstline = False
                    continue
                # csv_file_list.append(int(row[int(requestedColumnName)]))
                csv_file_list.append(int(row[int(requestedColumnName)]))
        if 'max' == request.GET.get('operation', ''):
            return JsonResponse({'error': 0, "attrs": max(csv_file_list), 'message': "Data Found"})
        elif 'min' == request.GET.get('operation', ''):
            return JsonResponse({'error': 0, "attrs": min(csv_file_list), 'message': "Data Found"})
        elif 'sum' == requestedOperation:
            return JsonResponse({'error': 0, "attrs": sum(csv_file_list), 'message': "Data Found"})
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 1, 'attrs': '', 'message': 'Something went wrong. Please try again later.'})

@api_view(['GET'])
def plot_csv(request,pk):
    if request.GET.get('column_name_1', '') == "":
        return JsonResponse({'error': 1, 'attrs': '', 'message': 'Missing column_name_1'})
    if request.GET.get('column_name_2', '') == "":
        return JsonResponse({'error': 1, 'attrs': '', 'message': 'Missing column_name_2'})
    
    requestedColumnName1 = int(request.GET.get('column_name_1', ''))
    requestedColumnName2 = int(request.GET.get('column_name_2', ''))
    
    try:
        csv_file = PitcherResume.objects.get(pitcher_id=pk)
        file_name = csv_file.pitcher_pdf_resume
        file_path = settings.PITCHER_PROJECT_STORAGE
        with open(file_path + '/' +file_name) as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            csv_file = csv.reader(file, dialect, quotechar='"')
            csv_row_list = []
            csv_column_list = []
            file.seek(0)
            firstline = True
            for row in csv_file:
                if firstline:    #skip first line
                    firstline = False
                    continue
                csv_row_list.append(row[requestedColumnName1])
                csv_column_list.append(row[requestedColumnName2])
        return JsonResponse({'error': 0, "attrs": {
            "x": csv_row_list,
            "y": csv_column_list,
            "type": 'scatter' 
        }, 'message': "Data Found"})
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 1, 'path': '', 'message': 'Something went wrong. Please try again later.'})





def index(request):
    return render(request, "frontend/index.html", {"showclass":True})


def data(request):
    return render(request, "frontend/data.html", {"showclass":True})


def plot(request):
    return render(request, "frontend/plot.html", {"showclass":True})


from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TaskSerializer
from .models import Task

import os
# Create your views here.


def homeview(request):
	return redirect('api-overview')


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List': '/task-list',
		'Detail View': '/task-detail/<str:pk>/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
	}


	return Response(api_urls)



#Get all tasks
@api_view(['GET'])
def taskList(request):

	tasks = Task.objects.all().order_by('-id') #Without - means ascending
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)



#Get a single task
@api_view(['GET'])
def taskDetail(request, pk):

	try:
		task = Task.objects.get(id=pk)
	except Task.DoesNotExist:
		return Response({'Error':'No such Id'})

	#If the id exists
	serializer = TaskSerializer(task, many=False)
	return Response(serializer.data)



#Create a task
@api_view(['POST'])
def taskCreate(request):

	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)



#Update a task
@api_view(['POST'])
def taskUpdate(request, pk):

	task = Task.objects.get(id=pk) #First get the object instance
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)



#Delete a task
@api_view(['DELETE'])
def taskDelete(request, pk):

	task = Task.objects.get(id=pk) #First get the object instance
	task.delete()

	return Response({"Success":"Task Deleted Successfully"})
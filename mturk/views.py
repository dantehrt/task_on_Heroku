from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Max

from .forms import AnnotationTaskForm, BoundingTaskForm, WorkerInformationForm
from .models import Input, Output, WorkerInformation


def index(request, worker_id, assignment_id, task_condition):
    context = {
        'worker_id': worker_id,
        'assignment_id': assignment_id,
        'task_condition': task_condition,
    }
    return render(request, 'mturk/index.html', context)


def task(request, worker_id, assignment_id, task_order, task_condition):
    annotation_task_form = AnnotationTaskForm()
    bounding_task_form = BoundingTaskForm()

    input_object = Input.objects.filter(task_order=task_order, task_condition=task_condition).first()
    context = {'input_object': input_object,
               'worker_id': worker_id,
               'assignment_id': assignment_id,
               'task_order': task_order,
               'task_condition': task_condition,
               'annotation_task_form': annotation_task_form,
               'bounding_task_form': bounding_task_form,
               }
    return render(request, 'mturk/task.html', context)


def submit(request, worker_id, assignment_id, task_order, task_condition):
    if request.method == 'POST':
        if request.POST['input_task_type'] == 'b':
            form = BoundingTaskForm(request.POST)
        else:
            form = AnnotationTaskForm(request.POST)
        if form.is_valid():
            form.save()

        if 'submit_button' in request.POST:
            limit = Input.objects.filter(task_condition=task_condition).aggregate(Max('task_order'))['task_order__max']
            if task_order == limit:
                return redirect('mturk:results', worker_id=worker_id, assignment_id=assignment_id, task_condition=task_condition)
            else:
                return redirect('mturk:task', worker_id=worker_id, assignment_id=assignment_id, task_order=task_order + 1, task_condition=task_condition)
        elif 'exit_button' in request.POST:
            return redirect('mturk:results', worker_id=worker_id, assignment_id=assignment_id, task_condition=task_condition)


def results(request, worker_id, assignment_id, task_condition):
    output_objects = Output.objects.filter(worker_id=worker_id, assignment_id=assignment_id)
    output_objects = output_objects.order_by('input_task_order').distinct('input_task_order')
    number_of_completed_tasks = len(output_objects)
    limit = Input.objects.all().aggregate(Max('task_order'))['task_order__max']
    if number_of_completed_tasks == limit:
        is_completed = True
    else:
        is_completed = False

    if request.method == 'POST':
        if 'ok_button' in request.POST:
            worker_information_object = WorkerInformation.objects.filter(worker_id=worker_id, assignment_id=assignment_id).first()
            if worker_information_object:
                worker_information_object.number_of_completed_tasks = number_of_completed_tasks
                worker_information_object.submit_time = request.POST['submit_time']
                worker_information_object.save()
            else:
                form = WorkerInformationForm(request.POST)
                if form.is_valid():
                    form.save()
            return redirect('mturk:thanks', worker_id=worker_id, assignment_id=assignment_id)
        elif 'back_button' in request.POST:
            return redirect('mturk:task', worker_id=worker_id, assignment_id=assignment_id, task_order=number_of_completed_tasks + 1, task_condition=task_condition)

    form = WorkerInformationForm(initial={
        'worker_id': worker_id,
        'assignment_id': assignment_id,
        'number_of_completed_tasks': number_of_completed_tasks,
        'task_condition': task_condition,
    })
    form.fields['worker_id'].label = ''
    form.fields['assignment_id'].label = ''
    form.fields['task_condition'].label = ''
    form.fields['submit_time'].label = ''

    context = {
        'worker_id': worker_id,
        'assignment_id': assignment_id,
        'task_condition': task_condition,
        'output_objects': output_objects,
        'number_of_completed_tasks': number_of_completed_tasks,
        'form': form,
        'is_completed': is_completed,
    }
    return render(request, 'mturk/results.html', context)


def thanks(request, worker_id, assignment_id):
    worker_information = WorkerInformation.objects.filter(worker_id=worker_id, assignment_id=assignment_id).first()
    form = WorkerInformationForm(instance=worker_information)
    form.fields['task_condition'].label = ''
    form.fields['submit_time'].label = ''
    context = {
        'worker_id': worker_id,
        'assignment_id': assignment_id,
        'form': form,
    }
    return render(request, 'mturk/thanks.html', context)


def is_there(request, worker_id):
    worker_information = WorkerInformation.objects.filter(worker_id=worker_id).first()
    if worker_information:
        response = HttpResponse("true", content_type="text/plain")
    else:
        response = HttpResponse("false", content_type="text/plain")

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response
from django.contrib import admin

from .models import Input, Output, WorkerInformation

import csv
from django.http import HttpResponse
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from io import TextIOWrapper, StringIO


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class InputAdmin(admin.ModelAdmin):
    list_display = ('task_order', 'task_type', 'task_condition', 'image_url')

    actions = ["export_as_csv"]
    change_list_template = "admin/output_changelist.html"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Export Selected"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding='utf-8')
            reader = csv.reader(csv_file)
            header = next(reader)
            # print(header)
            for row in reader:
                print(row)
                input, created = Input.objects.get_or_create(id = row[0])
                input.task_order = row[1]
                input.task_type = row[2]
                input.image_url = row[3]
                input.task_condition = row[4]
                input.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

class OutputAdmin(admin.ModelAdmin):
    list_display = ('worker_id', 'assignment_id', 'input_task_order', 'input_task_type', 'input_image_url', 'input_task_condition', 'answer_comments', 'work_time')

    actions = ["export_as_csv"]
    change_list_template = "admin/output_changelist.html"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Export Selected"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = TextIOWrapper(request.FILES["csv_file"].file, encoding='utf-8')
            reader = csv.reader(csv_file)
            header = next(reader)
            # print(header)
            for row in reader:
                output, created = Output.objects.get_or_create(id=row[0] ,accept_time = row[2], submit_time = row[3])
                # output.id = row[0]
                output.assignment_id = row[1]
                # output.accept_time = row[2]
                # output.submit_time = row[3]
                output.input_task_order = row[4]
                output.input_task_type = row[5]
                output.input_image_url = row[6]
                output.answer_annotation_data = row[7]
                output.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

class WorkerInformationAdmin(admin.ModelAdmin):
    list_display = ('worker_id', 'assignment_id', 'number_of_completed_tasks', 'task_condition', 'submit_time')

    actions = ["export_as_csv"]
    change_list_template = "admin/output_changelist.html"

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Export Selected"

admin.site.register(Input, InputAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(WorkerInformation, WorkerInformationAdmin)
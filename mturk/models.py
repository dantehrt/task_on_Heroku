from django.db import models


class Input(models.Model):
    task_order = models.IntegerField(null=True)
    task_type = models.CharField(max_length=1,null=True)
    image_url = models.CharField(max_length=3,null=True)
    task_condition = models.CharField(max_length=1,null=True)
    def __str__(self):
        return self.task_type


class Output(models.Model):
    worker_id = models.CharField(max_length=200)
    assignment_id = models.CharField(max_length=200)
    accept_time = models.DateTimeField()
    submit_time = models.DateTimeField()
    work_time = models.IntegerField()
    input_task_order = models.IntegerField()
    input_task_type = models.CharField(max_length=1)
    input_image_url = models.CharField(max_length=3)
    input_task_condition = models.CharField(max_length=1)
    answer_annotation_data = models.TextField(blank=True)
    answer_text_box1 = models.CharField(max_length=200, blank=True)
    answer_text_box3 = models.CharField(max_length=200, blank=True)
    answer_text_box4 = models.CharField(max_length=200, blank=True)
    answer_text_box2 = models.CharField(max_length=200, blank=True)
    answer_text_box5 = models.CharField(max_length=200, blank=True)
    answer_comments = models.TextField(blank=True)
    approve = models.CharField(max_length=200, blank=True)
    reject = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.assignment_id


class WorkerInformation(models.Model):
    worker_id = models.CharField(max_length=200)
    assignment_id = models.CharField(max_length=200)
    number_of_completed_tasks = models.IntegerField()
    task_condition = models.CharField(max_length=1)
    submit_time = models.DateTimeField()
    # identification_code = models.CharField(max_length=200)
    def __str__(self):
        return self.assignment_id

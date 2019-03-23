from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django import forms
from .models import Output, WorkerInformation


class AnnotationTaskForm(forms.ModelForm):
    field_order = ('answer_text_box1', 'answer_text_box2', 'answer_text_box3', 'answer_text_box4', 'answer_text_box5',
                   'answer_comments')

    def __init__(self, *args, **kwargs):
        super(AnnotationTaskForm, self).__init__(*args, **kwargs)
        self.fields['answer_text_box1'].required = True
        self.fields['answer_text_box2'].required = True
        self.fields['answer_text_box3'].required = True
        self.fields['answer_text_box4'].required = True
        self.fields['answer_text_box5'].required = True
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field_name == 'answer_comments':
                field.label = 'If you have any comments, advice or problem on this HIT, please fill in the following. (Optional)'
            elif 'answer_text_box' in field_name:
                field.label = field_name[-1]
            else:
                field.label = ''

    class Meta:
        model = Output
        # fields = '__all__'
        exclude = ('answer_annotation_data', 'approve', 'reject')


class BoundingTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoundingTaskForm, self).__init__(*args, **kwargs)
        # self.fields['answer_annotation_data'].required = True
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field_name == 'answer_comments':
                field.label = 'If you have any comments, advice or problem on this HIT, please fill in the following. (Optional)'
            else:
                field.label = ''


        # self.helper = FormHelper()
        # self.helper.form_show_labels = False
        # self.fields['answer_comments'].label = 'aaaa'

        # for field in self.fields.values():
        #     field.label = False
        # for field in self.fields.values():
        #     field.widget.attrs['placeholder'] = field.label
        #     field.label = ''

    class Meta:
        model = Output
        # fields = '__all__'
        exclude = (
            'answer_text_box1', 'answer_text_box2', 'answer_text_box3', 'answer_text_box4', 'answer_text_box5',
            'approve',
            'reject'
        )

class WorkerInformationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkerInformationForm, self).__init__(*args, **kwargs)
        self.fields['worker_id'].widget.attrs['readonly'] = True
        self.fields['assignment_id'].widget.attrs['readonly'] = True
        self.fields['number_of_completed_tasks'].widget.attrs['readonly'] = True
        self.fields['task_condition'].widget.attrs['readonly'] = True
        self.fields['submit_time'].widget.attrs['readonly'] = True

    class Meta:
        model = WorkerInformation
        fields = '__all__'

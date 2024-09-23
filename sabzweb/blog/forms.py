from django import forms
from django.core.exceptions import ValidationError
from .models import Comments

class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش مشکل', 'گزارش مشکل'),
    )

    name = forms.CharField(max_length=250, required=True, label='نام و نام خانوادگی ')
    email = forms.EmailField(required=True, label='آدرس ایمیل ')
    phone = forms.CharField(max_length=11, required=True, label='شماره تلفن ')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=True, label='موضوع ')
    message = forms.CharField(widget=forms.Textarea, required=True, label='پیام ')

    # Custom validation check for fields
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isdigit():
                raise ValidationError('شماره تلفن باید فقط شامل عدد باشد!')
            else:
                return phone


# Creates a form based of an existing model ( in this case our Comments model) declaring what fields we need from that
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'body']

        # #Edit the attributes of each field of the form manually
        # widgets = {
        #     'body': forms.TextInput(attrs={
        #         'placeholder': 'متن',
        #         'class': 'cm-body'
        #     }),
        #     'name': forms.TextInput(attrs={
        #         'placeholder': 'نام',
        #         'class': 'cm-name'
        #     })
        # }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('نام باید بیشتر از 3 کاراکتر باشد!')
        else:
            return name


class SearchForm(forms.Form):
    query = forms.CharField()
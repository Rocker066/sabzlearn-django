from django import forms
from django.core.exceptions import ValidationError


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
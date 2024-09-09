from django import forms


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
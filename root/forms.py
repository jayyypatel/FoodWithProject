from django import forms

from root.models import Mailbox

class EmailForm(forms.ModelForm):
    class Meta:
        model = Mailbox
        fields = ['name','email_id','subject','message']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}),
            'email_id': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}),
            'subject': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Subject'}),
            'message': forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Your Message'}),
        }
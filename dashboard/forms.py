from django import forms
from .models import Student, School

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'email', 'address', 'postal', 'country', 'city', 'school']

    
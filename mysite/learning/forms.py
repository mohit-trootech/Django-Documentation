from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Login Username"}
        ),
    )
    file = forms.FileField(widget=forms.FileInput(attrs={"class": "form-control"}))

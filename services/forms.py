from django import forms

from users.models import Company


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(required=True)

    def __init__(self, *args, choices='', ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        # adding choices to fields
        if choices:
            self.fields['field'].choices = choices
        # adding placeholders to form fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'

        self.fields['name'].widget.attrs['autocomplete'] = 'off'


class RequestServiceForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter service address'
        })
    )

    service_time = forms.DecimalField(
        decimal_places=1,
        max_digits=4,
        min_value=0.5,
        required=True,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Service time in hours',
            'step': '0.5'
        }),
        help_text="Please enter the time in hours (minimum 0.5 hours)"
    )

    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        # Adding a custom class to all form fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

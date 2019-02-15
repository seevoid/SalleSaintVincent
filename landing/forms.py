import datetime

from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
import datetime

now = datetime.datetime.now()

class BookForm(forms.Form):
    date_entrée = forms.DateField(
        required=True,
        widget=DatePicker(
            attrs={
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
            },
            options={
                'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            },
        ),
    )

    date_sortie = forms.DateField(
        required=True,
        widget=DatePicker(
            attrs={
               'append': 'fa fa-calendar',
               'input_toggle': True,
               'icon_toggle': True,
            },
            options={
                'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            },
        ),
    )
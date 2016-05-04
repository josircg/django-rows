# -*- coding: utf-8 -*-
from django import forms

import rows
import cStringIO as StringIO
from io import BytesIO


class ConvertForm(forms.Form):

    TYPE_CHOICES = (
        ('html', 'html'),
        ('csv', 'csv'),
        ('xls', 'xls'),
        ('txt', 'txt'),
    )

    convert_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    type_to = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(choices=TYPE_CHOICES, attrs={'class': 'form-control'}))

    def clean_convert_file(self):
        convert_file = self.cleaned_data.get('convert_file')
        if not convert_file.name.split('.')[-1] in [t[0] for t in self.TYPE_CHOICES]:
            raise forms.ValidationError(u'The accepted formats is %s. Send your file in one of these formats.' % u', '.join([t[0] for t in self.TYPE_CHOICES]))
        if convert_file.size/1024 > 1024:
            raise forms.ValidationError(u'The maximum size is 1MB.')
        return convert_file

    def convert(self):
        convert_file = self.cleaned_data.get('convert_file')
        convert_type = convert_file.name.split('.')[-1]
        type_to = self.cleaned_data.get('type_to')

        # Import
        data = getattr(rows, 'import_from_%s' % convert_type)(BytesIO(convert_file.read()))
        # Export
        result = StringIO.StringIO()
        getattr(rows, 'export_to_%s' % type_to)(data, result)

        return result
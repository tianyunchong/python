#/bin/python2.7
#coding=utf-8
from django import forms
import re
class UrladdForm(forms.Form):
    url = forms.CharField()

    def clean_url(self):
        """检测提交的url"""
        url = self.cleaned_data["url"]
        m = re.match(r'^(https?://)?([\da-z.-]+).([a-z.]{2,6})([/\w.-]*)*/?$', url)
        if not m:
            raise forms.ValidationError("not url!")
        return url

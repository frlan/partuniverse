from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Models we need
from .models import Part

#i18n (just in case)
from django.utils.translation import ugettext_lazy as _

class PartAddForm(forms.ModelForm):

	class Meta:
		model = Part
		exclude = ('user')

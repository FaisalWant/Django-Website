from .models import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field,Submit


class PostCreationForm(forms.ModelForm):
	class Meta:
		model= Post
		widgets= {

			"title":forms.TextInput(attrs={'class': 'single-input', 'placeholder':'Enter your title'}),
			"content":forms.Textarea(attrs={'class': 'single-input', 'placeholder':'Enter your content'})

		}

		fields=[
		"title",
		"category",
		"content",
		"image",


		]
# adding crispy forms for the post 
class PostUpdateForm(forms.ModelForm):
	def __init__(self, args,**kwargs):
		super(PostUpdateForm, self).__init__(*args, **kwargs)
		self.helper= FormHelper()
		self.helper.form_method='post'
		self.helper.field_class='mt-10'
		self.helper.layout= Layout(
			Field("title", css_class="single-input", placeholder="Title"), 
			Field("category", css_class="single-input"), 
			Field("content", css_class="single-input", placeholder="Your Content"), 
			Field("image", css_class="single-input"),
			Field("tag", css_class="single-input", placeholder="Your Tags"),  

			)




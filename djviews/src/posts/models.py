from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
# Create your models here.


class Category(models.Model):
	title= models.CharField(max_length=150)
	slug= models.SlugField(editable=False)
	def save(self,*args,**kwargs):
		self.slug= slugify(self.title)
		super(Category, self). save(*args, **kwargs)


	def __str__(self):
		return self.title







class Post(models.Model):
	title= models.CharField(max_length=150)
	content=models.TextField()
	publishing_date=models.DateTimeField(auto_now_add=True)
	image= models.ImageField(blank=True, null=True, upload_to='uploads/')
	user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	slug= models.SlugField(default="slug",editable=False)
	category=models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

	def save(self,*args,**kwargs):
		self.slug= slugify(self.title)
		super(Post, self). save(*args, **kwargs)

	def __str__(self):
		return self.title
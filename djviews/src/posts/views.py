from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import Post, Category, Tag
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import PostCreationForm
from django.template.defaultfilters import slugify
from django.urls import reverse



class IndexView(ListView):
	template_name="posts/index.html"
	model= Post
	context_object_name= "posts"

	def get_context_data(self, *, object_list=None, **kwargs):
		context= super(IndexView, self).get_context_data(**kwargs)
		context['slider_posts']= Post.objects.all().filter(slider_post=True)
		return context





class PostDetail(DetailView):
	template_name="posts/detail.html"
	model= Post
	context_object_name="single"
	def get_context_data(self, **kwargs):
		context= super(PostDetail, self).get_context_data(**kwargs)
		return context




class CategoryDetail(ListView):
	model= Post
	template_name= 'categories/category_detail.html'
	context_object_name='posts'

	def get_queryset(self):
		self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
		return Post.objects.filter(category=self.category).order_by('-id')


	def get_context_data(self,**kwargs):
		context= super(CategoryDetail, self).get_context_data(**kwargs)
		self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
		context['category']= self.category
		return context




class TagDetail(ListView):
	model= Post
	template_name= 'tag/tag_detail.html'
	context_object_name='posts'

	def get_queryset(self):
		self.tag= get_object_or_404(Tag, slug=self.kwargs['slug'])
		return Post.objects.filter(tag=self.tag).order_by('id')

	def get_context_data(self, **kwargs):
		context= super(TagDetail, self).get_context_data(**kwargs)
		self.tag= get_object_or_404(Tag, slug=self.kwargs['slug'])
		context['tag']=self.tag
		return context


@method_decorator(login_required(login_url='users/login'), name='dispatch')
class CreatePostView(CreateView):
	template_name= 'posts/create-post.html'
	form_class= PostCreationForm
	model= Post

	def get_success_url(self):
		return reverse('detail',kwargs={"pk":self.object.pk, "slug":self.object.slug})

	def form_valid(self, form):
		form.instance.user=self.request.user  #user needs to be logged in
		form.save()

		tags=self.request.POST.get("tag").split(",")

		for tag in tags:
			current_tag=Tag.objects.filter(slug=slugify(tag))
			if current_tag.count()<1:
				create_tag= Tag.objects.create(title=tag)
				form.instance.tag.add(create_tag)


			else:
				existed_tag= Tag.objects.get(slug=slugify(tag))
				form.instance.tag.add(existed_tag)

		return super(CreatePostView, self).form_valid(form)


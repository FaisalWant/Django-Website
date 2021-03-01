from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Tag
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import PostCreationForm, PostUpdateForm
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import F



class IndexView(ListView):
	template_name="posts/index.html"
	model= Post
	context_object_name= "posts"
	paginate_by=3

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
		context['previous']= Post.objects.filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
		context['next']= Post.objects.filter(id__gt=self.kwargs['pk']).order_by('pk').first()
		return context

	def get(self, request, *args, **kwargs):#hit count for a blog
		self.hit= Post.objects.filter(id= self.kwargs['pk']).update(hit=F('hit')+1)
		return super(PostDetail,self).get(request,*args, **kwargs)



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



@method_decorator(login_required(login_url='users/login'), name='dispatch')
class UpdatePostView(UpdateView):
	model=Post 
	template_name= 'posts/post-update.html'
	form_class= PostUpdateForm

	def get_success_url(self):
		return reverse('detail',kwargs={"pk":self.object.pk, "slug":self.object.slug})


	def form_valid(self, form):
		form.instance.user= self.request.user
		form.instance.tag.clear()
		tags=self.request.POST.get("tag").split(",")
		for tag in tags:
			current_tag=Tag.objects.filter(slug=slugify(tag))
			if current_tag.count()<1:
				create_tag= Tag.objects.create(title=tag)
				form.instance.tag.add(create_tag)


			else:
				existed_tag= Tag.objects.get(slug=slugify(tag))
				form.instance.tag.add(existed_tag)

		return super(UpdatePostView, self).form_valid(form)

	def get(self, request, *args, **kwargs):
		self.object= self.get_object()

		if self.object.user != request.user:
			return HttpResponseRedirect('/')


		return super(UpdatePostView, self).get(request, *args, **kwargs)



class DeletePostView(DeleteView):
	model= Post 
	success_url ='/'
	template_name='posts/delete.html'

	def delete(self, request, *args, **kwargs):
		self.object= self.get_object()
		if self.object.user == request.user:
			self.object.delete()
			return HttpResponseRedirect(self.success_url)


		else:
			return HttpResponseRedirect(self.success_url)


	def get(self, request, *args, **kwargs):
		self.object= self.get_object()
		if self.object.user != request.user:
			return HttpResponseRedirect('/')

		return super(DeletePostView, self).get(request, *args, **kwargs)
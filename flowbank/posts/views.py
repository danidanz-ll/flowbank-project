from django.shortcuts import redirect, render
from .models import Post
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by('-creation_date')
    return render(request, 'posts/posts_list.html', {'posts': posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html', {'post': post})

@login_required(login_url='/users/login/')
def new_post(request):
    form = forms.CreatePost()
    if request.method == 'POST':
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            # Criar o post mas não salvar no banco ainda
            post = form.save(commit=False)
            # Adicionar o autor antes de salvar
            post.author = request.user
            # Agora salvar no banco
            post.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/new_post.html', {'form': form})
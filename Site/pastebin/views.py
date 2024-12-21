from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy, reverse
from .forms import *
from .models import *

def index(request):
    return redirect('createpost')


def createpost(request):
    if request.method == 'POST':
        data = {'content' : request.POST['content'],
                'password' : request.POST['password']}
        if request.user.is_authenticated:
            data['user'] = request.user
        
        post = Post(**data)
        post.save()
        return redirect(reverse('viewpost', args=[post.id]))
    else:
        return render(request, 'pastebin/createpost.html', {'title' : 'Добавление сниппета'})
    
def viewpost(request, post_id):
    qeuryset = Post.objects.filter(id=post_id)
    print(Post.objects.all())

    if len(qeuryset) == 0:
        return Http404()
    val = qeuryset[0]

    my_user = False
    if request.user.is_authenticated and request.user == val.user:
        my_user = True

    return render(request, 'pastebin/viewpost.html', {'post' : val, 'havepassword' : bool(val.password), 'my_user' : my_user})

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'pastebin/login.html'
    success_url = reverse_lazy('createpost')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
    
    def get_success_url(self):
        return reverse_lazy('createpost')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'pastebin/register.html'
    success_url = reverse_lazy('createpost')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('createpost')
    
def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def post_list(request):
    posts = Post.objects.filter(user=request.user)
    # print(posts)
    for p in posts:
        c = p.content
        if len(c) > 300:
            c = c[:300]
            c += '\n...'
        p.content = c
    return render(request, 'pastebin/postlist.html', {'posts' : posts})

@login_required
def delete_post(request, post_id):
    if request.user == Post.objects.get(id=post_id).user:
        Post.objects.get(id=post_id).delete()
    return redirect('postlist')

@login_required
def changepost(request, post_id):
    q = Post.objects.filter(id=post_id)
    if len(q) == 0 or request.user != q[0].user:
        return Http404()
    post = q[0]

    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.content = request.POST['content']
        post.password = request.POST['password']
        post.save()
        return redirect(reverse('viewpost', args=[post.id]))
    else:
        return render(request, 'pastebin/changepost.html', {'content' : post.content, 'password' : post.password})

def checkpassword(request):
    post_id = int(request.GET['post_id'])
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        return JsonResponse({'correct': True})
    if len(post.password) == 0 or post.password == request.GET['password']:
        return JsonResponse({'correct': True})    
    return JsonResponse({'correct': False})
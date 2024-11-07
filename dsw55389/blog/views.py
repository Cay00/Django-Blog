# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Vote
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import CommentForm, VoteForm


# Main Page
def home(request):
    return render(request, 'blog/base.html')


# Blog Page
def blog_home(request):
    # Pobieramy wszystkie posty
    posts = Post.objects.all()
    # Renderujemy stronę bloga z listą postów
    return render(request, 'blog/blog_home.html', {'posts': posts})


# User Profiles
@login_required
def user_profile(request):
    # Pobieramy tylko posty dodane przez zalogowanego użytkownika
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/user_profile.html', {'posts': posts})


# Post Details
def post_detail(request, post_id):
    # Pobieramy post o podanym ID lub zwracamy 404, jeśli nie istnieje
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Pobieranie komentarzy powiązanych z postem

    # Obsługa formularza dodawania komentarzy
    if request.method == "POST" and 'comment' in request.POST:
        if request.user.is_authenticated:  # Czy użytkownik jest zalogowany
            form = CommentForm(request.POST)
            if form.is_valid():
                # Tworzymy obiekt komentarza, ale nie zapisujemy go jeszcze
                comment = form.save(commit=False)
                comment.post = post  # Przypisujemy komentarz do posta
                comment.author = request.user  # Przypisujemy autora komentarza
                comment.save()  # Zapisujemy komentarz w bazie danych
                # Przekierowujemy użytkownika z powrotem do szczegółów posta
                return redirect('post_detail', post_id=post.id)
        else:
            # Jeśli użytkownik nie jest zalogowany, przekierowujemy do strony logowania
            return redirect('login')
    else:
        form = CommentForm()

    # Obsługa formularza głosowania (łapka w górę lub w dół)
    if request.method == "POST" and 'vote' in request.POST:
        if request.user.is_authenticated:
            # Pobieramy wartość głosowania (łapka w górę: True, łapka w dół: False)
            vote_value = request.POST.get('vote') == 'True'
            # Próbujemy pobrać istniejący głos użytkownika dla tego posta
            vote, created = Vote.objects.get_or_create(post=post, user=request.user, defaults={'value': vote_value})
            if not created:
                # Jeśli głos już istnieje, aktualizujemy wartość głosu
                vote.value = vote_value
                vote.save()
                # Przekierowujemy z powrotem do szczegółów posta po oddaniu głosu
            return redirect('post_detail', post_id=post.id)
        else:
            return redirect('login')

    # Liczba głosów w górę i w dół dla posta
    upvotes = post.votes.filter(value=True).count()
    downvotes = post.votes.filter(value=False).count()

    # Renderujemy stronę szczegółów posta z postem, komentarzami, formularzem komentarza i liczbą głosów
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'upvotes': upvotes,
        'downvotes': downvotes
    })


# Create Post
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(title=title, content=content, author=request.user)
        return redirect('profile')  # Przekierowanie na profil po utworzeniu posta
    return render(request, 'blog/create_post.html')


# Edit Post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Sprawdzamy, czy użytkownik jest autorem posta
    if post.author != request.user:
        raise Http404("Nie masz uprawnień do edytowania tego posta")

    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('profile')  # Przekierowanie na profil po edytowaniu posta

    return render(request, 'blog/edit_post.html', {'post': post})


# Delete Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Sprawdzamy, czy użytkownik jest autorem posta
    if post.author != request.user:
        raise Http404("Nie masz uprawnień do usunięcia tego posta")

    post.delete()
    return redirect('profile')  # Przekierowanie na profil po edytowaniu posta

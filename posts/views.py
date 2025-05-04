from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from .models import Post, Comentario, Like, Favorito
from .forms import ComentarioForm  # lo crearemos en el siguiente paso
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator


@login_required
def crear_post(request):
    if not request.user.is_authenticated:
        return redirect('login_user')  # o al login que uses

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # <- ¡AQUÍ!
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('post')  # cambia a tu vista principal
    else:
        form = PostForm()

    return render(request, 'posts/crear_post.html', {'form': form})



@login_required
def post(request):
    liked_posts = []

    if request.user.groups.filter(name='usuario').exists():
        posts = Post.objects.filter(aprobado=True)
    elif request.user.groups.filter(name='administrador').exists():
        posts = Post.objects.all()
    else:
        posts = Post.objects.none()

    # Paginador
    paginator = Paginator(posts, 3)  # 10 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = Post.objects.filter(favoritos__usuario=request.user).values_list('id', flat=True)

    return render(request, 'posts/index.html', {
        'page_obj': page_obj,
        'liked_posts': liked_posts
    })

def comentar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.filter(post=post).order_by('creado')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = request.user
            comentario.save()
            return redirect('comentar_post', post_id=post.id)
    else:
        form = ComentarioForm()

    return render(request, 'posts/comentarios.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
    })



@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, usuario=request.user)

    if not created:
        like.delete()

    return redirect('post')  # Redirige a la lista de posts



def toggle_favorito(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        favorito, created = Favorito.objects.get_or_create(usuario=request.user, post=post)
        if not created:
            favorito.delete()
        return redirect('post')  # vuelve a la vista index
    return redirect('login')


@user_passes_test(lambda u: u.groups.filter(name='administrador').exists())
@csrf_exempt
def toggle_aprobado(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
            post.aprobado = not post.aprobado
            post.save()
            return JsonResponse({'success': True, 'aprobado': post.aprobado})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post no encontrado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


def favoritos(request):
    user = request.user
    favoritos = Favorito.objects.filter(usuario=user).select_related('post')  # Trae los posts favoritos
    posts = [f.post for f in favoritos]  # Extrae los posts de cada relación

    return render(request, 'posts/favoritos.html', {'data': posts})




# Solo permite acceso a usuarios staff o superusuarios
@user_passes_test(lambda u: u.is_staff)
def moderar_posts(request):
    posts_pendientes = Post.objects.filter(aprobado=False)

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        accion = request.POST.get('accion')
        post = get_object_or_404(Post, id=post_id)

        if accion == 'aprobar':
            post.aprobado = True
            post.save()
        elif accion == 'rechazar':
            post.delete()

        return redirect('moderar_posts')

    return render(request, 'posts/moderar_posts.html', {'posts_pendientes': posts_pendientes})

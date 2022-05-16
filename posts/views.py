from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from posts.models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages
from django.views import View


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 6
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('categoria_post')
        queryset = queryset.order_by('-id').filter(publicado_post=True)
        queryset = queryset.annotate(
            numero_comentarios=Count(
                Case(
                    When(comentario__publicado_comentario=True, then=1)
                )
            )
        )

        return queryset


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return queryset

        queryset = queryset.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return queryset


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        categoria = self.kwargs.get('categoria', None)
        if not categoria:
            return queryset

        queryset = queryset.filter(categoria_post__nome_cat__iexact=categoria)

        return queryset


class PostDetalhes(View):
    template_name = 'posts/post_detalhes.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, publicado_post=True)
        self.contexto = {
            'post': post,
            'comentarios': Comentario.objects.filter(post_comentario=post, publicado_comentario=True),
            'form': FormComentario(request.POST or None),
        }

    def get(self, request, *args, **kwags):
        return render(request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):
        form = self.contexto['form']
        if not form.is_valid():
            return render(request, self.template_name, self.contexto)

        comentario = form.save(commit=False)

        if request.user.is_authenticated:
            comentario.usuario_comentario = request.user

        comentario.post_comentario = self.contexto['post']

        comentario.save()

        messages.success(request, 'Comentário enviado com sucesso!')

        return redirect('post_detalhes', pk=self.kwargs.get('pk'))

# class PostDetalhes(UpdateView):
#     template_name = 'posts/post_detalhes.html'
#     model = Post
#     form_class = FormComentario
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         contexto = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comentarios = Comentario.objects.filter(publicado_comentario=True, post_comentario=post.id)
#         contexto['comentarios'] = comentarios
#         return contexto
#
#     def form_valid(self, form):
#         post = self.get_object()
#         comentario = Comentario(**form.cleaned_data)
#         comentario.post_comentario = post
#         if self.request.user.is_authenticated:
#             comentario.usuario_comentario = self.request.user
#
#         comentario.save()
#         messages.success(self.request, 'Comentário enviado com sucesso!')
#         return redirect('post_detalhes', pk=post.id)

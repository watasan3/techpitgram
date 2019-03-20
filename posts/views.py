from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views import View  # 3-2 追加

from .forms import PostForm
from .models import Post, Like, Comment  # 3-1 [like] 4-1 [Comment]を追加

# 投稿画面


class New(CreateView):
    # 使うためテンプレートの指定
    template_name = 'posts/new.html'
    # 使うformクラスの指定
    form_class = PostForm
    # 成功時に飛ぶURLの指定
    success_url = reverse_lazy('posts:index')

    # 入力に問題がない場合現在ログインしているアカウントを投稿者として登録するための処理
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(New, self).form_valid(form)

# 投稿一覧


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    # 最大表示件数を設定している。今回は100件
    paginate_by = 100
    # データを取得するときに行う処理を記述できる今回は投稿日を降順で並べる様にした
    queryset = Post.objects.order_by('created_at').reverse()

    # 3-1 以下追加
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        like_list = {}
        comment_list = {}
        # すでに取得されている投稿リストを一件づつ取り出す
        for post in context['post_list']:
            # 取り出したものから「いいね!」を探してlike_listに格納する
            like_list[post.id] = Like.objects.filter(post=post)
            comment_list[post.id] = Comment.objects.filter(post=post)  # 3-1 追記
        context['like_list'] = like_list
        context['comment_list'] = comment_list  # 4-1 追記
        return context

# 3-3 以下追加


class Likes(View):
    model = Like
    slug_field = 'post'
    slug_url_kwarg = 'postId'

    def get(self, request, postId):
        post = Post.objects.get(id=postId)
        like = Like.objects.filter(author=self.request.user, post=post)
        like_list = {}
        comment_list = {}  # 4-1 追記
        # 過去にいいねを押しているのか
        if like.exists():
            # いいねされていれば消す
            like.delete()
        else:
            # いいねされていなければ追加する
            like = Like(author=self.request.user, post=post)
            like.save()
        like_list[post.id] = Like.objects.filter(post=post)
        comment_list[post.id] = Comment.objects.filter(post=post)
        return render(request, 'posts/like.html', {
            'like_list': like_list,
            'comment_list': comment_list,  # 4-1 追記
            'post': post
        })

# 以下追加


class AddComment(View):
    def post(self, request, postId):
        like_list = {}
        comment_list = {}

        post = Post.objects.get(id=postId)
        text = request.POST["comment"]

        comment = Comment(author=self.request.user, post=post, text=text)
        comment.save()

        like_list[post.id] = Like.objects.filter(post=post)
        comment_list[post.id] = Comment.objects.filter(post=post)
        return render(request, 'posts/like.html', {
            'like_list': like_list,
            'comment_list': comment_list,
            'post': post
        })

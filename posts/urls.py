from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from . import views

# アプリ名を記述
app_name = 'posts'

# ここの配列の中にルーティングを書いていきます。
urlpatterns = [
    path('new/', login_required(views.New.as_view()), name='new'),  # この行を追加
    path('', login_required(views.Index.as_view()), name='index'),  # この行を追加
    path('<postId>/like/', login_required(views.Likes.as_view()), name='like'), # 3-3 追加
    path('<postId>/comment/', login_required(views.AddComment.as_view()),name='comment'), # 4-2 追加
]
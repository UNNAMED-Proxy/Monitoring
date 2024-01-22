# 사용자정의
from django.contrib.auth.models import User

# 렌더링
from django.shortcuts import render, redirect

from .models import Topic, Reply
# 모델의 클래스명

from django.http import HttpResponse


def home(request):
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics': topics})


# 위 내용과 같다.sdfsdfsdf


# 추가하기
def new_topic(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            message=message,
            writter=user
        )

        post = Reply.objects.create(
            message=message,
            created_by=user

        )

        return redirect('home')

    return render(request, 'new_topic.html', {'topics': topics})
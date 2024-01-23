# 사용자정의
from django.contrib.auth.models import User
from django.utils import timezone

# 렌더링
from django.shortcuts import render, redirect, get_object_or_404

from .models import Topic, Reply
# 모델의 클래스명

from django.http import HttpResponse


def home(request):
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics': topics})


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

        # post = Reply.objects.create(
        #     message=message,
        #     created_by=user
        #
        # )

        return redirect('home')

    return render(request, 'new_topic.html', {'topics': topics})

def answer_create(request, topick_id):
    topic = get_object_or_404(Topic, pk=topick_id)
    topic.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('new_topic.html', topick_id=topic.id)
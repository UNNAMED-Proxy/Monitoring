# 사용자정의
from django.contrib.auth.models import User
from django.utils import timezone
# 렌더링
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Topic, Reply, Answer
# 모델의 클래스명

from django.http import HttpResponse


def home(request):
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics': topics})


# 추가하기
def new_topic(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        user = request.user

        topic = Topic.objects.create(
            subject=subject,
            message=message,
            writter=user,
        )

        post = Reply.objects.create(
            message=message,
            created_by=user
        )

        # return redirect('home')
        return redirect('detail', topic_id=topic.id)

    return render(request, 'new_topic.html', {'topics': topics})

# 상세조회
def detail(request, topic_id):
    """
    topic Detail 조회
    """
    topic = Topic.objects.get(id=topic_id)

    # 김기년 조회수 Count
    counting(topic_id)

    return render(request, 'topic_detail.html', {'topic': topic})

# View Count
def counting(topic_id):
        if not Topic.objects.filter(id = topic_id).exists():
            return JsonResponse({'MESSAGE' : 'DOES_NOT_EXIST_POST'}, status = 404)

        topic = Topic.objects.get(id = topic_id)

        topic.view_count += 1 
        topic.save()


def answer_create(request, topic_id):
    print(123123)
    if request.method == "POST":
        topic = Topic.objects.get(id = topic_id)
        answer = Answer.objects.create(
            topic=topic,
            content=request.POST['content'],
            create_date=timezone.now(),
        )
        
        topic.view_count -= 1
        topic.save()


    return redirect('detail', topic_id=topic.id)
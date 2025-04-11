from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from user.models import User, Post, PostImage
import os
from Jinstagram.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from user.models import Dog 
from django.http import JsonResponse
import time
import json
from ast import literal_eval
from datetime import datetime, timezone
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
def user_login(request):
    if request.method == 'POST':
        print("요청 들어옴")
        print("POST 데이터:", request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({'result': 'fail', 'message': '요청 데이터가 없습니다.'}, status=400)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            request.session['email'] = email
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'fail', 'message': '아이디 또는 비밀번호가 틀렸습니다.'}, status=400)

    return JsonResponse({'result': 'fail', 'message': '잘못된 요청'}, status=400)



class GetMorePosts(APIView):
    def get(self, request):
        page = int(request.GET.get('page', 1))
        start = (page - 1) * 10
        end = start + 10
        
        posts = Post.objects.all().order_by('-created_at')[start:end]
        # 현재 시간 가져오기 (UTC 기준)
        current_time = datetime.now(timezone.utc)

        # 각 Post에 대한 시간 차이 계산 후, 인스턴스에 추가
        for post in posts:
            delta = current_time - post.created_at
            if delta.days < 1:
                # 시간 단위로 저장 (예: "5h")
                hours = delta.seconds // 3600
                post.time_difference = f"{hours}h"
            elif delta.days < 365:
                # 일 단위로 저장 (예: "150days")
                post.time_difference = f"{delta.days}days"
            else:
                # 연 단위로 저장 (예: "2years")
                years = delta.days // 365
                post.time_difference = f"{years}years"

        # 해시태그 필드 파싱
        for post in posts:
            post.hashtag_list = parse_string_list(post.hashtag)

        # posts를 JSON으로 변환
        post_data = serialize_posts_to_json(posts)  # serialize_posts_to_json은 실제로 작성해야 할 함수입니다.
        
        return JsonResponse({'posts': post_data})
    
def serialize_posts_to_json(posts):
    serialized_data = []

    for post in posts:
        # 기본 필드들
        post_data = {
            "user_nickname": post.user.nickname,
            "time_difference": post.time_difference,
            "text": post.text,
            "hashtag_list": post.hashtag_list,
            "images": [image_obj.image.url for image_obj in post.images.all()]
        }

        serialized_data.append(post_data)

    return serialized_data

def user_logout(request):
    logout(request)
    return redirect('main')

def parse_string_list(string_list):
    try:
        return literal_eval(string_list)
    except (ValueError, SyntaxError):
        return []

@csrf_exempt
def submit_user_info(request):
    if request.method == 'POST':
        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        user.company = request.POST['user_company']
        user.location = request.POST['user_location']
        user.save()
        return HttpResponseRedirect('../profile')

@csrf_exempt
def submit_pet_info(request):
    if request.method == 'POST':
        # 데이터 가져오기
        nickname = request.POST['dog_nickname']
        species = request.POST['breed']
        age = request.POST['age']
        sex = request.POST['gender']
        weight = request.POST['weight']
        activity = request.POST['activity']
        bcs = request.POST['bcs']
        weight_control = request.POST['weightChange']
        cycle = request.POST['cycle']
        improve = request.POST.get('desiredImprovement', '')
        disease = request.POST.get('medicalHistory', '')

        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        # 새로운 Dog 객체 생성 및 저장
        dog = Dog(
            nickname=nickname,
            species=species,
            age=age,
            sex=sex,
            weight=weight,
            activity=activity,
            bcs=bcs,
            weight_control=weight_control,
            food_cycle=cycle,
            improve=improve,
            disease=disease,
        )
        dog.user = user
        dog.save()

        print('print Dog id', dog.id)

        return HttpResponseRedirect('../profile')

def input_page(request):
    return render(request, 'content/input.html')

class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")
        
        user_example = User.objects.all().values_list('name', flat=True)

        posts = Post.objects.all().order_by('-created_at')[:10]
        # 현재 시간 가져오기 (UTC 기준)
        current_time = datetime.now(timezone.utc)

        # 각 Post에 대한 시간 차이 계산 후, 인스턴스에 추가
        for post in posts:
            delta = current_time - post.created_at
            if delta.days < 1:
                # 시간 단위로 저장 (예: "5h")
                hours = delta.seconds // 3600
                post.time_difference = f"{hours}h"
            elif delta.days < 365:
                # 일 단위로 저장 (예: "150days")
                post.time_difference = f"{delta.days}days"
            else:
                # 연 단위로 저장 (예: "2years")
                years = delta.days // 365
                post.time_difference = f"{years}years"

        # 해시태그 필드 파싱
        for post in posts:
            post.hashtag_list = parse_string_list(post.hashtag)

        for post in posts:
            # Splitting the text at "Hashtags" and keeping only the part before it
            post.text = post.text.split('Hashtags')[0]

            post.hashtag_list = parse_string_list(post.hashtag)


        return render(request, "jinstagram/main.html", context=dict(user=user, posts=posts, range_5=range(5), user_example=user_example[30:59]))

class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        asdf = uuid_name
        content123 = request.data.get('content')
        email = request.session.get('email', None)

        Feed.objects.create(image=asdf, content=content123, email=email)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")


        user = User.objects.get(email=email)
        dogs = Dog.objects.filter(user=user)
        
        # return render(request, 'your_app/dogs.html', context)
        feed_list = Feed.objects.filter(email=email)
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, 'content/profile.html', context=dict(feed_list=feed_list,
                                                                    like_feed_list=like_feed_list,
                                                                    bookmark_feed_list=bookmark_feed_list,
                                                                    user=user, dogs=dogs))

class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)

class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False
        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)

class ToggleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        print(bookmark_text)
        if bookmark_text == 'bookmark_border':
            is_marked = True
        else:
            is_marked = False
        email = request.session.get('email', None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)


# 미 구현 => Post 데이터 DB가 아직 없어서 나중에
# def post_api(request):
#     # data = list(YourModel.objects.values())
#     data = [0,1,2,3,4]
#     time.sleep(2)
#     return JsonResponse(data, safe=False)  # JSON 응답을 반환

def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('file')
        # 이미지 저장 또는 처리 로직
        # 예를 들면:
        # image_model = ImageModel(image=image)
        # image_model.save()

        return JsonResponse({'message': '이미지가 성공적으로 업로드되었습니다.'})

    return JsonResponse({'error': '잘못된 요청입니다.'})

def upload_post(request):
    if request.method == 'POST':
        email = request.session.get('email', None)
        user = User.objects.filter(email=email).first()
        text = request.POST.get('content')
        hashtag = request.POST.get('hashtag')
        data = json.loads(hashtag)
        hashtags = [f"#{item['value']}" for item in data]

        # Post 객체 생성 및 저장
        post = Post(user=user, text=text, hashtag=hashtags)
        post.save()

        # 이미지를 저장하기 위한 로직
        for file in request.FILES.getlist('files'): 
            # 'files'는 프론트엔드에서 이미지 파일을 보낼 때의 이름이어야 함
            post_image = PostImage(post=post, image=file)
            post_image.save()

        return JsonResponse({'message': 'Post uploaded successfully!'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
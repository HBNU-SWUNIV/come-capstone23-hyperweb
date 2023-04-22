import os
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from Jinstagram.settings import MEDIA_ROOT


class Join1(APIView):
    def get(self, request):
        return render(request, "user/join1.html")

    def post(self, request):
        # TODO 회원가입
        request.session['email'] = request.data.get('email', None)
        request.session['nickname']  = request.data.get('nickname', None)
        request.session['name']  = request.data.get('name', None)
        request.session['password']  = request.data.get('password', None)

        return render(request, 'user/join2.html')
    
class Join2(APIView):
    def get(self, request):
        return render(request, "user/join2.html")
    def post(self, request):
        request.session['species'] = request.data.get('species', None)
        request.session['age']  = request.data.get('age', None)
        request.session['sex']  = request.data.get('sex', None)
        request.session['weight']  = request.data.get('weight', None)
        return render(request, 'user/join3.html')
    
class Join3(APIView):    
    def get(self, request):
        return render(request, "user/join3.html")
    def post(self, request):
        request.session['activity'] = request.data.get('activity', None)
        request.session['weight_control']  = request.data.get('weight_control', None)
        request.session['bcs']  = request.data.get('bcs', None)
        return render(request, "user/join4.html")
    
class Join4(APIView):    
    def get(self, request):
        return render(request, "user/join4.html")
    def post(self, request):
        request.session['cycle'] = request.data.get('cycle', None)
        request.session['improve']  = request.data.get('improve', None)
        request.session['disease']  = request.data.get('disease', None)
        return render(request, "user/login.html")

class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)

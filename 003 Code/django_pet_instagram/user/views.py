import os
from uuid import uuid4
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Dog
from django.contrib.auth.hashers import make_password,check_password
from Jinstagram.settings import MEDIA_ROOT
import hashlib

class Add_dog(APIView):
    def get(self, request):
        return redirect('join2')
    def post(self, request):
        
        return Response(status=200)

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
        if not request.session.get('email'):
            return redirect('login')
        request.session['species'] = request.data.get('species', None)
        request.session['age']  = request.data.get('age', None)
        request.session['sex']  = request.data.get('sex', None)
        request.session['weight']  = request.data.get('weight', None)
        return render(request, 'user/join3.html')
    
class Join3(APIView):    
    def get(self, request):
        return render(request, "user/join3.html")
    def post(self, request):
        if not request.session.get('species'):
            return redirect('login')
        request.session['activity'] = request.data.get('activity', None)
        request.session['weight_control']  = request.data.get('weight_control', None)
        request.session['bcs']  = request.data.get('bcs', None)
        return render(request, "user/join4.html")
    
class Join4(APIView):    
    def get(self, request):
        return render(request, "user/join4.html")
    def post(self, request):
        if not request.session.get('bcs'):
            return redirect('login')
        request.session['cycle'] = request.data.get('cycle', None)
        request.session['improve']  = request.data.get('improve', None)
        request.session['disease']  = request.data.get('disease', None)
        
        
        if not request.session.get('password'): # 추가 정보 입력일 경우
            email = request.session.get('email')
            species = request.session.get('species')
            age = request.session.get('age')
            sex = request.session.get('sex')
            weight = request.session.get('weight')
            activity = request.session.get('activity')
            weight_control = request.session.get('weight_control')
            bcs = request.session.get('bcs')
            cycle = request.session.get('cycle')
            improve = request.session.get('improve')
            disease = request.session.get('disease')

            # Dog 객체 생성
            dog = Dog(species=species, age=age, sex=sex, weight=weight, activity=activity, weight_control=weight_control, bcs=bcs, cycle=cycle, improve=improve, disease=disease)
            dog.save()
            user = User.objects.filter(email=email).first()
            dog.user = user
            return Response(status=200) 
        
        email = request.session.get('email')
        nickname = request.session.get('nickname')
        name = request.session.get('name')
        password = request.session.get('password')
        species = request.session.get('species')
        age = request.session.get('age')
        sex = request.session.get('sex')
        weight = request.session.get('weight')
        activity = request.session.get('activity')
        weight_control = request.session.get('weight_control')
        bcs = request.session.get('bcs')
        cycle = request.session.get('cycle')
        improve = request.session.get('improve')
        disease = request.session.get('disease')

        # Dog 객체 생성
        dog = Dog(species=species, age=age, sex=sex, weight=weight, activity=activity, weight_control=weight_control, bcs=bcs, cycle=cycle, improve=improve, disease=disease)

        # 사용자 생성
        user = User.objects.create_user(email=email, nickname=nickname, name=name, password=password)

        # Dog 객체에 User 객체를 연결합니다.
        dog.user = user

        # Dog 객체를 저장합니다.
        dog.save()
        user.save()
        request.session.flush()
        return render(request, "user/login.html")

class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)        
        user = User.objects.filter(email=email).first()
        print( check_password(user.password, password))
        if user is None:
            return Response(status=400, data=dict(message="회원정보가 잘못되었습니다."))

        if check_password(password, user.password):
            # TODO 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="로그인 정보가 잘못되었습니다."))

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




def generate_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

def verify_hash(data, hash_code):
    calculated_hash = generate_hash(data)
    return calculated_hash == hash_code

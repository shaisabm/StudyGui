from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, UserForm, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Git testing

def loginPage(req):
    page = 'login'
    if req.user.is_authenticated:
        return redirect('home')
    if req.method == 'POST':
        username = req.POST.get('username')
        username.lower()
        password = req.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(req, 'Invalid username or password')
        user = authenticate(req,username=username,password=password)

        if user is not None:
            login(req,user)
            messages.success(req, 'You are now logged in')
            return redirect('home')


    context = {'page':page}
    return render(req,'base/login_register.html',context)

def logoutUser(req):
    logout(req)
    messages.success(req, 'You are now logged out')
    return redirect('home')

def registerPage(req):
    form = UserCreationForm()
    profile_form = UserProfile()
    context = {'form':form,'profile_form':profile_form}

    if req.method == "POST":
        form = UserCreationForm(req.POST)
        profile_form = UserProfile(req.POST,req.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user_id = user.id
            profile.save()

            login(req,user)
            return redirect('home')
        else:
            messages.error(req, "An error occured")
    return render(req, 'base/login_register.html',context)

def home(req):
    for topic in Topic.objects.all():
        if topic.room_set.count() == 0:
            topic.delete()

    if req.GET.get('q') is not None:
        q = req.GET.get('q')
    else: q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) | Q(description__icontains=q))


    room_count = Room.objects.count()
    topics = Topic.objects.all()[0:4]
    topicsCount = Topic.objects.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count,'room_messages':room_messages,'topicsCount':topicsCount}

    return render(req, 'base/home.html', context)

def room(req,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if req.method == "POST":
        message = Message.objects.create(
            user=req.user,
            room=room,
            body=req.POST.get('body'),
        )
        room.participants.add(req.user)
        return redirect('room', pk=room.id)

    context = {'room':room,'room_messages':room_messages, 'participants':participants}
    return render(req, 'base/room.html',context)

def userProfile(req,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(req, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(req):
    form = RoomForm()
    topics = Topic.objects.all()
    if req.method == 'POST':
        topic_name = req.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=req.user,
            topic = topic,
            name = req.POST.get('name'),
            description=req.POST.get('description')
        )

        return redirect('home')


    context = {'form':form,'topics':topics}
    return render(req, "base/room_form.html", context)

@login_required(login_url='login')
def updateRoom(req,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if req.user != room.host:
        return HttpResponse(f"You can not update room {room.id}")

    if req.method == 'POST':
        topic_name = req.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = req.POST.get('name')
        room.topic = topic
        room.description = req.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form,'topics':topics,'room':room}
    return render(req, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(req, pk):
    room = Room.objects.get(id = pk)

    if req.user != room.host:
        return HttpResponse(f"You can not delete room {room.id}")

    if req.method == "POST":
        room.delete()
        return redirect('home')
    return render(req, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(req, pk):
    message = Message.objects.get(id = pk)

    if req.user != message.user:
        return HttpResponse(f"You can not delete this message")

    if req.method == "POST":
        message.delete()
        return redirect('home')
    return render(req, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(req):
    user = req.user
    form = UserForm(instance=user)
    profile_instance = Profile.objects.get(user_id=user.id)
    profile_form = UserProfile(req.POST or None, req.FILES or None, instance=profile_instance)

    if req.method == "POST":
        form = UserForm(req.POST,instance=user)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()


            return redirect('profile',pk=user.id)
    context = {'form':form,'profile':profile_form,'user':user}
    return render(req,'base/update-user.html',context)

@login_required(login_url='login')
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        default_user = User.objects.get(username='user_deleted')
        Room.objects.filter(host = user).update(host=default_user)
        Message.objects.filter(user=user).update(user=default_user)
        user.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':user})



def topicsPage(req):
    if req.GET.get('q') is not None:
        q = req.GET.get('q')
    else: q = ''
    topics = Topic.objects.filter(name__contains=q)
    return render(req,'base/topics.html',{'topics':topics})

def activityPage(req):
    room_messages = Message.objects.all()
    return render(req,'base/activity.html',{'room_messages':room_messages})
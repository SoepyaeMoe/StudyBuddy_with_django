from django.shortcuts import render, redirect, HttpResponse
from . models import *
from .forms import RoomForm, UserFrom, MyUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .decorator import unauthenticated_user

# ____________ auth _____________
@unauthenticated_user
def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email Or Password incorrect!")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerUser(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, 'base/login_register.html', context)

# ________________ end auth __________________


@login_required(login_url='login')
def home(request):
    topics = Topic.objects.all()[0:5]
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    total_rooms = Room.objects.all().count()
    rooms = Room.objects.filter(
        Q(topic__name__icontains = query) |
        Q(host__username__icontains = query) |
        Q(name__icontains = query) |
        Q(description__icontains = query)
    )
    try:
        room_messages = Message.objects.filter(Q(room__topic__name__icontains = query))[0:5]
    except:
        room_messages = []

    context = {
        'rooms': rooms,
        'total_rooms': total_rooms,
        'topics': topics,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id= pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body')
        if body != '':
            message = Message.objects.create(
                user = request.user,
                room = room,
                body = body
            )
            room.participants.add(request.user)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            topic = topic,
            host = request.user,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    context = {'topics': topics, 'room': {'name': '', 'topic': '', 'description': ''}}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def editRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        if request.user == room.host:
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            room.topic = topic
            room.host = request.user
            room.name = request.POST.get('name')
            room.description = request.POST.get('description')
            room.save()
            return redirect('home')
        else:
            return HttpResponse("<h1 styel='color: red'>Stop!<h1> You don't have permision to perform it.")
    context = {'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        if room.host == request.user:
            room.delete()
            return redirect('home')
        else:
            return HttpResponse("<h1>Stop!<h1> <p>You don't have permision to perform it.<p>")
    context = {'obj': room.name}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        if request.user == message.user:
            message.delete()
            return redirect('room', message.room.id)
    context = {'obj': message.body}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()[0:5]
    total_rooms = user.room_set.all().count()
    rooms = user.room_set.filter(
        Q(host = request.user) &
        Q(topic__name__icontains = query) |
        Q(host__username__icontains = query) |
        Q(name__icontains = query) |
        Q(description__icontains = query)
    )
    try:
        room_messages = Message.objects.filter(Q(room__host = user) & Q(room__topic__name__icontains = query))
    except:
        room_messages = []
    context = {
        'user': user,
        'topics': topics,
        'rooms': rooms,
        'room_messages': room_messages,
        'total_rooms': total_rooms
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def editProfile(request, pk):
    user = User.objects.get(id=pk)
    form = UserFrom(instance=user)
    if request.method == 'POST':
        form = UserFrom(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', user.id)
    context = {'user': user, 'form': form}
    return render(request, 'base/edit-profile.html', context)

# ______________ mobile view __________________
@login_required(login_url='login')
def topics(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    total_rooms = Room.objects.all().count()
    context = {'topics': topics, 'total_rooms': total_rooms}
    return render(request, 'base/mobile_topics.html', context)

@login_required(login_url='login')
def activity(request):
    room_messages = Message.objects.all()[0:5]
    context = {'room_messages': room_messages}
    return render(request, 'base/mobile_activity.html', context)
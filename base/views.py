from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# With 'login_required' decorator will restrict access to the pages for not loggen in users.
from django.contrib.auth.decorators import login_required
# Q -> Django method that allows for serching in DB using AND OR etc Bool logic
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Java'},
#     {'id': 2, 'name': 'Python'},
#     {'id': 3, 'name': 'C#'},
# ]

# Note: Can't name this function 'login', because such Django method exist.
def loginPage(request):
    page = 'login'
    # If user alredy logged in, then redirect back 'home'
    if request.user.is_authenticated:
        return redirect('home')

    # Note: when we send login information we want to be able to extract those values.
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Deals with the case when entered user doesn't exist.
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        # Will check if User credentials are correct. 'authenticate' will either give an error(or None??) or will return User obj.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 'login' will add a 'Session' to the database (!!) and to the browser (!!).
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    # 'logout' will delete the session (token?)
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # To ensure that username doesn't include capitalised letters
            user.username = user.username.lower()
            user.save()
            # After registration we want to log in the user automaticaly
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'page': page, 'form': form}

    return render(request, 'base/login_register.html', context)



def home(request):
    # Extracting 'q' value from url
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # 'topic__name__icontains' --> 'name' field in 'topic' data model; 'icontains' --> the field should contain this value; 'i' --> case insensitive.
    # 'Q' -> is a special method that allows to use OR, AND, etc logic operators.
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    # 'count'-> quaryset method; len() could be used but count() is faster
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # (!!) It is a special Dj way to get a Set of all the Messages of this Room (!!). It can be used for ManyToOne relationship
    room_messages = room.message_set.all()
    # '.all()' used on ManyToMany relationship field
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # Adding User to M2M 'participants' field after message is created
        room.participants.add(request.user)
        # It is not necessary to 'redirect' and the page would be anyway refreshed, but I explicitly want this Page to fully reload (!!!)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # Getting all the children of 'room' by using '_set'
    rooms = user.room_set.all()
    # All the messages added in any room
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'rooms': rooms,'user':user, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# Unauthorised User will be redirected to 'login' url
@login_required(login_url='login')
def createRoom(request):
    # It creates an empty Form
    form = RoomForm()
    if request.method == 'POST':
        # Passing 'request.POST' to RoomForm and Django knows wich data to extract from 'request.POST'.
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() # Django will save Room model in DB
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # Form will be prefilled with 'room' values
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not authorized')

    if request.method == 'POST':
        # Need to specify which Room to update, therefor passing in 'instance=room'
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not authorized')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not authorized')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

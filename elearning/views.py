from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Room, Topic, Message, ForalUser
from .forms import RoomForm, Userform, MyusercreationForm
from django.db.models import Q


# Create your views here.


def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect(
            'homepage'
        )
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = ForalUser.objects.get(username=username)
        except:
            messages.error(request, 'usernaem does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'usernaem or password does not exist')

    return render(request, 'elearning/login_registration.html',
                  {'page': page})


def logoutpage(request):

    logout(request)
    return render(request, 'elearning/home.html')


def registerpage(request):
    page = 'register'
    form = MyusercreationForm()
    if request.method == 'POST':
        collected_data = MyusercreationForm(request.POST)
        if collected_data.is_valid():
            user = collected_data.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('homepage')
        else:
            messages.error(request, 'an error occured during registration')
    return render(request,
                  'elearning/login_registration.html',
                  {'page': page, 'form':form})

@login_required(login_url='loginpage')
def userprofile(request, pk):
    userprofile = ForalUser.objects.get(id=pk)
    users_room = userprofile.room_set.all()
    user_activity = userprofile.message_set.all()
    # the dice is in the room context below, rmemebr you access rooms in the center widet with room
    #your context to get user rooms must be name room or whatever yu name the
    # the context in conterwidget
    # this also goes for the acivity which is in the activty html and the sidebar widget
    topics = Topic.objects.all()
    # remeber the vairbales with the get all has being filter in the home function
    #which is the major reason for using exact context name so that it will function in likes manner
    #this is because we need to save time rewriting most coddes
    # this was achive when we included those pages in each pages
    # this help build reusanme codes without much stress

    return render(request, 'elearning/profile.html',
                  {'userprofile': userprofile, 'room': users_room,
                   'activity': user_activity, 'topics': topics})

@login_required(login_url='loginpage')
def edituser(request):
    userinfo = request.user
    form = Userform(instance=userinfo)
    if request.method == 'POST':
        editedform = Userform(request.POST, request.FILES, instance=userinfo)
        if editedform.is_valid():
            editedform.save()
            return redirect('profile', pk=userinfo.id)
    return render(request, 'elearning/edituser.html', {'form':form})

def home(request):
    # homeroom = Room.objects.all()
    # url_query  = request.GET.get('q') this help filter result based on the query
    url_query = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(Q(topic__name__icontains=url_query) |
                               Q(name__icontains=url_query) |
                               Q(description__icontains=url_query))
    # the query below help to filter recent activties by each topics created, remember the
    #url_query has been pass as q from the home.html file as the query set for fetching data from db
    recentactivity= Message.objects.filter(Q(room__topic__name__icontains=url_query))
    topics = Topic.objects.all()[0:5]

    room_count = room.count()
    return render(request, 'elearning/home.html',
                  {'room': room, 'topics': topics,
                   'total_room': room_count, 'activity': recentactivity})

@login_required(login_url=loginpage)
def room(request, pk):
    # roominfo = Room.objects.all()
    room = Room.objects.get(id=pk)
    # kindly know that we are getting information from the class roomm
    #     but because there is a forighn key of message in it
    #     we can access all information in the message class through the ID we
    #     just query
    conversation = room.message_set.all().order_by('-created')

    # this simply make use of the database information of manyto many field relation
    # to check list of particapnts that join the chat in the room
    participants= room.participant.all()

    # here you automatically add users to the group chat wen they drop a
    # comment in the group, this will make dem an automatic particpants

    if request.method == 'POST':
        roommessage = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participant.add(request.user)
        return redirect('room', pk=room.id)

    return render(request, 'elearning/room.html',
                  {'room': room, 'conversation': conversation,
                   'participants': participants})

@login_required(login_url=loginpage)
def create_room(request):
    forms = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topictoget')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        #the get_or_create fucntion check the db if the table topics
        #already had existomg tpics which was one of the dropdown options
        #for users, if the room existed, it passses the arguemtn get to
        #get the topics, and if it is not existing, it create new topics with the name
        #provided by users
        Room.objects.create(
            hostname = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('homepage')
        # forms = RoomForm(request.POST)
        # if forms.is_valid():
        #     roominfo= forms.save(commit=False)
        #     roominfo.hostname = request.user
        #     roominfo.save()
    else:
        forms = RoomForm()

    return render(request, 'elearning/roomform.html',
                  {'roomform': forms, 'topics': topics})

@login_required(login_url=loginpage )
def updateroom(request, pk):
    editroom = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    if request.user != editroom.hostname:
        return HttpResponse('error')
    else:
        forms = RoomForm(instance=editroom)
        if request.method == 'POST':
            topic_name = request.POST.get('topictoget')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            editroom.name = request.POST.get('name')
            editroom.topic = topic
            editroom.description = request.POST.get('description')
            editroom.save()
            return redirect('homepage')
        return render(request, 'elearning/roomform.html',
                          {'roomform': forms, 'topics': topics, 'editroom': editroom})
            # form = RoomForm(request.POST, instance=editroom)
            # if form.is_valid():
            #     form.save()


@login_required(login_url=loginpage )
def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.hostname:
        return HttpResponse('error')
    else:
        if request.method == 'POST':
            room.delete()
            return redirect('homepage')
    return render(request, 'elearning/delete.html',
                  {'obj': room})


@login_required(login_url=loginpage )
def conversationdelete(request, pk):
    conversationdelete = Message.objects.get(id=pk)
    if request.method == 'POST':
        conversationdelete.delete()
        return redirect('homepage')
    return render(request, 'elearning/delete.html',
                  {'obj': conversationdelete})


def topicspage(request):
    url_query = request.GET.get('q') if request.GET.get('q') != None else ''

    topics= Topic.objects.filter(name__icontains=url_query)
    return render(request, 'elearning/topics.html',
                  {'topics':topics})


def mobileactivity(request):
    url_query = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(Q(topic__name__icontains=url_query) |
                               Q(name__icontains=url_query) |
                               Q(description__icontains=url_query))
    recentactivity = Message.objects.filter(Q(room__topic__name__icontains=url_query))
    topics = Topic.objects.all()[0:5]
    room_count = room.count()
    return render(request, 'elearning/mobileactivity.html',
                  {'room': room, 'topics': topics,
                   'total_room': room_count, 'activity': recentactivity})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Question, Topic, Message
from .forms import QuestionForm
from django.contrib.auth import logout as auth_logout


def login_(request):

    page='login'
    if request.user.is_authenticated:
        return redirect('home')


    username=None
    password=None
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
           user=User.objects.get(username=username)
        except:
           messages.error(request, "User doesn't exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context={'page':page}
    return render(request, 'base/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('home')



def register(request):
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')


    form=UserCreationForm()
    context={'form':form}
 

    return render(request, 'base/register.html', context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    questions=Question.objects.filter(
        Q(topic__name__icontains=q)|
        Q(write_question__icontains=q)
        )
    questions_count=questions.count()
    question_messages=Message.objects.filter(Q(question__topic__name__icontains=q))
    topics=Topic.objects.all()
    context={"questions": questions, "topics": topics, "questions_count":questions_count, "question_messages":question_messages}
    return render(request, "base/home.html", context)


@login_required
def question(request, pk):
    question=Question.objects.get(id=pk)
 
    #question_messages=Message.objects.all()
    question_messages=question.message_set.filter(parent=None).order_by('-created')
    participants=question.participants.all() 

    reply_form_id=request.GET.get('reply_form_id')




    if request.method=="POST":
        parent_id=request.POST.get('parent_id')
        parent_comment=Message.objects.filter(id=parent_id).first() if parent_id else None


        message=Message.objects.create(
            user=request.user,
            question=question,
            comment=request.POST.get('comment'),
            parent=parent_comment
        )
            
        question.participants.add(request.user)
        return redirect('question', pk=question.id)

    
    context={"question":question, "question_messages": question_messages, 'participants': participants, 'reply_form_id':reply_form_id}
    return render(request, "base/question.html", context)



def userProfile(request, pk):
    user=User.objects.get(id=pk)
    questions=user.question_set.all()
    question_messages=user.message_set.all()
    topics=Topic.objects.all()

    context={'user':user, 'questions':questions, 'question_messages':question_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_question(request):
    form=QuestionForm()
    if request.method=="POST":
        form=QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request, "base/question_form.html", context)

@login_required(login_url='login')
def update_question(request, pk):
    question=Question.objects.get(id=pk)
    form=QuestionForm(instance=question)


    if request.user!=question.host:
        return HttpResponse("Your are not allowes here!")

    if request.method=="POST":
        form=QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request, "base/question_form.html", context)

@login_required(login_url='login')
def delete_question(request, pk):
    question=Question.objects.get(id=pk)

    if request.user!=question.host:
        return HttpResponse("Your are not allowes here!")
    
    if request.method=="POST":
        question.delete()
        return redirect("home")
    context={'obj': question}
    return render(request, "base/delete.html", context)

@login_required(login_url='login')
def delete_message(request, pk):
    message=Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse("Your are not allowes here!")
    
    if request.method=="POST":
        message.delete()
        return redirect("home")
    context={'obj': message}
    return render(request, "base/delete.html", context)


@login_required(login_url='login')
def delete_reply(request, pk):
    reply=get_object_or_404(Message,id=pk)
    question_id=reply.question.id

    if request.user!=reply.user:
        return HttpResponse("Your are not allowes here!")
    
    if request.method=="POST":
        reply.delete()
        return redirect("question", pk=question_id)
    context={'obj': reply}
    return render(request, "base/delete_reply.html", context)




    



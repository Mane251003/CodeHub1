from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from .models import Question, Topic, Message
from .forms import QuestionForm


def loginPage(request):
    username=None
    password=None
    if request.method=="POST":
        username=request.POST.get('username')
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

    context={}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    questions=Question.objects.filter(
        Q(topic__name__icontains=q)|
        Q(write_question__icontains=q)
        )
    questions_count=questions.count()
    topics=Topic.objects.all()
    context={"questions": questions, "topics": topics, "questions_count":questions_count}
    return render(request, "base/home.html", context)

def question(request, pk):
    question=Question.objects.get(id=pk)
    message=Message.objects.get(id=pk)
    context={"question":question, "message": message}
    return render(request, "base/question.html", context)

def create_question(request):
    form=QuestionForm()
    if request.method=="POST":
        form=QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request, "base/question_form.html", context)


def update_question(request, pk):
    question=Question.objects.get(id=pk)
    form=QuestionForm(instance=question)

    if request.method=="POST":
        form=QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request, "base/question_form.html", context)

    
def delete_question(request, pk):
    question=Question.objects.get(id=pk)
    if request.method=="POST":
        question.delete()
        return redirect("home")
    context={'obj': question}
    return render(request, "base/delete.html", context)






    



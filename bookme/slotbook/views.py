from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import users

def index(request):
    if request.method=="GET":
        if request.session.has_key('username'):
            username=request.session['username']
            return render(request, "slotbook/home.html", {
                    "data":users.objects.all(),
                    "username":username,
                    "email":"hello@iitd",
                })  
        return render(request, "slotbook/index.html")
def register(request):
    if request.method=="GET":
        if request.session.has_key('username'):
            username=request.session['username']
            return render(request, "slotbook/home.html", {
                    "data":users.objects.all(),
                    "username":username,
                    "email":"hello@iitd",
                })  
        return render(request, "slotbook/index.html")
    if request.method=="POST":
        form = request.POST
        mind=users()
        mind.email=form["email"]
        mind.username=form["name"]
        mind.password=form["password"]
        mind.save()
        return render(request, "slotbook/home.html", {
            "data":users.objects.all,
            "username":mind.username,
            "email":mind.email
        })
def login(request):
    if request.method=="GET":
        return render(request, "slotbook/login.html")
    if request.method=="POST":
        form=request.POST
        username=form["name"]
        password=form["password"]
        data=users.objects.all()
        for x in data:
            if x.username==username and x.password==password:
                request.session['username']=username
                return render(request, "slotbook/home.html", {
                        "data":users.objects.all,
                        "username":x.username,
                        "email":x.email
                    })
        return render(request, "slotbook/login.html",{
            "message":"Invalid Username/Password",
        })
def log_out(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, "slotbook/login.html",{
        "message":"Logged Out Succesfully",
    })

    


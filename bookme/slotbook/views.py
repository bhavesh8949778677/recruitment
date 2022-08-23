from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

from .models import *


def index(request):
    print("BYe")
    if request.method=="GET":
        # if request.session.has_key('admin'):
        #     admin=request.session['admin']
        #     return render(request, "admin_index.html",{
        #         "admin":admin,
        #     })
        if request.session.has_key('username'):
            user=request.session['username']
            rows=users.objects.filter(username=username)
            x=rows[0]
            print(x)
            return render(request, "slotbook/index.html", {
                    "data":users.objects.all(),
                    "user":x,
                    "sports": ["basketball", "football", "squash", "badminton", "cricket"],
                    "slots": ["1 to 3", "3 to 5", "5 to 7", "7 to 9"]
                })
    return HttpResponseRedirect(reverse("slotbook:login"))
def register(request):
    if request.method=="GET":
        if request.session.has_key('username'):
            username=request.session['username']
            return render(request, "slotbook/index.html", {
                    "data":users.objects.all(),
                    "username":username,
                    "email":"hello@iitd",
                })  
        return render(request, "slotbook/register.html")
    if request.method=="POST":
        form = request.POST
        mind=users()
        mind.email=form["email"]
        mind.username=form["name"]
        mind.password=form["password"]
        rows=users.objects.filter(username=mind.username)
        if len(rows)>0:
            return render(request, "slotbook/register.html",{
                "message": "User alredy exists"
            }) 
        rows=users.objects.all()
        mind.save()
        request.session["username"]=mind.username
        return HttpResponseRedirect("slotbook:index")
def login(request):
    if request.method=="GET":
        if request.session.has_key("username"):
            return HttpResponseRedirect(reverse("slotbook:index"))
        return render(request, "slotbook/login.html")
    if request.method=="POST":
        form=request.POST
        username=form["name"]
        password=form["password"]
        rows=mega.objects.filter(username=username, password=password)
        if len(rows)==1:
            print("HI")
            print("HI")
            request.session['admin']=rows[0]
            print("Hello")
            return HttpResponseRedirect(reverse("slotbook:index"))
        staff_data=staff.objects.all()
        data=users.objects.all()
        for x in data:
            if x.username==username and x.password==password:
                request.session['username']=x
                return HttpResponseRedirect(reverse("slotbook:index"))
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

def cp(request):
    if request.session.has_key('username'):
        if request.method=="GET":
            return render(request, "slotbook/cp.html")
        if request.method=="POST":
            form=request.POST
            oldpassword=form["oldpassword"]
            newpassword=form["newpassword"]
            confirmation=form["confirmation"]
            return HttpResponseRedirect(reverse("slotbook:index"))
    return HttpResponseRedirect(reverse("slotbook:login"))
    

    


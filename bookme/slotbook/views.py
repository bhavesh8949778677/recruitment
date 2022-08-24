from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from . import util, markdown2

# Create your views here.

from .models import *


def index(request):
    if request.method=="GET":
        if request.session.has_key('admin'):
            admin=request.session['admin']
            return render(request, "slotbook/admin_index.html",{
                "admin":admin,
                "user_data": users.objects.all(),
                "staff_data": staff.objects.all(),
            })
        if request.session.has_key('staff'):
            staffing=request.session['staff']
            return render(request, "slotbook/staff_index.html",{
                "user_data": users.objects.all(),
            })
        if request.session.has_key('username'):
            user=request.session['username']
            return render(request, "slotbook/index.html", {
                    "data":users.objects.all(),
                    "username": user["username"],
                    "email":user['email'],
                    "sports": ["basketball", "football", "squash", "badminton", "cricket"],
                    "slots": ["1 to 3", "3 to 5", "5 to 7", "7 to 9"],
                    "entries": util.list_entries()
                })
    if request.method=="POST":
        if request.session.has_key('username'):
            user=request.session['username']
            form=request.POST
            sport=form['sport']
            slot=form['slot']
            return render(request, "slotbook/index.html",{
                "message": "You slot is succesfully booked",
                "data":users.objects.all(),
                "username": user["username"],
                "email":user['email'],
                "sports": ["basketball", "football", "squash", "badminton", "cricket"],
                "slots": ["1 to 3", "3 to 5", "5 to 7", "7 to 9"],
                "entries": util.list_entries()
            })
    return HttpResponseRedirect(reverse("slotbook:login"))


def register(request):
    if request.method=="GET":
        if request.session.has_key('username'):
            user=request.session['username']
            return render(request, "slotbook/index.html", {
                    "data":users.objects.all(),
                    "username":user['username'],
                    "email":user['email'],
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
        request.session["username"]=mind
        return HttpResponseRedirect(reverse("slotbook:index"))
def login(request):
    if request.method=="GET":
        if request.session.has_key("username") or request.session.has_key("admin") or request.session.has_key("staff"):
            return HttpResponseRedirect(reverse("slotbook:index"))
        return render(request, "slotbook/login.html")
    if request.method=="POST":
        form=request.POST
        username=form["name"]
        password=form["password"]
        rows=mega.objects.filter(username=username, password=password)
        print()
        print()
        # print(rows[0])
        print()
        print()
        if len(rows)==1:
            request.session['admin'] = model_to_dict(rows[0]) ####################################################
            return HttpResponseRedirect(reverse("slotbook:index"))
        rows=staff.objects.filter(username=username, password=password)
        if len(rows)==1:
            request.session['staff'] = model_to_dict(rows[0])
            return HttpResponseRedirect(reverse("slotbook:index"))
        data=users.objects.all()
        for x in data:
            if x.username==username and x.password==password:
                request.session['username']=model_to_dict(x)
                return HttpResponseRedirect(reverse("slotbook:index"))
        return render(request, "slotbook/login.html",{
            "message":"Invalid Username/Password",
        })
def log_out(request):
    try:
        del request.session['admin']
    except:
        pass
    try:
        del request.session['staff']
    except:
        pass
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
    

    

def sports_pages(request, sport):
    if request.session.has_key('username'):
        if request.method=="GET":
            content=util.get_entry(sport)
            if content is not None:
                text = markdown2.markdown(util.get_entry(sport))
                return render(request, "slotbook/content.html",{
                    "title": sport,
                    "text": text,
                })
    return HttpResponseRedirect(reverse("slotbook:login"))

def profile(request):
    if request.method=="GET":
        if request.session.has_key("username"):
            user=request.session['username']
            return render(request, "slotbook/profile.html",{
                "user":user,
            })
    return HttpResponseRedirect(reverse("slotbook:login"))
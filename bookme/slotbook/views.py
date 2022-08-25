from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from django import forms
from django.forms.models import model_to_dict
from . import util, markdown2
from .models import *
from datetime import datetime

# Create your views here.
class newpageform(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-12'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-md-8 col-lg-12','rows': 10}))

rows=ava_data.objects.all()
ava_sport_obs=set()
ava_slot_obs=set()
ava_arena_obs=set()
print("Available Things")
for row in rows:
    row=model_to_dict(row)
    ava_sports=sports.objects.filter(id=row['sport_id'])
    ava_sport_obs.add(model_to_dict(ava_sports[0])['sport'])
    ava_slot=slots.objects.filter(id=row['slot_id'])
    ava_slot_obs.add(model_to_dict(ava_slot[0])['day']+' start '+str(model_to_dict(ava_slot[0])['start_time'])+' end ' +str(model_to_dict(ava_slot[0])['end_time']))
    ava_arena=arena.objects.filter(id=row['arena_id'])
    ava_arena_obs.add(model_to_dict(ava_arena[0])['arena'])
    # print(model_to_dict(ava_sports[0])['sport'], ava_slot[0], model_to_dict(ava_arena[0])['arena'])

#Failed attempt : I learnt I can't pass list_of_dict/set_of_tuples into an html file and extract data
"""
ava_sport_dict=[]
ava_slot_dict=[]
ava_arena_dict=[]
for x in ava_sport_obs:
    dick={'id':x[0],'sport':x[1]}
    ava_sport_dict.append(dick)
for x in ava_slot_obs:
    dick={'id':x[0],'day':x[1],'start':x[2],'end':x[3]}
    ava_slot_dict.append(dick)
for x in ava_arena_obs:
    dick={'id':x[0],'arena':x[1]}
    ava_arena_dict.append(dick)
"""



sports_hi = ["basketball", "football", "squash", "badminton", "cricket"]
available_slots =  ["1 to 3", "3 to 5", "5 to 7", "7 to 9"]
available_arena =  ["arena 1", "arena 2","arena 3"]

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
            data1=data.objects.all()
            l=[]
            for x in data1:
                x=model_to_dict(x)
                usera=users.objects.get(id=x['user_id'])
                usera=model_to_dict(usera)
                usera=usera['username']
                sport1=sports.objects.get(id=x['sport_id'])
                sport1=model_to_dict(sport1)
                sport1=sport1['sport']
                arena1=arena.objects.get(id=x['arena_id'])
                arena1=model_to_dict(arena1)
                arena1=arena1['arena']
                slot1=slots.objects.get(id=x['slot_id'])
                slot1=model_to_dict(slot1)
                slot1=slot1['day'] + ' start '+str(slot1['start_time'])+' end '+str(slot1['end_time'])
                dick={'usera':usera,'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l.append(dick)
            return render(request, "slotbook/staff_index.html",{
                "user_data": users.objects.all(),
                "l":l,
                "sports":sports.objects.all(),
            })




        if request.session.has_key('username'):
            user=request.session['username']
            return render(request, "slotbook/index.html", {
                    "data":users.objects.all(),
                    "username": user["username"],
                    "email":user['email'],
                    "sports": sports_hi,
                    "ava_sports": ava_sport_obs,
                    "slots": ava_slot_obs,
                    "courts": ava_arena_obs,
                    "entries": util.list_entries(),
                })

    if request.method=="POST":
        if request.session.has_key('username'):
            user=request.session['username']
            form=request.POST
            sport=form['sport']
            arena1=form['arena']
            slot1=form['slot']
            rows=sports.objects.filter(sport=sport)
            sport_id=model_to_dict(rows[0])['id']
            rows=arena.objects.filter(arena=arena1)
            arena_id=model_to_dict(rows[0])['id']
            slot1=slot1.split()
            rows=slots.objects.filter(day=slot1[0], start_time=datetime.strptime(slot1[2],'%H:%M:%S').time(), end_time=datetime.strptime(slot1[4],'%H:%M:%S').time())
            slot_id=model_to_dict(rows[0])['id']
            rows=ava_data.objects.filter(sport_id=sport_id,arena_id=arena_id, slot_id= slot_id)
            if len(rows)==1:
                rows=ava_data.objects.get(sport_id=sport_id,arena_id=arena_id, slot_id= slot_id)
                rows.delete()
                booking=data()
                booking.user_id=request.session['username']['id']
                booking.sport_id=sport_id
                booking.arena_id=arena_id
                booking.slot_id=slot_id
                booking.save()
                return render(request, "slotbook/index.html",{
                "message": "You slot is succesfully booked",
                    "data":users.objects.all(),
                    "username": user["username"],
                    "email":user['email'],
                    "sports": sports_hi,
                    "ava_sports": ava_sport_obs,
                    "slots": ava_slot_obs,
                    "courts": ava_arena_obs,
                    "entries": util.list_entries(),
                })
            else:
                return render(request, "slotbook/index.html",{
                "message": "This slot is not available",
                    "data":users.objects.all(),
                    "username": user["username"],
                    "email":user['email'],
                    "sports": sports_hi,
                    "ava_sports": ava_sport_obs,
                    "slots": ava_slot_obs,
                    "courts": ava_arena_obs,
                    "entries": util.list_entries(),
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
    if request.session.has_key('staff'):
        if request.method=="GET":
            content=util.get_entry(sport)
            if content is not None:
                text = markdown2.markdown(util.get_entry(sport))
                return render(request, "slotbook/content.html",{
                    "title": sport,
                    "text": text,
                    "edit_access": True,
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



def newpage(request):
    if request.session.has_key('staff'):
        if request.method=="GET":
            return render(request, "slotbook/newpage.html",{
                "form":newpageform(),
            })
    return HttpResponseRedirect(reverse("slotbook:index"))
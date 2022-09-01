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


def index(request):
    print()
    print()
    print(datetime.now())
    print()
    print()
    # data1=data.objects.all()
    # for x in data1:
    #     q=x['slot_id']
    #     row=slots.objects.get(id=q)
    #     if slots.end_time
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
            ava = ava_data.objects.all()
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
                slot1=' from '+str(slot1['start_time'])+' to '+str(slot1['end_time'])
                dick={'id':x['id'],'usera':usera,'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l.append(dick)
            l1=[]
            for x in ava:
                x=model_to_dict(x)
                sport1=sports.objects.get(id=x['sport_id'])
                sport1=model_to_dict(sport1)
                sport1=sport1['sport']
                arena1=arena.objects.get(id=x['arena_id'])
                arena1=model_to_dict(arena1)
                arena1=arena1['arena']
                slot1=slots.objects.get(id=x['slot_id'])
                slot1=model_to_dict(slot1)
                slot1='From '+ str(slot1['start_time']) +' To ' + str(slot1['end_time'])
                dick={'id':x['id'],'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l1.append(dick)
            return render(request, "slotbook/staff_index.html",{
                "user_data": users.objects.all(),
                "l":l,
                "l1":l1,
                "sports":sports.objects.all(),
            })


        if request.session.has_key('username'):
            user=request.session['username']
            sports_hi = sports.objects.all()
            slots_hi = slots.objects.all()
            arenas_hi = arena.objects.all()
            return render(request, "slotbook/index.html", {
                    "username": user["username"],
                    "email":user['email'],
                    "sports": sports_hi,
                    "slots": slots_hi,
                    "courts": arenas_hi,
                })

    if request.method=="POST":
        if request.session.has_key('username'):
            sports_hi = sports.objects.all()
            slots_hi = slots.objects.all()
            arenas_hi = arena.objects.all()
            user=request.session['username']
            sports_hi = sports.objects.all()
            form=request.POST
            sport1_id=form['sport']
            arena1_id=form['arena']
            slot1_id=form['slot']
            rows=ava_data.objects.filter(sport_id=sport1_id,arena_id=arena1_id, slot_id= slot1_id)
            if len(rows)==1:
                rows=ava_data.objects.get(sport_id=sport1_id,arena_id=arena1_id, slot_id= slot1_id)
                rows.delete()
                booking=data()
                booking.user_id=request.session['username']['id']
                booking.sport_id=sport1_id
                booking.arena_id=arena1_id
                booking.slot_id=slot1_id
                booking.save()
                return render(request, "slotbook/index.html", {
                    "message": "You slot is succesfully booked",
                    "username": user["username"],
                    "email":user['email'],
                    "sports": sports_hi,
                    "slots": slots_hi,
                    "courts": arenas_hi,
                    "entries": util.list_entries(),
                })
            else:
                return render(request, "slotbook/index.html",{
                "message": "This slot is not available",
                    "username": user["username"],
                    "email":user['email'],
                    "sports": sports_hi,
                    "slots": slots_hi,
                    "courts": arenas_hi,
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
            data1=data.objects.filter(user_id=user['id'])
            bookings=[]
            for x in data1:
                x=model_to_dict(x)
                sport1=sports.objects.get(id=x['sport_id'])
                sport1=model_to_dict(sport1)
                sport1=sport1['sport']
                arena1=arena.objects.get(id=x['arena_id'])
                arena1=model_to_dict(arena1)
                arena1=arena1['arena']
                slot1=slots.objects.get(id=x['slot_id'])
                slot1=model_to_dict(slot1)
                slot1='From '+str(slot1['start_time'])+'To '+str(slot1['end_time'])
                dick={'sport1':sport1,'arena1':arena1,'slot1': slot1}
                bookings.append(dick)
            return render(request, "slotbook/profile.html",{
                "user":user,
                "bookings":bookings,
            })
    return HttpResponseRedirect(reverse("slotbook:login"))



def newpage(request):
    if request.session.has_key('staff'):
        if request.method=="GET":
            return render(request, "slotbook/newpage.html",{
                "form":newpageform(),
            })
        if request.method=="POST":
            form=newpageform(request.POST)
            if form.is_valid():
                title=form.cleaned_data["title"]
                z=sports()
                z.sport=title
                z.save()
                content=form.cleaned_data["content"]
                if title not in util.list_entries():
                    util.save_entry(title,content)
                    text = markdown2.markdown(util.get_entry(title))
                    return render(request,"slotbook/content.html",{
                    "title":title,
                    "text":text,
                }) 
                return render(request,"slotbook/newpage.html",{
                    "form": form,
                    "message": "Error this title alredy exists"
                })
            return render(request,"slotbook/newpage.html",{
                "entry": random.choice(util.list_entries()),
                "form": newpageform()
            }) 
    return HttpResponseRedirect(reverse("slotbook:index"))



def edit(request,sport):
    if request.session.has_key('staff'):
        if request.method=="GET":
            title=sport
            content=util.get_entry(title)
            form=newpageform()
            form.fields["title"].initial = title
            form.fields["title"].widget = forms.HiddenInput()
            form.fields["content"].initial = content
            return render(request, "slotbook/edit.html",{
                "title":title,
                "form":form,
            })
        if request.method=="POST":
            form=newpageform(request.POST)
            if form.is_valid():
                title=form.cleaned_data["title"]
                content=form.cleaned_data["content"]
                if title in util.list_entries():
                    util.save_entry(title,content)
                    text = markdown2.markdown(util.get_entry(title))
                    return render(request,"slotbook/content.html",{
                    "title":title,
                    "text":text,
                    "edit_access":True,
                }) 
                return render(request,"slotbook/newpage.html",{
                    "form": form,
                    "message": "Error this title alredy exists"
                })    
    return HttpResponseRedirect(reverse("slotbook:login"))




def newslot(request):
    if request.session.has_key('staff'):
        if request.method=="GET":
            return render(request, "slotbook/newslot.html")

        if request.method=="POST":
            form = request.POST
            i_sport = form['input_sport']
            i_arena = form['input_arena']
            i_start=form['input_start']
            i_end=form['input_end']
            rows=sports.objects.filter(sport=i_sport)
            flag=0
            if len(rows)==0:
                flag=1
                a=sports()
                a.sport=i_sport
                a.save()
            rows=arena.objects.filter(arena=i_arena)
            if len(rows)==0:
                flag=1
                a=arena()
                a.arena=i_arena
                a.save()
            rows= slots.objects.filter(start_time=i_start, end_time=i_end)
            if len(rows)==0:
                flag=1
                a=slot()
                a.start_time=i_start
                a.end_time=i_end
                a.save()
            sport_id=model_to_dict(sports.objects.get(sport=i_sport))['id']
            arena_id=model_to_dict(arena.objects.get(arena=i_arena))['id']
            slot_id=model_to_dict(slots.objects.get( start_time=i_start, end_time=i_end))['id']
            rows=ava_data.objects.filter(sport_id=sport_id, arena_id=arena_id, slot_id=slot_id)
            if len(rows)==0:
                flag=1
                a=ava_data()
                a.sport_id=sport_id
                a.arena_id=arena_id
                a.slot_id=slot_id
                a.save()
            if flag==0:
                return render(request, "slotbook/newslot.html",{
                    "message": "This slot is already available."
                })
            else:
                return HttpResponseRedirect(reverse("slotbook:index"))
    return HttpResponseRedirect(reverse("slotbook:login"))


def newstaff(request):
    if request.session.has_key('admin'):
        if request.method=="GET":
            return render(request, 'slotbook/newstaff.html')
        if request.method=="POST":
            form = request.POST
            name=form['name']
            role=form['role']
            password=form['password']
            confirmation=form['confirmation']
            email=form['email']
            if password!=confirmation:
                return render(request, 'slotbook/newstaff.html',{
                    'message': "Passwords must match",
                })
            new=staff()
            new.username=name
            new.password=password
            new.role=role
            new.email=email
            new.save()
            admin=request.session['admin']
            return render(request, "slotbook/admin_index.html",{
                "admin":admin,
                "user_data": users.objects.all(),
                "staff_data": staff.objects.all(),
                "message": "New staff created successfully",
            })
            return 

    return HttpResponse("Make New Staff Here")



def cancel(request):
    if request.session.has_key("staff"):
        if request.method=="POST":
            form = request.POST
            id= form['y']
            row=data.objects.get(id=id)
            row.delete()
            staffing=request.session['staff']
            data1=data.objects.all()
            ava = ava_data.objects.all()
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
                slot1='From '+str(slot1['start_time'])+' To '+str(slot1['end_time'])
                dick={'id':x['id'],'usera':usera,'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l.append(dick)
            l1=[]
            for x in ava:
                x=model_to_dict(x)
                sport1=sports.objects.get(id=x['sport_id'])
                sport1=model_to_dict(sport1)
                sport1=sport1['sport']
                arena1=arena.objects.get(id=x['arena_id'])
                arena1=model_to_dict(arena1)
                arena1=arena1['arena']
                slot1=slots.objects.get(id=x['slot_id'])
                slot1=model_to_dict(slot1)
                slot1='From '+ str(slot1['start_time']) +' To ' + str(slot1['end_time'])
                dick={'id':x['id'],'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l1.append(dick)
            return render(request, "slotbook/staff_index.html",{
                "message": "booking cancelled succesfully",
                "user_data": users.objects.all(),
                "l":l,
                "l1":l1,
                "sports":sports.objects.all(),
            })


def deletestaff(request):
    if request.session.has_key('admin'):
        if request.method=="POST":
            id=request.POST['staffid']
            staff1=staff.objects.get(id=id)
            staff1.delete()
            admin=request.session['admin']
            return render(request, "slotbook/admin_index.html",{
                "admin":admin,
                "user_data": users.objects.all(),
                "staff_data": staff.objects.all(),
                "message": "Staff deleted succesfully",
            })
    return HttpResponseRedirect(reverse("slotbook:login"))


def unava(request):
    if request.session.has_key('staff'):
        if request.method=="POST":
            id =request.POST['y']
            x = ava_data.objects.get(id=id)
            x.delete()
            staffing=request.session['staff']
            data1=data.objects.all()
            ava = ava_data.objects.all()
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
                slot1='From '+str(slot1['start_time'])+' To '+str(slot1['end_time'])
                dick={'id':x['id'],'usera':usera,'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l.append(dick)
            l1=[]
            for x in ava:
                x=model_to_dict(x)
                sport1=sports.objects.get(id=x['sport_id'])
                sport1=model_to_dict(sport1)
                sport1=sport1['sport']
                arena1=arena.objects.get(id=x['arena_id'])
                arena1=model_to_dict(arena1)
                arena1=arena1['arena']
                slot1=slots.objects.get(id=x['slot_id'])
                slot1=model_to_dict(slot1)
                slot1='From '+ str(slot1['start_time']) +' To ' + str(slot1['end_time'])
                dick={'id':x['id'],'sport1':sport1,'arena1':arena1,'slot1': slot1}
                l1.append(dick)
            return render(request, "slotbook/staff_index1.html",{
                "message": "Slot made unavailable",
                "user_data": users.objects.all(),
                "l":l,
                "l1":l1,
                "sports":sports.objects.all(),
            })
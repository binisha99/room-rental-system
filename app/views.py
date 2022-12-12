from urllib import response
from django.shortcuts import render
from .models import appUser, Room, Room_request, SampleFile
import time as fathertime
import os
import base64
from django.db.models import Q
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse, reverse_lazy
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from random import randint
import datetime
from django.contrib import messages

def login_view(request):
    return render(request, "app/login_view.html", {"message": None})


def signup_view(request):
    return render(request, "app/signup_view.html", {"message": None})

def signup(request):
    if not validate_signUp(request):
        messages.success(request, "All fields with * is required. Thank You", extra_tags="0")
        return HttpResponseRedirect(reverse('signup_view'))

    else:
        if not email_validation(request):
            messages.success(request, "User with this email address already exists.", extra_tags="0")
            return HttpResponseRedirect(reverse('signup_view'))
        
        if not phone_validation(request):
            messages.success(request, "Please enter valid phone number. Thank You.", extra_tags="0")
            return HttpResponseRedirect(reverse('signup_view'))

        if not password_validation(request):
            messages.success(request, "Password must be atleast 8 character long.", extra_tags="0")
            return HttpResponseRedirect(reverse('signup_view'))

        username = request.POST.get('email', False)
        print("cool")
        try:
            exist = User.objects.filter(username=username)[0]
            return render(request, "app/signup_view.html", {"message": "user exists"})
        except:
            print("awesome")
            first = request.POST.get('first', False)
            last = request.POST.get('last', False)
            phone = request.POST.get('phone', False)
            email = request.POST.get('email', False)
            dob = request.POST.get('dob',False)
            password = request.POST.get('password', False)

            try:
                if appUser.objects.get(phone_number=request.POST.get('phone')):
                    print("dong")
                    return render(request, "app/signup_view.html", {"message": "user exists"})
            except appUser.DoesNotExist:
                print("ding0")
                pass        

            try:
                if first == '' or last == '' or phone == '' or password == '':
                    print("meep")
                    raise Exception('Some Fields are left Empty')
                try:
                    user = User.objects.create_user(username=str(
                        email), first_name=str(first), last_name=str(last), email=str(email), password=str(password))
                    print("User Created")
                except Exception as e:
                    user.delete()
                    raise Exception('Invalid User')
            except Exception as e:
                if user:
                    user.delete()
                print("Unable to create user")
                return render(request, "app/signup_view.html", {"message": e})

            user.save()
            verification_code = randint(10000, 99999)+user.id

            update_details = {
            'recipient_email': email,
            'email_subject': 'Koffee Doko | Registration verification code.',
            'email_body': f"""
                    Hi {first} {last},<br/><br/> You have registered. Your verification code is:
                    <span style="text-align:center;text-weight:bold"><h1>{verification_code}</h1></span><br/><br/>
                    <br/><br/>

                    Date Registered: <br/>
                    Note: This verification code expires soon. Please verify soon.</br>
                    Thank You,<br/>
                    Arun Thapa Chowk, Jhamsikhel,<br/>
                    Nepal.<br/>
                    9841360559
                    """
            }

            appuser = appUser.objects.create(
                user=user, phone_number=phone, date_of_birth=dob, verification_code=verification_code)
            if appuser:
                print("appUser Created")
                # if send_verification_email(request, update_details, user):
                #     pass
                # else:
                #     user.delete()
            appuser.save()
            print("Ding1")
            user1 = authenticate(request, username=username, password=password)
            print("Ding2")
            if user1 is not None:
                print("Ding3")
                login(request, user1)
                print("Ding4")
                return HttpResponseRedirect(reverse("index"))
            else:
                print("Ding5")
                return render(request, "app/login.html", {"message": "Invalid"}) 

def email_validation(request):
    try:
        user = User.objects.get(email=request.POST['email'])
        return False
    except User.DoesNotExist:
        return True
        
def phone_validation(request):
    if len(request.POST['phone'])<7:
        return False

    if '@' in request.POST['phone'] or '-' in request.POST['phone'] or '/' in request.POST['phone'] or '\\' in request.POST['phone'] or '#' in request.POST['phone'] or '$' in request.POST['phone']:
        return False
    return True


def password_validation(request):
    if len(request.POST['password'])<8:
        return False

    return True



def validate_signUp(request):
    
    if not request.POST['email']:
        return False

    if not request.POST['first']:
        return False

    if not request.POST['last']:
        return False

    if not request.POST['phone']:
        return False

    if not request.POST['password']:
        return False

    return True
def check_user(username):
    try:
        user = User.objects.get(username=username)
        if user:
            return True
        return False
    except Exception as e:
        print("Exception: "+e)
    return "Error"    

def check_landlord(username):
    try:
        user = appUser.objects.get(user=User.objects.get(username=username)).landlord_status
        if user:
            return True
        return False
    except:
        print("Not Landlord")
    return False

def check_tenant(username):
    try:
        user = appUser.objects.get(user=User.objects.get(username=username)).tenant_status
        if user:
            return True
        return False
    except:
        print("Not tenant")
    return False


def do_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        trying_user = appUser.objects.get(user = User.objects.get(username = username))
        if trying_user.blocked_status == True:
            logout(request)
            return render(request, "app/login_view.html", {"message": "You Have been blocked by the admin. Try contacting the Administrator via email"})
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/login_view.html", {"message": "Invalid username or password."}) 

@login_required(login_url=reverse_lazy("login_view"))
def logout_view(request):
    logout(request)
    return render(request, "app/index.html", {"message": "Logged Out"})

@login_required(login_url=reverse_lazy("login_view"))
def become_tenant(request):
    try:
        user = appUser.objects.get(user = User.objects.get(username=request.user.username))
    except Exception as e:
        print("Doomed 11 "+e)
        return HttpResponse("not a user")
    if user.tenant_status == False:
        user.tenant_status = True
        user.save()
    return HttpResponseRedirect(reverse("index"), {"messege": "Successfully registered as Tenant"}) 
    
    # render(request, "app/index.html", {"message": "Successfully registered as Tenant"})

@login_required(login_url=reverse_lazy("login_view"))
def become_landlord(request):
    try:
        user = appUser.objects.get(user = User.objects.get(username=request.user.username))
    except Exception as e:
        print("Doomed 11 "+e)
        return HttpResponse("not a user")
    if user.landlord_status == False:
        user.landlord_status = True
        user.save()
    
    return HttpResponseRedirect(reverse("index"), {"messege": "Successfully registered as landlord"})

@login_required(login_url=reverse_lazy("signup_view"))
def make_room(request):
    try: 
        user = appUser.objects.get(user = User.objects.get(username=request.user.username))
    except Exception as e:
        print("You doomed"+ e)
        return HttpResponse("Sed")
    if check_landlord(request.user.username) == False:
        return HttpResponse("Not a Landlord")
    name = request.POST.get('name', False)
    location = request.POST.get('location',False)
    facilities = request.POST.get('facilities',False)
    price = request.POST.get('price',False)
    time = str(datetime.datetime.now())
    path = os.path.join(os.getcwd()+'/app/static/app/uploads/rooms/', time)
    
    l = 'static/app/uploads/rooms/'+time
    os.mkdir(path)
    print(request.FILES['images'])
    pic_data_coded = request.FILES['images']
    fs = FileSystemStorage(location=path)
    filename = fs.save("aa.jpg", pic_data_coded)
    
    try: 
        room = Room.objects.create(name= name, location=location, facilities=facilities,price=price, landlord=user, photos = l)
        room.save()
    except Exception as e:
        print("You done fed up now:: " + e)
        return HttpResponse("Oh so sad u died")
    print("room created")
    context = {
        "landlord": check_landlord(request.user.username),
        "tenant": check_tenant(request.user.username),  
        "message": "Room Created",
        
    }
    return render(request, "app/index.html", context)

@login_required(login_url=reverse_lazy("signup_view"))
def clear_room(request):
    if check_user(request.user.username) and check_landlord(request.user.username):
        
        
        try:
            room = Room.objects.get(id = request.POST.get("id"))
            room.tenant = ''
            room.status = 'Empty'
            room.save()
        except Exception as e:
            print("********\n"+ str(e))
            return HttpResponse("error occured")
        context = {
        "landlord": check_landlord(request.user.username),  
        "tenant": check_tenant(request.user.username),
        "message": "Room Cleared",
        
        }
        return render(request, "app/index.html", context)
        
    return HttpResponse("Not user or Landlord")

@login_required(login_url=reverse_lazy("signup_view"))
def manage_rooms(request):
    if check_user(request.user.username) and check_landlord(request.user.username):
        if request.method == 'POST':
            room_id = request.POST.get('id')
            room = Room.objects.get(id =  room_id)
            l = room.photos
            name = request.POST.get('name', False)
            location = request.POST.get('location',False)
            facilities = request.POST.get('facilities',False)
            price = request.POST.get('price',False)
            status = request.POST.get('status', "Empty")
            try:
                pic_data_coded = request.FILES['images']
                time = str(datetime.datetime.now())
                path = os.path.join(os.getcwd()+'/app/static/app/uploads/rooms/', time)
                
                l = 'static/app/uploads/rooms/'+time
                os.mkdir(path)
                print(request.FILES['images'])
                
                fs = FileSystemStorage(location=path)
                filename = fs.save("aa.jpg", pic_data_coded)
            except:
                l =  room.photos
            try:
                room.name = name
                room.location = location
                room.facilities = facilities
                room.price = price
                room.photos = l
                room.status = status
                room.save()
                return HttpResponseRedirect(reverse("index"),{"message": "Succcessfully updated room"})
            except Exception as e:
                return HttpResponse(e)
        else:  
            print("not post")
            rooms = []
            try: 
                landlord = appUser.objects.get(user = User.objects.get(username = request.user.username))
                for room in Room.objects.filter(landlord = landlord):
                    rooms.append({
                        "id": room.id,
                        "name": room.name, 
                        "location":  room.location,
                        "facilities":  room.facilities,
                        "price":  room.price,
                        "photos":  room.photos,
                        "tenant":  room.tenant,
                        "status": str(room.status)
                    })
                print(rooms)
                context = {
                    "rooms": rooms,
                    "landlord": True,
                    "tenant": check_tenant(request.user.username)
                }
                return render(request, "app/manage_rooms.html", context)
            except Exception as e:
                print("zorp ")
                print(e)
                return HttpResponse("nope")
    return HttpResponse("Not user or Landlord")

@login_required(login_url=reverse_lazy("signup_view"))
def requested(request):
    if check_user(request.user.username) and check_landlord(request.user.username):
        if request.method == 'POST':
            req_id = request.POST.get('req_id',False)
            req = Room_request.objects.get(id = req_id)
            room = Room.objects.get(id = req.room_id)
            try:
                room.tenant = req.from_user.user.username
                req.status = 2
                room.status = "Occupied"
                room.save()
                req.save()
            except Exception as e:
                print("********\n"+ str(e))
                return HttpResponse("error occured")
            context = {
            "landlord": check_landlord(request.user.username),  
            "tenant": check_tenant(request.user.username),
            "message": "Room booked",
            
            }
            return render(request, "app/index.html", context)
        else:
            res = []
            try:
                landlord = appUser.objects.get(user = User.objects.get(username = request.user.username))
                rooms = Room.objects.filter(landlord = landlord)
                reqs = Room_request.objects.all()
                for room in rooms:
                    for req in reqs:
                        if req.room_id == room.id and int(req.status) == 1:
                            res.append({
                                "req_id": req.id,
                                "req_date": req.requested_date,
                                "room_name": room.name,
                                "location": room.location,
                                "tenant": req.from_user,
                                "status": req.get_req_status()
                            })
                print(res)
                context = {
                    "room_requests": res,
                    "landlord": True,
                    "tenant": check_tenant(request.user.username)
                }
                return render(request, "app/requested.html", context)
            except Exception as e:
                print("zorp11 "+ str(e))
                return HttpResponse("nope")
    return HttpResponse("Not user or tenant")

@login_required(login_url=reverse_lazy("signup_view"))
def my_requests(request):
    if check_user(request.user.username) and check_tenant(request.user.username):
        res = []
        try:
            tenant = appUser.objects.get(user = User.objects.get(username = request.user.username))
            reqs = Room_request.objects.filter(from_user = tenant)
            
            for req in reqs:
                room = Room.objects.get(id = req.room_id)
                res.append({
                    "req_id": req.id,
                    "req_date": req.requested_date,
                    "room_name": room.name,
                    "location": room.location,
                    "tenant": req.from_user,
                    "status": req.get_req_status()
                })
            print(res)
            context = {
                "room_requests": res,
                "landlord": check_landlord(request.user.username),
                "tenant": True
            }
            return render(request, "app/my_requests.html", context)
        except Exception as e:
            print("zorp11 "+ str(e))
            return HttpResponse("nope")
    return HttpResponse("Not user or Landlord")

@login_required(login_url=reverse_lazy("signup_view"))
def request_room(request):
    if check_user(request.user.username) and check_tenant(request.user.username):
        if request.method == 'POST':

            room_id = request.POST.get('id',False)
            tenant = appUser.objects.get(user = User.objects.get(username = request.user.username))
            room_reqs = Room_request.objects.filter(from_user = tenant)
            for r in room_reqs:
                
                if int(r.room_id) == int(room_id[0]) and int(r.status) == 1:
                    return HttpResponse("pending Room request already exisits") 
            
            
            try:
                req = Room_request.objects.create(room_id = int(room_id[0]), from_user=tenant)
                req.save()
                context = {
                    "message": "request sent",
                    "landlord": check_landlord(request.user.username),
                    "tenant": True
                }
                return render(request, "app/index.html", context)
            except Exception as e:
                print("fail "+ e)
                return HttpResponse("Nopee")
        else:
            res = []
            try:
                rooms = Room.objects.all()
                for room in rooms:
                    if room.status == "Empty":
                        res.append({
                                "id": room.id,
                                "name": room.name, 
                                "location":  room.location,
                                "facilities":  room.facilities,
                                "price":  room.price,
                                "photos":  room.photos,
                            })
                print(res)
                context = {
                        "rooms": res,
                        "landlord": check_landlord(request.user.username),
                        "tenant": True
                    }
                return render(request, "app/request_room.html", context)
            except Exception as e:
                print("zorp133 "+ e)
                return HttpResponse("nope")
    print("Horppp")
    return HttpResponse("Not user or Landlord")

@login_required(login_url=reverse_lazy("login_view"))
def view_rooms(request):
    if check_user(request.user.username) and check_tenant(request.user.username):
        res = []
        try:
            rooms = Room.objects.all()
            for room in rooms:
                if room.status == "Empty":
                    res.append({
                            "id": room.id,
                            "name": room.name, 
                            "location":  room.location,
                            "facilities":  room.facilities,
                            "price":  room.price,
                            "photos":  room.photos,
                        })
            print(res)
            context = {
                    "rooms": res,
                    "landlord": False,
                    "tenant": True
                }
            return render(request, "app/view_rooms.html", context)
        except Exception as e:
            print("zorp133 "+ e)
            return HttpResponse("nope")
    print("zorppp")
    return HttpResponse("Not user or tenant")



def index(request):
    context = {}
    if request.user.username:
        context = {
            "landlord": check_landlord(request.user.username),
            "tenant": check_tenant(request.user.username),
            }
        print(context)
    return render(request, "app/index.html", context)

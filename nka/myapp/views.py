
from distutils.command.config import config
import email
import re
import string
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from virtualenv import session_via_cli
from mypro import settings
import pyrebase
from django.contrib import auth


config = {
  "apiKey": "AIzaSyBh54bhUiOduOlyq6k6DTTeXL_lAg0L94w",
  "authDomain": "cpanel-10ae6.firebaseapp.com",
  "databaseURL":"https://cpanel-10ae6-default-rtdb.firebaseio.com",
  "projectId": "cpanel-10ae6",
  "storageBucket": "cpanel-10ae6.appspot.com",
  "messagingSenderId": "206710126999",
  "appId": "1:206710126999:web:ee4da3d9d3f7de6bd4ecd2"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


# Create your views here.
def sign(request):
    return render(request, 'sign.html')

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:

        user = authe.sign_in_with_email_and_password(email,password)

    except:
        message = "Invalid user"
        return render(request, 'sign.html',{"m":message})

    session_id = user["idToken"]
    request.session["uid"]=str(session_id)
    return render(request, 'postsign.html',{"e":email})



def logout(request):
    auth.logout(request)
    return render(request, 'sign.html')


def up(request):

    return render(request, 'up.html')


def postup(request):

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:


        user = authe.create_user_with_email_and_password(email,password)

    except:
        message = "Invalid details"
        return render(request, 'up.html',{"m":message})

    user1 = user['idToken']


    authe.send_email_verification(user1)
    messag = "verification link sent, Kindly confirm then signup"
    

    return render(request, "sign.html",{"rw":messag})


def fp(request):
    return render(request, "fp.html")

def postfp(request):

    email = request.POST.get('email')

    authe.send_password_reset_email(email)

    message = "Reset link sent"

    return render(request, "sign.html", {"r":message})

def create(request):
    

    return render(request, "create.html")


def postcreate(request):


    #email = request.POST.get("email")
    #name = request.POST.get("name")
    cname = request.POST.get("cname")
    cid = request.POST.get("cid")
    ename = request.POST.get("ename")
    clevel = request.POST.get("clevel")
    csp = request.POST.get("csp")
    validity = request.POST.get("validity")
    edate = request.POST.get("edate")
    cdate = request.POST.get("cdate")

    url = request.POST.get("url")


    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a["users"]
    a = a[0]
    email = a["email"]
    a = a["localId"]
    

    data = {
        "csp":csp,
        "clevel":clevel,
        "cname":cname,
        "cid":cid,
        "url":url,
        "edate":edate,
        "cdate":cdate,
        "validity":validity,
        "ename":ename

    }

    database.child("users").child(a).child(csp+"  "+ cname).set(data)


    subject = " Update from certihub "
    message = "new certificate has been created in your account"
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)



    #nu = database.child("users").child(a).child("p_details").child("name").get().val()
    messag = "certificate added succsessfully"

    return render(request, "postsign.html",{"m":messag,"e":email})



def existing(request):


    if request.method == "GET" and "csrfmiddlewaretoken" in request.GET:
        search = request.GET.get("search")
        search = search.lower()

        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a["users"]
        a = a[0]
        uid = a["localId"]

        #uid = request.GET.get("uid")
       
        to_sho = database.child("users").child(uid).shallow().get().val()
        work_id = []

        for i in to_sho:
            wor = database.child("users").child(uid).child(i).child("cid").get().val()
            wor = str(wor)+"$"+str(i)
            work_id.append(wor)

        matching = [str(string) for string in work_id if search in string.lower()]

        s_work = []
        s_id = []

        for i in matching:
            work,id=i.split("$")
            s_work.append(work)
            s_id.append(id)

        fin = zip(s_id,s_work)

        return render(request, "existing.html", {"m":fin,"uid":uid})

    else:

        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a["users"]
        a = a[0]
        a = a["localId"]


        try:

            to_show = database.child("users").child(a).shallow().get().val()
            lis = []

            for i in to_show:
                lis.append(i)


            ind_ls = []

            for i in lis:

            
                wo = database.child("users").child(a).child(i).child("cid").get().val()

                ind_ls.append(wo)

            fin = zip(lis,ind_ls)

            return render(request, "existing.html", {"m":fin,"uid":a})

        except:
            message = "you do not have any existing certification"
            return render(request, 'postsign.html',{"m":message})


def pe(request):

    b = request.GET.get("z")

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a["users"]
    a = a[0]
    a = a["localId"]

    wor1 = database.child("users").child(a).child(b).child("csp").get().val()
    wor2 = database.child("users").child(a).child(b).child("cid").get().val()
    wor3 = database.child("users").child(a).child(b).child("cname").get().val()
    wor4 = database.child("users").child(a).child(b).child("clevel").get().val()
    wor5 = database.child("users").child(a).child(b).child("url").get().val()
    wor6 = database.child("users").child(a).child(b).child("edate").get().val()
    wor7 = database.child("users").child(a).child(b).child("cdate").get().val()
    wor8 = database.child("users").child(a).child(b).child("ename").get().val()
    wor9 = database.child("users").child(a).child(b).child("validity").get().val()

    return render(request, "pe.html", {"cid":wor2,"cname":wor3,"csp":wor1,"clevel":wor4,"c":b,"cimg":wor5,"edate":wor6,"cdate":wor7,
    "ename":wor8,"validity":wor9})

def delete(request):
    b = request.GET.get("w")

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a["users"]
    a = a[0]
    email = a["email"]
    a = a["localId"]

    database.child("users").child(a).child(b).set({})

    subject = " Update from certihub "
    message = "a certificate has been deleted from your account"
    from_email = settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    

    return render(request, "postsign.html")

def cancelsignup(request):

    return render(request, "sign.html")

    
    


from django.shortcuts import render,HttpResponse

def index(request):
    return render(request, "index.html")

def welcome(request):
    return render(request, "welcome.html")
def memberlist(request):
    return render(request, "member-list.html")
def memberadd(request):
    return render(request, "member-add.html")
def memberdel(request):
    return render(request, "member-del.html")
def memberedit(request):
    return render(request, "member-edit.html")
def memberpwd(request):
    return render(request, "member-password.html")
def orgtree(request):
    return render(request, "orgtree.html")
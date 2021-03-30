from django.shortcuts import render, redirect
from django.views import View
from .models import Stuff, MyUser
# Create your views here.

class Home(View):
    def get(self,request):
        return render(request,"home.html",{})
    def post(self,request):
        try:
            m = MyUser.objects.get(name=request.POST['name'])
            isValid = (m.password == request.POST['password'])
        except:
            pass
        if isValid:
            return redirect("/things/")
        else:
            return render(request,"home.html",{})


class Things(View):
    def get(self,request):
        things = map(str,list(Stuff.objects.all()))
        return render(request, "things.html", {"things":things})
    def post(self,request):
        s = request.POST.get('stuff','')
        if s != '':
            newThing = Stuff(name=s)
            newThing.save()
        things = map(str,list(Stuff.objects.all()))
        return render(request, "things.html", {"things":things})

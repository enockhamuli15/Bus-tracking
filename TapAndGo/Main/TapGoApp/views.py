from django.shortcuts import redirect, render
from django.views.generic import  DeleteView, CreateView, UpdateView, DetailView
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
# Create your views here.





    ####   "CREATING VIEWS" #####

def registration(request):
    form = AccountForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            
            form.save()
            return redirect('login_now')
        else:
            return render(request, 'register.html' , {'register_here':form})
    else:
        form = AccountForm()
        return render(request, 'register.html', {'register_here':form})


class NationalIdPost(LoginRequiredMixin, CreateView):
    form_class = NationalForm
    model = NationalId
    template_name = 'report.html'
    success_url = reverse_lazy('profile')


class HealthPost(LoginRequiredMixin, CreateView):
    form_class = HealthForm
    model = HealthReport
    template_name = 'report.html'
    success_url = reverse_lazy('profile')


    def get_object(self, slug=None):
        slug = self.kwargs.get('id_num')
        citizen = NationalId.objects.get(id_num=slug)
        return citizen

    def form_valid(self, form):
        user = NationalId.objects.get(user=self.get_object)
        form.instance.citizen = user.id
        return super().form_valid(form)

class CardPost(LoginRequiredMixin, CreateView):
    form_class = CardForm
    model = Card
    template_name = 'report.html'
    success_url = reverse_lazy('profile')


class ProfilePost(LoginRequiredMixin, CreateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'report.html'
    success_url = reverse_lazy('profile')

    #### ????? #####

    def form_valid(self, form):
        user = PersonnalizedAccount.objects.get(id=self.request)
        form.instance.citizen = user
        return super().form_valid(form)

class CashPost(LoginRequiredMixin, CreateView):
    form_class = CashForm
    model = Cash
    template_name = 'report.html'
    success_url = reverse_lazy('profile')

class RoadPost(CreateView):
    form_class = RoadForm
    model = Road
    template_name = 'road.html'
    success_url = reverse_lazy('roads')

class BusStationPost(LoginRequiredMixin, CreateView):
    form_class = BusStationForm
    model = BusStation
    template_name = 'report.html'
    success_url = reverse_lazy('profile')

class BusPost(LoginRequiredMixin, CreateView):
    form_class = BusForm
    model = Bus
    template_name = 'report.html'
    success_url = reverse_lazy('profile')



    ###### DETAILS #####

def busDetailView(request):
    
    if request.method == 'POST':
        
        form2 = BusForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect('buses')

            
        else:
            context = {
                
                'form_bus' : form2
            }
            return render(request, 'buses.html' , context)

    else:
        
        form2 = BusForm()
        context = {
            
            'form_bus' : form2,
            'stations': BusStation.objects.all(),
            'bus_assign': Bus.objects.all(),
            'profile': Profile.objects.filter(account=request.user),
        }
        return render(request, 'buses.html' , context)

def station(request):
    
    if request.method == 'POST':
        form = BusStationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('stations')

       
        else:
            context = {
                'form_station':form,
                
            }
            return render(request, 'station.html' , context)

    else:
        form = BusStationForm()
      
        context = {
            'form_station':form,
            'stations': BusStation.objects.all(),
            'bus_assign': Bus.objects.all(),
            'profile': Profile.objects.filter(account=request.user),
        }
        return render(request, 'station.html' , context)

def user(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            card = Card.objects.get(pk = form.instance.cardNum.id)
            card.status = 'online'
            card.save()
            form.save()
            return redirect('user')
        else:
            return render(request, 'User.html' , {'add_user':form})

    else:
        form = ProfileForm()
        context = {
            'profile': Profile.objects.filter(account=request.user),
            'add_user':form,
            'all_user': Profile.objects.all()
        }
        return render(request, 'User.html' , context)
    


def roads(request):
    if request.method == 'POST':
        form = RoadForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('roads')
        else:
            return render(request, 'road.html' , {'form_road':form})

    else:
        form = RoadForm()
        context = {
            'profile': Profile.objects.filter(account=request.user),
            'form_road':form,
            'roads': Road.objects.all()
        }
        return render(request, 'road.html' , context)


def balance(request):
    check_type = Profile.objects.get(account=request.user)
    if check_type.typeUser == 'Admin':
        template = 'balance.html'
    elif check_type.typeUser == 'Agent':
        template = 'balance.html'
    else:
        template = 'passenger.html'

    if request.method == 'POST':
        form = CashForm(request.POST)
        
        if form.is_valid():
            #profile = Profile.objects.filter(account = form.instance.account.id)
            card = Card.objects.get(pk = form.instance.account.cardNum.id)
            total = card.balance + form.instance.balance
            card.balance = total
            card.save()
            form.save()
            return redirect('balance')
        else:
            return render(request, template , {'form':form})

    else:
        form = CashForm()
        context = {
            'profile': Profile.objects.filter(account=request.user),
            'form':form,
            'cash': Cash.objects.all(),
            'my_cash': Cash.objects.filter(account=check_type)
        }
        return render(request, template , context)
   


def dashboard(request):
    check_type = Profile.objects.get(account=request.user)
    template = 'dashboard.html'
    if request.user.is_staff:
        template = 'dashboard.html'

    else:
        check_type = Profile.objects.get(account=request.user)
        if check_type.typeUser == 'Agent':
                template = 'agent_dashboard.html'
        if check_type.typeUser == 'Passenger':
                template = 'passenger.html'


    income = Card.objects.all()
    output = 0.0
    for show in income:
        output = show.get_transaction_total


    context = {
        'profile': check_type,
        'card_inuse': Card.objects.filter(status='online').count(),
        'bus': Bus.objects.all().count(),
        'roads':Road.objects.all().count(),
        'stations':BusStation.objects.all().count(),
        'agents':Profile.objects.filter(typeUser='Agent').count(),
        'drivers':Profile.objects.filter(typeUser='Driver').count(),
        'passengers':Profile.objects.filter(typeUser='Passenger').count(),
        'my_cash': Cash.objects.filter(account=check_type),
        'agent_add_user': Profile.objects.all(),
        'add_user': AssignForm(),
        'output': output
    }
    return render(request, template, context)


def drivers(request):
    query = Profile.objects.filter(typeUser='Driver')
    
    context = {
        'profile': Profile.objects.filter(account=request.user),
        'all_drivers': query
    }
    return render(request, 'driver.html' , context)

def passenger(request):
    
    context = {
        'profile': Profile.objects.get(account=request.user),
        'all_passengers': Profile.objects.filter(typeUser='Passenger')
    }
    return render(request, 'passengers.html' , context)

def records(request):
    if request.method == 'POST':
        form = NationalForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('records')
        else:
            return render(request, 'external_records.html' , {'national':form})

    else:
        form = NationalForm()
        context = {
            #'profile': Profile.objects.filter(account=request.user),
            'national':form,
            'citizen': NationalId.objects.all()
        }
        return render(request, 'external_records.html' , context)


def health(request):
    if request.method == 'POST':
        form = HealthForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('health')
        else:
            return render(request, 'health.html' , {'health':form})

    else:
        form = HealthForm()
        context = {
            #'profile': Profile.objects.filter(account=request.user),
            'health':form,
            'citizen_health': HealthReport.objects.all()
        }
        return render(request, 'health.html' , context)



def cards(request):
    
    if request.user.is_staff:
        if request.method == 'POST':
            form = CardForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('cards')
            else:
                return render(request, 'cards.html' , {'card_form':form})

        else:
            form = CardForm()
            context = {
                'card_form':form,
                'cards': Card.objects.all(),
                'profile': Profile.objects.get(account=request.user),
            }
            return render(request, 'cards.html' , context)
    else:
        return redirect('/')

def track(request):
    context = {
        
        'profile': Profile.objects.get(account=request.user),
    }
    return render(request, 'track_bus.html', context)

    

    ########  UPDATE & DELETE ACTIONS #########


class RoadUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RoadForm
    model = Road
    template_name = 'edit_form.html'
    success_url = reverse_lazy('roads')
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editform"]=context["form"]

        return context

class DeleteRoad(LoginRequiredMixin, DeleteView):
    model = Road
    template_name = 'delete_form.html'
    success_url = reverse_lazy('roads')

class CardUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CardForm
    model = Card
    template_name = 'edit_form.html'
    success_url = reverse_lazy('cards')
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editform"]=context["form"]

        return context

class DeleteCard(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'delete_form.html'
    success_url = reverse_lazy('cards')

class BusStationUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BusStationForm
    model = BusStation
    template_name = 'edit_form.html'
    success_url = reverse_lazy('buses')
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editform"]=context["form"]

        return context

class DeleteBusStation(LoginRequiredMixin, DeleteView):
    model = BusStation
    template_name = 'delete_form.html'
    success_url = reverse_lazy('buses')

class BusUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BusForm
    model = Bus
    template_name = 'edit_form.html'
    success_url = reverse_lazy('buses')
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editform"]=context["form"]

        return context

class DeleteBus(LoginRequiredMixin, DeleteView):
    model = Bus
    template_name = 'delete_form.html'
    success_url = reverse_lazy('buses')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    model = Profile
    template_name = 'edit_form.html'
    success_url = reverse_lazy('user')
   
    def get_object(self, pk=None):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(account=pk)
      
       
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editform"]=context["form"]
        
        return context




class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'delete_form.html'
    success_url = reverse_lazy('user')

class UserDetailView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'detail_user.html'
    
    def get_object(self, cardNum=None):
        cardNum = self.kwargs.get('cardNum')
        profile = Profile.objects.get(cardNum__cardnum=cardNum)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cardNum = self.kwargs.get('cardNum')
        profile = Profile.objects.get(cardNum__cardnum=cardNum)
        context['profile'] = profile

        return context

def increment(request, pk):

    card_info = Card.objects.get(cardnum=pk)
    profile = Profile.objects.get(cardNum__cardnum=card_info)
    available_sits = Bus.objects.get()
  
    amount = 200.00
    new_balance = 0.0
    new_transaction = 0.0

   
    if card_info.balance >= amount:
        new_balance = card_info.balance - amount
        new_transaction = card_info.transaction + amount
        card_info.position = True
        card_info.balance=new_balance
        card_info.transaction = new_transaction
        card_info.save()
        card_true = Card.objects.filter(position=True).count()

        available_sits.sitAvailable = available_sits.sitNum - card_true
        available_sits.save()

        
    else:
        pass

    context = {
        
        'ID': profile.health.citizen.id_num,
        'Name': profile.account.first_name +" "+ profile.account.last_name,
        'Health report': profile.health.report,
        'CardId': card_info.cardnum,
        'Balance': card_info.balance,
        'Card location': card_info.position,
        'Card status': card_info.status,
        'User type': profile.typeUser
    }

  
    return JsonResponse(context, safe=False)


def decrement(request, pk):
    card_info = Card.objects.get(cardnum=pk)
    profile = Profile.objects.get(cardNum__cardnum=card_info)
    available_sits = Bus.objects.get()
    card_info.position = False
    card_info.save()
   

    available_sits.sitAvailable = available_sits.sitAvailable + 1
    available_sits.save()
    

    
    context = {
        
        'ID': profile.health.citizen.id_num,
        'Name': profile.account.first_name +" "+ profile.account.last_name,
        'Health report': profile.health.report,
        'CardId': card_info.cardnum,
        'Balance': card_info.balance,
        'Card location': card_info.position,
        'Card status': card_info.status,
        'User type': profile.typeUser
    }
    
    return JsonResponse(context, safe=False)

    
def sits(self, pk):
    bus = Bus.objects.get(pk=pk)
    context = {
        'Sits available': bus.sitAvailable
    }
    return JsonResponse(context, safe=False)

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from . forms import SignUpForm,RoomForm,PersonForm,TransactionForm
from . models import Room,Person,Transaction, TransactionDetail
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_rooms = Room.objects.filter(created_by=request.user)
        return render(request, 'index.html', {'rooms': user_rooms})
    else:
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}.')
                return redirect('index') 
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'logged out successfully!')
        return redirect('index') 
    #optional
    elif request.method == 'GET':
        return redirect('index') 

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('index') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def newroom(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            messages.success(request, f'Room created Successfully!')
            return redirect('index')
    else:
        form = RoomForm()
    return render(request, 'newroom.html', {'form': form})

@login_required
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Person created Successfully!')
            return redirect('index')
    else:
        form = PersonForm(user = request.user)
    return render(request, 'add_person.html', {'form' : form})

def view_members(request, room_id):
    room = get_object_or_404(Room, pk=room_id) 
    members = room.people.all()
    return render(request, 'view_members.html', {'room': room, 'members': members})

@login_required
def transactions(request, room_id):
    roomObj = Room.objects.get(id=room_id)
    members = Person.objects.filter(room=roomObj)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            persons = form.cleaned_data['persons']
            paid_amount = form.cleaned_data['paid']
            who_paid = form.cleaned_data['who_paid']
            
            # Calculate the amount each person should be charged
            num_persons = len(persons)
            charged_amount = paid_amount / num_persons
            
            # Update the paid amount for the person who actually paid
            who_paid.paid += round(paid_amount, 2)
            who_paid.charged += round(charged_amount, 2)
            who_paid.balance += round(paid_amount - charged_amount, 2)
            who_paid.save()
            
            # Create TransactionDetail entries and update balances for all persons
            for person in persons:
                TransactionDetail.objects.create(
                    transaction=transaction,
                    person=person,
                    paid=0,  # Only the who_paid person has paid, others have 0
                    who_paid=who_paid
                )
                
                if person != who_paid:
                    person.charged += round(charged_amount, 2)
                    person.balance -= round(charged_amount, 2)  # Balance will be negative for others
                    person.save()
            messages.success(request, 'Transaction added Successfully')
            return HttpResponseRedirect(request.get_full_path())
                    
    else:
        form = TransactionForm()
        form.fields['persons'].queryset = members
        form.fields['who_paid'].queryset = members

    return render(request, 'transaction.html', {
        'roomId': room_id,
        'roomObj': roomObj,
        'members': members,
        'form': form
    })


@login_required
def settle(request,room_id):
    roomObj = Room.objects.get(id=room_id)
    members = Person.objects.filter(room=roomObj)
    owed_users = [user for user in members if user.balance > 0]
    owing_users = [user for user in members if user.balance < 0]
    
    transactions = []
    while owing_users and owed_users:
        owing = owing_users[0]
        owed = owed_users[0]
        
        amount = min(-owing.balance, owed.balance)
        
        transactions.append({
            'from': owing.name,
            'to': owed.name,
            'amount': amount
        })
        
        owing.balance += amount
        owed.balance -= amount

        if owing.balance == 0:
            owing_users.pop(0)
        if owed.balance == 0:
            owed_users.pop(0)
    return render(request,'settle.html',{'settle' : transactions})
        
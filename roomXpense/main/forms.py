from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Room,Person,Transaction, TransactionDetail

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room 
        fields = ['name']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'contact', 'room']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['room'].queryset = Room.objects.filter(created_by=user)


class TransactionForm(forms.ModelForm):
    persons = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Members Included"
    )
    paid = forms.FloatField(label="Amount Paid")
    who_paid = forms.ModelChoiceField(queryset=Person.objects.all(), label="Who Paid"
)
    class Meta:
        model = Transaction
        fields = ['product', 'persons', 'paid', 'who_paid']

class TransactionDetailForm(forms.ModelForm):
    class Meta:
        model = TransactionDetail
        fields = ['person', 'paid', 'who_paid']
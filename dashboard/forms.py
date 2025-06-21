from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Reservation
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from core.models import Reservation, Room
from core.models import Staff
from core.models import Payment
from core.models import Cleaning
from core.models import Product, ProductOrder
from django import forms
from core.models import Destination
from core.models import MaintenanceRequest


class AdminRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

class ReservationForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Reservation
        fields = ['guest', 'room', 'check_in', 'check_out', 'user']  # ✅ must be a list or tuple of field names


class StaffForm(forms.ModelForm):
    hired_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Staff
        fields = ['name', 'role', 'hired_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})  # assuming 'role' is a choice field

        
class PaymentForm(forms.ModelForm):
    paid_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Payment
        fields = ['reservation', 'amount', 'paid_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style dropdown for reservation
        self.fields['reservation'].widget.attrs.update({'class': 'form-select'})

        # Style amount input
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})


from django import forms
from core.models import Cleaning

class CleaningForm(forms.ModelForm):
    class Meta:
        model = Cleaning
        fields = ['room', 'staff', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Only rooms under maintenance
        self.fields['room'].queryset = Room.objects.filter(status='maintenance')
        self.fields['room'].widget.attrs.update({'class': 'form-select'})

        # ✅ Only staff with role 'housekeeping'
        self.fields['staff'].queryset = Staff.objects.filter(role='housekeeping')
        self.fields['staff'].widget.attrs.update({'class': 'form-select'})

        # Style status field
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = ProductOrder
        fields = ['user', 'produk', 'jumlah']  # ✅ user is the new link

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DestinationForm, self).__init__(*args, **kwargs)

        # Apply Bootstrap 'form-control' styling to all fields
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.Textarea, forms.URLInput)):
                widget.attrs.update({'class': 'form-control'})
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs.update({'class': 'form-select'})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({'class': 'form-check-input'})
        
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'room_type', 'status', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['number'].widget.attrs.update({'class': 'form-control'})
        self.fields['room_type'].widget.attrs.update({'class': 'form-select'})  # ✅ fixed
        self.fields['status'].widget.attrs.update({'class': 'form-select'})     # ✅ fixed
        

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MaintenanceRequestForm, self).__init__(*args, **kwargs)

        # ✅ Only rooms under maintenance
        self.fields['room'].queryset = Room.objects.filter(status='maintenance')
        self.fields['room'].widget.attrs.update({'class': 'form-select'})

        # ✅ Style reported_by field
        self.fields['reported_by'].queryset = Staff.objects.all()
        self.fields['reported_by'].widget.attrs.update({'class': 'form-select'})

        # ✅ Style issue and resolution_notes as text input/textarea
        self.fields['issue'].widget.attrs.update({'class': 'form-control'})
        self.fields['resolution_notes'].widget.attrs.update({'class': 'form-control'})

        # ✅ Boolean checkbox for resolved
        self.fields['resolved'].widget.attrs.update({'class': 'form-check-input'})
        
from django import forms
from core.models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']


from django import forms

class GuestClusterForm(forms.Form):
    age = forms.IntegerField(label="Age")
    visit_count = forms.IntegerField(label="Visit Count")
    avg_nights = forms.FloatField(label="Average Nights per Stay")
    spent_room = forms.FloatField(label="Total Room Spend ($)")
    spent_addon = forms.FloatField(label="Total Add-On Spend ($)")
    
    room_type = forms.ChoiceField(
        choices=[
            ("standard", "Standard"),
            ("deluxe", "Deluxe"),
            ("suite", "Suite"),
            ("family", "Family"),
            ("executive", "Executive"),
            ("presidential", "Presidential")
        ],
        label="Preferred Room Type"
    )

    payment_method = forms.ChoiceField(
        choices=[
            ("Cash", "Cash"),
            ("Credit Card", "Credit Card"),
            ("Transfer", "Transfer"),
            ("E-Wallet", "E-Wallet")
        ],
        label="Payment Method"
    )

    rating = forms.FloatField(label="Rating Given")

    def __init__(self, *args, **kwargs):
        super(GuestClusterForm, self).__init__(*args, **kwargs)

        # ✅ Style numeric inputs
        for field_name in ['age', 'visit_count', 'avg_nights', 'spent_room', 'spent_addon', 'rating']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

        # ✅ Style dropdowns
        self.fields['room_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-select'})






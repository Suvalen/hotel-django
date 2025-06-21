from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdminRegisterForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import Room, Reservation, Payment, Guest
from django.urls import reverse_lazy
from .forms import ReservationForm
from .forms import StaffForm
from django.db import models
from .forms import PaymentForm
from django.utils.timezone import now
from datetime import timedelta
from core.models import Payment
from django.db.models import Sum
from django.http import JsonResponse
from core.models import Cleaning
from .forms import CleaningForm
from core.models import Product, ProductOrder
from .forms import ProductForm, ProductOrderForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core.models import Invoice
from django import forms
from core.models import Coupon
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Destination
from .forms import DestinationForm
from core.models import MaintenanceRequest
from .forms import MaintenanceRequestForm
from .forms import RoomForm
from core.models import ProductOrder, ConfirmedProductOrder
import pandas as pd
import plotly.express as px


@login_required

def dashboard_home(request):
    total_sales = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Get most recent 7 snapshots
    snapshots = OccupancyRateSnapshot.objects.order_by('-date')[:7][::-1]

    chart_labels = [s.date.strftime('%Y-%m-%d') for s in snapshots]
    chart_occupied = [s.occupied_rooms for s in snapshots]
    chart_available = [s.available_rooms for s in snapshots]
    chart_maintenance = [s.maintenance_rooms for s in snapshots]

    context = {
        'total_sales': total_sales,
        'chart_labels': chart_labels,
        'chart_occupied': chart_occupied,
        'chart_available': chart_available,
        'chart_maintenance': chart_maintenance,
    }

    return render(request, 'admin_lte/dashboard.html', context)

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('admin-login')
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_lte/register.html', {'form': form})

def room_dashboard(request):
    return render(request, 'admin_lte/rooms.html')

def guest_dashboard(request):
    return render(request, 'admin_lte/guests.html')

def reservation_dashboard(request):
    return render(request, 'admin_lte/reservations.html')

def payment_dashboard(request):
    return render(request, 'admin_lte/payments.html')

def staff_dashboard(request):
    return render(request, 'admin_lte/staff.html')

#ROOM MODELS
class RoomListView(ListView):
    model = Room
    template_name = 'admin_lte/rooms/list.html'
    context_object_name = 'rooms'


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm  
    template_name = 'admin_lte/rooms/form.html'
    success_url = reverse_lazy('room-dashboard')


class RoomUpdateView(UpdateView):
    model = Room
    # We exclude 'price' here because save() auto-sets it.
    form_class = RoomForm  
    template_name = 'admin_lte/rooms/form.html'
    success_url = reverse_lazy('room-dashboard')


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'admin_lte/rooms/delete_confirm.html'
    success_url = reverse_lazy('room-dashboard')




# GUEST MODELS
class GuestListView(ListView):
    model = Guest
    template_name = 'admin_lte/guests/list.html'
    context_object_name = 'guests'

class GuestCreateView(CreateView):
    model = Guest
    fields = ['name', 'email', 'phone']
    template_name = 'admin_lte/guests/form.html'
    success_url = reverse_lazy('guest-dashboard')

class GuestUpdateView(UpdateView):
    model = Guest
    fields = ['name', 'email', 'phone']
    template_name = 'admin_lte/guests/form.html'
    success_url = reverse_lazy('guest-dashboard')

class GuestDeleteView(DeleteView):
    model = Guest
    template_name = 'admin_lte/guests/delete_confirm.html'
    success_url = reverse_lazy('guest-dashboard')
    
    #RESERVATION MODEL

class ReservationListView(ListView):
    model = Reservation
    template_name = 'admin_lte/reservations/list.html'
    context_object_name = 'reservations'

class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'admin_lte/reservations/form.html'
    success_url = reverse_lazy('reservation-dashboard')
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user  # if using Django's auth
        return super().form_valid(form)

class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'admin_lte/reservations/form.html'
    success_url = reverse_lazy('reservation-dashboard')

class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'admin_lte/reservations/delete_confirm.html'
    success_url = reverse_lazy('reservation-dashboard')
    
    from core.models import Payment
    

    
    #PAYMENT MODEL
class PaymentListView(ListView):
    model = Payment
    template_name = 'admin_lte/payments/list.html'
    context_object_name = 'payments'

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm 
    template_name = 'admin_lte/payments/form.html'
    success_url = reverse_lazy('payment-dashboard')

class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'admin_lte/payments/form.html'
    success_url = reverse_lazy('payment-dashboard')

class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'admin_lte/payments/delete_confirm.html'
    success_url = reverse_lazy('payment-dashboard')


from core.models import Staff
#staff model
class StaffListView(ListView):
    model = Staff
    template_name = 'admin_lte/staff/list.html'
    context_object_name = 'staffs'

class StaffCreateView(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'admin_lte/staff/form.html'
    success_url = reverse_lazy('staff-dashboard')

class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'admin_lte/staff/form.html'
    success_url = reverse_lazy('staff-dashboard')

class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'admin_lte/staff/delete_confirm.html'
    success_url = reverse_lazy('staff-dashboard')

from django.shortcuts import render


def payment_chart_data(request):
    today = now().date()
    last_30_days = [today - timedelta(days=i) for i in range(29, -1, -1)]  # 30 days back

    labels = []
    totals = []

    for date in last_30_days:
        total = Payment.objects.filter(paid_at__date=date).aggregate(sum=Sum('amount'))['sum'] or 0
        labels.append(date.strftime('%b %d'))  # e.g. May 29
        totals.append(float(total))

    return JsonResponse({
        'labels': labels,
        'totals': totals
    })
    
def total_sales_api(request):
    total_sales = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    return JsonResponse({'total_sales': float(total_sales)})

def guest_table_partial(request):
    guests = Guest.objects.all()[:5]
    return render(request, 'admin_lte/partials/guest_table.html', {'guests': guests})


from django.http import HttpResponse
import csv

from core.models import Room, Guest, Reservation, Payment, Staff

# Export Rooms
def export_rooms_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rooms.csv"'
    writer = csv.writer(response)
    writer.writerow(['Number', 'Type', 'Price', 'Status'])
    for room in Room.objects.all():
        writer.writerow([room.number, room.room_type, room.price, room.status])
    return response

# Export Guests
def export_guests_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guests.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Phone', ])
    for guest in Guest.objects.all():
        writer.writerow([guest.name, guest.email, guest.phone])
    return response

# Export Reservations
def export_reservations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reservations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Guest', 'Room', 'Check-In', 'Check-Out'])
    for r in Reservation.objects.all():
        writer.writerow([r.guest.name, r.room.number, r.check_in, r.check_out])
    return response

# Export Payments
def export_payments_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'
    writer = csv.writer(response)
    writer.writerow(['Reservation', 'Amount',])
    for p in Payment.objects.all():
        writer.writerow([str(p.reservation), p.amount,])
    return response

# Export Staff
def export_staff_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="staff.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Role', 'Hired Date'])
    for s in Staff.objects.all():
        writer.writerow([s.name, s.role, s.hired_date])
    return response



class CleaningListView(ListView):
    model = Cleaning
    template_name = 'admin_lte/cleaning/list.html'
    context_object_name = 'cleanings'

class CleaningCreateView(CreateView):
    model = Cleaning
    form_class = CleaningForm
    template_name = 'admin_lte/cleaning/form.html'
    success_url = reverse_lazy('cleaning-list')

class CleaningUpdateView(UpdateView):
    model = Cleaning
    form_class = CleaningForm
    template_name = 'admin_lte/cleaning/form.html'
    success_url = reverse_lazy('cleaning-list')

class CleaningDeleteView(DeleteView):
    model = Cleaning
    template_name = 'admin_lte/cleaning/confirm_delete.html'
    success_url = reverse_lazy('cleaning-list')


from core.models import WebsiteUser

def website_users_view(request):
    users = WebsiteUser.objects.all()
    return render(request, 'admin_lte/website_users/list.html', {'users': users})

def user_logout(request):
    request.session.flush()  # Clears all session data
    return redirect('user-login')  # or redirect to 'home'

class ProductListView(ListView):
    model = Product
    template_name = 'admin_lte/shop/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_lte/shop/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'admin_lte/shop/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'admin_lte/shop/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

# Orders
class ProductOrderListView(ListView):
    model = ProductOrder
    template_name = 'admin_lte/shop/order_list.html'
    context_object_name = 'orders'

class ProductOrderCreateView(CreateView):
    model = ProductOrder
    form_class = ProductOrderForm
    template_name = 'admin_lte/shop/order_form.html'
    success_url = reverse_lazy('order-list')
    
class ProductOrderUpdateView(UpdateView):
    model = ProductOrder
    form_class = ProductOrderForm
    template_name = 'admin_lte/shop/order_form.html'
    success_url = reverse_lazy('order-list')
    
class ProductOrderDeleteView(DeleteView):
    model = ProductOrder
    template_name = 'admin_lte/shop/order_confirm_delete.html'
    success_url = reverse_lazy('order-list')
    
def admin_dashboard_view(request):
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='available').count()
    total_guests = Guest.objects.count()
    total_reservations = Reservation.objects.count()
    total_payments = Payment.objects.count()
    staff_count = Staff.objects.count()
    recent_reservations = Reservation.objects.order_by('-created_at')[:5]
    total_receivables = Invoice.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_guests': total_guests,
        'total_reservations': total_reservations,
        'total_payments': total_payments,
        'staff_count': staff_count,
        'recent_reservations': recent_reservations,
        'total_receivables': total_receivables,
    }
    
    return render(request, 'admin_lte/dashboard.html', context)

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'admin_lte/invoices/list.html'
    context_object_name = 'invoices'

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'admin_lte/invoices/detail.html'
    context_object_name = 'invoice'
    
class InvoiceDeleteView(DeleteView):
    model = Invoice
    template_name = 'admin_lte/invoices/confirm_delete.html'
    success_url = reverse_lazy('invoice-dashboard')
    

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percent', 'is_active']

class CouponListView(ListView):
    model = Coupon
    template_name = 'admin_lte/coupons/list.html'
    context_object_name = 'coupons'

class CouponCreateView(CreateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'admin_lte/coupons/form.html'
    success_url = reverse_lazy('coupon-dashboard')

class CouponUpdateView(UpdateView):
    model = Coupon
    form_class = CouponForm
    template_name = 'admin_lte/coupons/form.html'
    success_url = reverse_lazy('coupon-dashboard')

class CouponDeleteView(DeleteView):
    model = Coupon
    template_name = 'admin_lte/coupons/confirm_delete.html'
    success_url = reverse_lazy('coupon-dashboard')
    
    
from core.models import ContactMessage

def contact_message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_lte/contact_messages/list.html', {'messages': messages})

def destination_dashboard(request):
    destinations = Destination.objects.all()
    return render(request, 'admin_lte/destinations/list.html', {'destinations': destinations})

# Add view
def add_destination(request):
    form = DestinationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('destination-dashboard')
    return render(request, 'admin_lte/destinations/form.html', {'form': form, 'action': 'Add'})

# Edit view
def edit_destination(request, pk):
    dest = get_object_or_404(Destination, pk=pk)
    form = DestinationForm(request.POST or None, request.FILES or None, instance=dest)
    if form.is_valid():
        form.save()
        return redirect('destination-dashboard')
    return render(request, 'admin_lte/destinations/form.html', {'form': form, 'action': 'Edit'})

# Delete view
def delete_destination(request, pk):
    dest = get_object_or_404(Destination, pk=pk)
    dest.delete()
    return redirect('destination-dashboard')


def maintenance_list(request):
    logs = MaintenanceRequest.objects.all()
    return render(request, 'admin_lte/maintenance/list.html', {'logs': logs})

def maintenance_add(request):
    form = MaintenanceRequestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('maintenance-list')
    return render(request, 'admin_lte/maintenance/form.html', {'form': form, 'action': 'Add'})

def maintenance_edit(request, pk):
    entry = get_object_or_404(MaintenanceRequest, pk=pk)
    form = MaintenanceRequestForm(request.POST or None, instance=entry)
    if form.is_valid():
        form.save()
        return redirect('maintenance-list')
    return render(request, 'admin_lte/maintenance/form.html', {'form': form, 'action': 'Edit'})

def maintenance_delete(request, pk):
    MaintenanceRequest.objects.filter(id=pk).delete()
    return redirect('maintenance-list')

    
class ConfirmedOrderListView(ListView):
    model = ConfirmedProductOrder
    template_name = 'admin_lte/confirmed_orders/list.html'
    context_object_name = 'orders'

class ConfirmedOrderCreateView(CreateView):
    model = ConfirmedProductOrder
    fields = ['user', 'product', 'quantity', 'total_price']
    template_name = 'admin_lte/confirmed_orders/form.html'
    success_url = reverse_lazy('confirmed-orders')

class ConfirmedOrderUpdateView(UpdateView):
    model = ConfirmedProductOrder
    fields = ['user', 'product', 'quantity', 'total_price']
    template_name = 'admin_lte/confirmed_orders/form.html'
    success_url = reverse_lazy('confirmed-orders')

class ConfirmedOrderDeleteView(DeleteView):
    model = ConfirmedProductOrder
    template_name = 'admin_lte/confirmed_orders/delete_confirm.html'
    success_url = reverse_lazy('confirmed-orders')
    
    
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.models import Feedback

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'admin_lte/feedback/list.html'
    context_object_name = 'feedbacks'

class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ['guest', 'room', 'rating', 'comment']
    template_name = 'admin_lte/feedback/form.html'
    success_url = reverse_lazy('feedback-list')

class FeedbackUpdateView(UpdateView):
    model = Feedback
    fields = ['user', 'room', 'rating', 'comment']
    template_name = 'admin_lte/feedback/form.html'
    success_url = reverse_lazy('feedback-list')

class FeedbackDeleteView(DeleteView):
    model = Feedback
    template_name = 'admin_lte/feedback/delete_confirm.html'
    success_url = reverse_lazy('feedback-list')


from django.shortcuts import redirect
from django.views.generic import CreateView
from core.models import Feedback, WebsiteUser
from .forms import FeedbackForm
from django.urls import reverse_lazy

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'admin_lte/feedback/form.html'
    success_url = reverse_lazy('feedback-list')  # Or redirect to room or thank-you page

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')  # Replace with your custom login view name
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room_id')
        if room_id:
            initial['room'] = room_id
        return initial

    def form_valid(self, form):
        user_id = self.request.session.get('user_id')
        website_user = WebsiteUser.objects.get(id=user_id)
        form.instance.user = website_user
        return super().form_valid(form)

from django.shortcuts import render, redirect, get_object_or_404
from core.models import Room, Feedback, WebsiteUser
from .forms import FeedbackForm

def submit_review(request, room_id):
    # Custom auth check
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  # custom login route

    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(WebsiteUser, id=user_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = user
            feedback.room = room
            feedback.save()
            return redirect('room_page')  # or a thank-you page
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {
        'form': form,
        'room': room
    })
    
from django.views.generic import ListView
from core.models import OccupancyRateSnapshot

class OccupancyRateSnapshotListView(ListView):
    model = OccupancyRateSnapshot
    template_name = 'admin_lte/occupancy/list.html'
    context_object_name = 'snapshots'
    
class OccupancyRateSnapshotDeleteView(DeleteView):
    model = OccupancyRateSnapshot
    template_name = 'admin_lte/occupancy/delete_confirm.html'
    success_url = reverse_lazy('occupancy-snapshot-list')

from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from core.models import Room, OccupancyRateSnapshot

def generate_occupancy_snapshot(request):
    today = timezone.now().date()

    # Prevent duplicate snapshot
    if OccupancyRateSnapshot.objects.filter(date=today).exists():
        messages.warning(request, "Snapshot for today already exists.")
        return redirect('occupancy-snapshot-list')

    occupied = Room.objects.filter(status='occupied').count()
    available = Room.objects.filter(status='available').count()
    maintenance = Room.objects.filter(status='maintenance').count()

    total = occupied + available + maintenance
    rate = round((occupied / total) * 100, 2) if total else 0

    OccupancyRateSnapshot.objects.create(
        date=today,
        occupied_rooms=occupied,
        available_rooms=available,
        maintenance_rooms=maintenance,
        occupancy_rate=rate
    )

    messages.success(request, "Occupancy snapshot generated for today.")
    return redirect('occupancy-snapshot-list')

from django.http import JsonResponse
from core.models import OccupancyRateSnapshot

def occupancy_chart_data(request):
    today = timezone.now().date()
    try:
        snapshot = OccupancyRateSnapshot.objects.get(date=today)
        return JsonResponse({
            'labels': ['Occupied', 'Available', 'Maintenance'],
            'values': [
                snapshot.occupied_rooms,
                snapshot.available_rooms,
                snapshot.maintenance_rooms
            ]
        })
    except OccupancyRateSnapshot.DoesNotExist:
        return JsonResponse({
            'labels': [],
            'values': []
        })
        
        ## predict model##
        
import os
import joblib
import numpy as np
from django.shortcuts import render
from .forms import GuestClusterForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../models/ml')
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler_guest.joblib'))
pca = joblib.load(os.path.join(MODEL_DIR, 'pca_guest.joblib'))
kmeans = joblib.load(os.path.join(MODEL_DIR, 'kmeans_guest_model.joblib'))

CSV_PATH = os.path.join(MODEL_DIR, 'clustered_guests_usd.csv')

USD_TO_IDR = 15000

def predict_guest_cluster(request):
    result = None
    profile_summary = None

    if request.method == 'POST':
        form = GuestClusterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # === Manual Encoding ===
            room_map = {
                "standard": 0,
                "deluxe": 1,
                "suite": 2,
                "family": 3,
                "executive": 4,
                "presidential": 5
            }

            pay_map = {"Cash": 0, "Credit Card": 1, "Transfer": 2, "E-Wallet": 3}

            # === Convert USD to IDR before model input ===
            features = [
                data['age'],
                data['visit_count'],
                data['avg_nights'],
                data['spent_room'] * USD_TO_IDR,
                data['spent_addon'] * USD_TO_IDR,
                room_map[data['room_type']],
                pay_map[data['payment_method']],
                data['rating'],
            ]

            # === Predict cluster ===
            scaled = scaler.transform([features])
            reduced = pca.transform(scaled)
            cluster = int(kmeans.predict(reduced)[0])
            result = f"Predicted Cluster: {cluster}"

            # === Load cluster tags from summary (session) ===
            try:
                summary_json = request.session.get("guest_cluster_summary")
                if summary_json:
                    import io
                    import pandas as pd
                    cluster_summary = pd.read_json(io.StringIO(summary_json))
                    profile_row = cluster_summary[cluster_summary["Cluster"] == cluster].iloc[0]
                    profile_summary = profile_row["Tags"]
                else:
                    profile_summary = "⚠️ Cluster tag info not found."
            except Exception as e:
                print("Tag loading error:", e)
                profile_summary = "⚠️ Error while retrieving cluster profile."

    else:
        form = GuestClusterForm()

    return render(request, 'admin_lte/guest_cluster/form.html', {
        'form': form,
        'result': result,
        'profile_summary': profile_summary
    })


def guest_cluster_results(request):
    df = pd.read_csv(CSV_PATH)

    # Summarize each cluster
    summary = (
    df.groupby('Cluster')
    .agg({
        'Age': 'mean',
        'Visit Count': 'mean',
        'Avg Nights per Stay': 'mean',
        'Room_Spend': 'mean',
        'Addon_Spend': 'mean',
        'Rating Given': 'mean',
        'Guest ID': 'count'
    })
    .rename(columns={
        'Age': 'Avg_Age',
        'Visit Count': 'Visit_Count',
        'Avg Nights per Stay': 'Avg_Nights',
        'Room_Spend': 'Room_Spend',
        'Addon_Spend': 'Addon_Spend',
        'Rating Given': 'Rating',
        'Guest ID': 'Guest_Count'
    })
    .round(2)
    .reset_index()
)
    color_map = {
    0: '#1f77b4',  # blue
    1: '#ff7f0e',  # orange
    2: '#2ca02c',  # green
    3: '#d62728',  # red
}

    charts = {
        'guest_count': px.bar(
            summary, x='Cluster', y='Guest_Count', text='Guest_Count',
            title='Number of Guests per Cluster',
            color='Cluster', color_discrete_map=color_map
        ).to_html(full_html=False),

        'room_spend': px.bar(
            summary, x='Cluster', y='Room_Spend', text='Room_Spend',
            title='Average Room Spend',
            color='Cluster', color_discrete_map=color_map
        ).to_html(full_html=False),

        'addon_spend': px.bar(
            summary, x='Cluster', y='Addon_Spend', text='Addon_Spend',
            title='Average Add-on Spend',
            color='Cluster', color_discrete_map=color_map
        ).to_html(full_html=False),

        'rating': px.bar(
            summary, x='Cluster', y='Rating', text='Rating',
            title='Average Rating per Cluster',
            color='Cluster', color_discrete_map=color_map
        ).to_html(full_html=False),

        'nights': px.bar(
            summary, x='Cluster', y='Avg_Nights', text='Avg_Nights',
            title='Average Nights per Stay',
            color='Cluster', color_discrete_map=color_map
        ).to_html(full_html=False),
}
    def tag_cluster(row):
        tags = []

        if row['Room_Spend'] >= 520:
            tags.append("Luxury Guest")
        elif row['Room_Spend'] <= 150:
            tags.append("Budget Guest")
        else:
            tags.append("Midrange Guest")

        if row['Visit_Count'] >= 3:
            tags.append("Frequent Visitor")
        elif row['Visit_Count'] <= 2:
            tags.append("Infrequent")

        if row['Addon_Spend'] >= 150:
            tags.append("High Extras")
        elif row['Addon_Spend'] <= 50:
            tags.append("Minimal Add-Ons")

        if row['Rating'] >= 4.2:
            tags.append("Happy Guest")
        elif row['Rating'] <= 3.5:
            tags.append("Low Satisfaction")

        return ", ".join(tags)

    summary['Tags'] = summary.apply(tag_cluster, axis=1)
    request.session['guest_cluster_summary'] = summary.to_json()




    # Create 2D scatterplot using PC1 and PC2 if present
    if 'PC1' in df.columns and 'PC2' in df.columns:
        fig = px.scatter(
            df, x="PC1", y="PC2", color=df["Cluster"].astype(str),
            hover_data=["Age", "Total Spent (Room)", "Visit Count"],
            title="Guest Clusters (PCA Projection)"
        )
        graph_html = fig.to_html(full_html=False)
    else:
        graph_html = None
        
        

    return render(request, 'admin_lte/guest_cluster/results.html', {
    'summary': summary.to_dict(orient='records'),
    'graph_html': graph_html,
    'charts': charts
})

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from core.models import RoomServiceRequest
from core.forms import RoomServiceRequestForm

class RoomServiceRequestListView(ListView):
    model = RoomServiceRequest
    template_name = 'admin_lte/room_service/list.html'
    context_object_name = 'requests'

class RoomServiceRequestCreateView(CreateView):
    model = RoomServiceRequest
    form_class = RoomServiceRequestForm
    template_name = 'admin_lte/room_service/form.html'
    success_url = reverse_lazy('roomservice-list')

class RoomServiceRequestUpdateView(UpdateView):
    model = RoomServiceRequest
    form_class = RoomServiceRequestForm
    template_name = 'admin_lte/room_service/form.html'
    success_url = reverse_lazy('roomservice-list')

class RoomServiceRequestDeleteView(DeleteView):
    model = RoomServiceRequest
    template_name = 'admin_lte/room_service/delete_confirm.html'
    success_url = reverse_lazy('roomservice-list')


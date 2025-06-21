from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Room, Guest, Reservation, Payment, Staff
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from core.models import Room,Dashboard, Invoice
from .forms import ReservationForm
from .forms import WebsiteUserRegisterForm
from django.contrib.auth.hashers import check_password
from .models import WebsiteUser, ContactMessage
from .forms import WebsiteUserLoginForm, WebsiteUserRegisterForm
from core.models import Product
from django.utils import timezone
from decimal import Decimal
from core.models import Coupon, ConfirmedProductOrder, RoomType
from django.db.models import Q
from .forms import ContactMessageForm
from .models import Destination



class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room_types"] = dict(Room.ROOM_TYPES)
        context["destinations"] = Destination.objects.filter(featured=True)[:3]  # Top 3 featured
        return context
    
def about_page(request):
    return render(request, "about.html")




def destination(request):
    return render(request, "destination.html")

def public_room_list(request):
    room_types = dict(Room.ROOM_TYPES)

    # Define specs per room type
    room_specs = {
        'standard': {'size': '24 sqm', 'bed': '1 Bed', 'bath': '1 Bathroom'},
        'deluxe': {'size': '32 sqm', 'bed': '2 Beds', 'bath': '1 Bathroom'},
        'suite': {'size': '45 sqm', 'bed': '1 King Bed', 'bath': '2 Bathrooms'},
        'family': {'size': '50 sqm', 'bed': '2 Queen Beds', 'bath': '2 Bathrooms'},
        'executive': {'size': '60 sqm', 'bed': '1 King Bed + 1 Sofa Bed', 'bath': '2 Bathrooms'},
        'presidential': {'size': '80 sqm', 'bed': '2 King Beds', 'bath': '3 Bathrooms'},
    }

    grouped_rooms = []

    for key, label in room_types.items():
        all_rooms = Room.objects.filter(room_type=key)
        available_rooms = all_rooms.filter(status='available')

        grouped_rooms.append({
            'type_key': key,
            'type_label': label,
            'price': Room.FIXED_PRICES.get(key, 0),
            'available': available_rooms.exists(),
            'specs': room_specs.get(key)
        })

    return render(request, 'room.html', {'grouped_rooms': grouped_rooms})

from .models import Room, Guest, Reservation
from .forms import GuestForm, ReservationForm
from django.shortcuts import render, redirect

def book_room(request, room_type):
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    try:
        checkin_date = datetime.strptime(checkin, "%m/%d/%Y") if checkin else None
        checkout_date = datetime.strptime(checkout, "%m/%d/%Y") if checkout else None
    except ValueError:
        checkin_date = checkout_date = None

    # Step 1: Find an available room of this type that has no conflicting reservation
    available_room = None
    candidate_rooms = Room.objects.filter(room_type=room_type, status='available')

    for room in candidate_rooms:
        if checkin_date and checkout_date:
            has_conflict = Reservation.objects.filter(
                room=room,
                check_in__lt=checkout_date,
                check_out__gt=checkin_date
            ).exists()
            if not has_conflict:
                available_room = room
                break
        else:
            available_room = room
            break

    # Step 2: If no room is available, show fallback page
    if not available_room:
        return render(request, 'no_rooms_available.html', {'room_type': room_type})

    # Step 3: Prepare static room info preview (for UI)
    room_info = {
        'room_type': room_type,
        'price': available_room.price,
        'images': [
            'images/shop/shop-single/1.jpg',
            'images/shop/shop-single/2.jpg',
            'images/shop/shop-single/3.jpg',
        ],
        'description': f"A comfortable and stylish {room_type.title()} room ideal for your stay.",
        'features': ["Free Wi-Fi", "Air Conditioning", "Private Bathroom", "Room Service"]
    }

    # Step 4: Handle reservation form
    if request.method == 'POST':
        guest_form = GuestForm(request.POST)
        res_form = ReservationForm(request.POST)
        if guest_form.is_valid() and res_form.is_valid():
            guest = guest_form.save()
            reservation = res_form.save(commit=False)
            reservation.guest = guest
            reservation.room = available_room

            # Link to WebsiteUser if logged in
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    reservation.user = WebsiteUser.objects.get(id=user_id)
                except WebsiteUser.DoesNotExist:
                    pass

            reservation.save()

            # Mark room as occupied
            available_room.status = 'occupied'
            available_room.save()

            # Optional: update dashboard for this user
            if reservation.user:
                dashboard, _ = Dashboard.objects.get_or_create(user=reservation.user)
                dashboard.last_booking = timezone.now()
                dashboard.total_bookings += 1
                dashboard.save()

            return redirect('room-list')  # or a confirmation page

    else:
        guest_form = GuestForm()
        res_form = ReservationForm()

    return render(request, 'book_room.html', {
        'guest_form': guest_form,
        'res_form': res_form,
        'room': room_info,
        'room_obj': available_room,
        'checkin': checkin,
        'checkout': checkout,
    })

from django.contrib.auth.hashers import check_password
from .models import WebsiteUser

def user_register(request):
    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        form = WebsiteUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = WebsiteUserRegisterForm()
    return render(request, 'user_register.html', {'form': form})

def user_login(request):
    if request.session.get('user_id'):
        return redirect('home')
    if request.method == 'POST':
        form = WebsiteUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = WebsiteUser.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('home')
                else:
                    form.add_error(None, "Invalid password.")
            except WebsiteUser.DoesNotExist:
                form.add_error(None, "User not found.")
    else:
        form = WebsiteUserLoginForm()
    return render(request, 'user_login.html', {'form': form})

def user_logout(request):
    request.session.flush()  # Clears all session data
    return redirect('user-login')  # or redirect to 'home'

def checkout_page(request):
    return render(request, "checkout.html")

def shop_page(request):
    products = Product.objects.filter(tersedia=True)
    return render(request, 'shop.html', {'products': products})

def get_logged_in_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return WebsiteUser.objects.get(id=user_id)
        except WebsiteUser.DoesNotExist:
            return None
    return None

class PublicReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'templates/admin_lte/reservations/form.html'  # Change this to your actual site path
    success_url = reverse_lazy('reservation-success')

    def form_valid(self, form):
        form.instance.user = get_logged_in_user(self.request)
        return super().form_valid(form)
    
def my_reservations(request):
    user = get_logged_in_user(request)
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'my_reservations.html', {'reservations': reservations})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from core.models import Product, ProductOrder, WebsiteUser, Reservation

def order_product(request, product_id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "You must be logged in to place an order.")
            return redirect('shop')

        try:
            user = WebsiteUser.objects.get(id=user_id)
        except WebsiteUser.DoesNotExist:
            messages.error(request, "Invalid user session.")
            return redirect('shop')

        product = get_object_or_404(Product, id=product_id)
        jumlah = int(request.POST.get('jumlah', 1)) 

        order = ProductOrder.objects.create(
            user=user,
            produk=product,
            jumlah=jumlah
        )

        messages.success(request, f"Ordered {jumlah} × {product.nama_produk}.")
        return redirect('shop')
    
def cart_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user-login')

    user = WebsiteUser.objects.get(id=user_id)
    product_orders = ProductOrder.objects.filter(user=user)
    reservations = Reservation.objects.filter(user=user)

    # Total for product orders
    total_product_price = sum(order.total_harga for order in product_orders)

    # Total for room reservations (price per night × nights)
    total_room_price = 0
    for res in reservations:
        nights = (res.check_out - res.check_in).days
        total_room_price += res.room.price * Decimal(nights)

    grand_total = total_product_price + total_room_price

    return render(request, 'cart.html', {
        'product_orders': product_orders,
        'reservations': reservations,
        'total_product_price': total_product_price,
        'total_room_price': total_room_price,
        'grand_total': grand_total
    })
    
def delete_product_order(request, order_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user-login')

    order = get_object_or_404(ProductOrder, id=order_id, user_id=user_id)
    order.delete()
    return redirect('cart')

def update_cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user-login')

    if request.method == 'POST':
        orders = ProductOrder.objects.filter(user_id=user_id)
        for order in orders:
            qty = request.POST.get(f'jumlah_{order.id}')
            if qty:
                try:
                    new_qty = int(qty)
                    if new_qty > 0 and new_qty != order.jumlah:
                        order.jumlah = new_qty
                        order.save()
                except ValueError:
                    continue

    return redirect('cart')

def checkout_page(request):
    print("📩 checkout_page view loaded")

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user-login')

    user = WebsiteUser.objects.get(id=user_id)
    orders = ProductOrder.objects.filter(user=user)
    reservations = Reservation.objects.filter(user=user)

    product_total = sum(order.total_harga for order in orders)
    room_total = sum(res.room.price for res in reservations)
    total_price = product_total + room_total

    discount = 0
    applied_coupon = None

    # ✅ Check for existing coupon from session
    if 'applied_coupon_code' in request.session:
        try:
            coupon = Coupon.objects.get(code=request.session['applied_coupon_code'], is_active=True)
            discount = total_price * (Decimal(coupon.discount_percent) / Decimal('100'))
            applied_coupon = coupon
            total_price -= discount
        except Coupon.DoesNotExist:
            discount = 0
            applied_coupon = None
            del request.session['applied_coupon_code']  # Clean up invalid code

    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')

        # 🔹 Coupon submission
        if form_type == 'coupon':
            print("🧪 Coupon form submitted.")
            print("POST data:", request.POST.dict())

            code = request.POST.get('coupon_code', '').strip().upper()
            try:
                coupon = Coupon.objects.get(Q(code__iexact=code), is_active=True)
                request.session['applied_coupon_code'] = coupon.code
                print(f"✅ Coupon '{coupon.code}' saved to session.")
            except Coupon.DoesNotExist:
                if 'applied_coupon_code' in request.session:
                    del request.session['applied_coupon_code']
                print("❌ Invalid or inactive coupon code")

            return redirect('checkout')

        # 🔹 Invoice submission
        else:
            fname = request.POST.get('fname', '').strip()
            lname = request.POST.get('lname', '').strip()
            billing_name = f"{fname} {lname}".strip()
            billing_email = request.POST.get('email', '').strip()
            billing_address = request.POST.get('address', '').strip()
            payment_method = request.POST.get('payment', 'unknown').strip()
            card_number = request.POST.get('card', '').strip()
            last_digits = card_number[-4:] if payment_method == 'card' and card_number.isdigit() else None

            print("✅ Invoice submission received")
            print("Calculated total (after discount):", total_price)

            invoice = Invoice.objects.create(
                user=user,
                billing_name=billing_name,
                billing_email=billing_email,
                billing_address=billing_address,
                payment_method=payment_method,
                card_last_digits=last_digits,
                total_amount=total_price
            )
            print("✅ Invoice saved:", invoice)

            # ✅ Convert ProductOrder into ConfirmedProductOrder
            for order in orders:
                print("➡️ Creating confirmed order for:", order.produk.nama_produk)
                ConfirmedProductOrder.objects.create(
                    user=user,
                    product=order.produk,
                    quantity=order.jumlah,
                    total_price=order.total_harga
                )

            # ✅ Now clear the cart
            orders.delete()

            if 'applied_coupon_code' in request.session:
                del request.session['applied_coupon_code']

            return redirect('user-invoice', pk=invoice.pk)


    return render(request, 'checkout.html', {
        'orders': orders,
        'reservations': reservations,
        'total_price': total_price,
        'discount': discount,
        'applied_coupon': applied_coupon,
    })

def contact_view(request):
    success = False
    error = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        note = request.POST.get('note')  # "note" is the textarea

        if name and email and phone and subject and note:
            message = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=note
            )

            user_id = request.session.get('user_id')
            if user_id:
                try:
                    message.user = WebsiteUser.objects.get(id=user_id)
                except WebsiteUser.DoesNotExist:
                    pass

            message.save()
            success = True
        else:
            error = True

    return render(request, 'contact.html', {
        'success': success,
        'error': error
    })
    
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination.html', {'destinations': destinations})


def login_register_view(request):
    login_form = WebsiteUserLoginForm()
    register_form = WebsiteUserRegisterForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            login_form = WebsiteUserLoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                try:
                    user = WebsiteUser.objects.get(username=username)
                    if check_password(password, user.password):
                        request.session['user_id'] = user.id
                        request.session['username'] = user.username
                        return redirect('home')
                    else:
                        login_form.add_error(None, "Invalid password.")
                except WebsiteUser.DoesNotExist:
                    login_form.add_error(None, "User not found.")

        elif form_type == 'register':
            register_form = WebsiteUserRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                return redirect('user-login')  # or 'home'

    return render(request, 'user_auth/login_register.html', {
        'login_form': login_form,
        'register_form': register_form,
    })

from django.shortcuts import render
from core.models import Room, Reservation
from datetime import datetime

def room_search(request):
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    room_type_code = request.GET.get('room_type')
    available_rooms = []

    # ✅ Get room types from model choices
    room_types = dict(Room.ROOM_TYPES)

    if checkin and checkout and room_type_code:
        try:
            checkin_date = datetime.strptime(checkin, "%m/%d/%Y")
            checkout_date = datetime.strptime(checkout, "%m/%d/%Y")

            # ✅ Filter only rooms that are available and match room type
            rooms = Room.objects.filter(room_type=room_type_code, status='available')

            # ✅ Remove any rooms with a reservation conflict
            for room in rooms:
                has_conflict = Reservation.objects.filter(
                    room=room,
                    check_in__lt=checkout_date,
                    check_out__gt=checkin_date
                ).exists()

                if not has_conflict:
                    available_rooms.append(room)

        except ValueError:
            # Invalid date format
            pass

    return render(request, "room_search_results.html", {
        "room_types": room_types,
        "available_rooms": available_rooms,
        "checkin": checkin,
        "checkout": checkout,
        "selected_room_type": room_type_code,
    })
    
# views.py
def user_invoice_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if invoice.user.id != request.session.get('user_id'):
        return redirect('user-login')

    return render(request, 'invoice_receipt.html', {
        'invoice': invoice
    })
    

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    # Optional: protect against other users
    if invoice.user.id != request.session.get('user_id'):
        return redirect('user-login')

    template_path = 'invoice_pdf_template.html'
    context = {'invoice': invoice}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors while generating the PDF <pre>' + html + '</pre>')

    return response

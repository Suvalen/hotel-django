from django.urls import path
from .views import HomePageView
from . import views
from core.views import about_page, destination, checkout_page, book_room, delete_product_order
from .views import public_room_list
from .views import user_login, user_register
from .views import user_logout, cart_view
from .views import shop_page, my_reservations, order_product, update_cart, contact_view
from django.conf import settings
from django.conf.urls.static import static
from core.views import destination_list
from .views import login_register_view, user_invoice_view, generate_invoice_pdf


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', about_page, name='about'),
    
    path('room/', public_room_list, name='room_page'),
    path('checkout/', checkout_page, name='check_out'),
    path('rooms/', public_room_list, name='room-list'),
    path('book/<str:room_type>/', book_room, name='book-room'),
    path('user-login/', user_login, name='user-login'),
    path('user-register/', user_register, name='user-register'),
    path('user-logout/', user_logout, name='user-logout'),
    path('shop/', shop_page, name='shop'),
    path('shop/order/<int:product_id>/', order_product, name='order-product'),
    path('my-reservations/', my_reservations, name='my-reservations'),
    path('cart/', cart_view, name='cart'),
    path('cart/delete/<int:order_id>/', delete_product_order, name='delete-order'),
    path('cart/update/', update_cart, name='update-cart'),
    path('checkout/', checkout_page, name='checkout'),
    path('contact/', contact_view, name='contact'),
    path('destinations/', destination_list, name='destination-list'),
    path('auth/', login_register_view, name='user-login'),
    path('register/', login_register_view, name='user-register'),  # same view handles both
    path('search/', views.room_search, name='room-search'),
    path('invoice/receipt/<int:pk>/', user_invoice_view, name='user-invoice'),
    path('invoice/<int:pk>/download/', generate_invoice_pdf, name='invoice-download'),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
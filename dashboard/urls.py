from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import dashboard_home, admin_register
from django.contrib.auth import views as auth_views
from .views import payment_chart_data
from .views import guest_table_partial
from .views import (
    export_rooms_csv, export_guests_csv, export_reservations_csv,
    export_payments_csv, export_staff_csv
)
from .views import (
    CleaningListView, CleaningCreateView,
    CleaningUpdateView, CleaningDeleteView
)
from .views import website_users_view
from .views import (
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductOrderListView, ProductOrderCreateView, ProductOrderDeleteView, ProductOrderUpdateView
)
from .views import admin_dashboard_view
from dashboard.views import InvoiceListView, InvoiceDetailView
from .views import InvoiceDeleteView

from .views import (
    CouponListView, CouponCreateView, CouponUpdateView, CouponDeleteView
)
from dashboard.views import contact_message_list
from dashboard.views import destination_dashboard, add_destination, edit_destination, delete_destination
from dashboard.views import maintenance_list, maintenance_edit, maintenance_add, maintenance_delete

from django.urls import path
from .views import (
    ConfirmedOrderListView, ConfirmedOrderCreateView,
    ConfirmedOrderUpdateView, ConfirmedOrderDeleteView,
)
from .views import FeedbackListView, FeedbackCreateView, FeedbackUpdateView, FeedbackDeleteView, submit_review
from .views import OccupancyRateSnapshotListView, generate_occupancy_snapshot, OccupancyRateSnapshotDeleteView, occupancy_chart_data
from .views import predict_guest_cluster, guest_cluster_results

from .views import (
    RoomServiceRequestListView, RoomServiceRequestCreateView,
    RoomServiceRequestUpdateView, RoomServiceRequestDeleteView,)


urlpatterns = [
 
    path('register/', admin_register, name='admin-register'),
    path('login/', auth_views.LoginView.as_view(template_name='admin_lte/login.html'), name='admin-login'),
    path('rooms/', views.RoomListView.as_view(), name='room-dashboard'),
    path('rooms/add/', views.RoomCreateView.as_view(), name='room-add'),
    path('rooms/<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room-edit'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room-delete'),
    path('guests/', views.GuestListView.as_view(), name='guest-dashboard'),
    path('guests/add/', views.GuestCreateView.as_view(), name='guest-add'),
    path('guests/<int:pk>/edit/', views.GuestUpdateView.as_view(), name='guest-edit'),
    path('guests/<int:pk>/delete/', views.GuestDeleteView.as_view(), name='guest-delete'),
    path('reservations/', views.ReservationListView.as_view(), name='reservation-dashboard'),
    path('reservations/add/', views.ReservationCreateView.as_view(), name='reservation-add'),
    path('reservations/<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='reservation-edit'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation-delete'),
    path('payments/', views.PaymentListView.as_view(), name='payment-dashboard'),
    path('payments/add/', views.PaymentCreateView.as_view(), name='payment-add'),
    path('payments/<int:pk>/edit/', views.PaymentUpdateView.as_view(), name='payment-edit'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment-delete'),
    path('staff/', views.StaffListView.as_view(), name='staff-dashboard'),
    path('staff/add/', views.StaffCreateView.as_view(), name='staff-add'),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name='staff-edit'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff-delete'),
    path('payments/chart-data/', views.payment_chart_data, name='payment-chart-data'),
    path('api/total-sales/', views.total_sales_api, name='total-sales-api'),
    path('guest-table/', views.guest_table_partial, name='guest-table-partial'),
    path('rooms/export/', export_rooms_csv, name='export-rooms-csv'),
    path('guests/export/', export_guests_csv, name='export-guests-csv'),
    path('reservations/export/', export_reservations_csv, name='export-reservations-csv'),
    path('payments/export/', export_payments_csv, name='export-payments-csv'),
    path('staff/export/', export_staff_csv, name='export-staff-csv'),
    path('logout/', LogoutView.as_view(next_page='admin-login'), name='logout'),
    path('cleaning/', CleaningListView.as_view(), name='cleaning-list'),
    path('cleaning/add/', CleaningCreateView.as_view(), name='cleaning-add'),
    path('cleaning/<int:pk>/edit/', CleaningUpdateView.as_view(), name='cleaning-edit'),
    path('cleaning/<int:pk>/delete/', CleaningDeleteView.as_view(), name='cleaning-delete'),
    path('website-users/', website_users_view, name='website-users'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product-edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('orders/', ProductOrderListView.as_view(), name='order-list'),
    path('orders/add/', ProductOrderCreateView.as_view(), name='order-add'),
     path('orders/edit/<int:pk>/', ProductOrderUpdateView.as_view(), name='order-edit'),
    path('orders/delete/<int:pk>/', ProductOrderDeleteView.as_view(), name='order-delete'),
    path('home', admin_dashboard_view, name='dashboard'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-dashboard'),
    path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('coupons/', CouponListView.as_view(), name='coupon-dashboard'),
    path('coupons/add/', CouponCreateView.as_view(), name='coupon-add'),
    path('coupons/edit/<int:pk>/', CouponUpdateView.as_view(), name='coupon-edit'),
    path('coupons/delete/<int:pk>/', CouponDeleteView.as_view(), name='coupon-delete'),
    path('contact-messages/', contact_message_list, name='contact-messages'),
    path('destinations/', destination_dashboard, name='destination-dashboard'),
    path('destinations/add/', add_destination, name='add-destination'),
    path('destinations/edit/<int:pk>/', edit_destination, name='edit-destination'),
    path('destinations/delete/<int:pk>/', delete_destination, name='delete-destination'),
    path('maintenance/', maintenance_list, name='maintenance-list'),
    path('maintenance/add/', maintenance_add, name='maintenance-add'),
    path('maintenance/edit/<int:pk>/', maintenance_edit, name='maintenance-edit'),
    path('maintenance/delete/<int:pk>/', maintenance_delete, name='maintenance-delete'),
    path('confirmed-orders/', ConfirmedOrderListView.as_view(), name='confirmed-orders'),
    path('confirmed-orders/add/', ConfirmedOrderCreateView.as_view(), name='confirmed-order-add'),
    path('confirmed-orders/<int:pk>/edit/', ConfirmedOrderUpdateView.as_view(), name='confirmed-order-edit'),
    path('confirmed-orders/<int:pk>/delete/', ConfirmedOrderDeleteView.as_view(), name='confirmed-order-delete'),
    path('feedback/', FeedbackListView.as_view(), name='feedback-list'),
    path('feedback/create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/<int:pk>/edit/', FeedbackUpdateView.as_view(), name='feedback-edit'),
    path('feedback/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('feedback/create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('submit-review/<int:room_id>/', submit_review, name='submit-review'),
    path('occupancy/', OccupancyRateSnapshotListView.as_view(), name='occupancy-snapshot-list'),
    path('occupancy/generate/', generate_occupancy_snapshot, name='generate-occupancy-snapshot'),
    path('occupancy/delete/<int:pk>/', OccupancyRateSnapshotDeleteView.as_view(), name='delete-occupancy-snapshot'),
    path('api/occupancy-chart-data/', occupancy_chart_data, name='occupancy-chart-data'),
    path('predict-guest-cluster/', predict_guest_cluster, name='predict_guest_cluster'),
    path('guest-cluster-results/', guest_cluster_results, name='guest_cluster_results'),
    path('room-service/', RoomServiceRequestListView.as_view(), name='roomservice-list'),
    path('room-service/create/', RoomServiceRequestCreateView.as_view(), name='roomservice-create'),
    path('room-service/update/<int:pk>/', RoomServiceRequestUpdateView.as_view(), name='roomservice-update'),
    path('room-service/delete/<int:pk>/', RoomServiceRequestDeleteView.as_view(), name='roomservice-delete'),
]

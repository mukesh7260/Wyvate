
from django.contrib import admin
from django.urls import path
from authenticateapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.Register.as_view(),name="create"),
    path('login/',views.LoginApi.as_view(),name="create"),
    # path('api/cart/add/<int:product_id>/', views.CartOperationsView.as_view(), name='add-to-cart'),
    # path('api/cart/remove/<int:product_id>/', views.CartOperationsView.as_view(), name='remove-from-cart'),
    # path('api/cart/all/', views.AllCartItemsView.as_view(), name='all-cart-items'),
    # path('api/cart/item/<int:product_id>/', views.SpecificCartItemView.as_view(), name='specific-cart-item'),
    # path('payment/', views.PaymentView.as_view(), name='payment'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('get_all_cart/', views.get_all_items, name='add_to_cart'),
    path('get_spefic_items/<int:pk>', views.get_specific_items, name='add_to_cart'),
    path('delete_cart/<int:pk>', views.delete_cart, name='add_to_cart'),
    
]

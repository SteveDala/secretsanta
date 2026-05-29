from django.urls import path

from . import views

app_name = "gifting"

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path("<int:pk>/", views.WishListDetailView.as_view(),
         name='wishlist_detail'),
    path("<int:wishlist_id>/wishes/<int:pk>/",
         views.WishUpdateView.as_view(), name='wish_detail'),
    path("new_wishlist/", views.WishListCreateView.as_view(),
         name='wishlist_create'),
    path("<int:wishlist_id>/wishes/new/",
         views.WishCreateView.as_view(), name="wish_create"),
    path("<int:wishlist_id>/wishes/<int:pk>/delete/",
         views.WishDeleteView.as_view(), name="wish_delete"),
    path("<int:pk>/delete/", views.WishListDeleteView.as_view(),
         name="wishlist_delete")
]

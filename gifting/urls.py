from django.urls import path

from . import views

app_name = "gifting"

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    # eg  wishlists/
    path('wishlists/', views.UserWishLists.as_view(), name='wishlist_list'),
    # eg  wishlists/new/
    path('wishlists/new/', views.WishListCreateView.as_view(),
         name='wishlist_create'),
    # eg  wishlists/empty/
    path('wishlists/empty/', views.WishListEmptyView.as_view(),
         name='wishlist_empty'),
    # eg  wishlists/1/
    path('wishlists/<int:pk>/', views.WishListDetailView.as_view(),
         name='wishlist_detail'),
    # eg  wishlists/5/delete/
    path('wishlists/<int:pk>/delete/', views.WishListDeleteView.as_view(),
         name='wishlist_delete'),
    # eg  wishlists/3/wishes/new/
    path('wishlists/<int:wishlist_id>/wishes/new/',
         views.WishCreateView.as_view(), name='wish_create'),
    # eg  wishlists/2/wishes/4/
    path('wishlists/<int:wishlist_id>/wishes/<int:pk>/',
         views.WishUpdateView.as_view(), name='wish_detail'),
    # eg  wishlists/4/wishes/2/delete/
    path('wishlists/<int:wishlist_id>/wishes/<int:pk>/delete/',
         views.WishDeleteView.as_view(), name='wish_delete'),
    # eg  events/
    path('events/', views.EventsList.as_view(), name='event_dash'),
    # eg  events/1/
    path('events/<int:pk>/',
         views.EventDetail.as_view(), name='event_detail'),
    # eg  events/empty/
    path('events/empty/', views.EventEmpty.as_view(), name='event_empty'),
    # eg  events/1/choose-wishlist
    path('events/<int:pk>/choose-wishlist/',
         views.EventParticipantSetWishList.as_view(),
         name='event_choose_wishlist'
         )
]

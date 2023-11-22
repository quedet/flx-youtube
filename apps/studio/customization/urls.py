from django.urls import path

from apps.studio.customization import views

urlpatterns = [
    path('', views.StudioCustomizationView.as_view(), name='customization'),
    path('branding/', views.LoadCustomizationBrandingView.as_view(), name='customization-branding'),
    path('branding/picture/', views.StudioCustomizationBrandingPictureView.as_view(), name='customization-branding-picture'),
    path('branding/banner/', views.StudioCustomizationBrandingBannerView.as_view(), name='customization-branding-banner'),

    path('layout/', views.LoadCustomizationLayoutView.as_view(), name='customization-layout'),
    path('layout/trailer/', views.LoadCustomizationLayoutTrailerView.as_view(), name='customization-layout-trailer'),
    path('layout/trailer/play/<trailer_uid>/', views.LoadCustomizationLayoutTrailerPlayView.as_view(), name='customization-layout-trailer-play'),
    path('basic-info/', views.LoadCustomizationBasicInfoView.as_view(), name='customization-basic-info'),

    path('update/channel-link-order/', views.ChannelLinkOrderView.as_view(), name='update-link-order')
]

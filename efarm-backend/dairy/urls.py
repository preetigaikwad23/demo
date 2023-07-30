from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'dairy'

router = routers.DefaultRouter()
router.register(r'cows', CowViewSet, basename='cows')
router.register(r'cow-breeds', CowBreedViewSet, basename='cow-breeds')
router.register(r'milk-records', MilkViewSet, basename='milk-records')
router.register(r'lactations-records', LactationViewSet, basename='lactation-records')
router.register(r'pregnancy-records', PregnancyViewSet, basename='pregnancy-records')
router.register(r'weight-records', WeightRecordViewSet, basename='weight-records')
router.register(r'culling-records', CullingViewSet, basename='culling-records')
router.register(r'barns', BarnViewSet, basename='barn')
router.register(r'cow-pens', CowPenViewSet, basename='cow-pen')
router.register(r'cow-in-pen-movements', CowInPenMovementViewSet, basename='cow-in-pen-movement')
router.register(r'cow-in-barn-movements', CowInBarnMovementViewSet, basename='cow-in-barn-movement')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/dashboard/daily-milk-production', MilkTodayView.as_view()),
    path('admin/dashboard/milked-cows', CowsMilkedTodayView.as_view()),
    path('admin/dashboard/total-alive-cows', TotalAliveCowsView.as_view()),
    path('admin/dashboard/total-alive-male-cows', TotalAliveMaleCowsView.as_view()),
    path('admin/dashboard/total-alive-female-cows', TotalAliveFemaleCowsView.as_view()),
    path('admin/dashboard/weekly-milk-chart-data', MilkProductionWeeklyView.as_view()),
    path('admin/dashboard/pregnant-cows', PregnantCowsView.as_view()),
    path('admin/dashboard/lactating-cows', LactatingCowsView.as_view()),
]

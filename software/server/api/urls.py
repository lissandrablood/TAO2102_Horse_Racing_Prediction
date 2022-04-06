from django.urls import path, include
from .views import main, getBets, getPrediction, getHorseDetails, getRaceDate, updateRace

urlpatterns = [
    path('', main),
    path('get/bet/', getBets),
    path('get/prediction/', getPrediction),
    path('get/details/', getHorseDetails),
    path('get/race_date/', getRaceDate),
    path('update/race/', updateRace)
]
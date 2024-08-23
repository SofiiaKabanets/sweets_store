from django.urls import path
from . import views
from .views import SearchResultListView


app_name='search'

urlpatterns = [
    path('', SearchResultListView.as_view(), name='searchResult'),
]
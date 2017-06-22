from django.conf.urls import url
from haystack.views import SearchView

from . import views
from django.views.generic import RedirectView

urlpatterns = [

   # url(r'^$' , SearchView() ,name='search_views'),
   url(r'^song_id/(?P<song_num>[0-9]+)/$',views.song_id, name='song_id'),
   url(r'^search_results/$', views.get_search_results, name='search_results'),
   url(r'^$' , views.get_search_results, name='search_results'),
   url(r'^singer/$' , views.get_search_singers, name='search_singers'),
   url(r'^album/$' , views.get_search_albums, name='search_albums'),
   url(r'^lyric/$' , views.get_search_lyrics, name='search_lyrics'),
   url(r'^recognize/$' , views.get_recognize_results, name='search_voice'),
]


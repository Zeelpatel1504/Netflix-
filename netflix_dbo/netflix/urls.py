from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import register_user,add_to_watchlist,remove_from_watchlist,logout_user,tv_shows,movies,browse_by_lang
from .views import login_user,profile_list,create_profile,delete_profile,edit_profile,profile_media,media_details, statistics_dashboard
from .views import browse_by_genres,media_list_by_genre,get_episodes, genre_media_statistics, latest_media_by_genre, ranked_media_in_genre, action_drama_media
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', profile_list, name='profile_list'),
    path('profile/create/', create_profile, name='create_profile'),  # Define URL for creating a profile
    path('profile/<int:profile_id>/edit/', edit_profile, name='edit_profile'),
    path('profile/<int:profile_id>/delete/', delete_profile, name='delete_profile'),
    path('profile/<int:profile_id>/media/', profile_media, name='profile_media'),
    path('profile/<int:profile_id>/media/<int:media_id>/', media_details, name='media_details'),

    path('profile/<int:profile_id>/media/<int:media_id>/add_to_watchlist/', add_to_watchlist, name='add_to_watchlist'),
    path('profile/<int:profile_id>/media/<int:media_id>/remove_from_watchlist/', remove_from_watchlist, name='remove_from_watchlist'),

    path('profile/<int:profile_id>/tv_shows/', tv_shows, name='tv_shows'),
    path('profile/<int:profile_id>/movies/', movies, name='movies'),
    path('profile/<int:profile_id>/browse_by_lang/', browse_by_lang, name='browse_by_lang'),

    path('profile/<int:profile_id>/browse_by_genres/', browse_by_genres, name='browse_by_genres'),
    path('profile/<int:profile_id>/browse_by_genres/<int:genre_id>/', media_list_by_genre, name='media_list_by_genre'),
    path('get_episodes/', get_episodes, name='get_episodes'),
    path('profile/<int:profile_id>/genre-stats/', genre_media_statistics, name='genre_stats'),
    path('profile/<int:profile_id>/latest-media-by-genre/', latest_media_by_genre, name='latest_media_by_genre'),
    path('profile/<int:profile_id>/ranked-media/', ranked_media_in_genre, name='ranked_media'),
    # path('profile/<int:profile_id>/action-drama-media/', action_drama_media, name='action_drama_media'),
    path('profile/<int:profile_id>/statistics-dashboard/', statistics_dashboard, name='statistics_dashboard'),


    path('logout/', logout_user, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

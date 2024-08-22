
# from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm,ProfileForm,EditProfileForm
from .models import Profile, Language,Users,ProfileGenre,Genre,Media,MediaGenre,ProfileWatchlist,Season,Episode
from django.contrib.auth import  login
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Avg,Count,Window, F,Q
from django.db.models.functions import Rank
from django.http import JsonResponse
import os
from django.shortcuts import render, get_object_or_404
from django.db.models import OuterRef, Subquery, Max


#Sign up
def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        default_language = Language.objects.get_or_create(LName='English')[0]
        
        if user_form.is_valid():
            # user = user_form.save()
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']

            # Hash the password
            user = Users.objects.create(email=email, password=password,first_name=first_name,last_name=last_name)
            profile =Profile.objects.create(user=user , language = default_language, PName=f"{user.first_name}'s Profile")
            # Now add default genres to ProfileGenre
            default_genres = Genre.objects.all()[:3]  # Get the first three genres
            for genre in default_genres:
                ProfileGenre.objects.create(profile=profile, genre=genre)
            return redirect('login')  # Redirect to login page
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})

#login
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = Users.objects.get(email=email)
        if (password==user.password):
            login(request, user)
            return redirect('profile_list')   
    else:
        return render(request, 'login.html')

# profile list
def profile_list(request):
    user_id = request.user.uid
    profiles = Profile.objects.filter(user_id=user_id)

    #return render(request, 'profile_list.html', {'profiles': profiles})
    show_create_button = profiles.count() < 4  # Check if the user has less than 4 profiles
    return render(request, 'profile_list.html', {'profiles': profiles, 'show_create_button': show_create_button})

#create profile
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)


        if form.is_valid():
            # Create a new profile object with the form data
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the profile with the logged-in user
            profile.save()
             # Save selected genres in ProfileGenre table
            for genre in form.cleaned_data['genres']:
                ProfileGenre.objects.create(profile=profile, genre=genre)

            return redirect('profile_list')  # Redirect back to the profile list page
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})

#edit profile
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, PID=profile_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_list')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form,'profile': profile})

#delete profile
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, PID=profile_id)
    if request.method == 'POST':
        profile.delete()
        return redirect('profile_list')
    # return redirect('profile_list')
    return render(request, 'confirm_delete_profile.html', {'profile': profile})

#profile watchlist

def profile_media(request, profile_id):
    # Calculate average rating to filter top media
    average_rating = Media.objects.aggregate(avg_rating=Avg('Rating'))['avg_rating']

    # Retrieve top rated movies and seasons based on average rating
    top_movies = Media.objects.filter(MTID=1, Rating__gt=average_rating).order_by('-Rating')[:10]
    top_seasons = Media.objects.filter(MTID=2, Rating__gt=average_rating).order_by('-Rating')[:10]

    # Retrieve genre IDs associated with the profile
    profile_genres = ProfileGenre.objects.filter(profile_id=profile_id).values_list('genre_id', flat=True)
    profile_watchlist = ProfileWatchlist.objects.filter(PID=profile_id).values_list('MID', flat=True)

    # Check if there is media in watchlist
    watchlist_media = Media.objects.filter(pk__in=profile_watchlist) if profile_watchlist else Media.objects.none()

    # Annotate each media with its rank within its genre based on rating
    ranked_media = Media.objects.annotate(
        rank=Window(
            expression=Rank(),
            partition_by=[F('mediagenre__GID__GName')],
            order_by=F('Rating').desc()
        )
    ).filter(rank=1).distinct()

    # Enhance all media objects with dynamically generated image paths
    all_media = list(top_movies) + list(top_seasons) + list(watchlist_media) + list(ranked_media)
    for media in all_media:
        image_name = media.MName.replace(" ", "_")
        image_path='/media/'+f'{image_name}.jpg'
        media.image_path = image_path

    return render(request, 'profile_media.html', {
        'profile_id': profile_id,
        'top_movies': top_movies,
        'top_seasons': top_seasons,
        'watchlist_media': watchlist_media,
        'ranked_media': ranked_media
    })

# def profile_media(request, profile_id):
#     # Retrieve top 10 movies

#     average_rating = Media.objects.aggregate(avg_rating=Avg('Rating'))['avg_rating']
#     # high_rated_media = Media.objects.filter(Rating__gt=average_rating)
#     top_movies = Media.objects.filter(MTID=1,Rating__gt=average_rating).order_by('-Rating')[:3]
#     # Retrieve top 10 seasons

#     top_seasons = Media.objects.filter(MTID=2,Rating__gt=average_rating).order_by('-Rating')[:3]
#     # Retrieve genre IDs associated with the profile
#     profile_genres = ProfileGenre.objects.filter(profile_id=profile_id).values_list('genre_id', flat=True)
#     profile_watchlist = ProfileWatchlist.objects.filter(PID=profile_id).values_list('MID', flat=True)
#     # Retrieve media IDs based on the genre IDs
#     media_ids = MediaGenre.objects.filter(GID__in=profile_genres).values_list('MID', flat=True)
#     # Retrieve media based on the media IDs
#     # top_genre_media = Media.objects.filter(pk__in=media_ids)
#     watchlist_media = Media.objects.none()
#     show_watchlist_media = profile_watchlist.count() >0  # Check if the user has less than 4 profiles

#     if show_watchlist_media:
#         watchlist_media = Media.objects.filter(pk__in=profile_watchlist)

#     #OLAP
#     # Annotate each media with its rank within its genre based on rating
#     ranked_media = Media.objects.annotate(
#     rank=Window(
#         expression=Rank(),
#         partition_by=[F('mediagenre__GID__GName')],
#         order_by=F('Rating').desc()
#     )
# ).filter(rank=1)

#     # Filter the ranked media to only include those with rank 1 (top-rated media in each genre)
#     ranked_media = ranked_media.values('mediagenre__GID__GName', 'MName', 'Rating','MID')

#     return render(request, 'profile_media.html', {
#         'profile_id': profile_id,  # Adding profile_id to the context
#         'top_movies': top_movies,
#         'top_seasons': top_seasons,
#         # 'top_genre_media': top_genre_media,
#         'watchlist_media': watchlist_media,
#         'show_watchlist_media': show_watchlist_media, 
#         'ranked_media':ranked_media   
#     })

def get_episodes(request):
    if request.method == 'GET':
        season_id = request.GET.get('season_id')
        if season_id:

            # Retrieve episodes for the selected season
            episodes = Episode.objects.filter(SID=season_id)
            # Serialize the episodes data
            serialized_episodes = [{'EID': episode.EID, 'EName': episode.EName,'Number':episode.Number,'Plot':episode.Plot}
                                    for episode in episodes]
            # serialized_episodes = [{'EID': episode.EID, 'EName': episode.EName} for episode in episodes]

            # Return serialized episodes as JSON response
            return JsonResponse({'episodes': serialized_episodes})
        else:
            # If season_id is not provided, return an empty response
            return JsonResponse({'episodes': []})
    else:
        # Handle non-GET requests (if necessary)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

def media_details(request, profile_id, media_id):
    media = get_object_or_404(Media, pk=media_id)
    genre_ids = MediaGenre.objects.filter(MID=media_id).values_list('GID', flat=True)
    genres = Genre.objects.filter(GID__in=genre_ids)
    is_in_watchlist = ProfileWatchlist.objects.filter(PID=profile_id, MID=media_id).exists()

    # Get seasons associated with the media
    seasons = Season.objects.filter(MID=media_id)

    # Get the default season (the first one)
    default_season = seasons.first()
    
    # Get episodes of the default season
    episodes = Episode.objects.filter(SID=default_season)

    return render(request, 'media_details.html', {
        'media': media,
        'profile_id': profile_id,
        'genres': genres,
        'seasons': seasons,
        'default_season': default_season,
        'episodes': episodes,
        'is_in_watchlist': is_in_watchlist
    })

# def media_details(request,profile_id,media_id):
#     # Retrieve media details
#     media = get_object_or_404(Media, pk=media_id)
#     # Retrieve genre IDs associated with the media
#     genre_ids = MediaGenre.objects.filter(MID=media_id).values_list('GID', flat=True)
#     # Retrieve genre names based on the genre IDs
#     genres = Genre.objects.filter(GID__in=genre_ids)

# #set membership
#     is_in_watchlist = ProfileWatchlist.objects.filter(PID=profile_id, MID=media_id).exists()

#     # Check if media type is season
#     if media.MTID_id == 2:
       
#         seasons = Season.objects.filter(MID=media_id)
#         # Initialize an empty list to store episodes for each season
#         season_episodes = []
#         # Retrieve episodes for each season
#         for season in seasons:
#             episodes = Episode.objects.filter(SID=season.SID)
#             season_episodes.append({'season': season, 'episodes': episodes})


#         return render(request, 'media_details.html', {'media': media, 'profile_id': profile_id, 'genres': genres, 'season_episodes': season_episodes,'is_in_watchlist':is_in_watchlist})
#     else:
#         return render(request, 'media_details.html', {'media': media, 'profile_id': profile_id, 'genres': genres,'is_in_watchlist':is_in_watchlist})

def add_to_watchlist(request, profile_id, media_id):
    # Add media to watchlist
    profile = get_object_or_404(Profile, PID=profile_id)
    media = get_object_or_404(Media, MID=media_id)
    ProfileWatchlist.objects.create(PID=profile, MID=media)
    return redirect('media_details',profile_id=profile_id, media_id=media_id)

def remove_from_watchlist(request, profile_id, media_id):
    # Remove media from watchlist
    profile = get_object_or_404(Profile, PID=profile_id)
    media = get_object_or_404(Media, MID=media_id)
    ProfileWatchlist.objects.filter(PID=profile, MID=media).delete()
    return redirect('media_details', profile_id=profile_id,media_id=media_id)

def logout_user(request):
    # Clear the session data
    request.session.flush()

    # Redirect to the login page
    return redirect('login')

def movies(request, profile_id):
    # Retrieve top 10 movies
    top_rated_movies = Media.objects.filter(MTID=1).order_by('-Rating')[:10]
    recent_movies = Media.objects.filter(MTID=1).order_by('-Released_on')[:10]

    # Set operation
    action_genre_id = Genre.objects.filter(GName='Action').first().GID
    media_ids = MediaGenre.objects.filter(GID=action_genre_id).values_list('MID', flat=True)
    action_movies = Media.objects.filter(MID__in=media_ids, MTID=1).order_by('-Released_on')[:10]

    action_media = set(MediaGenre.objects.filter(GID__GName='Action').values_list('MID', flat=True))
    drama_media = set(MediaGenre.objects.filter(GID__GName='Adventure').values_list('MID', flat=True))
    
    common_media = action_media.intersection(drama_media)
    media_objects = Media.objects.filter(MID__in=common_media)  # Corrected from id to MID

    print(media_objects)
    # Enhance media objects with image paths
    all_movies = list(top_rated_movies) + list(recent_movies) + list(action_movies)
    for movie in all_movies:
        image_name = movie.MName.replace(" ", "_")
        image_path='/media/'+f'{image_name}.jpg'
        movie.image_path = image_path


    for movie in media_objects:
        image_name = movie.MName.replace(" ", "_")
        image_path='/media/'+f'{image_name}.jpg'
        movie.image_path = image_path

    return render(request, 'movies.html', {
        'profile_id': profile_id,
        'top_rated_movies': top_rated_movies,
        'recent_movies': recent_movies,
        'action_adventure_shows': media_objects,    
    })

# def movies(request,profile_id):
#     # Retrieve top 10 movies
#     top_rated_movies = Media.objects.filter(MTID=1).order_by('-Rating')[:10]
#     recent_movies = Media.objects.filter(MTID=1).order_by('-Released_on')[:10]

#     #set operation
#     action_genres=Genre.objects.filter(GName='Action').first().GID

#     media_ids = MediaGenre.objects.filter(GID=action_genres).values_list('MID', flat=True)

#     action_movies = Media.objects.filter(MID__in=media_ids,MTID=1).order_by('-Released_on')[:10]

#     return render(request, 'movies.html', {
#         'profile_id': profile_id,  # Adding profile_id to the context
#         'top_rated_movies': top_rated_movies,   
#         'recent_movies': recent_movies,    
#         'action_movies': action_movies,    
 
#     })

def tv_shows(request,profile_id):
   # Retrieve top 10 movies
    top_rated_shows = Media.objects.filter(MTID=2).order_by('-Rating')[:10]
    recent_shows = Media.objects.filter(MTID=2).order_by('-Released_on')[:10]
    action_genres=Genre.objects.filter(GName='Action').first().GID

    media_ids = MediaGenre.objects.filter(GID=action_genres).values_list('MID', flat=True)

    action_shows = Media.objects.filter(MID__in=media_ids,MTID=2).order_by('-Released_on')[:10]

    # action_media = set(MediaGenre.objects.filter(GID__GName='Action').values_list('MID', flat=True))
    # drama_media = set(MediaGenre.objects.filter(GID__GName='Adventure').values_list('MID', flat=True))
    
    # common_media = action_media.intersection(drama_media)
    # media_objects = Media.objects.filter(MID__in=common_media)  # Corrected from id to MID

    return render(request, 'tv_shows.html', {
        'profile_id': profile_id,  # Adding profile_id to the context
        'top_rated_shows': top_rated_shows,   
        'recent_shows': recent_shows,    
        'action_shows': action_shows,    
 
    })


def browse_by_lang(request, profile_id):
    profile = get_object_or_404(Profile, PID=profile_id)
    languages = Language.objects.all()
    language_id = request.GET.get('language')
    sort_by = request.GET.get('sort_by', '-Rating')  # Default sorting

    if language_id is None:
        language_id = Language.objects.get(LName='English').LID

    language_media = Media.objects.filter(LID=language_id).order_by(sort_by)
    
    for media in language_media:
        # Replace spaces in MName with underscores
        image_name = media.MName.replace(" ", "_")
        # Construct the image path
        # image_path = os.path.join('/media/', f'{image_name}.jpg')
        image_path='/media/'+f'{image_name}.jpg'
        # Add image_path attribute to the media object
        media.image_path = image_path

    return render(request, 'browse_by_lang.html', {
        'profile_id': profile_id,
        'languages': languages,
        'language_media': language_media,
        'selected_language': language_id
    })
# def browse_by_lang(request, profile_id):
#     # Retrieve profile
#     profile = get_object_or_404(Profile, PID=profile_id)

#     # Retrieve all languages
#     languages = Language.objects.all()

#     # Retrieve language ID from GET request
#     language_id = request.GET.get('language')
    
#     sort_by = request.GET.get('sort_by')

#     if language_id==None:
#         def_lang=Language.objects.get(LName='English')
#         language_id=def_lang.LID
#     # Retrieve all media initially
#     if sort_by==None:
#         def_sort='-Rating'
#         sort_by=def_sort


#     # If a language is selected, filter media by that language
#     language_media = Media.objects.filter(LID=language_id).order_by(sort_by)

#     # Perform search if search query is provided
#     # if search_query:
#     #     language_media = language_media.filter(
#     #         Q(MName__icontains=search_query) |
#     #         Q(Plot__icontains=search_query)
#     #     )

#     return render(request, 'browse_by_lang.html', {
#         'profile_id': profile_id,
#         'languages': languages,
#         'language_media': language_media,
#     })


def browse_by_genres(request, profile_id):
    genres = Genre.objects.filter(mediagenre__isnull=False).distinct()
    displaycount = 2
    
    genre_stats = genres.annotate(
        media_count=Count('mediagenre__MID'),
        average_rating=Avg('mediagenre__MID__Rating')
    ).order_by('-media_count', '-average_rating')
    genre_stats=genre_stats.distinct()
    # Prepare genre data with top media info and dynamically set image paths
    enhanced_genres = []
    for genre in genre_stats:
        if genre.average_rating is not None:
            genre.average_rating = round(genre.average_rating, 1)

        # Fetch top media for the genre
        top_media = MediaGenre.objects.filter(GID=genre.GID).order_by('-MID__Rating').first()
        if top_media and top_media.MID:
            media = top_media.MID
            image_name = media.MName.replace(" ", "_")
            image_path='/media/'+f'{image_name}.jpg'
            enhanced_genres.append({
                'genre': genre,
                'top_media': media,
                'image_path': image_path
            })

    return render(request, 'genre_list.html', {
        'profile_id': profile_id,
        'enhanced_genres': enhanced_genres,
        'displaycount': displaycount
    })
# def browse_by_genres(request,profile_id):
#     genres = Genre.objects.filter(mediagenre__isnull=False).distinct()
#     displaycount=2
#     genre_stats = genres.annotate(
#         media_count=Count('mediagenre__MID'),
#         average_rating=Avg('mediagenre__MID__Rating')
#         ).order_by('-media_count', '-average_rating')

#     # Round the average_rating to one decimal place
#     for genre in genre_stats:
#         if genre.average_rating is not None:
#             genre.average_rating = round(genre.average_rating, 1)

    
#     return render(request, 'genre_list.html', {'genres': genres,'profile_id': profile_id,'genre_stats': genre_stats,'displaycount':displaycount})

# def media_list_by_genre(request, genre_id,profile_id):
#     genre = get_object_or_404(Genre, pk=genre_id)
#     media_ids = MediaGenre.objects.filter(GID=genre_id).values_list('MID', flat=True)
#     media_list = Media.objects.filter(MID__in=media_ids).order_by('-Released_on')


    
#     return render(request, 'media_list_by_genre.html', {'genre': genre,'media_list': media_list,'profile_id': profile_id})

def media_list_by_genre(request, genre_id, profile_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    media_ids = MediaGenre.objects.filter(GID=genre_id).values_list('MID', flat=True)
    media_list = Media.objects.filter(MID__in=media_ids).order_by('-Released_on')

    # Add image_path attribute to each media object
    for media in media_list:
        # Replace spaces in MName with underscores
        image_name = media.MName.replace(" ", "_")
        # Construct the image path
        image_path='/media/'+f'{image_name}.jpg'
        # Add image_path attribute to the media object
        media.image_path = image_path

    return render(request, 'media_list_by_genre.html', {
        'genre': genre,
        'media_list': media_list,
        'profile_id': profile_id
    })

# These are the Deliverable-5 OLAP Queries.

#This query will calculate the average rating and count of media items for each genre and order them by the count and average rating.

def genre_media_statistics(request,profile_id):
    genre_stats = Genre.objects.annotate(
        avg_rating=Avg('mediagenre__MID__Rating'),
        media_count=Count('mediagenre__MID')
    ).order_by('-media_count', '-avg_rating')

    return render(request, 'genre_stats.html', {'genre_stats': genre_stats,'profile_id':profile_id})

def latest_media_by_genre(request,profile_id):
    # Subquery to get the latest release date and media name for each genre
    latest_media = MediaGenre.objects.filter(
        GID_id=OuterRef('pk')
    ).annotate(
        latest_date=Max('MID__Released_on')
    ).order_by('-latest_date').values('latest_date', 'MID__MName')[:1]

    # Annotate each genre with the latest date and media name from MediaGenre
    genres_with_media = Genre.objects.annotate(
        latest_media_date=Subquery(latest_media.values('latest_date')),
        latest_media_name=Subquery(latest_media.values('MID__MName'))
    )

    return render(request, 'latest_media_by_genre.html', {'genres': genres_with_media,'profile_id':profile_id})

def ranked_media_in_genre(request,profile_id):
    # Ensure that Media objects are annotated with a rank based on their genre and rating
    ranked_media = Media.objects.annotate(
        rank=Window(
            expression=Rank(),
            partition_by=[F('mediagenre__GID')],
            order_by=F('Rating').desc()
        ),
        genre_name=F('mediagenre__GID__GName')
    ).filter(rank__lte=3)  # To get top 3 rated media in each genre

    return render(request, 'ranked_media.html', {'media': ranked_media,'profile_id':profile_id})

def action_drama_media(request,profile_id):
    action_media = set(MediaGenre.objects.filter(GID__GName='Action').values_list('MID', flat=True))
    drama_media = set(MediaGenre.objects.filter(GID__GName='Adventure').values_list('MID', flat=True))
    
    common_media = action_media.intersection(drama_media)
    media_objects = Media.objects.filter(MID__in=common_media)  # Corrected from id to MID

    return render(request, 'action_drama_media.html', {'media': media_objects,'profile_id':profile_id})

def statistics_dashboard(request,profile_id):
    return render(request, 'statistics_dashboard.html',{'profile_id': profile_id})
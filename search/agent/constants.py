import api

API_KEY = api.get_api_key()

CATEGORY_DICT = {
    1: 'Film & Animation',
    2: 'Autos & Vehicles',
    10: 'Music',
    15: 'Pets & Animals',
    17: 'Sports',
    18: 'Short Movies',
    19: 'Travel & Events',
    20: 'Gaming',
    21: 'Videoblogging',
    22: 'People & Blogs',
    23: 'Comedy',
    24: 'Entertainment',
    25: 'News & Politics',
    26: 'Howto & Style',
    27: 'Education',
    28: 'Science & Technology',
    29: 'Nonprofits & Activism',
    30: 'Movies',
    31: 'Anime/Animation',
    32: 'Action/Adventure',
    33: 'Classics',
    34: 'Comedy',
    35: 'Documentary',
    36: 'Drama',
    37: 'Family',
    38: 'Foreign',
    39: 'Horror',
    40: 'Sci-Fi/Fantasy',
    41: 'Thriller',
    42: 'Shorts',
    43: 'Shows',
    44: 'Trailers'
}

COLUMNS = {
    'ID': "id",
    'title': "snippet.title",
    'channel_title': "snippet.channelTitle",
    'category': "snippet.categoryId",
    'view_count': "statistics.viewCount",
    'like_count': "statistics.likeCount",
    'dislike_count': "statistics.dislikeCount",
    'favorite_count': "statistics.favoriteCount",
    'comment_count': "statistics.commentCount",
    'duration': "contentDetails.duration",
    'latitude': "recordingDetails.location.latitude",
    'longitude': "recordingDetails.location.longitude",
    'recording_date': "recordingDetails.recordingDate",
    'average_of_sentiments': "average_of_sentiments"
}


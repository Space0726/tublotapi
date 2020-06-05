import csv
import requests
import pandas as pd
from textblob import TextBlob
from constants import API_KEY, CATEGORY_DICT, COLUMNS
OUTPUT_PATH = ""

def _average(list_):
    try:
        return float(sum(list_)) / float(len(list_))
    except ZeroDivisionError:
        return 0

def _analyze_sentiment(txt):
    return TextBlob(txt).polarity

def _make_url(url, option_parameters):
    for option in option_parameters:
        url += option + "=" + str(option_parameters[option]) + "&"
    url = url[:-1]
    return url

def get_text_from_comment_thread(comment_thread):
    if comment_thread is None:
        return
    comments = []
    for comment in comment_thread:
        try:
            comments.append(comment['snippet']['topLevelComment']['snippet']['textOriginal'])
        except KeyError:
            continue
    return comments

def request_comment_thread(videoId):
    url = "https://www.googleapis.com/youtube/v3/commentThreads?"
    option_parameters = {'key': API_KEY, 'part': "snippet", 'videoId': videoId}
    url = _make_url(url, option_parameters)

    try:
        return requests.get(url).json()['items']
    except KeyError:
        return None

# For category.csv file #
def requests_categories(category_Ids):
    url = "https://www.googleapis.com/youtube/v3/videoCategories?"
    print(category_Ids)
    category_Ids = ",".join(category_Ids)
    option_parameters = {'id': category_Ids, 'part':'snippet', 'key':API_KEY}
    url = _make_url(url, option_parameters)

    try:
        return requests.get(url).json()['items']
    except KeyError:
        return None

def request_videos(video_Ids, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/videos?"
    video_Ids = ",".join(video_Ids)
    option_parameters = {'key': API_KEY, 'part': "snippet,statistics,contentDetails,recordingDetails", 'id': video_Ids, 'maxResults': str(max_results)}
    url = _make_url(url, option_parameters)

    return requests.get(url).json()['items']

def request_search_by_keyword(keyword, max_results=5, video_category_id=None):
    url = "https://www.googleapis.com/youtube/v3/search?"
    option_parameters = {'q':keyword, 'part':"snippet", 'key':API_KEY, 'maxResults':str(max_results)}
    if video_category_id is not None:
        option_parameters['type'] = "video"
        option_parameters['videoCategoryId'] = str(video_category_id)
    url = _make_url(url, option_parameters)
    try:
        return requests.get(url).json()['items']
    except KeyError:
        return None

def request_channelId_by_username(forUsername):
    url = "https://www.googleapis.com/youtube/v3/channels?"
    option_parameters = {'part': 'id', 'key':API_KEY, 'forUsername': forUsername}
    url = _make_url(url, option_parameters)

    return requests.get(url).json()['items'][0]

def request_playlist_by_channelId(channelId, maxResults=5):
    url = "https://www.googleapis.com/youtube/v3/playlists?"
    option_parameters = {'part':"snippet", 'key':API_KEY, 'channelId': channelId, 'maxResults': maxResults}
    url = _make_url(url, option_parameters)

    playlists = requests.get(url).json()['items']
    playlists_Ids = [pl['id'] for pl in playlists]
    sample_videoIds = request_videoIds_by_playlistIds(playlists_Ids)

    return sample_videoIds

def request_videoIds_by_playlistIds(playlistIds):
    sample_videoIds = []

    url = "https://www.googleapis.com/youtube/v3/playlistItems?"
    option_parameters = {'part':"snippet", 'key':API_KEY, 'playlistId':''}
    for playlistId in playlistIds:
        option_parameters['playlistId'] = playlistId
        temp_url = _make_url(url, option_parameters)
        sample_videoIds.extend([items['snippet']['resourceId']['videoId'] for items in requests.get(temp_url).json()['items']])

    return sample_videoIds

def get_channel_averages_of_videos(channelId):
    sample_videoIds = request_playlist_by_channelId("UCiBr0bK06imaMbLc8sAEz0A")

def get_category_name_dict_by_response(response):
    categories = {}
    for res in response:
        categories[res['id']] = res['snippet']['title']

    return categories

def get_video_Ids(search_responses):
    video_Ids = {}
    if None in search_responses:
        search_responses = filter(lambda x: x is not None, search_responses)
    for response in search_responses:
        try:
            video_Ids[response['snippet']['title']] = response['id']['videoId']
        except KeyError:
            continue

    return video_Ids

def get_attributes_from_video_response(columns_info, response):
    results = {}
    for column, attribute in columns_info.items():
        if column == "average_of_sentiments":
            continue
        res = response
        attr = attribute.split('.')
        while attr:
            try:
                temp_attr = attr.pop(0)
                if temp_attr == 'categoryId':
                    res = CATEGORY_DICT[int(res[temp_attr])]
                else:
                    res = res[temp_attr]
            except (KeyError, TypeError):
                res = "None"
        results[column] = res

    return results

def get_comments_from_videos(video_Ids):
    comments = []
    '''
    video_Ids = ",".join(video_Ids)
    comment_threads = request_comment_thread(video_Id)
    for comment_thread in comment_threads:
        comments.append(get_text_from_comment_thread(comment_thread)
    '''
    for video_Id in video_Ids:
        comment_thread = request_comment_thread(video_Id)
        comments.append(get_text_from_comment_thread(comment_thread))

    return comments

def get_average_sentiment_of_comments_from_video(video_Id):
    comments_thread = request_comment_thread(video_Id)
    comments = get_text_from_comment_thread(comments_thread)

    try:
        return _average(get_senitments_from_comments(comments).values())
    except AttributeError:
        return "None"

def get_senitments_from_comments(comments):
    if comments is None:
        return 0
    sentiments = {}
    for comment in comments:
        if comment is None:
            continue
        sentiments[comment] = _analyze_sentiment(comment)

    return sentiments

# For category.csv file #
def write_csv_by_dict(columns, dict_, filename="output_dict.csv"):
    filename = OUTPUT_PATH + filename
    with open(filename, 'w', newline='', encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(columns)
        print(dict_)
        for k, v in dict_.items():
            writer.writerow([k,v])

def write_csv(columns, data, filename="output.csv"):
    filename = OUTPUT_PATH + filename
    # if filename.split('/')[-1] in os.listdir(OUTPUT_PATH):
        # csvfile = open(filename, 'a', newline='', encoding="UTF-8")
        # writer = csv.writer(csvfile, delimiter=',')
    # else:
    csvfile = open(filename, 'w', newline='', encoding="UTF-8")
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(columns)
    number_of_data = 0
    for d in data:
        writer.writerow(d)
        number_of_data += 1
    print("Done! {} rows saved at ".format(number_of_data) + filename)
    csvfile.close()

def read_video_ids_csv(filename):
    video_ids = set()
    filename = OUTPUT_PATH + filename
    with open(filename, encoding="UTF-8") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            video_ids.add(row[0])

    print(video_ids)
    return video_ids

def run_tui():
    # Type output file
    output_filename = input("Type output file name (default is output.csv): ")
    video_Ids = set()
    # if output_filename in os.listdir(OUTPUT_PATH):
        # video_Ids = read_video_ids_csv(output_filename)
    keyword = 'default'
    while True:
        # Type keyword
        keyword = input("Type search keyword (quit = type 'q!'): ")
        if keyword == 'q!':
            break

        # Type categories that user want
        print(CATEGORY_DICT)
        category = input("Type category ID that you want (If not, just type Enter): ")
        if category == '':
            category = None

        # Type number of results
        number_of_results = input("Type number of results that you want (default is 5, [5, 50]): ")
        if number_of_results == "":
            res = request_search_by_keyword(keyword, video_category_id=category)
        else:
            res = request_search_by_keyword(keyword, max_results=number_of_results, video_category_id=category)

        # Get video IDs
        ids = list(get_video_Ids(res).values())
        data = []

        # Get video objects
        response = request_videos(ids)

        # Get attributes of videos
        for res in response:
            attributes = get_attributes_from_video_response(COLUMNS, res)

            # Remove duplicate value
            if attributes['ID'] in video_Ids:
                continue
            else:
                video_Ids.add(attributes['ID'])
                data.append(list(attributes.values()))

            # Calculate senitments
            average_of_sentiments = get_average_sentiment_of_comments_from_video(attributes['ID'])
            data[-1].append(average_of_sentiments)
            print(data[-1], '\n')

        # Write csv file
        write_csv(COLUMNS.keys(), data, output_filename)

if __name__ == "__main__":
    run_tui()
    # # #
    # *** For analyze output file ***
    # output_filename = OUTPUT_PATH + "output.csv"
    # sample_videoIds = request_playlist_by_channelId("UCiBr0bK06imaMbLc8sAEz0A")
    # print("Videos:", sample_videoIds)
    # # Get video objects
    # response = request_videos(sample_videoIds)
    # data = []

    # # Get attributes of videos
    # for res in response:
    #     attributes = get_attributes_from_video_response(COLUMNS, res)
    #     data.append(list(attributes.values()))

    #     # Calculate senitments
    #     average_of_sentiments = get_average_sentiment_of_comments_from_video(attributes['ID'])
    #     data[-1].append(average_of_sentiments)
    #     print(data[-1], '\n')

    # # Write csv file
    # write_csv(COLUMNS.keys(), data, output_filename)
    # # #

    # # #
    # *** To receive category name *** #
    # write_csv_by_dict(["ID", "Category"], get_category_name_dict_by_response(requests_categories([str(c) for c in range(1,45)])))
    # # #


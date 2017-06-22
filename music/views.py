
# -- coding=UTF-8 --
from django.shortcuts import render
from .models import Music_Info_Detail
import urllib
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
#def search(request):
#    return render(request,'music/search.html')
from haystack.query import SearchQuerySet
import os

from haystack.generic_views import SearchView

"""
def search_results(request):
    latest_search_result_list = Music_Info_Detail.objects.filter(music_title=request.POST['search_text'])
    #latest_search_result_list_2 = Music_Info_Detail.objects.order_by('music_cloud_id')[:5]
    context = {'latest_search_result_list':latest_search_result_list}
    return render(request, 'music/search_list.html',context)
"""

def song_id(request, song_num):
    song = Music_Info_Detail.objects.get(music_local_id=song_num)
    song.music_played_times = song.music_played_times+1
    song.save()
    lyric = song.music_lyric_content
    print lyric
    new_lyric = ""
    flag = 0
    for c in lyric:
        print c
        if c == u'[':
            flag = 1
        else:
            if c==u']':
                flag = 0
            else:
                if flag == 0:
                    new_lyric = new_lyric + c
    img_url = "/Class"+str(song.Class_Num)+"/Cover/"+str(song.music_album_id)+"_"+song.music_album
    mp3_url = "/Class"+str(song.Class_Num)+"/Music/"+str(song.music_local_id)+"_"+str(song.music_cloud_id)+"_"+song.music_singer+"_"+song.music_title+".mp3"

    # print img_url
    # print mp3_url
    return render(request,'music/song_detail.html',{'song':song ,'new_lyric':new_lyric, 'img_url':img_url, 'mp3_url':mp3_url})

from haystack.inputs import AutoQuery

def get_search_results(request):
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    query = str(request.GET.get("search_text"))

    results = SearchQuerySet().filter(content=AutoQuery(query))
    score_record = []
    for re in results:
        score_record.append(re.score)
    rank_weight_1 = 5
    i = 0

    for re in results:
        score_record[i] = score_record[i] + rank_weight_1*float(re.object.music_popularity/100)
        i = i+1

    import sys
    min_played_time = sys.maxint
    max_played_time = 0
    for re in results:
        if re.object.music_played_times > max_played_time:
            max_played_time = re.object.music_played_times
        if re.object.music_played_times < min_played_time:
            min_played_time = re.object.music_played_times

    i = 0
    norm = max_played_time - min_played_time
    rank_weight_2 = 10
    if norm == 0:
        norm  = max_played_time+1
    for re in results:
        score_record[i] = score_record[i] + rank_weight_2*float(re.object.music_played_times/norm)
        i=i+1


    result_len = len(score_record)
    sort_can = []
    for i in range(0,result_len):
        sort_can.append((i, score_record[i]))

    sort_can.sort(key=lambda x:x[1],reverse = True)


    final_results = []

    for i in range(0,result_len):
        final_results.append(results[sort_can[i][0]])


    img_urls = {}
    mp3_urls = {}
    for result in final_results:
        img_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Cover/"+str(result.object.music_album_id)+"_"+result.object.music_album
        mp3_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Music/"+str(result.object.music_local_id)+"_"+str(result.object.music_cloud_id)+"_"+result.object.music_singer+"_"+result.object.music_title+".mp3"
        # img_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Cover/",str(result.object.music_album_id),"_",result.object.music_album)
        # mp3_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Music/",str(result.object.music_local_id),"_",str(result.object.music_cloud_id),"_"+result.object.music_singer,"_",result.object.music_title,".mp3")

    return render(request, "music/search.html", {"query":len(results) , "results": final_results, 'mp3_urls':mp3_urls,'img_urls':img_urls})


def get_search_singers(request):
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    query = str(request.GET.get("search_text"))

    results = SearchQuerySet().filter(content=AutoQuery(query)).filter(text_singer=AutoQuery(query))
    score_record = []
    for re in results:
        score_record.append(re.score)
    rank_weight_1 = 5
    i = 0

    for re in results:
        score_record[i] = score_record[i] + rank_weight_1*float(re.object.music_popularity/100)
        i = i+1

    import sys
    min_played_time = sys.maxint
    max_played_time = 0
    for re in results:
        if re.object.music_played_times > max_played_time:
            max_played_time = re.object.music_played_times
        if re.object.music_played_times < min_played_time:
            min_played_time = re.object.music_played_times

    i = 0
    norm = max_played_time - min_played_time
    rank_weight_2 = 10
    if norm == 0:
        norm  = max_played_time+1
    for re in results:
        score_record[i] = score_record[i] + rank_weight_2*float(re.object.music_played_times/norm)
        i=i+1


    result_len = len(score_record)
    sort_can = []
    for i in range(0,result_len):
        sort_can.append((i, score_record[i]))

    sort_can.sort(key=lambda x:x[1],reverse = True)


    final_results = []

    for i in range(0,result_len):
        final_results.append(results[sort_can[i][0]])


    img_urls = {}
    mp3_urls = {}
    for result in final_results:
        img_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Cover/"+str(result.object.music_album_id)+"_"+result.object.music_album
        mp3_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Music/"+str(result.object.music_local_id)+"_"+str(result.object.music_cloud_id)+"_"+result.object.music_singer+"_"+result.object.music_title+".mp3"
        # img_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Cover/",str(result.object.music_album_id),"_",result.object.music_album)
        # mp3_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Music/",str(result.object.music_local_id),"_",str(result.object.music_cloud_id),"_"+result.object.music_singer,"_",result.object.music_title,".mp3")

    return render(request, "music/search_singer.html", {"query":len(results) , "results": final_results, 'mp3_urls':mp3_urls,'img_urls':img_urls})


def get_search_albums(request):
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    query = str(request.GET.get("search_text"))

    results = SearchQuerySet().filter(content=AutoQuery(query)).filter(text_album=AutoQuery(query))
    score_record = []
    for re in results:
        score_record.append(re.score)
    rank_weight_1 = 5
    i = 0

    for re in results:
        score_record[i] = score_record[i] + rank_weight_1*float(re.object.music_popularity/100)
        i = i+1

    import sys
    min_played_time = sys.maxint
    max_played_time = 0
    for re in results:
        if re.object.music_played_times > max_played_time:
            max_played_time = re.object.music_played_times
        if re.object.music_played_times < min_played_time:
            min_played_time = re.object.music_played_times

    i = 0
    norm = max_played_time - min_played_time
    rank_weight_2 = 10
    if norm == 0:
        norm  = max_played_time+1
    for re in results:
        score_record[i] = score_record[i] + rank_weight_2*float(re.object.music_played_times/norm)
        i=i+1


    result_len = len(score_record)
    sort_can = []
    for i in range(0,result_len):
        sort_can.append((i, score_record[i]))

    sort_can.sort(key=lambda x:x[1],reverse = True)


    final_results = []

    for i in range(0,result_len):
        final_results.append(results[sort_can[i][0]])


    img_urls = {}
    mp3_urls = {}
    for result in final_results:
        img_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Cover/"+str(result.object.music_album_id)+"_"+result.object.music_album
        mp3_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Music/"+str(result.object.music_local_id)+"_"+str(result.object.music_cloud_id)+"_"+result.object.music_singer+"_"+result.object.music_title+".mp3"
        # img_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Cover/",str(result.object.music_album_id),"_",result.object.music_album)
        # mp3_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Music/",str(result.object.music_local_id),"_",str(result.object.music_cloud_id),"_"+result.object.music_singer,"_",result.object.music_title,".mp3")

    return render(request, "music/search_album.html", {"query":len(results) , "results": final_results, 'mp3_urls':mp3_urls,'img_urls':img_urls})


def get_search_lyrics(request):
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
    query = str(request.GET.get("search_text"))

    results = SearchQuerySet().filter(content=AutoQuery(query)).filter(text_lyrics=AutoQuery(query))

    score_record = []
    for re in results:
        score_record.append(re.score)
    rank_weight_1 = 5
    i = 0

    for re in results:
        score_record[i] = score_record[i] + rank_weight_1*float(re.object.music_popularity/100)
        i = i+1

    import sys
    min_played_time = sys.maxint
    max_played_time = 0
    for re in results:
        if re.object.music_played_times > max_played_time:
            max_played_time = re.object.music_played_times
        if re.object.music_played_times < min_played_time:
            min_played_time = re.object.music_played_times

    i = 0
    norm = max_played_time - min_played_time
    rank_weight_2 = 10
    if norm == 0:
        norm  = max_played_time+1
    for re in results:
        score_record[i] = score_record[i] + rank_weight_2*float(re.object.music_played_times/norm)
        i=i+1


    result_len = len(score_record)
    sort_can = []
    for i in range(0,result_len):
        sort_can.append((i, score_record[i]))

    sort_can.sort(key=lambda x:x[1],reverse = True)


    final_results = []

    for i in range(0,result_len):
        final_results.append(results[sort_can[i][0]])


    img_urls = {}
    mp3_urls = {}
    for result in final_results:
        img_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Cover/"+str(result.object.music_album_id)+"_"+result.object.music_album
        mp3_urls[result.object.music_local_id] = "Class"+str(result.object.Class_Num)+"/Music/"+str(result.object.music_local_id)+"_"+str(result.object.music_cloud_id)+"_"+result.object.music_singer+"_"+result.object.music_title+".mp3"
        # img_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Cover/",str(result.object.music_album_id),"_",result.object.music_album)
        # mp3_urls[result.object.music_local_id] = os.path.join("Class",str(result.object.Class_Num),"/Music/",str(result.object.music_local_id),"_",str(result.object.music_cloud_id),"_"+result.object.music_singer,"_",result.object.music_title,".mp3")

    return render(request, "music/search_lyric.html", {"query":len(results) , "results": final_results, 'mp3_urls':mp3_urls,'img_urls':img_urls})



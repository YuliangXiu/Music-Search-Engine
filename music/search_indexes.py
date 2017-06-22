from haystack import indexes
from music.models import Music_Info_Detail

class Music_Info_DetailIndex(indexes.SearchIndex, indexes.Indexable):
    text  = indexes.CharField(document = True, use_template = True)
    text_id = indexes.CharField(model_attr='music_local_id')
    text_title = indexes.CharField(model_attr='music_title')
    text_singer = indexes.CharField(model_attr = 'music_singer')
    text_album = indexes.CharField(model_attr = 'music_album')
    text_lyrics = indexes.CharField(model_attr='music_lyric_content')

    def get_model(self):
        return Music_Info_Detail

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

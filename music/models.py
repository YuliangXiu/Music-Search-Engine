from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Music_Info_Detail(models.Model):
      ##
      #     music info
      ##
      music_local_id = models.IntegerField(default=0,primary_key=True)
      music_cloud_id = models.IntegerField(default=0)
      music_title = models.CharField(max_length=100,default=' ')

      ##
      #     singer info
      ##
      music_singer = models.CharField(max_length=100,default=' ')
      music_singer_id = models.IntegerField(default=0)

      ##
      #     album_info
      ##
      music_album = models.CharField(max_length=100,default=' ')
      music_album_id = models.IntegerField(default=0)

      ##
      #     music lyric
      ##
      music_lyric_content= models.CharField(max_length=5000,default=' ',blank=True)

      #music_path = models.CharField(max_length=200, default=' ',blank=True)
      #album_cover_path = models.CharField(max_length=200, default=' ',blank=True)
      #music_type_label = models.CharField(max_length=200,default=' ')

      ##
      #     music play info
      ##
      music_popularity = models.IntegerField(default=0,blank=True)
      music_played_times = models.IntegerField(default=0,blank=True)

      ##
      #     music tag
      ##

      music_tags = models.CharField(max_length=200,default=' ')

      ##
      #     Class Num, decide which folder to store
      ##

      Class_Num = models.IntegerField(default=0,blank=True)

      def __str__(self):
          return str(self.music_local_id) +" "+ self.music_title

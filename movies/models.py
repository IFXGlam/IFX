from django.db import models


class Tag(models.Model):
    tid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    type1_id = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class Field(models.Model):
    fid = models.CharField(unique=True, max_length=300)
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Movie(models.Model):
    bid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    lang = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class Movie_Tag_Field(models.Model):
    tag = models.ForeignKey(Tag)
    movie = models.ForeignKey(Movie)
    field = models.ForeignKey(Field)

    def __str__(self):
        return self.movie, self.field, self.tag

class Description(models.Model):
    movie = models.ForeignKey(Movie)
    summery = models.TextField()
    lang = models.CharField(max_length=300)
    def __str__(self):
        return self.movie

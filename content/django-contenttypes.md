---
date: 2017-07-29
location: Kathmandu, Nepal
title: Understanding Django's ContentType
description: A gentle introduction to django.contrib.contenttypes
draft: true
---

I have to admit, it was difficult for me to really grok ContentType in my early days as a developer. It can be a difficult grasp if you are not seasoned to a little bit of abstraction.

A ContentType always points to a model. Every model you have in your project has a ContentType. Whenever you add a new model and migrate the database, django creates a ContentType for that model. An important thing to note is that, ContentType itself is a django model located at django.contrib.contenttypes app. Since it is a django model, it also has its own ContentType.

Whenever we wire up two models using `models.ForeignKey` field, we create a *direct foreign key* relationship between those two models. Take a look at the example below. 

```python
from django.db import models
from django.conf import settings

class Publisher(models.Model):
    name = models.CharField(max_length=50)

class Author(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    publisher = models.ForeignKey(Publisher)
    authors = models.ManyToManyField(Author)
    title = models.CharField(max_length=100)

class BookRating(models.Model):
    book = models.ForeignKey(Book)
    rating = models.FloatField()
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
```

Imagine this is a `models.py` of the library management app you are building for a local library. You have three models to store records for publishers, books and ratings for the books respectively.

A few months later, you get a call from the librarian. She wants to know if she can add ratings for the authors. You say, "Sure, no problem". You add a new model called `AuthorRating` to and implement the rating feature.

```python

class AuthorRating(models.Model):
    author = models.ForeignKey(Author)
    rating = models.FloatField()
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
```

Few months later, you get another call. Now the librarian wants to know if it is possible to rate the publishers too. You say, "Sure, okay" and get to work. This time you don't add a `PublisherRating` model, instead you add a `GenericRating` model.

```python
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class GenericRating(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    rated_object = GenericForeignKey()

    rating = models.FloatField()
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL)
```

The `GenericRating` model has a generic foreign key instead of a direct one. Let me explain how this works.

Whenever a relationship is created by using the `models.ForeignKey` field, the database needs a unique field from another model to unambiguously identify a particular row. For this purpose, django defaults to using the primary key of the model. The `id` field, which is automatically created, is the primary key of a model by default. In case of `AuthorRating`, to attach it to the `Author` model through `models.ForeignKey(Author)`, django adds a hidden `author_id` field on the inside. This `author_id` field refers to the primary key i.e. `id` field of the `Author` model. This is called a direct foreign key.

```python

# you can verify this in the interactive shell
first_rating = AuthorRating.objects.first()    # fetch any object that has foreign key
print(first_rating.author_id)    # print the value of the internal field
```

Similarly, when it comes to `GenericRating`, the `object_id` field works the same way the `author_id` works for `AuthorRating`. Which basically means that the `object_id` field will hold the primary key of the foreign key relationship. But just saving the primary key of the item is not enough. In addition to the primary key, we also need to know which model the primary key belongs to. This is the part where the direct foreign key to `ContentType` model comes to into play. By pointing the direct foreign key to the `ContentType` model we can dynamically set the model we want to connect to from anywhere in our code. Since we know that every django model has a distinct content type we can unambiguously refer to another model. This is how the `content_type` and `object_id` fields work together to act like a regular foreign key field. Mind you, it is not a direct foreign key.

Now comes the `rated_object = GenericForeignKey()` field. This is actually just meant to be a convenience for us developers. It can be used to access the instance the `content_type` and `object_id` fields represent together. This field will not change anything in the database. Let's try to work with GenericRating for `Author` model in the following example.

```python
from django.contrib.contenttypes.models import ContentType
from .models import Author, GenericRating

# fetch the ContentType for the Author model using the
# convenience method provided by the ContentType model manager
author_type = Author.objects.get_for_model(Author)

# create an author and rate him
kurt = Author.objects.create(name="Kurt Vonnegut Jr.")
GenericRating.objects.create(content_type=author_type, object_id=kurt.id, rating=5)

# now if we want to fetch GenericRating objects for the author
ratings_for_kurt = GenericRating.objects.filter(content_type=author_type, object_id=kurt.id)

```

#### Caution

After you've understood contenttypes, it is difficult to restrain yourself from trying to use it everywhere. There are a few ceveats to contenttypes that makes it worthwhile in only a few cases.

One of the most unsettling thing about a generic foreign key is that the relationship between your models cannot be presented clearly through an ER diagram. You cannot do `select_related` or `prefetch_related` optimizations. It adds an extra database query for every object that has a generic foreign key. The use of contenttypes adds extra complexity to a codebase.

My general rule is to not use generic relation unless there is no alternative available. However, there are some cases where you can abuse the power contenttypes gives you and use it to your advantage.


#### More

* The official [django docs for contenttypes](https://docs.djangoproject.com/en/1.11/ref/contrib/contenttypes/) is a must read.

* This [answer from stackoverflow](https://stackoverflow.com/a/21440397) goes to great lengths to teach contenttypes.

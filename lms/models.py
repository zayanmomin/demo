from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.db.models.functions import Round


class Author(models.Model):
    name = models.CharField(max_length=120, unique=True)
    birth_date = models.DateField()

    def __str__(self):
        return self.name
    

class Publisher(models.Model):
    name = models.CharField(max_length=120, unique=True)
    website = models.URLField()

    def __str__(self):
        return self.name
    

class Reviewer(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    authors = models.ManyToManyField(Author, related_name='books')
    average_rating = models.FloatField(default=0.0)
    is_poorly_rated = models.BooleanField(default=False)
    favorite_reviewers = models.ManyToManyField(Reviewer, related_name='favorite_books', blank=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=120)
    rating = models.IntegerField()
    text = models.TextField()

    # Link explicitly to a reviewer
    reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, null=True, related_name='reviews')

    def save(self, *args, **kwargs):
        is_new = not self.pk
        
        if is_new:
            reviewer = Reviewer.objects.create(name=self.reviewer_name)
            self.reviewer = reviewer
            
        super().save(*args, **kwargs)
        
        if is_new and self.rating == 5:
            self.book.favorite_reviewers.add(self.reviewer)


    def __str__(self):
        return f'Review of {self.book.title} by {self.reviewer_name}'


@receiver([post_save, post_delete], sender=Review)
def update_book_rating(sender, instance, **kwargs):
    """Update book rating whenever reviews change"""
    book = instance.book
    
    # Use database aggregation
    avg_rating = book.reviews.aggregate(avg=Round(Avg('rating'), 1))['avg'] or 0.0
    
    # Update without triggering additional saves
    Book.objects.filter(pk=book.pk).update(
        average_rating=avg_rating,
        is_poorly_rated=avg_rating < 2.0
    )
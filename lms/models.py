from django.db import models


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
        if not self.pk:
            # Create a new reviewer instance for each review in anonymous system
            reviewer = Reviewer.objects.create(
                name=self.reviewer_name
            )
            self.reviewer = reviewer
            
            # Handle 5-star reviews directly in save method
            if self.rating == 5:
                self.book.favorite_reviewers.add(reviewer)
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Review of {self.book.title} by {self.reviewer_name}'



# @receiver(post_save, sender=Review)
# def add_favorite_reviewer(sender, instance, created, **kwargs):
#     """
#     Signal handler to automatically add a reviewer to book.favorite_reviewers
#     when they submit a 5-star review
#     """
#     if created and instance.rating == 5:
#         # Get or create the reviewer
#         reviewer, _ = Reviewer.objects.get_or_create(name=instance.reviewer_name)
        
#         # Add to favorite reviewers
#         instance.book.favorite_reviewers.add(reviewer)
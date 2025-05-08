from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .models import Author, Publisher, Book, Review
from .serializers import AuthorSerializer, PublisherSerializer, BookSerializer, ReviewSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Author instances"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Publisher instances"""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Book instances with filtering"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Review instances nested under Books"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Return reviews for a specific book"""
        return Review.objects.filter(book_id=self.kwargs['book_pk'])

    def perform_create(self, serializer):
        """Save the review with the book from the URL"""
        book = get_object_or_404(Book, pk=self.kwargs['book_pk'])
        serializer.save(book=book)
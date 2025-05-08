from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import AuthorViewSet, PublisherViewSet, BookViewSet, ReviewViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

# Create nested router for reviews under books
books_router = NestedSimpleRouter(router, r'books', lookup='book')
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
]
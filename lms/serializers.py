from rest_framework import serializers
from .models import Author, Publisher, Book, Review, Reviewer
from django.utils import timezone


class AuthorSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        # Check birth_date is not in the future
        if 'birth_date' in attrs and attrs['birth_date'] > timezone.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return super().validate(attrs)

    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields = ['name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'reviewer_name', 'rating', 'text']
        read_only_fields = ['book']
    
    def validate_rating(self, value):
        """
        Check that the rating is between 1 and 5.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
    
    def create(self, validated_data):
        """
        Create and return a new Review instance.
        The favorite-reviewer side-effect is handled in the model's save method.
        """
        return Review.objects.create(**validated_data)


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, required=False)
    average_rating = serializers.FloatField(read_only=True)
    is_poorly_rated = serializers.BooleanField(read_only=True)
    favorite_reviewers = ReviewerSerializer(many=True, read_only=True)

    author_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()),
        write_only=True,
        required=False
    )   # This field is used to set authors when creating/updating a book
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'publication_date', 'authors', 
                  'average_rating', 'is_poorly_rated', 'favorite_reviewers',
                'author_ids']
        read_only_fields = ['average_rating', 'is_poorly_rated', 'favorite_reviewers']
    
    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        # Only proceed if we need to include reviews
        if request and request.query_params.get('include_reviews') == 'true':
            # Get ratings filter parameters
            rating_min = request.query_params.get('rating_min')
            rating_max = request.query_params.get('rating_max')
            
            # Start with all reviews
            reviews = instance.reviews.all()
            
            # Apply filters if provided based on the query params
            if rating_min:
                reviews = reviews.filter(rating__gte=float(rating_min))
            if rating_max:
                reviews = reviews.filter(rating__lte=float(rating_max))
            
            # Add filtered reviews to response
            representation['reviews'] = ReviewSerializer(reviews, many=True).data
        
        return representation
    
    def create(self, validated_data):
        author_ids = validated_data.pop('author_ids', [])
        book = Book.objects.create(**validated_data)
        
        # Add authors to book
        if author_ids:
            book.authors.add(*author_ids)
            
        return book
    
    def update(self, instance, validated_data):
        # Pop author_ids so we can handle them separately
        author_ids = validated_data.pop('author_ids', None)
        
        # Update all other fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update authors if author_ids were provided
        if author_ids is not None:
            # Use .set() to replace all existing authors
            instance.authors.set(author_ids)
        
        return instance
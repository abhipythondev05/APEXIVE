from django.shortcuts import render
from .models import ImagePic
from rest_framework import viewsets
from rest_framework.response import Response
from .models import ImagePic
from .serializers import ImagePicSerializer

def uploaded_and_downloaded_view(request):
    # Get all images that are both uploaded and downloadable
    uploaded_and_downloaded_images = ImagePic.objects.uploaded_and_downloaded_images()
    
    # Print for debugging (optional)
    print(uploaded_and_downloaded_images)

    # Check if the queryset is empty and handle accordingly
    if not uploaded_and_downloaded_images:
        return render(request, 'uploaded_and_downloaded.html', {
            'images': [],  # Pass an empty list if no images found
            'message': 'No uploaded and downloadable images found.'  # Provide a user-friendly message
        })

    # Return a rendered template with the context
    return render(request, 'uploaded_and_downloaded.html', {
        'images': uploaded_and_downloaded_images
    })

def recently_modified_view(request):
    # Get all images modified in the last 30 days
    recent_images = ImagePic.objects.images_modified_recently(1500)

    # Print for debugging (optional)
    print(recent_images)

    # Check if the queryset is empty and handle accordingly
    if not recent_images:
        return render(request, 'recent_images.html', {
            'recent_images': [],  # Pass an empty list if no images found
            'message': 'No recently modified images found.'  # Provide a user-friendly message
        })

    # Return a rendered template with the context
    return render(request, 'recent_images.html', {
        'recent_images': recent_images
    })


# image viewset

class ImagePicViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing image records.
    """
    queryset = ImagePic.objects.all()
    serializer_class = ImagePicSerializer

    def list(self, request, *args, **kwargs):
        """
        Return a list of all images with dynamic fields.
        """
        queryset = self.get_queryset()
        
        # Specify fields dynamically based on some condition, e.g., user role or query params
        fields = request.query_params.get('fields', None)  # Expecting a comma-separated list of fields
        if fields:
            fields = fields.split(',')  # Split the fields into a list

        serializer = self.get_serializer(queryset, many=True, fields=fields)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Return a single image record.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new image record.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        """
        Update an existing image record.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


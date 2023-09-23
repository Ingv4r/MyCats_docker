from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Achievement, Cat
from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    """View set for Cat's model."""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """Create a new cat whose Owner is a current user."""
        serializer.save(owner=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    """View set for Achievement's model."""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None

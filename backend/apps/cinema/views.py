from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Movie
from .serializers import MovieSerializer
from utils.pagination import StandardResultsSetPagination
from django.db.models import Q


class MovieViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para películas.
    """
    queryset = Movie.objects.all().order_by('-release_date')
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['classification', 'is_active', 'is_scheduled', 'release_date']
    search_fields = ['title', 'director', 'main_cast', 'production_company', 'original_language']
    ordering_fields = ['release_date', 'title', 'expected_audience']


class MovieSearchView(generics.ListAPIView):
    """
    Vista especializada para búsqueda libre.
    """
    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination  # opcional si quieres paginar resultados de búsqueda también

    def get_queryset(self):
        """
        Permite búsqueda por título, director, reparto, productora.
        """
        queryset = self.queryset
        q = self.request.query_params.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(director__icontains=q) |
                Q(main_cast__icontains=q) |
                Q(production_company__icontains=q)
            )

        return queryset.order_by('-release_date')

from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters

from .models import Ticket
from .serializers import TicketSerializer
from utils.pagination import StandardResultsSetPagination


class TicketViewSet(viewsets.ModelViewSet):
    """
    CRUD + endpoints extra para gestión de tickets.
    """
    queryset = Ticket.objects.select_related('user', 'movie', 'room', 'seat').all().order_by('-purchase_datetime')
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'movie', 'show_date']
    search_fields = ['ticket_code', 'user__username', 'movie__title']
    ordering_fields = ['purchase_datetime', 'show_date', 'price']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_tickets(self, request):
        """
        Endpoint personalizado para listar solo los tickets del usuario autenticado.
        """
        tickets = self.queryset.filter(user=request.user)
        page = self.paginate_queryset(tickets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tickets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """
        Endpoint para cancelar un ticket.
        Solo permite cancelar si el ticket está activo.
        """
        ticket = self.get_object()
        if ticket.status != 'active':
            return Response({'detail': 'El ticket no se puede cancelar porque no está activo.'},
                            status=status.HTTP_400_BAD_REQUEST)
        ticket.status = 'cancelled'
        ticket.save()
        return Response({'detail': f'Ticket {ticket.ticket_code} cancelado correctamente.'})


class TicketSearchView(generics.ListAPIView):
    """
    Búsqueda avanzada de tickets.
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Permite búsqueda libre por código, película o sala.
        """
        user = self.request.user
        queryset = Ticket.objects.filter(user=user)
        q = self.request.query_params.get('q')

        if q:
            queryset = queryset.filter(
                models.Q(ticket_code__icontains=q) |
                models.Q(movie__title__icontains=q) |
                models.Q(room__name__icontains=q)
            )

        return queryset.order_by('-purchase_datetime')

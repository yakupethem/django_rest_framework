from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from favourite.api.paginations import FAVPagination
from favourite.api.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from favourite.models import Favourite
from favourite.api.serializers import FavouriteListCreateAPISerialiers,FavouriteAPISerialiers

class FavouriteListCreateAPIView(ListCreateAPIView):
    pagination_class = FAVPagination
    serializer_class = FavouriteListCreateAPISerialiers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavouriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteAPISerialiers
    permission_classes = [IsOwner]
    lookup_field = "pk"
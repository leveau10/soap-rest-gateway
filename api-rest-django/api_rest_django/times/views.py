from rest_framework.viewsets import ModelViewSet
from .serializers import TimeSerializer
from .models import Time

class TimeView(ModelViewSet):
    serializer_class = TimeSerializer
    queryset = Time.objects.all()
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .business_logic import get_line_min_distance, get_line_min_score
from .models import PointModel
from .serializers import LineLengthSerializer, LineScoreSerializer
# Create your views here.


class PointViewSet(viewsets.GenericViewSet):

    queryset = PointModel.objects.all()

    @action(detail=True, methods=['GET'])
    def min_distance(self, request, pk):
        p1 = self.get_object()
        err_response, p2 = self.check_to_in_query_string(request)
        if err_response is not None:
            return err_response
        min_dist_line = get_line_min_distance(p1, p2)
        serializer = LineLengthSerializer(
            {
                'geometry': min_dist_line['line'],
                'properties':
                    {
                        'length':
                            min_dist_line['length']
                    }
            })
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def min_score(self, request, pk):
        p1 = self.get_object()
        err_response, p2 = self.check_to_in_query_string(request)
        if err_response is not None:
            return err_response
        min_dist_line = get_line_min_score(p1, p2)
        serializer = LineScoreSerializer(
            {
                'geometry': min_dist_line['line'],
                'properties':
                    {
                        'score':
                            min_dist_line['score']
                    }
            })
        return Response(serializer.data)

    def check_to_in_query_string(self, request):
        p2_id = request.GET.get('to')
        if p2_id is None:
            return Response("No 'to' value in query string", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        p2 = PointModel.objects.filter(pk=p2_id)
        if not p2:
            return Response("Point referred in 'to' doesn't exist", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        p2 = p2[0]  # actual evaluation of queryset
        return None, p2

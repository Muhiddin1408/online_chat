import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from starlette import status
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import User
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination

from chat.serializers import SerializerUser


# Create your views here.


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        ip = request.data.get('ip')
        years = request.data.get('years')
        choose_years = request.data.get('choose_years')
        choose_gen = request.data.get('choose_gen')
        gen = request.data.get('gen')

        user = User.objects.filter(username=ip)
        if not user:
            number = User.objects.create(
                username=ip,
                ip=ip,
                years_id=years,
                choose_years_id=choose_years,
                choose_gen=choose_gen,
                gen=gen,
                login_time=datetime.datetime.now()
            )
            number.save()
            token = RefreshToken.for_user(number)
            result = {
                'access': str(token.access_token),
                'refresh': str(token),
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0
            }

            return Response(res, status=status.HTTP_200_OK)

    except KeyError:

        return Response(status=status.HTTP_404_NOT_FOUND)


class SmallPagesPagination(PageNumberPagination):
    page_size = 20


class SearchUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SerializerUser
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        product = User.objects.filter(years_id=user.choose_years.id,  gen=user.choose_gen)
        serializer = SerializerUser(product, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat():
    pass


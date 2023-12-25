import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from starlette import status
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import User, Chat, Massage, Years
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .serializers import SerializerUser, SerializerChat, SerializerYears


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        ip = request.data.get('ip')
        lang = request.data.get('lang')
        years = request.data.get('years')
        choose_years = request.data.get('choose_years')
        choose_gen = request.data.get('choose_gen')
        gen = request.data.get('gen')

        user = User.objects.filter(username=ip)
        if not user:
            number = User.objects.create(
                username=ip,
                ip=ip,
                lang=lang,
                years_id=years,
                choose_gen=choose_gen,
                gen=gen,
                login_time=datetime.datetime.now()
            )
            for i in choose_years:
                number.choose_years.add(Years.objects.get(id=i))
                number.save()
            print(SerializerUser(number).data)
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


class YearView(generics.ListAPIView):
    queryset = Years.objects.all()
    serializer_class = SerializerYears
    permission_classes = [AllowAny]
    pagination_class = SmallPagesPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        product = Years.objects.all()
        serializer = SerializerYears(product, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat(request):
    data = request.POST
    user_id = data.get('id')
    user2 = request.user
    user = User.objects.get(id=user_id)
    Chat.objects.create(
        create=user,
        create2=user2,
    )
    return HttpResponseRedirect(reverse_lazy('create'))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    user = request.user
    chat = Chat.objects.filter(create=user) | Chat.objects.filter(create2=user)
    chat.order_by('id').values()
    return Response(SerializerChat(chat, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def massage_list(request, pk):
    chat = Massage.objects.filter(chat_id=pk)
    chat.order_by('-id')
    return Response(SerializerChat(chat, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    data = request.POST
    chat_id = data.get('id')
    massage = data.get('massage')
    user = request.user
    Massage.objects.create(
        massage=massage,
        chat_id=chat_id,
        user=user
    )
    return

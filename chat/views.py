from datetime import timedelta, datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from starlette import status
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import User, Chat, Massage, Years
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import SerializerUser, SerializerChat, SerializerYears, SerializerMassage


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
                choose_years_id=choose_years[0],
                gen=gen,
                login_time=datetime.now()
            )
            # for i in choose_years:
            #     number.choose_years.add(Years.objects.get(id=i))
            #     number.save()
            token = RefreshToken.for_user(number)
            result = {
                'access': str(token.access_token),
                'refresh': str(token),
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            user = User.objects.get(username=ip)
            user.gen = gen
            user.choose_gen = choose_gen
            user.choose_years_id = choose_years[0]
            user.years_id = years
            user.lang = lang
            user.login_time = datetime.now()
            user.save()
            token = RefreshToken.for_user(user.last())
            result = {
                'access': str(token.access_token),
                'refresh': str(token),
            }

            return Response(result, status=status.HTTP_200_OK)
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
        product = User.objects.filter(lang=user.lang, years=user.choose_years,  gen=user.choose_gen,
                                      choose_gen=user.gen, choose_years=user.years,
                                      login_time__range=[datetime.now() - timedelta(minutes=5), datetime.now()])
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
    data = request.data
    user_id = data.get('id')
    user = request.user.id
    user2 = User.objects.get(id=user_id)
    chat = Chat.objects.create(
        create_id=user,
        create2=user2,
    )
    context = {
        "id": chat.id
    }
    return Response(context, status=status.HTTP_201_CREATED)


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
    return Response(SerializerMassage(chat, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def last_login(request):
    user = request.user
    user.login_time = datetime.now()
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def chat_delete(request, pk):
    chat = Chat.objects.get(id=pk)
    chat.delete = False
    chat.save()
    return Response(SerializerChat(chat).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def massage_read(request, pk):
    chat = Massage.objects.get(id=pk)
    chat.read = True
    chat.save()
    return Response(SerializerMassage(chat).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def online(request):
    user = User.objects.filter(login_time__date__range=[datetime.now() - timedelta(minutes=5), datetime.now()]).count()
    return Response({'online': user}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def writing(request):
    chat = Chat.objects.get(id=request.data.get('id'))
    if request.user == chat.create:
        user_ip = chat.create2.ip
    else:
        user_ip = chat.create.ip
    context = {
        'user_ip': user_ip,
        'method': request.data.get('method')
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    data = request.data
    chat_id = data.get('id')
    massage = data.get('massage')
    user = request.user
    Massage.objects.create(
        massage=massage,
        chat_id=chat_id,
        user=user
    )
    return Response(status=status.HTTP_201_CREATED)



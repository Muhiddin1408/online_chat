from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from starlette import status
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import ReportTheme, User, Chat, Massage, Years, Apartment, Privacy
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .serializers import SerializerUser, SerializerChat, SerializerYears, SerializerMassage, ApartmentMassage, SpamThemeSerializer, UserReponseSerializer, UserSpamSerializer
from chat.tasks import check_restricted_word
from django.db import IntegrityError

@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        ip = request.data.get('ip')
        uuid = request.data.get('uuid')
        language = request.data.get('language')
        years = request.data.get('years')
        target_years = request.data.get('target_years')
        target_gender = request.data.get('target_gender')
        gender = request.data.get('gender')
        user= User.objects.create(
            username=ip,
            ip=ip,
            uuid=uuid,
            language=language,
            years_id=years,
            target_gender=target_gender,
            gender=gender,
            login_time=timezone.now(),
        )
        for year in target_years:
            user.target_years.add(Years.objects.get(id=year))
            user.save()
        token = RefreshToken.for_user(user)
        data = {
            'access': str(token.access_token),
            'refresh': str(token),
            'id': user.id,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    except IntegrityError:
        user = User.objects.get(uuid=uuid)
        token = RefreshToken.for_user(user)
        data = {
            'access': str(token.access_token),
            'refresh': str(token),
            'id': user.id,
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
            )


class SmallPagesPagination(PageNumberPagination):
    page_size = 20


class SearchUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SerializerUser
    permission_classes = [IsAuthenticated]
    pagination_class = SmallPagesPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.target_gender == 'all':
            search = Chat.objects.filter(sender__language=user.language, sender__years__in=user.target_years.all(),
                                         sender__target_years=user.years,
                                         sender__login_time__range=[timezone.now() - timedelta(minutes=5), timezone.now()],
                                         free=True)

        else:
            search = Chat.objects.filter(sender__language=user.language, sender__years__in=user.target_years.all(),
                                         sender__gender=user.target_gender,
                                         sender__target_years=user.years,
                                         sender__login_time__range=[timezone.now() - timedelta(minutes=5), timezone.now()],
                                         free=True)

        if search:
            for i in search:
                if i.sender.target_gender == 'all' or i.sender.target_gender == user.gender:
                    result = search.last()
                    result.receiver = user
                    result.free = False
                    result.save()
                    context = {
                        'chat_id': result.id,
                        'user_1': result.sender.ip,
                        'user_2': result.receiver.ip,
                    }
                    return Response(context, status=status.HTTP_200_OK)
        else:
            chat_create = Chat.objects.create(
                name=user.ip,
                sender=user,
                updated_at=timezone.now(),
            )
            return Response({'chat_id': chat_create.id}, status=status.HTTP_200_OK)

        # else:
        #     product = User.objects.filter(lang=user.lang, years__in=user.choose_years.all(),  gen=user.choose_gen,
        #                               choose_gen=user.gen, choose_years=user.years,
        #                               login_time__range=[datetime.now() - timedelta(minutes=5), datetime.now()])
        # serializer = SerializerUser(product, many=True)
        # page = self.paginate_queryset(serializer.data)
        # return self.get_paginated_response(page)


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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat(request, pk):
    # chat = Chat.objects.get(id=pk)
    # chat.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_chat(request):
    data = request.data
    receiver_id = data.get('id')
    user = request.user
    receiver = User.objects.get(id=receiver_id)
    chat = Chat.objects.create(
        sender=user,
        receiver=receiver,
        updated_at=timezone.now()
    )
    context = {
        "id": chat.id
    }
    return Response(context, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_list(request):
    user = request.user
    chat = Chat.objects.filter(sender=user, is_deleter=True) | Chat.objects.filter(receiver=user, is_deleted=True)
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
    user.login_time = timezone.now()
    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def chat_delete(request, pk):
    chat = Chat.objects.get(id=pk)
    if not chat:
        return Response(data={
            "message": "Not found !"
        }, status=status.HTTP_400_BAD_REQUEST)
    chat.is_deleted = False
    chat.save()
    return Response(SerializerChat(chat).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def massage_read(request, pk):
    chat = Massage.objects.get(id=pk)
    chat.is_read = True
    chat.save()
    return Response(SerializerMassage(chat).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def online(request):
    user = Chat.objects.filter(free=False).count()
    return Response({'online': user*2}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def writing(request):
    if request.data.get('method') == 'write':
        request.user.writing = True
    else:
        request.user.writing = False
    request.user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def writingid(request, pk):
    chat = Chat.objects.get(id=pk)
    if request.user == chat.sender:
        user_ip = chat.receiver.ip
        user_id = chat.receiver.writing
    else:
        user_ip = chat.sender.ip
        user_id = chat.sender.writing
    context = {
        'user_ip': user_ip,
        'method': user_id
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    data = request.data
    chat_id = data.get('id')
    message = data.get('message')
    user = request.user
    Massage.objects.create(
        message=message,
        chat_id=chat_id,
        user=user
    )
    check_restricted_word.delay(message=message, user_id=user.id, chat_id=chat_id)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def file(request):
    files = Apartment.objects.get(id=1)
    return Response(ApartmentMassage(files).data)


def html(request):
    privacy = Privacy.objects.all()
    context = {
        "privacy": privacy,
    }
    return render(request, 'post.html', context=context)


@api_view(['GET'])
@permission_classes([AllowAny])
def report_themes(request):
    themes = ReportTheme.objects.filter(is_active=True)
    serializer = SpamThemeSerializer(themes, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_user(request):
    data = request.data
    data['reporter_id'] = request.user.id
    serializer = UserSpamSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMe(request):
    serializer = UserReponseSerializer(instance=request.user)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
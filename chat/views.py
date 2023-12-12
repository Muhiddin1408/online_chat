import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from starlette import status

from chat.models import User


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
                years=years,
                choose_years=choose_years,
                choose_gen=choose_gen,
                gen=gen,
                login_time=datetime.datetime.now()
            )
            number.save()
        elif user.last().sms_status == False:
            user.last().delete()
            number = User.objects.create(
                username=phone,
                first_name=first_name
            )
            number.set_password(password)
            sms_code = random.randint(1000, 9999)
            number.phone = int(phone)
            number.sms_code = sms_code
            number.save()
            # send_sms(phone, "Tasdiqlash codi " + str(sms_code))

            if number:
                result = {
                    'status': 1,
                    'msg': 'Sms sended',
                    'user': SerializerUser(number, many=False, context={"request": request}).data,
                }
                SendSmsApiWithEskiz(message="https://star-one.uz/ Tasdiqlash kodi " + str(sms_code), phone=phone).send()
                return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0
            }

            return Response(res, status=status.HTTP_200_OK)

    except KeyError:

        return Response(status=status.HTTP_404_NOT_FOUND)



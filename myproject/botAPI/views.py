import time
import datetime
import string
import requests

from random import choices
from bs4 import BeautifulSoup

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from botAPI.models import CustomUser, Space, SpaceLog, PersonStatus, SpendingCategory, ReferralCode, Spending
from botAPI.serializers import UserSerializer, SpaceSerializer, UserConnectSerializer, CreatingSpaceSerializer, \
    SpendingCategorySerializer, ReferralCodeSerializer, PersonStatusSerializer, SpendingSerializer, \
    NewSpendingSerializer


def generate_random_referral_code():
    referral_code = ''.join(choices(string.ascii_letters + string.digits, k=15))
    return referral_code


def exchange_rate():

    URL = 'https://www.nbrb.by/statistics/rates/ratesdaily.asp'

    source = requests.get(URL)
    soup = BeautifulSoup(source.text, 'html.parser')
    table = soup.find('table')
    list_info =[]

    for tr in table.findAll('tr'):
        for td in tr.findAll('td', {'class': 'curAmount'}):
            if td.text == '1 USD' or td.text == '1 EUR':
                list_info.append(tr)
                if len(list_info) == 2:
                    break

    dollar = list_info[0]
    euro = list_info[1]

    dollar = dollar.find('td', {'class': 'curCours'})
    dollar = float(dollar.text.strip().replace(',', '.'))

    euro = euro.find('td', {'class': 'curCours'})
    euro = float(euro.text.strip().replace(',', '.'))

    return {'USD': dollar, 'EUR': euro}


def time_finder(difference):
    now = datetime.date.today()
    year = int(str(now)[:4])
    month = int(str(now)[5:7])
    day = int(str(now)[8:10])
    if month - difference <= 0:
        year -= 1
        month = month - difference + 12

    return datetime.date(year, month, day)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["POST"], url_path="connect", url_name="connect")
    def connect_telegram_account(self, request):
        serializer = UserConnectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user, created = CustomUser.objects.get_or_create(telegram_id=data["telegram_id"])

        if created or user.name != data['name']:
            old_name = user.name
            user.name = data["name"]
            user.save()
            if created:
                SpaceLog.objects.create(user=user, action=f"Добавлен пользователь")
            else:
                SpaceLog.objects.create(user=user, action=f'Имя пользователя "{old_name}" изменено на "{user.name}"')

        return Response(UserConnectSerializer(user).data, status.HTTP_200_OK)

    @action(detail=False, methods=["PATCH"], url_path="update_user", url_name="update_user")
    def update_user_info(self, request):
        main_user = CustomUser.objects.get(pk=request.data['user_id'])
        del request.data['user_id']
        change_user = CustomUser.objects.get(name=request.data['change_user'])
        space = Space.objects.get(title=request.data['space_title'])
        change_status = PersonStatus.objects.get(user=change_user, space=space)

        if str(main_user.name) == str(change_status.user):
            return Response({'text': 'It is you'}, status.HTTP_200_OK)

        if change_status.grade == 'M':
            change_status.grade = 'C'
        else:
            change_status.grade = 'M'

        user_grade = {
            'C': 'Casual user',
            'M': 'Master user'
        }

        change_status.save()
        SpaceLog.objects.create(user=main_user, action=f'В SPACE "{space.title}" изменен статус пользователя '
                                                       f'{change_user.name} на {user_grade[change_status.grade]}')
        return Response(PersonStatusSerializer(change_status).data, status.HTTP_200_OK)

    @action(detail=False, methods=["PATCH"], url_path="ban_user", url_name="ban_user")
    def ban_user(self, request):
        main_user = CustomUser.objects.get(pk=request.data['user_id'])
        del request.data['user_id']
        ban_user = CustomUser.objects.get(name=request.data['ban_user'])
        space = Space.objects.get(title=request.data['space_title'])
        ban_user_status = PersonStatus.objects.get(user=ban_user, space=space, is_banned=request.data['is_banned'])

        if request.data['is_banned']:
            ban_user_status.is_banned = False
            SpaceLog.objects.create(user=main_user,
                                    action=f'В SPACE "{space.title}" был раззабанен пользователь {ban_user.name}')
        else:
            ban_user_status.is_banned = True
            ban_user_status.grade = 'C'
            SpaceLog.objects.create(user=main_user,
                                    action=f'В SPACE "{space.title}" был забанен пользователь {ban_user.name}')

        ban_user_status.save()
        return Response(PersonStatusSerializer(ban_user_status).data, status.HTTP_200_OK)



class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

    @action(detail=False, methods=["POST"], url_path="space_create", url_name="space_create")
    def space_create(self, request):
        user = CustomUser.objects.get(pk=request.data['id'])
        del request.data['id']
        serializer = CreatingSpaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        space = Space.objects.create(title=data['title'], currency=data['currency'])
        PersonStatus.objects.create(user=user, space=space, grade='A')
        SpaceLog.objects.create(user=user, action=f'Создан новый SPACE - "{space.title}"')
        return Response(CreatingSpaceSerializer(space).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"], url_path="get_space_info", url_name="get_space_info")
    def get_space_info(self, request):
        # user = CustomUser.objects.get(pk=request.data['id'])
        # del request.data['id']
        space = Space.objects.get(title=request.data['title'])
        return Response(SpaceSerializer(space).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["DELETE"], url_path="delete_space", url_name="delete_space")
    def delete_space(self, request):
        user = CustomUser.objects.get(pk=request.data['user_id'])
        del request.data['user_id']
        space = Space.objects.get(title=request.data['space'])
        space.delete()
        SpaceLog.objects.create(user=user, action=f'SPACE "{space.title}" был удален')
        return Response({'text': 'Success delete'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["DELETE"], url_path="delete_user", url_name="delete_user")
    def delete_user_from_space(self, request):
        user = CustomUser.objects.get(pk=request.data['user_id'])
        del request.data['user_id']
        space = Space.objects.get(title=request.data['space'])
        delete_status = PersonStatus.objects.get(user=user, space=space)
        delete_status.delete()
        SpaceLog.objects.create(user=user, action=f'Пользователь {user.name} вышел из "{space.title}"')
        return Response({'text': 'Success delete'}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = SpendingCategory.objects.all()
    serializer_class = SpendingCategorySerializer

    @action(detail=False, methods=["POST"], url_path="category_create", url_name="category_create")
    def category_create(self, request):
        user = CustomUser.objects.get(pk=request.data['id'])
        del request.data['id']
        space = Space.objects.get(title=request.data['space'])
        request.data['space'] = space.id
        serializer = SpendingCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        category, created = SpendingCategory.objects.get_or_create(title=data['title'], space=data['space'])
        if not created:
            return Response({'text': 'Nope'}, status=status.HTTP_200_OK)
        else:
            SpaceLog.objects.create(user=user, action=f'В "{space.title}" добавлена новая категория - "{category.title}"')
            return Response(SpendingCategorySerializer(category).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"], url_path="show_categories", url_name="show_categories")
    def show_categories(self, request):
        space = Space.objects.get(title=request.data['space_title'])
        categories = SpendingCategory.objects.filter(space=space.id)
        return Response(SpendingCategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["DELETE"], url_path="delete_category", url_name="delete_category")
    def delete_category(self, request):
        user = CustomUser.objects.get(pk=request.data['user_id'])
        del request.data['user_id']
        space = Space.objects.get(title=request.data['space'])
        category = SpendingCategory.objects.get(space=space, title=request.data['category'])
        category.delete()
        SpaceLog.objects.create(user=user, action=f'Из "{space.title}" было удалена '
                                                  f'категория "{request.data["category"]}"')
        return Response({'text': 'Success delete'}, status=status.HTTP_200_OK)


class ReferralCodeViewSet(viewsets.ModelViewSet):
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCodeSerializer

    @action(detail=False, methods=["POST"], url_path="generate_code", url_name="generate_code")
    def generate_code(self, request):
        user = CustomUser.objects.get(pk=request.data['user'])
        space = Space.objects.get(title=request.data['space'])
        request.data['space'] = space.id
        request.data['code'] = generate_random_referral_code()
        serializer = ReferralCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        exist_code = ReferralCode.objects.filter(space=data['space'])

        if exist_code:
            ReferralCode.objects.get(space=data['space']).delete()

        code = ReferralCode.objects.create(user=data['user'], space=data['space'], code=request.data['code'])
        SpaceLog.objects.create(user=user, action=f'Для "{space.title}" cгенерирован реферальный код - "{code.code}"')
        return Response(ReferralCodeSerializer(code).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"], url_path="join_space", url_name="join_space")
    def join_space(self, request):
        user = CustomUser.objects.get(pk=request.data['user'])

        try:
            code = ReferralCode.objects.get(code=request.data['code'])
        except Exception:
            return Response({'text': 'No code'}, status=status.HTTP_200_OK)

        space = Space.objects.get(title=code.space)

        if datetime.datetime.now() < code.expiration_time:

            try:
                PersonStatus.objects.get(user=user, space=space)
            except Exception:
                join_space = PersonStatus.objects.create(user=user, space=space, grade='C')
                SpaceLog.objects.create(user=user, action=f'"{user.name}" присоединился к "{space.title}"')
                return Response(PersonStatusSerializer(join_space).data, status=status.HTTP_201_CREATED)
            else:
                return Response({'text': 'Exist', 'space': space.title}, status=status.HTTP_200_OK)

        else:
            code.delete()
            SpaceLog.objects.create(user=user, action=f'Для "{space.title}" истек срок действия реферального кода')
            return Response({'text': 'Invalid code'}, status=status.HTTP_200_OK)

class SpendingViewSet(viewsets.ModelViewSet):
    queryset = Spending.objects.all()
    serializer_class = SpendingSerializer

    @action(detail=False, methods=["POST"], url_path="make_spending", url_name="make_spending")
    def make_spending(self, request):
        user = CustomUser.objects.get(pk=request.data['user'])
        space = Space.objects.get(title=request.data['space'])
        category = SpendingCategory.objects.get(title=request.data['category'], space=space)
        request.data['space'] = space.id
        request.data['category'] = category.id
        serializer = SpendingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data['currency'] == "BYN" and space.currency == "EUR":
            course = exchange_rate()['EUR']
            data['expense'] = float(data['expense']) / course

        elif data['currency'] == "USD" and space.currency == "EUR":
            course = exchange_rate()
            course_eur = course['EUR']
            course_usd = course['USD']
            data['expense'] = float(data['expense']) * course_usd / course_eur

        elif data['currency'] == "BYN" and space.currency == "USD":
            course = exchange_rate()['USD']
            data['expense'] = float(data['expense']) / course

        elif data['currency'] == "EUR" and space.currency == "USD":
            course = exchange_rate()
            course_eur = course['EUR']
            course_usd = course['USD']
            data['expense'] = float(data['expense']) * course_eur / course_usd

        elif data['currency'] == "EUR" and space.currency == "BYN":
            course = exchange_rate()['EUR']
            data['expense'] = float(data['expense']) * course

        elif data['currency'] == "USD" and space.currency == "BYN":
            course = exchange_rate()['USD']
            data['expense'] = float(data['expense']) * course

        spending = Spending.objects.create(user=data['user'], space=data['space'], currency=space.currency,
                                               expense=data['expense'], category=data['category'])

        SpaceLog.objects.create(user=user, action=f'Для "{space.title}" в категорию {category.title} был внесен '
                                                  f'расход {data["expense"]} {space.currency}')

        return Response(SpendingSerializer(spending).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="get_expenses_history", url_name="get_expenses_history")
    def get_history(self, request):

        less_than = 0

        if request.data['time'] == 'day':
            less_than = datetime.datetime.now() - datetime.timedelta(days=1)
        elif request.data['time'] == 'week':
            less_than = datetime.datetime.now() - datetime.timedelta(days=7)
        elif request.data['time'] == 'month':
            less_than = time_finder(1)
        elif request.data['time'] == 'threemonths':
            less_than = time_finder(3)
        elif request.data['time'] == 'sixmonths':
            less_than = time_finder(6)
        elif request.data['time'] == 'year':
            less_than = datetime.datetime.now() - datetime.timedelta(days=365)

        space = Space.objects.get(title=request.data['space'])

        if len(request.data) == 3:
            user = CustomUser.objects.get(pk=request.data['user'])
            expenses = Spending.objects.filter(space=space, user=user, created_at__gte=less_than)
        else:
            expenses = Spending.objects.filter(space=space, created_at__gte=less_than)

        return Response(NewSpendingSerializer(expenses, many=True).data, status=status.HTTP_200_OK)


@api_view(["GET"])
def health_check(request):
    time.sleep(1)
    return Response({"status": "Ok"}, status.HTTP_200_OK)
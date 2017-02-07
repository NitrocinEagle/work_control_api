from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth, TruncDay, TruncYear
from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.permissions import NotAuthenticated
from app.time_control.models import TimeControl
from .serializers import TimeControlSerializer, UserSerializer


class Registration(CreateAPIView):
    model = User
    permission_classes = (NotAuthenticated,)
    serializer_class = UserSerializer


class StartWork(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['user'] = request.user
        if TimeControl.objects.filter(user=request.user, end__isnull=True).exists():
            message = '{}, сначала закончите работу, чтобы начать работать снова'.format(
                request.user.first_name,
                request.user.last_name
            )
            return Response(message, status=status.HTTP_428_PRECONDITION_REQUIRED)
        obj = TimeControl.objects.create(**data)
        message = '{} {}. Работа началась {}'.format(
            request.user.first_name,
            request.user.last_name,
            obj.start.strftime('%d.%m.%y в %H:%M:%S')
        )
        return Response(message, status=status.HTTP_201_CREATED)


class StoptWork(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not TimeControl.objects.filter(user=request.user, end__isnull=True).exists():
            message = '{}, чтобы закончить работу, её нужно сначала начать'.format(
                request.user.first_name,
                request.user.last_name
            )
            return Response(message, status=status.HTTP_428_PRECONDITION_REQUIRED)
        obj = TimeControl.objects.get(user=request.user, end__isnull=True)
        obj.end = now()
        obj.save()
        message = '{} {}. Работа началась {}. Закончилась в {}'.format(
            request.user.first_name,
            request.user.last_name,
            obj.start.strftime('%d.%m.%y в %H:%M:%S'),
            obj.end.strftime('%d.%m.%y в %H:%M:%S')
        )
        return Response(message, status=status.HTTP_201_CREATED)


class ReportWork(ListAPIView):
    serializer_class = TimeControlSerializer
    permission_classes = (IsAdminUser,)
    days_week = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    sort = ['d', 'm', 'y']

    def get_queryset(self):
        queryset = TimeControl.objects.all()

        sort_by = self.request.GET.get('sort_by')
        sort_by = filter(lambda x: x in self.sort, list(sort_by)) if sort_by else None

        if sort_by:
            queryset = queryset.annotate(
                d=TruncDay('start'),
                m=TruncMonth('start'),
                y=TruncYear('start')
            ).order_by(*sort_by)

        by_day_week = self.request.GET.get('by_day_week')
        by_day_week = self.days.index(by_day_week) + 1 if by_day_week in self.days_week else None

        by_day = int(self.request.GET.get('by_day', 0))
        by_day = by_day if by_day > 0 and by_day < 32 else None

        by_month = self.request.GET.get('by_month')
        by_month = self.months.index(by_month) + 1 if by_month in self.months else None

        by_year = self.request.GET.get('by_year')
        by_year = int(by_year) if by_year else None

        filters = {
            'start__week_day': by_day_week,
            'start__day': by_day,
            'start__month': by_month,
            'start__year': by_year,
        }

        # Delete empty filters (orm can't handle empty filters)
        filters = dict((k, v) for k, v in filters.items() if v)

        if filters:
            return queryset.filter(**filters)

        return queryset

import datetime

from django.db import models


currency_choices = (
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("BYN", "BYN"),
    )

class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время последнего изменения')

    class Meta:
        abstract = True


class CustomUser(BaseDateMixin):
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    telegram_id = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'

    class Meta(BaseDateMixin.Meta):
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'


class Space(BaseDateMixin):
    title = models.CharField(max_length=50, verbose_name='Название')
    currency = models.CharField(max_length=3, choices=currency_choices, verbose_name='Валюта')
    users = models.ManyToManyField(CustomUser, related_name='space', through='PersonStatus')

    @property
    def cost_amount(self):
        total = sum(obj.expense for obj in self.space_spending.all())
        return total

    def __str__(self):
        return self.title



class PersonStatus(BaseDateMixin):

    status_choices = (
        ('A', 'Admin user'),
        ('C', 'Casual user'),
        ('M', 'Master user')
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_space',
                             verbose_name='Пользователь')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='status')
    grade = models.CharField(max_length=1, choices=status_choices)
    is_banned = models.BooleanField(default=False, verbose_name='Забанен')

    def __str__(self):
        return f'{self.user} | {self.space} | {self.grade}'


class SpendingCategory(BaseDateMixin):
    title = models.CharField(max_length=30, verbose_name='Название')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='space_category')

    def __str__(self):
        return self.title

    class Meta(BaseDateMixin.Meta):
        verbose_name = 'категорию расходов'
        verbose_name_plural = 'категории расходов'


class Spending(BaseDateMixin):
    category = models.ForeignKey(SpendingCategory, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    expense = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Расход')
    currency = models.CharField(max_length=3, choices=currency_choices, verbose_name='Валюта')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='space_spending')

    def __str__(self):
        return f"{self.user} | {self.category} | {self.space} | {self.expense} {self.currency}"

    class Meta(BaseDateMixin.Meta):
        verbose_name = 'расход'
        verbose_name_plural = 'расходы'


class ReferralCode(BaseDateMixin):
    code = models.TextField(verbose_name='Реферальный код')
    expiration_time = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1),
                                           verbose_name='Время истечения')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} | {self.expiration_time}'

    class Meta(BaseDateMixin.Meta):
        verbose_name = 'релефальный код'
        verbose_name_plural = 'реферальные коды'


class SpaceLog(BaseDateMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.TextField(verbose_name='Действие')


    def __str__(self):
        return f'{self.user} | {self.action}'

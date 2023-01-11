from django.db import models


currency_choices = (
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("BYN", "BYN"),
    )

class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(BaseDateMixin):
    name = models.CharField(max_length=50)
    telegram_id = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'


class Space(BaseDateMixin):
    title = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, choices=currency_choices)
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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_space')
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='status')
    grade = models.CharField(max_length=1, choices=status_choices)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} | {self.space} | {self.grade}'


class SpendingCategory(BaseDateMixin):
    title = models.CharField(max_length=30)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='space_category')

    def __str__(self):
        return self.title


class Spending(BaseDateMixin):
    category = models.ForeignKey(SpendingCategory, on_delete=models.CASCADE)
    expense = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(max_length=3, choices=currency_choices)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='space_spending')


class ReferralCode(BaseDateMixin):
    code = models.TextField()
    expire_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.code} | {self.expire_time}'


class SpaceLog(BaseDateMixin):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.TextField()


    def __str__(self):
        return f'{self.user} | {self.action}'

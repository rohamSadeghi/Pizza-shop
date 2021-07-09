from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _

from utils.managers import ApprovedManager


class Pizza(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_("name"), max_length=50)
    price = models.PositiveIntegerField(_("price"))
    price_discount = models.PositiveIntegerField(_("price discount"), default=0)
    image = models.ImageField(_("image"), upload_to='pizzas', blank=True)
    description = models.TextField(_("description"), blank=True)
    is_enable = models.BooleanField(_('is enable'), default=True)

    class Meta:
        verbose_name = _("Pizza")
        verbose_name_plural = _("Pizzas")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rating_data = None

    def get_rating_data(self):
        if self._rating_data is None:
            self._rating_data = PizzaRate.objects.filter(pizza=self).aggregate(
                avg=Coalesce(models.Avg('rate'), 0, output_field=models.FloatField()),
                count=models.Count('id')
            )
            self._rating_data['avg'] = round(self._rating_data['avg'], 1)
        return self._rating_data

    def rating_avg(self):
        rating_data = self.get_rating_data()
        return rating_data['avg']

    def rating_count(self):
        rating_data = self.get_rating_data()
        return rating_data['count']

    def __str__(self):
        return self.name


class PizzaRate(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name='rates',
                             on_delete=models.CASCADE)
    pizza = models.ForeignKey('Pizza', verbose_name=_('pizza'), related_name='rates', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(_("rate"), validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Pizza rate")
        verbose_name_plural = _("Pizza rates")
        constraints = [
            models.UniqueConstraint(fields=['user', 'pizza'], name='unique user_pizza_rate')
        ]

    def __str__(self):
        return f"user: {str(self.user)}->pizza: {str(self.pizza)}, rate: {str(self.rate)}"


class PizzaComment(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    pizza = models.ForeignKey("Pizza", verbose_name=_("pizza"), on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name="comment_users",
                             on_delete=models.CASCADE)
    content = models.TextField(_('content'))
    approved_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name="approved_users", verbose_name=_("approved user"), editable=False)
    approved_time = models.DateTimeField(_("approved time"), blank=True, null=True, editable=False)

    objects = models.Manager()
    approves = ApprovedManager()

    def is_approved(self):
        """ This method and attribute is used in admin page for showing tick or cross """
        return bool(self.approved_user)

    is_approved.boolean = True

    class Meta:
        verbose_name = _("Pizza comment")
        verbose_name_plural = _("Pizza comments")

    def __str__(self):
        return f"user: {str(self.user)}->pizza: {str(self.pizza)}"

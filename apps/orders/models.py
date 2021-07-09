from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class OrderPizza(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), related_name="orders",
                             on_delete=models.CASCADE)
    pizza = models.ForeignKey("pizzas.Pizza", verbose_name=_("pizza"), related_name="orders", on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_("price"))
    is_paid = models.BooleanField(_('is paid'), default=False)
    description = models.TextField(_("description"), blank=True)
    is_enable = models.BooleanField(_('is enable'), default=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"user: {str(self.user)}->pizza: {str(self.pizza)}"

from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from products_app.models import Product, ProductCategory

#Asociating Payment Listeners#Asociate Listeners
from sermepa.signals import payment_was_successful
from sermepa.signals import payment_was_error
from sermepa.signals import signature_error

#Define Payment Lsiteners
def payment_ok(sender, **kwargs):
    '''sender es un objecto de clase SermepaResponse. Utiliza el campo Ds_MerchantData
    para asociarlo a tu Pedido o Carrito'''
    print 'payment ok signal initiated'
    order = Order.objects.get(pk=sender.Ds_MerchantData)
    order.status = 'pagado'
    order.auth_code = sender.Ds_AuthorisationCode #Guardar este valor en caso
    # de poder hacer devoluciones, es necesario.
    order.save()
    #Maddar emails etc ....

    print 'Order Pagado'

def payment_ko(sender, **kwargs):
    print 'payment_ko'
    order = Order.objects.get(pk=sender.Ds_MerchantData)
    order.status = 'error_pago'
    order.save()
    print 'Error pago'
    pass

def sermepa_ipn_error(sender, **kwargs):
    print 'payment ipn error'
    order = Order.objects.get(pk=sender.Ds_MerchantData)
    order.status = 'error_pago'
    order.save()
    pass

payment_was_successful.connect(payment_ok)
payment_was_error.connect(payment_ko)
signature_error.connect(sermepa_ipn_error)


#Customer Model
class Customer(models.Model):
    class Meta:
        verbose_name_plural = 'Clientes'
        verbose_name = 'Cliente'

    created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False, null = False, verbose_name = 'Creado')
    first_name = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Nombre')
    last_name = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Apellidos')
    city = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Ciudad')
    adress = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Direccion')
    phone_number = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Telefono')
    email = models.EmailField(max_length = 100, null=True, blank = True, verbose_name = 'Email')

    def __unicode__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.first_name, self.last_name)

#Modelo Consulta
class Booking(models.Model):
    class Meta:
        verbose_name_plural='Consultas'
        verbose_name='Consulta'
    created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False, null = False, verbose_name = 'Creado')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, blank = False, null = False, verbose_name = 'Actualizado')
    date_booking = models.DateTimeField(auto_now=False, auto_now_add=False, blank = False, null = False, verbose_name = 'Fecha de la Consulta')
    adress = models.CharField(max_length = 500, blank = False, null = False, verbose_name = 'Direccion')
    city = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Ciudad')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name = 'Cliente')
    customer_first_name = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Nombre')
    customer_last_name = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Apellidos')
    customer_email = models.EmailField(max_length = 100, null=True, blank = True, verbose_name = 'Email')
    customer_phone_number = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Telefono')

    def __unicode__(self):              # __unicode__ on Python 2
      return "%s|%s" % (self.city, self.date_booking )


#Pet Model
class Pet(models.Model):
    class Meta:
        verbose_name_plural='Mascotas'
        verbose_name='Mascota'

    name = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Nombre')
    species = models.CharField(max_length = 100, blank = False, null = False,verbose_name = 'Especie')
    breed = models.CharField(max_length = 100, blank = False, null = False, verbose_name = 'Raza')
    conditions = models.TextField(max_length=5000, verbose_name = 'Razon de la consulta')
    #user_customer = models.ForeignKey('UserCustomer', null=True , blank = True, verbose_name = 'Dueno')
    age = models.CharField(max_length=100, verbose_name = 'Edad')
    GENDER = (
       ('hembra_normal','Hembra Normal'),
       ('hembra_esterilizada','Hembra Esterilizada'),
       ('macho_normal','Macho Normal'),
       ('macho_esterilizado','Macho Esterilizado'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name = 'Cliente')
    gender = models.CharField(max_length=20, choices=GENDER, blank = True, null=True, verbose_name = 'Sexo' )
    booking = models.ForeignKey(Booking, blank =True, null = True, verbose_name = 'Mascota')

    def __unicode__(self):              # __unicode__ on Python 2
      return "%s %s" % (self.name, self.breed)

class Order(models.Model):
    class Meta:
        verbose_name_plural = 'Pedidos'
        verbose_name = 'Pedido'
    auth_code = models.CharField(max_length = 100, null=True, blank = True, verbose_name = 'Authorization Code')
    ref_code = models.CharField(max_length = 100, null=False, blank = True, verbose_name = 'Codigo de referencia')
    created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False, null = False, verbose_name = 'Creado')
    ORDER_STATUSES = (
       ('pagado','Pagado'),
       ('pendiente','Pendiente'),
       ('error_pago','Error de Pago'),
    )
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, blank = True, null=True, verbose_name = 'Estatus del pedido' )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name = 'Cliente')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name = 'Reserva Relacionada')

    def __unicode__(self):              # __unicode__ on Python 2
      return "%s|%s" % (self.ref_code, self.status )

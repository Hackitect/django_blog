from django.db import models

from mpesa_api.util.managers import AuthTokenManager


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


# Mpesa Payment models

class MpesaCalls(BaseModel):
	ip_address = models.TextField()
	caller = models.TextField()
	conversation_id = models.TextField()
	content = models.TextField()

	class Meta:
		verbose_name = 'Mpesa Call'
		verbose_name_plural = 'Mpesa Calls'

class MpesaCallBacks(BaseModel):
	ip_address = models.TextField()
	caller = models.TextField()
	conversation_id = models.TextField()
	content = models.TextField()

	class Meta:
		verbose_name = 'Mpesa Call Back'
		verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField()
	type = models.TextField()
	reference = models.TextField()
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=10)
	organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
	
	class Meta:
		verbose_name = 'Mpesa Payment'
		verbose_name_plural = 'Mpesa Payments'
	
	def __str__(self):
		return self.first_name


class AuthToken(models.Model):
	access_token = models.CharField(max_length=40)
	type = models.CharField(max_length=3)
	expires_in = models.BigIntegerField()
	objects = AuthTokenManager()

	def __str__(self):
		return self.access_token

	class Meta:
		db_table = 'tbl_access_token'

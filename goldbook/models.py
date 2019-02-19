from django.db import models

class GoldenMessage(models.Model):
	name = models.CharField(max_length=100)
	message = models.TextField(null=True)
	rate = models.IntegerField(default=0)

	class Meta:
		verbose_name = "golden message"
		ordering = ['pk']

	def __str__(self):
		return self.message
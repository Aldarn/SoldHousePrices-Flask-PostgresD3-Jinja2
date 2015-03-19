from django.db import models

class SoldProperty(models.Model):
	uid = models.CharField(max_length = 36, primary_key = True)
	price = models.IntegerField()
	date = models.IntegerField()
	postCode = models.CharField(max_length = 8)
	type = models.CharField(max_length = 1)
	isOld = models.BooleanField()
	duration = models.CharField(max_length = 1)
	paon = models.CharField(max_length = 255) # Could it go above this?
	saon = models.CharField(max_length = 255) # Could it go above this?
	street = models.CharField(max_length = 255) # Could it go above this?
	locality = models.CharField(max_length = 255) # Could it go above this?
	town = models.CharField(max_length = 255) # Could it go above this?
	district = models.CharField(max_length = 255) # Could it go above this?
	county = models.CharField(max_length = 255) # Could it go above this?

	def __unicode__(self):
		return self.question
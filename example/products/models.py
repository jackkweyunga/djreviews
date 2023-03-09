from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from djreviews.models import BaseReviewModel, BaseReviewedModel


# Create your models here.

class Customer(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=20)


class ProductReview(BaseReviewModel):
    """
    Product Reviews
    """


class Product(BaseReviewedModel):
    name = models.CharField(max_length=20)
    description = models.TextField()
    objects = models.Manager()

    # important
    REVIEW_MODEL = ProductReview

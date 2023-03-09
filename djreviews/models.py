from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ReviewManager(models.Manager):

    def add_review(self, content, rating, reviewer_object, reviewed_object, **kwargs):
        """
        Add a new review.

        :param reviewed_object: Object being reviewed
        :param reviewer_object: Object making the review
        :param content: review string
        :param rating: rating int value
        :param kwargs: additional model fields.
        :return: BaseReviewModel or the Custom Review Model
        """

        return self.create(
            content=content,
            rating=rating,
            reviewer_object=reviewer_object,
            reviewed_object=reviewed_object,
            **kwargs
        )


class BaseReviewModel(models.Model):
    """
    Basic review fields and functionalities.
    Should be extended bu inheriting this model class.
    After which more fields can ba added to it.

    Attributes
        reviewer_object The object making the review.
        reviewed_object The object being reviewed.
    """

    rating = models.SmallIntegerField(default=0)
    content = models.TextField()
    objects = ReviewManager()

    # reviewer
    # the object making a review.
    reviewer_content_type = models.ForeignKey(ContentType, related_name="reviewed", on_delete=models.CASCADE)
    reviewer_object_id = models.PositiveIntegerField()
    reviewer_object = GenericForeignKey('reviewer_content_type', 'reviewer_object_id')

    # reviewed
    # the object being reviewed
    reviewed_content_type = models.ForeignKey(ContentType, related_name="reviews", on_delete=models.CASCADE)
    reviewed_object_id = models.PositiveIntegerField()
    reviewed_object = GenericForeignKey('reviewed_content_type', 'reviewed_object_id')

    class Meta:
        abstract = True


class BaseReviewedModel(models.Model):
    REVIEW_MODEL: BaseReviewModel = None

    def __init__(self, *args, **kwargs):
        if self.REVIEW_MODEL is None:
            raise ValueError(
                f"attribute REVIEW_MODEL is None in the model `{self._meta.model_name}`. Set it to solve this error.")
        super(BaseReviewedModel, self).__init__(*args, **kwargs)

    @property
    def reviews(self):
        content_type = ContentType.objects.get_for_model(self)
        return self.REVIEW_MODEL.objects.filter(
            reviewed_content_type=content_type, reviewed_object_id=self.id).all()

    def add_review(self, content, rating, reviewer, **kwargs):
        return self.REVIEW_MODEL.objects.add_review(
            content=content,
            rating=rating,
            reviewer_object=reviewer,
            reviewed_object=self,
            **kwargs
        )

    class Meta:
        abstract = True

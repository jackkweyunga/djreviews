# DJANGO REVIEWS & RATING

Add reviews and ratings functionalities to your dango app.

## Installation

```shell
pip install djreviews
```

## Usage

Extending functionality in models

```python
from django.db import models
from djreviews.models import BaseReviewModel, BaseReviewedModel


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

```

usage in views

```python


product = Product.objects.get(pk=product_pk)
customer = Customer.objects.get(pk=customer_pk)

product.add_review(
    content=review_text,
    rating=rating_score,
    reviewer=customer,
)

# OR

ProductReview.objects.add_review(
    content=review_text,
    rating=rating_score,
    reviewed_object=product,
    reviewer_object=customer,
)


```

in templates

```html

{% for review in object.reviews.all|dictsortreversed:"id" %}
<div>
    <p>{{ review.reviewer }}</p>
    <p>rating: {{ review.rating }}</p>
    <p>review: {{ review.content }}</p>
</div>
{% empty %}
<p>No reviews</p>
{% endfor %}

```
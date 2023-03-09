from django.urls import path
from .views import ProductDetails, ProductReviewForm

urlpatterns = [
    path("<pk>/", ProductDetails.as_view(), name="product_details"),
    path("<product_pk>/<customer_pk>", ProductReviewForm.as_view(), name="product_review_add")
]

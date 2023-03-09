from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic, View
from django.shortcuts import redirect

from .models import Product, Customer


# Create your views here.

class ProductDetails(generic.DetailView):
    model = Product
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        print(self.get_object().reviews.all())
        return super(ProductDetails, self).get(request, *args, **kwargs)


class ProductReviewForm(View):

    def post(self, request, product_pk, customer_pk):
        data = self.request.POST.copy()

        review_text = data.get("review_text", None)
        rating_score = data.get("rating_score", None)

        product = Product.objects.get(pk=product_pk)
        customer = Customer.objects.get(pk=customer_pk)

        product.add_review(
            content=review_text,
            rating=rating_score,
            reviewer=customer,
        )

        messages.success(self.request, "Review submitted successfully")

        return redirect(reverse_lazy("product_details", args=[product_pk]))

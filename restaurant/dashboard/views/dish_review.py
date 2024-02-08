from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView

from .. import forms
from .. import models


class DishReviewCreateView(LoginRequiredMixin, CreateView):
    model = models.DishReview
    fields = "__all__"
    template_name = "dashboard/dish_review/dish_review_create.html"
    success_url = reverse_lazy("dashboard:menu")

    def get(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        form = forms.DishReviewForm(initial={"dish": dish})
        return render(request, self.template_name, {"form": form, "dish": dish})

    def post(self, request: HttpRequest, pk: int):
        dish = models.Dish.objects.get(pk=pk)
        form = forms.DishReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("dashboard:menu"))
        return render(request, self.template_name, {"form": form, "dish": dish})


class DishReviewListView(ListView):
    model = models.DishReview
    template_name = "dashboard/dish_review/dish_reviews_list.html"
    context_object_name = "reviews"


class DishReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.DishReview
    template_name = "dashboard/dish_review/dish_review_delete.html"
    permission_required = "dashboard.delete_dishreview"
    success_url = reverse_lazy("dashboard:reviews")

    def get(self, request: HttpRequest, pk: int):
        review = models.DishReview.objects.get(pk=pk)
        return render(request, self.template_name, {"review": review})

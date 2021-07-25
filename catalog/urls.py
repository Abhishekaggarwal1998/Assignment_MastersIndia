from django.urls import path

from catalog.views import CategoryListAPIView, SubCategoryListAPIView, ProductListAPIView


urlpatterns = [

    path(r'category/', CategoryListAPIView.as_view(), name="category-list"),
    path(r'sub-category/', SubCategoryListAPIView.as_view(), name="sub-category-list"),
    path(r'product/', ProductListAPIView.as_view(), name="product-list"),
]

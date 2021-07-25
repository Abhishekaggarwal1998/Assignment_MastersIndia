from django.db.models import QuerySet, Q
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Optional
from catalog.models import Category, SubCategory, Product
from catalog.serializers import CategorySerializer, SubCategorySerializer, ProductCreateRequestSerializer


class CategoryListAPIView(ListAPIView):
    """
    listed categories.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class SubCategoryListAPIView(ListAPIView):
    """
    listed sub categories.
    """
    queryset = SubCategory.objects.all().order_by('name')
    serializer_class = SubCategorySerializer


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateRequestSerializer

    def get_queryset(self):
        queryset: QuerySet[Product] = super(ProductListAPIView, self).get_queryset()
        lookup_params: Dict = {}
        sub_category_id: Optional[int] = self.request.GET.get('sub_category_id', None)
        if sub_category_id: lookup_params.update({'sub_category_id': sub_category_id})
        category_id: Optional[int] = self.request.GET.get('category_id', None)
        if category_id: lookup_params.update({'sub_category__category_id': category_id})
        filters = Q()
        for item in lookup_params:
            filters |= Q(**{item: lookup_params[item]})
        return queryset.filter(filters)

    def post(self, request, *args, **kwargs):
        serializer: ProductCreateRequestSerializer = ProductCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'msg': 'Product has been created successfully'}, status=status.HTTP_200_OK)

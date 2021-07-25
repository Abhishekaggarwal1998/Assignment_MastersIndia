from typing import Optional
from rest_framework import serializers
from catalog.models import Category, SubCategory, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Serialize category objects.
    """
    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Serialize sub-category objects.
    """
    class Meta:
        model = SubCategory
        fields = "__all__"


def validate_category(category_id):
    if category_id:
        if not Category.objects.filter(id=category_id):
            raise serializers.ValidationError('Invalid category id')
        if not SubCategory.objects.filter(category_id=category_id):
            raise serializers.ValidationError('Category does not have any SubCategory')


class ProductCreateRequestSerializer(serializers.ModelSerializer):
    """
    Product serializer to create and list view
    """
    category = serializers.IntegerField(required=False, allow_null=True, validators=[validate_category])

    def validate(self, attrs):
        # validating if either category or subcategory has been provided in request or not
        if not attrs.get('category') and not attrs.get('sub_category'):
            raise serializers.ValidationError('Either sub_category_id or category_id is required')
        return super(ProductCreateRequestSerializer, self).validate(attrs)

    def save(self, **kwargs):
        if self.validated_data.get('sub_category'):
            # if validated sub_category is provided, then save the object
            return super(ProductCreateRequestSerializer, self).save()
        else:
            # if validated category is provided, first find sub_category and save the object
            sub_category_obj: Optional[SubCategory] = SubCategory.objects.filter(category_id=self.validated_data.pop('category')).first()
            if sub_category_obj:
                self.validated_data['sub_category']: SubCategory = sub_category_obj
                return super(ProductCreateRequestSerializer, self).save()
        raise serializers.ValidationError('Invalid request')

    class Meta:
        model = Product
        fields = "__all__"

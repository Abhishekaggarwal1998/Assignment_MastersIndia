from django.db import models


class Category(models.Model):
    """
    Category model stored all categories.
    """
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = models.TextField(help_text="Category description", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        """
        :return: It return category slug.
        """
        return self.slug


class SubCategory(models.Model):
    """
    Sub Category model stored all sub categories with parent category.
    """
    category = models.ForeignKey(Category, null=True, blank=True, related_name="main_category", on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    description = models.TextField(help_text="Category description", null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        """
        :return: It return sub-category name.
        """
        return self.slug


class Product(models.Model):
    """
    Product model stores product information of product
    """
    title = models.CharField(max_length=220, default="Default product")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    sub_category = models.ForeignKey("SubCategory", null=True, blank=True, on_delete=models.CASCADE)
    cost = models.IntegerField(default=10)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        """
        :return: It return product name.
        """
        return self.slug

from rest_framework import serializers

from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'image',
            'thumbnail',
        )

    def get_category(self, obj):
        return obj.category.name

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return ''

    def get_thumbnail(self, obj):
        request = self.context.get('request')
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return ''


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'products'
        )

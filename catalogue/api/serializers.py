from rest_framework import serializers

from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'vendor', 'category', 'tag_final_price']

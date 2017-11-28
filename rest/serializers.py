from rest_framework import serializers
from user.models import CustomUser
from .models import Dinner, IngredientType, Ingredient
from enkelmiddag import settings

class UserSerializer(serializers.ModelSerializer):

    #answers = serializers.PrimaryKeyRelatedField(many=True, queryset=ChecklistAnswer.objects.all())

    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class IngredientSerializer(serializers.ModelSerializer):

    dinner_id = serializers.PrimaryKeyRelatedField(queryset=Dinner.objects.all(), source='dinner.pk')
    type = serializers.PrimaryKeyRelatedField(queryset=IngredientType.objects.all(), source='type.name')
    type_id = serializers.PrimaryKeyRelatedField(queryset=IngredientType.objects.all(), source='type.pk')
    #image_ing = serializers.PrimaryKeyRelatedField(queryset=IngredientType.objects.all(), source='type.image')
    image_url = serializers.SerializerMethodField()
    class Meta:

        model = Ingredient
        fields = ('dinner_id', 'type', 'type_id', 'amount', 'annotation', 'image_url')

    def get_image_url(self, obj):
        #return self.context['request'].build_absolute_uri(obj.type.image)
        return '%s%s' % (settings.MEDIA_URL, obj.type.image)


class IngredientTypeSerializer(serializers.ModelSerializer):

    ingredients = IngredientSerializer(many=True)
    class Meta:

        model = IngredientType
        fields = ('name', 'image', 'ingredients')

class DinnerSerializer(serializers.ModelSerializer):

    ingredients = IngredientSerializer(many=True)
    #image_url = serializers.SerializerMethodField()

    class Meta:

        model = Dinner
        fields = ('pk', 'name', 'type', 'recipe', 'image', 'ingredients')

    #def get_image_url(self, dinner):
     #   request = self.context.get('request')
      #  image_url = dinner.image.url
       # return request.build_absolute_uri(image_url)
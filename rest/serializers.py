from rest_framework import serializers
from user.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    #answers = serializers.PrimaryKeyRelatedField(many=True, queryset=ChecklistAnswer.objects.all())

    class Meta:
        model = CustomUser
        fields = ('id', 'email')
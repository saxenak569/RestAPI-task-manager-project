from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[('basic_user', 'Basic User'), ('admin', 'Admin')],
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        # extra_kwargs = {
        #     'username': {'example': 'shiv'},
        #     'password': {'example': 'shiv123'},
        #     'role': {'example': 'user'}
        # }

    def create(self, validated_data):
        role = validated_data.pop('role')

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        # Only allow admin role if current user is already staff
        request = self.context.get('request')

        if role == 'admin' and request and request.user.is_staff:
            user.is_staff = True
            user.save()

        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
        # extra_kwargs = {
        #     'title': {'example': 'Bulding ToDo'},
        #     'description': {'example': 'Document REST API'},
        #     'completed': {'example': False},
        # }
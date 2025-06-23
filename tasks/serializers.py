from rest_framework import serializers

from .models import Task, Status


class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    status = serializers.ChoiceField(
        choices=Status.choices(), default=Status.TODO.value
    )
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Task(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

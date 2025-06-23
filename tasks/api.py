from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Task, Status
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound()
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"])
    def partial(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def summary(self, request):

        pipeline = [
            {
                "$group": {
                    "_id": "$status",
                    "total": {"$sum": 1},
                }
            }
        ]

        aggregation_result = list(Task.objects.aggregate(pipeline))

        summary_data = {}
        for item in aggregation_result:
            status_value = item["_id"]
            try:
                status_name = Status(status_value).name.title().replace("_", " ")
            except ValueError:
                status_name = f"Unknown Status ({status_value})"

            summary_data[status_name] = item["total"]

        for status_enum in Status:
            status_name = status_enum.name.title().replace("_", " ")
            if status_name not in summary_data:
                summary_data[status_name] = 0

        return Response(summary_data, status=status.HTTP_200_OK)

from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

# создать GET


class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# просмотр списка GET


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]

    def get_queryset(self):
        # Если пользователь модератор, возвращаем все уроки
        if self.request.user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()

        # Если пользователь не модератор, возвращаем только уроки, созданные им
        return Lesson.objects.filter(owner=self.request.user)

# просмотр деталей одного объекта GET


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]
    lookup_field = 'pk'

# удаление объекта


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]
    lookup_field = 'pk'

# обновление объекта


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]
    lookup_field = 'pk'

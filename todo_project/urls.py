from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from todo.views import TaskViewSet, SubtaskViewSet, CommentViewSet, ActivityLogViewSet

# 1) Base router for top‐level endpoints
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'subtasks', SubtaskViewSet, basename='subtask')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'logs', ActivityLogViewSet, basename='activitylog')

# 2) Nested router: /tasks/{task_pk}/subtasks/
tasks_router = NestedSimpleRouter(router, r'tasks', lookup='task')
tasks_router.register(
    r'subtasks',
    SubtaskViewSet,
    basename='task-subtasks'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # All app endpoints under /api/
    path('api/', include(router.urls)),
    path('api/', include(tasks_router.urls)),
]

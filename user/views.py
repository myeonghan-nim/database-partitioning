from django.http import JsonResponse

from .models import UserActivity


def create_activity(request):
    activity = UserActivity.objects.create(user_id=1, action="User logged in")
    return JsonResponse({"message": "Activity created", "id": activity.id})


def get_activity(request, activity_id):
    try:
        activity = UserActivity.objects.get(id=activity_id)
        return JsonResponse({"user_id": activity.user_id, "action": activity.action, "created_at": activity.created_at})
    except UserActivity.DoesNotExist:
        return JsonResponse({"message": "Activity not found"}, status=404)


def update_activity(request, activity_id):
    try:
        activity = UserActivity.objects.get(id=activity_id)
        activity.action = "User updated profile"
        activity.save()
        return JsonResponse({"message": "Activity updated"})
    except UserActivity.DoesNotExist:
        return JsonResponse({"message": "Activity not found"}, status=404)


def delete_activity(request, activity_id):
    try:
        activity = UserActivity.objects.get(id=activity_id)
        activity.delete()
        return JsonResponse({"message": "Activity deleted"})
    except UserActivity.DoesNotExist:
        return JsonResponse({"message": "Activity not found"}, status=404)

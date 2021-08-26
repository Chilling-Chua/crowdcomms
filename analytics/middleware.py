from .models import UserVisit


class UserVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # it's not completely clear if the analytics should show anonymous users or only
        # authenticated
        if request.user.is_authenticated:
            analytics_user, created = UserVisit.objects.get_or_create(
                user_id=request.user.pk
            )
            analytics_user.visits += 1
            analytics_user.save()
        response = self.get_response(request)

        return response

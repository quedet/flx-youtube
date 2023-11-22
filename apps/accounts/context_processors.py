from apps.accounts.models import User


def user_followings(request):
    user = getattr(request, 'user', None)
    email = getattr(user, 'email', None)

    try:
        user = User.objects.get(email=email)
        followings = user.followings.all()

    except User.DoesNotExist:
        followings = None

    return {
        'followings': followings
    }

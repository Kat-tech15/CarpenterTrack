from .models import Contact
def unread_messages_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        count = Contact.objects.filter(is_read=False).count()
    else:
        count = 0
    return {'admin_unread_count': count}

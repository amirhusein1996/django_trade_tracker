from django.utils.timezone import timezone

def get_past_time_delta(**kwargs):
    return timezone.now() - timezone.timedelta(**kwargs)

def is_expired (created_date,**kwargs):
    if timezone.now() - created_date <= timezone.timedelta(**kwargs):
        return True
    return False





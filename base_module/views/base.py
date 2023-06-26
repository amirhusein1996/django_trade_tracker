from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt , csrf_protect
from django.views.decorators.http import require_GET, require_POST , require_http_methods

#redirect / url to /home/
@require_GET
@login_required
def reditector(request):
    return redirect(reverse('home:index'))

@require_GET
@login_required
def get_home_and_manage_urls(request):
    import json
    from django.http import JsonResponse
    from django.urls import NoReverseMatch
    from home_module.urls import app_name as home_app_name
    from manage_module.urls import app_name as manage_app_name


    view_name_list = json.loads(list(request.GET)[0])

    result_dict = dict()
    for view_name in view_name_list:
        try:
            url_match = reverse(home_app_name + ':' + view_name)
            result_dict[view_name] = url_match
        except NoReverseMatch:
            url_match = reverse(manage_app_name + ':' + view_name)
            result_dict[view_name] = url_match
        except:
            pass

    return JsonResponse({'result':json.dumps(result_dict)})
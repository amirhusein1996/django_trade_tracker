from django.http import Http404 , JsonResponse



class JsonDeleteViewMixin :

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return JsonResponse({'message': True})

class JsonUpdateViewMixin:
    def form_valid(self, form):
        form.save()
        return JsonResponse({'message':True})

    def form_invalid(self, form):
        errors = [error.as_text() for error in form.errors.values()]
        return JsonResponse({'message': "\n".join(errors)})
from django.shortcuts import redirect , reverse ,get_object_or_404 , Http404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  ListView , UpdateView ,FormView ,DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt , csrf_protect
from django.views.decorators.http import require_GET, require_POST , require_http_methods
from .models import  TradeAccount  , MoreInfo
from .forms import TradeAccountModelForm , IsActiveModelForm
from base_module.views.mixin.json import JsonUpdateViewMixin , JsonDeleteViewMixin
from base_module.views.mixin.http import HttpListViewMixin


@method_decorator(require_GET, name='dispatch')
@method_decorator(login_required, name='dispatch')
class TradeAccountManagement(HttpListViewMixin , ListView):
    template_name = 'manage_module/trade_account_management.html'
    model = TradeAccount
    ordering = 'title'
    context_object_name = 'trade_accounts'
    paginate_by = 10
    paginate_orphans = 1

    def get_queryset(self,*args , **kwargs):
        print('query')
        query = super().get_queryset(*args , **kwargs)
        query : TradeAccount = query.filter(user_id=self.request.user.pk ).select_related('more_info')
        return query

    def render_to_response(self, context, **response_kwargs):
        trade_accounts = context['trade_accounts']
        if not trade_accounts:
            # if there's no trade account , it will redirect user to home page
            return redirect(reverse("home:index"))
        return super().render_to_response(context, **response_kwargs)

# @method_decorator(require_http_methods(['GET' , 'POST']), name='dispatch')
@method_decorator(login_required, name='dispatch')
class UpdateTradeAccount(JsonUpdateViewMixin,UpdateView):
    form_class = TradeAccountModelForm
    model = MoreInfo

    def get_object(self, queryset=None):
        from django.utils.text import slugify
        user_id = self.request.user.pk
        slug = self.request.POST.get('slug') if self.request.method == "POST" else slugify(self.request.GET.get('title'))

        if not slug:
            raise Http404("Trade Account doesnt exist or already exist with same title")
        try:
            print(user_id, ' :user')
            return self.model.objects.select_related('tradeaccount').get(tradeaccount__slug=slug,tradeaccount__user_id=user_id,)
        except:
            raise Http404("Trade Account doesnt exist or already exist with same title")

    def get(self,request ):
        more_info_obj=self.get_object()
        main_model_obj = more_info_obj.tradeaccount
        form = self.form_class(instance=more_info_obj,initial={'title':main_model_obj.title,'slug':main_model_obj.slug})
        return JsonResponse({'form':str(form.as_div())})

    def form_valid(self, form):
        title = form.cleaned_data['title']
        more_info_obj = form.save(commit=False)
        trade_account = more_info_obj.tradeaccount
        does_title_exist =TradeAccount.objects.exclude(id=trade_account.id).filter(title__iexact=title,user_id=self.request.user.pk).exists()
        if does_title_exist :
            return JsonResponse({'error':"An Acoount with same title already exists"}, status=400)
        form.save()
        trade_account.title = title
        trade_account.save()
        return JsonResponse({'message': True})

@method_decorator(require_http_methods(['GET' , 'POST']), name='dispatch')
@method_decorator(login_required, name='dispatch')
class CreateNewTradeAccountFormView(FormView):
    form_class = TradeAccountModelForm
    model = TradeAccount

    def form_valid(self, form):
        user_id = self.request.user.pk
        title = form.cleaned_data.get('title')
        is_trade_account = self.model.objects.filter(user_id=user_id,
                                                       title__iexact=title, is_active=True).exists()
        if not is_trade_account:
            more_info = form.save(commit=True)
            trade_account = self.model(title=title, more_info=more_info, user_id=user_id)
            trade_account.save()

            return JsonResponse({'message': True,'newButtonTitle':title, 'newButtonSlug':trade_account.slug})
        return JsonResponse({'message': "This Title Already Exists!"})

    def form_invalid(self, form):
        errors = [ value.as_text() for value in form.errors.values()]
        return JsonResponse({'message':"\n".join(errors)})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get(self,request):
        form = self.get_form()
        context = self.get_context_data(form=form)
        form_html = context['form'].as_div()
        return JsonResponse({'form': str(form_html)})

    def post(self,request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

@method_decorator(require_POST, name='dispatch')
@method_decorator(login_required, name='dispatch')
class IsActive(JsonUpdateViewMixin , UpdateView):
    model = TradeAccount
    form_class = IsActiveModelForm

    def get_object(self, queryset=None):
        from django.utils.text import slugify
        slug = slugify( self.request.POST.get('account_name') )
        user_id = self.request.user.pk
        return get_object_or_404(self.model ,slug__iexact=slug , user_id=user_id)

@method_decorator(require_POST, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class IsDelete (JsonDeleteViewMixin ,  DeleteView):
    model = TradeAccount

    def get_object(self, queryset=None):
        from django.utils.text import slugify
        title = self.request.POST.get('account_name')
        slug =slugify( title )
        user_id = self.request.user.pk
        return get_object_or_404(self.model, user_id=user_id, slug__iexact=slug)

from django.shortcuts import render  ,get_object_or_404 , Http404
from django.http import JsonResponse
from django.views.generic import View , ListView , UpdateView , CreateView ,DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST , require_http_methods
from .models import TradeRecord ,TradeAccount , TimeInterval ,CurrencyType
from .forms import ( TradeRecordModelForm ,UpdateNoteModelForm)
from base_module.views.mixin.json import JsonDeleteViewMixin  , JsonUpdateViewMixin
from base_module.views.mixin.http import HttpListViewMixin



@require_GET
@login_required
def index(request):
    user_id = request.user.pk
    active_accounts_by_user = TradeAccount.objects.filter(user_id=user_id, is_active=True).all()
    total_accounts_count_by_user = TradeAccount.objects.filter(user_id=user_id).count()
    time_interval = TimeInterval.objects.order_by("order_index")
    currency_types = CurrencyType.objects.order_by("order_index")
    context = {
        'total_account_count': total_accounts_count_by_user,
        'accounts': active_accounts_by_user,
        'time_interval': time_interval,
        'currency_types': currency_types,
    }
    return render(request, 'home_module/index.html', context)

@method_decorator(require_GET, name='dispatch')
@method_decorator(login_required, name='dispatch')
class TradeListAjax(HttpListViewMixin , ListView):
    model = TradeRecord
    template_name = 'home_module/components/_trading_list.html'
    context_object_name = 'trades'
    paginate_by = 5
    ordering = '-time',

    def get_queryset(self, *args, **kwargs ):
        user_id = self.request.user.pk
        time_selected = self.request.GET.get('time_selected')
        account_name = self.request.GET.get('account_name')

        queryset = super().get_queryset(*args, **kwargs).select_related('currency_type').filter(
            trade_account__user_id=user_id ,
            trade_account__slug__iexact=account_name ,
            trade_account__is_active=True
        )
        return self._query_time_filter(queryset,time_selected)

    def render_to_response(self, context, **response_kwargs):
        from django.template.loader import render_to_string
        html = render_to_string(self.template_name ,context , request=self.request)
        pagination = render_to_string('shared/components/_paginaton.html', context, request=self.request)
        return JsonResponse({'html' : html ,'pagination': pagination})

    def _query_time_filter(self , queryset = None , time_selected : str = 'all'):
        from utils.time import get_past_time_delta
        from django.utils.timezone import localdate

        if time_selected == 'one-hour':
            return queryset.filter(time__gte=get_past_time_delta(hours=1) )
        elif time_selected == 'four-hours':
            return queryset.filter(time__gte=get_past_time_delta(hours=4) )
        elif time_selected == 'daily':
            return queryset.filter(time__date__gte=localdate() )
        elif time_selected == 'weekly':
            return queryset.filter(time__gte=get_past_time_delta(weeks=1) )
        elif time_selected == 'monthly':
            return queryset.filter(time__gte=get_past_time_delta(days=30) )
        elif time_selected == 'six-month':
            return queryset.filter(time__gte=get_past_time_delta(days=183) )
        elif time_selected == 'yearly':
            return queryset.filter(time__gte=get_past_time_delta(days=365) )
        # 'all' ond other undefined time_selected are returned to avoid raising error
        return queryset



@method_decorator(require_GET, name='dispatch')
@method_decorator(login_required, name='dispatch')
class TradeOverviewAjax(View):
    model = TradeAccount

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return JsonResponse(context)

    def get_context_data(self):
        from django.db.models import Sum

        trade_account = self.get_object()
        more_info = trade_account.more_info
        trade_records = trade_account.traderecord_set

        self._risk = trade_records.filter(profit__lt=0).aggregate(Sum('profit'))['profit__sum'] or 0
        self._reward = trade_records.filter(profit__gt=0).aggregate(Sum('profit'))['profit__sum'] or 0

        context = self._get_detail_stat_context(more_info, trade_records, Sum)
        context.update(self._get_trading_objectives_context(more_info, trade_records, Sum))
        return context

    def get_object(self):
        from django.db.models import Prefetch
        from django.core.exceptions import ObjectDoesNotExist

        account_name = self.request.GET.get('account_name')
        user_id = self.request.user.pk

        try:
            # Filter trade accounts and prefetch related objects
            return self.model.objects.select_related('more_info').prefetch_related(
                Prefetch('traderecord_set', queryset=TradeRecord.objects.order_by('time'))
            ).get(
                user_id=user_id,
                slug__iexact=account_name,
                is_active=True
            )
        except :
            raise Http404()


    def _get_detail_stat_context(self, more_info, trade_records , Sum):
        total_win_count = trade_records.filter(profit__gt=0).count()
        total_lose_count = trade_records.filter(profit__lt=0).count()
        total_trades = total_win_count + total_lose_count

        risk = self._risk
        reward = self._reward

        detail_stat = {
            'equity': more_info.balance + risk + reward,
            'balance': more_info.balance,
            'avg_win': reward / total_win_count if total_win_count else 0,
            'avg_lose': risk / total_lose_count if total_lose_count else 0,
            'total_trades': total_trades,
            'r_r': abs(reward / risk) if risk else 0,
            'win_rate': (total_win_count / total_trades) * 100 if total_trades else 0,
        }

        return {'detail_stat': detail_stat}

    def _get_trading_objectives_context(self, more_info, trade_records , Sum):
        from django.utils import timezone
        daily_max_loss_record = trade_records.filter(
            time__date=timezone.localdate(),
            profit__lt=0
        ).aggregate(Sum('profit'))['profit__sum'] or 0

        risk = self._risk
        reward = self._reward

        trading_objectives = {
                'minimum_trading_days': more_info.minimum_trading_days,
                'days_traded': more_info.days_traded or 0,
                'daily_loss_limit':abs(more_info.daily_loss_limit)*(-1) ,
                'daily_max_loss_record' : abs(daily_max_loss_record)*(-1) or 0,
                'overal_loss_limit': abs(more_info.overal_loss_limit)*(-1) ,
                'max_loss_record': risk or 0,
                'profit_target' : more_info.profit_target,
                'current_profit': (reward + risk) or 0,
            }
        return {'trading_objectives' : trading_objectives}

@method_decorator(require_POST, name='dispatch')
@method_decorator(login_required , name='dispatch')
class TradeRecordCreateView(CreateView):
    form_class =TradeRecordModelForm
    model = TradeRecord

    def form_valid(self, form):
        slug = form.cleaned_data['account_name']
        currency_name = form.cleaned_data['currency_name']
        user_id = self.request.user.pk
        new_record = form.save(commit=False)
        # try:
        trade_account = TradeAccount.objects.get(slug__iexact=slug, user_id=user_id,is_active=True)
        print(trade_account)
        currency_type = CurrencyType.objects.get(currency_name__iexact=currency_name)
        print(currency_type)

        new_record.trade_account = trade_account
        new_record.currency_type = currency_type
        new_record.save()
        return JsonResponse({'message': True})
        # except:
        #     raise Http404('Related account doesn\'t exist or is not allowed')

    def form_invalid(self, form):
        errors = [error.as_text() for error in form.errors.values()]
        return JsonResponse({'message': "\n".join(errors)})

@method_decorator(require_GET, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DownloadTradeChartView(View):
    model = TradeAccount

    def get(self, request , *args , **kwargs):
        from django.utils.crypto import get_random_string

        trade_account = self.get_object()
        balance = trade_account.more_info.balance
        trade_records = trade_account.traderecord_set.all()

        if len(trade_records) == 0:
            raise Http404('There\'s no Record to download' )

        response = self._generate_chart(balance=balance , trade_records=trade_records)
        file_name = trade_account.title + '_' + get_random_string(12)
        response['Content-Disposition'] = f'attachment; filename={file_name}.png'
        return response

    def get_object(self):
        from django.db.models import Prefetch
        slug: str = self.request.GET.get('slug')
        user_id = self.request.user.pk

        try:
            return self.model.objects.select_related('more_info').prefetch_related(
                Prefetch("traderecord_set",queryset=TradeRecord.objects.order_by("time") )
            ).get(user_id=user_id, slug__iexact=slug, is_active=True)

        except:
            raise Http404()

    def _equity_list(self , balance: float, profit_list: list):
        equity = [balance]
        for profit in profit_list:
            equity.append(equity[-1] + profit)
        return equity

    def _generate_chart(self, balance, trade_records):
        from django.http import HttpResponse
        import plotly.graph_objects as go
        # import matplotlib
        # matplotlib.use('Agg')
        # import matplotlib.pyplot as plt
        from io import BytesIO
        import numpy
        profits = [float(record.profit) for record in trade_records]
        # Generate the chart
        equity = numpy.array(self._equity_list(balance=balance, profit_list=profits))
        x = numpy.array(numpy.arange(len(equity)))

        # #matplotlib
        # fig, ax = plt.subplots(figsize=(25, 15))
        # plt.plot(x,equity)
        # plt.title('Trade Chart')
        # plt.ylabel('Equity')
        # # Save the chart as a PNG image in memory
        # buffer = BytesIO()
        # plt.savefig(buffer, format='png')
        # buffer.seek(0)

        # Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=equity, mode='lines'))
        fig.update_layout(title='Trade Chart', yaxis_title='Equity', width=1680, height=1050)

        # Save the chart as a PNG image in memory
        buffer = BytesIO()
        fig.write_image(buffer, format='png')
        buffer.seek(0)

        # Return the chart as a response
        response = HttpResponse(buffer, content_type='image/png')
        return response




# @method_decorator(require_http_methods([ 'GET' , 'POST' ]), name='dispatch')
@method_decorator(login_required, name='dispatch')
class UpdateNoteUpdateView(JsonUpdateViewMixin ,  UpdateView):
    model = TradeRecord
    form_class = UpdateNoteModelForm

    def get_object(self, queryset=None):
        id = self.request.POST.get('id') if self.request.method == 'POST' else self.request.GET.get('id')
        user_id = self.request.user.id
        # check GET and POST data for slug
        slug = self.request.GET.get('account_name') or self.request.POST.get('account_name')
        return get_object_or_404(self.model, id=id , trade_account__user_id=user_id ,trade_account__slug__iexact=slug,
                                        trade_account__is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        context['form'] = form.as_div()
        return context

    def render_to_response(self, context, **response_kwargs):
        form = context['form']
        return JsonResponse({'form':str(form)})

@method_decorator(require_POST, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DeleteTradeRecord(JsonDeleteViewMixin ,DeleteView):
    model = TradeRecord

    def get_object(self, queryset=None):
        id = self.request.POST.get('id')
        user_id = self.request.user.pk
        slug = self.request.POST.get('account_name')
        obj = get_object_or_404(self.model, id=id,trade_account__slug__iexact=slug,trade_account__user_id=user_id,trade_account__is_active=True)
        return obj
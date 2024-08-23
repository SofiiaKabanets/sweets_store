from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Voucher
from .forms import VoucherApplyForm


@require_POST
def voucher_apply(request):
    form = VoucherApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            voucher = Voucher.objects.get(code__iexact=code, active=True, 
                                          valid_from__lte=timezone.now(), 
                                          valid_to__gte=timezone.now())
            request.session['voucher_id'] = voucher.id
        except Voucher.DoesNotExist:
            request.session['voucher_id'] = None
    return redirect('cart:cart_detail')

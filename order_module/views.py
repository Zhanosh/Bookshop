from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from bookModel_module.models import BookModels
from order_module.models import Order, OrderDetail

@login_required
def add_product_to_order(request):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({'text': 'Not Valid',
                             'icon': 'error',
                             'confirm_button_text': 'Ok'})
    if request.user.is_authenticated:
        product = BookModels.objects.filter(id=product_id, active=True).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += float(count)
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()
            return JsonResponse({
                'text': 'Add to cart',
                'icon': 'success',
                'confirm_button_text': 'Ok'
            })
    else:
        return JsonResponse({
            'text': 'Not login',
            'icon': 'error',
            'confirm_button_text': 'Ok'
        })


@login_required
def RemoveOrderDetailCount(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'text': 'Not Valid',
            'icon': 'error',
            'confirm_button_text': 'Ok'
        })
    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'text': 'Product is NONE',
            'icon': 'error',
            'confirm_button_text': 'Ok'
        })
    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render('Acount_module/Panel/cart-detail.html', context)
    return JsonResponse({
        'status': 'success',
        'body': data,
    })

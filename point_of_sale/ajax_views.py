from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum

from catalogue.models import Product
from .models import OrderItem, Order
from .tables import ProfileTable
from accounts.models import Profile
from site_settings.constants import CURRENCY
from django_tables2 import RequestConfig


@staff_member_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(Order, id=pk)
    products = Product.my_query.active()
    search_name = request.GET.get('search_name', None)
    search_name = search_name.capitalize() if search_name else search_name
    products = products.filter(Q(title__startswith=search_name) |
                               Q(sku__startswith=search_name)
                               ).distinct() if search_name else products
    products = products[:12]
    data = dict()
    data['products_container'] = render_to_string(template_name='point_of_sale/ajax/products_container.html',
                                                  request=request,
                                                  context={'products': products,
                                                           'instance': instance
                                                           }
                                                  )
    return JsonResponse(data)


@staff_member_required
def ajax_order_item(request, action, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    if action == 'add':
        order_item.qty += 1
    if action == 'remove':
        order_item.qty -= 1 if order_item.qty > 1 else order_item.qty
    order_item.save()
    if action == 'delete':
        order_item.delete()
    instance = order_item.order
    instance.refresh_from_db()
    data = dict()
    data['order_container'] = render_to_string(template_name='point_of_sale/ajax/order_container.html',
                                               request=request,
                                               context={
                                                   'instance': instance
                                               })
    return JsonResponse(data)


@staff_member_required
def ajax_add_product(request, pk, dk):
    order = get_object_or_404(Order, id=pk)
    product = get_object_or_404(Product, id=dk)
    order_item, created = OrderItem.objects.get_or_create(order=order, title=product)
    if created:
        order_item.value = product.price
        order_item.discount_value = product.price_discount
        order_item.cost = product.price_buy
        order_item.qty = 1
    else:
        order_item.qty += 1
    order_item.save()
    order.refresh_from_db()
    data = dict()
    data['order_container'] = render_to_string(template_name='point_of_sale/ajax/order_container.html',
                                               request=request,
                                               context={
                                                   'instance': order
                                               })
    return JsonResponse(data)


@staff_member_required
def ajax_costumers_report(request):
    data = {}
    costumers = Profile.filters_data(request, Profile.objects.all())
    dept = costumers.aggregate(Sum('balance'))['balance__sum'] if costumers.exists() else 0.00
    data['report_result'] = render_to_string(template_name='point_of_sale/ajax/report_result.html',
                                             request=request,
                                             context={
                                                 'page_title': 'Υπόλοιπο Πελατών',
                                                 'dept': dept,
                                                 'currency': CURRENCY
                                             }
                                             )
    return JsonResponse(data)


@staff_member_required
def ajax_search_costumers(request):
    data = dict()
    search_name = request.GET.get('search_name', None)
    qs = Profile.objects.filter(Q(last_name__contains=search_name.capitalize()) |
                                Q(first_name__contains=search_name.capitalize()) |
                                Q(notes__contains=search_name)
                                ).distinct() if search_name else Profile.objects.all()[:10]
    queryset_table = ProfileTable(qs)
    print(qs, search_name, 'works!')
    RequestConfig(request).configure(queryset_table)
    data['result_table'] = render_to_string(template_name='point_of_sale/ajax/search_container.html',
                                            request=request,
                                            context={
                                                'queryset_table': queryset_table
                                            }
                                            )
    return JsonResponse(data)

from django.shortcuts import get_object_or_404, render
from django.db.models import Sum, F
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from catalogue.categories import Category
from catalogue.models import Product, ProductPhotos
from catalogue.product_attritubes import AttributeTitle, AttributeProductClass, Attribute
from .models import ProductDiscount
from catalogue.forms import CategorySiteForm, BrandForm, VendorForm
from django.db.models import F
from site_settings.constants import CURRENCY


@staff_member_required
def ajax_category_site(request, slug,  pk, dk):
    instance = get_object_or_404(Product, id=pk)
    category = get_object_or_404(Category, id=dk)
    if slug == 'add':
        instance.category_site.add(category)
    if slug == 'delete':
        instance.category_site.remove(category)
    instance.save()
    selected_data = instance.category_site.all()
    data = dict()
    data['result'] = render_to_string(template_name='dashboard/ajax_calls/result_container.html',
                                      request=request,
                                      context={'selected_data': selected_data,
                                               'instance': instance
                                               }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_related_products_view(request, slug, pk, dk):
    instance = get_object_or_404(Product, id=pk)
    related = get_object_or_404(Product, id=dk)
    if slug == 'add':
        instance.related_products.add(related)
    if slug == 'delete':
        instance.related_products.remove(related)
    instance.save()
    selected_data = instance.related_products.all()
    data = dict()
    data['result'] = render_to_string(template_name='dashboard/ajax_calls/result_container.html',
                                      request=request,
                                      context={'selected_data': selected_data,
                                               'instance': instance
                                               }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_product_images(request, slug, pk, dk):
    instance = get_object_or_404(Product, id=pk)
    image = get_object_or_404(ProductPhotos, id=dk)
    if slug == 'is_primary':
        queryset = instance.images.all()
        queryset.update(is_primary=False)
        image.is_primary = True
        image.save()
    if slug == 'delete':
        image.delete()
    data = dict()
    instance.refresh_from_db()
    photos = instance.images.all()
    data['result'] = render_to_string(template_name='dashboard/ajax_calls/images.html',
                                      request=request,
                                      context={'photos': photos,
                                               'instance': instance
                                               }
                                      )
    return JsonResponse(data)


def ajax_add_or_delete_attribute(request, slug, pk, dk):
    instance = get_object_or_404(AttributeProductClass, id=pk)
    attr_class = instance
    attr_title = get_object_or_404(AttributeTitle, id=dk)
    if slug == 'add':
        my_attr, created = Attribute.objects.get_or_create(class_related=instance,
                                                           title=attr_title
                                                           )
    if slug == 'delete':
        my_attr, created = Attribute.objects.get_or_create(class_related=instance,
                                                           title=attr_title
                                                           )
        my_attr.delete()
    data = dict()
    attr_class.refresh_from_db()
    selected_data = instance.my_attributes.all()
    data['result'] = render_to_string(template_name='dashboard/ajax_calls/result_container_attr.html',
                                      request=request,
                                      context={
                                          'selected_data': selected_data,
                                          'attr_class': attr_class
                                      })
    return JsonResponse(data)


@staff_member_required
def ajax_add_or_delete_related_item(request, pk, dk):
    data = {}
    instance = get_object_or_404(Product, id=pk)
    related_instance = get_object_or_404(Product, id=dk)
    instance.related_products.add(related_instance)
    related_products = instance.related_products.all()
    data['html_data'] = render_to_string(request=request, template_name='dashboard/ajax_calls/related.html',
                                         context=locals())
    return JsonResponse(data)


@staff_member_required
def ajax_change_qty_on_attribute(request, pk):
    attr_data = get_object_or_404(Attribute, id=pk)
    qty = request.GET.get('qty', 1)
    print(qty)
    try:
        qty = int(qty)
    except:
        qty = 1
    if isinstance(qty, int):
        attr_data.qty = qty
        attr_data.save()
    data = dict()
    return JsonResponse(data)


def popup_category(request):
    form = CategorySiteForm(request.POST or None)
    form_title = 'Create category'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "dashboard/form.html", {"form": form, 'form_title': form_title})


def popup_brand(request):
    form = BrandForm(request.POST or None)
    form_title = 'Create Brand'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_brand");</script>' % (instance.pk, instance))
    return render(request, "dashboard/form.html", locals())


def popup_vendor(request):
    form = VendorForm(request.POST or None)
    form_title = 'Create Vendor'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_vendor");</script>' % (instance.pk, instance))
    return render(request, "dashboard/form.html", locals())


@staff_member_required
def ajax_product_calculate_view(request):
    data = dict()
    qs = Product.filters_data(request, Product.objects.all())
    total_qty = qs.aggregate(Sum('qty'))['qty__sum'] if qs.exists() else 0
    total_cost_value = qs.aggregate(total=Sum(F('qty')*F('price_buy')))['total'] if qs.exists() else 0
    total_value = qs.aggregate(total=Sum(F('qty')*F('final_price')))['total'] if qs.exists() else 0
    qs_vendor = qs.values_list('vendor__title').annotate(qty_=Sum('qty'),
                              total_cost_=Sum(F('qty')*F('price_buy')),
                              total_value_=Sum(F('qty')*F('final_price'))
                              ).order_by('qty_')
    data['report_result'] = render_to_string(
        template_name='dashboard/ajax_calls/product_result.html',
        request=request,
        context={
            'currency': CURRENCY,
            'qs_vendor': qs_vendor[:10],
            'total_qty': total_qty,
            'total_cost_value': total_cost_value,
            'total_value': total_value
        })
    return JsonResponse(data)


@staff_member_required
def ajax_products_discount_add(request, pk):
    data = dict()
    discount_order = get_object_or_404(ProductDiscount, id=pk)
    products = Product.filters_data(request, Product.objects.all())
    products = list(products)
    discount_order.products_related.add(*products)
    discount_order.save()
    discount_order.refresh_from_db()
    data['result'] = render_to_string(template_name='dashboard/ajax_calls/discount_result.html',
                                               request=request,
                                               context={'object': discount_order})
    return JsonResponse(data)


@staff_member_required
def ajax_product_discount_delete(request, pk, dk):
    instance = get_object_or_404(ProductDiscount, id=pk)
    product = get_object_or_404(Product, id=dk)
    product.price_discount = 0
    product.save()
    instance.products_related.remove(product)
    instance.refresh_from_db()
    data = dict()
    data['result'] = render_to_string(template_name='dashboard/ajax_calls/discount_result.html',
                                      request=request,
                                      context={'object': instance})
    return JsonResponse(data)

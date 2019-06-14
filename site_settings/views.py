from django.shortcuts import reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from .mixins import StoreBaseMixin, PaymentBaseMixin, ShippingBaseMixin
from .models import Store, PaymentMethod, Shipping, Banner
from .forms import StoreForm, PaymentMethodForm, ShippingForm, BannerForm
from .tables import PaymentMethodTable, StoreTable, ShippingTable, BannerTable
from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'site_settings/dashboard.html'


@method_decorator(staff_member_required, name='dispatch')
class StoreListView(ListView):
    template_name = 'dashboard/list_page.html'
    model = Store

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title, create_url, back_url = 'Σημεία Πώλησης',  reverse('site_settings:store_create'), reverse('dashboard:home')
        queryset_table = StoreTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class StoreCreateView(StoreBaseMixin, CreateView):
    model = Store
    template_name = 'dashboard/form.html'
    form_class = StoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Δημιουργία'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class StoreEditView(StoreBaseMixin, UpdateView):
    model = Store
    template_name = 'dashboard/form.html'
    form_class = StoreForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Επεξεργασία {self.object}'
        back_url, delete_url = self.get_success_url(), self.object.get_delete_url()
        context.update(locals())
        return context


@staff_member_required
def store_delete_view(request, pk):
    instance = get_object_or_404(Store, id=pk)
    instance.delete()
    return redirect(reverse('site_settings:stores'))


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodListView(ListView):
    model = PaymentMethod
    template_name = 'dashboard/list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Payment Method'
        create_url = reverse('site_settings:payment_create')
        queryset_table = PaymentMethodTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodCreateView(PaymentBaseMixin, CreateView):
    model = PaymentMethod
    template_name = 'dashboard/form.html'
    form_class = PaymentMethodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Payment'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodUpdateView(UpdateView):
    model = PaymentMethod
    template_name = 'dashboard/form.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('site_settings:payment_methods')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url, self.object.get_delete_url()
        context.update(locals())
        return context


@staff_member_required
def payment_delete_view(request, pk):
    instance = get_object_or_404(PaymentMethod, id=pk)
    instance.delete()
    return redirect(reverse('site_settings:payment_methods'))


@method_decorator(staff_member_required, name='dispatch')
class ShippingListView(ListView):
    model = Shipping
    template_name = 'dashboard/list_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Shipping'
        queryset_table = ShippingTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        create_url = reverse('site_settings:shipping_create')

        # filters
        active_name, search_name = [True]*2
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class ShippingCreateView(ShippingBaseMixin, CreateView):
    model = Shipping
    template_name = 'dashboard/form.html'
    form_class = ShippingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create New Shipping'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class ShippingEditView(ShippingBaseMixin, UpdateView):
    model = Shipping
    template_name = 'dashboard/form.html'
    form_class = ShippingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit {self.object}'
        back_url, delete_url = self.get_success_url(), None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BannerListView(ListView):
    model = Banner
    template_name = 'dashboard/list_page.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Banners'
        create_url, back_url = reverse('site_settings:banner_create'), reverse('dashboard:home')
        queryset_table = BannerTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('site_settings:banner_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = 'Create Banner'
        back_url, delete_url = self.success_url, None
        context.update(locals())
        return context


@method_decorator(staff_member_required, name='dispatch')
class BannerUpdateView(UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'site_settings/form.html'
    success_url = reverse_lazy('site_settings:banner_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_title = f'Edit Banner {self.object}'
        back_url, delete_url = self.success_url, reverse('site_settings:banner_delete', kwargs={'pk': self.object.id})
        context.update(locals())
        return context


@staff_member_required
def banner_delete_view(request, pk):
    instance = get_object_or_404(Banner, id=pk)
    instance.delete()
    return redirect(reverse('site_settings:banner_list'))

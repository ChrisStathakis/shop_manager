from django.db import models
from django.db.models import Sum, Q, F
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.text import slugify
import os, datetime
from decimal import Decimal
from tinymce.models import HTMLField

from site_settings.abstract_models import DefaultBasicModel
from .categories import Category, WarehouseCategory
from .product_details import Vendor, Brand

from site_settings.constants import MEDIA_URL, CURRENCY, UNIT
from .managers import ProductManager

WAREHOUSE_ORDERS_TRANSCATIONS = settings.WAREHOUSE_ORDERS_TRANSCATIONS
RETAIL_TRANSCATIONS = settings.RETAIL_TRANSCATIONS


class ProductClass(models.Model):
    title = models.CharField(unique=True, max_length=150)
    is_service = models.BooleanField(default=False, verbose_name='Υπηρεσία')
    have_transcations = models.BooleanField(default=True, verbose_name='Υποστηρίζει συναλλαγές')
    have_attribute = models.BooleanField(default=False, verbose_name='Μεγεθολόγιο')

    class Meta:
        verbose_name = 'Product Class'
        verbose_name_plural = 'Product Classes'

    def __str__(self):
        return self.title


class Product(DefaultBasicModel):
    is_offer = models.BooleanField(default=False, verbose_name='Προσφορά')
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, verbose_name='Είδος')
    featured_product = models.BooleanField(default=False, verbose_name='Εμφάνιση Πρώτη Σελίδα')
    #  warehouse data
    order_code = models.CharField(null=True, blank=True, max_length=100, verbose_name="Κωδικός Τιμολογίου")
    price_buy = models.DecimalField(decimal_places=2, max_digits=6, default=0, verbose_name="Αξία Αγοράς")
    order_discount = models.IntegerField(default=0, verbose_name="'Έκπτωση Τιμολογίου")
    category = models.ForeignKey(WarehouseCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Κατηγορία Αποθήκης')
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Προμηθευτής')

    qty_measure = models.DecimalField(max_digits=5, decimal_places=3, default=1, verbose_name='Ποσότητα Ανά Τεμάχιο')
    qty = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Ποσότητα')
    qty_add = models.DecimalField(default=0, verbose_name="Qty Add", max_digits=10, decimal_places=2,
                                  help_text='System use it only if warehouse transations')
    qty_remove = models.DecimalField(default=0, verbose_name="Qty Remove", max_digits=10, decimal_places=2,
                                     help_text='System use it only if warehouse transations')
    barcode = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True, verbose_name='Περιγραφή')
    measure_unit = models.CharField(max_length=1, default='1', choices=UNIT, blank=True, null=True, verbose_name='Μονάδα Μέτρησης')
    safe_stock = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Όριο αποθέματος')

    objects = models.Manager()
    my_query = ProductManager()

    #site attritubes
    sku = models.CharField(max_length=150, blank=True, null=True)
    site_text = HTMLField(blank=True, null=True)
    category_site = models.ManyToManyField(Category, blank=True, null=True, verbose_name='Κατηγορία Site')
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name='Brand Name', on_delete=models.SET_NULL)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    # price sell and discount sells
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0, verbose_name="Αρχική Τιμή")
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Εκπτωτική Τιμή')
    final_price = models.DecimalField(default=0, decimal_places=2, max_digits=10, blank=True, verbose_name='Τιμή Πώλησης')

    #size and color
    related_products = models.ManyToManyField('self', blank=True, verbose_name='Related Products')

    class Meta:
        verbose_name_plural = "1. Products"
        ordering = ['-id', ]

    def save(self, *args, **kwargs):
        self.final_price = self.price_discount if self.price_discount > 0 else self.price
        self.is_offer = True if self.price_discount > 0 else False

        self.qty = self.qty_add - self.qty_remove
        super(Product, self).save(*args, **kwargs)

    def calculate_qty_if_attributes(self):
        attributes = self.attr_class.all()
        qty = 0
        for ele in attributes:
            if ele.class_related.have_transcations:
                qty = ele.my_attributes.aggregate(Sum('qty'))['qty__sum'] if ele.my_attributes else 0
        return qty

    def warehouse_calculations(self):
        if not WAREHOUSE_ORDERS_TRANSCATIONS:
            # if our program don't support warehouse transcations, we pass
            pass
        warehouse_order_items = self.invoice_products.all()
        # we will calculate two different values, the incomes and outcomes
        warehouse_in_items = warehouse_order_items.filter(order__order_type__in=['1', '2', '4'])
        warehouse_out_items = warehouse_order_items.filter(order__order_type='5')
        warehouse_in_qty = warehouse_in_items.aggregate(Sum('qty'))['qty__sum'] if warehouse_in_items else 0
        warehouse_out_qty = warehouse_out_items.aggregate(Sum('qty'))['qty__sum'] if warehouse_out_items else 0
        self.qty_add = warehouse_in_qty - warehouse_out_qty
        self.save()

    def order_calculations(self):
        if not RETAIL_TRANSCATIONS:
            self.qty_remove = 0
            self.save()
            return ''
        if self.product_class.is_service:
            pass
        if not self.product_class.have_transcations:
            return self.qty
        order_items = self.retail_items.all()
        qty_analysis = order_items.values('order__order_type').annotate(total_qty=(Sum('qty'))).order_by(
            'order__order_type')
        for qty_data in qty_analysis:
            qty_remove = qty_data['total_qty'] if qty_data['order__order_type'] in ['r', 'e', 'wa'] else 0
            qty = qty_remove - qty_data['total_qty'] if qty_data['order__order_type'] in ['b', 'wr'] else qty_remove
        self.qty_remove = qty_remove
        self.save()

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('dashboard:product_detail', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('dashboard:product_delete',  kwargs={'pk': self.id})

    @property
    def have_attr(self):
        return self.product_class.have_attribute if self.product_class else False

    def get_edit_url(self):
        return reverse('dashboard:product_detail', kwargs={'pk': self.id})

    def get_cart_url(self):
        return reverse('cart:check', kwargs={'pk': self.id, 'action': 'add'})

    def get_absolute_url(self):
        return reverse('product_view', kwargs={'slug': self.slug})

    def tag_qty(self):
        return f'{self.qty}  {self.get_measure_unit_display()}'

    @property
    def image(self):
        try:
            return ProductPhotos.objects.filter(active=True, product=self, is_primary=True).last().image
        except:
            pass

    def tag_final_price(self):
        return f'{self.final_price} {CURRENCY}'

    def tag_price_buy(self):
        return f'{self.price_buy} {CURRENCY}'

    def get_all_images(self):
        return ProductPhotos.objects.filter(active=True, product=self)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s%s" class="img-responsive">' % (MEDIA_URL, self.image))
        return mark_safe('<img src="%s" class="img-responsive">' % "{% static 'home/no_image.png' %}")

    def image_tag_tiny(self):
        if self.image:
            return mark_safe('<img src="%s%s" width="100px" height="100px">' % (MEDIA_URL, self.image))

    def show_warehouse_remain(self):
        return self.qty * self.qty_kilo

    @staticmethod
    def filters_data(request, queryset=None):
        if not queryset:
            queryset = Product.objects.all()
        search_name = request.GET.get('search_name', None)
        cate_name = request.GET.getlist('cate_name', None)
        brand_name = request.GET.getlist('brand_name', None)
        active_name = request.GET.get('active_name', None)
        discount_name = request.GET.get('discount_name')
        qty_name = request.GET.get('qty_exists_name')
        vendor_name = request.GET.getlist('vendor_name', None)
        ware_cate = request.GET.getlist('ware_cate', None)

        queryset = queryset.filter(vendor__id__in=vendor_name) if vendor_name else queryset
        queryset = queryset.filter(category__id__in=ware_cate) if ware_cate else queryset
        queryset = queryset.filter(active=True) if active_name == '1' else queryset.filter(
            active=False) if active_name == '2' else queryset
        queryset = queryset.filter(price_discount__gt=0) if discount_name else queryset
        queryset = queryset.filter(qty__gt=0) if qty_name else queryset

        queryset = queryset.filter(category_site__id__in=cate_name) if cate_name else queryset
        queryset = queryset.filter(brand__id__in=brand_name) if brand_name else queryset
        queryset = queryset.filter(title__icontains=search_name) if search_name else queryset

        return queryset


@receiver(post_save, sender=Product)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Product.objects.filter(slug=new_slug).exists()
        instance.slug = f'{new_slug}-{instance.id}' if qs_exists else new_slug
        instance.save()


class ProductPhotos(models.Model):
    image = models.ImageField()
    alt = models.CharField(null=True, blank=True, max_length=200,
                           help_text='Θα δημιουργηθεί αυτόματα εάν δεν συμπληρωθεί')
    title = models.CharField(null=True, blank=True, max_length=100,
                             help_text='Θα δημιουργηθεί αυτόματα εάν δεν συμπληρωθεί')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False, verbose_name='Primary Picture')
    is_back = models.BooleanField(default=False, verbose_name='Δεύτερη Εικόνα')

    class Meta:
        verbose_name_plural = 'Gallery'
        ordering = ['-is_primary', ]

    def save(self, *args, **kwargs):
        self.title = f'{self.product.title}' if self.product and not self.title else self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.title

    def image_status(self):
        return 'Primary Image' if self.is_primary else 'Secondary Image' if self.is_back else 'Image'

    def tag_image(self):
        return mark_safe('<img width="150px" height="150px" src="%s%s" />' % (MEDIA_URL, self.image))

    tag_image.short_description = 'Photo'

    def tag_image_tiny(self):
        return mark_safe(f'<img width="150px" height="150px" src="{self.image.url}" />')

    tag_image_tiny.short_description = 'Εικόνα'

    def tag_status(self):
        return 'First Picture' if self.is_primary else 'Back Picture' if self.is_back else 'Picture'

    def tag_primary(self):
        return 'Primary' if self.is_primary else 'No Primary'

    def tag_secondary(self):
        return 'Secondary' if self.is_back else "No Back Image"


class Gifts(models.Model):
    title = models.CharField(max_length=150, unique=True)
    gift_message = models.CharField(max_length=200, unique=True)
    status = models.BooleanField(default=False)
    product_related = models.ManyToManyField(Product, related_name='product_related')
    products_gift = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def tag_status(self):
        return 'Active' if self.status else 'Non Active'






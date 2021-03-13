from django.db import models
from users.models import User
from products.models import Product, Category
from users.models import get_user
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
import time

# Create your models here.

class Coupon(models.Model):
    USAGE_TYPE_CHOICES = [
        ('single', 'Один раз на каждого пользователя'),
        ('multiple', 'Множество раз на каждого'),
    ]
    code = models.CharField(max_length = 100, unique = True)
    # description = models.TextField(default = None,
    # null = True, blank = True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    from_amount = models.IntegerField(default = None,
    null = True, blank = True)
    usage_type = models.CharField(
        max_length = 50,
        choices = USAGE_TYPE_CHOICES,
        default = "single")
    products = models.ManyToManyField(Product,
    null = True, blank = True)
    categories = models.ManyToManyField(Category,
    null = True, blank = True)
    active = models.BooleanField()

    def __str__(self):
        return self.code
    def get_products_list(self):
        return list(self.products.values_list('id', flat = True))
    def get_categories_list(self):
        return list(self.categories.values_list('id', flat = True))
    def check_user(self, request):
        user = get_user(request)
        if user != None:
            return True
        else:
            return False
    def process_cart_coupon(self, request):
        print('self products is', self.products)
        print(self.products == None)
        print('self categories is', self.categories)
        success = True
        msg = ''
        cart = Cart.objects.get(
            session_key = request.session.session_key
        )
        if self.from_amount:
            if cart.get_total() < self.from_amount:
                success = False
                msg = 'Промокод действует при заказе от {} руб.'.format(self.from_amount)
        if success == True:
            if (not self.products.exists()) and (not self.categories.exists()):
                success = True
                msg = ''
            elif self.products.exists():
                products_pass_ids = []
                coupon_products_ids = self.get_products_list()
                cart_products_ids = cart.get_items_list()
                for item in cart_products_ids:
                    if item in coupon_products_ids:
                        products_pass_ids.append(item)
                if len(products_pass_ids) > 0:
                    success = True
                    msg = "{}".format(products_pass_ids)
                else:
                    success = False
                    msg = 'Промокод не подходит к выбранным товарам'
            elif self.categories.exists():
                products_pass_ids = []
                coupon_categories_ids = self.get_categories_list()
                # cart_categories_ids = cart.get_items_cat_list()
                for item in cart.item_set.all():
                    item_category_id = Product.objects.get(
                        id = item.pr_id
                    ).category.id
                    if item_category_id in coupon_categories_ids:
                        products_pass_ids.append(item.pr_id)
                if len(products_pass_ids) > 0:
                    success = True
                    msg = "{}".format(products_pass_ids)
                else:
                    success = False
                    msg = 'Промокод не подходит к выбранным товарам'

        if success == True:
            cart.apply_promo(self)
            msg = 'promo added'
        return JsonResponse({
            'success': success,
            'msg': msg,
        }, status = 200)
        
class Favorite(models.Model):
    created_at = models.DateTimeField(auto_now_add = True) 
    session_key = models.CharField(max_length = 200)
    def get_items(self):
        items = self.favoriteitem_set.all()
        return len(items)

class Favoriteitem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete = models.CASCADE, default = None,
    blank = True, null = True)
    pr_id = models.IntegerField(default = None)

class Cart(models.Model):  
    created_at = models.DateTimeField(auto_now_add = True) 
    session_key = models.CharField(max_length = 200)
    coupon = models.ForeignKey(Coupon, on_delete = models.DO_NOTHING,
    blank = True, null = True)

    # def __str__(self):
    #     return self.id

    def get_total(self):
        total = 0
        for item in self.item_set.all():
            total += item.get_price()
        return total

    def apply_promo(self, promo):
        self.coupon = promo
        self.save()

    def get_items_list(self):
        return list(self.item_set.values_list('pr_id', flat = True))
    def get_items_cat_list(self):
        pr_id_list = list(self.item_set.values_list('pr_id', flat = True))
        products = Product.objects.filter(id__in = pr_id_list)
        # return list(dict.fromkeys(list(products.values_list('category__id', flat = True))))
        return list(products.values_list('category__id', flat = True))
    def items_in_cart(self):
        return len(self.item_set.all())

    def get_total_discount(self):
        products = self.item_set.all()
        total_discount = 0
        for product in products:
            if product.has_sale():
                total_discount += product.discount_val()
        return total_discount
    def get_current_cart(self, request):
        cart = Cart.objects.get(
            session_key = request.session.session_key
        )
        return cart


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('in_progress','В процессе'),
        ('completed','Завершен'),
        ('cancelled','Отменен'),
    ]

    user = models.ForeignKey(User, on_delete = models.SET_NULL,
    default = None, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True) 
    name = models.CharField(max_length = 200, default = '')
    phone = models.CharField(max_length = 50, default = '')
    # email = models.CharField(max_length = 200, default = '')
    delivery = models.CharField(max_length = 200, default = '')
    address = models.CharField(max_length = 1000, default = '')
    payment = models.CharField(max_length = 200, default = '')
    bonus_gained = models.IntegerField(default = 0, blank = True,
    null = True)
    coupon = models.ForeignKey(Coupon, on_delete = models.DO_NOTHING,
    blank = True, null = True)
    status = models.CharField(
        max_length = 100,
        choices = ORDER_STATUS_CHOICES, 
        default = 'in_progress'
    )

    def __str__(self):
        return self.name + ' ' + self.phone

    def save(self, *args, **kwargs):
        # print('trigger order save')
        # print('user is: ', self.user)
        # print('user bonus', self.user.bonus)
        if self.user != None:
            if self.status == 'completed':
                self.user.bonus += self.bonus_gained
                self.user.save()
        super(Order, self).save(*args, **kwargs)

    def get_order_cost(self):
        cost = 0
        for item in self.item_set.all():
            item_cost = item.product_get_price() * item.quantity
            cost += item_cost
        return cost

    
class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, default = None,
    blank = True, null = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, 
    default = None, blank = True, null = True)

    pr_id = models.IntegerField(default = 0)
    name = models.CharField(max_length = 200, default = '')
    price = models.IntegerField(default = 0)
    sale_price = models.IntegerField(default = 0)
    category =  models.ForeignKey(Category,
    on_delete=models.CASCADE, default = None)
    quantity = models.IntegerField(default = 1)
    imgsrc = models.ImageField(upload_to="static/images/products")

    def get_price(self):
        item_price = self.product_get_price() * self.quantity
        if self.cart.coupon == None:
            return item_price
        else:
            if self.cart.coupon.categories.exists() or self.cart.coupon.products.exists():
                coupon_products_list = []
                coupon_categories_list = []
                if self.cart.coupon.categories.exists():
                    coupon_categories_list = self.cart.coupon.get_categories_list()
                if self.cart.coupon.products.exists():
                    coupon_products_list = self.cart.coupon.get_products_list()
                if self.pr_id in coupon_products_list or self.category.id in coupon_categories_list:
                    return int(item_price - ((item_price * self.cart.coupon.discount)/100))
                else:
                    return item_price
            else:
                return int(item_price - ((item_price * self.cart.coupon.discount)/100))

    def product_price(self):
        return self.price * self.quantity
    def product_sale_price(self):
        return self.sale_price * self.quantity
    def product_get_price(self):
        if self.sale_price > 1:
            return self.sale_price
        else:
            return self.price
    def __str__(self):
        return self.name 

    def discount_perc(self):
            return int((self.sale_price / self.price) * 100)
    def discount_val(self):
        return int(self.price - self.sale_price) * self.quantity
    def has_sale(self):
        if self.sale_price > 0:
            return True
        else:
            return False


def calc_bonus_gained(user, purchase_amount):
        if user != None:
            disc = user.calc_user_discount()
            bonus = purchase_amount * disc / 100
        else:
            bonus = 0
        return bonus
    

def delete_all_cart():
    carts = Cart.objects.all()
    items = Item.objects.all()
    orders = Order.objects.all()
    fav = Favorite.objects.all()
    fav_items = Favoriteitem.objects.all()
    fav.delete()
    print('fav is deleted')
    fav_items.delete()
    print('fav items are deleted')
    carts.delete()
    print("All carts are deleted")
    items.delete()
    print("All items are deleted")
    orders.delete()
    print("All orders are deleted")






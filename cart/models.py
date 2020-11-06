from django.db import models

# Create your models here.

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

    def get_total(self):
        total = 0
        for item in self.item_set.all():
            total += item.price * item.quantity
        return total
    def items_in_cart(self):
        return len(self.item_set.all())

    def get_total_discount(self):
        products = self.item_set.all()
        total_discount = 0
        for product in products:
            if product.has_sale():
                total_discount += product.discount_val()
        return total_discount
    


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add = True) 
    name = models.CharField(max_length = 200, default = '')
    phone = models.CharField(max_length = 50, default = '')
    # email = models.CharField(max_length = 200, default = '')
    delivery = models.CharField(max_length = 200, default = '')
    address = models.CharField(max_length = 1000, default = '')
    payment = models.CharField(max_length = 200, default = '')

    def __str__(self):
        return self.name + ' ' + self.phone
    
    
class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, default = None,
    blank = True, null = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, 
    default = None, blank = True, null = True)

    pr_id = models.IntegerField(default = 0)
    name = models.CharField(max_length = 200, default = '')
    price = models.IntegerField(default = 0)
    sale_price = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 1)
    imgsrc = models.ImageField(upload_to="static/images/products")

    def product_price(self):
        return self.price * self.quantity
    def product_sale_price(self):
        return self.sale_price * self.quantity
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






from django.db import models


# Create your models here.

def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key  



class User(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(default = None, max_length = 50)
    email = models.CharField(default = None, max_length = 100,
    blank = True, null = True)
    password = models.CharField(default = None, max_length = 200)
    name = models.CharField(default = None, max_length = 100)
    bonus = models.IntegerField(default = 0, 
    null = True, blank = True)

    def __str__(self):
        return self.phone
    def check_password_correct(self, password):
        if self.password == password:
            return True
        else:
            return False
    def set_password(self, password):
        self.password = password
    def get_total_spend(self):
        total_spend = 0
        for order in self.order_set.all():
            # total_spend += order.get_order_cost()
            total_spend += order.amount
        return total_spend
    def get_total_bonus_gained(self):
        return self.bonus
    def calc_user_discount(self):
        total_spend = self.get_total_spend()
        discount = 5
        if total_spend > 5000:
            discount = 7
        if total_spend > 10000:
            discount = 10
        return discount

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
    blank = True, null = True)
    city = models.CharField(default = None, max_length = 200,
    null = True, blank = True)
    street = models.CharField(default = None, max_length = 200,
    null = True, blank = True)
    house = models.CharField(default = None, max_length = 200,
    null = True, blank = True)
    flat = models.CharField(default = None, max_length = 200,
    null = True, blank = True)
    comment = models.TextField(default = None, max_length = 1000,
    null = True, blank = True)

    def get_full(self):
        main = self.city + ', ' +  self.street + ' ул. ' +'д. '+ self.house
        if len(self.flat) > 0:
            main += ', кв. ' + self.flat
        return main


def auth_user(username, password):
    if User.objects.filter(
        phone__iexact = username
    ).exists():
        user = User.objects.get(phone = username)
        if user.password == password:
            return user
        else:
            return None
    else:
        return None

def login_user(request, user):
    session_key = get_session_key(request)
    request.session[session_key] = user.id

def login_out_user(request):
    del request.session[request.session.session_key]

def get_user(request):
    session_key = get_session_key(request)
    try:
        user_id = request.session[request.session.session_key]
        user = User.objects.get(id = user_id)
        return user
    except:
        # login_out_user(request)
        return None

def is_authorized(request):
    if request.session.session_key in request.session:
        return True
    else:
        return False

def exist_user(username):
    exist = User.objects.filter(
        phone = username
    ).exists()
    return exist

def register_user(name, username, password):
    user = User(
        name = name,
        phone = username,
        password = password,
    )
    user.save()
    return user







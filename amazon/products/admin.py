from django.contrib import admin
from users.models import User_info,Cart_table,Order_history,Payment_history
from products.models import ProductTable
# Register your models here.
admin.site.register(User_info)
admin.site.register(Cart_table)
admin.site.register(Order_history)
admin.site.register(Payment_history)
admin.site.register(ProductTable)


from django.shortcuts import render
from django.db import transaction

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem

from orders.tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            # launch asynchronous tasks
            # order_created.delay(order.id)
            return render(request, 'orders/created.html', {'order': order})
    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

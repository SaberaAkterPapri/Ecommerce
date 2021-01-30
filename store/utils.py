import json
from .models import *


def cookieCart(request):
    try:
        print('TRY IN COOKIE CART', request.COOKIES)
        cart = JSON.loads(request.COOKIES['cart'])
        return cart
    except:
        print('EXCEPT IN COOKIE CART')
        cart = {}    
        print('Cart:', cart)
        print('User is not authenticated')
        items = []   
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems = order['get_cart_items']  

        for i in cart:
            try:
                cartItems += cart[i]['quantity'] 

                Product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                    }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True

            except:
                pass       

        return{'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print(order) 
        items = order.orderitem_set.all()
        print(order.orderitem_set.all()) 
        cartItems = order.get_cart_items    
           
    else:
        cookieData = cookieCart(request)
        print('COOKE DATA: ', cookieData)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']  
    return{'cartItems':cartItems, 'order':order, 'items':items}   

def guestOrder(request, data):
    print('User is not logged in..')   

    print('COOKIES:', request.COOKIES) 
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
        )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )
    return customer, order
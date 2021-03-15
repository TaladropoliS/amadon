from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    quantity_from_form = int(request.POST["quantity"])
    price_from_form = float(request.POST["price"])
    id_producto = request.POST["caracola"]
    precio_real = Product.objects.filter(id=id_producto)
    for precio in precio_real:
        print('precio_real', precio.price)
        if precio.price == price_from_form:
            total_charge = quantity_from_form * price_from_form
            print("Charging credit card...")
            Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
            return redirect(pago)
        else:
            return redirect('/')

def pago(request):
    todas_las_compras = Order.objects.all()
    gastado_en_total = 0
    for gasto in todas_las_compras:
        gastado_en_total += gasto.total_price

    total_productos = 0
    for producto in todas_las_compras:
        total_productos += producto.quantity_ordered

    total_charge = Order.objects.last().total_price

    context = {
        'total_charge': total_charge,
        'total_productos': total_productos,
        'gastado_en_total': gastado_en_total,
    }

    return render(request, "store/checkout.html", context)
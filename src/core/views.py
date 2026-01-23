from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
)

# ----- Template-based views -----
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')[:50]
    return render(request, 'core/home.html', {
        'categories': categories,
        'products': products,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, 'core/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('core:product_detail', pk=product_id)

    product = get_object_or_404(Product, pk=product_id, available=True)
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    messages.success(request, 'تمت إضافة المنتج للسلة.')
    return redirect('core:cart')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.line_total() for item in items)
    return render(request, 'core/cart.html', {'items': items, 'total': total})

@login_required
def update_cart(request):
    if request.method != 'POST':
        return redirect('core:cart')
    action = request.POST.get('action')
    item_id = request.POST.get('item_id')
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    if action == 'remove':
        item.delete()
        messages.success(request, 'تم حذف المنتج من السلة.')
    else:
        qty = int(request.POST.get('quantity', item.quantity))
        if qty <= 0:
            item.delete()
            messages.success(request, 'تم حذف المنتج من السلة.')
        else:
            item.quantity = qty
            item.save()
            messages.success(request, 'تم تحديث السلة.')
    return redirect('core:cart')

@login_required
@transaction.atomic
def checkout(request):
    if request.method == 'GET':
        items = CartItem.objects.filter(user=request.user).select_related('product')
        if not items.exists():
            messages.warning(request, 'سلتك فارغة.')
            return redirect('core:home')
        total = sum(item.line_total() for item in items)
        return render(request, 'core/checkout.html', {'items': items, 'total': total})

    # POST -> create order
    address = request.POST.get('address', '').strip()
    if not address:
        messages.error(request, 'يرجى إدخال عنوان التوصيل.')
        return redirect('core:checkout')

    items = CartItem.objects.filter(user=request.user).select_related('product')
    if not items.exists():
        messages.warning(request, 'سلتك فارغة.')
        return redirect('core:home')

    total = sum(item.line_total() for item in items)
    order = Order.objects.create(user=request.user, total=total, address=address)
    order_items = []
    for c in items:
        oi = OrderItem(order=order, product=c.product, quantity=c.quantity, price=c.product.price)
        order_items.append(oi)
    OrderItem.objects.bulk_create(order_items)
    items.delete()
    messages.success(request, f'تم إنشاء الطلب بنجاح. رقم الطلب: #{order.id}')
    return redirect('core:home')


# ----- API viewsets (DRF) -----
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({ 'detail': 'cart cleared' }, status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        items = order.items.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)
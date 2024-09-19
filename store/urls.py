
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter 
from rest_framework_nested  import routers

router = routers.DefaultRouter()

router.register('products', ProductViewSet , basename='products')
router.register('collections', CollectionViewSet)
router.register('cart', CartViewSet)
router.register('customers', CustomerViewSet)

products_router = routers.NestedDefaultRouter(router , 'products' , lookup ='product')
products_router.register('reviews', ReviewViewSet , basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router , 'cart' , lookup ="cart" )
carts_router.register('items' , CartItemViewSet , basename="cart-item")

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(products_router.urls)),
    path(r'', include(carts_router.urls)),
    
]
# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView



from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.viewsets import ModelViewSet , GenericViewSet
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin , DestroyModelMixin , UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action 
from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import *
from .serializers import *



class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']
    
    def get_serializer_context(self):
        return {'request' : self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__id = kwargs['pk']).count() > 0 :
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)

    


        
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count = Count('products')).all()
    serializer_class = CollectionSerializer   
    
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection__id = kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    
class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    
class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin, 
                  GenericViewSet):

    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializers
        return CartItemSerilizer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    

    def get_queryset(self):
        return CartItem.objects.\
            filter(cart_id = self.kwargs['cart_pk'])\
            .select_related('product')
    

class CustomerViewSet(CreateModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers

    @action(detail=False, methods=['GET','PUT'])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializers(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializers(customer, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
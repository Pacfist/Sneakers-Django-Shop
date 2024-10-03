from goods.models import Products
from django.db.models import Q
from django.db.models import F, ExpressionWrapper, DecimalField

def q_search(query):

    if query.isdigit() and len(query) <=5:
        return Products.objects.filter(id=int(query))
    
    keywords=[word for word in query.split() if len(word)>2]
    q_objects=Q()
    for token in keywords:
        q_objects|= Q(name__icontains=token)
        
        
    return Products.objects.filter(q_objects)



def anotation(products):
    products = products.annotate(
        sell_price=ExpressionWrapper(
            F('price') - F('price') * F('descount') / 100,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )
    return products
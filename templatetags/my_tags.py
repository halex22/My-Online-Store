from django import template

register = template.Library()


@register.filter(name='custom_range')
def custom_range(value:str):
    print(value)
    if value:
        value = str(value).split('.')[0]
        
        return range(int(value))
    else:
        pass

@register.filter(name='mid_star')
def fun(value):
    value = str(value).split('.')[1]
    result = int(value) != 0
    return result

@register.filter(name='remainer_range')
def remainer_range(value):
    n = 4 if fun(value) else 5
    return range( n - int(str(value).split('.')[0])) 

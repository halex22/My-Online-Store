from django import template

register = template.Library()


@register.filter(name='custom_range')
def custom_range(value:str):
    value = str(value).split('.')[0]
    return range(int(value))


@register.filter(name='mid_star')
def fun(value):
    value = float(value)
    value = str(value).split('.')[1]
    result = int(value) != 0
    return result


@register.filter(name='remainer_range')
def remainer_range(value):
    n = 4 if fun(value) else 5
    return range( n - int(str(value).split('.')[0])) 


@register.filter(name='make_float')
def make_float(value):
    return round(float(value), 1)


@register.filter(name='another_page')
def number_test(value, direction):
    current_page = value.number
    total_pages = value.paginator.num_pages
    if direction:
        return True if (current_page + 2) <= total_pages else False
    else:
        return True if (current_page - 2) >= 1 else False
@register.filter(name='add_page_number')
def add_page_number(value, direction):
    return (value.number + 2) if direction else (value.number - 2)
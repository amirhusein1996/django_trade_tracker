from django import template

register = template.Library()
#
#
#
@register.filter('comma_seprator')
def comma_seprator(value):
    if value % 1 == 0:  # is_integer?
        return '{:,.0f}'.format(value)
    return '{:,.2f}'.format(value)

@register.filter('dollar_sign')
def dollar_sign(value):
    if value % 1 == 0: # is_integer?
        return '${:,.0f}'.format(value)
    return '${:,.2f}'.format(value)
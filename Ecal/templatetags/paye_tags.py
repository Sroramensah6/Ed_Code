from django import template
from Eformulas.individual_models import ECALBasic, ECALAdvance

register = template.Library()


@register.inclusion_tag('tag.html')
def total_paye(request):
    show_results = ECALAdvance.objects.order_by('-id')
    return {"show_results": show_results, "request": request}


@register.inclusion_tag('basic_details.html')
def basic_paye(request):
    show_results = ECALBasic.objects.order_by('-id')

    return {"show_results": show_results, "request": request}

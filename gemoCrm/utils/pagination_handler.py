from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from pip._vendor.distlib.locators import Page


def get_pagination_data(paginator: Paginator, page: int):
    """
    return data object from a given pagination page
    """
    data = None
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return data

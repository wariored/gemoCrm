from django.db.models import Q


def get_deal_filters(request, filter_params) -> (Q, dict):
    query = None

    deal_stage = request.GET.get('deal-stage')
    deal_type = request.GET.get('deal-type')
    amount_from = request.GET.get('amount-from')
    amount_to = request.GET.get('amount-to')
    contains_text = request.GET.get('contains-text')

    filter_params["deal_stage"] = deal_stage
    filter_params["deal_type"] = deal_type
    filter_params["amount_from"] = amount_from
    filter_params["amount_to"] = amount_to
    filter_params["contains_text"] = contains_text

    if deal_stage:
        query = Q(deal_stage__name=deal_stage)
    if deal_type:
        q = Q(deal_type__name=deal_type)
        query = query & q if query is not None else q
    if amount_from:
        q = Q(amount__gte=amount_from)
        query = query & q if query is not None else q
    if amount_to:
        q = Q(amount__lte=amount_to)
        query = query & q if query is not None else q
    if contains_text:
        q = Q(name__icontains=contains_text)
        query = query & q if query is not None else q

    return query, filter_params

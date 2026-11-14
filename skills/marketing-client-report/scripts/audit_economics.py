"""Calculate explicitly supplied campaign scenarios without inventing actuals."""

from decimal import Decimal, InvalidOperation, ROUND_CEILING


def number(value, *, positive=False):
    if isinstance(value, bool):
        raise ValueError("A number is required")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("A finite number is required") from exc
    if not result.is_finite() or result < 0 or (positive and result == 0):
        raise ValueError("A positive value is required" if positive else "A non-negative value is required")
    return result


def campaign_case(total_cost, media_cost, buyers, contribution_per_buyer=None, attendees=None):
    """Contribution excludes campaign costs already included in total_cost."""
    total = number(total_cost)
    media = number(media_cost)
    buyers = number(buyers, positive=True)
    if media > total:
        raise ValueError("Media cannot exceed the full campaign cost")
    result = {
        "full_campaign_cost_per_buyer": total / buyers,
        "media_cost_per_buyer": media / buyers,
        "campaign_balance_before_other_overhead": None,
        "break_even_buyers": None,
        "break_even_attendee_purchase_rate": None,
    }
    if contribution_per_buyer is not None:
        contribution = number(contribution_per_buyer, positive=True)
        needed = (total / contribution).to_integral_value(rounding=ROUND_CEILING)
        result.update({
            "campaign_balance_before_other_overhead": buyers * contribution - total,
            "break_even_buyers": needed,
        })
        if attendees is not None:
            result["break_even_attendee_purchase_rate"] = needed / number(attendees, positive=True)
    return result


def acquisition_case(media_spend, visits, buyers):
    spend = number(media_spend)
    visits = number(visits, positive=True)
    buyers = number(buyers, positive=True)
    return {"media_cost_per_buyer": spend / buyers, "buyers_per_visit": buyers / visits}

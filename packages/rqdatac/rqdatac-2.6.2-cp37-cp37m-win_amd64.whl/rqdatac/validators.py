# -*- coding: utf-8 -*-
import warnings
import datetime

from dateutil.relativedelta import relativedelta
from six import string_types, binary_type, text_type

from rqdatac.utils import listify, to_date


def ensure_list_of_string(s, name=""):
    if isinstance(s, string_types):
        return [s]

    result = list(s)
    for v in result:
        if not isinstance(v, string_types):
            raise ValueError("{}: expect string or list of string, got {!r}".format(name, v))
    return result


def ensure_list(s, name="", except_type=None):
    result = list(s)
    if except_type is None:
        return result
    for v in result:
        if not isinstance(v, except_type):
            raise ValueError("{}: expect {!r}, got {!r}".format(name, except_type, v))
    return result


def ensure_string(s, name="", decoding="utf-8"):
    if isinstance(s, binary_type):
        return s.decode(decoding)
    if not isinstance(s, text_type):
        raise ValueError("{}: expect a string, got {!r}".format(name, s))
    return s


def ensure_string_in(s, should_in, name="", decoding="utf-8"):
    s = ensure_string(s, name, decoding)
    if s not in should_in:
        raise TypeError("{}: expect value in {!r}".format(name, should_in))
    return s


def check_type(s, t, name=""):
    if not isinstance(s, t):
        raise ValueError("{}: expect value in type {}, got {!r}.".format(name, t, s))


def ensure_int(s, name=""):
    try:
        return int(s)
    except TypeError:
        raise ValueError("{}: expect int value, got {!r}.".format(name, s))


def check_items_in_container(items, should_in, name):
    items = listify(items)
    for item in items:
        if item not in should_in:
            raise ValueError(
                "{}: got invalided value {}, choose any in {}".format(name, item, should_in)
            )


def ensure_order(items, ordered):
    # type: (list, iter) -> list
    items = set(items)
    return [i for i in ordered if i in items]


def ensure_date_str(date):
    # type: (...) -> str
    date = to_date(date)
    return "%04d-%02d-%02d" % (date.year, date.month, date.day)


def ensure_date_int(date):
    date = to_date(date)
    return date.year * 10000 + date.month * 100 + date.day


def ensure_date_or_today_int(date):
    if date:
        return ensure_date_int(date)
    return _to_date_int(datetime.datetime.today())


def _to_date_int(date):
    # type: (datetime.datetime or datetime.date) -> int
    return date.year * 10000 + date.month * 100 + date.day


def ensure_date_range(start_date, end_date, delta=relativedelta(months=3)):
    if start_date is None and end_date is None:
        return _to_date_int(datetime.date.today() - delta), _to_date_int(datetime.date.today())

    if start_date is None:
        end_date = to_date(end_date)
        return _to_date_int(end_date - delta), _to_date_int(end_date)

    if end_date is None:
        start_date = to_date(start_date)
        return _to_date_int(start_date), _to_date_int(start_date + delta)

    s, e = ensure_date_int(start_date), ensure_date_int(end_date)
    if s > e:
        raise ValueError("invalid date range: [{!r}, {!r}]".format(start_date, end_date))
    return s, e


def ensure_dates_base_on_listed_date(instrument, start_date, end_date, market):
    from rqdatac.services.calendar import get_previous_trading_date, get_latest_trading_date
    if to_date(instrument.listed_date) > datetime.date.today():
        raise ValueError("instrument {} is not listed yet".format(instrument.order_book_id))

    if start_date is None:
        start_date = instrument.listed_date
    elif to_date(start_date) < to_date(instrument.listed_date):
        start_date = to_date(instrument.listed_date)
    elif instrument.de_listed_date != "0000-00-00" and to_date(start_date) >= to_date(instrument.de_listed_date):
        warnings.warn("{} has been delisted on {}".format(instrument.order_book_id, instrument.de_listed_date))
        return None, None

    if end_date is None:
        if instrument.de_listed_date != "0000-00-00":
            end_date = get_previous_trading_date(instrument.de_listed_date, market=market)
        else:
            end_date = get_latest_trading_date(market=market)
    elif instrument.de_listed_date != "0000-00-00" and to_date(end_date) >= to_date(instrument.de_listed_date):
        warnings.warn("{} has been delisted on {}".format(instrument.order_book_id, instrument.de_listed_date))
        end_date = get_previous_trading_date(instrument.de_listed_date, market=market)
    return start_date, end_date


def ensure_instruments(order_book_ids, type=None, market="cn"):
    order_book_ids = ensure_list_of_string(order_book_ids)
    from rqdatac.services.basic import _all_instruments_dict

    all_instruments = _all_instruments_dict(market)
    result = []
    for ob in set(order_book_ids):
        i = all_instruments.get(ob)
        if not i:
            warnings.warn("invalid order_book_id: {}".format(ob), stacklevel=0)
            continue
        if type is not None and i.type != type:
            warnings.warn(
                "expect {} instrument, got {}({}), ignored".format(type, i.type, ob), stacklevel=0
            )
            continue
        result.append(i)
    if not result:
        raise ValueError("order_book_ids: at least one valid instrument expected, got none")
    return result


def ensure_instruments_in_order(order_book_ids, type=None, market="cn"):
    order_book_ids = ensure_list_of_string(order_book_ids)
    from rqdatac.services.basic import _all_instruments_dict

    all_instruments = _all_instruments_dict(market)
    result = []
    unique = set()
    result_append = result.append
    unique_add = unique.add
    for ob in order_book_ids:
        i = all_instruments.get(ob)
        if not i:
            warnings.warn("invalid order_book_id: {}".format(ob), stacklevel=0)
            continue
        if type is not None and i.type != type:
            warnings.warn(
                "expect {} instrument, got {}({}), ignored".format(type, i.type, ob), stacklevel=0
            )
            continue
        if ob in unique:
            warnings.warn("duplicated order_book_id: {}".format(ob), stacklevel=0)
            continue
        unique_add(ob)
        result_append(i)
    if not result:
        raise ValueError("order_book_ids: at least one valid instrument expected, got none")
    return result


def ensure_order_book_ids(order_book_ids, type=None, market="cn"):
    order_book_ids = ensure_list_of_string(order_book_ids)
    from rqdatac.services.basic import _all_instruments_dict

    all_instruments = _all_instruments_dict(market)
    result = []
    for ob in set(order_book_ids):
        i = all_instruments.get(ob)
        if not i:
            warnings.warn("invalid order_book_id: {}".format(ob))
            continue
        if type is not None and i.type != type:
            warnings.warn("expect {} instrument, got {}({}), ignored".format(type, i.type, ob))
            continue
        result.append(i.order_book_id)
    if not result:
        raise ValueError("order_book_ids: at least one valid instrument expected, got none")
    return result


def ensure_order_book_id(ob, type=None, market="cn"):
    ob = ensure_string(ob, "order_book_id")
    from rqdatac.services.basic import _all_instruments_dict

    all_instruments = _all_instruments_dict(market)
    try:
        i = all_instruments[ob]
    except KeyError as e:
        raise ValueError("invalid order_book_id: {!s}".format(e))
    if type is not None and i.type != type:
        raise ValueError("expect {} instrument, got {}({}), ignored".format(type, i.type, ob))
    return i.order_book_id


def ensure_trading_date(date):
    from rqdatac.services.calendar import get_trading_dates, get_previous_trading_date, get_next_trading_date

    trading_dates = get_trading_dates(get_previous_trading_date(date), get_next_trading_date(date))
    if date not in trading_dates:
        raise ValueError(
            "expect a trading date, got {}, for reference {}".format(date.strftime("%Y%m%d"), trading_dates)
        )
    return date


import rqdatac.services.fund
import rqdatac.services.stock_status
import rqdatac.services.future
import rqdatac.services.ksh_auction_info
import rqdatac.client
import rqdatac.services.tmall
import rqdatac.services.basic
import rqdatac.services.get_price
import rqdatac.services.index
import rqdatac.services.calendar
import rqdatac.services.live
import rqdatac.services.structured_fund
import rqdatac.services.market_data
import rqdatac.services.convertible
import rqdatac.services.xueqiu
import rqdatac.services.options
import rqdatac.services.factor
import rqdatac.services.financial
import rqdatac.services.get_capital_flow
import rqdatac.services.shenwan
import rqdatac.services.concept
import rqdatac.services.constant

__version__: str = ...
init = rqdatac.client.init
reset = rqdatac.client.reset
concept_list = rqdatac.services.concept.concept_list
concept = rqdatac.services.concept.concept
concept_names = rqdatac.services.concept.concept_names
shenwan_industry = rqdatac.services.shenwan.shenwan_industry
shenwan_instrument_industry = rqdatac.services.shenwan.shenwan_instrument_industry
zx_industry = rqdatac.services.shenwan.zx_industry
zx_instrument_industry = rqdatac.services.shenwan.zx_instrument_industry
get_industry = rqdatac.services.shenwan.get_industry
get_instrument_industry = rqdatac.services.shenwan.get_instrument_industry
get_industry_mapping = rqdatac.services.shenwan.get_industry_mapping
industry_code = rqdatac.services.constant.IndustryCode
IndustryCode = rqdatac.services.constant.IndustryCode
sector_code = rqdatac.services.constant.SectorCode
SectorCode = rqdatac.services.constant.SectorCode
get_trading_dates = rqdatac.services.calendar.get_trading_dates
get_next_trading_date = rqdatac.services.calendar.get_next_trading_date
get_previous_trading_date = rqdatac.services.calendar.get_previous_trading_date
get_latest_trading_date = rqdatac.services.calendar.get_latest_trading_date
trading_date_offset = rqdatac.services.calendar.trading_date_offset
is_trading_date = rqdatac.services.calendar.is_trading_date
has_night_trading = rqdatac.services.calendar.has_night_trading
id_convert = rqdatac.services.basic.id_convert
instruments = rqdatac.services.basic.instruments
all_instruments = rqdatac.services.basic.all_instruments
sector = rqdatac.services.basic.sector
industry = rqdatac.services.basic.industry
get_future_contracts = rqdatac.services.basic.get_future_contracts


class futures:
    get_commission_margin = rqdatac.services.future.get_commission_margin
    get_contracts = rqdatac.services.basic.get_contracts
    get_dominant = rqdatac.services.future.get_dominant
    get_member_rank = rqdatac.services.future.get_member_rank
    get_warehouse_stocks = rqdatac.services.future.get_warehouse_stocks


jy_instrument_industry = rqdatac.services.basic.jy_instrument_industry


class econ:
    get_factors = rqdatac.services.basic.get_factors
    get_money_supply = rqdatac.services.basic.get_money_supply
    get_reserve_ratio = rqdatac.services.basic.get_reserve_ratio


get_main_shareholder = rqdatac.services.basic.get_main_shareholder
get_current_news = rqdatac.services.basic.get_current_news
get_trading_hours = rqdatac.services.basic.get_trading_hours
get_private_placement = rqdatac.services.basic.get_private_placement
get_share_transformation = rqdatac.services.basic.get_share_transformation


class user:
    get_quota = rqdatac.services.basic.get_quota


get_update_status = rqdatac.services.basic.get_update_status
info = rqdatac.services.basic.info


class convertible:
    all_instruments = rqdatac.services.convertible.all_instruments
    get_call_info = rqdatac.services.convertible.get_call_info
    get_cash_flow = rqdatac.services.convertible.get_cash_flow
    get_conversion_info = rqdatac.services.convertible.get_conversion_info
    get_conversion_price = rqdatac.services.convertible.get_conversion_price
    get_put_info = rqdatac.services.convertible.get_put_info
    instruments = rqdatac.services.convertible.instruments
    real_cash_flow = rqdatac.services.convertible.real_cash_flow


get_dominant_future = rqdatac.services.future.get_dominant_future
future_commission_margin = rqdatac.services.future.future_commission_margin
get_future_member_rank = rqdatac.services.future.get_future_member_rank
is_st_stock = rqdatac.services.stock_status.is_st_stock
_is_st_stock = rqdatac.services.stock_status._is_st_stock
is_suspended = rqdatac.services.stock_status.is_suspended
get_stock_connect = rqdatac.services.stock_status.get_stock_connect
get_securities_margin = rqdatac.services.stock_status.get_securities_margin
get_margin_stocks = rqdatac.services.stock_status.get_margin_stocks
get_shares = rqdatac.services.stock_status.get_shares
current_snapshot = rqdatac.services.live.current_snapshot
get_ticks = rqdatac.services.live.get_ticks
current_minute = rqdatac.services.live.current_minute
get_price = rqdatac.services.get_price.get_price


class options:
    get_contracts = rqdatac.services.get_price.get_contracts
    get_greeks = rqdatac.services.options.get_greeks


get_all_factor_names = rqdatac.services.factor.get_all_factor_names
get_factor = rqdatac.services.factor.get_factor
get_factor_return = rqdatac.services.factor.get_factor_return
get_factor_exposure = rqdatac.services.factor.get_factor_exposure
get_style_factor_exposure = rqdatac.services.factor.get_style_factor_exposure
get_descriptor_exposure = rqdatac.services.factor.get_descriptor_exposure
get_stock_beta = rqdatac.services.factor.get_stock_beta
get_factor_covariance = rqdatac.services.factor.get_factor_covariance
get_specific_return = rqdatac.services.factor.get_specific_return
get_specific_risk = rqdatac.services.factor.get_specific_risk
get_index_factor_exposure = rqdatac.services.factor.get_index_factor_exposure
Financials = rqdatac.services.financial.Financials
financials = rqdatac.services.financial.Financials
get_financials = rqdatac.services.financial.get_financials
PitFinancials = rqdatac.services.financial.PitFinancials
pit_financials = rqdatac.services.financial.PitFinancials
get_pit_financials = rqdatac.services.financial.get_pit_financials
get_fundamentals = rqdatac.services.financial.get_fundamentals
deprecated_fundamental_data = rqdatac.services.financial.deprecated_fundamental_data
current_performance = rqdatac.services.financial.current_performance
performance_forecast = rqdatac.services.financial.performance_forecast
Fundamentals = rqdatac.services.financial.Fundamentals
fundamentals = rqdatac.services.financial.Fundamentals
query = rqdatac.services.financial.query_entities


class fund:
    all_instruments = rqdatac.services.fund.all_instruments
    get_amc = rqdatac.services.fund.get_amc
    get_amc_rank = rqdatac.services.fund.get_amc_rank
    get_asset_allocation = rqdatac.services.fund.get_asset_allocation
    get_bond_stru = rqdatac.services.fund.get_bond_stru
    get_credit_quality = rqdatac.services.fund.get_credit_quality
    get_dividend = rqdatac.services.fund.get_dividend
    get_etf_cash_components = rqdatac.services.fund.get_etf_cash_components
    get_etf_components = rqdatac.services.fund.get_etf_components
    get_ex_factor = rqdatac.services.fund.get_ex_factor
    get_holdings = rqdatac.services.fund.get_holdings
    get_indicators = rqdatac.services.fund.get_indicators
    get_industry_allocation = rqdatac.services.fund.get_industry_allocation
    get_irr_sensitivity = rqdatac.services.fund.get_irr_sensitivity
    get_manager = rqdatac.services.fund.get_manager
    get_manager_info = rqdatac.services.fund.get_manager_info
    get_nav = rqdatac.services.fund.get_nav
    get_ratings = rqdatac.services.fund.get_ratings
    get_snapshot = rqdatac.services.fund.get_snapshot
    get_split = rqdatac.services.fund.get_split
    get_stock_change = rqdatac.services.fund.get_stock_change
    get_term_to_maturity = rqdatac.services.fund.get_term_to_maturity
    get_units_change = rqdatac.services.fund.get_units_change
    instruments = rqdatac.services.fund.instruments


get_capital_flow = rqdatac.services.get_capital_flow.get_capital_flow
get_open_auction_info = rqdatac.services.get_capital_flow.get_open_auction_info
index_components = rqdatac.services.index.index_components
index_weights = rqdatac.services.index.index_weights
index_indicator = rqdatac.services.index.index_indicator
get_ksh_auction_info = rqdatac.services.ksh_auction_info.get_ksh_auction_info
get_split = rqdatac.services.market_data.get_split
get_dividend = rqdatac.services.market_data.get_dividend
get_dividend_info = rqdatac.services.market_data.get_dividend_info
get_ex_factor = rqdatac.services.market_data.get_ex_factor
get_turnover_rate = rqdatac.services.market_data.get_turnover_rate
get_price_change_rate = rqdatac.services.market_data.get_price_change_rate
get_yield_curve = rqdatac.services.market_data.get_yield_curve
get_block_trade = rqdatac.services.market_data.get_block_trade


class fenji:
    get = rqdatac.services.structured_fund.get
    get_a_by_interest_rule = rqdatac.services.structured_fund.get_a_by_interest_rule
    get_a_by_yield = rqdatac.services.structured_fund.get_a_by_yield
    get_all = rqdatac.services.structured_fund.get_all


ecommerce = rqdatac.services.tmall.ecommerce


class xueqiu:
    history = rqdatac.services.xueqiu.history
    top_stocks = rqdatac.services.xueqiu.top_stocks


"""Screener page — stock screener results, KPI summary and performance chart."""

from nicegui import ui
from services.notifications import notify

_STOCKS = [
    {'ticker': 'AAPL',  'company': 'Apple Inc',       'sector': 'Technology',  'pe': 28.5, 'roe': 45.2, 'mkt_cap': 'Large',  'rating': 'Strong Buy', 'rating_cls': 'badge-success'},
    {'ticker': 'MSFT',  'company': 'Microsoft Corp',  'sector': 'Technology',  'pe': 32.1, 'roe': 38.7, 'mkt_cap': 'Large',  'rating': 'Buy',       'rating_cls': 'badge-success'},
    {'ticker': 'GOOGL', 'company': 'Alphabet Inc',    'sector': 'Technology',  'pe': 22.4, 'roe': 25.3, 'mkt_cap': 'Large',  'rating': 'Buy',       'rating_cls': 'badge-success'},
    {'ticker': 'NVDA',  'company': 'NVIDIA Corp',     'sector': 'Technology',  'pe': 58.2, 'roe': 69.8, 'mkt_cap': 'Large',  'rating': 'Hold',      'rating_cls': 'badge-warning'},
    {'ticker': 'JPM',   'company': 'JPMorgan Chase',  'sector': 'Finance',     'pe': 11.3, 'roe': 15.2, 'mkt_cap': 'Large',  'rating': 'Buy',       'rating_cls': 'badge-success'},
    {'ticker': 'JNJ',   'company': 'Johnson & Johnson','sector': 'Healthcare',  'pe': 15.8, 'roe': 23.4, 'mkt_cap': 'Large',  'rating': 'Hold',      'rating_cls': 'badge-warning'},
    {'ticker': 'XOM',   'company': 'ExxonMobil',      'sector': 'Energy',      'pe': 9.2,  'roe': 18.6, 'mkt_cap': 'Large',  'rating': 'Sell',      'rating_cls': 'badge-danger'},
    {'ticker': 'CRM',   'company': 'Salesforce Inc',  'sector': 'Technology',  'pe': 45.6, 'roe': 8.2,  'mkt_cap': 'Mid',    'rating': 'Hold',      'rating_cls': 'badge-warning'},
    {'ticker': 'AMD',   'company': 'AMD Inc',         'sector': 'Technology',  'pe': 42.3, 'roe': 12.5, 'mkt_cap': 'Mid',    'rating': 'Buy',       'rating_cls': 'badge-success'},
    {'ticker': 'PFE',   'company': 'Pfizer Inc',      'sector': 'Healthcare',  'pe': 12.1, 'roe': 15.8, 'mkt_cap': 'Large',  'rating': 'Strong Buy','rating_cls': 'badge-success'},
]

_PERFORMANCE = {
    'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
    'avg_pe':  [28.5, 29.2, 30.1, 31.5, 32.8, 31.2, 30.5, 29.8],
    'avg_roe': [25.3, 26.1, 27.2, 28.5, 29.1, 28.8, 27.5, 26.8],
}

_TT = {'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_AX = {'axisLine': {'lineStyle': {'color': '#e4e4e7'}}, 'axisTick': {'show': False},
       'axisLabel': {'color': '#71717a', 'fontSize': 11}}
_SL = {'splitLine': {'lineStyle': {'color': '#f4f4f5', 'type': 'dashed'}}}


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Screener').classes('page-title')
            ui.label('Screen stocks based on fundamental metrics and ratings.').classes('text-sm text-muted')
        ui.button('+ New Screen', color='white',
                  on_click=lambda: notify('Screening wizard coming soon', type='info')).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    buy_count = sum(1 for s in _STOCKS if s['rating'] in ['Strong Buy', 'Buy'])
    avg_pe = sum(s['pe'] for s in _STOCKS) / len(_STOCKS)
    avg_roe = sum(s['roe'] for s in _STOCKS) / len(_STOCKS)
    sectors = len(set(s['sector'] for s in _STOCKS))
    high_pe = sum(1 for s in _STOCKS if s['pe'] > 35)

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Stocks Passing', f'{buy_count} / {len(_STOCKS)}',  'meet criteria',              'text-success',                          'check_circle'),
            ('Avg P/E',        f'{avg_pe:.1f}',                    'price to earnings',          'text-info',                             'analytics'),
            ('Avg ROE',        f'{avg_roe:.1f}%',                  'return on equity',           'text-success' if avg_roe > 20 else 'text-warning','trending_up'),
            ('Sectors',        str(sectors),                      'covered in screen',          'text-info',                             'category'),
            ('High P/E',       str(high_pe),                      'above 35x multiple',         'text-warning' if high_pe else 'text-muted','warning'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Results table ─────────────────────────────────────────────
    with ui.element('div').classes('card mb-6'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label('Screen Results').classes('card-title')
                ui.label(f'{len(_STOCKS)} stocks matching criteria').classes('text-xs text-muted mt-1')
            ui.button('Refresh', color='white',
                      on_click=lambda: notify('Screen data refreshed', type='info')).props('flat no-caps').classes('button button-ghost button-sm')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Ticker', 'Company', 'Sector', 'P/E Ratio', 'ROE %', 'Market Cap', 'Rating']:
                        with ui.element('th'): ui.label(col)
            with ui.element('tbody'):
                for stock in _STOCKS:
                    pe_color = '#4ade80' if stock['pe'] < 25 else '#fbbf24' if stock['pe'] < 40 else '#f87171'
                    roe_color = '#4ade80' if stock['roe'] > 20 else '#fbbf24' if stock['roe'] > 10 else '#f87171'
                    with ui.element('tr'):
                        with ui.element('td'):
                            ui.label(stock['ticker']).classes('font-semi')
                        with ui.element('td'): ui.label(stock['company'])
                        with ui.element('td'): ui.label(stock['sector'])
                        with ui.element('td'):
                            ui.label(f'{stock["pe"]:.1f}').classes('text-sm')
                            ui.label('x multiple').classes('text-xs text-muted')
                        with ui.element('td'):
                            ui.label(f'{stock["roe"]:.1f}%').classes('text-sm')
                        with ui.element('td'): ui.label(stock['mkt_cap'])
                        with ui.element('td'):
                            ui.label(stock['rating']).classes(f'badge {stock["rating_cls"]}')

    # ── Performance chart ────────────────────────────────────────
    with ui.element('div').classes('card mb-4').style('padding:20px 20px 12px 20px'):
        with ui.row().classes('items-start justify-between mb-1'):
            with ui.column().classes('gap-0'):
                ui.label('Metric Trends').classes('card-title')
                ui.label('Average P/E and ROE over time').classes('text-xs text-muted mt-1')
        ui.echart({
            'tooltip': {'trigger': 'axis', **_TT,
                        'axisPointer': {'type': 'cross', 'label': {'backgroundColor': '#60a5fa'}}},
            'legend': {'data': ['Avg P/E', 'Avg ROE'], 'top': 0,
                       'textStyle': {'color': '#71717a', 'fontSize': 12},
                       'itemWidth': 10, 'itemHeight': 10, 'itemGap': 16},
            'grid': {'left': '2%', 'right': '2%', 'bottom': '2%', 'top': '14%', 'containLabel': True},
            'xAxis': {'type': 'category', 'data': _PERFORMANCE['months'], 'boundaryGap': False, **_AX},
            'yAxis': {**_AX, **_SL, 'type': 'value',
                      'axisLabel': {'color': '#71717a', 'fontSize': 11}},
            'series': [
                {'name': 'Avg P/E', 'type': 'line', 'smooth': True,
                 'data': _PERFORMANCE['avg_pe'], 'symbol': 'circle', 'symbolSize': 5,
                 'lineStyle': {'width': 2.5, 'color': '#60a5fa'},
                 'itemStyle': {'color': '#60a5fa'},
                 'areaStyle': {'color': '#60a5fa', 'opacity': 0.10}},
                {'name': 'Avg ROE', 'type': 'line', 'smooth': True,
                 'data': _PERFORMANCE['avg_roe'], 'symbol': 'circle', 'symbolSize': 5,
                 'lineStyle': {'width': 2.5, 'color': '#4ade80'},
                 'itemStyle': {'color': '#4ade80'},
                 'areaStyle': {'color': '#4ade80', 'opacity': 0.10}},
            ],
        }).classes('w-full').style('height:380px')
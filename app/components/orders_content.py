"""Portfolio page — KPI summary, sector allocation chart and holdings table."""

from nicegui import ui
from services.notifications import notify

# ── Mock data ─────────────────────────────────────────────────────────────────
_HOLDINGS = [
    {'id': 'POS-1001', 'ticker': 'AAPL',  'company': 'Apple Inc',       'shares': 150, 'value': '$ 28,500',  'gain_loss': '+$4,200',  'gain_pct': '+17.3%', 'status': 'Gain',    'open_date': 'Jan 15, 2025'},
    {'id': 'POS-1002', 'ticker': 'MSFT',  'company': 'Microsoft Corp',  'shares': 80,  'value': '$ 32,000',  'gain_loss': '+$6,400',  'gain_pct': '+25.0%', 'status': 'Gain',    'open_date': 'Dec 10, 2024'},
    {'id': 'POS-1003', 'ticker': 'NVDA',  'company': 'NVIDIA Corp',     'shares': 45,  'value': '$ 18,000',  'gain_loss': '+$8,100',  'gain_pct': '+82.0%', 'status': 'Gain',    'open_date': 'Feb 20, 2025'},
    {'id': 'POS-1004', 'ticker': 'GOOGL', 'company': 'Alphabet Inc',    'shares': 100, 'value': '$ 14,500',  'gain_loss': '-$1,500',  'gain_pct': '-9.4%',  'status': 'Loss',    'open_date': 'Mar 05, 2025'},
    {'id': 'POS-1005', 'ticker': 'TSLA',  'company': 'Tesla Inc',       'shares': 60,  'value': '$ 15,000',  'gain_loss': '-$2,400',  'gain_pct': '-13.8%', 'status': 'Loss',    'open_date': 'Feb 28, 2025'},
    {'id': 'POS-1006', 'ticker': 'JPM',   'company': 'JPMorgan Chase',  'shares': 200, 'value': '$ 48,000',  'gain_loss': '+$3,600',  'gain_pct': '+8.1%',  'status': 'Gain',    'open_date': 'Jan 22, 2025'},
]

_SECTOR_COUNTS = {'Technology': 4, 'Finance': 1, 'Consumer': 1}
_MONTHLY = {
    'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
    'portfolio': [100000, 105000, 112000, 108000, 115000, 118000, 122000, 125000],
    'benchmark': [100000, 102000, 105000, 103000, 107000, 109000, 111000, 113000],
}

_STATUS_STYLE = {
    'Gain':    ('badge-success', '#4ade80'),
    'Loss':    ('badge-danger',  '#f87171'),
    'Watch':   ('badge-warning', '#fbbf24'),
    'Hold':    ('badge-info',    '#60a5fa'),
}

_TT  = {'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_AX  = {'axisLine': {'lineStyle': {'color': '#e4e4e7'}}, 'axisTick': {'show': False},
        'axisLabel': {'color': '#71717a', 'fontSize': 11}}
_SL  = {'splitLine': {'lineStyle': {'color': '#f4f4f5', 'type': 'dashed'}}}


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Portfolio').classes('page-title')
            ui.label('Track your holdings and investment performance.').classes('text-sm text-muted')
        ui.button('+ Add Position', color='white', on_click=_new_position_dialog).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    total_value = 156000
    total_gain = 18400
    gain_positions = sum(1 for h in _HOLDINGS if h['status'] == 'Gain')
    loss_positions = sum(1 for h in _HOLDINGS if h['status'] == 'Loss')

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Total Positions', str(len(_HOLDINGS)),              'active holdings',  'text-info',    'account_balance'),
            ('Total Value',     f'$ {total_value:,}',              'portfolio value',  'text-success', 'payments'),
            ('Total Gain',      f'+$ {total_gain:,}',              'unrealized P&L',   'text-success', 'trending_up'),
            ('Winners',         str(gain_positions),               'profitable',       'text-success', 'check_circle'),
            ('Losers',          str(loss_positions),               'under water',      'text-danger',  'cancel'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Charts row ────────────────────────────────────────────────
    with ui.row().classes('gap-4 flex-wrap w-full mb-6'):

        # Sector allocation donut
        with ui.element('div').classes('card').style('flex:1;min-width:280px'):
            ui.label('Holdings by Sector').classes('card-title mb-1')
            ui.echart({
                'tooltip': {'trigger': 'item', **_TT},
                'legend':  {'bottom': 0, 'left': 'center',
                            'textStyle': {'color': '#71717a', 'fontSize': 12},
                            'itemWidth': 10, 'itemHeight': 10, 'itemGap': 12},
                'series': [{
                    'type': 'pie', 'radius': ['46%', '70%'], 'center': ['50%', '44%'],
                    'avoidLabelOverlap': False,
                    'label': {'show': False},
                    'emphasis': {'label': {'show': True, 'fontSize': 13, 'fontWeight': 'bold', 'color': '#09090b'}},
                    'labelLine': {'show': False},
                    'data': [
                        {'name': k, 'value': v, 'itemStyle': {'color': c}}
                        for (k, v), c in zip(_SECTOR_COUNTS.items(), ['#3b82f6', '#4ade80', '#f59e0b'])
                    ],
                }],
            }).classes('w-full').style('height:280px')

        # Portfolio vs Benchmark
        with ui.element('div').classes('card').style('flex:2;min-width:360px'):
            ui.label('Portfolio vs Benchmark (SPY)').classes('card-title mb-1')
            ui.echart({
                'tooltip': {'trigger': 'axis', **_TT, 'axisPointer': {'type': 'cross'}},
                'legend': {'data': ['Portfolio', 'Benchmark'], 'top': 0,
                           'textStyle': {'color': '#71717a', 'fontSize': 12}},
                'grid': {'left': '3%', 'right': '4%', 'bottom': '3%', 'top': '14%', 'containLabel': True},
                'xAxis': {'type': 'category', 'data': _MONTHLY['months'], **_AX},
                'yAxis': [
                    {**_AX, **_SL, 'type': 'value', 'name': 'Value ($)',
                     'axisLabel': {':formatter': 'v => "$" + (v/1000) + "k"', 'color': '#71717a', 'fontSize': 11}},
                ],
                'series': [
                    {'name': 'Portfolio', 'type': 'line', 'smooth': True,
                     'data': _MONTHLY['portfolio'], 'symbol': 'circle', 'symbolSize': 6,
                     'lineStyle': {'width': 2.5, 'color': '#4ade80'},
                     'itemStyle': {'color': '#4ade80', 'borderWidth': 2, 'borderColor': '#fff'},
                     'areaStyle': {'color': '#4ade80', 'opacity': 0.1}},
                    {'name': 'Benchmark', 'type': 'line', 'smooth': True,
                     'data': _MONTHLY['benchmark'], 'symbol': 'circle', 'symbolSize': 6,
                     'lineStyle': {'width': 2.5, 'color': '#60a5fa', 'type': 'dashed'},
                     'itemStyle': {'color': '#60a5fa', 'borderWidth': 2, 'borderColor': '#fff'}},
                ],
            }).classes('w-full').style('height:280px')

    # ── Holdings table ────────────────────────────────────────────
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label('Holdings').classes('card-title')
                ui.label(f'{len(_HOLDINGS)} positions').classes('text-xs text-muted mt-1')
            ui.button('Rebalance', color='white',
                      on_click=lambda: notify('Rebalancing wizard opening…', type='info')).props('flat no-caps').classes('button button-ghost button-sm')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Position ID', 'Ticker', 'Company', 'Shares', 'Value', 'Gain/Loss', 'Status', 'Open Date']:
                        with ui.element('th'): ui.label(col)
            with ui.element('tbody'):
                for h in _HOLDINGS:
                    badge_cls, _ = _STATUS_STYLE.get(h['status'], ('badge-default', '#a1a1aa'))
                    with ui.element('tr'):
                        with ui.element('td'):
                            ui.label(h['id']).classes('font-semi text-sm')
                        with ui.element('td'): ui.label(h['ticker'])
                        with ui.element('td'): ui.label(h['company'])
                        with ui.element('td'): ui.label(str(h['shares']))
                        with ui.element('td'):
                            ui.label(h['value']).classes('font-semi')
                        with ui.element('td'):
                            ui.label(h['gain_loss']).classes('text-success' if h['status'] == 'Gain' else 'text-danger')
                            ui.label(h['gain_pct']).classes('text-xs text-muted')
                        with ui.element('td'):
                            ui.label(h['status']).classes(f'badge {badge_cls}')
                        with ui.element('td'):
                            ui.label(h['open_date']).classes('text-muted')


def _new_position_dialog() -> None:
    with ui.dialog(value=True) as dlg, ui.card().style('min-width:380px;padding:28px 32px'):
        with ui.row().classes('items-center justify-between w-full mb-4'):
            ui.label('New Position').classes('card-title')
            ui.button(icon='close', color='white', on_click=dlg.close).props('flat round dense').classes('button button-ghost')
        with ui.column().classes('gap-4 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label('Ticker').classes('field-label')
                ui.select(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'JPM'],
                          value='AAPL').classes('w-full').props('outlined dense')
            with ui.element('div').classes('w-full'):
                ui.label('Company').classes('field-label')
                ui.input(value='Apple Inc').classes('w-full').props('outlined dense')
            with ui.row().classes('gap-4 w-full'):
                with ui.element('div').classes('flex-1'):
                    ui.label('Shares').classes('field-label')
                    ui.number(value=100, min=1).classes('w-full').props('outlined dense')
                with ui.element('div').classes('flex-1'):
                    ui.label('Entry Price').classes('field-label')
                    ui.number(value=150.00, min=0.01).classes('w-full').props('outlined dense')
        ui.element('div').classes('divider mt-4 mb-4')
        with ui.row().classes('gap-3 justify-end w-full'):
            ui.button('Cancel', color='white', on_click=dlg.close).props('flat no-caps').classes('button button-outline button-sm')
            ui.button('Add Position', color='white', on_click=lambda: [
                notify('Position added successfully', type='positive', title='Position Added'),
                dlg.close(),
            ]).props('flat no-caps').classes('button button-primary button-sm')
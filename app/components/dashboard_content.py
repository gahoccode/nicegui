"""Dashboard page — Fundamental metrics, price trend, sector allocation and RSI charts."""

from nicegui import ui
import services.dashboard_data as data
from services.notifications import notify


# ── Shared EChart base style ─────────────────────────────────────────────────

_GRID    = {'left': '3%', 'right': '3%', 'bottom': '3%', 'top': '12%', 'containLabel': True}
_TT_AXIS = {'trigger': 'axis', 'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_TT_ITEM = {'trigger': 'item', 'backgroundColor': '#fff', 'borderColor': '#e4e4e7', 'textStyle': {'color': '#09090b', 'fontSize': 12}}
_LEGEND  = {'textStyle': {'color': '#71717a', 'fontSize': 12}}


# ── KPI helpers ──────────────────────────────────────────────────────────────

def _kpi_card(container, label: str, icon: str, key: str, kpis: dict) -> dict:
    v    = kpis[key]
    val  = v['value']
    d    = v['delta']
    unit = v['unit']
    refs = {}
    with container:
        with ui.element('div').classes('card flex-1').style('min-width:160px'):
            with ui.row().classes('items-center justify-between mb-3'):
                ui.label(label).classes('label-text')
                ui.icon(icon).style('font-size:1.2rem;color:var(--muted-fg)')
            refs['value'] = ui.label(f"{val}{unit}").classes('text-2xl font-bold')
            delta_color  = 'text-success' if d >= 0 else 'text-danger'
            delta_prefix = '▲' if d >= 0 else '▼'
            refs['delta'] = ui.label(f"{delta_prefix} {abs(d)}{unit} vs last period").classes(f'text-xs {delta_color} mt-1')
    return refs


# ── Chart builders ───────────────────────────────────────────────────────────

def _price_chart(price_data: dict):
    return ui.echart({
        'tooltip': {**_TT_AXIS, 'axisPointer': {'type': 'cross', 'label': {'backgroundColor': '#18181b'}}},
        'legend': {**_LEGEND, 'data': ['Price', 'MA(7)'], 'left': 'center', 'top': 0},
        'grid': {'left': '3%', 'right': '3%', 'bottom': '3%', 'top': '14%', 'containLabel': True},
        'xAxis': {'type': 'category', 'boundaryGap': False, 'data': price_data['days'],
                  'axisLine': {'lineStyle': {'color': '#e4e4e7'}},
                  'axisTick': {'show': False},
                  'axisLabel': {'color': '#71717a', 'fontSize': 11}},
        'yAxis': {'type': 'value',
                  'splitLine': {'lineStyle': {'color': '#f4f4f5', 'type': 'dashed'}},
                  'axisLabel': {':formatter': 'v => "$" + v.toFixed(0)', 'color': '#71717a', 'fontSize': 11}},
        'series': [
            {
                'name': 'Price', 'type': 'line', 'smooth': 0.3,
                'data': price_data['price'],
                'symbol': 'circle', 'symbolSize': 6,
                'lineStyle': {'width': 2.5, 'color': '#64748b'},
                'itemStyle': {'color': '#64748b', 'borderWidth': 2, 'borderColor': '#fff'},
                'emphasis': {'focus': 'series'},
            },
            {
                'name': 'MA(7)', 'type': 'line', 'smooth': 0.3,
                'data': price_data['ma'], 'symbol': 'diamond', 'symbolSize': 7,
                'lineStyle': {'width': 2.5, 'type': 'dashed', 'color': '#60a5fa'},
                'itemStyle': {'color': '#60a5fa', 'borderWidth': 2, 'borderColor': '#fff'},
                'emphasis': {'focus': 'series'},
            },
        ],
    }).classes('w-full').style('height:300px')


def _donut_chart(allocation: list):
    return ui.echart({
        'tooltip': _TT_ITEM,
        'legend': {**_LEGEND, 'orient': 'horizontal', 'bottom': 0, 'left': 'center',
                   'itemWidth': 10, 'itemHeight': 10, 'itemGap': 12},
        'color': ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
        'series': [{
            'type': 'pie', 'radius': ['44%', '68%'], 'center': ['50%', '44%'],
            'avoidLabelOverlap': False,
            'label': {'show': False},
            'emphasis': {'label': {'show': True, 'fontSize': 13, 'fontWeight': 'bold', 'color': '#09090b'}},
            'labelLine': {'show': False},
            'data': allocation,
        }],
    }).classes('w-full').style('height:260px')


def _bar_chart(volume: dict):
    return ui.echart({
        'tooltip': _TT_AXIS,
        'legend': {**_LEGEND, 'data': ['Buy Volume', 'Sell Volume'], 'left': 'center', 'top': 0},
        'grid': _GRID,
        'xAxis': {'type': 'category', 'data': volume['days'],
                  'axisLine': {'lineStyle': {'color': '#e4e4e7'}},
                  'axisLabel': {'color': '#71717a', 'fontSize': 11}},
        'yAxis': {'type': 'value', 'splitLine': {'lineStyle': {'color': '#f4f4f5'}},
                  'axisLabel': {'color': '#71717a', 'fontSize': 11}},
        'series': [
            {'name': 'Buy Volume', 'type': 'bar', 'data': volume['buy_volume'],
             'barMaxWidth': 32, 'itemStyle': {'color': '#4ade80', 'borderRadius': [4, 4, 0, 0]}},
            {'name': 'Sell Volume', 'type': 'bar', 'data': volume['sell_volume'],
             'barMaxWidth': 32, 'itemStyle': {'color': '#f87171', 'borderRadius': [4, 4, 0, 0]}},
        ],
    }).classes('w-full').style('height:240px')


def _area_chart(rsi_data: dict):
    return ui.echart({
        'tooltip': {**_TT_AXIS, 'axisPointer': {'type': 'cross', 'label': {'backgroundColor': '#8b5cf6'}}},
        'legend': {**_LEGEND, 'data': ['RSI', 'Overbought', 'Oversold'], 'left': 'center', 'top': 0},
        'grid': _GRID,
        'xAxis': {'type': 'category', 'boundaryGap': False, 'data': rsi_data['periods'],
                  'axisLabel': {'color': '#71717a', 'fontSize': 10, 'interval': 2},
                  'axisLine': {'lineStyle': {'color': '#e4e4e7'}}},
        'yAxis': {'type': 'value', 'min': 0, 'max': 100,
                  'splitLine': {'lineStyle': {'color': '#f4f4f5'}},
                  'axisLabel': {':formatter': 'v => v', 'color': '#71717a', 'fontSize': 11}},
        'series': [
            {'name': 'RSI', 'type': 'line', 'smooth': True,
             'data': rsi_data['rsi'], 'symbol': 'none',
             'lineStyle': {'width': 2, 'color': '#8b5cf6'},
             'itemStyle': {'color': '#8b5cf6'},
             'areaStyle': {'color': '#8b5cf6', 'opacity': 0.18}},
            {'name': 'Overbought', 'type': 'line',
             'data': rsi_data['overbought'], 'symbol': 'none',
             'lineStyle': {'width': 1.5, 'type': 'dashed', 'color': '#ef4444'},
             'itemStyle': {'color': '#ef4444'}},
            {'name': 'Oversold', 'type': 'line',
             'data': rsi_data['oversold'], 'symbol': 'none',
             'lineStyle': {'width': 1.5, 'type': 'dashed', 'color': '#4ade80'},
             'itemStyle': {'color': '#4ade80'}},
        ],
    }).classes('w-full').style('height:240px')


# ── Main entry point ─────────────────────────────────────────────────────────

def content() -> None:

    # ── Header ──────────────────────────────────────────────────
    with ui.row().classes('w-full items-center justify-between mb-2'):
        with ui.column().classes('gap-0'):
            ui.label('Market Overview').classes('page-title')
            ui.label('Fundamental & Technical Analysis').classes('text-sm text-muted')
        refresh_btn = ui.button('Refresh', icon='refresh', color='white') \
            .props('flat no-caps').classes('button button-outline')

    ui.element('div').classes('divider mb-4')

    # ── KPI cards (Fundamental Metrics) ──────────────────────────
    kpis = data.get_kpis()
    kpi_refs = {}
    with ui.row().classes('w-full gap-4 flex-wrap mb-4') as kpi_row:
        kpi_refs['current_ratio']  = _kpi_card(kpi_row, 'Current Ratio',  'account_balance',      'current_ratio',  kpis)
        kpi_refs['quick_ratio']    = _kpi_card(kpi_row, 'Quick Ratio',    'speed',                'quick_ratio',    kpis)
        kpi_refs['roe']            = _kpi_card(kpi_row, 'ROE',            'trending_up',          'roe',            kpis)
        kpi_refs['asset_turnover'] = _kpi_card(kpi_row, 'Asset Turnover', 'autorenew',            'asset_turnover', kpis)

    # ── Row 2 — Price trend + Sector allocation ──────────────────
    with ui.row().classes('w-full gap-4 flex-wrap mb-4'):
        with ui.element('div').classes('card flex-1').style('min-width:320px'):
            with ui.row().classes('items-center justify-between mb-3'):
                ui.label('Price Trend').classes('section-title')
                ui.label('Last 30 days').classes('text-xs text-muted')
            price_data  = data.get_price_series()
            price_chart = _price_chart(price_data)

        with ui.element('div').classes('card').style('min-width:240px;width:280px'):
            with ui.row().classes('items-center justify-between mb-3'):
                ui.label('Sector Allocation').classes('section-title')
                ui.label('Current').classes('text-xs text-muted')
            allocation_data = data.get_sector_allocation()
            donut_chart     = _donut_chart(allocation_data)

    # ── Row 3 — Volume analysis + RSI ─────────────────────────────
    with ui.row().classes('w-full gap-4 flex-wrap mb-4'):
        with ui.element('div').classes('card flex-1').style('min-width:280px'):
            with ui.row().classes('items-center justify-between mb-3'):
                ui.label('Volume Analysis').classes('section-title')
                ui.label('Last 7 days').classes('text-xs text-muted')
            volume_data = data.get_volume_analysis()
            bar_chart   = _bar_chart(volume_data)

        with ui.element('div').classes('card flex-1').style('min-width:280px'):
            with ui.row().classes('items-center justify-between mb-3'):
                ui.label('RSI Indicator').classes('section-title')
                ui.label('Last 24 periods').classes('text-xs text-muted')
            rsi_data    = data.get_rsi_series()
            area_chart  = _area_chart(rsi_data)

    # ── Refresh handler ──────────────────────────────────────────
    def refresh() -> None:
        # KPIs
        new_kpis = data.get_kpis()
        for key, refs in kpi_refs.items():
            v    = new_kpis[key]
            unit = v['unit']
            val  = v['value']
            d    = v['delta']
            refs['value'].set_text(f"{val}{unit}")
            delta_color  = 'text-success' if d >= 0 else 'text-danger'
            delta_prefix = '▲' if d >= 0 else '▼'
            refs['delta'].set_text(f"{delta_prefix} {abs(d)}{unit} vs last period")
            refs['delta'].classes(replace=f'text-xs {delta_color} mt-1')

        # Price chart
        price = data.get_price_series()
        price_chart.options['xAxis']['data']     = price['days']
        price_chart.options['series'][0]['data'] = price['price']
        price_chart.options['series'][1]['data'] = price['ma']
        price_chart.update()

        # Donut
        donut_chart.options['series'][0]['data'] = data.get_sector_allocation()
        donut_chart.update()

        # Bar chart
        volume = data.get_volume_analysis()
        bar_chart.options['xAxis']['data']       = volume['days']
        bar_chart.options['series'][0]['data']   = volume['buy_volume']
        bar_chart.options['series'][1]['data']   = volume['sell_volume']
        bar_chart.update()

        # Area chart
        rsi = data.get_rsi_series()
        area_chart.options['xAxis']['data']      = rsi['periods']
        area_chart.options['series'][0]['data']  = rsi['rsi']
        area_chart.options['series'][1]['data']  = rsi['overbought']
        area_chart.options['series'][2]['data']  = rsi['oversold']
        area_chart.update()

        notify('Dashboard refreshed', type='positive', title='Refreshed')

    refresh_btn.on('click', refresh)
"""Watchlist page — AG Grid stock list with live search, signal badges and KPI cards."""

import random
from nicegui import ui
from services.notifications import notify

_SECTORS  = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer']
_TICKERS  = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'JPM', 'V', 'JNJ',
             'UNH', 'HD', 'PG', 'MA', 'DIS', 'PYPL', 'ADBE', 'NFLX', 'CMCSA', 'PEP']
_COMPANIES = {
    'AAPL': 'Apple Inc', 'MSFT': 'Microsoft Corp', 'GOOGL': 'Alphabet Inc', 'AMZN': 'Amazon.com Inc',
    'NVDA': 'NVIDIA Corp', 'META': 'Meta Platforms', 'TSLA': 'Tesla Inc', 'JPM': 'JPMorgan Chase',
    'V': 'Visa Inc', 'JNJ': 'Johnson & Johnson', 'UNH': 'UnitedHealth', 'HD': 'Home Depot',
    'PG': 'Procter & Gamble', 'MA': 'Mastercard Inc', 'DIS': 'Walt Disney Co', 'PYPL': 'PayPal Holdings',
    'ADBE': 'Adobe Inc', 'NFLX': 'Netflix Inc', 'CMCSA': 'Comcast Corp', 'PEP': 'PepsiCo Inc'
}
_EXCHANGES = ['NASDAQ', 'NYSE', 'LSE', 'TSE']

_ROWS = [
    {'id': f'TKR-{1000+i}',
     'ticker':      _TICKERS[i % len(_TICKERS)],
     'company':     _COMPANIES[_TICKERS[i % len(_TICKERS)]],
     'exchange':    _EXCHANGES[i % len(_EXCHANGES)],
     'sector':      _SECTORS[i % len(_SECTORS)],
     'signal':      s,
     'target_price': round(random.uniform(100, 500), 2),
     'market_cap':   round(random.uniform(50, 3000) / 10, 1)}
    for i, s in enumerate(
        ['Buy', 'Hold', 'Sell', 'Buy', 'Watch',
         'Hold', 'Buy', 'Sell', 'Hold', 'Watch',
         'Buy', 'Hold', 'Sell', 'Buy', 'Watch']
    )
]


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Watchlist').classes('page-title')
            ui.label('Track stocks and monitor trading signals.').classes('text-sm text-muted')
        ui.button('+ Add Stock', color='white',
                  on_click=lambda: _add_row(grid_ref, notify)).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    counts = {'Buy': sum(1 for r in _ROWS if r['signal'] == 'Buy'),
              'Hold': sum(1 for r in _ROWS if r['signal'] == 'Hold'),
              'Sell': sum(1 for r in _ROWS if r['signal'] == 'Sell'),
              'Watch': sum(1 for r in _ROWS if r['signal'] == 'Watch')}
    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Total Watched', str(len(_ROWS)),           'stocks tracked',     'text-info',    'visibility'),
            ('Buy Signals',   str(counts['Buy']),        'bullish outlook',    'text-success', 'trending_up'),
            ('Hold',          str(counts['Hold']),       'neutral stance',     'text-info',    'pause'),
            ('Watch',         str(counts['Watch']),      'monitoring closely', 'text-warning', 'radar'),
            ('Sell Signals',  str(counts['Sell']),       'bearish outlook',    'text-danger',  'trending_down'),
        ]:
            with ui.element('div').classes('card').style('min-width:150px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Toolbar ───────────────────────────────────────────────────
    grid_ref = {}
    with ui.row().classes('w-full items-center gap-3 mb-3 flex-wrap'):
        search = ui.input(placeholder='Search stocks…').classes('flex-1').props('outlined rounded dense clearable')
        search.add_slot('prepend', '<q-icon name="search" />')
        ui.button('Export', color='white',
                  on_click=lambda: notify('Export started', type='info', title='Export')).props('flat no-caps').classes('button button-outline button-sm')

    # ── AG Grid ───────────────────────────────────────────────────
    grid = ui.aggrid({
        'columnDefs': [
            {'headerName': 'Ticker',     'field': 'ticker',        'width': 90, 'pinned': 'left'},
            {'headerName': 'Company',    'field': 'company',       'filter': 'agTextColumnFilter',   'floatingFilter': True, 'flex': 1},
            {'headerName': 'Exchange',   'field': 'exchange',      'filter': 'agTextColumnFilter',   'floatingFilter': True, 'width': 100},
            {'headerName': 'Sector',     'field': 'sector',        'filter': 'agTextColumnFilter',   'floatingFilter': True, 'width': 110},
            {'headerName': 'Signal',     'field': 'signal',        'width': 90},
            {'headerName': 'Target ($)', 'field': 'target_price',  'width': 100, 'filter': 'agNumberColumnFilter'},
            {'headerName': 'Mkt Cap (B)','field': 'market_cap',    'width': 100, 'filter': 'agNumberColumnFilter'},
        ],
        'rowData': _ROWS,
        'rowSelection': {'mode': 'multiRow'},
        'domLayout': 'autoHeight',
        'suppressCellFocus': True,
    }).classes('w-full')
    grid_ref['grid'] = grid

    search.on('update:model-value', lambda e: grid.run_grid_method(
        'setGridOption', 'quickFilterText', e.args or ''))


def _add_row(grid_ref, notify_fn):
    grid = grid_ref.get('grid')
    if not grid:
        return
    i = len(grid.options['rowData'])
    s = random.choice(['Buy', 'Hold', 'Sell', 'Watch'])
    ticker = random.choice(_TICKERS)
    row = {
        'id':          f'TKR-{2000+i}',
        'ticker':      ticker,
        'company':     _COMPANIES[ticker],
        'exchange':    random.choice(_EXCHANGES),
        'sector':      random.choice(_SECTORS),
        'signal':      s,
        'target_price': round(random.uniform(100, 500), 2),
        'market_cap':   round(random.uniform(50, 3000) / 10, 1),
    }
    grid.options['rowData'].append(row)
    grid.run_grid_method('ensureIndexVisible', i)
    grid.update()
    notify_fn(f'Added {row["ticker"]}', type='positive', title='Stock added')
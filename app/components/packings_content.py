"""Backtest page — Kanban board (Running → Completed → Archived) with strategy results."""

from nicegui import ui
from services.notifications import notify

_COLUMNS = {
    'Running': [
        {'id': 'BT-5001', 'strategy': 'Moving Avg Crossover', 'asset': 'AAPL',  'timeframe': '1D', 'trades': 0,   'duration': '2h 15m', 'return': '0.0%'},
        {'id': 'BT-5002', 'strategy': 'RSI Mean Reversion',   'asset': 'SPY',   'timeframe': '4H', 'trades': 0,   'duration': '1h 30m', 'return': '0.0%'},
        {'id': 'BT-5003', 'strategy': 'Bollinger Bands',      'asset': 'NVDA',  'timeframe': '1H', 'trades': 0,   'duration': '45m',   'return': '0.0%'},
        {'id': 'BT-5004', 'strategy': 'MACD Divergence',      'asset': 'BTC',   'timeframe': '15M', 'trades': 0,  'duration': '20m',   'return': '0.0%'},
    ],
    'Completed': [
        {'id': 'BT-5005', 'strategy': 'Moving Avg Crossover', 'asset': 'MSFT',  'timeframe': '1D', 'trades': 156, 'duration': '2020-2025', 'return': '+24.5%'},
        {'id': 'BT-5006', 'strategy': 'RSI Mean Reversion',   'asset': 'QQQ',   'timeframe': '1D', 'trades': 89,  'duration': '2019-2025', 'return': '+18.2%'},
        {'id': 'BT-5007', 'strategy': 'Pairs Trading',        'asset': 'XLE/XLB','timeframe': '1D', 'trades': 42,  'duration': '2021-2025', 'return': '+12.8%'},
    ],
    'Archived': [
        {'id': 'BT-5008', 'strategy': 'Moving Avg Crossover', 'asset': 'TSLA',  'timeframe': '4H', 'trades': 234, 'duration': '2020-2024', 'return': '-5.3%'},
        {'id': 'BT-5009', 'strategy': 'Momentum Factor',      'asset': 'SPY',   'timeframe': '1W', 'trades': 78,  'duration': '2018-2024', 'return': '+31.2%'},
        {'id': 'BT-5010', 'strategy': 'Volatility Breakout',  'asset': 'BTC',   'timeframe': '1D', 'trades': 112, 'duration': '2022-2024', 'return': '+45.7%'},
        {'id': 'BT-5011', 'strategy': 'Mean Reversion',       'asset': 'GLD',   'timeframe': '1D', 'trades': 67,  'duration': '2020-2024', 'return': '+8.4%'},
        {'id': 'BT-5012', 'strategy': 'Sector Rotation',      'asset': 'XLK/XLV','timeframe': '1M', 'trades': 24, 'duration': '2019-2024', 'return': '+22.1%'},
    ],
}

_COL_STYLE = {
    'Running':    ('badge-info',    'text-info',    'play_circle',    '#60a5fa'),
    'Completed':  ('badge-success', 'text-success', 'check_circle',   '#4ade80'),
    'Archived':   ('badge-warning', 'text-warning', 'archive',        '#fbbf24'),
}

_COL_ACTION = {
    'Running':    ('Cancel',     'button-outline',  'warning', 'Cancelled'),
    'Completed':  ('Archive',    'button-success',  'positive', 'Archived'),
    'Archived':   ('Rerun',      'button-primary',  'info',     'Rerunning'),
}


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Backtest').classes('page-title')
            ui.label('Run and analyze trading strategy backtests.').classes('text-sm text-muted')
        ui.button('+ New Backtest', color='white',
                  on_click=lambda: notify('Backtest configuration wizard coming soon', type='info')).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── Pipeline summary strip ────────────────────────────────────
    total       = sum(len(v) for v in _COLUMNS.values())
    total_trades = sum(j['trades'] for jobs in _COLUMNS.values() for j in jobs)

    with ui.row().classes('gap-0 flex-wrap mb-6 w-full').style(
            'border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden'):
        # Left summary
        with ui.element('div').style(
                'flex:1;min-width:160px;padding:18px 24px;border-right:1px solid var(--border)'):
            ui.label('TOTAL BACKTESTS').classes('label-text mb-1')
            ui.label(str(total)).classes('text-2xl font-bold text-info')
            ui.label(f'{total_trades} total trades simulated').classes('text-xs text-muted mt-1')

        # Pipeline stages
        for col_name in ('Running', 'Completed', 'Archived'):
            badge_cls, text_cls, col_icon, col_color = _COL_STYLE[col_name]
            cnt = len(_COLUMNS[col_name])
            pct = int(cnt / total * 100) if total else 0
            is_last = col_name == 'Archived'
            with ui.element('div').style(
                    f'flex:1;min-width:140px;padding:18px 24px;'
                    f'{"" if is_last else "border-right:1px solid var(--border)"}'):
                with ui.row().classes('items-center gap-2 mb-1'):
                    ui.icon(col_icon).style(f'font-size:1rem;color:{col_color}')
                    ui.label(col_name).classes('label-text')
                ui.label(str(cnt)).classes(f'text-2xl font-bold {text_cls}')
                ui.label(f'{pct} % of tests').classes('text-xs text-muted mt-1')

    # ── Kanban board ──────────────────────────────────────────────
    with ui.row().classes('gap-4 items-start w-full'):
        for col_name, tests in _COLUMNS.items():
            badge_cls, text_cls, col_icon, col_color = _COL_STYLE[col_name]
            action_label, action_cls, action_type, action_title = _COL_ACTION[col_name]

            with ui.element('div').style(
                    f'flex:1;min-width:260px;padding:14px;border-radius:var(--radius-lg);'
                    f'border:1px solid var(--border);background:var(--faint)'):

                # Column header
                with ui.row().classes('items-center justify-between mb-4').style(
                        f'padding-bottom:12px;border-bottom:2px solid {col_color}'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon(col_icon).style(f'font-size:1.1rem;color:{col_color}')
                        ui.label(col_name).classes('font-semi text-base')
                    ui.label(str(len(tests))).classes(f'badge {badge_cls}')

                # Test cards
                with ui.column().classes('gap-3 w-full'):
                    for test in tests:
                        return_color = 'text-success' if '+' in test['return'] else 'text-danger' if '-' in test['return'] else 'text-muted'
                        with ui.element('div').classes('card').style('padding:16px 18px'):

                            # Card top: ID + duration
                            with ui.row().classes('items-center justify-between mb-2'):
                                ui.label(test['id']).classes('font-semi text-sm')
                                with ui.row().classes('items-center gap-1'):
                                    ui.icon('schedule').style('font-size:12px;color:var(--faint-fg)')
                                    ui.label(test['duration']).classes('text-xs text-faint')

                            # Strategy + asset
                            ui.label(test['strategy']).classes('text-sm font-medium mb-1')
                            ui.label(test['asset']).classes('text-xs text-muted mb-3')

                            # Chips row
                            with ui.row().classes('gap-2 flex-wrap mb-3'):
                                with ui.element('span').classes('chip'):
                                    ui.icon('timer').style('font-size:11px;margin-right:3px')
                                    ui.label(test['timeframe'])
                                with ui.element('span').classes('chip'):
                                    ui.icon('swap_horiz').style('font-size:11px;margin-right:3px')
                                    ui.label(f'{test["trades"]} trades')

                            # Return display
                            ui.element('div').classes('divider mt-0 mb-2')
                            with ui.row().classes('items-center justify-between'):
                                ui.label('Return:').classes('text-xs text-muted')
                                ui.label(test['return']).classes(f'text-sm font-bold {return_color}')

                            # Footer: action
                            ui.element('div').classes('divider mt-2 mb-2')
                            ui.button(action_label, color='white',
                                      on_click=lambda tid=test['id'], t=action_type, ti=action_title:
                                      notify(f'{tid} — {ti.lower()}', type=t, title=ti),
                                      ).props('flat no-caps').classes(f'button {action_cls} button-sm w-full')
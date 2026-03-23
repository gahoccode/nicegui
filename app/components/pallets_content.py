"""Alerts page — price alert cards, KPI row and alert status summary."""

from nicegui import ui
from services.notifications import notify

_ALERTS = [
    {'id': 'ALT-1001', 'ticker': 'AAPL',  'condition': 'Above', 'target': 195.00, 'current': 190.50, 'status': 'Active',    'dot': 'info'},
    {'id': 'ALT-1002', 'ticker': 'MSFT',  'condition': 'Below', 'target': 380.00, 'current': 400.20, 'status': 'Active',    'dot': 'info'},
    {'id': 'ALT-1003', 'ticker': 'NVDA',  'condition': 'Above', 'target': 450.00, 'current': 448.75, 'status': 'Triggered', 'dot': 'warning'},
    {'id': 'ALT-1004', 'ticker': 'GOOGL', 'condition': 'Below', 'target': 140.00, 'current': 145.00, 'status': 'Active',    'dot': 'info'},
    {'id': 'ALT-1005', 'ticker': 'TSLA',  'condition': 'Above', 'target': 250.00, 'current': 250.50, 'status': 'Triggered', 'dot': 'warning'},
    {'id': 'ALT-1006', 'ticker': 'JPM',   'condition': 'Above', 'target': 260.00, 'current': 240.00, 'status': 'Active',    'dot': 'info'},
    {'id': 'ALT-1007', 'ticker': 'META',  'condition': 'Below', 'target': 480.00, 'current': 505.00, 'status': 'Active',    'dot': 'info'},
    {'id': 'ALT-1008', 'ticker': 'AMD',   'condition': 'Above', 'target': 180.00, 'current': 155.00, 'status': 'Expired',   'dot': 'danger'},
]

_STATUS_BADGE = {
    'Active':    'badge-info',
    'Triggered': 'badge-warning',
    'Expired':   'badge-danger',
}

_CONDITION_COUNTS: dict = {}
for _a in _ALERTS:
    _CONDITION_COUNTS[_a['condition']] = _CONDITION_COUNTS.get(_a['condition'], 0) + 1


def content() -> None:

    # ── Page header ───────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mt-4 mb-2'):
        with ui.column().classes('gap-1'):
            ui.label('Price Alerts').classes('page-title')
            ui.label('Monitor price movements and get notified on triggers.').classes('text-sm text-muted')
        ui.button('+ Create Alert', color='white',
                  on_click=lambda: notify('Alert creation form coming soon', type='info')).props('flat no-caps').classes('button button-primary')
    ui.element('div').classes('divider mb-4')

    # ── KPI row ───────────────────────────────────────────────────
    by_status: dict = {}
    for a in _ALERTS:
        by_status[a['status']] = by_status.get(a['status'], 0) + 1

    total_active = by_status.get('Active', 0)
    total_triggered = by_status.get('Triggered', 0)
    total_expired = by_status.get('Expired', 0)

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for label, value, sub, color, icon in [
            ('Total Alerts',  str(len(_ALERTS)),            'configured',       'text-info',    'notifications'),
            ('Active',        str(total_active),            'monitoring',       'text-success', 'radar'),
            ('Triggered',     str(total_triggered),         'awaiting action',  'text-warning', 'priority_high'),
            ('Expired',       str(total_expired),           'past validity',    'text-danger',  'schedule'),
            ('Trigger Rate',  f'{int(total_triggered/len(_ALERTS)*100)}%', 'conversion rate',  'text-info', 'speed'),
        ]:
            with ui.element('div').classes('card').style('min-width:130px;flex:1'):
                with ui.row().classes('items-start justify-between mb-3'):
                    ui.label(label).classes('label-text')
                    ui.icon(icon).style('font-size:1.15rem;color:var(--muted-fg)')
                ui.label(value).classes(f'text-2xl font-bold {color}')
                ui.label(sub).classes('text-xs text-muted mt-1')

    # ── Alert cards ──────────────────────────────────────────────
    with ui.row().classes('items-center justify-between mb-3'):
        with ui.column().classes('gap-0'):
            ui.label('Alert Inventory').classes('card-title')
            ui.label(f'{len(_ALERTS)} alerts configured').classes('text-xs text-muted mt-1')

    with ui.row().classes('gap-4 flex-wrap mb-6'):
        for a in _ALERTS:
            progress = min(100, int((a['current'] / a['target']) * 100)) if a['condition'] == 'Below' else min(100, int((a['target'] / a['current']) * 100))
            bar_color = ('#f87171' if a['status'] == 'Expired'
                         else '#fbbf24' if a['status'] == 'Triggered'
                         else '#4ade80' if progress >= 90
                         else '#60a5fa')
            with ui.element('div').classes('card').style('min-width:220px;max-width:220px;height:220px'):
                # Card header
                with ui.row().classes('items-center justify-between mb-2'):
                    with ui.row().classes('items-center gap-2'):
                        ui.element('span').classes(f'status-dot {a["dot"]}')
                        ui.label(a['id']).classes('font-semi text-sm')
                    ui.label(a['status']).classes(f'badge {_STATUS_BADGE.get(a["status"], "badge-default")}')
                # Meta
                with ui.column().classes('gap-0 mb-2'):
                    ui.label(a['ticker']).classes('text-lg font-bold')
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('trending_up' if a['condition'] == 'Above' else 'trending_down').style('font-size:13px;color:var(--muted-fg)')
                        ui.label(f'{a["condition"]} ${a["target"]:.2f}').classes('text-xs text-faint')
                # Progress bar
                with ui.element('div').classes('w-full mb-2'):
                    with ui.row().classes('items-center justify-between mb-1'):
                        ui.label('Current Price').classes('text-xs text-muted')
                        ui.label(f'${a["current"]:.2f}').classes('text-xs font-semi')
                    ui.element('div').style(
                        'height:6px;border-radius:9999px;background:#f4f4f5;overflow:hidden;width:100%'
                    ).add_slot('default',
                        f'<div style="width:{progress}%;height:100%;background:{bar_color};'
                        f'border-radius:9999px;transition:width .4s"></div>'
                    )
                    ui.label(f'{progress}% to target').classes('text-xs text-faint mt-1')
                # Actions
                ui.element('div').classes('divider mt-auto mb-2')
                with ui.row().classes('gap-2'):
                    ui.button('Edit', color='white',
                              on_click=lambda aid=a['id']: notify(f'{aid} edit mode', type='info')).props('flat no-caps').classes('button button-outline button-sm')
                    ui.button('Delete', color='white',
                              on_click=lambda aid=a['id']: notify(f'{aid} deleted', type='warning')).props('flat no-caps').classes('button button-ghost button-sm')

    # ── Condition summary ────────────────────────────────────────
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('items-center justify-between mb-4'):
            with ui.column().classes('gap-0'):
                ui.label('By Condition Type').classes('card-title')
                ui.label(f'{len(_CONDITION_COUNTS)} condition types').classes('text-xs text-muted mt-1')
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Condition', 'Count', 'Avg Target', 'Status']:
                        with ui.element('th'): ui.label(col)
            with ui.element('tbody'):
                for cond, cnt in sorted(_CONDITION_COUNTS.items()):
                    cond_alerts = [a for a in _ALERTS if a['condition'] == cond]
                    avg_target = sum(a['target'] for a in cond_alerts) / len(cond_alerts) if cond_alerts else 0
                    active_cnt = sum(1 for a in cond_alerts if a['status'] == 'Active')
                    bar_c  = '#4ade80' if active_cnt > 0 else '#fbbf24'
                    with ui.element('tr'):
                        with ui.element('td'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('trending_up' if cond == 'Above' else 'trending_down').style('font-size:16px;color:#60a5fa')
                                ui.label(cond).classes('font-semi')
                        with ui.element('td'): ui.label(str(cnt))
                        with ui.element('td'): ui.label(f'${avg_target:.2f}').classes('text-muted')
                        with ui.element('td'):
                            with ui.element('div').classes('flex items-center gap-3'):
                                ui.element('div').style(
                                    f'flex:1;height:6px;border-radius:9999px;background:#f4f4f5;overflow:hidden'
                                ).add_slot('default',
                                    f'<div style="width:{int(active_cnt/cnt*100)}%;height:100%;background:{bar_c};'
                                    f'border-radius:9999px;transition:width .4s"></div>'
                                )
                                ui.label(f'{active_cnt} active').classes('text-xs text-muted').style('min-width:60px')
"""Print Demo page — interactive showcase of all three print_component modes."""

import base64

from nicegui import ui

from components.print_component import encode_html, encode_image, encode_page, open_print

# ── Sample assets generated at module load ─────────────────────────────────────

# A minimal SVG bar-chart used for the image-print demo (no file dependency)
_SAMPLE_SVG = """\
<svg xmlns="http://www.w3.org/2000/svg" width="640" height="320" font-family="system-ui,sans-serif">
  <rect width="640" height="320" fill="#fafafa" rx="10"/>
  <text x="320" y="36" text-anchor="middle" font-size="17" font-weight="700" fill="#09090b">Monthly Portfolio Returns</text>
  <!-- Y-axis labels -->
  <text x="42" y="260" text-anchor="end" font-size="11" fill="#71717a">0%</text>
  <text x="42" y="200" text-anchor="end" font-size="11" fill="#71717a">5%</text>
  <text x="42" y="140" text-anchor="end" font-size="11" fill="#71717a">10%</text>
  <text x="42" y="80"  text-anchor="end" font-size="11" fill="#71717a">15%</text>
  <!-- Grid lines -->
  <line x1="50" y1="255" x2="620" y2="255" stroke="#e4e4e7" stroke-width="1"/>
  <line x1="50" y1="195" x2="620" y2="195" stroke="#e4e4e7" stroke-width="1"/>
  <line x1="50" y1="135" x2="620" y2="135" stroke="#e4e4e7" stroke-width="1"/>
  <line x1="50" y1="75"  x2="620" y2="75"  stroke="#e4e4e7" stroke-width="1"/>
  <!-- Bars: Q1 = primary (#18181b), Q2 = success (#4ade80) -->
  <rect x="65"  y="135" width="55" height="120" fill="#18181b" rx="4" opacity=".90"/>
  <rect x="140" y="100" width="55" height="155" fill="#18181b" rx="4" opacity=".90"/>
  <rect x="215" y="80"  width="55" height="175" fill="#18181b" rx="4" opacity=".90"/>
  <rect x="290" y="115" width="55" height="140" fill="#18181b" rx="4" opacity=".90"/>
  <rect x="365" y="90"  width="55" height="165" fill="#4ade80" rx="4" opacity=".90"/>
  <rect x="440" y="70"  width="55" height="185" fill="#4ade80" rx="4" opacity=".90"/>
  <rect x="515" y="85"  width="55" height="170" fill="#4ade80" rx="4" opacity=".90"/>
  <!-- X labels -->
  <text x="92"  y="275" text-anchor="middle" font-size="11" fill="#71717a">Jan</text>
  <text x="167" y="275" text-anchor="middle" font-size="11" fill="#71717a">Feb</text>
  <text x="242" y="275" text-anchor="middle" font-size="11" fill="#71717a">Mar</text>
  <text x="317" y="275" text-anchor="middle" font-size="11" fill="#71717a">Apr</text>
  <text x="392" y="275" text-anchor="middle" font-size="11" fill="#71717a">May</text>
  <text x="467" y="275" text-anchor="middle" font-size="11" fill="#71717a">Jun</text>
  <text x="542" y="275" text-anchor="middle" font-size="11" fill="#71717a">Jul</text>
  <!-- Legend -->
  <rect x="480" y="42" width="12" height="12" fill="#18181b" rx="2"/>
  <text x="496" y="53" font-size="11" fill="#09090b">Q1</text>
  <rect x="520" y="42" width="12" height="12" fill="#4ade80" rx="2"/>
  <text x="536" y="53" font-size="11" fill="#09090b">Q2</text>
</svg>"""

_SAMPLE_SVG_B64 = base64.b64encode(_SAMPLE_SVG.encode()).decode()

# Sample HTML report used for the structured-page demo
_REPORT_TABLE = """
<table>
  <thead>
    <tr><th>Position ID</th><th>Ticker</th><th>Shares</th><th>Status</th><th>Open Date</th></tr>
  </thead>
  <tbody>
    <tr><td>POS-1001</td><td>AAPL</td><td>150</td><td>Gain</td><td>2026-01-15</td></tr>
    <tr><td>POS-1002</td><td>MSFT</td><td>80</td><td>Gain</td><td>2025-12-10</td></tr>
    <tr><td>POS-1003</td><td>NVDA</td><td>45</td><td>Gain</td><td>2026-02-20</td></tr>
    <tr><td>POS-1004</td><td>GOOGL</td><td>100</td><td>Loss</td><td>2026-03-05</td></tr>
    <tr><td>POS-1005</td><td>TSLA</td><td>60</td><td>Loss</td><td>2026-02-28</td></tr>
  </tbody>
</table>
"""


# ── Component ──────────────────────────────────────────────────────────────────

def content() -> None:

    # ── Page header ───────────────────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mb-1'):
        with ui.column().classes('gap-0'):
            ui.label('Print Demo').classes('page-title')
            ui.label('Live examples of every print_component mode — click any card to open the print dialog.') \
                .classes('text-sm text-muted')
    ui.element('div').classes('divider mb-4')

    # ── Three mode cards ──────────────────────────────────────────────────────
    with ui.row().classes('w-full gap-4 flex-wrap items-stretch'):

        # ── Card 1: Raw HTML ──────────────────────────────────────────────────
        with ui.element('div').classes('card flex-1 flex flex-col').style('min-width:260px; max-width:380px'):
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.icon('code', size='sm').classes('text-primary')
                ui.label('HTML Print').classes('card-title')
            ui.label(
                'Pass any HTML string — headings, paragraphs, lists, tables. '
                'Great for quick financial reports.'
            ).classes('text-sm text-muted mt-2')

            ui.element('div').style('flex:1')  # aligns separator across cards
            ui.separator().classes('my-4')

            ui.label('Preview').classes('text-xs text-faint font-semi mb-1')
            with ui.element('div').classes('rounded p-3 text-sm').style('background:var(--faint); border:1px solid var(--border)'):
                ui.html(
                    '<b>Daily Market Summary</b><br>'
                    '<p style="margin:4px 0 0; color:#374151">Portfolio Return: <b>+2.4%</b> — Sharpe Ratio: <b>1.85</b></p>',
                    sanitize=False,
                )

            ui.element('div').style('flex:1')  # pushes button to bottom
            ui.separator().classes('my-4')

            ui.button('Print HTML report', icon='print', on_click=_print_html) \
                .props('unelevated').classes('btn btn-primary w-full')

        # ── Card 2: Base64 Image ──────────────────────────────────────────────
        with ui.element('div').classes('card flex-1 flex flex-col').style('min-width:260px; max-width:380px'):
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.icon('image', size='sm').classes('text-primary')
                ui.label('Image Print').classes('card-title')
            ui.label(
                'Pass a plain base64 string (PNG, JPEG, SVG). '
                'The print view centres it on the page with an optional caption.'
            ).classes('text-sm text-muted mt-2')

            ui.element('div').style('flex:1')  # aligns separator across cards
            ui.separator().classes('my-4')

            ui.label('Preview').classes('text-xs text-faint font-semi mb-1')
            ui.html(
                f'<img src="data:image/svg+xml;base64,{_SAMPLE_SVG_B64}" '
                f'style="width:100%;border-radius:6px;border:1px solid var(--border)">',
                sanitize=False,
            )

            ui.element('div').style('flex:1')  # pushes button to bottom
            ui.separator().classes('my-4')

            ui.button('Print chart image', icon='print', on_click=_print_image) \
                .props('unelevated').classes('btn btn-primary w-full')

        # ── Card 3: Structured page ───────────────────────────────────────────
        with ui.element('div').classes('card flex-1 flex flex-col').style('min-width:260px; max-width:380px'):
            with ui.row().classes('items-center gap-2 mb-1'):
                ui.icon('article', size='sm').classes('text-primary')
                ui.label('Structured Page').classes('card-title')
            ui.label(
                'Combine a title, subtitle, and any mix of HTML and image sections '
                'into one print-ready document.'
            ).classes('text-sm text-muted mt-2')

            ui.element('div').style('flex:1')  # aligns separator across cards
            ui.separator().classes('my-4')

            ui.label('Preview').classes('text-xs text-faint font-semi mb-1')
            with ui.element('div').classes('rounded p-3 text-sm').style('background:var(--faint); border:1px solid var(--border); font-family:system-ui'):
                ui.html(
                    '<div style="font-weight:700;font-size:14px;margin-bottom:2px">Portfolio Report — Mar 2026</div>'
                    '<div style="font-size:11px;color:#6b7280;margin-bottom:6px">Taxable Account</div>'
                    '<div style="font-size:12px;color:#374151">2 sections: summary paragraph + returns chart + holdings table</div>',
                    sanitize=False,
                )

            ui.element('div').style('flex:1')  # pushes button to bottom
            ui.separator().classes('my-4')

            ui.button('Print full report', icon='print', on_click=_print_page) \
                .props('unelevated').classes('btn btn-primary w-full')


# ── Print actions ──────────────────────────────────────────────────────────────

def _print_html() -> None:
    html = (
        '<h1>Daily Portfolio Summary</h1>'
        '<p>Report date: <b>2026-03-23</b> &nbsp;|&nbsp; Account: <b>Taxable</b></p>'
        '<h2>Key Metrics</h2>'
        '<ul>'
        '<li>Portfolio Value: <b>$156,000</b></li>'
        '<li>Daily Return: <b>+1.2%</b></li>'
        '<li>Sharpe Ratio: <b>1.85</b></li>'
        '<li>Open Positions: <b>6</b></li>'
        '</ul>'
        '<h2>Notes</h2>'
        '<p>NVDA position hit price target at $450, alert triggered for potential profit taking. '
        'All other positions performing within expected parameters.</p>'
    )
    open_print(encode_html(html))


def _print_image() -> None:
    open_print(encode_image(
        _SAMPLE_SVG_B64,
        mime='image/svg+xml',
        caption='Monthly Portfolio Returns — Jan–Jul 2026',
    ))


def _print_page() -> None:
    summary_html = (
        '<p>This report covers all positions in the taxable portfolio as of March 2026. '
        'Total value: <b>$156,000</b>. YTD Return: <b>+12.4%</b>.</p>'
    )
    token = encode_page(
        title    = 'Portfolio Report — March 2026',
        subtitle = 'Taxable Account · Generated 2026-03-23',
        sections = [
            {'type': 'html',  'content': summary_html},
            {'type': 'image', 'content': _SAMPLE_SVG_B64,
             'mime': 'image/svg+xml', 'caption': 'Monthly Returns Chart'},
            {'type': 'html',  'content': _REPORT_TABLE},
        ],
    )
    open_print(token)
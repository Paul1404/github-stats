"""Dependency-free SVG layout for the existing GitHub language statistics."""

from html import escape
import re


def language_markup(languages):
    """Keep the chart and legend consistent, grouping overflow as Other."""
    entries = sorted(languages.items(), key=lambda item: item[1].get('size', 0), reverse=True)
    if len(entries) > 12:
        rest = entries[11:]
        entries = entries[:11] + [('Other', {
            'prop': sum(data.get('prop', 0) for _, data in rest),
            'color': '#8b949e',
        })]
    if not entries:
        return '', '<text class="muted" x="20" y="118">No language data available.</text>', 'No language data available.'
    progress, legend, summary = [], [], []
    offset = 20.0
    for i, (name, data) in enumerate(entries):
        prop = float(data.get('prop', 0))
        color = data.get('color') or '#8b949e'
        if not re.fullmatch(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?', color):
            color = '#8b949e'
        width = 3.2 * prop
        progress.append(f'<rect x="{offset:.3f}" y="74" width="{width:.3f}" height="10" fill="{color}" />')
        offset += width
        x = 20 + (i % 2) * 168
        y = 114 + (i // 2) * 25
        label = name if len(name) <= 15 else name[:14] + '…'
        legend.append(
            f'<g><title>{escape(name)}: {prop:.2f}%</title>'
            f'<circle cx="{x + 3}" cy="{y - 4}" r="3" fill="{color}" />'
            f'<text class="language" x="{x + 12}" y="{y}">{escape(label)}</text>'
            f'<text class="percent" x="{x + 152}" y="{y}" text-anchor="end">{prop:.2f}%</text></g>'
        )
        summary.append(f'{name} {prop:.2f}%')
    return '\n'.join(progress), '\n'.join(legend), escape(', '.join(summary))

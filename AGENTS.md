# GitHub statistics cards

- Keep the existing Stats collector and scheduled GitHub Actions refresh. Rendering changes must not alter metric definitions or repository exclusions.
- Edit `templates/*.svg` for appearance and `card_layout.py` for the language chart and legend. Use native SVG with a `viewBox`, accessible descriptions, and readable light and dark palettes.
- Preserve the `gh-dark-mode-only` root ID and fragment-based theme selectors used by profile READMEs.
- Keep chart and legend in sync. If more than 12 languages are available, show the largest 11 and aggregate the rest as Other.
- Check XML parsing, escaped names, empty data, and overflow grouping after rendering changes. Inspect both themes and a narrow profile layout.
- `generated/*.svg` are published assets. Regenerate them through `generate_images.py` in the existing workflow; never invent or hand-edit metric values.
- Production generation uses existing Actions secrets. Do not retrieve or print tokens or change secret configuration for visual work.
- `generate_images.py` uses CRLF line endings. Preserve them and check its diff with `git -c core.whitespace=cr-at-eol diff --check`.

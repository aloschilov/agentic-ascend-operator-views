#!/usr/bin/env bash
set -euo pipefail

out_dir="${1:-dist}"
marp_bin="${MARP_BIN:-marp}"

decks=(
  "agentic_ascend_operator_views_overview.ru"
  "agentic_ascend_operator_views_overview.en"
  "agentic_ascend_operator_views_survey.ru"
  "agentic_ascend_operator_views_survey.en"
  "babble_pyasc_applicability.ru"
  "babble_pyasc_applicability.en"
)

mkdir -p "${out_dir}"

for deck in "${decks[@]}"; do
  "${marp_bin}" "presentations/${deck}.marp.md" \
    --theme-set chapter-theme.css \
    --allow-local-files \
    --no-stdin \
    --pdf \
    -o "${out_dir}/${deck}.pdf"

  "${marp_bin}" "presentations/${deck}.marp.md" \
    --theme-set chapter-theme.css \
    --allow-local-files \
    --no-stdin \
    --pptx \
    -o "${out_dir}/${deck}.pptx"
done

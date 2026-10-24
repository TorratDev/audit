#!/usr/bin/env bash
# Regenera el panel de progreso de épicas en el issue de seguimiento.
# Uso: REPO=owner/repo DASHBOARD_ISSUE=26 .github/scripts/epic-progress.sh
set -euo pipefail

REPO=${REPO:-${GITHUB_REPOSITORY:?define REPO}}
DASHBOARD_ISSUE=${DASHBOARD_ISSUE:?define DASHBOARD_ISSUE}
WIDTH=10

bar() {
  local pct=$1 full=$(( $1 * WIDTH / 100 )) out="" i
  for ((i = 0; i < WIDTH; i++)); do
    if ((i < full)); then out+="█"; else out+="░"; fi
  done
  printf '`%s` %3d %%' "$out" "$pct"
}

epics=$(gh api "repos/$REPO/issues?labels=epic&state=all&per_page=100" \
  --jq 'sort_by(.number) | .[] | [.number, .state, .title, .sub_issues_summary.completed, .sub_issues_summary.total] | @tsv')

total_done=0 total_all=0 table="" details=""
while IFS=$'\t' read -r num state title done all; do
  [[ -z $num ]] && continue
  pct=$(( all > 0 ? done * 100 / all : 0 ))
  total_done=$(( total_done + done )) total_all=$(( total_all + all ))
  icon=$([[ $state == closed ]] && echo "✅" || echo "🟡")
  ((done == 0)) && [[ $state == open ]] && icon="⚪"
  pipe='|'; safe=${title//"$pipe"/'\|'}
  table+="| $icon #$num ${safe#Épica · } | $(bar "$pct") | $done / $all |"$'\n'

  rows=$(gh api "repos/$REPO/issues/$num/sub_issues?per_page=100" \
    --jq '.[] | "- " + (if .state == "closed" then "✅" elif .issue_dependencies_summary.blocked_by > 0 then "🔒" else "⬜" end) + " #\(.number)"')
  details+="<details><summary><b>#$num</b> ${title#Épica · } · $done / $all</summary>"$'\n\n'"$rows"$'\n\n'"</details>"$'\n'
done <<< "$epics"

overall=$(( total_all > 0 ? total_done * 100 / total_all : 0 ))

body="# 📊 Progreso de épicas

Panel generado automáticamente por \`.github/workflows/epic-progress.yml\`; no editar a mano.

**Total:** $(bar "$overall") · $total_done / $total_all tareas

| Épica | Progreso | Hechas |
|---|---|---|
$table
## Detalle

$details
**Leyenda:** ✅ cerrada · ⬜ lista para empezar · 🔒 bloqueada por otra issue · ⚪ épica sin empezar · 🟡 épica en curso

_Actualizado: $(date -u '+%Y-%m-%d %H:%M UTC')_"

gh api -X PATCH "repos/$REPO/issues/$DASHBOARD_ISSUE" -f body="$body" --jq '"Panel actualizado: \(.html_url)"'

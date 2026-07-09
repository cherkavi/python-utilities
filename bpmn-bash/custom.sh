#!/usr/bin/env bash

set -euo pipefail

prepare_request() {
  wf_log "Preparing initial request context"
  wf_set request_status pending
  wf_set requester developer
  wf_set requested_amount 10 number
}

finalize_approval() {
  local amount
  amount="$(wf_get final_amount)"
  wf_log "Approved request with final amount ${amount}"
  wf_set request_status approved
}

finalize_rejection() {
  wf_log "Rejected request"
  wf_set request_status rejected
}
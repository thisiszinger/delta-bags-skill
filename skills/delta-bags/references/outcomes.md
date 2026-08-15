# Request outcomes

Interpret the stable rendered result after each submission. Delta's current page wording and result determine the outcome; codes below are recognition aids, not a substitute for the live response.

| Outcome | Assign when | Next action |
| --- | --- | --- |
| `approved` | Delta explicitly shows its successful result, currently headed “Claim Successful” | Report the success text and any confirmation; record it |
| `rejected` | Delta says the request is ineligible, details do not match, no checked bag exists, airports are ineligible, or the account is invalid | Report Delta's reason; correct inputs only with evidence |
| `duplicate` | Delta says a request already exists | Report it; do not resubmit automatically |
| `expired` | Delta says the request missed the deadline | Report the deadline result; stop |
| `failed` | Delta clearly reports a technical or processing failure | Report it; ask before retrying |
| `unknown` | The final click, navigation, or response is ambiguous | Preserve visible evidence; never retry automatically |

Current recognition aids include:

- `1010`: outside the current 120-minute deadline;
- `1011`: no checked bags associated with the reservation;
- `1998`: bags recorded as arriving on time;
- `2001`: ineligible airports;
- `1004`, `1005`, `07641`, or `V018`: itinerary/input mismatch variants.

Do not label a request `approved` merely because the form accepted a click, navigation completed, or Delta acknowledged receipt. A Submission Confirmation is not necessarily an award confirmation.

For a Request Batch, report results separately:

```text
<traveler>: approved — <Delta summary>
<traveler>: rejected — <Delta reason>
<traveler>: unknown — final response could not be verified; not retried
```

Continue after traveler-specific results. Stop remaining submissions when the form itself changed, the policy became unreadable, or a shared browser/session problem makes later results unreliable.

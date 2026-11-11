
# Judgment Framework
## Lost and Found Matcher

| Decision | System Responsibility | Human Responsibility |
|---|---|---|
| Item identification | Extract item category | Check unclear item descriptions |
| Colour identification | Extract explicitly mentioned colour | Verify if colour is uncertain |
| Brand identification | Extract brand only when mentioned | Ask claimant to confirm brand |
| Place identification | Extract mentioned campus location | Confirm exact location if needed |
| Match scoring | Calculate score using Python rules | Review suggested matches |
| Likely match | Display as a strong suggestion | Verify ownership before returning item |
| Possible match | Display as a possible suggestion | Investigate further |
| Double claims | Flag found items linked to multiple lost reports | Resolve the claims |
| No match | Report when no suitable match exists | Help the student search further |

## Human Checkpoint

The application must never decide ownership automatically.

When a possible or likely match is found:

1. The administrator reviews the suggested match.
2. The claimant is asked to provide an additional detail that is not already present in either report.
3. The administrator checks the answer.
4. Only the administrator can approve the claim and return the item.

## Important Rule

AI suggestions are not proof of ownership.

Final decisions must always be made by a human administrator.

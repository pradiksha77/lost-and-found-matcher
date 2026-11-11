
# Judgment Framework
## AI-Based Lost and Found Matcher

### 1. Purpose

The purpose of this framework is to explain which tasks can be handled by AI and which decisions require human involvement.

The AI system helps college administrators find possible matches between lost and found item reports. However, it cannot decide who owns an item.

### 2. Decision Responsibility Table

| Decision | AI Role | Human Role | Rule |
|---|---|---|---|
| Extract item details | Identifies item, colour, brand and place | Checks incorrect details | AI must not guess missing information |
| Validate reports | Checks required fields and facts | Reviews invalid reports | Only valid information is used |
| Calculate match score | Compares lost and found reports | Reviews suggested matches | Follow the defined scoring rules |
| Identify possible matches | Suggests likely and possible matches | Checks the suggestions | AI suggestions are not final decisions |
| Detect duplicate claims | Flags one found item matched with multiple lost reports | Investigates the claims | Human review is required |
| Verify ownership | Does not decide ownership | Asks the claimant questions and verifies evidence | Only a human can approve ownership |
| Return the item | Does not return the item automatically | Authorizes the return | Final approval belongs to the administrator |

### 3. Human Checkpoint

Before returning an item, the college help desk must verify the claimant.

The administrator should:

1. Ask the claimant to describe one identifying detail that was not included in the original lost and found reports.
2. Check whether the claimant's answer is consistent with the item.
3. Request additional proof when necessary.
4. Approve or reject the claim after verification.

The AI system must never decide ownership or automatically return an item.

### 4. Safety Rules

- AI must not invent missing information.
- Conflicting item details must be checked.
- Reports with different known colours or brands must not be matched.
- Reports more than 30 days apart must not be matched.
- Items categorized as "other" must not be automatically matched.
- Multiple claims for one found item must be flagged.
- A human administrator must make the final ownership decision.

### 5. Conclusion

The AI system is designed to assist college administrators, not replace them. It saves time by identifying possible matches, while human verification ensures that items are returned to the correct owners.

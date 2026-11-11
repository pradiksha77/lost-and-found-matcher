
# AI Decision Journal
## AI-Based Lost and Found Matcher

### Decision 1: Choosing the AI Model

Initially, I planned to use a cloud-based AI API. However, I faced an API credit limitation. So, I decided to use Qwen 2.5 (0.5B) through Ollama.

Reason: It is free to use locally and does not require paid API credits.

### Decision 2: Choosing the Extraction Format

I decided to use JSON with five fields:
- Item
- Colour
- Brand
- Place
- Summary

Reason: JSON makes the extracted information structured and easier for Python to process.

### Decision 3: Setting Temperature to Zero

I selected temperature 0 for AI extraction.

Reason: It helps make the model's responses more consistent and predictable.

### Decision 4: Adding a Validator

I created a separate validator.py file.

Reason: AI responses may contain incorrect or unsupported information. The validator checks the extracted details against the original report.

### Decision 5: Creating Matching Rules

I used a scoring system:
- Same colour: +2
- Same brand: +2
- Same place: +1

Reports with different known colours or brands are rejected. Reports more than 30 days apart are also rejected.

Reason: These rules help identify more relevant possible matches.

### Decision 6: Adding Human Verification

I decided that AI should only suggest possible matches.

Reason: AI cannot prove ownership. A college administrator must verify the claimant before returning an item.

### Decision 7: Performing Red-Team Testing

I tested three situations:
1. Vague lost-item report.
2. Brand guessing.
3. Malicious instructions inside a report.

Reason: These tests help identify unsafe or incorrect AI behaviour.

The validator detected the incorrect item extraction in the malicious instruction test.

### Decision 8: Choosing Local Processing

I decided to process reports using a local AI model.

Reason: It avoids paid API charges and allows reports to be processed on the computer.

### Conclusion

During this project, I learned that building an AI application is not only about getting answers from an AI model. It is also important to validate information, test unexpected inputs, create clear rules and keep humans involved in important decisions.

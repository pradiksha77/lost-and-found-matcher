
# Cost and Latency Note
## AI-Based Lost and Found Matcher

### 1. AI Model Used

This project uses the Qwen 2.5 (0.5B) language model through Ollama.

The model runs locally on the computer instead of using a paid cloud AI API.

### 2. Cost Analysis

| Component | Cost |
|---|---|
| Qwen 2.5 (0.5B) model | Free to download |
| Ollama | Free |
| Python | Free |
| Required Python libraries | Free |
| Cloud API usage | Not used |
| Internet usage during local extraction | Not required |

There is no per-request API charge because the AI model runs locally. However, the computer uses electricity and system resources while processing reports.

### 3. Latency Analysis

Latency means the time taken by the AI system to process a report and return its extracted details.

The processing time depends on:
- Computer processor speed.
- Available RAM.
- Whether GPU acceleration is available.
- Length of the report.
- AI model performance.

The project sends one extraction request for each report.

For 10 lost reports and 10 found reports:
- Lost reports: 10 AI requests.
- Found reports: 10 AI requests.
- Total: 20 AI requests per complete run.

### 4. Advantages of Local AI

- No paid API key is required.
- Reports can be processed locally.
- No per-request cloud API charges.
- Useful for testing and college demonstrations.

### 5. Limitations

- Processing may be slower on computers with limited resources.
- Small models may sometimes produce incorrect information.
- The model must be downloaded before use.
- Ollama must be running during processing.

### 6. Conclusion

Using Qwen 2.5 through Ollama makes this project affordable and suitable for a college-level demonstration. It avoids cloud API charges while allowing the system to extract information from lost and found reports locally.

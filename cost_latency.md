
# Cost and Latency Report
## Lost and Found Matcher

### 1. Current Implementation

The current version uses a temporary rule-based extractor written in Python.

- AI API calls: 0
- API cost: 0
- Report extraction: Performed locally using Python.
- Matching: Performed using Python logic.
- CSV output generation: Performed locally.

### 2. Planned AI Integration

In the final version, an LLM API will extract structured information from each lost and found report.

The system will process each report only once and store its extracted information.

Python will perform all pairwise matching without additional LLM calls.

### 3. Cost Measurement

After connecting the API, the following details will be recorded:

- AI provider and model name
- Number of reports processed
- Total input tokens
- Total output tokens
- Cost per report
- Total API cost

Actual API pricing will be calculated using the provider's published pricing.

### 4. Latency Measurement

After API integration, processing time will be measured.

The total time will include:

- Time taken for API extraction
- Python validation time
- Matching time
- Output file generation time

### 5. Conclusion

The current prototype does not require an API key or incur API charges.

Actual AI cost and latency measurements will be added after LLM integration and testing.
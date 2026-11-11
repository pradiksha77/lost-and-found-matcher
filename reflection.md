
# Project Reflection
## AI-Based Lost and Found Matcher

Working on this AI-Based Lost and Found Matcher project was a useful learning experience for me. Initially, I thought building an AI application would be very difficult. I was not sure how to connect Python with an AI model or how to compare lost and found reports. But by completing each step, I slowly understood how the project works.

One of the biggest challenges was choosing an AI model. Initially, I planned to use a cloud-based API, but I faced an API credit limitation. So, I decided to use Qwen 2.5 (0.5B) through Ollama. This helped me run the AI model locally without paying for API requests.

I learned how to send reports to an AI model and extract useful information in JSON format. The model identifies details such as item name, colour, brand, place and summary. I also learned why validation is important. An AI model can sometimes produce incorrect information, so I created a separate validator to check the extracted details against the original report.

Another important part was the matching logic. I used Python to compare every lost report with every found report. I assigned points for matching colour, brand and place. I also added rules to reject reports with conflicting details or dates more than 30 days apart.

Red-team testing was another interesting experience. I tested vague reports, brand guessing and malicious instructions. During testing, I discovered that the AI could change a bottle into a phone when an instruction was included in the report. I improved my validator to detect this incorrect extraction. This taught me that AI outputs should never be trusted without checking them.

I also understood the importance of human involvement. The system can suggest possible matches, but it cannot decide who owns an item. A college administrator must verify the claimant before returning anything.

Overall, this project improved my understanding of Python, AI models, JSON, data validation and testing. I also learned that failures and errors are part of development. Instead of giving up, finding and correcting mistakes helped me understand the project better. This experience gave me more confidence to work on future AI-based projects.

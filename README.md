# AI Interview Transcript Analyzer

## Overview
This project aims to develop an AI specialized in analyzing text transcripts from interviews. The AI will output a JSON file named `data.json`, categorizing the candidate’s performance into various areas and scoring them accordingly.

## Categories for Analysis
The AI will assess the candidate's performance based on the following categories:

1. Relevance of Answers
2. Depth of Knowledge
3. Problem-solving Skills
4. Experience and Examples
5. Technical Proficiency
6. Communication Skills
7. Listening Skills
8. Interpersonal Skills
9. Enthusiasm and Motivation
10. Cultural Fit
11. Creativity and Innovation
12. Adaptability and Flexibility
13. Leadership Potential
14. Type of questions

Each category will have a `Score` and `Comments` field. The final output will include an `Overall Score` and a `Summary`.

### Weighting Criteria for Overall Score
The `Overall Score` will be calculated using the following weights:

- Relevance of Answers: 0.1
- Depth of Knowledge: 0.12
- Problem-solving Skills: 0.12
- Experience and Examples: 0.1
- Technical Proficiency: 0.15
- Communication Skills: 0.06
- Listening Skills: 0.05
- Interpersonal Skills: 0.05
- Enthusiasm and Motivation: 0.05
- Cultural Fit: 0.06
- Creativity and Innovation: 0.05
- Adaptability and Flexibility: 0.03
- Leadership Potential: 0.05
- Type of questions: 0.01

## Input Format
The AI will expect the rating for each category to be provided by the user. The rating scale is from 1 (poor) to 10 (excellent).

Example input:
```
Rate the candidate's performance in the following areas from 1 (poor) to 10 (excellent) based on their responses in the interview transcript.
Rate how directly and effectively the candidate's responses addressed the questions asked: 
```

## Configuration
The project uses environment variables for configuration. These settings should be placed in a `.env` file.

### Example .env File:
```
GPT_MODEL="gpt-4o"
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
```

## Usage Instructions
1. Clone the repository.
2. Create a `.env` file in the root directory and fill in the required details as shown above.
3. Run the application using your preferred method.

## Output
The output will be a JSON file named `data.json` containing the structured assessment of the interview transcript.

Example output:
```json
{
  "Relevance of Answers": { "Score": 8, "Comments": "Good understanding of the main topics." },
  "Depth of Knowledge": { "Score": 7, "Comments": "Satisfactory depth." },
  // ...other categories
  "Overall Score": 7.5,
  "Summary": "The candidate shows strong technical proficiency and depth of knowledge ..."
}
```


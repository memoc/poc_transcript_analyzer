<table>
  <tr>
    <td><img src="https://github.com/memoc/poc_transcript_analyzer/raw/main/static/images/icon.png" alt="Project Logo" style="width:100px;height:auto;"></td>
    <td><h1>AI Interview Transcript Analyzer</h1></td>
  </tr>
</table>


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
The format of the transcript provided is a well-structured record of an interview, capturing the dialogue between multiple speakers during an interaction, specifically a job interview for a technical role. It has a clear timestamp system that indicates the exact time at which each speaker contributes to the conversation, which aids in tracking the flow of dialogue over time.

Example input:
```
00:01:00 Speaker 1: Moving on to our next question, how do you handle project deadlines and pressure? 
00:01:10 Candidate: I prioritize my tasks based on urgency and complexity, and communicate regularly with the team to ensure we're all aligned and can meet deadlines comfortably. 
00:01:30 Speaker 2: That sounds like a solid strategy. How do you integrate feedback into your projects? 
00:01:40 Candidate: I actively seek feedback from all stakeholders and use it to make iterative improvements to ensure the project always aligns with business goals.
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

## Output Example
Below is a example of a rated interview

Candidate Interview Results: Candidate A
========================================

Summary
-------

Candidate C performed exceptionally well in the interview, demonstrating strong technical proficiency, problem-solving skills, and leadership potential. Their responses were highly relevant and detailed, supported by real-world examples. The candidate's enthusiasm and motivation for the role were evident, and they showed a good cultural fit with the organization. While their communication and interpersonal skills were strong, there is room for slight improvement in these areas. Overall, Candidate C is a highly qualified and promising candidate for the role.

Overall Score: 8.91
-------------------

![Radar Chart](/static/images/radar_chart.png)

Candidate Interview Results: Candidate A
========================================

| **Category**                     | **Score** | **Comments**                                                                                                                                                         |
|----------------------------------|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Relevance of Answers**         | 9         | The candidate provided highly relevant and direct answers to the questions asked, demonstrating a clear understanding of the topics discussed.                       |
| **Depth of Knowledge**           | 9         | The candidate showcased a deep understanding of cloud architecture, Terraform, Azure, and leadership principles, providing detailed explanations and examples.       |
| **Problem-solving Skills**       | 9         | The candidate effectively described their approach to solving complex problems, such as optimizing a legacy application and ensuring zero downtime during migration. |
| **Experience and Examples**      | 9         | The candidate shared multiple relevant examples from their professional experience, including specific projects and challenges they addressed.                       |
| **Technical Proficiency**        | 10        | The candidate demonstrated strong technical expertise in cloud platforms, Terraform, and Azure, as well as advanced problem-solving techniques.                      |
| **Communication Skills**         | 8         | The candidate communicated their ideas clearly and concisely, with well-structured responses and appropriate technical terminology.                                  |
| **Listening Skills**             | 8         | The candidate actively listened to the interviewers' questions and provided thoughtful, relevant answers without deviating from the topic.                           |
| **Interpersonal Skills**         | 8         | The candidate displayed a collaborative and approachable demeanor, emphasizing teamwork and conflict resolution strategies.                                          |
| **Enthusiasm and Motivation**    | 9         | The candidate expressed genuine enthusiasm for the role and demonstrated motivation to contribute to the team and organization.                                      |
| **Cultural Fit**                 | 8         | The candidate's values and approach to teamwork and leadership align well with a collaborative and innovative work culture.                                          |
| **Creativity and Innovation**    | 8         | The candidate showcased creativity in problem-solving, such as implementing a blue-green deployment strategy and optimizing costs in Azure.                          |
| **Adaptability and Flexibility** | 8         | The candidate demonstrated adaptability by working across multiple cloud platforms and handling diverse challenges effectively.                                      |
| **Leadership Potential**         | 9         | The candidate provided strong examples of team management, conflict resolution, and fostering a collaborative environment, indicating leadership potential.          |
| **Type of questions**            | 8         | The candidate asked thoughtful questions about the company, team dynamics, and project timelines, showing genuine interest in the role.                              |

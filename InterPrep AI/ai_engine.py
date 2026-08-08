import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"


def generate_response(prompt):

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=4000
        )
    )

    return response.text


def analyze_resume(resume, job_description):

    prompt = f"""
You are an expert technical recruiter.

Analyze the candidate's resume against the job description.

================ RESUME ================

{resume}

================ JOB DESCRIPTION ================

{job_description}

================ ANALYSIS ================

Provide:

1. Candidate Profile
2. Skills found in the resume
3. Skills required by the job description
4. Matching skills
5. Missing skills / skill gaps
6. Relevant projects
7. Relevant experience
8. Technologies the interviewer is likely to ask about
9. Potential weaknesses
10. Resume-JD Match Score out of 100
11. Top preparation topics

IMPORTANT:

- Use only information actually present in the resume.
- Do not invent skills or experience.
- Clearly separate existing skills from required skills.
- Focus on interview preparation.
- Explain what the candidate should prepare.

Return a clear structured analysis.
"""

    return generate_response(prompt)


def generate_questions(
    resume,
    job_description,
    category,
    difficulty,
    count
):

    prompt = f"""
You are an expert technical interviewer.

Create personalized interview questions based on the
candidate's resume.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

CATEGORY:
{category}

DIFFICULTY:
{difficulty}

NUMBER OF QUESTIONS:
{count}

Rules:

- Questions must be related to the resume.
- Prioritize projects and technologies actually mentioned.
- Do not invent technologies.
- For projects, ask architecture, implementation,
  challenges, decisions and improvements.
- For technical skills, ask both conceptual and practical questions.
- Include realistic interview questions.

Return ONLY a numbered list of questions.
"""

    return generate_response(prompt)



def evaluate_answer(
    question,
    answer,
    resume,
    job_description
):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer briefly and honestly.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the answer based on:
1. Technical correctness
2. Relevance
3. Depth
4. Clarity
5. Completeness
6. Communication

Give the result EXACTLY in this format:

### Score
X/10

### What was good
- Give 1-2 short points.

### What is missing
- Give 1 short point.
- If nothing is missing, write "Nothing significant."

### What is incorrect
- Give 1 short point.
- If everything is correct, write "No major errors."

### How to improve
- Give 1 short improvement.

### Interview Tips
- Give exactly 2 short, practical tips for answering this type of question in an interview.

### Ideal Answer
Give a concise ideal answer in 3-5 sentences.

IMPORTANT:
- Keep the feedback concise.
- Do not repeat the question.
- Do not give long explanations.
- Do not add extra sections.
- Keep the entire response under 150 words.
"""

    return generate_response(prompt)


def generate_follow_up(question, answer, resume):

    prompt = f"""
You are conducting a technical interview.

Candidate resume:
{resume}

Previous question:
{question}

Candidate answer:
{answer}

Generate ONE challenging follow-up question.

The question must test deeper understanding
of the candidate's answer and resume.

Return ONLY the question.
"""

    return generate_response(prompt)

def transcribe_audio(audio_file):

    audio_bytes = audio_file.getvalue()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            "Transcribe the candidate's speech exactly and return only the transcript.",
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/wav"
            )
        ]
    )

    return response.text.strip()
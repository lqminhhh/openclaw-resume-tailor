---
name: resume-tailor
description: Tailor an existing resume to a target job, generate the tailored resume in strict markdown internally, render exactly one final DOCX file, and return only the saved output path plus concise strengths, gaps, and improvements.
---

# Resume Tailor

Use this skill when the user wants to tailor, customize, revise, or optimize an existing resume for a specific job or role.

## I. Trigger Conditions

Trigger this skill when the user provides:
- a resume and a pasted job description
- a resume and a job link
- a resume and a request to adapt it for a target role

Do not trigger this skill for:
- writing a resume from scratch
- inventing missing experience
- generating cover letters unless explicitly requested as a separate task

## II. Accepted Inputs

Resume inputs may include: `PDF`, `DOC`, `DOCX`, `TEX` (`.tex`)

Job inputs may include:
- pasted job description text
- job link URL
- local job description file if available

## III. Goals

This skill must:
1. Read the source resume.
2. Read the target job description.
3. Generate the tailored resume internally in strict markdown.
4. Render exactly one final saved output file.
5. Save the final output to `resume-project/data/output`.
6. Render the final output as `DOCX`.
7. Preserve factual accuracy.
8. Prefer a compact, one-page-first resume whenever the source content supports it.

## IV. Hard Rules

- Never overwrite the original resume.
- Never return the full tailored resume in chat.
- Never invent, exaggerate, or hallucinate experience.
- Only improve wording, emphasis, ordering, and relevance based on content already present.
- If the source material does not support a claim, do not add it.
- If parsing fails or inputs are insufficient, report the issue clearly.
- Always produce the tailored resume internally as strict markdown first.
- The final saved output must be exactly one file.
- The final saved output must always be `DOCX`.
- Never save a final `.md` file for this skill.
- Do not save both `.docx` and `.md` for the same request.
- Do not stop at a markdown intermediate file.
- Treat the task as incomplete until the final saved output file is rendered in the requested format.
- Optimize for a one-page resume by default when the candidate is early-career or the source resume can reasonably be compressed to one page.
- Only allow the tailored resume to grow beyond one page when the source content is clearly strong, relevant, and cannot be reduced without losing important information.
- The tailored resume must contain these sections in this order when supported by the source content: `EDUCATION`, `EXPERIENCE`, `PROJECTS`, `SKILLS`.
- Include `LEADERSHIP & ACTIVITIES` only when it adds clear value for the target role.
- `EDUCATION` must contain no more than 2 entries.
- `EDUCATION` must contain at most 3 bullets total across the section.
- `EDUCATION` coursework must include at most 4 relevant courses.
- Remove GPA if it is below 3.50.
- `EXPERIENCE` must contain no more than 4 entries.
- If the source resume has more than 4 experience entries, include only the 4 most relevant entries and remove the rest entirely.
- One experience entry means one `**Company Name** | Date Range` block with its role line and bullets.
- The most relevant experience entry may contain at most 4 bullets.
- All other experience entries should contain 1 to 2 bullets when possible.
- `PROJECTS` must contain no more than 2 entries.
- Each project should contain 1 to 2 bullets when possible.
- Each project title line should include at most 3 relevant tools or keywords.
- Each project must use exactly one header line in this format: `**Project Name** | SQL, Python, Tableau`
- Do not add a second italic tools, date, link, or location line under a project title.
- `SKILLS` must remain a compact grouped section with at most 3 lines.
- `LEADERSHIP & ACTIVITIES` may contain at most 2 entries.
- Each leadership/activity entry should contain at most 1 bullet.
- Omit weak, redundant, or low-relevance content instead of expanding the document.
- Avoid repeating the same skills across multiple sections unless necessary.
- Before finalizing the tailored resume markdown, verify that all section-entry caps above are satisfied.
- Before finalizing the task, verify that the saved output path points to `resume-project/data/output`.

## V. Behavioral Guidance

When tailoring:
- prioritize the most relevant experience for the target role
- use keywords from the job description only when truthful
- improve clarity and specificity without changing facts
- de-emphasize less relevant content instead of fabricating new material
- prefer a one-page-first version over a more complete but longer version
- remove weak, redundant, or low-relevance bullets before allowing the resume to expand
- keep bullets short, high-signal, and compact
- prefer dense accomplishment bullets over explanatory prose
- use Google XYZ bullet style when the source material supports it

## VI. Required Workflow

Follow these steps in order:

1. Extract resume text using the local parser:
```bash
python skills/resume-tailor/scripts/parse_resume.py --resume "<RESUME_PATH>"
```

2. Get the target job description:
- if the user pasted the JD directly, use that text directly
- if the user provided a JD file, run:
```bash
python skills/resume-tailor/scripts/parse_job.py --jd-file "<JD_FILE_PATH>"
```
- if the user provided a job URL, run:
```bash
python skills/resume-tailor/scripts/parse_job.py --jd-url "<JOB_URL>"
```

3. Generate the tailored resume in the exact markdown schema below.

4. Render the final output using the local renderer:
```bash
python skills/resume-tailor/scripts/render_output.py \
  --content-file "<TAILORED_RESUME_MARKDOWN_FILE>" \
  --output-dir "resume-project/data/output" \
  --base-name "<OUTPUT_BASE_NAME>"
```

5. Return only:
- `output_file`
- `strengths`
- `gaps`
- `improvements`

## VII. Strict Markdown Resume Template

The tailored resume must strictly be produced in this exact structure:

```markdown
# FULL NAME

email@example.com | phone | LinkedIn | GitHub (if provided)

## EDUCATION
**School Name** | Graduation Date
*Degree, Major / Minor* | Location
- Optional bullet if needed

## EXPERIENCE
**Company Name** | Date Range
*Role Title* | Location
- Bullet 1
- Bullet 2
- Bullet 3

**Company Name** | Date Range
*Role Title* | Location
- Bullet 1
- Bullet 2

## PROJECTS
**Project Name** | Python, SQL, Tableau
- Bullet 1
- Bullet 2

## SKILLS
**Languages:** Python, SQL
**Tools:** Tableau, Excel, Git
**Techniques:** Data Analysis, ETL, Machine Learning

## LEADERSHIP & ACTIVITIES
**Organization Name** | Date Range
*Role Title* | Location
- Bullet 1
```

## VIII. Markdown Formatting Rules

- Use `#` only for the candidate name.
- Use `##` only for section headers.
- Use `**...** | ...` for organization/date lines.
- Use `*...* | ...` for role/location lines only.
- Use `- ` for bullets only.
- Do not use tables.
- Do not use code fences in the generated resume.
- Do not add commentary before or after the markdown resume.
- If a section has no supported content, omit the section instead of fabricating content.
- Keep the markdown compact enough to support a one-page-first DOCX render when possible.
- In `PROJECTS`, do not add any italic subline below the project title.

## IX. Required Output Contract

Internally, produce content equivalent to this structure:

```json
{
  "tailored_resume_markdown": "strict markdown resume here",
  "strengths": ["..."],
  "gaps": ["..."],
  "improvements": ["..."]
}
```

The final chat response must include only:
- `output_file`
- `strengths`
- `gaps`
- `improvements`

Do not include the full tailored resume in the chat response.

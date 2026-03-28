# 📑 Resume Tailor

`resume-tailor` is an OpenClaw skill for tailoring an existing resume to a target job while preserving factual accuracy. It reads a resume, reads a job description, produces a strict internal markdown version of the tailored resume, renders exactly one final `.docx` file, and returns only a concise summary.

## What It Supports

- Resume inputs: `PDF`, `DOCX`, `TEX`
- Job description inputs:
  - pasted text
  - job URL
  - local job description file

## Expected Output

For each run, the skill should:
- save exactly one final `.docx` file under `resume-project/data/output`
- return only:
  - `output_file`
  - `strengths`
  - `gaps`
  - `improvements`

It should not print the full tailored resume in chat.

## Project Structure

```text
skills/resume-tailor/
├── SKILL.md
├── README.md
├── assets/
├── scripts/
│   ├── parse_resume.py
│   ├── parse_job.py
│   ├── render_output.py
│   └── utils.py
└── evals/
    ├── evals.json
    └── files/
        └── expected_notes.md
```

## Local Notes

- `parse_resume.py` extracts text from supported resume formats
- `parse_job.py` normalizes pasted JD text, local JD files, or job URLs
- `render_output.py` renders strict markdown resume content into a final `.docx`

Example renderer usage:

```bash
python skills/resume-tailor/scripts/render_output.py \
  --content-file /path/to/tailored_resume.md \
  --output-dir resume-project/data/output \
  --base-name tailored_resume
```

## Evals

Minimal MVP eval fixtures are included under `skills/resume-tailor/evals/`.

They cover:
- `PDF` + pasted JD
- `PDF` + JD URL
- `DOCX` + pasted JD
- `DOCX` + JD URL
- `TEX` + pasted JD
- `TEX` + JD URL

Use `expected_notes.md` as the manual checklist when reviewing each eval run.

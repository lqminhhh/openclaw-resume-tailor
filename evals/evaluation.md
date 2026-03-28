# Resume Tailor Test Evaluation

This note reflects the actual behavior I observed while testing the `resume-tailor` skill with the eval cases in `evals.json`.

I tested both:

- prompts that explicitly use the skill
- prompts that do not explicitly use the skill

The evals are now grouped into:

- `with_skill`
- `without_skill`

Each eval case also includes a small set of `assertions` so I can record what I specifically checked in that run, such as:

- whether a valid `.docx` file was created
- whether the job description was parsed correctly
- whether the output followed the expected markdown structure before rendering
- whether the run incorrectly left behind a `.md` file
- whether the returned strengths, gaps, and improvements were useful

Overall, both the `with_skill` and `without_skill` prompts worked well in most of the test cases. The system was generally able to read the resume input, process the job description, tailor the resume, and save a new output file.

## What Worked Well

- It correctly returned `strengths`, `gaps`, and `improvements` in a concise format.
- It generated `.docx` output files in the expected location.
- Most of the workflow defined in `SKILL.md` was followed correctly.
- So far, URL scraping has not been a major issue in my tests. The job links I used were processed without major blocking problems.
- The skill generally did a good job producing a tailored result instead of simply rewriting the original resume without direction.
- The per-eval `assertions` made the testing more concrete because I could capture case-specific observations instead of writing only general notes.

## Problems I Observed

- It is hard to guarantee the best possible `.docx` layout for every resume.
- Some resumes have a lot of experience, which can easily push the output beyond one page.
- Other resumes have very little content, which can leave too much white space and make the page feel sparse.
- Because resume density varies a lot from candidate to candidate, a single renderer setup will not always produce the ideal visual format.
- In some test cases, the system still returned a `.md` file in addition to the `.docx` output, even though the intended behavior is to end with only one final `.docx` file.

## Main Takeaway

The core skill behavior is working:

- resume input parsing works
- job description handling works
- summary outputs are useful
- DOCX generation works
- the new eval structure makes it easier to compare `with_skill` and `without_skill` behavior directly

But the testing also showed two practical issues that still need improvement:

- making the final DOCX formatting more adaptable to resumes with very different content density
- ensuring the workflow never leaves behind an extra markdown output when the final contract should be DOCX-only

## Overall Assessment

The skill is already functional and testable through saved eval cases, and the prompt behavior is mostly aligned with the assignment requirements.

The strongest parts right now are:

- summary quality
- output file creation
- general workflow reliability
- job description ingestion

The weakest parts right now are:

- perfectly consistent resume formatting across different resume lengths
- strict enforcement of DOCX-only final output in every test case

## Next Steps

After building this MVP, the next step is to make the skill more reliable and easier to use in a real workflow, not just in controlled eval cases.

Some practical next steps are:

- Improve the DOCX renderer so it can adapt better to resumes with very different content density.
- Enforce the final output contract more strictly so the workflow never leaves behind an extra `.md` file when only a `.docx` file should be returned.
- Expand the eval set with more edge cases, such as very short resumes, very long resumes, and job descriptions that are messy or partially structured.
- Normalize the wording of eval `assertions` so they can be reused more consistently across runs.
- Add more formatting controls, such as smarter spacing, bullet limits, and section balancing, so the final file looks more polished across different resume styles.
- Add stronger validation after generation to check that the final resume still follows the section limits and output rules defined in `SKILL.md`.

One product idea for a next version is drag-and-drop resume upload through a connected interface. Since this MVP is currently being used through OpenClaw UI, I could not fully build that interaction here, but it would be a strong next step to connect OpenClaw with another platform or frontend that allows users to:

- drag and drop a resume directly
- paste or upload a job description
- preview the tailored result
- download the final DOCX file more smoothly

That would make the skill feel much closer to a complete end-user product instead of just a prompt-driven workflow.

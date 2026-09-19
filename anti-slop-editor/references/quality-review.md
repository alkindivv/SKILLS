# Editorial quality review

## Apply hard gates first

Check requested scope/format, protected meaning, evidence boundaries, source
coverage, author voice, and machine-readable integrity. Any changed obligation,
invented material claim, lost exception, broken placeholder, or contradictory
figure needs repair before calling the result final. Do not average away a
serious defect with a high style score.

## Then inspect editorial quality

Consider purpose, specificity, structure, fluency, appropriate concision, register,
and medium fit. Explain a defect through an exact span and its consequence.
Avoid diagnoses such as "80% AI" or a claim that a sentence proves authorship.

When an audit is requested, use a compact structure:
`location | issue | why it matters | proposed repair | confidence`.
Then give the revised text when requested. Do not display a hidden deliberation
transcript; give editorial findings that the user can verify.

When only finished copy is requested, keep this review internal. Surface only
material unresolved issues outside the publishable copy. Do not add routine
scores, audit tables, or version-by-version drafts to every response.

## Test by task

For a report, recheck figures, periods, comparisons, and evidence limits.
For a homepage, recheck product truth and the actual next action.
For a translation, compare source and target for addition, omission, negation,
modality, terminology, names, and variables.
For a summary, recheck scope, caveats, attribution, and missing source coverage.
For a poem or personal essay, check voice and purposeful form before cutting.
For a file, validate its format and rendered output with the appropriate tools.

## Maintain and evaluate the skill

Use `evals/cases.json` as a starting suite, not a benchmark claim. Include tests
where the correct behavior is to keep an existing sentence or preserve formal
language. Add failures from actual use, with permission and private data removed.

To evaluate effectiveness, run identical prompts on the same model/settings with
and without the skill. Randomize output order for reviewers. Score meaning,
usefulness, register, and format separately; treat factual failures as blockers.
Use fresh holdout cases and, for translation, proficient bilingual reviewers.
Record model/version, date, prompts, configuration, and source access. Do not
advertise improvement until such a comparison actually supports it.

The packaged Python tests check the checker and packaging mechanics. The worked
examples demonstrate intended behavior. Neither is independent evidence that
all models will improve or that every output will be free of slop.

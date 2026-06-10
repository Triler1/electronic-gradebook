# Review Report

## Scope

Reviewed the `Triler1/electronic-gradebook` project as of the current `main` branch.
The project is a small Python electronic gradebook with:

- `GradeBook` domain logic in `src/gradebook.py`
- `Student` data model in `src/student.py`
- console output helpers in `src/utils.py`
- a demo entry point in `main.py`
- unit tests in `tests/test_gradebook.py`

Validation run:

```bash
python3 -m unittest discover -s tests -v
```

Result: all 7 existing tests pass.

## Findings

### 1. Missing-student lookup by name silently returns `None`

Severity: Medium

`GradeBook.get_score_by_name()` returns a score when a matching student is found, but falls through with an implicit `None` when the name is unknown.

Location: `src/gradebook.py`, lines 22-25

Why this matters:

- The rest of the public API raises `ValueError` for missing students.
- Callers may treat `None` as a valid result or display it as a score.
- The behavior is not covered by tests, so a future caller can depend on the inconsistent behavior accidentally.

Recommendation:

Raise `ValueError("Студент с таким именем не найден")` or document the `None` contract explicitly. Prefer raising `ValueError` for consistency with `get_score_by_id()`, `update_score()`, and `delete_student()`.

Suggested test:

```python
def test_get_score_by_unknown_name_error(self):
    with self.assertRaises(ValueError):
        self.journal.get_score_by_name("Unknown")
```

### 2. Scores are accepted without validation

Severity: Medium

`add_student()` and `update_score()` accept any value for `score`, including negative numbers, values above the expected grading range, strings, and `None`.

Locations:

- `src/gradebook.py`, line 7
- `src/gradebook.py`, line 12
- `src/student.py`, lines 3-7

Why this matters:

- The gradebook can enter invalid states immediately.
- Console output and future calculations can break or produce misleading results.
- Type hints in `Student` are not runtime validation.

Recommendation:

Add score validation in one place, for example a private helper in `GradeBook` or validation in `Student.__post_init__()`. If the intended range is 0-100, reject non-integer scores and values outside that range. Add tests for invalid scores in both create and update flows.

### 3. Student names are not normalized or validated

Severity: Low

`add_student()` accepts empty strings, whitespace-only names, and duplicate names. `get_score_by_name()` returns the first matching student, so duplicate names create ambiguous lookups.

Locations:

- `src/gradebook.py`, line 7
- `src/gradebook.py`, lines 22-25

Why this matters:

- `get_score_by_name()` can return an arbitrary student's score when names are duplicated.
- Empty names make the gradebook harder to use from the CLI or another UI.

Recommendation:

Decide whether duplicate names are allowed. If they are allowed, avoid name-based lookup or return all matches. If they are not allowed, reject duplicate normalized names in `add_student()`. Also reject empty and whitespace-only names.

### 4. Public internal state can be mutated by callers

Severity: Low

`GradeBook.students` is a public dictionary of mutable `Student` objects. Callers can bypass all validation and error handling by changing the dictionary or the objects directly.

Location: `src/gradebook.py`, line 5

Why this matters:

- Even if validation is added to `add_student()` and `update_score()`, external code can still insert invalid data.
- Tests currently interact only through public methods, so this risk is not visible.

Recommendation:

Rename the attribute to `_students` and keep changes behind methods. If stronger protection is needed, return immutable DTOs or copies from `show_all_students()`.

### 5. Project metadata is missing

Severity: Low

The repository has no `README.md`, dependency metadata, packaging metadata, or test command documentation.

Why this matters:

- New contributors do not have an obvious entry point.
- CI setup is harder because there is no documented supported Python version or canonical test command.

Recommendation:

Add a short `README.md` with project purpose, usage, and test instructions. Add minimal project metadata if the project is meant to be installed or reused.

## Test Coverage Gaps

Existing tests cover the happy path and several ID-based errors. Recommended additions:

- unknown name lookup
- invalid score on add
- invalid score on update
- duplicate or empty names, depending on intended behavior
- ordering contract for `show_all_students()`, if order matters

## Summary

The code is compact and readable, and the current unit test suite passes. The main improvement area is tightening the domain model so invalid gradebook states cannot be created and all lookup methods have consistent error behavior.

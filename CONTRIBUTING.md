# Team collaboration

Use Python 3.12 and the committed Pixi manifest and lock file. Install Pixi
using its official installer: https://pixi.sh/latest/installation/ .
Create one branch per task from the current default branch, and merge through
a pull request. Do not push task changes directly to the default branch.
Ex1 hooks, CSV ignore policy, and type hints need separate coursework PRs
and two non-author reviews/approvals. The Ex1 setup PR is left for its owner
to review and merge.

Agree notebook cell ownership before editing. Prefer separate Python modules
for concurrent code changes; nominate one person to integrate each notebook.
Every author supplies the explanation for their own analysis. Pull the latest
default branch before starting a new task. Coordinate dependency changes and
commit the regenerated pixi.lock with its manifest.

Local agent prompts/configuration, environments, credentials, and scratch
work are ignored. Shared project instructions can be deliberately force-added
only after team agreement. Existing tracked CSVs remain tracked: .gitignore
does not remove them. New local CSVs/databases stay out of commits. Final
figures and submitted notebooks are NOT ignored.

Empty coursework files are intentional placeholders, not completed work.
Do not treat an empty hook configuration or pyproject.toml as functional.
Do not run pre-commit until the relevant configuration has been completed
(except Ex3, which already supplies one). Install hooks separately in every
clone; installation on one computer does not install them for teammates.

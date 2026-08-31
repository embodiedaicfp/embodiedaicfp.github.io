# FLAIRS-40 special track: Embodied AI Agents, Robotics, and IoT

Public web page for the FLAIRS-40 special track on Embodied AI Agents, Robotics, and IoT. FLAIRS-40, the 40th International FLAIRS Conference, takes place at the TradeWinds Resort, St. Pete Beach, Florida, May 24-27, 2027.

Track chair: Marius Silaghi, Florida Institute of Technology. Track co-chair: Muntaser Syed, Florida Institute of Technology.

Live site: https://jemsbhai.github.io/flairs40-tracks/

## What is here

- `index.html`: the whole page (call for papers, topics, dates, submission rules, organizers, program committee, contact)
- `styles.css`: the stylesheet; fonts are loaded from Google Fonts
- `scripts/check.py`: scan to run before every commit
- `.nojekyll`: tells GitHub Pages to serve the files as they are, without Jekyll

There is no build step. Edit the files, run the check, commit, push.

## Editing

All content lives in `index.html`. The edits that will come up most often:

- Dates: the table in the section with `id="dates"`. Cross-check against https://www.flairs-40.info/important-dates before changing anything.
- Program committee: the list in the section with `id="committee"`, alphabetical by surname.
- The "Page updated" line in the footer.

Text rules, enforced by `scripts/check.py`: no em-dashes, en-dashes, curly quotes, or ellipsis characters; none of the words in the banned list inside the script; every in-page anchor points to an existing id; external links use https; the EasyChair link, the two paper deadlines, the conference dates, and both chair emails are present.

## Preview locally

From the repository root, in PowerShell:

    python -m http.server 8000

Then open http://localhost:8000/ in a browser. Stop the server with Ctrl+C.

## Check before committing

    python scripts/check.py

Exit code 0 and an `OK` line mean the page is clean. Any finding is printed as `file:line: message`.

## Hosting

GitHub Pages, deployed from the `main` branch, root folder. In the repository on GitHub: Settings, Pages, Source: Deploy from a branch, Branch: `main`, Folder: `/ (root)`. Pages publishes within a few minutes of each push.

## License

Code and styles are released under the MIT License (see `LICENSE`). The track description and call for papers text belong to the track chairs.

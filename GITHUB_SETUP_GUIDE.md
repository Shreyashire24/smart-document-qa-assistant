# GitHub Setup Guide (Website-Only — No Git Installation Needed)

This guide explains exactly how to put your Smart Document Q&A Assistant on GitHub using **only the GitHub website**. You do not need to install Git or use any command line.

---

## Why Multiple Commits Matter

The assignment explicitly says:

> *"Your repository should include regular commits with meaningful commit messages... The repository must clearly show the evolution of the project across all submission steps."*

That means **you should not upload all files at once**. Instead, you upload them in **five separate batches**, each one representing a stage of the project. This produces a commit history that visibly shows how the project grew.

---

## Step 1 — Create the Repository

1. Go to **https://github.com** and sign in.
2. Click the **"+"** icon in the top-right corner → **"New repository"**.
3. Fill in:
   - **Repository name:** `smart-document-qa-assistant`
   - **Description:** `AI-based document Q&A assistant — Applied System Software (DIP392) at RTU.`
   - **Visibility:** **Public** (the professor needs to be able to open it)
   - **DO NOT** check "Add a README file", "Add .gitignore" or "Choose a license" — your downloaded files already include these.
4. Click **"Create repository"**.

You will land on an empty repo page with instructions. Ignore the command-line instructions — you'll use the website upload feature instead.

---

## Step 2 — Upload Files in Five Batches

For each batch below:

1. On the repo page, click **"Add file"** → **"Upload files"**.
2. **Drag and drop** the files listed for that batch into the upload area.
3. At the bottom of the page, in the **"Commit changes"** box:
   - Enter the **commit message** shown below.
   - Leave the **extended description** blank.
   - Make sure **"Commit directly to the main branch"** is selected.
4. Click the green **"Commit changes"** button.

Wait until each upload finishes before starting the next batch.

---

### Batch 1 — Project skeleton (Step 1 of the course)

**Commit message:** `Initial commit: project skeleton and Step 1 documentation`

Upload these files:

- `README.md`
- `.gitignore`
- `requirements.txt`

After committing, the repo has the basic structure and the documentation explaining what will be built.

---

### Batch 2 — Configuration and tool stubs (early Step 2)

**Commit message:** `Add config module and tool package structure`

Upload these files:

- `config.py`
- `tools/__init__.py`

After committing, the tool package exists but is empty.

---

### Batch 3 — All four tools (Step 2 main work)

**Commit message:** `Implement file reader, search, summary, and statistics tools`

Upload these files (drop them all together into the upload area):

- `tools/file_reader.py`
- `tools/search_tool.py`
- `tools/summary_tool.py`
- `tools/statistics_tool.py`

> **Important:** When uploading files that live inside `tools/`, GitHub's web uploader needs you to **drag the actual files** (not the folder). The web uploader will preserve the `tools/` path automatically if you drag from a file picker that shows the folder structure. If you have trouble, see the *"Uploading into a subfolder"* tip at the end of this guide.

---

### Batch 4 — Agent and main entry point (end of Step 2)

**Commit message:** `Add Agent class with intent detection and CLI entry point`

Upload these files:

- `agent.py`
- `main.py`

After committing, the application is runnable end-to-end.

---

### Batch 5 — Test suite (Step 3)

**Commit message:** `Add pytest test suite covering all tools and agent integration`

Upload these files:

- `tests/__init__.py`
- `tests/conftest.py`
- `tests/fixtures/sample.txt`
- `tests/fixtures/empty.txt`
- `tests/test_file_reader.py`
- `tests/test_search_tool.py`
- `tests/test_summary_tool.py`
- `tests/test_statistics_tool.py`
- `tests/test_agent.py`

---

### Batch 6 — Sample document (final touch)

**Commit message:** `Add sample document for demonstration`

Upload these files:

- `sample_documents/photosynthesis.txt`

---

## Step 3 — Verify the Repository

After all six commits are in:

1. Open your repo's main page. You should see all the files and folders.
2. Click **"commits"** (just above the file list, on the right). You should see all six commits in order with meaningful messages.
3. Click the **README.md** preview at the bottom — confirm it renders correctly.
4. Open one of the Python files (e.g., `agent.py`) and confirm the code is readable on GitHub.

---

## Step 4 — Get the Repo Link for the Final Submission

The link to share with the professor is just the main page URL:

```
https://github.com/<your-username>/smart-document-qa-assistant
```

Replace `<your-username>` with your actual GitHub username. Paste this link at the end of **Section 5 (Deployment Preparation)** of the Final journal document.

---

## Uploading Into a Subfolder (Tip)

If GitHub's web uploader puts files at the root instead of inside `tools/` or `tests/`, do this:

1. Go to the repo main page.
2. Click **"Add file"** → **"Create new file"**.
3. In the filename box, type the folder name followed by a forward slash and then the filename — for example: `tools/file_reader.py`. GitHub will automatically create the folder.
4. Open the corresponding file on your computer in a text editor (Notepad on Windows, TextEdit on Mac, or any IDE), select all the content (Ctrl+A), copy (Ctrl+C), and paste it into the GitHub editor.
5. Scroll down, enter the commit message, and click **"Commit new file"**.

You can also do this trick for ALL the uploads if drag-and-drop is being difficult — just create one file at a time.

---

## What If Something Goes Wrong

- **A file went to the wrong folder?** Click the file in the GitHub repo → click the pencil icon (Edit) → in the filename box, prepend the correct folder name and forward slash (e.g., change `file_reader.py` to `tools/file_reader.py`). Commit the change.
- **Need to delete a file?** Click the file → click the trash icon → commit the deletion.
- **Want to fix a typo in a file?** Click the file → click the pencil icon → edit → commit.

Every change creates a new commit, which is exactly what you want for the evolution history.

---

## Summary of Final Repo Layout

After all batches your repo should look like this on GitHub:

```
smart-document-qa-assistant/
├── README.md
├── .gitignore
├── requirements.txt
├── config.py
├── agent.py
├── main.py
├── tools/
│   ├── __init__.py
│   ├── file_reader.py
│   ├── search_tool.py
│   ├── summary_tool.py
│   └── statistics_tool.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── fixtures/
│   │   ├── sample.txt
│   │   └── empty.txt
│   ├── test_file_reader.py
│   ├── test_search_tool.py
│   ├── test_summary_tool.py
│   ├── test_statistics_tool.py
│   └── test_agent.py
└── sample_documents/
    └── photosynthesis.txt
```

That's it — your project is on GitHub, has a clear commit history showing evolution across all four submission stages, and the link is ready to include in your Final journal submission.

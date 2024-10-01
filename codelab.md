
**Author:** Nischal Olety Nagesh  
**Summary:** This CodeLab will guide you through setting up a GitHub repository to automatically compile a CodeLab markdown file and deploy it to a live site using GitHub Actions and Github Pages
**Categories:** codelab, GitHub Actions, automation  
**Environments:** Web  
**Status:** Published  
**Feedback link:** [GitHub Feedback](https://github.com/nischalon10/codelabtesting/issues/new)

# Automate CodeLab Creation Using GitHub Actions

## Overview  
Duration: 0:03:00

In this CodeLab, you’ll learn how to set up an automation that:
1. Watches for changes to a `codelab.md` file in the `codelab` branch.
2. Compiles the markdown file using the `claat` tool.
3. Pushes the generated HTML and JSON files to a `codelab-page` branch.

By the end of this CodeLab, you'll have your own GitHub repository capable of automatically generating and deploying a CodeLab.


## Step 1: Repository Setup  
Duration: 0:02:00

### Step 1.1: Create a New GitHub Repository
1. Go to GitHub and create a new repository.
2. Name it something like `codelab-automator` (or any name you prefer).
3. Clone the repository to your local machine.

### Step 1.2: Create the Branches
In addition to your existing main branch or any other branch add these two branches with this naming convention
1. Create a `codelab` branch where you'll place the markdown file and most importantly `codelab.yml` file
2. Create a `codelab-page` branch to hold the compiled CodeLab files.

```bash
$ git checkout -b codelab
$ git checkout -b codelab-page
```

## Step 2: Add the CodeLab Markdown File  
Duration: 0:03:00

### Step 2.1: Create a `codelab.md` File
1. On the `codelab` branch, create a markdown file named `codelab.md`.
2. This file will contain the content of your CodeLab.

```bash
$ touch codelab.md
```

### Step 2.2: Example Markdown Content
You can add some basic markdown content for testing:

```markdown
# My First CodeLab
Welcome to this sample CodeLab created with GitHub Actions.

## Section 1
Duration: 0:05:00

This is an example section for testing.
```

Commit the file:

```bash
$ git add codelab.md
$ git commit -m "Added sample codelab.md"
$ git push origin codelab
```

## Step 3: Set Up GitHub Action  
Duration: 0:05:00

Now, you’ll set up a GitHub Action that will:
1. Monitor the `codelab` branch for changes to `codelab.md`.
2. Compile the CodeLab using `claat`.
3. Push the compiled HTML and JSON to the `codelab-page` branch.

### Step 3.1: Create a Workflow File
In your repository, create a `.github/workflows/codelab.yml` file.

```bash
$ mkdir -p .github/workflows
$ touch .github/workflows/codelab.yml
```

### Step 3.2: Add the GitHub Action Code
Copy and paste the following code into the `codelab.yml` file:

```yaml
name: Codelab Export

on:
  push:
    branches:
      - codelab
    paths:
      - 'codelab.md'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        with:
          ref: codelab
          fetch-depth: 0  # Important: This is needed to push back to the repo

      - name: Setup Go
        uses: actions/setup-go@v5

      - name: Install claat
        run: go install github.com/googlecodelabs/tools/claat@latest

      - name: Export codelab
        run: |
          claat export codelab.md

      - name: Push back
        run: |
          git config user.name "codelab-bot"
          git config user.email "<insert your email>"
          mv codelab-4-codelab-markdown/* .
          git add .
          git commit -m "Adding Codelab"
          git checkout codelab-page
          git checkout codelab index.html codelab.json
          git add .
          git commit -m "Updated the HTML and Json"
          git push https://<insert your username>:${{secrets.GH_PAT}}@github.com/<insert your username>/<insert your repository>.git codelab-page
          git checkout codelab
          git reset --hard HEAD^
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}
```

### Step 3.3: Add GitHub Secrets
You’ll need to set up a secret in your GitHub repository for authentication.

1. Go to your repository’s Settings.
2. Click **Secrets and variables** > **Actions**.
3. Create a new secret called `GH_PAT` and paste your GitHub Personal Access Token here.

Here are some resources on how to make a PAT and learn about Secrets 
- [Github PATs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Github Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

## Step 4: Test the Workflow  
Duration: 0:03:00

Now that the action is set up, it's time to test it.

### Step 4.1: Make a Change in the `codelab` Branch
Make any change to your `codelab.md` file, commit, and push the change:

```bash
$ echo "## New Section" >> codelab.md
$ git add codelab.md
$ git commit -m "Added new section"
$ git push origin codelab
```

### Step 4.2: Check the Workflow Run
1. Go to the **Actions** tab in your GitHub repository.
2. You should see the workflow running.
3. Once it’s complete, check the `codelab-page` branch for the generated `index.html` and `codelab.json` files.

## Step 5: Hosting Your CodeLab  
Duration: 0:03:00

Once the files are generated and pushed to the `codelab-page` branch, you can host the CodeLab using GitHub Pages or Netlify.

### Step 5.1: GitHub Pages Setup
1. Go to the **Settings** tab of your repository.
2. Scroll down to the **Pages** section.
3. Set the branch to `codelab-page` and the folder to `/ (root)`.
4. Your CodeLab will now be available at `https://<your-username>.github.io/<your-repository-name>`.

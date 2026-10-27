# Publishing InfraPilot to GitHub when you are ready

These steps intentionally happen only when **you** decide to publish. Review the repository first, especially the files ignored by Git.

1. Create an empty repository named `InfraPilot` on GitHub. Do not add a README, license, or `.gitignore` there because this folder already contains them.
2. In PowerShell, open this project folder and initialise the local history:

   ```powershell
   git init
   git add .
   git status
   ```

3. Carefully read `git status`. It should not list `.venv/`, `reports/`, or real diagnostic output. If you see a sensitive file, stop and remove it from the staging area before continuing.
4. Create the first commit:

   ```powershell
   git commit -m "Initial InfraPilot MVP"
   git branch -M main
   ```

5. Copy the repository URL from GitHub, then connect and push:

   ```powershell
   git remote add origin https://github.com/YOUR-USERNAME/InfraPilot.git
   git push -u origin main
   ```

GitHub may ask you to sign in. Do not share your password or access token in an issue, source file, report, or chat message.

After publishing, enable GitHub’s security features and add a short release note for version 0.1.0.

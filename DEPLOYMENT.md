# Deployment Guide: AI Resume Builder Pro

The easiest way to deploy your Streamlit app for free is using **Streamlit Community Cloud**.

## 1. Prepare your GitHub Repository
1. Create a new repository on [GitHub](https://github.com).
2. Push your project files to this repository.
   - **Crucial:** Do NOT push your `.env` file. Create a `.gitignore` file and add `.env` to it.
   - Files to include: `app.py`, `styles.css`, `requirements.txt`, and the `utils/` folder.

## 2. Deploy to Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Sign in with your GitHub account.
3. Click **"New app"**.
4. Select your repository, branch (`main`), and main file path (`app.py`).

## 3. Set up your Secrets (API Key)
Since you won't be using a `.env` file in the cloud, you need to add your API key to Streamlit's Secrets:
1. In your Streamlit Cloud dashboard, go to your app settings.
2. Find the **"Secrets"** section.
3. Paste the following:
   ```toml
   GOOGLE_API_KEY = "your-actual-api-key-here"
   ```
4. Clicking Save. The app will automatically restart and use this key.

## 4. Alternate Option: Hugging Face Spaces
If you prefer Hugging Face:
1. Create a new "Space".
2. Choose "Streamlit" as the SDK.
3. Upload your files.
4. Add `GOOGLE_API_KEY` under "Settings" > "Variables and Secrets".

## 🚀 That's it! 
Your app will be live at a public URL like `https://your-app-name.streamlit.app`.

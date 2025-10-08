# 🔐 Security Guidelines

## API Key Security

This project uses environment variables to securely store API keys. **Never commit API keys to version control.**

### ✅ Secure Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API key to `.env`:**
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Never commit `.env` files:**
   - `.env` files are in `.gitignore`
   - Only `.env.example` should be committed

### 🚫 What NOT to do

- ❌ Don't hardcode API keys in source code
- ❌ Don't commit `.env` files to Git
- ❌ Don't share your `.env` file with others
- ❌ Don't put API keys in public repositories

### 🔑 Getting API Keys

- **Gemini API:** https://aistudio.google.com/
- Create a new project and generate an API key
- Keep your API keys private and secure

### 🛡️ Security Features

- ✅ No hardcoded API keys in source code
- ✅ Environment variable validation
- ✅ Proper `.gitignore` configuration
- ✅ Clear setup instructions for users

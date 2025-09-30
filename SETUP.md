# Quick Setup Guide - Hong Kong Tourism AI 

## 🚀 Get Started in 3 Steps

### Step 1: Get Your API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key (you'll need it in Step 3)

💡 **Note**: If you get "location not supported" errors, you might need to use a VPN to connect from a supported region.

### Step 2: Download and Open the Project
1. Download or clone this repository
2. Open the folder in VS Code
3. Install the recommended extensions if prompted

### Step 3: Add Your API Key
1. In the `backend` folder, find the `.env` file
2. Replace `your_gemini_api_key_here` with your actual API key from Step 1
3. Save the file

### Step 4: Start Everything
1. Press `Ctrl+Shift+P` in VS Code
2. Type "Tasks: Run Task" and press Enter
3. Select "Start Both Servers"
4. Wait for both servers to start (you'll see "Application startup complete")
5. Open your browser to `http://localhost:3000`

## 🎉 You're Ready!

Your Hong Kong Tourism AI is now running! Try asking it:
- "What are the best dim sum places in Central?"
- "Plan a 2-day itinerary for a food lover"
- "How do I get to Victoria Peak?"

## 🔧 If Something Goes Wrong

### "Location not supported" error?
- Use a VPN to connect from the US or another supported region
- Or try switching to a different Google account

### Frontend won't start?
- Make sure you have Node.js installed
- Try running `npm install` in the frontend folder first

### Backend won't start?
- Make sure you have Python 3.9+ installed
- Try running `pip install -r requirements.txt` in the backend folder first

### Still having issues?
- Check that your API key is correct in the `.env` file
- Make sure both servers show "startup complete" messages
- Try restarting VS Code and running the tasks again

## 📱 Using the App

### On Desktop
- Use the top navigation to switch between features
- Chat, plan trips, translate text, and get recommendations

### On Mobile  
- Use the bottom navigation for easy thumb access
- Tap the camera icon in translation to scan menus and signs
- Everything is optimized for touch and mobile use

## 💡 Pro Tips

- **Ask specific questions**: Instead of "tell me about Hong Kong", ask "best street food in Mong Kok"
- **Use the camera**: Point it at Chinese text for instant translation
- **Set your preferences**: The more you tell it about your interests, the better recommendations you'll get
- **Save favorites**: Use the itinerary planner to save places you want to visit

Enjoy exploring Hong Kong! 🇭🇰✨

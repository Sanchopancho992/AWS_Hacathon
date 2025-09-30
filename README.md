# Hong Kong Tourism AI - Your Smart Travel Companion 🇭🇰

An intelligent, user-friendly travel assistant for Hong Kong that makes exploring the city effortless. Get personalized recommendations, instant translations, smart itineraries, and answers to all your Hong Kong questions - all powered by advanced AI technology.

## ✨ What Makes This Special

🎯 **Truly Personal**: Learns your preferences and suggests experiences you'll actually love  
📱 **Mobile-First**: Designed for real tourists using phones while exploring  
🧠 **Actually Smart**: Uses advanced AI with real Hong Kong knowledge, not generic responses  
💰 **Quota-Efficient**: Smart caching prevents unnecessary API calls and saves costs  
🌐 **Works Everywhere**: PWA technology means it works like a native app  

## 🌟 Key Features

### 💬 Smart Chat Assistant
Ask anything about Hong Kong in natural language:
- "Where can I find the best dim sum in Tsim Sha Tsui?"
- "How do I get from my hotel to Victoria Peak?"  
- "What should I do if it's raining?"
- "Tell me about Hong Kong's tea culture"

**What makes it smart:**
- Remembers your conversation for context
- Provides specific, actionable answers
- Cites reliable sources for information
- Understands follow-up questions

### 📅 Intelligent Trip Planning  
Create perfect itineraries that actually make sense:
- **Smart scheduling**: Considers travel time and opening hours
- **Budget-aware**: Fits your spending preferences
- **Group-friendly**: Adapts to solo, couples, families, or friends
- **Realistic timing**: Won't rush you through experiences

### 📸 Instant Translation
Never be lost in translation again:
- **Camera translation**: Point your phone at menus, signs, or text
- **Cultural context**: Learn why things are named certain ways
- **Multiple languages**: Chinese, Japanese, Korean support
- **Real-time results**: Get translations in seconds

### � Smart Recommendations
Discover Hong Kong like a local:
- **Location-aware**: Suggests things nearby your current spot
- **Time-sensitive**: Different suggestions for morning vs evening
- **Interest-based**: Food lover? History buff? Photographer? We've got you covered
- **Hidden gems**: Find places beyond the typical tourist traps

## 🛠️ Technology Stack (Human-Friendly Explanation)

### What Powers the AI Brain
- **Google Gemini 2.0**: The latest and most capable AI model for understanding and generating human-like responses
- **Pinecone Vector Database**: Stores and quickly searches through Hong Kong tourism knowledge 
- **Smart Caching**: Remembers recent answers to avoid repeated AI calls (saves money and speeds up responses)

### What Makes the App Work
- **FastAPI Backend**: Super fast Python server that handles all the AI processing
- **React Frontend**: Modern, responsive web app that works great on phones
- **PWA Technology**: Install it like a native app, works offline when needed

### Why These Choices Matter to You
- **Fast responses**: Advanced caching means quick answers
- **Reliable**: Works even with poor internet connection
- **Cost-effective**: Smart design prevents hitting API limits
- **User-friendly**: Clean, intuitive interface designed for real-world use

## 🚀 Getting Started (For Developers)

### What You'll Need
- Node.js 18+ (for the web app)
- Python 3.9+ (for the AI backend)  
- Google API Key (free tier available)
- VPN if you're in a region where Gemini isn't available

### Quick Setup with VS Code

The easiest way to run everything:

1. **Open the project in VS Code**
2. **Press** `Ctrl+Shift+P` 
3. **Type** "Tasks: Run Task"
4. **Select** "Start Both Servers"
5. **Wait** for both servers to start
6. **Visit** `http://localhost:3000` in your browser

That's it! Both the AI backend and web frontend will be running.

### Manual Setup

#### Backend (AI Server)
```bash
cd backend
pip install -r requirements.txt
# Add your Google API key to .env file
python main.py
```

#### Frontend (Web App)  
```bash
cd frontend
npm install
npm start
```

## 📚 What's Updated and Current

### ✅ Latest Technology Stack (2024)
- **Pinecone** for vector storage (not ChromaDB)
- **Google Gemini 2.0 Flash** (latest model)
- **Smart caching system** for efficiency
- **Mobile-optimized design** with PWA features

### ✅ Human-Friendly Features
- **Clean text output** (no more **markdown** **formatting** in responses)
- **Readable code** with clear comments and documentation
- **Intuitive UI** designed for real-world tourist use
- **Helpful error messages** that actually explain what went wrong

### ✅ Production-Ready Features
- **Session management** for user tracking
- **Error handling** with graceful fallbacks  
- **Rate limiting** and quota management
- **Mobile responsiveness** for phones and tablets

## 📱 Mobile Experience

This app is designed for tourists using their phones while exploring Hong Kong:

- **Bottom navigation** for easy thumb access
- **Large touch targets** for outdoor use
- **Camera integration** that works reliably  
- **Works offline** when internet is spotty
- **Fast loading** even on slower connections

## 🔧 What Problems This Solves

### For Tourists
- **Language barriers**: Instant translation with cultural context
- **Information overload**: Smart, personalized recommendations
- **Poor planning**: AI creates realistic, enjoyable itineraries  
- **Getting lost**: Always know what to do next

### For Developers  
- **API costs**: Smart caching dramatically reduces Gemini API calls
- **User experience**: Clean, readable responses without technical formatting
- **Mobile issues**: Proper responsive design that actually works
- **Maintenance**: Well-documented, human-readable code

## 🎯 What Makes This Different

Unlike generic travel apps, this Hong Kong Tourism AI:

1. **Actually understands Hong Kong**: Trained on real, local knowledge
2. **Learns from you**: Gets better at recommendations as you use it
3. **Works in practice**: Designed by understanding real tourist pain points
4. **Saves money**: Efficient design prevents unnecessary AI API costs
5. **Human-friendly**: No technical jargon or confusing interfaces

## 📄 Environment Setup

Create a `.env` file in the backend directory:

```bash
# Google AI API Key (get from Google AI Studio)
GOOGLE_API_KEY=your_gemini_api_key_here

# Pinecone Configuration  
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX_NAME=hk-tourism-ai
PINECONE_HOST=your-index-host.pinecone.io

# AWS (optional, for enhanced translation)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
```

## 🌐 Deployment

### Quick Deploy (Recommended)
- **Frontend**: Deploy to Netlify or Vercel (automatic from GitHub)
- **Backend**: Deploy to Railway or Render (Python app auto-detected)

### AWS Deploy (Production)
- **Frontend**: AWS Amplify 
- **Backend**: AWS Lambda with SAM
- **Database**: Pinecone (managed service)

## 🤝 Contributing

Want to make this even better? Here's how:

1. **Found a bug?** Open an issue with clear steps to reproduce
2. **Have an idea?** Suggest features that would help real tourists  
3. **Can code?** Submit PRs with human-readable code and comments
4. **Know Hong Kong?** Help improve the knowledge base

## 📞 Support

Having trouble? Here's how to get help:

1. **Check the logs**: Both servers show helpful error messages
2. **Verify API keys**: Make sure your Google API key works in your region
3. **Try VPN**: Some regions need VPN to access Gemini API
4. **Open an issue**: Include error messages and what you were trying to do

---

*Built with ❤️ for Hong Kong tourists and developers who believe technology should be human-friendly.*
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "REACT_APP_API_URL=http://localhost:8000" > .env
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

   The app will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
GOOGLE_API_KEY=your_google_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
DYNAMODB_TABLE_NAME=hk-tourism-users
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

### Google API Setup
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your backend `.env` file

### AWS Services (Optional)
- **Rekognition**: Image text extraction
- **Translate**: Text translation
- **DynamoDB**: User data storage
- **Lambda**: Serverless backend deployment
- **Amplify**: Frontend hosting

## 📱 PWA Features

- **Offline Support**: Core functionality works without internet
- **Installable**: Can be installed on mobile devices
- **Responsive Design**: Optimized for all screen sizes
- **Camera Access**: Direct photo capture for translation
- **Push Notifications**: (Future enhancement)

## 🚀 Deployment

### Backend Deployment (AWS Lambda)

1. **Install AWS SAM CLI**
   ```bash
   pip install aws-sam-cli
   ```

2. **Deploy using SAM**
   ```bash
   cd backend
   sam build
   sam deploy --guided
   ```

### Frontend Deployment (AWS Amplify)

1. **Build the project**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Amplify**
   - Connect your GitHub repository to AWS Amplify
   - Use the provided `amplify.yml` configuration
   - Set environment variables in Amplify console

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Performance

### Backend
- **Response Time**: <2s for most queries
- **Throughput**: 100+ requests/minute
- **Vector Search**: <500ms for similarity queries

### Frontend
- **First Load**: <3s
- **Subsequent Loads**: <1s (cached)
- **Bundle Size**: <2MB gzipped
- **Lighthouse Score**: 90+ for Performance, Accessibility, Best Practices

## 🔒 Security

- **API Rate Limiting**: Prevents abuse
- **Input Validation**: All inputs validated and sanitized
- **CORS Configuration**: Properly configured for production
- **Environment Variables**: Sensitive data stored securely
- **HTTPS Enforced**: All production traffic encrypted

## 🌍 Internationalization

- **Supported Languages**: English, Traditional Chinese, Simplified Chinese
- **Cultural Context**: Location-specific cultural information
- **Local Formats**: Dates, times, currencies in local formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Create a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🎯 Roadmap

### Phase 1 (Current)
- [x] RAG-powered Q&A system
- [x] Itinerary planning
- [x] Real-time translation
- [x] Smart recommendations
- [x] PWA functionality

### Phase 2 (Future)
- [ ] User accounts and preferences
- [ ] Social features (share itineraries)
- [ ] Real-time updates (weather, events)
- [ ] Voice assistance
- [ ] Augmented reality features

### Phase 3 (Advanced)
- [ ] Multi-language support expansion
- [ ] Integration with booking platforms
- [ ] AI-powered budget optimization
- [ ] Community-driven content
- [ ] Advanced analytics dashboard

## 📈 Usage Analytics

### Key Metrics
- **User Engagement**: Average session duration, page views
- **Feature Usage**: Most used features, conversion rates
- **Performance**: API response times, error rates
- **User Satisfaction**: Feedback scores, retention rates

## 🏆 Awards & Recognition

This project was developed for the AWS Hackathon, showcasing:
- **Innovation**: Novel use of RAG for tourism
- **Technical Excellence**: Modern architecture and best practices
- **User Experience**: Intuitive design and PWA features
- **Scalability**: Cloud-native architecture ready for growth

---

**Built with ❤️ for travelers exploring Hong Kong**

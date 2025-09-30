import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Home } from './pages/Home';
import { Chat } from './pages/Chat';
import { Itinerary } from './pages/Itinerary';
import { Translate } from './pages/Translate';
import { Recommendations } from './pages/Recommendations';
import { ApiProvider } from './context/ApiContext';
import './App.css';

function App() {
  return (
    <ApiProvider>
      <Router>
        <div className="App">
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/itinerary" element={<Itinerary />} />
              <Route path="/translate" element={<Translate />} />
              <Route path="/recommendations" element={<Recommendations />} />
            </Routes>
          </Layout>
        </div>
      </Router>
    </ApiProvider>
  );
}

export default App;

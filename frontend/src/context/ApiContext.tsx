import React, { createContext, useContext, useState, ReactNode } from 'react';
import axios from 'axios';
import {
  ChatRequest,
  ChatResponse,
  ItineraryRequest,
  ItineraryResponse,
  TranslationRequest,
  TranslationResponse,
  RecommendationRequest,
  RecommendationResponse,
} from '../types/api';

// Configure API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

interface ApiContextType {
  // Chat API
  sendMessage: (request: ChatRequest) => Promise<ChatResponse>;
  
  // Itinerary API
  generateItinerary: (request: ItineraryRequest) => Promise<ItineraryResponse>;
  
  // Translation API
  translateText: (request: TranslationRequest) => Promise<TranslationResponse>;
  translateImage: (imageFile: File) => Promise<TranslationResponse>;
  
  // Recommendations API
  getRecommendations: (request: RecommendationRequest) => Promise<RecommendationResponse>;
  
  // Loading states
  isLoading: boolean;
  error: string | null;
}

const ApiContext = createContext<ApiContextType | undefined>(undefined);

interface ApiProviderProps {
  children: ReactNode;
}

export const ApiProvider: React.FC<ApiProviderProps> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleApiCall = async <T,>(apiCall: () => Promise<T>): Promise<T> => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await apiCall();
      return result;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
    return handleApiCall(async () => {
      const response = await api.post('/api/chat', request);
      return response.data;
    });
  };

  const generateItinerary = async (request: ItineraryRequest): Promise<ItineraryResponse> => {
    return handleApiCall(async () => {
      const response = await api.post('/api/itinerary', request);
      return response.data;
    });
  };

  const translateText = async (request: TranslationRequest): Promise<TranslationResponse> => {
    return handleApiCall(async () => {
      const response = await api.post('/api/translate', request);
      return response.data;
    });
  };

  const translateImage = async (imageFile: File): Promise<TranslationResponse> => {
    return handleApiCall(async () => {
      const formData = new FormData();
      formData.append('file', imageFile);
      
      const response = await api.post('/api/translate-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    });
  };

  const getRecommendations = async (request: RecommendationRequest): Promise<RecommendationResponse> => {
    return handleApiCall(async () => {
      const response = await api.post('/api/recommendations', request);
      return response.data;
    });
  };

  const value: ApiContextType = {
    sendMessage,
    generateItinerary,
    translateText,
    translateImage,
    getRecommendations,
    isLoading,
    error,
  };

  return (
    <ApiContext.Provider value={value}>
      {children}
    </ApiContext.Provider>
  );
};

export const useApi = (): ApiContextType => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};

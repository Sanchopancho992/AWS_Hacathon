export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface UserContext {
  location?: string;
  language_preference: string;
  interests: string[];
  budget_range?: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  conversation_history: ConversationMessage[];
  user_context?: UserContext;
}

export interface Source {
  title: string;
  content: string;
  url?: string;
  relevance_score: number;
}

export interface ChatResponse {
  message: string;
  sources: Source[];
  conversation_id?: string;
}

export interface ItineraryRequest {
  duration: number;
  interests: string[];
  budget: 'low' | 'medium' | 'high';
  accommodation?: string;
  travel_style: 'slow' | 'moderate' | 'fast';
  group_size: number;
  special_requirements?: string[];
}

export interface Activity {
  name: string;
  time: string;
  duration: string;
  cost: number;
  description: string;
  transport: string;
  tips: string;
}

export interface DayPlan {
  day: number;
  date?: string;
  activities: Activity[];
  estimated_cost?: number;
  transportation_info?: string;
}

export interface ItineraryResponse {
  itinerary: DayPlan[];
  total_estimated_cost?: number;
  tips: string[];
}

export interface TranslationRequest {
  text: string;
  source_language: string;
  target_language: string;
  context_type?: string;
}

export interface TranslationResponse {
  translated_text: string;
  original_text?: string;
  cultural_context?: string;
  confidence: number;
}

export interface RecommendationRequest {
  user_preferences: Record<string, any>;
  current_location?: string;
  time_context?: string;
  limit: number;
}

export interface Recommendation {
  name: string;
  description: string;
  category: string;
  location: string;
  rating?: number;
  estimated_time?: string;
  cost_range?: string;
  reasons: string[];
}

export interface RecommendationResponse {
  recommendations: Recommendation[];
}

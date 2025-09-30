import React, { useState, useEffect, useRef } from 'react';
import { MapPin, Clock, DollarSign, Star, Filter, Loader2 } from 'lucide-react';
import { useApi } from '../context/ApiContext';
import { RecommendationRequest, Recommendation } from '../types/api';

export const Recommendations: React.FC = () => {
  const { getRecommendations, isLoading, error } = useApi();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const hasInitialized = useRef(false);
  const [filters, setFilters] = useState({
    interests: [] as string[],
    budget: 'medium',
    time_context: '',
    location: '',
  });
  const [showFilters, setShowFilters] = useState(false);

  const interestOptions = [
    'Food & Dining',
    'Cultural Sites',
    'Shopping',
    'Nature & Hiking',
    'Nightlife',
    'Museums',
    'Architecture',
    'Photography',
    'Local Markets',
    'History',
  ];

  const timeContextOptions = [
    { value: '', label: 'Any Time' },
    { value: 'morning', label: 'Morning (6AM-12PM)' },
    { value: 'afternoon', label: 'Afternoon (12PM-6PM)' },
    { value: 'evening', label: 'Evening (6PM-12AM)' },
  ];

  const locationOptions = [
    { value: '', label: 'All Areas' },
    { value: 'Central', label: 'Central' },
    { value: 'Tsim Sha Tsui', label: 'Tsim Sha Tsui' },
    { value: 'Causeway Bay', label: 'Causeway Bay' },
    { value: 'Mong Kok', label: 'Mong Kok' },
    { value: 'Wan Chai', label: 'Wan Chai' },
    { value: 'Sheung Wan', label: 'Sheung Wan' },
  ];

  const fetchRecommendations = async (customFilters?: typeof filters) => {
    try {
      const filtersToUse = customFilters || filters;
      const request: RecommendationRequest = {
        user_preferences: {
          interests: filtersToUse.interests,
          budget: filtersToUse.budget,
        },
        current_location: filtersToUse.location || undefined,
        time_context: filtersToUse.time_context || undefined,
        limit: 10,
      };

      const response = await getRecommendations(request);
      setRecommendations(response.recommendations);
    } catch (err) {
      // Error handled by context
    }
  };

  // Load initial recommendations only once on component mount
  useEffect(() => {
    if (!hasInitialized.current) {
      hasInitialized.current = true;
      
      const loadInitialRecommendations = async () => {
        try {
          const request: RecommendationRequest = {
            user_preferences: {
              interests: [],
              budget: 'medium',
            },
            limit: 10,
          };

          const response = await getRecommendations(request);
          setRecommendations(response.recommendations);
        } catch (err) {
          // Error handled by context
        }
      };

      loadInitialRecommendations();
    }
  }); // No dependency array to avoid re-running

  const handleInterestToggle = (interest: string) => {
    setFilters(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest],
    }));
  };

  const applyFilters = () => {
    // Use the current filters state directly
    fetchRecommendations(filters);
    setShowFilters(false);
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case 'food':
      case 'restaurant':
        return '🍜';
      case 'attraction':
      case 'sightseeing':
        return '🏛️';
      case 'shopping':
        return '🛍️';
      case 'nature':
      case 'outdoor':
        return '🌿';
      case 'culture':
      case 'cultural':
        return '🎭';
      case 'nightlife':
        return '🌃';
      default:
        return '📍';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'food':
      case 'restaurant':
        return 'bg-orange-100 text-orange-800';
      case 'attraction':
      case 'sightseeing':
        return 'bg-blue-100 text-blue-800';
      case 'shopping':
        return 'bg-purple-100 text-purple-800';
      case 'nature':
      case 'outdoor':
        return 'bg-green-100 text-green-800';
      case 'culture':
      case 'cultural':
        return 'bg-red-100 text-red-800';
      case 'nightlife':
        return 'bg-indigo-100 text-indigo-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Discover Hong Kong
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Get personalized recommendations based on your interests and preferences
          </p>
        </div>

        {/* Filter Section */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Recommendations for You
            </h2>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center px-4 py-2 text-primary-600 border border-primary-600 rounded-lg hover:bg-primary-50 transition-colors"
            >
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </button>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Interests */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Interests
                  </label>
                  <div className="space-y-2 max-h-40 overflow-y-auto">
                    {interestOptions.map(interest => (
                      <label key={interest} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.interests.includes(interest)}
                          onChange={() => handleInterestToggle(interest)}
                          className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">{interest}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Budget */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Budget
                  </label>
                  <select
                    value={filters.budget}
                    onChange={(e) => setFilters(prev => ({ ...prev, budget: e.target.value }))}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="low">Budget (HK$200-500/day)</option>
                    <option value="medium">Moderate (HK$500-1000/day)</option>
                    <option value="high">Premium (HK$1000+/day)</option>
                  </select>
                </div>

                {/* Time */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Time of Day
                  </label>
                  <select
                    value={filters.time_context}
                    onChange={(e) => setFilters(prev => ({ ...prev, time_context: e.target.value }))}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {timeContextOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Location */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Location
                  </label>
                  <select
                    value={filters.location}
                    onChange={(e) => setFilters(prev => ({ ...prev, location: e.target.value }))}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {locationOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="flex justify-end mt-6 space-x-3">
                <button
                  onClick={() => setShowFilters(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={applyFilters}
                  disabled={isLoading}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                      Loading...
                    </>
                  ) : (
                    'Apply Filters'
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Recommendations Grid */}
        {isLoading && recommendations.length === 0 ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <Loader2 className="w-12 h-12 animate-spin text-primary-600 mx-auto mb-4" />
              <p className="text-gray-600">Finding the best recommendations for you...</p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((recommendation, index) => (
              <div
                key={index}
                className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{getCategoryIcon(recommendation.category)}</span>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {recommendation.name}
                        </h3>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCategoryColor(recommendation.category)}`}>
                            {recommendation.category}
                          </span>
                          {recommendation.rating && (
                            <div className="flex items-center">
                              <Star className="w-4 h-4 text-yellow-400 fill-current" />
                              <span className="text-sm text-gray-600 ml-1">
                                {recommendation.rating}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-gray-600 text-sm leading-relaxed mb-4">
                    {recommendation.description}
                  </p>

                  {/* Details */}
                  <div className="space-y-2 mb-4">
                    {recommendation.location && (
                      <div className="flex items-center text-sm text-gray-600">
                        <MapPin className="w-4 h-4 mr-2 flex-shrink-0" />
                        <span>{recommendation.location}</span>
                      </div>
                    )}
                    
                    {recommendation.estimated_time && (
                      <div className="flex items-center text-sm text-gray-600">
                        <Clock className="w-4 h-4 mr-2 flex-shrink-0" />
                        <span>{recommendation.estimated_time}</span>
                      </div>
                    )}
                    
                    {recommendation.cost_range && (
                      <div className="flex items-center text-sm text-gray-600">
                        <DollarSign className="w-4 h-4 mr-2 flex-shrink-0" />
                        <span>{recommendation.cost_range}</span>
                      </div>
                    )}
                  </div>

                  {/* Reasons */}
                  {recommendation.reasons && recommendation.reasons.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 mb-2">
                        Why we recommend this:
                      </h4>
                      <ul className="space-y-1">
                        {recommendation.reasons.slice(0, 3).map((reason, reasonIndex) => (
                          <li key={reasonIndex} className="text-sm text-gray-600 flex items-start">
                            <span className="text-primary-600 mr-2">•</span>
                            <span>{reason}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && recommendations.length === 0 && (
          <div className="text-center py-20">
            <MapPin className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">
              No recommendations found
            </h3>
            <p className="text-gray-600 mb-6">
              Try adjusting your filters or interests to discover more places.
            </p>
            <button
              onClick={() => setShowFilters(true)}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Update Preferences
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

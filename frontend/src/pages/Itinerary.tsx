import React, { useState } from 'react';
import { Calendar, Clock, DollarSign, Users, MapPin, Loader2, Download } from 'lucide-react';
import { useApi } from '../context/ApiContext';
import { ItineraryRequest, DayPlan } from '../types/api';

export const Itinerary: React.FC = () => {
  const { generateItinerary, isLoading, error } = useApi();
  const [formData, setFormData] = useState<ItineraryRequest>({
    duration: 3,
    interests: [],
    budget: 'medium',
    accommodation: '',
    travel_style: 'moderate',
    group_size: 1,
    special_requirements: [],
  });
  const [generatedItinerary, setGeneratedItinerary] = useState<DayPlan[] | null>(null);

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

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest],
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const response = await generateItinerary(formData);
      setGeneratedItinerary(response.itinerary);
    } catch (err) {
      // Error handled by context
    }
  };

  const resetForm = () => {
    setGeneratedItinerary(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            AI Itinerary Planner
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create a personalized Hong Kong travel itinerary based on your preferences and style
          </p>
        </div>

        {!generatedItinerary ? (
          /* Planning Form */
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Trip Duration */}
              <div>
                <label className="block text-lg font-semibold text-gray-900 mb-4">
                  <Calendar className="inline w-5 h-5 mr-2" />
                  Trip Duration
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {[1, 2, 3, 4, 5, 6, 7].map(days => (
                    <button
                      key={days}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, duration: days }))}
                      className={`p-3 rounded-lg border-2 text-center transition-colors ${
                        formData.duration === days
                          ? 'border-primary-600 bg-primary-50 text-primary-600'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {days} {days === 1 ? 'Day' : 'Days'}
                    </button>
                  ))}
                </div>
              </div>

              {/* Interests */}
              <div>
                <label className="block text-lg font-semibold text-gray-900 mb-4">
                  <MapPin className="inline w-5 h-5 mr-2" />
                  Interests (Select all that apply)
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  {interestOptions.map(interest => (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => handleInterestToggle(interest)}
                      className={`p-3 rounded-lg border-2 text-left transition-colors ${
                        formData.interests.includes(interest)
                          ? 'border-primary-600 bg-primary-50 text-primary-600'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {interest}
                    </button>
                  ))}
                </div>
              </div>

              {/* Budget */}
              <div>
                <label className="block text-lg font-semibold text-gray-900 mb-4">
                  <DollarSign className="inline w-5 h-5 mr-2" />
                  Budget Level
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {[
                    { value: 'low', label: 'Budget', desc: 'HK$200-500/day' },
                    { value: 'medium', label: 'Moderate', desc: 'HK$500-1000/day' },
                    { value: 'high', label: 'Premium', desc: 'HK$1000+/day' },
                  ].map(option => (
                    <button
                      key={option.value}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, budget: option.value as any }))}
                      className={`p-4 rounded-lg border-2 text-left transition-colors ${
                        formData.budget === option.value
                          ? 'border-primary-600 bg-primary-50 text-primary-600'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="font-medium">{option.label}</div>
                      <div className="text-sm opacity-75">{option.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Travel Style */}
              <div>
                <label className="block text-lg font-semibold text-gray-900 mb-4">
                  <Clock className="inline w-5 h-5 mr-2" />
                  Travel Style
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {[
                    { value: 'slow', label: 'Relaxed', desc: '2-3 activities per day' },
                    { value: 'moderate', label: 'Balanced', desc: '3-4 activities per day' },
                    { value: 'fast', label: 'Packed', desc: '4-5 activities per day' },
                  ].map(option => (
                    <button
                      key={option.value}
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, travel_style: option.value as any }))}
                      className={`p-4 rounded-lg border-2 text-left transition-colors ${
                        formData.travel_style === option.value
                          ? 'border-primary-600 bg-primary-50 text-primary-600'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <div className="font-medium">{option.label}</div>
                      <div className="text-sm opacity-75">{option.desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Group Size & Accommodation */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label className="block text-lg font-semibold text-gray-900 mb-4">
                    <Users className="inline w-5 h-5 mr-2" />
                    Group Size
                  </label>
                  <select
                    value={formData.group_size}
                    onChange={(e) => setFormData(prev => ({ ...prev, group_size: parseInt(e.target.value) }))}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {[1, 2, 3, 4, 5, 6].map(size => (
                      <option key={size} value={size}>
                        {size} {size === 1 ? 'Person' : 'People'}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-lg font-semibold text-gray-900 mb-4">
                    Accommodation Area (Optional)
                  </label>
                  <input
                    type="text"
                    value={formData.accommodation}
                    onChange={(e) => setFormData(prev => ({ ...prev, accommodation: e.target.value }))}
                    placeholder="e.g., Central, Tsim Sha Tsui, Causeway Bay"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Error Display */}
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-600">{error}</p>
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-center">
                <button
                  type="submit"
                  disabled={isLoading || formData.interests.length === 0}
                  className="px-8 py-4 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center text-lg font-medium"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin mr-2" />
                      Creating Your Itinerary...
                    </>
                  ) : (
                    'Generate Itinerary'
                  )}
                </button>
              </div>
            </form>
          </div>
        ) : (
          /* Generated Itinerary */
          <div className="space-y-8">
            {/* Header with actions */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <div className="flex justify-between items-center">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">
                    Your {formData.duration}-Day Hong Kong Itinerary
                  </h2>
                  <p className="text-gray-600 mt-1">
                    {formData.budget.charAt(0).toUpperCase() + formData.budget.slice(1)} budget • {formData.travel_style} pace
                  </p>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={() => window.print()}
                    className="px-4 py-2 text-primary-600 border border-primary-600 rounded-lg hover:bg-primary-50 transition-colors flex items-center"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Export
                  </button>
                  <button
                    onClick={resetForm}
                    className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    Create New
                  </button>
                </div>
              </div>
            </div>

            {/* Itinerary Days */}
            {generatedItinerary.map((day, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="bg-primary-600 text-white p-6">
                  <h3 className="text-xl font-bold">Day {day.day}</h3>
                  {day.estimated_cost && (
                    <p className="text-primary-100 mt-1">
                      Estimated cost: HK${day.estimated_cost}
                    </p>
                  )}
                </div>
                
                <div className="p-6">
                  <div className="space-y-6">
                    {day.activities.map((activity, actIndex) => (
                      <div key={actIndex} className="border-l-4 border-primary-200 pl-6">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="text-lg font-semibold text-gray-900">
                            {activity.name}
                          </h4>
                          {activity.cost > 0 && (
                            <span className="text-primary-600 font-medium">
                              HK${activity.cost}
                            </span>
                          )}
                        </div>
                        
                        <div className="text-gray-600 space-y-2">
                          {activity.time && (
                            <p><Clock className="inline w-4 h-4 mr-1" /> {activity.time}</p>
                          )}
                          {activity.duration && (
                            <p>Duration: {activity.duration}</p>
                          )}
                          {activity.description && (
                            <p>{activity.description}</p>
                          )}
                          {activity.transport && (
                            <p><MapPin className="inline w-4 h-4 mr-1" /> {activity.transport}</p>
                          )}
                          {activity.tips && (
                            <p className="text-blue-600 bg-blue-50 p-2 rounded">
                              💡 {activity.tips}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  {day.transportation_info && (
                    <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                      <h5 className="font-medium text-gray-900 mb-2">Transportation Tips:</h5>
                      <p className="text-gray-600">{day.transportation_info}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

import React from 'react';
import { Link } from 'react-router-dom';
import { 
  MessageCircle, 
  Calendar, 
  Languages, 
  MapPin,
  ArrowRight,
  Star,
  Users,
  Clock
} from 'lucide-react';

const features = [
  {
    icon: MessageCircle,
    title: 'AI Travel Assistant',
    description: 'Ask questions about Hong Kong attractions, culture, food, and transportation',
    link: '/chat',
    color: 'bg-blue-500',
  },
  {
    icon: Calendar,
    title: 'Smart Itinerary Planner',
    description: 'Get personalized day-by-day travel plans based on your interests and budget',
    link: '/itinerary',
    color: 'bg-green-500',
  },
  {
    icon: Languages,
    title: 'Real-time Translation',
    description: 'Translate menus, signs, and conversations with cultural context',
    link: '/translate',
    color: 'bg-purple-500',
  },
  {
    icon: MapPin,
    title: 'Local Recommendations',
    description: 'Discover hidden gems and popular spots tailored to your preferences',
    link: '/recommendations',
    color: 'bg-orange-500',
  },
];

const stats = [
  { icon: Star, value: '4.9/5', label: 'User Rating' },
  { icon: Users, value: '50K+', label: 'Happy Travelers' },
  { icon: Clock, value: '24/7', label: 'AI Support' },
];

export const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <section className="relative px-4 pt-16 pb-20 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Your AI-Powered
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-secondary-600">
                {' '}Hong Kong{' '}
              </span>
              Travel Guide
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Discover Hong Kong like never before with our intelligent travel assistant. 
              Get personalized recommendations, instant translations, and smart itineraries 
              powered by advanced AI.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/chat"
                className="inline-flex items-center px-8 py-3 text-lg font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 transition-colors"
              >
                Start Planning
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/itinerary"
                className="inline-flex items-center px-8 py-3 text-lg font-medium text-primary-600 bg-white border-2 border-primary-600 rounded-lg hover:bg-primary-50 transition-colors"
              >
                Create Itinerary
              </Link>
            </div>
          </div>
        </div>

        {/* Floating Elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-yellow-200 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-pink-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-blue-200 rounded-full opacity-20 animate-pulse delay-500"></div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-3 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-3">
                    <Icon className="w-8 h-8 text-primary-600" />
                  </div>
                  <div className="text-2xl font-bold text-gray-900 mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-600">
                    {stat.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Everything You Need for the Perfect Hong Kong Trip
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform combines local expertise with cutting-edge technology 
              to make your Hong Kong adventure unforgettable.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Link
                  key={index}
                  to={feature.link}
                  className="group relative p-8 bg-white rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-primary-200"
                >
                  <div className="flex items-start space-x-4">
                    <div className={`flex-shrink-0 w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                        {feature.title}
                      </h3>
                      <p className="text-gray-600 leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all" />
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Explore Hong Kong?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of travelers who've discovered the perfect Hong Kong experience 
            with our AI travel assistant.
          </p>
          <Link
            to="/chat"
            className="inline-flex items-center px-8 py-4 text-lg font-medium text-primary-600 bg-white rounded-lg hover:bg-gray-50 transition-colors"
          >
            Get Started Now
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

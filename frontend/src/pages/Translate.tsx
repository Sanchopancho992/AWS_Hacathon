import React, { useState, useRef } from 'react';
import { Camera, Upload, Languages, Loader2, Copy, Volume2 } from 'lucide-react';
import { useApi } from '../context/ApiContext';
import { TranslationRequest } from '../types/api';

export const Translate: React.FC = () => {
  const { translateText, translateImage, isLoading, error } = useApi();
  const [activeTab, setActiveTab] = useState<'text' | 'image'>('text');
  const [textInput, setTextInput] = useState('');
  const [sourceLanguage, setSourceLanguage] = useState('auto');
  const [targetLanguage, setTargetLanguage] = useState('en');
  const [translation, setTranslation] = useState<any>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [cameraActive, setCameraActive] = useState(false);

  const languages = [
    { code: 'auto', name: 'Auto-detect' },
    { code: 'en', name: 'English' },
    { code: 'zh', name: 'Chinese (Traditional)' },
    { code: 'zh-cn', name: 'Chinese (Simplified)' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
  ];

  const contextTypes = [
    { value: '', label: 'General' },
    { value: 'menu', label: 'Restaurant Menu' },
    { value: 'sign', label: 'Street Sign' },
    { value: 'conversation', label: 'Conversation' },
  ];

  const [contextType, setContextType] = useState('');

  const handleTextTranslation = async () => {
    if (!textInput.trim()) return;

    try {
      const request: TranslationRequest = {
        text: textInput,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        context_type: contextType || undefined,
      };

      const result = await translateText(request);
      setTranslation(result);
    } catch (err) {
      // Error handled by context
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
      
      handleImageTranslation(file);
    }
  };

  const handleImageTranslation = async (file: File) => {
    try {
      const result = await translateImage(file);
      setTranslation(result);
    } catch (err) {
      // Error handled by context
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } // Use back camera on mobile
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
      }
    } catch (err) {
      console.error('Camera access denied:', err);
      alert('Camera access is required for this feature.');
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setCameraActive(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(video, 0, 0);
        
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
            const url = URL.createObjectURL(blob);
            setImagePreview(url);
            handleImageTranslation(file);
            stopCamera();
          }
        }, 'image/jpeg', 0.8);
      }
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  const speakText = (text: string, lang: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang === 'zh' ? 'zh-HK' : lang;
      speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Real-time Translation
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Translate text or images with cultural context for Hong Kong
          </p>
        </div>

        {/* Tab Selection */}
        <div className="flex mb-8">
          <button
            onClick={() => setActiveTab('text')}
            className={`flex-1 py-3 px-6 text-center font-medium rounded-l-lg border-2 transition-colors ${
              activeTab === 'text'
                ? 'bg-primary-600 text-white border-primary-600'
                : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'
            }`}
          >
            <Languages className="inline w-5 h-5 mr-2" />
            Text Translation
          </button>
          <button
            onClick={() => setActiveTab('image')}
            className={`flex-1 py-3 px-6 text-center font-medium rounded-r-lg border-2 border-l-0 transition-colors ${
              activeTab === 'image'
                ? 'bg-primary-600 text-white border-primary-600'
                : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'
            }`}
          >
            <Camera className="inline w-5 h-5 mr-2" />
            Image Translation
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              {activeTab === 'text' ? 'Enter Text' : 'Upload or Capture Image'}
            </h2>

            {activeTab === 'text' ? (
              /* Text Input */
              <div className="space-y-4">
                {/* Language Selection */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      From
                    </label>
                    <select
                      value={sourceLanguage}
                      onChange={(e) => setSourceLanguage(e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    >
                      {languages.map(lang => (
                        <option key={lang.code} value={lang.code}>
                          {lang.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      To
                    </label>
                    <select
                      value={targetLanguage}
                      onChange={(e) => setTargetLanguage(e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    >
                      {languages.filter(lang => lang.code !== 'auto').map(lang => (
                        <option key={lang.code} value={lang.code}>
                          {lang.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Context Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Context (Optional)
                  </label>
                  <select
                    value={contextType}
                    onChange={(e) => setContextType(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    {contextTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Text Input */}
                <div>
                  <textarea
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    placeholder="Enter text to translate..."
                    rows={6}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                  />
                </div>

                <button
                  onClick={handleTextTranslation}
                  disabled={!textInput.trim() || isLoading}
                  className="w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin mr-2" />
                      Translating...
                    </>
                  ) : (
                    'Translate'
                  )}
                </button>
              </div>
            ) : (
              /* Image Input */
              <div className="space-y-6">
                {/* Camera */}
                {!cameraActive ? (
                  <button
                    onClick={startCamera}
                    className="w-full py-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors flex flex-col items-center"
                  >
                    <Camera className="w-12 h-12 text-gray-400 mb-2" />
                    <span className="text-gray-600">Take Photo</span>
                  </button>
                ) : (
                  <div className="space-y-4">
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      className="w-full rounded-lg"
                    />
                    <div className="flex space-x-3">
                      <button
                        onClick={capturePhoto}
                        className="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                      >
                        Capture
                      </button>
                      <button
                        onClick={stopCamera}
                        className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

                {/* File Upload */}
                <div className="text-center text-gray-500">or</div>
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
                
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  className="w-full py-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors flex flex-col items-center disabled:opacity-50"
                >
                  <Upload className="w-12 h-12 text-gray-400 mb-2" />
                  <span className="text-gray-600">Upload Image</span>
                </button>

                {/* Image Preview */}
                {imagePreview && (
                  <div className="mt-4">
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="w-full rounded-lg shadow-sm"
                    />
                  </div>
                )}
              </div>
            )}

            <canvas ref={canvasRef} className="hidden" />
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Translation Result</h2>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg mb-6">
                <p className="text-red-600">{error}</p>
              </div>
            )}

            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
                <span className="ml-3 text-gray-600">Processing...</span>
              </div>
            ) : translation ? (
              <div className="space-y-6">
                {/* Original Text (for images) */}
                {translation.original_text && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Detected Text:</h3>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <p className="text-gray-900">{translation.original_text}</p>
                    </div>
                  </div>
                )}

                {/* Translation */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-medium text-gray-700">Translation:</h3>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => copyToClipboard(translation.translated_text)}
                        className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Copy"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => speakText(translation.translated_text, targetLanguage)}
                        className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Listen"
                      >
                        <Volume2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  <div className="p-4 bg-primary-50 rounded-lg border border-primary-200">
                    <p className="text-gray-900 text-lg">{translation.translated_text}</p>
                  </div>
                </div>

                {/* Cultural Context */}
                {translation.cultural_context && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Cultural Context:</h3>
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <p className="text-blue-900">{translation.cultural_context}</p>
                    </div>
                  </div>
                )}

                {/* Confidence */}
                {translation.confidence > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-700 mb-2">Confidence:</h3>
                    <div className="flex items-center">
                      <div className="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${translation.confidence * 100}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-600">
                        {Math.round(translation.confidence * 100)}%
                      </span>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Languages className="w-12 h-12 mx-auto mb-4 opacity-30" />
                <p>Translation results will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

import React from 'react';
import { MarketPulse } from './MarketPulse';

export const AuthHero: React.FC = () => (
  <div className="relative w-full md:w-1/2 bg-gradient-to-br from-blue-600 to-indigo-800 p-8 md:p-12 flex flex-col justify-between overflow-hidden">
    <div className="absolute inset-0 bg-grid-white/[0.2] -z-1" />
    
    <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-blue-400 opacity-20 blur-3xl" />
    <div className="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-indigo-400 opacity-20 blur-3xl" />
    
    <div className="relative z-10">
      <h1 className="text-3xl md:text-5xl font-bold text-white mb-4">
        Macedonian Stock Exchange
      </h1>
      <p className="text-blue-100 text-lg md:text-xl font-light">
        Empowering your investment decisions with real-time market insights
      </p>
    </div>

    <MarketPulse />
  </div>
);
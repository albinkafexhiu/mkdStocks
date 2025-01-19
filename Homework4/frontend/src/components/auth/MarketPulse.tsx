import React from 'react';

export const MarketPulse: React.FC = () => (
  <div className="relative z-10 backdrop-blur-lg bg-white/10 rounded-2xl p-6 mt-8 md:mt-0">
    <h3 className="text-white text-xl mb-4 font-medium">Market Pulse</h3>
    <div className="space-y-4">
      <div className="flex justify-between items-center text-sm">
        <span className="text-blue-100">MBI10 Index</span>
        <span className="text-emerald-400 font-medium">+1.2%</span>
      </div>
      <div className="flex justify-between items-center text-sm">
        <span className="text-blue-100">Daily Volume</span>
        <span className="text-white font-medium">€2.5M</span>
      </div>
      <div className="flex justify-between items-center text-sm">
        <span className="text-blue-100">Market Status</span>
        <span className="text-emerald-400 font-medium">Open</span>
      </div>
    </div>
  </div>
);

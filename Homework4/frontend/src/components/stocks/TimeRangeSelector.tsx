import React from 'react';
import { TimeRange } from '../../types/stockdata';

interface TimeRangeSelectorProps {
  timeRanges: TimeRange[];
  onSelect: (days: number) => void;
}

export const TimeRangeSelector: React.FC<TimeRangeSelectorProps> = ({ timeRanges, onSelect }) => (
  <div className="flex flex-wrap gap-2 mb-6">
    {timeRanges.map((range) => (
      <button
        key={range.label}
        onClick={() => onSelect(range.days)}
        className="px-4 py-2 rounded-lg bg-blue-100 hover:bg-blue-200 text-blue-700 font-medium"
      >
        {range.label}
      </button>
    ))}
  </div>
);
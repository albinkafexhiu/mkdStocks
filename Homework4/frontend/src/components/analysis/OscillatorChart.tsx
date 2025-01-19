import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AnalysisData, PeriodOption } from '../../types/analysis';

interface OscillatorChartProps {
  data: AnalysisData[];
  period: PeriodOption;
}

export const OscillatorChart: React.FC<OscillatorChartProps> = ({ data, period }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="h-96 w-full mt-4 bg-white p-4 rounded-lg shadow">
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            interval="preserveStartEnd"
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: 'white', border: '1px solid #ccc' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey={`stoch_k_${period}`}
            stroke="#2563eb"
            dot={false}
            name="Stochastic %K"
          />
          <Line
            type="monotone"
            dataKey={`stoch_d_${period}`}
            stroke="#16a34a"
            dot={false}
            name="Stochastic %D"
          />
          <Line
            type="monotone"
            dataKey={`mfi_${period}`}
            stroke="#9333ea"
            dot={false}
            name="MFI"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
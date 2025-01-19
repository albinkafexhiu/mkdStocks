import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AnalysisData, PeriodOption } from '../../types/analysis';

interface PriceChartProps {
  data: AnalysisData[];
  period: PeriodOption;
}

export const PriceChart: React.FC<PriceChartProps> = ({ data, period }) => {
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
            yAxisId="price"
            orientation="right"
            domain={['auto', 'auto']}
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            yAxisId="indicator"
            orientation="left"
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: 'white', border: '1px solid #ccc' }}
          />
          <Legend />
          <Line
            yAxisId="price"
            type="monotone"
            dataKey="close"
            stroke="#2563eb"
            dot={false}
            name="Price"
          />
          <Line
            yAxisId="price"
            type="monotone"
            dataKey={`sma_${period}`}
            stroke="#16a34a"
            dot={false}
            name="SMA"
          />
          <Line
            yAxisId="price"
            type="monotone"
            dataKey={`ema_${period}`}
            stroke="#9333ea"
            dot={false}
            name="EMA"
          />
          <Line
            yAxisId="indicator"
            type="monotone"
            dataKey={`rsi_${period}`}
            stroke="#dc2626"
            dot={false}
            name="RSI"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
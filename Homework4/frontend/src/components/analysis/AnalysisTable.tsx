import { AnalysisData, PeriodOption } from '../../types/analysis';

interface AnalysisTableProps {
  data: AnalysisData[];
  period: PeriodOption;
}

export const AnalysisTable: React.FC<AnalysisTableProps> = ({ data, period }) => {
  if (!data || data.length === 0) return null;

  const getSignalColor = (signal?: string) => {
    switch (signal?.toUpperCase()) {
      case 'BUY':
        return 'text-green-600';
      case 'SELL':
        return 'text-red-600';
      default:
        return 'text-yellow-600';
    }
  };

  return (
    <div className="overflow-x-auto mt-4">
      <table className="min-w-full bg-white rounded-lg shadow">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-3 text-left">Date</th>
            <th className="p-3 text-left">Close</th>
            <th className="p-3 text-left">RSI</th>
            <th className="p-3 text-left">Stoch K</th>
            <th className="p-3 text-left">Stoch D</th>
            <th className="p-3 text-left">MFI</th>
            <th className="p-3 text-left">Signal</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx} className="border-t hover:bg-gray-50">
              <td className="p-3">{row.date}</td>
              <td className="p-3">{row.close?.toFixed(2)}</td>
              <td className="p-3">{row[`rsi_${period}`]?.toFixed(2)}</td>
              <td className="p-3">{row[`stoch_k_${period}`]?.toFixed(2)}</td>
              <td className="p-3">{row[`stoch_d_${period}`]?.toFixed(2)}</td>
              <td className="p-3">{row[`mfi_${period}`]?.toFixed(2)}</td>
              <td className={`p-3 font-semibold ${getSignalColor(row[`signal_${period}`])}`}>
                {row[`signal_${period}`]}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

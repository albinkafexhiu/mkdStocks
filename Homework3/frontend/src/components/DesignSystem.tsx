import { FC } from 'react';

export const DesignSystem: FC = () => {
  return (
    <div className="p-8 space-y-8">
      {/* Typography */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Typography</h2>
        <div className="space-y-2">
          <h1 className="text-3xl font-display font-bold">Heading 1 (3xl)</h1>
          <h2 className="text-2xl font-display font-bold">Heading 2 (2xl)</h2>
          <h3 className="text-xl font-display font-bold">Heading 3 (xl)</h3>
          <p className="text-base">Base text (base)</p>
          <p className="text-sm">Small text (sm)</p>
          <p className="font-mono">Monospace text</p>
        </div>
      </section>

      {/* Colors */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Colors</h2>
        <div className="grid grid-cols-5 gap-4">
          {/* Primary colors */}
          {[50, 100, 200, 300, 400, 500, 600, 700, 800, 900].map((weight) => (
            <div key={weight} className="space-y-2">
              <div 
                className={`h-12 w-full rounded bg-primary-${weight}`}
              />
              <p className="text-sm">{weight}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Common Components */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Common Components</h2>
        
        {/* Buttons */}
        <div className="space-y-4">
          <div className="space-x-4">
            <button className="bg-primary-500 text-white px-4 py-2 rounded hover:bg-primary-600 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
              Primary Button
            </button>
            <button className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
              Secondary Button
            </button>
          </div>
        </div>

        {/* Input */}
        <div className="mt-4">
          <input
            type="text"
            placeholder="Input field"
            className="w-full max-w-md px-4 py-2 border border-gray-300 rounded focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
          />
        </div>
      </section>
    </div>
  );
};
export const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'MKD',
      minimumFractionDigits: 2
    }).format(value);
  };
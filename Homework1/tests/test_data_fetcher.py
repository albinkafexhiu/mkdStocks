import unittest
from src.filters.data_fetcher import DataFetcherFilter

class TestDataFetcherFilter(unittest.TestCase):
    def setUp(self):
        self.fetcher = DataFetcherFilter()

    def test_price_formatting(self):
        test_cases = [
            # Basic cases
            ('21600', '21,600.00'),
            ('21600.00', '21,600.00'),
            ('21,600', '21,600.00'),
            ('21,600.00', '21,600.00'),
            
            # Edge cases
            ('0', '0.00'),
            ('', '0.00'),
            ('0.00', '0.00'),
            
            # Decimal cases
            ('1234.56', '1,234.56'),
            ('1234.5', '1,234.50'),
            ('1234.567', '1,234.57'),  # Should round to 2 decimals
            
            # Large numbers
            ('1234567.89', '1,234,567.89'),
            ('1000000', '1,000,000.00'),
            
            # Percentage values
            ('10.5%', '10.50'),
            ('-5.2%', '-5.20'),
            
            # Invalid inputs
            ('invalid', '0.00'),
            ('N/A', '0.00'),
            (None, '0.00'),
        ]

        for input_value, expected in test_cases:
            with self.subTest(input_value=input_value):
                result = self.fetcher.format_price(input_value)
                self.assertEqual(
                    result, 
                    expected,
                    f"Price formatting failed for input '{input_value}'. "
                    f"Expected '{expected}' but got '{result}'"
                )

    def test_row_processing(self):
        # Create a mock row with test data
        class MockTag:
            def __init__(self, text):
                self.text = text
            
            def find_all(self, tag):
                return [
                    MockTag('12/31/2023'),  # date
                    MockTag('21,600'),      # last_trade_price
                    MockTag('21,800'),      # max_price
                    MockTag('21,400'),      # min_price
                    MockTag('21,600'),      # avg_price
                    MockTag('1.5%'),        # change_percentage
                    MockTag('100'),         # volume
                    MockTag('2,160,000'),   # turnover_best
                    MockTag('2,160,000')    # total_turnover
                ]

        mock_row = MockTag('')
        result = self.fetcher._process_rows([mock_row], 'TEST')

        self.assertEqual(len(result), 1, "Should process one row")
        processed_row = result[0]

        # Verify each field is formatted correctly
        self.assertEqual(processed_row['last_trade_price'], '21,600.00')
        self.assertEqual(processed_row['max_price'], '21,800.00')
        self.assertEqual(processed_row['min_price'], '21,400.00')
        self.assertEqual(processed_row['avg_price'], '21,600.00')
        self.assertEqual(processed_row['change_percentage'], '1.50')
        self.assertEqual(processed_row['volume'], '100.00')
        self.assertEqual(processed_row['turnover_best'], '2,160,000.00')
        self.assertEqual(processed_row['total_turnover'], '2,160,000.00')

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, mock_open
from test import (
    read_integer_between_numbers,
    read_nonempty_string,
    read_integer,
    winner_of_race,
    display_races,
    race_venues,
    runners_data,
    reading_race_results
)

class TestMainFunctions(unittest.TestCase):

    def test_read_integer_between_numbers_valid(self):
        with patch('builtins.input', side_effect=['5']):
            self.assertEqual(read_integer_between_numbers("Enter a number: ", 1, 10), 5)

    def test_read_integer_between_numbers_out_of_range(self):
        with patch('builtins.input', side_effect=['15', '5']):
            self.assertEqual(read_integer_between_numbers("Enter a number: ", 1, 10), 5)

    def test_read_nonempty_string_valid(self):
        with patch('builtins.input', side_effect=['Runner']):
            self.assertEqual(read_nonempty_string("Enter your name: "), "Runner")

    def test_read_integer_valid(self):
        with patch('builtins.input', side_effect=['7']):
            self.assertEqual(read_integer("Enter a number: "), 7)

    def test_read_integer_negative(self):
        with patch('builtins.input', side_effect=['-3', '7']):
            self.assertEqual(read_integer("Enter a number: "), 7)

    def test_winner_of_race(self):
        ids = ['R1', 'R2', 'R3']
        times = [320, 300, 310]
        self.assertEqual(winner_of_race(ids, times), ['R2', 'R3', 'R1'])

    @patch('builtins.open', new_callable=mock_open, read_data="Venue1\nVenue2\n")
    def test_race_venues(self, mock_file):
        self.assertEqual(race_venues(), ['Venue1', 'Venue2'])

    @patch('builtins.open', new_callable=mock_open, read_data="Runner1,R1\nRunner2,R2\n")
    def test_runners_data(self, mock_file):
        names, ids = runners_data()
        self.assertEqual(names, ['Runner1', 'Runner2'])
        self.assertEqual(ids, ['R1', 'R2'])

    @patch('builtins.open', new_callable=mock_open, read_data="R1,320\nR2,300\nR3,310\n")
    def test_reading_race_results(self, mock_file):
        ids, times = reading_race_results("Venue1")
        self.assertEqual(ids, ['R1', 'R2', 'R3'])
        self.assertEqual(times, [320, 300, 310])

if __name__ == '__main__':
    unittest.main()

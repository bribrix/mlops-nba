import unittest
import subprocess
import sys

class TestEndToEnd(unittest.TestCase):
    def test_application_run(self):
        # Run the main.py script
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True)
        
        # Check if the script runs without errors
        self.assertEqual(result.returncode, 0, "main.py should exit with code 0")

if __name__ == '__main__':
    unittest.main()

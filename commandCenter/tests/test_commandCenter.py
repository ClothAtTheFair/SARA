import unittest
from src.CommandCenter import CommandCenter

class TestCommandCenter(unittest.TestCase):

    def setup(self):
        return CommandCenter()

    def test_check_intent_happy(self):
        #Given an intent, check that it is supported by the command center
        intent = 'email_sendemail'
        commandObj = self.setup()
        result = commandObj.check_intent(intent)
        self.assertTrue(result)

    def test_check_intent_sad(self):
        #Given an intent that isn't supported, return False
        intent = 'world_domination'
        commandObj = self.setup()
        result = commandObj.check_intent(intent)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()

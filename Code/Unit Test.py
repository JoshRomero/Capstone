from mainGUI import validateTextInput
import unittest

class TestTextInput(unittest.TestCase):

    def test_TextInput(self):

        #Testing each item it is expecting
        item = validateTextInput("keys")
        self.assertEqual(item, "Keys")

        item = validateTextInput("wallet")
        self.assertEqual(item, "Wallet")

        item = validateTextInput("thermos")
        self.assertEqual(item, "Thermos")

        item = validateTextInput("phone")
        self.assertEqual(item, "Phone")

        item = validateTextInput("Keys")
        self.assertEqual(item, "Keys")

        item = validateTextInput("Wallet")
        self.assertEqual(item, "Wallet")

        item = validateTextInput("Thermos")
        self.assertEqual(item, "Thermos")

        item = validateTextInput("Phone")
        self.assertEqual(item, "Phone")

        item = validateTextInput("WaLlEt")
        self.assertEqual(item, "Wallet")

        #Showing that the test is actuallying doing something
        item = validateTextInput("wenbiuaweugawopi;hnfgoiaweuoghn")
        self.assertEqual(item, "Wallet")

        #Testing invalid items or inputs
        item = validateTextInput("wenbiuaweugawopi;hnfgoiaweuoghn")
        self.assertEqual(item, "Invalid input. Try again")  

        item = validateTextInput("")
        self.assertEqual(item, "Invalid input. Try again")

        item = validateTextInput("unbrella")
        self.assertEqual(item, "Invalid input. Try again")

        item = validateTextInput("wallet;")
        self.assertEqual(item, "Invalid input. Try again")             


if __name__ == '__main__':
    unittest.main()





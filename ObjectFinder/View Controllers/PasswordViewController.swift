//
//  PasswordViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/22/21.
//


import UIKit
import FirebaseAuth

class PasswordViewController: UIViewController {

    
    @IBOutlet weak var oldPassTextField: UITextField!
    
    @IBOutlet weak var newPassTextField: UITextField!
    
    @IBOutlet weak var confirmPassTextField: UITextField!
    
    @IBOutlet weak var submitButton: UIButton!
    
    @IBOutlet weak var successLabel: UILabel!
    
    @IBOutlet weak var errorLabel: UILabel!
    
  
    @IBOutlet weak var emailAddresslabel: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setUpElements()
        
        let currentUser = Auth.auth().currentUser
        
        self.emailAddresslabel.text = currentUser!.email!
        
    }
    
    // sets up extra stuff after the page has been loaded
    func setUpElements() {
        Utilities.styleFilledButton(submitButton)
        Utilities.styleTextField(oldPassTextField)
        successLabel.alpha = 0
        errorLabel.alpha = 0
    }
    
    // handles the return to the previous page if back button is pressed
    @IBAction func backPressed(_ sender: Any) {
        self.dismiss(animated: false, completion: nil)
    }
    
    // handles the sending an email to the user which will allow them to reset the password
    @IBAction func submitPressed(_ sender: Any) {
        let email = emailAddresslabel.text
        
        let password = oldPassTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
    
        // Signing in the user
        Auth.auth().signIn(withEmail: email!, password: password) { (result, error) in
    
            if error != nil {
                // Couldn't sign in
                self.errorLabel.text = error!.localizedDescription
                self.errorLabel.alpha = 1
            }
            else {
                self.resetPassword(email: email!)
            }
        }
        
    }
    
    // shows any errors messages they users run into
    func showError(_ message: String) {
            errorLabel.text = message
            successLabel.alpha = 0
            errorLabel.alpha = 1
    }
    
    // shows any success messages if the email was sent to the user with no issues
    func showsuccess(_ message: String) {
        self.successLabel.text = message
        self.successLabel.alpha = 1
        self.errorLabel.alpha = 0
    }
    
    // resets the password for the user
    func resetPassword(email: String)
    {
        Auth.auth().sendPasswordReset(withEmail: email){ (error) in
            if error == nil
            {
                print("success")
                self.showsuccess("We have just sent you a password reset email. Please check your inbox and follow the instructions to reset your password.")
            }
            else
            {
                print("something went wrong")
                self.showError("Something went wrong, Please try again later.")
            }
        }
    }
    
}

//
//  ForgotPasswordViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/25/21.
//

import UIKit
import FirebaseAuth

class ForgotPasswordViewController : UIViewController {

    @IBOutlet weak var emailAddresslabel: UITextField!
    
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var successLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()
        setUpElements()

    }
    
    
    func setUpElements() {
        Utilities.styleTextField(emailAddresslabel)
        successLabel.alpha = 0
        errorLabel.alpha = 0
    }
    
    // handles the function of reseting the password on the login page
    // the user provides the email address and if it is a good email address the user will get a reset password
    // email. else they will get nothing
    @IBAction func resetPasswordPressed(_ sender: Any) {
        errorLabel.alpha = 0
        // keyboard dismiss
        self.view.endEditing(true)
        let email = emailAddresslabel.text
        // the user must enter something
        if email == ""{
            showError("Please enter a valid email address.")
        }
        else{
            self.resetPassword(email: email!)
        }
    }
    
    // handles the reseting password function
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
    
    // shows the user all the error messages
    func showError(_ message: String) {
            errorLabel.text = message
            successLabel.alpha = 0
            errorLabel.alpha = 1
    }
    
    // shows the user the success message if the email was sent correctly
    func showsuccess(_ message: String) {
        self.successLabel.text = message
        self.successLabel.alpha = 1
        self.errorLabel.alpha = 0
    }
}

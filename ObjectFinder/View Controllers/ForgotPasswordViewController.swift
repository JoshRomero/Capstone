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
    
    @IBAction func resetPasswordPressed(_ sender: Any) {
        let email = emailAddresslabel.text
        if email == ""{
            showError("Please enter a valid email address.")
        }
        else{
            self.resetPassword(email: email!)
        }
    }
    
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
    
    func showError(_ message: String) {
            errorLabel.text = message
            successLabel.alpha = 0
            errorLabel.alpha = 1
    }
    
    func showsuccess(_ message: String) {
        self.successLabel.text = message
        self.successLabel.alpha = 1
        self.errorLabel.alpha = 0
    }
}

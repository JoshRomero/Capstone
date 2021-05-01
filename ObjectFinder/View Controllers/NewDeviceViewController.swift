//
//  NewDeviceViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/27/21.
//

import UIKit
import FirebaseAuth

class NewDeviceViewController: UIViewController {

    
    @IBOutlet weak var emailAddress: UILabel!
    
    @IBOutlet weak var password: UITextField!
    
    @IBOutlet weak var submitbutton: UIButton!
    
    @IBOutlet weak var errorlabel: UILabel!
    
    @IBOutlet weak var successLabel: UILabel!
    
    @IBOutlet weak var newDeviceName: UITextField!
    override func viewDidLoad() {
        super.viewDidLoad()
        setUpElements()
        let currentUser = Auth.auth().currentUser
        
        self.emailAddress.text = currentUser!.email!
        self.errorlabel.alpha = 0
        self.successLabel.alpha = 0
    }

    // sets up extra stuff after the page has been loaded
    func setUpElements() {
        Utilities.styleFilledButton(submitbutton)
    }
    
    
    
    @IBAction func submitPressed(_ sender: Any) {
        // keyboard dismiss
        self.view.endEditing(true)
        self.errorlabel.alpha = 0
        
        if newDeviceName.text != ""
        {
            let email = emailAddress.text!
            
            let password1 = password.text!.trimmingCharacters(in: .whitespacesAndNewlines)
        
            // Signing in the user
            Auth.auth().signIn(withEmail: email, password: password1) { (result, error) in
        
                if error != nil {
                    // Couldn't sign in
                    self.errorlabel.text = error!.localizedDescription
                    self.errorlabel.alpha = 1
                }
                else {
                    // a message needs to be sent to the Pi
                    
                    let url1 = URL(string: "http://138.47.138.44:5000/register")!
                    let session = URLSession.shared
                    var request = URLRequest(url: url1)
                    request.httpMethod = "POST"
                    
                    
                    let json: [String: Any] = ["email": email, "password": password1, "roomID": self.newDeviceName.text!]
                    let jsonData = try? JSONSerialization.data(withJSONObject: json)
                    request.httpBody = jsonData
                    
                    
                    _ = session.synchronousDataTask(urlrequest: request)
                    
                    
                    
                    // need to make a static ip address for the first time pi start up.
                    self.showsuccess("\(self.newDeviceName.text!) has succuessfully been added. Please return to the Devices page and refresh the page.")
                }
            }
        }else{
            showError("Please enter a name for the new device.")
        }
    }
    
    func showError(_ message: String) {
        self.errorlabel.text = message
        self.successLabel.alpha = 0
        self.errorlabel.alpha = 1
    }
    
    // shows the user the success message if the email was sent correctly
    func showsuccess(_ message: String) {
        self.successLabel.text = message
        self.successLabel.alpha = 1
        self.errorlabel.alpha = 0
    }
}

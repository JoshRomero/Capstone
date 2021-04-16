//
//  SignUpViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
import FirebaseAuth
import Firebase
//import WatchConnectivity

class SignUpViewController: UIViewController {
//    var got_message = false
//    var message = ""
//    var session: WCSession?
    
    @IBOutlet weak var firstNameTextField: UITextField!
    
    @IBOutlet weak var lastNameTextField: UITextField!
    
    @IBOutlet weak var emailTextField: UITextField!
    
    @IBOutlet weak var passwordTextField: UITextField!
    
    @IBOutlet weak var signUpButton: UIButton!
    
    @IBOutlet weak var errorLabel: UILabel!

//    func createWCSession()
//    {
//        if WCSession.isSupported()
//        {
//            session = WCSession.default
//            session?.delegate = self
//            session?.activate()
//        }
//    }
//
//    func listening()
//    {
//        DispatchQueue.global(qos: .userInitiated).async {
//            while true
//            {
//                if self.got_message
//                {
//                    if let validSession = self.session, validSession.isReachable {
//                    validSession.sendMessage(["iPhone": "false"], replyHandler: nil, errorHandler: nil)
//                      }
//                    self.got_message = false
//
//                }
//            }
//        }
//
//    }
    override func viewDidLoad() {
        super.viewDidLoad()
        setUpElements()
//        createWCSession()
//        listening()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        navigationController?.setNavigationBarHidden(true, animated: animated)
    }
    
    func setUpElements() {
        
        // Hide the error label
        errorLabel.alpha = 0
        
        Utilities.styleTextField(firstNameTextField)
        Utilities.styleTextField(lastNameTextField)
        Utilities.styleTextField(emailTextField)
        Utilities.styleTextField(passwordTextField)
        Utilities.styleFilledButton(signUpButton)
    }
    
    // Check the fields and validate that the data is correct. If everything
    // is correct, this method returns nil. Otherwise, returns error.
    func validateFields() -> String? {
        
        // Check that all fields are filled in
        if (firstNameTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines) == "" || lastNameTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines) == "" || emailTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines) == "" || passwordTextField.text?.trimmingCharacters(in: .whitespacesAndNewlines) == "")
        {
            return "Please fill in all fields."
        }
         
        // Check if password is secure
        let cleanedPassword = passwordTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
        
        if Utilities.isPasswordValid(cleanedPassword) == false {
            return "Please make sure your password is at least 8 characters, contains a special character and a number."
        }
        
        return nil
    }
    
    
    @IBAction func signUpTapped(_ sender: Any) {
        
        // Validate the fields
        let error = validateFields()
        
        if error != nil {
            
            // There's something wrong with the fields, show error message
            showError(error!)
        }
        
        else {
            
            // Create cleaned versions of the data
            let firstName = firstNameTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            let lastName = lastNameTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            let email = emailTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            let password = passwordTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            
            // Create the user
            Auth.auth().createUser(withEmail: email, password:
                password) { (result, err) in
                
                // Check for errors
                if err != nil {
                    
                    // There was an error creating the user
                    self.showError("Error creating user.")
                }
                else {
                    
                    // User was created successfully, now store the first and last
                    let db = Firestore.firestore()

                    db.collection("users").addDocument(data: ["firstname":firstName, "lastname":lastName, "uid": result!.user.uid ]) { (error) in
                        print(result!.user.uid)
                        if error != nil {
                            // Show error message
                            self.showError("Error saving user data")
                        }
                    }
                    
                    // prepare json data
//                    let json: [String: Any] = ["email": email, "password": password]
//
//                    let jsonData = try? JSONSerialization.data(withJSONObject: json)
//
//                    // create post request
//                    let url = URL(string: "https://objectfinder.tech/signup")!
//                    var request = URLRequest(url: url)
//                    request.httpMethod = "POST"
//
//                    // insert json data to the request
//                    request.httpBody = jsonData
//
//                    let task = URLSession.shared.dataTask(with: request) { data, response, error in
//                        guard let data = data, error == nil else {
//                            print(error?.localizedDescription ?? "No data")
//                            return
//                        }
//                        let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
//                        if let responseJSON = responseJSON as? [String: Any] {
//                            print(responseJSON)
//                        }
//                    }
//
//                    task.resume()
                    
                    // Transition to the home screen
                    self.transitionToHome()
                }
            }
        }
    }
    
    func showError(_ message: String) {
        errorLabel.text = message
        errorLabel.alpha = 1
    }
    
    func transitionToHome() {
        
        let homeViewController = storyboard?.instantiateViewController(identifier: Constants.Storyboard.homeViewController) as? HomeViewController
        
        view.window?.rootViewController = homeViewController
        view.window?.makeKeyAndVisible()
    }
}
//extension SignUpViewController: WCSessionDelegate {
//    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
// }
//    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
//         if let value = message["watch"] as? String {
//            self.message = value
//         }
//        self.got_message = true
//        
//        print("Iphone got message from watch:",self.message)
//       }
//    func sessionDidBecomeInactive(_ session: WCSession) {
// }
//    func sessionDidDeactivate(_ session: WCSession) {
// }
//}

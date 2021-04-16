//
//  LoginViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
import FirebaseAuth
//import WatchConnectivity

class LoginViewController: UIViewController {
//    var got_message = false
//    var message = ""
//    var session: WCSession?
    
    @IBOutlet weak var emailTextField: UITextField!
    
    @IBOutlet weak var passwordTextField: UITextField!
    
    @IBOutlet weak var loginButton: UIButton!
        
    @IBOutlet weak var errorLabel: UILabel!
    
    public var DEBUG = true
    
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
        
        // Do any additional setup after loading the view.
        // self.textField.delegate = self
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
        
        // Style the elements
        Utilities.styleTextField(emailTextField)
        Utilities.styleTextField(passwordTextField)
        Utilities.styleFilledButton(loginButton)
    }
    
    @IBAction func loginTapped(_ sender: Any) {
        
        // TODO: Validate Text Fields
            
                // Create cleaned versions of the text field
                let email = emailTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
                let password = passwordTextField.text!.trimmingCharacters(in: .whitespacesAndNewlines)
            
                // Signing in the user
                Auth.auth().signIn(withEmail: email, password: password) { (result, error) in
            
                    if error != nil {
                        // Couldn't sign in
                        self.errorLabel.text = error!.localizedDescription
                        self.errorLabel.alpha = 1
                    }
                    else {
                        self.transitionToHome()
                    }
                }
    }
    
    func transitionToHome() {
        let homeViewController = self.storyboard?.instantiateViewController(identifier: Constants.Storyboard.homeViewController) as? HomeViewController

        self.view.window?.rootViewController = homeViewController
        self.view.window?.makeKeyAndVisible()
    }
}

//extension LoginViewController: WCSessionDelegate {
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

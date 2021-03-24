//
//  HomeViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
import FirebaseAuth
// import SideMenu
import SocketIO

class HomeViewController:
    UIViewController {
    
    @IBOutlet weak var objectToLocate: UITextField!
    
    @IBOutlet weak var locateButton: UIButton!
    
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var objectLabel: UILabel!
    
//    static let manager = SocketManager(socketURL: URL(string: "http://18.188.84.183:12001")!, config: [.log(true), .compress])
//    static let socket = manager.defaultSocket

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        setUpElements()
        
//        HomeViewController.socket.connect()
//
//        HomeViewController.socket.on(clientEvent: .connect) {data, ack in
//            print("socket connected")
//        }
//
//        HomeViewController.socket.on(clientEvent: .error) {data, ack in
//            print("socket error")
//        }
    }
    
    func setUpElements() {
        
        // Hide the object and error messages (for now)
        objectLabel.alpha = 0
        errorLabel.alpha = 0
        
        // Style the text field and button
        Utilities.styleTextField(objectToLocate)
        Utilities.styleFilledButton(locateButton)
    }
    
    func validateFields() -> String? {
        
        // Check that all fields are filled in
        if (objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "keys" || objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "cup" || objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "glasses" || objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "remote")
        {
            return nil
        }
        
        return "Invalid object"
    }
    
    @IBAction func locateTapped(_ sender: Any) {
        
        // Validate the fields
        let error = validateFields()
        
        if error != nil {
            
            // There's something wrong with the field, show error message
            showError(error!)
        }
        
        else {
            
            // Create cleaned versions of the object
            let object = objectToLocate.text!.lowercased().capitalizingFirstLetter().trimmingCharacters(in: .whitespacesAndNewlines)
                    
            // Show object message
            self.showObject("You're looking for: \(object)")
//            HomeViewController.socket.emit("object", object)
//            SocketIOManager.sharedInstance.emit(message: "message": "This is a test message")
//            SocketIOManager.sharedInstance.emit(object: "object": "testing")
        }
    }
    
    // display the error message
    func showError(_ message: String) {
            errorLabel.text = message
            objectLabel.alpha = 0
            errorLabel.alpha = 1
        }
    
    // display which object the user is looking for
    func showObject(_ message: String) {
            objectLabel.text = message
            objectLabel.alpha = 1
            errorLabel.alpha = 0
        }
    
    @IBAction func signOutTapped(_ sender: Any) {
        
        let firebaseAuth = Auth.auth()
        do {
          try firebaseAuth.signOut()
            self.transitionToRoot()
        } catch let signOutError as NSError {
          print ("Error signing out: %@", signOutError)
        }
    }
    
    func transitionToRoot() {
        
        let viewController = storyboard?.instantiateViewController(identifier: Constants.Storyboard.viewController) as? ViewController
        
        view.window?.rootViewController = viewController
        view.window?.makeKeyAndVisible()
            
    }
    
}

// extension to capitalize the first letter of the object
extension String {
    func capitalizingFirstLetter() -> String {
        return prefix(1).capitalized + dropFirst()
    }

    mutating func capitalizeFirstLetter() {
        self = self.capitalizingFirstLetter()
    }
}

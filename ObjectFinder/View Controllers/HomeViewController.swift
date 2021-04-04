//
//  HomeViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
import FirebaseAuth
import SideMenu

class HomeViewController:
    UIViewController, MenuControllerDelegate {
    
    @IBOutlet weak var objectToLocate: UITextField!
    
    @IBOutlet weak var locateButton: UIButton!
    
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var objectLabel: UILabel!
    
    private var sideMenu: SideMenuNavigationController?
    
    private let aboutController = AboutViewController()
    private let settingsController = SettingsViewController()

    override func viewDidLoad() {
        super.viewDidLoad()
        setUpElements()
        let menu = MenuController(with: SideMenuItem.allCases)
        menu.delegate = self
        sideMenu = SideMenuNavigationController(rootViewController: menu)
        sideMenu?.leftSide = true
        SideMenuManager.default.leftMenuNavigationController = sideMenu
        SideMenuManager.default.addPanGestureToPresent(toView: view)
        
        addChildControllers()
    }
    
    private func addChildControllers() {
        addChild(aboutController)
        addChild(settingsController)
        
        view.addSubview(aboutController.view)
        view.addSubview(settingsController.view)
        
        aboutController.view.frame = view.bounds
        settingsController.view.frame = view.bounds
        
        aboutController.didMove(toParent: self)
        settingsController.didMove(toParent: self)
        
        aboutController.view.isHidden = true
        settingsController.view.isHidden = true
    }
    
    @IBAction func didTapMenuButton(_ sender: Any) {
        present(sideMenu!, animated: true)
    }
    
    func didSelectMenuItem(named: SideMenuItem) {
        sideMenu?.dismiss(animated: true, completion: nil)
            
        title = named.rawValue
        
        switch named {
        case .home:
            aboutController.view.isHidden = true
            settingsController.view.isHidden = true
        case .settings:
            settingsController.view.isHidden = false
            aboutController.view.isHidden = true
        case .sign_out:
            let firebaseAuth = Auth.auth()
            do {
                try firebaseAuth.signOut()
                transitionToRoot()
            } catch let signOutError as NSError {
                showError("Error signing out: \(signOutError)")
            }
        case .about:
            settingsController.view.isHidden = true
            aboutController.view.isHidden = false
        }
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
        if (objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "keys" || objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "glasses" || objectToLocate.text?.lowercased().trimmingCharacters(in: .whitespacesAndNewlines) == "remote")
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
            errorLabel.alpha = 0
            let object = objectToLocate.text!.lowercased().capitalizingFirstLetter().trimmingCharacters(in: .whitespacesAndNewlines)
            
            let url1 = URL(string: "https://objectfinder.tech/pidata?userID=testID&objectQueried=\(object)")!
            let request = URLRequest(url: url1)
//            request.httpBody = body
//            request.httpMethod = "PUT"
            let (cleaned, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
            if let error = error {
                print("Synchronous task ended with error: \(error)")
                self.showError("No internet connection.")
            }
            else {
                print("Synchronous task ended without errors.")
                let item = cleaned[15].dropLast()
                let room = cleaned[11].dropLast()
                let dateTime = cleaned[7].dropLast()
                if (item == "keys" || item == "glasses") {
                    self.showObject("Your \(item) were found in room \(room) at \(dateTime).")
                }
                else {
                    self.showObject("Your \(item) was found in room \(room) at \(dateTime).")
                }
            }
            
            // Show object message
//            self.showObject("Item: \(item)")
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
        self.objectLabel.text = message
        self.objectLabel.alpha = 1
        self.errorLabel.alpha = 0
    }
    
    func transitionToRoot() {
        
        let rootViewController = storyboard?.instantiateViewController(identifier: Constants.Storyboard.rootViewController) as? ViewController
        
        view.window?.rootViewController = rootViewController
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

extension URLSession {
    func synchronousDataTask(urlrequest: URLRequest) -> (cleaned: [String], response: URLResponse?, error: Error?) {
        var data: Data?
        var response: URLResponse?
        var error: Error?

        let semaphore = DispatchSemaphore(value: 0)
        
        let dataTask = self.dataTask(with: urlrequest) {
            data = $0
            response = $1
            error = $2

            semaphore.signal()
        }
        dataTask.resume()
        
        _ = semaphore.wait(timeout: .distantFuture)
        
        let unformatted = String(data: data!, encoding: .utf8)!
        let cleaned = unformatted.split{$0 == "\""}.map(String.init)
        return (cleaned, response, error)
    }
}

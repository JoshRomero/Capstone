//
//  HomeViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
import FirebaseAuth
import SideMenu
import WatchConnectivity

class HomeViewController:
    UIViewController, MenuControllerDelegate, WCSessionDelegate, UITextFieldDelegate {
    
    // Needed for the communication between the watch and IOS app
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
 }
    // If we get a message from the watch, check the request and return the appropriate response
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        
         if let value = message["watch"] as? String {
            self.message = value
         }
        
        print("Iphone got message from watch:",self.message)
        self.got_message = true
        if self.got_message {
            
            // if the watch is asking if the IOS app is logged in, if so return true else false
            if self.message == "logged in?" {
                let return_message = self.BoolToString(b: self.logged_in)
                print("sent message to watch:", return_message)
                if let validSession = self.session, validSession.isReachable {
                validSession.sendMessage(["iPhone": return_message], replyHandler: nil, errorHandler: nil)
                }
            }
            
            else {
                
                // Any other message is assumed to be a request for the DB so it search the DB if logged in and returns the results
                                
                let currentUser = Auth.auth().currentUser
                print(currentUser!.email!)
                currentUser?.getIDTokenForcingRefresh(true) { idToken, error in
                  if let error = error {
                    // Handle error
                    print("error:", error)
                    return;
                  }

                    // Send token to backend via HTTPS
                    var object = self.message.lowercased().capitalizingFirstLetter().trimmingCharacters(in: .whitespacesAndNewlines)
                    
                    // Trim whitespace
                    object = object.filter { !$0.isWhitespace }
                    
                    let url1 = URL(string: "https://objectfinder.tech/pidata?object=\(object)")!
                    var request = URLRequest(url: url1)
                    request.setValue(idToken, forHTTPHeaderField: "Authorization")
                    request.httpMethod = "GET"
                    let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                    let unformatted = String(data: data!, encoding: .utf8)!
                    let cleaned = unformatted.split{$0 == "\""}.map(String.init)
                    
                    if let error = error {
                        print("Synchronous task ended with error: \(error)")
                        self.showError("No internet connection.")
                    }
                    
                    else {
                        print("Synchronous task ended without errors.")
                        var room = cleaned[7]
                        room = "Room \(room)"
                        if let validSession = self.session, validSession.isReachable {
                        validSession.sendMessage(["iPhone": room], replyHandler: nil, errorHandler: nil)
                        }
                    }
                }
            }
        }
        self.got_message = false
        
       }
    
    func sessionDidBecomeInactive(_ session: WCSession) {
 }
    func sessionDidDeactivate(_ session: WCSession) {
 }
    
    
    var got_message = false
    var message = ""
    var session: WCSession?
    var logged_in = true
    let valid_item = ["Cellphone" , "Remote", "Laptop", "Handbag"]
    
    @IBOutlet weak var objectToLocate: UITextField!
    
    @IBOutlet weak var locateButton: UIButton!
    
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var objectLabel: UILabel!
    
    @IBOutlet weak var showImageButton: UIButton!
    
    var dateTime = ""
    
    @IBOutlet weak var DBimage: UIImageView!
    
    private var sideMenu: SideMenuNavigationController?
    
    private let settingsController = SettingsViewController()
    private let aboutController = AboutViewController()

    func createWCSession()
    {
        if WCSession.isSupported()
        {
            session = WCSession.default
            session?.delegate = self
            session?.activate()
        }
    }
    
    // used to change bools to strings
    func BoolToString(b: Bool?)->String { return b?.description ?? "<None>"}
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.objectToLocate.delegate = self
        setUpElements()
        
        createWCSession()
        addChildControllers()
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        navigationController?.setNavigationBarHidden(false, animated: animated)
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
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
    
    // handles showing the user the side menu if the button is pressed
    @IBAction func didTapMenuButton(_ sender: Any) {
        let menu = MenuController(with: SideMenuItem.allCases)
        menu.delegate = self
        sideMenu = SideMenuNavigationController(rootViewController: menu)
        sideMenu?.leftSide = true
        SideMenuManager.default.leftMenuNavigationController = sideMenu
        present(sideMenu!, animated: true)
    }
    
    // handles if the user selects something from the side menu
    func didSelectMenuItem(named: SideMenuItem) {
        sideMenu?.dismiss(animated: true, completion: nil)
            
        title = named.rawValue
        
        switch named {
        case .settings:
            transitionToSettings()
            print("Settings")
        case .sign_out:
            logged_in = false
            let firebaseAuth = Auth.auth()
            do {
                try firebaseAuth.signOut()
                transitionToRoot()
            } catch let signOutError as NSError {
                showError("Error signing out: \(signOutError)")
            }
        case .about:
            transitionToAbout()
            print("About")
        }
    }
    
    func setUpElements() {
        
        // Hide the object and error messages (for now)
        objectLabel.alpha = 0
        errorLabel.alpha = 0
        showImageButton.alpha = 0
        
        
        // Style the text field and button
        Utilities.styleTextField(objectToLocate)
        Utilities.styleFilledButton(locateButton)
        Utilities.styleFilledButton(showImageButton)
    }
    
    
    // handles showing the images to the user of the requested item
    @IBAction func showImagePressed(_ sender: Any) {
        self.transitionToImage(object: self.dateTime)
    }
    

    
    // when the user is searching for an item, handles the request to the DB for the IOS app only not watch
    @IBAction func locateTapped(_ sender: Any) {
        // keyboard dismiss
        self.view.endEditing(true)
        
        // make errorLabel go away
        errorLabel.alpha = 0
        // get the object that we are looking for and formate it correctly
        var object = objectToLocate.text!.lowercased().capitalizingFirstLetter().trimmingCharacters(in: .whitespacesAndNewlines)
        // remove all whitespace
        object = object.filter { !$0.isWhitespace }
        // check if the object is a valid searchable object
        if self.valid_item.contains(object)
        {
            // authenticate the user
            let currentUser = Auth.auth().currentUser
            
            currentUser?.getIDTokenForcingRefresh(true) { idToken, error in
              if let error = error {
                // Handle error
                print("error:", error)
                return;
              }

              // Send token to your backend via HTTPS
              // ...
                        
                let url1 = URL(string: "https://objectfinder.tech/pidata?object=\(object)")!
                var request = URLRequest(url: url1)
                request.setValue(idToken, forHTTPHeaderField: "Authorization")
                request.httpMethod = "GET"
                let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                let unformatted = String(data: data!, encoding: .utf8)!
                if unformatted != "{\"message\": \"The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.\"}\n"
                {
                    let cleaned = unformatted.split{$0 == "\""}.map(String.init)
                    if let error = error {
                        print("Synchronous task ended with error: \(error)")
                        self.showError("No internet connection.")
                    }
                    else {
                        print("Synchronous task ended without errors.")
                        let item = cleaned[11]
                        let room = cleaned[7]
                        let dateTime1 = cleaned[3]
                        self.dateTime = dateTime1
                        
                        if (item.last! == "s") {
        //                  Show object message
                            self.showObject("Your \(item) were found in room \(room) at \(dateTime1).")
                        }
                        else {
        //                  Show object message
                            self.showObject("Your \(item) was found in room \(room) at \(dateTime1).")
                        }
                    }
                }
                else{
                    self.showError("Sorry, could not find \(object).")
                }
            }
        }
            else{
                self.showError("Sorry, \(object) is not an item I can find. List of searchable items can be find on the ABOUT page.")
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
        self.showImageButton.alpha = 1
        self.objectLabel.alpha = 1
        self.errorLabel.alpha = 0
    }
    
    // displays the image of the requested object
    func transitionToImage(object:String) {
        let story = UIStoryboard(name: "Main", bundle: nil)
        let controller = story.instantiateViewController(identifier: "ImageViewController") as! ImageViewController
        controller.dateTime = dateTime
        self.present(controller, animated: true, completion: nil)
    }
    
    // displays the about page if selected in the side menu
    func transitionToAbout() {
        let story = UIStoryboard(name: "Main", bundle: nil)
        let controller = story.instantiateViewController(identifier: "AboutViewController") as! AboutViewController
        self.present(controller, animated: true, completion: nil)
    }
    
    
    
    // displays the setting page if selected in the side menu
    func transitionToSettings() {
        let story = UIStoryboard(name: "Main", bundle: nil)
        let controller = story.instantiateViewController(identifier: "SettingsViewController") as! SettingsViewController
        self.present(controller, animated: true, completion: nil)
    }
   
    // displays the login/signup page if selected in the side menu
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
    func synchronousDataTask(urlrequest: URLRequest) -> (Data?, response: URLResponse?, error: Error?) {
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
        
        return (data, response, error)
    }
}

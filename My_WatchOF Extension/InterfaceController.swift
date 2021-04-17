//
//  InterfaceController.swift
//  ObjectFinderWatchOSApp WatchKit Extension
//
//  Created by William Francis on 4/6/21.
//

import WatchKit
import Foundation
import WatchConnectivity


var loggedin = false
var returned = false
var searching_for = ""
var timed_out = false

class InterfaceController: WKInterfaceController {
    
    let session = WCSession.default
    
    @IBOutlet var SearchButton: WKInterfaceButton!
    
    @IBOutlet var StartButton: WKInterfaceButton!
    
    @IBOutlet var TextLabel: WKInterfaceLabel!
    
    @IBOutlet var TextLabel2: WKInterfaceLabel!
    
    @IBOutlet private var loadingLabel: WKInterfaceLabel!
    
    
    override func awake(withContext context: Any?) {
        super.awake(withContext: context)
        // Configure interface objects here.
        session.delegate = self
        session.activate()
    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
        super.willActivate()
    }
    
    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
        super.didDeactivate()
    }
    
    @IBAction func TryAgainButtonPressed() {
        self.pushController(withName: "Start Screen", context: nil)
    }
    
    
    func send_message(data1: String) -> Void
    {
        DispatchQueue.global(qos: .userInitiated).async {
            let data: [String: Any] = ["watch": data1 as Any] //Create your dictionary as per uses
            self.session.sendMessage(data, replyHandler: nil, errorHandler: nil) //**6.1
        }
    }
    
    func check_if_logged_in() -> Void{
        if !loggedin
        {
            returned = false
            var winner = 0
            // if the app does not respond within 5 seconds then if will for try again page (in the background)
            DispatchQueue.global(qos: .userInitiated).async {
                sleep(10)
                if winner == 0{
                    winner = 2
                }
            }
            print("watch sent message to phone")
            // communicate to the app to see if it is logged in (in the background)
            DispatchQueue.global(qos: .userInitiated).async {
                let data: [String: Any] = ["watch": "logged in?" as Any] //Create your dictionary as per uses
                self.session.sendMessage(data, replyHandler: nil, errorHandler: nil) //**6.1
                while returned == false
                {
                    if winner == 2{
                        break
                    }
                }
                
                //
                if winner == 0{
                    winner = 1
                }
            }
        // keep looping until you get the feedback from the app or it times out
        while true{
            if winner == 2{
                timed_out = true
                return
            }else if winner == 1{
                return
            }
        }
        }
    }
    
    @IBAction func StartButtonPressed() {
        
        // grab the information from the app and update the UI in the background
        DispatchQueue.global(qos: .userInitiated).async {
            // controlling the Loading... changes in the background
            DispatchQueue.global(qos: .userInitiated).async {
                var count = 0
                while true{
                    if count == 1{
                        // updating the UI
                        DispatchQueue.main.async {
                            self.StartButton.setTitle("Loading.")
                        }
                    }else if count == 2 {
                        // updating the UI
                        DispatchQueue.main.async {
                            self.StartButton.setTitle("Loading..")
                        }
                    }else if count == 3 {
                        // updating the UI
                        DispatchQueue.main.async {
                            self.StartButton.setTitle("Loading...")
                        }
                    }else{
                        // updating the UI
                        DispatchQueue.main.async {
                            self.StartButton.setTitle("Loading")
                        }
                    }
                    
                    count += 1
                    sleep(1)
                    if count == 4 && !loggedin{
                        count = 0
                    }
                    else if loggedin{
                        break
                    }
                }
            }
            
            // get data from app
            self.check_if_logged_in()
            // after getting the logged in results update the UI
            if loggedin{
                DispatchQueue.main.async {
                    self.pushController(withName: "Search Screen", context: nil)
                }
            }else{
                DispatchQueue.main.async {
                    self.pushController(withName: "Login", context: nil)
                }
            }
        
        }
    }
    
    
    
    @IBAction func HomeButtonPressed() {
        self.pushController(withName: "Start Screen", context: nil)
    }
    
        
    @IBAction func SearchButtonPressed() {
        
        // grab the information from the app and update the UI in the background
        DispatchQueue.global(qos: .userInitiated).async {
            DispatchQueue.global(qos: .userInitiated).async {
                var count = 0
                while true{
                    if count == 1{
                        // updating the UI
                        DispatchQueue.main.async {
                            self.SearchButton.setTitle("Loading.")
                        }
                    }else if count == 2 {
                        // updating the UI
                        DispatchQueue.main.async {
                            self.SearchButton.setTitle("Loading..")
                        }
                    }else if count == 3 {
                        // updating the UI
                        DispatchQueue.main.async {
                            self.SearchButton.setTitle("Loading...")
                        }
                    }else{
                        // updating the UI
                        DispatchQueue.main.async {
                            self.SearchButton.setTitle("Loading")
                        }
                    }
                    
                    count += 1
                    sleep(1)
                    if count == 4 && !loggedin{
                        count = 0
                    }
                    else if loggedin{
                        self.SearchButton.setTitle("Search Again")
                        break
                    }
                }
            }
            
            
            // get data from app
            self.check_if_logged_in()
            // after getting the logged in results update the UI
            if loggedin{
                let options = ["Keys", "Wallet"]
                self.presentTextInputController(withSuggestions: options, allowedInputMode: .plain, completion: { results in
                    guard let results = results else { return }
                    OperationQueue.main.addOperation {
                        self.dismissTextInputController()
                        let UserInput = (results[0] as? String)
                        let LowercaseInput = UserInput?.lowercased()
                        
                        if LowercaseInput!.contains("keys") {
                            self.send_message(data1: "Keys")
                            self.TextLabel.setText("Keys")
                            self.TextLabel2.setText("Searching for:")
                            
                        }
                        
                        else if LowercaseInput!.contains("wallets") {
                            self.send_message(data1: "Wallet")
                            self.TextLabel.setText("Wallet")
                            self.TextLabel2.setText("Searching for:")
                        }
                        
                        else {
                            self.TextLabel.setText("Error, Please Try Again")
                        }
                        
                    }
                    })
            }else{
                DispatchQueue.main.async {
                    self.pushController(withName: "Login", context: nil)
                }
            }
        }
    }
}

extension InterfaceController: WCSessionDelegate
{
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
    }
    
    
    func session(_ session: WCSession, didReceiveMessage message: [String : Any])
    {
        if let value = message["iPhone"] as? String
        {
            print("Got message from Phone:" , value)
            if !timed_out{
                if value == "true"
                {
                    loggedin = true
                    returned = true
                    DispatchQueue.global(qos: .userInitiated).async {
                        sleep(60)
                        loggedin = false
                    }
                    
                }
                else if value == "false"
                {
                    returned = true
                    loggedin = false
                }
                else{
                    returned = true
                    self.TextLabel.setText(value)
                    self.TextLabel2.setText("Found in:")
                }
                
            }else{
                timed_out = false
            }
            
        }
    }
}


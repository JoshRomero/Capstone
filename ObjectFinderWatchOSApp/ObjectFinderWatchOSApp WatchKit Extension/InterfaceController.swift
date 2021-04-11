//
//  InterfaceController.swift
//  ObjectFinderWatchOSApp WatchKit Extension
//
//  Created by William Francis on 4/6/21.
//

import WatchKit
import Foundation

var loggedin = false

class InterfaceController: WKInterfaceController {
    
    
    @IBOutlet var SearchButton: WKInterfaceButton!
    
    @IBOutlet var StartButton: WKInterfaceButton!
    
    @IBOutlet var TextLabel: WKInterfaceLabel!
    
    @IBOutlet var TextLabel2: WKInterfaceLabel!
    
    @IBOutlet private var loadingLabel: WKInterfaceLabel!
    
    
    override func awake(withContext context: Any?) {
        // Configure interface objects here.
    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
    }
    
    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
    }
    
    @IBAction func LoginButtonPressed() {
        self.pushController(withName: "Search Screen", context: nil)
    }
    
    
    func check_if_logged_in() -> Bool{
        var winner = 0
        
        // if the app does not respond within 5 seconds then if will for try again page (in the background)
        DispatchQueue.global(qos: .userInitiated).async {
            sleep(5)
            if winner == 0{
                winner = 2
            }
        }
        
        // communicate to the app to see if it is logged in (in the background)
        DispatchQueue.global(qos: .userInitiated).async {
            
            
            // TODO 
//            sleep(UInt32(Int.random(in: 1..<10)))
            sleep(4)
            // add the get data function that will grab the information from the app
//            loggedin = Bool.random()
            loggedin = true
            
            //
            if winner == 0{
                winner = 1
            }
        }
        
        // keep looping until you get the feedback from the app or it times out
        while true{
            if winner == 2{
                loggedin = false
                return false
            }else if winner == 1{
                // trash this after we get info from app
//                loggedin = true
                return true
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
            let returned = self.check_if_logged_in()
            // after getting the logged in results update the UI
            if returned && loggedin{
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
        loggedin = false
        self.pushController(withName: "Start Screen", context: nil)
    }
    
        
    @IBAction func SearchButtonPressed() {
        loggedin = false
        
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
                        sleep(1)
                        self.SearchButton.setTitle("Search Again")
                        break
                    }
                }
            }
            
            
            // get data from app
            let returned = self.check_if_logged_in()
            // after getting the logged in results update the UI
            if returned && loggedin{
                let options = ["Keys", "Wallet"]
                self.presentTextInputController(withSuggestions: options, allowedInputMode: .plain, completion: { results in
                    guard let results = results else { return }
                    OperationQueue.main.addOperation {
                        self.dismissTextInputController()
                        let UserInput = (results[0] as? String)
                        let LowercaseInput = UserInput?.lowercased()
                        
                        if LowercaseInput!.contains("key") {
                            self.TextLabel.setText("Keys")
                            self.TextLabel2.setText("Searching for:")
                            
                        }
                        
                        else if LowercaseInput!.contains("keys") {
                            self.TextLabel.setText("Keys")
                            self.TextLabel2.setText("Searching for:")
                        }
                        
                        else if LowercaseInput!.contains("wallet") {
                            self.TextLabel.setText("Wallet")
                            self.TextLabel2.setText("Searching for:")
                        }
                        
                        else if LowercaseInput!.contains("wallets") {
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


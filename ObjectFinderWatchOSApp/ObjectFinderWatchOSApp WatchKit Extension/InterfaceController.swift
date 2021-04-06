//
//  InterfaceController.swift
//  ObjectFinderWatchOSApp WatchKit Extension
//
//  Created by William Francis on 4/6/21.
//

import WatchKit
import Foundation

class InterfaceController: WKInterfaceController {

    @IBOutlet var StartButton: WKInterfaceButton!
    
    @IBOutlet var SearchButton: WKInterfaceButton!
    
    @IBOutlet var TextLabel: WKInterfaceLabel!
    
    @IBOutlet var TextLabel2: WKInterfaceLabel!
    
    override func awake(withContext context: Any?) {
        // Configure interface objects here.
    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
    }
    
    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
    }
    
    @IBAction func StartButtonPressed() {
        self.pushController(withName: "Search Screen", context: nil)
    }
    
    @IBAction func SearchButtonPressed() {
        SearchButton.setTitle("Search Again")
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
    }
}

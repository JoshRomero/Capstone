//
//  InterfaceController.swift
//  Communication Test WatchOS Extension
//
//  Created by William Francis on 4/13/21.
//

import WatchKit
import Foundation

import WatchConnectivity
class InterfaceController: WKInterfaceController, WCSessionDelegate {

    
    @IBOutlet weak var lblShowMsg: WKInterfaceLabel!
    var session = WCSession.default
    
    
    override func awake(withContext context: Any?) {
        session.delegate = self
        session.activate()
        // Configure interface objects here.
    }
    
    override func willActivate() {
        // This method is called when watch view controller is about to be visible to user
    }
    
    override func didDeactivate() {
        // This method is called when watch view controller is no longer visible
    }
    
    @IBAction func btnSendToPhone() {
        let dic : [String : Any] = ["watch" : "Hello iPhone" as Any]
        session.sendMessage(dic, replyHandler: nil, errorHandler: nil)
    }
    
    //MARK: session delegate
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        
    }
    
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        print("Message from iPhone : \(message)")
        DispatchQueue.main.async {
            if let value = message["iPhoneMsg"] as? String
            {
                self.lblShowMsg.setText(value)
            }
        }
    }
    
}

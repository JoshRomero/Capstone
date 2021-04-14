//
//  ViewController.swift
//  Communication Test
//
//  Created by William Francis on 4/13/21.
//

import UIKit
import WatchConnectivity
class ViewController: UIViewController,WCSessionDelegate {
    

    @IBOutlet weak var lblWatchMsg: UILabel!
    
    var session : WCSession?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if WCSession.isSupported() {
            session = WCSession.default
            session?.delegate = self
            session?.activate()
        }
        // Do any additional setup after loading the view.
    }

    @IBAction func brnConnectWatch(_ sender: Any) {
        if let validSession = self.session, validSession.isReachable {
            let dic : [String : Any] = ["iPhoneMsg" : "Hello Watch" as Any]
            validSession.sendMessage(dic, replyHandler: nil, errorHandler: nil)
        }
    }
    
    //MARK: - session delegate
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
        
    }
    
    func sessionDidBecomeInactive(_ session: WCSession) {
        
    }
    
    func sessionDidDeactivate(_ session: WCSession) {
        
    }
    
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        print("Message from Watch : \(message)")
        DispatchQueue.main.async {
            if let value = message["watch"] as? String
            {
                self.lblWatchMsg.text = value
            }
        }
    }
    
}



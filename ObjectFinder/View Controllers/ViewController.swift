//
//  ViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
<<<<<<< Updated upstream

class ViewController: UIViewController {
    
=======
import WatchConnectivity

class ViewController: UIViewController {
    
    var got_message = false
    var message = ""
    var session: WCSession?
    
>>>>>>> Stashed changes
    @IBOutlet weak var signUpButton: UIButton!
    
    @IBOutlet weak var loginButton: UIButton!
    
<<<<<<< Updated upstream
=======
    func createWCSession()
    {
        if WCSession.isSupported()
        {
            session = WCSession.default
            session?.delegate = self
            session?.activate()
        }
    }
    
    
    func listening()
    {
        DispatchQueue.global(qos: .userInitiated).async {
            while true
            {
                if self.got_message
                {
                    self.got_message = false
                    if let validSession = self.session, validSession.isReachable {
                    validSession.sendMessage(["iPhone": "true"], replyHandler: nil, errorHandler: nil)
                      }
                }
            }
        }
        
    }
    
>>>>>>> Stashed changes
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        setUpElements()
<<<<<<< Updated upstream
=======
        createWCSession()
        listening()
>>>>>>> Stashed changes
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // navigationController?.setNavigationBarHidden(true, animated: animated)
    }
    
    func setUpElements() {
        
        Utilities.styleFilledButton(signUpButton)
        Utilities.styleHollowButton(loginButton)
        
    }
<<<<<<< Updated upstream
=======
    
    @IBAction func test_tap(_ sender: Any) {
        
        if let validSession = self.session, validSession.isReachable {
        validSession.sendMessage(["iPhone": "true"], replyHandler: nil, errorHandler: nil)
          }
    }
    
    
}

extension ViewController: WCSessionDelegate {
    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {
 }
    func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
        self.got_message = true
         if let value = message["watch"] as? String {
            self.message = value
         }
        
        print("Iphone got message from watch:",self.message)
       }
    func sessionDidBecomeInactive(_ session: WCSession) {
 }
    func sessionDidDeactivate(_ session: WCSession) {
 }
>>>>>>> Stashed changes
}

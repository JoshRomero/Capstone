//
//  ViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 2/21/21.
//

import UIKit
//import WatchConnectivity

class ViewController: UIViewController {
    
//    var got_message = false
//    var message = ""
//    var session: WCSession?
    
    @IBOutlet weak var signUpButton: UIButton!
    
    @IBOutlet weak var loginButton: UIButton!
    
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
        setUpElements()
//        createWCSession()
//        listening()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // navigationController?.setNavigationBarHidden(true, animated: animated)
    }
    
    func setUpElements() {
        
        Utilities.styleFilledButton(signUpButton)
        Utilities.styleHollowButton(loginButton)
        
    }
    
        
    
}

//extension ViewController: WCSessionDelegate {
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

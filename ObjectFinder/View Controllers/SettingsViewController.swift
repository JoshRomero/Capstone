//
//  SettingsViewController.swift
//  ObjectFinder
//
//  Created by Branson Hanzo on 4/4/21.
//

import UIKit
import MessageUI

class SettingsViewController: UIViewController, MFMailComposeViewControllerDelegate {
    
    // helps with the support button (displays the users interaction)
    func mailComposeController(_ controller: MFMailComposeViewController, didFinishWith result: MFMailComposeResult, error: Error?) {
        if let _ = error {
            controller.dismiss(animated: true)
            return
        }
        switch result {
        case .cancelled:
            print("Cancelled")
        case .failed:
            print("Failed to send")
        case .saved:
            print("Saved")
        case .sent:
            print("Email Sent")
        }
        controller.dismiss(animated: true)
    }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
    }
    
    // handles the support button
    func showMailComposer()
    {
        guard MFMailComposeViewController.canSendMail() else {
            // show alert to inform the user they cant send mail from this device
            print("Device cant send an email mail")
            return
        }
        
        let composer = MFMailComposeViewController()
        composer.mailComposeDelegate = self
        // #########################################    need to add a good support email
        composer.setToRecipients(["supp0rt.objectfinder@gmail.com"])
        // #########################################    need to add a good support email
        composer.setSubject("HELP!")
        composer.setMessageBody("I need help, can you please assist me with: ", isHTML: false)
        present(composer, animated: true)
    }
    
    // if the support button is pressed call the above func
    @IBAction func supportPressed(_ sender: Any) {
        showMailComposer()
    }
    
    // handles the github button (send the user to the creaters github page)
    @IBAction func githubPressed(_ sender: Any) {
        
        UIApplication.shared.open(URL(string: "https://github.com/JoshRomero/Capstone")!as URL, options: [:], completionHandler: nil)
    }
    
    
    
}

//
//  DevicesStatusViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/26/21.
//

import UIKit

class DevicesStatusViewController: UIViewController, UITableViewDataSource, UITabBarDelegate, UITableViewDelegate {
    
    // handles the number of items in the table which should be 4 at all times
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return table_title.count
    }
    
    // adds all the information in the table for the user to see
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "DevicesStatusViewController", for: indexPath)
        cell.textLabel?.text = table_title[indexPath.row]
        let table_detail = [id_detail, status_detail, IP_detail, MAC_detail]
        cell.detailTextLabel?.text = table_detail[indexPath.row]
        return cell
    }
    @IBOutlet weak var tableview: UITableView!
    
    let table_title = ["ID", "Status", "IP Address", "MAC Address"]
    var id_detail = ""
    var status_detail = ""
    var IP_detail = ""
    var MAC_detail = ""
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableview.delegate = self
        tableview.dataSource = self
        tableview.alpha = 1
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    // handles the reaction to if the user presses the restart button, are you sure message and sending the POST
    // request to the Device to restart it
    @IBAction func restartPressed(_ sender: Any) {
        let refreshAlert = UIAlertController(title: "Restart", message: "Are you sure you would like to restart this device?", preferredStyle: UIAlertController.Style.alert)

        refreshAlert.addAction(UIAlertAction(title: "Confirm", style: .default, handler: { (action: UIAlertAction!) in
            // need to send a message to the pi that we want to restart (IP = IP_detail)
            print("Handle Ok logic here")
          }))

        refreshAlert.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: { (action: UIAlertAction!) in
            // this should be good we should not have to do anything here
            print("Handle Cancel Logic here")
          }))

        present(refreshAlert, animated: true, completion: nil)
    }
    
    // handles the reaction to if the user presses the reset button, are you sure message and sending the POST
    // request to the Device to reset it
    @IBAction func resetPressed(_ sender: Any) {
        let refreshAlert = UIAlertController(title: "Reset", message: "All data will be lost after reset.", preferredStyle: UIAlertController.Style.alert)

        refreshAlert.addAction(UIAlertAction(title: "Ok", style: .default, handler: { (action: UIAlertAction!) in
            // need to send a message to the pi that we want to restart (IP = IP_detail)
            print("Handle Ok logic here")
          }))

        refreshAlert.addAction(UIAlertAction(title: "Cancel", style: .cancel, handler: { (action: UIAlertAction!) in
            // this should be good we should not have to do anything here
            print("Handle Cancel Logic here")
          }))

        present(refreshAlert, animated: true, completion: nil)
    }
    
    
    
}

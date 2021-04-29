//
//  connectedDevicesViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/25/21.
//

import UIKit
import FirebaseAuth

class connectedDevicesViewController: UIViewController, UITableViewDataSource, UITabBarDelegate, UITableViewDelegate {
    // controls if the user selects an item to get more details about the devices
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        self.transitionToStatus(num: indexPath.row)
    }
    // returns the number of rows needed to display (set to the amount of devices connected)
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return devices.count
    }
    
    // adds the information to the table that displays the devices connected
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "connectedDevicesViewController", for: indexPath)
        cell.textLabel?.text = devices[indexPath.row]
        cell.detailTextLabel?.text = devices_status[indexPath.row]
        return cell
    }
    
    // if user wants to get more information on a device this will go to a new controller that will provide
    // details like (MAC, IP, Device ID, Devices Status)
    func transitionToStatus(num: Int) {
        let story = UIStoryboard(name: "Main", bundle: nil)
        let controller = story.instantiateViewController(identifier: "DevicesStatusViewController") as! DevicesStatusViewController
        controller.id_detail = devices[num]
        controller.status_detail = devices_status[num]
        controller.IP_detail = devices_IP[num]
        controller.MAC_detail = devices_MAC[num]
        self.present(controller, animated: true, completion: nil)
    }
    
    func transitionToAddNewDevice() {
        let story = UIStoryboard(name: "Main", bundle: nil)
        let controller = story.instantiateViewController(identifier: "NewDeviceViewController") as! NewDeviceViewController
        self.present(controller, animated: true, completion: nil)
    }
    
    
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var tableview: UITableView!
    
    @IBOutlet weak var addNewDeviceLabel: UIButton!
    
    // Get this data from devices
    var devices = ["Room 0", "Room 1"]
    var devices_status = ["inactive0", "inactive1"]
    var devices_IP = ["192.168.0.10", "192.168.0.11"]
    var devices_MAC = ["MAC0", "MAC1"]
    //
    
        
    let myRefreshControl = UIRefreshControl()
    
    // if the users swipes down on the table it will refresh the data from the above info after 3 seconds
    @objc func handleRefresh(_ sender: UIRefreshControl) {
            Timer.scheduledTimer(withTimeInterval: 3.0, repeats: false) { (timer) in
                self.get_device_status()
                self.tableview.reloadData()
                self.myRefreshControl.endRefreshing()
            }
        }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableview.delegate = self
        tableview.dataSource = self
        tableview.alpha = 1
        errorLabel.alpha = 0
        
        Utilities.styleFilledButton(addNewDeviceLabel)
        
        myRefreshControl.addTarget(self, action: #selector(connectedDevicesViewController.handleRefresh), for: .valueChanged)
        tableview.refreshControl = myRefreshControl
//        get_device_status()
        
    }
    
    
    // grab all the information to display
    func get_device_status(){
        
        // empties data so we can grab updated info
        self.devices = []
        self.devices_status = []
        self.devices_IP = []
        self.devices_MAC = []
        
        // making sure the user is a valid user
        let currentUser = Auth.auth().currentUser
        
        // getting/checking the idToken
        currentUser?.getIDTokenForcingRefresh(true) { idToken, error in
          if let error = error {
            // Handle error
            print("error:", error)
            return;
          }

          // Send token to your backend via HTTPS
          // ...
            // get IP's and MAC'S for connected devices; add to arrays
            let url1 = URL(string: "https://objectfinder.tech/pidata?object=IP&MAC")!
            var request = URLRequest(url: url1)
            request.setValue(idToken, forHTTPHeaderField: "Authorization")
            request.httpMethod = "GET"
            let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
            let unformatted = String(data: data!, encoding: .utf8)!
//            if unformatted != "{\"message\": \"The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.\"}\n"
//            {
//                let cleaned = unformatted.split{$0 == "\""}.map(String.init)
//                if let error = error {
//                    print("Synchronous task ended with error: \(error)")
//                    self.showError("No internet connection.")
//                }
//                else {
//                    print("Synchronous task ended without errors.")
//                    let item = cleaned[11]
//                    let room = cleaned[7]
//                    let dateTime1 = cleaned[3]
//                    self.dateTime = dateTime1
//
//                    if (item.last! == "s") {
//    //                  Show object message
//                        self.showObject("Your \(item) were found in room \(room) at \(dateTime1).")
//                    }
//                    else {
//    //                  Show object message
//                        self.showObject("Your \(item) was found in room \(room) at \(dateTime1).")
//                    }
//                }
//            }
//            else{
//                self.showError("Sorry, could not find \(object).")
//            }
        }
    }
    
    // display the error message
    func showError() {
            errorLabel.text = "Something went wrong please go back and try again."
            tableview.alpha = 0
            errorLabel.alpha = 1
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    // going back the the previous screen
    @IBAction func backPressed(_ sender: Any) {
        self.dismiss(animated: false, completion: nil)
        
    }
    
    
    @IBAction func addNewDevicePressed(_ sender: Any) {
        transitionToAddNewDevice()
    }
    
}
//
//extension URLSession {
//    func synchronousDataTask(urlrequest: URLRequest) -> (Data?, response: URLResponse?, error: Error?) {
//        var data: Data?
//        var response: URLResponse?
//        var error: Error?
//
//        let semaphore = DispatchSemaphore(value: 0)
//
//        let dataTask = self.dataTask(with: urlrequest) {
//            data = $0
//            response = $1
//            error = $2
//
//            semaphore.signal()
//        }
//        dataTask.resume()
//
//        _ = semaphore.wait(timeout: .distantFuture)
//
//        return (data, response, error)
//    }
//}


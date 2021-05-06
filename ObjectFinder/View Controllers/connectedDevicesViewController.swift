//
//  connectedDevicesViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/25/21.
//  and by branson
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
        return self.table_size
    }
    
    
    func set_count (num: Int){
        self.table_size = num
    }
    
    // adds the information to the table that displays the devices connected
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "connectedDevicesViewController", for: indexPath)
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
            let url1 = URL(string: "https://objectfinder.tech/devices")!
            var request = URLRequest(url: url1)
            request.setValue(idToken, forHTTPHeaderField: "Authorization")
            request.httpMethod = "GET"
            let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
            var unformatted = String(data: data!, encoding: .utf8)!
            
            unformatted = String(unformatted.filter { !"\n\t\r\"\\".contains($0) })
            
            if unformatted != "[]"
            {
            unformatted = self.get_all(info: unformatted)
            unformatted = self.get_all(info: unformatted)
            }
            //
            let devices_list = unformatted.components(separatedBy: "}, {")
            if devices_list[0] != "[]"
            {
                
                for device in devices_list
                {
                    let current_device_info = device.components(separatedBy: ", ")
                    self.devices_MAC.append(self.get_mac(info: current_device_info[0]))
                    self.devices_IP.append(self.get_ip(info: current_device_info[1]))
                    self.devices.append(self.get_name(info: current_device_info[2]))
                    self.devices_status.append("INACTIVE")
                    
                }
                
                var count = 0
                for dev in self.devices_IP
                {
                    
                    let url1 = URL(string: "http://\(dev):5000/status")!
                    var request = URLRequest(url: url1)
                    request.setValue(idToken, forHTTPHeaderField: "Authorization")
                    request.httpMethod = "GET"
                    let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                    if error == nil{
                        self.devices_status[count] = "ACTIVE"
                    }
                    count += 1
                }
                
               
            }
            self.set_count(num: devices_list.count)
//            self.tableview.reloadData()
                
            cell.textLabel?.text = self.devices[indexPath.row]
            cell.detailTextLabel?.text = self.devices_status[indexPath.row]
            
        }
        
        return cell
    }
    
    // if user wants to get more information on a device this will go to a new controller that will provide
    // details like (MAC, IP, Device ID, Devices Status)
    func transitionToStatus(num: Int) {
        // making sure the user is a valid user
        let currentUser = Auth.auth().currentUser
        
        // getting/checking the idToken
        currentUser?.getIDTokenForcingRefresh(true) { idToken, error in
          if let error = error {
            // Handle error
            print("error:", error)
            return;
          }

//          // Send token to your backend via HTTPS
//          // ...
//            // get IP's and MAC'S for connected devices; add to arrays
//            for dev in self.devices_IP
//            {
//
//                let url1 = URL(string: "http://\(dev):5000/room")!
//                var request = URLRequest(url: url1)
//                request.setValue(idToken, forHTTPHeaderField: "Authorization")
//                request.httpMethod = "GET"
//                let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
//                if error == nil{
//                    var unformatted = String(data: data!, encoding: .utf8)!
//
//                    // {roomID: "name"}
//
//                    unformatted = String(unformatted.filter { !"\n\t\r\"\\".contains($0) })
//                    unformatted = self.get_all(info: unformatted)
//                    let devices_list = unformatted.components(separatedBy: ": ")
//
//                    self.devices.append(devices_list[1])
//                }else{
//                    return
//                }
//
//            }
//
//
//            for dev in self.devices_IP
//            {
//                let url1 = URL(string: "http://\(dev):5000/status")!
//                var request = URLRequest(url: url1)
//                request.setValue(idToken, forHTTPHeaderField: "Authorization")
//                request.httpMethod = "GET"
//                let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
//                if error == nil
//                {
//                var unformatted = String(data: data!, encoding: .utf8)!
//
//                // {roomID: "name"}
//
//                unformatted = String(unformatted.filter { !"\n\t\r\"\\".contains($0) })
//                unformatted = self.get_all(info: unformatted)
//                let devices_list = unformatted.components(separatedBy: ": ")
//                self.devices_status.append(devices_list[1])
//                }
//
//            }
            // Send token to your backend via HTTPS
            // ...
              // get IP's and MAC'S for connected devices; add to arrays
              let url1 = URL(string: "https://objectfinder.tech/devices")!
              var request = URLRequest(url: url1)
              request.setValue(idToken, forHTTPHeaderField: "Authorization")
              request.httpMethod = "GET"
              let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
              var unformatted = String(data: data!, encoding: .utf8)!
              
              unformatted = String(unformatted.filter { !"\n\t\r\"\\".contains($0) })
                if unformatted != "[]"
                {
                unformatted = self.get_all(info: unformatted)
                unformatted = self.get_all(info: unformatted)
                }
            
              //
              let devices_list = unformatted.components(separatedBy: "}, {")
              if devices_list[0] != ""
              {
                  
                  for device in devices_list
                  {
                      let current_device_info = device.components(separatedBy: ", ")
                      self.devices_MAC.append(self.get_mac(info: current_device_info[0]))
                      self.devices_IP.append(self.get_ip(info: current_device_info[1]))
                      self.devices.append(self.get_name(info: current_device_info[2]))
                      self.devices_status.append("INACTIVE")
                      
                  }
                  
                  var count = 0
                  for dev in self.devices_IP
                  {
                      
                      let url1 = URL(string: "http://\(dev):5000/status")!
                      var request = URLRequest(url: url1)
                      request.setValue(idToken, forHTTPHeaderField: "Authorization")
                      request.httpMethod = "GET"
                      let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                      if error == nil{
                          self.devices_status[count] = "ACTIVE"
                      }
                      count += 1
                  }
            
//
            
            let story = UIStoryboard(name: "Main", bundle: nil)
            let controller = story.instantiateViewController(identifier: "DevicesStatusViewController") as! DevicesStatusViewController
            
            controller.id_detail = self.devices[num]
            controller.status_detail = self.devices_status[num]
            controller.IP_detail = self.devices_IP[num]
            controller.MAC_detail = self.devices_MAC[num]
            self.present(controller, animated: true, completion: nil)
        }
        }
    
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
    var devices = ["Room 0", "Room 1",""]
    var devices_status = ["inactive0", "inactive1",""]
    var devices_IP = ["192.168.0.10", "192.168.0.11",""]
    var devices_MAC = ["MAC0", "MAC1",""]
    var table_size = 0
    var run  = 0
    //
    
        
//    let myRefreshControl = UIRefreshControl()
//
//    // if the users swipes down on the table it will refresh the data from the above info after 3 seconds
//    @objc func handleRefresh(_ sender: UIRefreshControl) {
//            Timer.scheduledTimer(withTimeInterval: 3.0, repeats: false) { (timer) in
//                self.tableview.reloadData()
//                self.myRefreshControl.endRefreshing()
//            }
//        }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableview.delegate = self
        tableview.dataSource = self
        tableview.alpha = 1
        errorLabel.alpha = 0
        DispatchQueue.global(qos: .userInitiated).async {
            self.devices = []
            self.devices_status = []
            self.devices_IP = []
            self.devices_MAC = []
    //
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
                let url1 = URL(string: "https://objectfinder.tech/devices")!
                var request = URLRequest(url: url1)
                request.setValue(idToken, forHTTPHeaderField: "Authorization")
                request.httpMethod = "GET"
                let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                var unformatted = String(data: data!, encoding: .utf8)!
                
                unformatted = String(unformatted.filter { !"\n\t\r\"\\".contains($0) })
                
                if unformatted != "[]"
                {
                unformatted = self.get_all(info: unformatted)
                unformatted = self.get_all(info: unformatted)
                }
                
                //
                let devices_list = unformatted.components(separatedBy: "}, {")
                if devices_list[0] != "[]"
                {
                    for device in devices_list
                    {
                        let current_device_info = device.components(separatedBy: ", ")
                        self.devices_MAC.append(self.get_mac(info: current_device_info[0]))
                        self.devices_IP.append(self.get_ip(info: current_device_info[1]))
                        self.devices.append(self.get_name(info: current_device_info[2]))
                        self.devices_status.append("INACTIVE")
                    }
                    
                    var count = 0
                    for dev in self.devices_IP
                    {
                        
                        let url1 = URL(string: "http://\(dev):5000/status")!
                        var request = URLRequest(url: url1)
                        request.setValue(idToken, forHTTPHeaderField: "Authorization")
                        request.httpMethod = "GET"
                        let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                        if error == nil{
                            self.devices_status[count] = "ACTIVE"
                        }
                        count += 1
                    }
                    
                    self.set_count(num: devices_list.count)
                    self.tableview.reloadData()
                }
                
            }
        }
            
            
            
        Utilities.styleFilledButton(addNewDeviceLabel)
            
    //
    //        myRefreshControl.addTarget(self, action: #selector(connectedDevicesViewController.handleRefresh), for: .valueChanged)
    //        tableview.refreshControl = myRefreshControl
    //        get_device_status()
        
        
    }
    
    func get_status()
    {
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
            var count = 0
            for dev in self.devices_IP
            {
                
                let url1 = URL(string: "http://\(dev):5000/status")!
                var request = URLRequest(url: url1)
                request.setValue(idToken, forHTTPHeaderField: "Authorization")
                request.httpMethod = "GET"
                let (data, _, error) = URLSession.shared.synchronousDataTask(urlrequest: request)
                if error == nil{
                    self.devices_status[count] = "ACTIVE"
                }
                count += 1
            }
        
        }
    }
    
    
    func get_all(info: String) -> String
    {
        let start = info.index(info.startIndex, offsetBy: 1)
        let end = info.index(info.endIndex, offsetBy: -1)
        let range = start..<end
        return String(info[range])
    }
    
    func get_name(info: String) -> String
    {
        let start = info.index(info.startIndex, offsetBy: 6)
        let end = info.index(info.endIndex, offsetBy: 0)
        let range = start..<end
        return String(info[range])
    }
    
    func get_ip(info: String) -> String
    {
        let start = info.index(info.startIndex, offsetBy: 4)
        let end = info.index(info.endIndex, offsetBy: 0)
        let range = start..<end
        return String(info[range])
    }
    
    func get_mac(info: String) -> String
    {
        let start = info.index(info.startIndex, offsetBy: 5)
        let end = info.index(info.endIndex, offsetBy: 0)
        let range = start..<end
        return String(info[range])
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

//
//  connectedDevicesViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/25/21.
//

import UIKit
import FirebaseAuth

class connectedDevicesViewController: UIViewController, UITableViewDataSource, UITabBarDelegate, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return devices.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "connectedDevicesViewController", for: indexPath)
        cell.textLabel?.text = devices[indexPath.row]
        cell.detailTextLabel?.text = devices_status[indexPath.row]
        return cell
    }
    
    @IBOutlet weak var errorLabel: UILabel!
    
    @IBOutlet weak var tableview: UITableView!
    var devices = ["Room 1", "Room 2", "Room 3"]
    var devices_status = ["inactive", "inactive", "inactive"]
    let myRefreshControl = UIRefreshControl()
    
    
    @objc func handleRefresh(_ sender: UIRefreshControl) {
            Timer.scheduledTimer(withTimeInterval: 3.0, repeats: false) { (timer) in
                self.get_device_status()
                self.myRefreshControl.endRefreshing()
            }
        }
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableview.delegate = self
        tableview.dataSource = self
        tableview.alpha = 1
        errorLabel.alpha = 0
        
        myRefreshControl.addTarget(self, action: #selector(connectedDevicesViewController.handleRefresh), for: .valueChanged)
        tableview.refreshControl = myRefreshControl
        get_device_status()
        
    }
    
    
    
    func get_device_status(){
        self.devices = []
        self.devices_status = []
        let currentUser = Auth.auth().currentUser
        
        currentUser?.getIDTokenForcingRefresh(true) { idToken, error in
          if let error = error {
            // Handle error
            print("error:", error)
            return;
          }

          // Send token to your backend via HTTPS
          // ...
                    
            let url1 = URL(string: "https://objectfinder.tech/pidata?object=Cellphone")!
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
    
    
    @IBAction func backPressed(_ sender: Any) {
        self.dismiss(animated: false, completion: nil)
        
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


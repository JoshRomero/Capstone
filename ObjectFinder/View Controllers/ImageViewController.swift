//
//  ImageViewController.swift
//  ObjectFinder
//
//  Created by Josh Romero on 4/21/21.
//

import UIKit
import FirebaseAuth

class ImageViewController: UIViewController {

    @IBOutlet weak var imageView: UIImageView!
    
    // need dateTime because that is the name of the image in the DB
    var dateTime = ""
    func getData(from urlrequest: URLRequest, completion: @escaping (Data?, URLResponse?, Error?) -> ()) {
        URLSession.shared.dataTask(with: urlrequest, completionHandler: completion).resume()
    }


    // grabes the image from the DB and displays it
    func downloadImage() {
        
        // confirms the idToken
        let currentUser = Auth.auth().currentUser
                    currentUser?.getIDTokenForcingRefresh(true) { idToken, error in
                      if let error = error {
                        // Handle error
                        print("error:", error)
                        return;
                      }

                      // Send token to your backend via HTTPS
                      // ...
                        let url1 = URL(string: "https://objectfinder.tech/pidata/image?dateTime=\(self.dateTime)")!
                        var request = URLRequest(url: url1)
                        request.setValue(idToken, forHTTPHeaderField: "Authorization")
                        request.httpMethod = "GET"
                        print("Download Started")
                        self.getData(from: request) { data, response, error in
                            guard let data = data, error == nil else { return }
                            print(response?.suggestedFilename ?? url1.lastPathComponent)
                            print("Download Finished")
                            // always update the UI from the main thread
                            DispatchQueue.main.async() { [weak self] in
                                self?.imageView.image = UIImage(data: data)
                            }
                        }
                       
                    }
        

    }



    override func viewDidLoad() {
        super.viewDidLoad()
        print("Begin of code")
        downloadImage()
        print("End of code. The image will continue downloading in the background and it will be loaded when it ends.")
    }
}


extension UIImageView {
    func downloaded(from url: URL, contentMode mode: ContentMode = .scaleAspectFit) {
        contentMode = mode
        URLSession.shared.dataTask(with: url) { data, response, error in
            guard
                let httpURLResponse = response as? HTTPURLResponse, httpURLResponse.statusCode == 200,
                let mimeType = response?.mimeType, mimeType.hasPrefix("image"),
                let data = data, error == nil,
                let image = UIImage(data: data)
                else { return }
            DispatchQueue.main.async() { [weak self] in
                self?.image = image
            }
        }.resume()
    }
    func downloaded(from link: String, contentMode mode: ContentMode = .scaleAspectFit) {
        guard let url = URL(string: link) else { return }
        downloaded(from: url, contentMode: mode)
    }
}


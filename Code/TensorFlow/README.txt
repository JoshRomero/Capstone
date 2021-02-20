############################	This is a document explaining how to use the code in the folder to create new trained neural networks, then how to use them on images, videos, and webcams.

Note: I am on a windows system which mean it does \ instead of /. YOU MUST CHANGE IN CODE

Note: You must have the correct version, Tensorflow is very moody.

    1. Version list can be found https://www.tensorflow.org/install 
       
    2. Make sure your GPU is supported. https://developer.nvidia.com/cuda-gpus
       
    3. Make sure you gpu driver is up todate. https://www.nvidia.com/download/index.aspx?lang=en-us
       
       # If you have a GPU that is compatible
    4. 1: install Cuda 10.0 and CudNN 7.6.0
        a. https://developer.nvidia.com/cuda-toolkit-archive
        b. https://developer.nvidia.com/rdp/cudnn-archive
    5. install anaconda: https://www.anaconda.com/products/individual#windows
        a. Note: during installation you should select the option to add the Path to your environment variables. It makes things easier.
    6. Open command prompt
    7. create a virtual environment using anaconda
        a. conda create --name tensorflow1 python=3.7.9
            i. y
    8. You must activate the tensorflow1 environment
        a.  conda activate tensorflow1
    9. install tensorflow: 
        a. pip install tensorflow-gpu==1.15.0
    10. navigate to the virtual environment folder 
        a. C:\Users\<name>\anaconda3\envs\tensorflow1
    11. create a folder called TensorFlow
    12. navigate into TensorFlow
    13. download the tensorflow models
        a. get clone https://github.com/tensorflow/models.git
    14. 





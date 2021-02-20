############################	This is a document explaining how to use the code in the folder to create new trained neural networks, then how to use them on images, videos, and webcams.

Note: I am on a windows system which mean it does \ instead of /. YOU MUST CHANGE IN CODE

Note: You must have the correct version, Tensorflow is very moody.

    1) Version list can be found https://www.tensorflow.org/install 
        
    2) Make sure your GPU is supported. https://developer.nvidia.com/cuda-gpus
             
    3) Make sure you gpu driver is up todate.
        a. https://www.nvidia.com/download/index.aspx?lang=en-us
              
       # If you have a GPU that is compatible
    4) install Cuda 10.0 and CudNN 7.6.0
        a. https://developer.nvidia.com/cuda-toolkit-archive
        b. https://developer.nvidia.com/rdp/cudnn-archive
           
    5) install anaconda: https://www.anaconda.com/products/individual#windows
        a. Note: during installation you should select the option to add the Path to your environment variables. It makes things easier.
    6) Open command prompt
    7) create a virtual environment using anaconda
        a. conda create --name tensorflow1 python=3.7.9
            i. y
    8) You must activate the tensorflow1 environment
        a. conda activate tensorflow1
    9) install tensorflow: 
        a. pip install tensorflow-gpu==1.15.0

    10) navigate to the virtual environment folder 
        a. cd C:\Users\<name>\anaconda3\envs\tensorflow1
    11) create a folder called TensorFlow
    12) navigate into TensorFlow
    13) download the tensorflow models
        a. get clone https://github.com/tensorflow/models.git
    14) set PYTHONPATH and PATH
        a. set PATH=%PATH%;PYTHONPATH
        b. set PYTHONPATH=C:\Users\<name>\anaconda3\envs\tensorflow1\TensorFlow\models;C:\Users\<name>\anaconda3\envs\tensorflow1\TensorFlow\models\research;C:\Users\<name>\anaconda3\envs\tensorflow1\TensorFlow\models\research\slim
    15) install other important things
        a. conda install -c anaconda protobuf==3.15.0
        b. pip install pillow==8.1.0
        c. pip install lxml==4.6.2
        d. pip install Cython==0.29.21
        e. pip install contextlib2==0.6.0.post1
        f. pip install jupyter
        g. pip install matplotlib==3.3.4
        h. pip install pandas==1.2.2
        i. pip install opencv-python==4.5.1.48
    16) replace the protos folder in the downloaded github with the protos in the add to downloaded repo in our github
    17) move the setup.py from the research\slim folder to the research folder
    18) from the research folder run
        a. python setup.py build
        b. python setup.py install
    19) test tensorflow 
        a. python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
    20) move all file and folders from our github to the downloaded github except bin folder to the research\object_detection folder 
    21) move bin to the models\research folder
    22) add the above bin folder to you environment variables (Path)
    






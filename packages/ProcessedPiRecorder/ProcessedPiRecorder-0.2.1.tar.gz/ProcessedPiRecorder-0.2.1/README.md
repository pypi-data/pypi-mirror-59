# ProcessedPiRecorder
A multiprocessed class of picamera for simplified deployment of high framerate computer vision on raspberry pi. 

## Installation

      pip install ProcessedPiRecorder

## Requires

Library | Version
--------|--------
tifffile | 2019.7.26    
picamera | 1.13         
opencv-contrib-python | 3.4.4.19     
numpy | 1.17.0  
imageio | 2.6.1

I'm sure it would work with other versions, but these are the ones used during dev.

## Basic Usage
You have to initialize the recorder and then tell it when to start recording. 

### Initialize:

      from ProcessedPiRecorder import ProcessedPiRecorder as ppr

      myRecorder = ppr(tif_path, x_resolution=0, y_resolution=0, scale_factor=1, framerate=0, 
                       rec_length=0, display=True, display_proc='camera_reader', stereo=False,
                       timestamp=False, report_Hz=False, monitor_qs= False,
                       callback=None, cb_type=None, blocking=True, 
                       write_vid=True, tif_compression=6, buffer_length=1, Hz_buffer=10,
                       log_file=None)
Arg | Description
----|------------
tif_path | file to the output big tif file
(x_resolution, y_resolution) | pixel dimensions acquired by the sensor(s), is autmatically rounded to nearest multiple of 16, or nearest multiple of 32 for StereoPi x_resolution. 
scale_factor | sets the resize parameter at resolultion*scale_factor, neede for StereoPi
framerate | desired framerate in Hz
rec_length | number of seconds to record
stereo | if True, sets up for the stereopi hflip=True, stereo_mode='side-by-side', stereo_decimate=False
display | if True, display video stream 
display_proc | specifies which process should be used to display. Either 'camera_reader' or 'file_writer'. 
timestamp | if True, all frames are timestapmed at aquisition
report_Hz | if True, all frames have the current frame rate stamped at aquisition
monitor_qs | if True, all frames have all queue lengths stamped at aquisition
callback | if True, execute a callback function
cb_type | if executing a callback, specifies either the 2 process (='2Proc') or 3 process (='3Proc') workflow
blocking | if True, block the main thread after spawning processes
write_vid | if True, saves the video stream into tif_path
tif_compression | specifies the degress of image compression used by tifffile
buffer_length | number of frames to be held in collections.deque frame buffer which is passed to the callback 
Hz_buffer | number of frames to average over when displaying framerate (report_Hz=True)
log_file | if path is provided, write frame log to destination, useful for debugging 

### Start recording

      myRecorder.recordVid()
      
## Queues and Callbacks

ProcessedPiRecorder works by separating the acquisition, computer vision, and file encoding tasks across multiple python processes using the standard python multiprocessing library. These processes pass frames using multiprocessing.Queue objects which are scoped to be inaccessible to the user so you don't muck them up. 

### Queue Structure

![image](https://docs.google.com/drawings/d/e/2PACX-1vTXOWzwBbJXiHAlQ2O2yern1L8TyWnSlfooWjhQqmJVHwOtCrFQGigZHY8wW8yBQOjxfdXcpGitcOYS/pub?w=1006&h=828)

### Callback structure
Computer vision can be easily added by means of a callback function. This function can be executed in same process as the file encoding (cb_type='2Proc') or in its own process (cb_type='3Proc'). In either case the callback can communicate with the main process, if unblocked, using the cb_queue attached to the ProcessedPiRecorder object. Buffer is a collection.deque of frames with maxlen=buffer_length.

       callback_fucntion(buffer, cb_queue):
            #Make sure the deque is full
            if len(buffer) == self.buffer_length:
                  
                  #do some stuff to the frame buffer
                  frame = some_fn(buffer)

                  #Communicate to the main_process over the queue
                  cb_queue.put('HiMom')

                  #Must return the processed frame
                  return(frame)
            
            
Arg | Description
----|------------
buffer | a collections.deque with maxlen=buffer_length containing the last buffer_length of frames. I would advise making callback execution conditional on len(buffer) as the deque will not be full until buffer_length frames have been aquired.
cb_queue | multiprocessing.Queue object attached to the ppr object (myRecorder.cb_queue). Enables comunication between the callback and the main_process.

## StereoPi support

The StereoPi is cool, but using standard PiCamera you can't save a highframerate video to file without dropping frames, ProcessedPiRecorder fixes that. Be aware that the scale_factor parameter must be used to down sample the frames. I use the following parameters as a starting point for high framerate acquisition (~28Hz) on stereopi: 

      x_resolution=1280, y_resolution=480, scale_factor=0.3, framerate=25

## Contributors
This code was written and is maintained by [Matt Davenport](https://github.com/mattisabrat) (mdavenport@rockefeller.edu).

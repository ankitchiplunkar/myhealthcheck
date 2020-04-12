from PIL import Image
import numpy as np
import cv2
import sys

# Webcam Parameters
realWidth = 320
realHeight = 240
videoWidth = 160
videoHeight = 120
videoChannels = 3
videoFrameRate = 15

# Color Magnification Parameters
levels = 3
alpha = 170
minFrequency = 1.0
maxFrequency = 2.0
bufferSize = 150
bufferIndex = 0

# Output Display Parameters
font = cv2.FONT_HERSHEY_SIMPLEX
loadingTextLocation = (20, 30)
bpmTextLocation = (videoWidth//2 + 5, 30)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2
boxColor = (0, 255, 0)
boxWeight = 3

def buildGauss(frame, levels):
            pyramid = [frame]
            for level in range(levels):
                frame = cv2.pyrDown(frame)
                pyramid.append(frame)
            return pyramid


def reconstructFrame(pyramid, index, levels):
            filteredFrame = pyramid[index]
            for level in range(levels):
                filteredFrame = cv2.pyrUp(filteredFrame)
            filteredFrame = filteredFrame[:videoHeight, :videoWidth]
            return filteredFrame

print('reached here!')

# Initialize Gaussian Pyramid
firstFrame = np.zeros((videoHeight, videoWidth, videoChannels))
firstGauss = buildGauss(firstFrame, levels+1)[levels]
videoGauss = np.zeros(
    (bufferSize, firstGauss.shape[0], firstGauss.shape[1], videoChannels))
fourierTransformAvg = np.zeros((bufferSize))

# Bandpass Filter for Specified Frequencies
frequencies = (1.0*videoFrameRate) * np.arange(bufferSize) / (1.0*bufferSize)
mask = (frequencies >= minFrequency) & (frequencies <= maxFrequency)

# Heart Rate Calculation Variables
bpmCalculationFrequency = 15
bpmBufferIndex = 0
bpmBufferSize = 10
bpmBuffer = np.zeros((bpmBufferSize))



class HeartMonitor(object):
    def __init__(self):
        pass

    def apply_makeup(self, frame):

        detectionFrame = frame[videoHeight//2:realHeight -
                           videoHeight//2, videoWidth//2:realWidth-videoWidth//2, :]
        
        videoGauss[bufferIndex] = buildGauss(detectionFrame, levels+1)[levels]
        fourierTransform = np.fft.fft(videoGauss, axis=0)

        # Bandpass Filter
        fourierTransform[mask == False] = 0

        # Grab a Pulse
        if bufferIndex % bpmCalculationFrequency == 0:
            i = i + 1
            for buf in range(bufferSize):
                fourierTransformAvg[buf] = np.real(fourierTransform[buf]).mean()
            hz = frequencies[np.argmax(fourierTransformAvg)]
            bpm = 60.0 * hz
            bpmBuffer[bpmBufferIndex] = bpm
            bpmBufferIndex = (bpmBufferIndex + 1) % bpmBufferSize

        # Amplify
        filtered = np.real(np.fft.ifft(fourierTransform, axis=0))
        filtered = filtered * alpha

        # Reconstruct Resulting Frame
        filteredFrame = reconstructFrame(filtered, bufferIndex, levels)
        outputFrame = detectionFrame + filteredFrame
        outputFrame = cv2.convertScaleAbs(outputFrame)

        bufferIndex = (bufferIndex + 1) % bufferSize

        frame[videoHeight//2:realHeight-videoHeight//2,
            videoWidth//2:realWidth-videoWidth//2, :] = outputFrame
        cv2.rectangle(frame, (videoWidth//2, videoHeight//2), (realWidth -
                                                            videoWidth//2, realHeight-videoHeight//2), boxColor, boxWeight)
        if i > bpmBufferSize:
            cv2.putText(frame, "BPM: %d" % bpmBuffer.mean(),
                        bpmTextLocation, font, fontScale, fontColor, lineType)
        else:
            cv2.putText(frame, "Calculating BPM...", loadingTextLocation,
                        font, fontScale, fontColor, lineType)
        return frame


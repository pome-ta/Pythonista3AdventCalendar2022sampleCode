from math import sin, pi
import ctypes

from objc_util import ObjCClass, ObjCBlock
import ui

#import pdbg

CHANNEL = 1

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
AVAudioFormat = ObjCClass('AVAudioFormat')


class AudioBuffer(ctypes.Structure):
  _fields_ = [
    ('mNumberChannels', ctypes.c_uint32),
    ('mDataByteSize', ctypes.c_uint32),
    ('mData', ctypes.c_void_p),
  ]


class AudioBufferList(ctypes.Structure):
  _fields_ = [
    ('mNumberBuffers', ctypes.c_uint32),
    ('mBuffers', AudioBuffer * CHANNEL),
  ]


class Synth:
  def __init__(self):
    self.audioEngine: AVAudioEngine
    self.sampleRate: float = 44100.0  # set_up メソッド: outputNode より確定
    self.deltaTime: float = 0.0  # 1/sampleRate 時間間隔
    self.timex: float = 0.0  # Render の間隔カウンター

    self.render_block = ObjCBlock(
      self.source_node_render,
      restype=OSStatus,
      argtypes=[
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
        ctypes.POINTER(AudioBufferList)
      ])

    self.set_up()

  def set_up(self):
    audioEngine = AVAudioEngine.new()
    sourceNode = AVAudioSourceNode.alloc()
    mainMixer = audioEngine.mainMixerNode()
    outputNode = audioEngine.outputNode()
    format = outputNode.inputFormatForBus_(0)

    self.sampleRate = format.sampleRate()
    self.deltaTime = 1 / self.sampleRate

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat(), self.sampleRate, CHANNEL, format.isInterleaved())

    sourceNode.initWithFormat_renderBlock_(inputFormat, self.render_block)

    audioEngine.attachNode_(sourceNode)
    sourceNode.volume = 0.1

    audioEngine.connect_to_format_(sourceNode, mainMixer, inputFormat)
    audioEngine.connect_to_format_(mainMixer, outputNode, inputFormat)

    audioEngine.prepare()
    self.audioEngine = audioEngine

  def source_node_render(self,
                         _cmd: ctypes.c_void_p,
                         _isSilence_ptr: ctypes.c_void_p,
                         _timestamp_ptr: ctypes.c_void_p,
                         frameCount: ctypes.c_void_p,
                         outputData_ptr: ctypes.POINTER) -> OSStatus:
    # todo: ここに処理を書く
    ablPointer = outputData_ptr.contents
    for frame in range(frameCount):
      sampleVal = sin(440.0 * 2.0 * pi * self.timex)
      #self._outlog(sampleVal)
      self.timex += self.deltaTime

      for bufferr in range(ablPointer.mNumberBuffers):
        _mData = ablPointer.mBuffers[bufferr].mData
        _pointer = ctypes.POINTER(ctypes.c_float * frameCount)
        buffer = ctypes.cast(_mData, _pointer).contents
        buffer[frame] = sampleVal
    return 0

  @ui.in_background
  def _outlog(self, value):
    """ 確認用で基本呼び出さない """
    print(value)

  def start(self):
    self.audioEngine.startAndReturnError_(None)

  def stop(self):
    self.audioEngine.stop()


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.synth = Synth()
    self.synth.start()

  def will_close(self):
    self.synth.stop()


if __name__ == '__main__':
  view = View()
  view.present()
  #view.present(style='fullscreen', orientations=['portrait'])

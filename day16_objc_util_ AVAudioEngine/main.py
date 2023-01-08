from math import sin, pi
from random import uniform
import ctypes
from io import BytesIO

import numpy as np
import matplotlib.image

from objc_util import ObjCClass, ObjCInstance, ObjCBlock
import ui

#import pdbg

CHANNEL = 1

OSStatus = ctypes.c_int32

AVAudioEngine = ObjCClass('AVAudioEngine')
AVAudioSourceNode = ObjCClass('AVAudioSourceNode')
AVAudioFormat = ObjCClass('AVAudioFormat')
AVAudioUnitDelay = ObjCClass('AVAudioUnitDelay')


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


class Oscillator:
  def __init__(self):
    self.amplitude: float = 1.0
    self.frequency: float = 440.0
    self.wave_types = [
      self.mixwave,
      self.sine,
      self.triangle,
      self.sawtooth,
      self.square,
      self.white_noise,
      self.tone_triangle,
    ]

  def sine(self, time, *args):
    frequency = args[0] if args else self.frequency
    wave = self.amplitude * sin(2.0 * pi * frequency * time)
    return wave

  def triangle(self, time, frq=None):
    frequency = frq if frq else self.frequency
    period = 1.0 / frequency
    currentTime = time % period
    value = currentTime / period
    result = 0.0
    if value < 0.25:
      result = value * 4
    elif value < 0.75:
      result = 2.0 - (value * 4.0)
    else:
      result = value * 4 - 4.0
    wave = self.amplitude * result
    return wave

  def sawtooth(self, time, frq=None):
    frequency = frq if frq else self.frequency
    period = 1.0 / frequency
    currentTime = time % period
    wave = self.amplitude * ((currentTime / period) * 2 - 1.0)
    return wave

  def square(self, time, frq=None):
    frequency = frq if frq else self.frequency
    period = 1.0 / frequency
    currentTime = time % period
    if (currentTime / period) < 0.5:
      wave = self.amplitude
    else:
      wave = -1.0 * self.amplitude
    return wave

  def white_noise(self, _, frq=None):
    return uniform(-1.0, 1.0)

  def tone_triangle(self, time, frq=None):
    frequency = frq if frq else self.frequency
    period = 1.0 / frequency
    currentTime = time % period
    value = currentTime / period
    result = 0.0
    if value < 0.0:
      result = value * 4
    elif value > 0.8:
      result = value * 4 - 4.0
    else:
      result = 0
    wave = self.amplitude * result
    return wave

  def mixwave(self, time):
    _step = 3 + int(sin(pi * time) * 10)
    steps = _step if _step else 1
    wave01 = self.square(time) * self.tone_triangle(time, _step)
    wave02 = self.white_noise(time) * self.tone_triangle(time, 1)
    wave = wave01 + wave02
    return wave


class Synth:
  def __init__(self, parent):
    self.parent: ui.View = parent  # 親となるui.View
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

    self.tap_block = ObjCBlock(
      self.audio_node_tap,
      restype=None,
      argtypes=[
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
      ])

    self.set_up()

  def set_up(self):
    audioEngine = AVAudioEngine.new()
    sourceNode = AVAudioSourceNode.alloc()
    mainMixer = audioEngine.mainMixerNode()
    outputNode = audioEngine.outputNode()
    format = outputNode.inputFormatForBus_(0)

    delay = AVAudioUnitDelay.new()
    delay.delayTime = 0.3
    delay.feedback = 80

    self.sampleRate = format.sampleRate()
    self.deltaTime = 1 / self.sampleRate

    inputFormat = AVAudioFormat.alloc(
    ).initWithCommonFormat_sampleRate_channels_interleaved_(
      format.commonFormat(), self.sampleRate, CHANNEL, format.isInterleaved())

    sourceNode.initWithFormat_renderBlock_(inputFormat, self.render_block)

    audioEngine.attachNode_(sourceNode)
    sourceNode.volume = 0.1

    audioEngine.attachNode_(delay)

    audioEngine.connect_to_format_(sourceNode, delay, inputFormat)
    audioEngine.connect_to_format_(delay, mainMixer, inputFormat)

    audioEngine.connect_to_format_(mainMixer, outputNode, inputFormat)

    audioEngine.prepare()

    _bufsize = 64 * 64  # 取得する情報量
    mainMixer.installTapOnBus_bufferSize_format_block_(
      0, _bufsize, inputFormat, self.tap_block)
    self.audioEngine = audioEngine

  def source_node_render(self,
                         _cmd: ctypes.c_void_p,
                         _isSilence_ptr: ctypes.c_void_p,
                         _timestamp_ptr: ctypes.c_void_p,
                         frameCount: ctypes.c_void_p,
                         outputData_ptr: ctypes.POINTER) -> OSStatus:
    ablPointer = outputData_ptr.contents
    for frame in range(frameCount):
      sampleVal = self.parent.toneGenerator(self.timex)

      self.timex += self.deltaTime

      for bufferr in range(ablPointer.mNumberBuffers):
        _mData = ablPointer.mBuffers[bufferr].mData
        _pointer = ctypes.POINTER(ctypes.c_float * frameCount)
        buffer = ctypes.cast(_mData, _pointer).contents
        buffer[frame] = sampleVal
    return 0

  def audio_node_tap(self, _cmd, buffer, when):
    buf = ObjCInstance(buffer)
    _array = buf.floatChannelData()[0]
    # 画像生成用に配列組み替え
    np_buff = np.ctypeslib.as_array(_array, (256, 16))
    with BytesIO() as bIO:
      matplotlib.image.imsave(bIO, np_buff + 1, format='png')
      img = ui.Image.from_data(bIO.getvalue())
      self.parent.visualize_view.image = img

  def start(self):
    self.audioEngine.startAndReturnError_(None)

  def stop(self):
    self.audioEngine.stop()


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)

    self.visualize_view = ui.ImageView()
    self.visualize_view.bg_color = 0
    self.visualize_view.flex = 'WH'
    #self.visualize_view.flex = 'TBRL'
    self.add_subview(self.visualize_view)

    self.type_osc = ui.Slider()
    self.level_frq = ui.Slider()
    self.osc_log = ui.Label()
    self.frq_log = ui.Label()

    self.osc = Oscillator()
    self.toneGenerator: Oscillator
    self.setup_osc()

    self.synth = Synth(self)
    self.synth.start()

  def setup_osc(self):
    self.toneGenerator = self.osc.wave_types[0]
    self.setup_type_osc()
    self.setup_frq_level()

  def setup_type_osc(self):
    # --- slider
    self.type_len = len(self.osc.wave_types) - 1
    self.type_osc.continuous = False
    self.type_osc.value = 0
    self.type_osc.flex = 'W'
    self.type_osc.action = self.change_osc
    self.add_subview(self.type_osc)

    # --- label
    self.osc_log.text = self.toneGenerator.__name__
    self.osc_log.bg_color = 1
    self.osc_log.flex = 'W'
    self.osc_log.size_to_fit()
    self.add_subview(self.osc_log)

  def change_osc(self, sender):
    val = int(sender.value * self.type_len)
    self.toneGenerator = self.osc.wave_types[val]
    self.type_osc.value = val / self.type_len
    self.osc_log.text = self.toneGenerator.__name__

  def setup_frq_level(self):
    # --- slider
    self.max_level_frq = 880.0
    self.level_frq.value = self.osc.frequency / self.max_level_frq
    self.level_frq.flex = 'W'
    self.level_frq.action = self.change_frq
    self.add_subview(self.level_frq)

    # --- label
    self.frq_log.text = f'{self.osc.frequency}'
    self.frq_log.bg_color = 1
    self.frq_log.flex = 'W'
    self.frq_log.size_to_fit()
    self.add_subview(self.frq_log)

  def change_frq(self, sender):
    val = sender.value * self.max_level_frq
    self.osc.frequency = val
    self.frq_log.text = f'{self.osc.frequency}'

  def layout(self):
    # --- slider
    self.type_osc.y = self.type_osc.height
    self.level_frq.y = self.type_osc.height + self.type_osc.y * 2

    # --- label
    self.osc_log.y = self.frame.height / 2 - self.osc_log.height
    self.frq_log.y = self.osc_log.y + self.frq_log.height

    logs_width = self.frame.width / 2
    self.osc_log.width = self.frq_log.width = logs_width

  def will_close(self):
    self.synth.stop()


if __name__ == '__main__':
  view = View()
  #view.present()
  # スライダー操作時にView が動いてしまうため
  view.present(style='fullscreen', orientations=['portrait'])

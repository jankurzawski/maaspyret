#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Wed Feb 25 13:49:27 2026
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup, plugins, prefs

plugins.activatePlugins()
import os  # handy system and path functions
import sys  # to get file system encoding

import numpy as np  # whole numpy lib is available, prepend 'np.'
import psychopy.iohub as io
from numpy import (
    asarray,
    average,
    cos,
    deg2rad,
    linspace,
    log,
    log10,
    pi,
    rad2deg,
    sin,
    sqrt,
    std,
    tan,
)
from numpy.random import choice as randchoice
from numpy.random import normal, randint, random, shuffle

# Run 'Before Experiment' code from code
from PIL import Image
from psychopy import (
    clock,
    colors,
    core,
    data,
    event,
    gui,
    hardware,
    layout,
    logging,
    sound,
    visual,
)
from psychopy.constants import (
    FINISHED,
    FOREVER,
    NOT_STARTED,
    PAUSED,
    PLAYING,
    PRESSED,
    RELEASED,
    STARTED,
    STOPPED,
    priority,
)
from psychopy.hardware import keyboard
from psychopy.tools import environmenttools


def alternating_blocks(a, b, length, n_switches):
    n_blocks = n_switches + 1
    block_size = length // n_blocks

    values = [a, b] * ((n_blocks + 1) // 2)
    values = values[:n_blocks]

    lst = []
    for v in values:
        lst.extend([v] * block_size)

    # pad remainder if length not divisible
    remainder = length - len(lst)
    if remainder > 0:
        lst.extend([values[-1]] * remainder)

    return lst


# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = "2024.2.4"
expName = "maaspyret"  # from the Builder filename that created this script
# Default Paths, used throughtout, for masks and images.
base_mask_folder = "./masks/"
base_image_folder = "./carriers/"


def get_subfolders(base_mask_folder, base_image_folder):
    """
    Get the subfolders in the image and mask folders.

    Parameters
    ==========
    base_image_folder : str
        Path to the image folder, hard coded, relative to python file.
    base_mask_folder : str
        Path to the mask folder, hard coded, relative to python file.

    Returns
    ==========
    tuple of lists
        List of subfolders in the image folder and list of subfolders in the mask folder.
    """

    # Read the masks folder, what subfolders do we have?
    mask_subfolders = [
        f
        for f in os.listdir(base_mask_folder)
        if os.path.isdir(os.path.join(base_mask_folder, f))
    ]
    # Same for the carriers folder
    carrier_subfolders = [
        f
        for f in os.listdir(base_image_folder)
        if os.path.isdir(os.path.join(base_image_folder, f))
    ]
    return mask_subfolders, carrier_subfolders


# Run this once to populate, then use again in loop in main.
mask_subfolders, carrier_subfolders = get_subfolders(
    base_mask_folder=base_mask_folder, base_image_folder=base_image_folder
)


def load_previous_run_info():

    try:
        with open("_last_subject.txt", "r") as f:
            # Can be string, number, etc
            saved_subject_num = f.read().strip()
    except (FileNotFoundError, ValueError):
        saved_subject_num = 100  # Default subject number

    try:
        with open("_last_session.txt", "r") as f:
            # Can be string, number, etc
            saved_session = f.read().strip()
    except (FileNotFoundError, ValueError):
        saved_session = 1  # Default session number

    try:
        with open("_last_run.txt", "r") as f:
            saved_run_num = (
                int(f.read().strip()) + 1
            )  # Increment the run number for the next run
    except (FileNotFoundError, ValueError):
        saved_run_num = 1  # Use the default run_num from expInfo

    try:
        with open("_last_Hz.txt", "r") as f:
            saved_Hz = float(
                f.read().strip()
            )  # Increment the run number for the next run
    except (FileNotFoundError, ValueError):
        saved_Hz = 3.0  # Use the default run_num from expInfo

    try:
        with open("_last_duration.txt", "r") as f:
            saved_duration = float(
                f.read().strip()
            )  # Increment the run number for the next run
    except (FileNotFoundError, ValueError):
        saved_duration = 1.0  # Use the default run_num from expInfo

    return saved_subject_num, saved_session, saved_run_num, saved_Hz, saved_duration


saved_subject_num, saved_session, saved_run_num, saved_Hz, saved_duration = (
    load_previous_run_info()
)

# information about this experiment
expInfo = {
    "sub-": f"{saved_subject_num}",
    "ses-": f"{saved_session}",
    "run-": f"{saved_run_num:02d}",
    "date|hid": data.getDateStr(),
    "expName|hid": expName,
    "psychopyVersion|hid": psychopyVersion,
    "Stim Hz": f"{saved_Hz:.1f}",
    "Aperture Duration": f"{saved_duration:.2f}",
    "mask": mask_subfolders,
    "carrier": carrier_subfolders,
}

# --- Define some variables which will change depending on pilot mode ---
"""
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
"""
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1800, 1169]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting["forceWindowed"]:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting["forcedWindowSize"]


def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.

    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)

    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = "data/exp-%s_sub-%s_ses-%s_task-%s_run-%s_%s" % (
        expInfo["expName"],
        expInfo["sub-"],
        expInfo["ses-"],
        expInfo["mask"],
        expInfo["run-"],
        expInfo["date"],
    )
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)

    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName,
        version="",
        extraInfo=expInfo,
        runtimeInfo=None,
        originPath=None,
        savePickle=True,
        saveWideText=True,
        dataFileName=dataDir + os.sep + filename,
        sortColumns="time",
    )
    thisExp.setPriority("thisRow.t", priority.CRITICAL)
    thisExp.setPriority("expName", priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.

    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.

    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(prefs.piloting["pilotConsoleLoggingLevel"])
    else:
        logging.console.setLevel("warning")
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename + ".log")
    if PILOTING:
        logFile.setLevel(prefs.piloting["pilotLoggingLevel"])
    else:
        logFile.setLevel(logging.getLevel("exp"))

    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.

    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug("Fullscreen settings ignored as running in pilot mode.")

    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize,
            fullscr=_fullScr,
            screen=1,
            winType="pyglet",
            allowGUI=False,
            allowStencil=False,
            monitor="UM_3T_Proj",
            color=[0, 0, 0],
            colorSpace="rgb",
            backgroundImage="",
            backgroundFit="none",
            blendMode="avg",
            useFBO=True,
            units="pix",
            checkTiming=False,  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0, 0, 0]
        win.colorSpace = "rgb"
        win.backgroundImage = ""
        win.backgroundFit = "none"
        win.units = "pix"
    if expInfo is not None:
        expInfo["frameRate"] = 60
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting["showPilotingIndicator"]:
        win.showPilotingIndicator()

    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to
    the device manager (deviceManager)

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}

    # Setup iohub keyboard
    ioConfig["Keyboard"] = dict(use_keymap="psychopy")

    # Setup iohub experiment
    ioConfig["Experiment"] = dict(filename=thisExp.dataFileName)

    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)

    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer

    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice("defaultKeyboard") is None:
        deviceManager.addDevice(
            deviceClass="keyboard", deviceName="defaultKeyboard", backend="iohub"
        )
    if deviceManager.getDevice("wait_trigger") is None:
        # initialise wait_trigger
        wait_trigger = deviceManager.addDevice(
            deviceClass="keyboard",
            deviceName="wait_trigger",
        )
    if deviceManager.getDevice("key_resp") is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass="keyboard",
            deviceName="key_resp",
        )
    # return True if completed successfully
    return True


def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.

    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return

    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice("defaultKeyboard")
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass="keyboard",
            deviceName="defaultKeyboard",
            backend="ioHub",
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.

    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice("defaultKeyboard")
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass="keyboard", deviceName="defaultKeyboard", backend="ioHub"
        )
    eyetracker = deviceManager.getDevice("eyetracker")
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if "frameRate" in expInfo and expInfo["frameRate"] is not None:
        frameDur = 1.0 / round(expInfo["frameRate"])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess

    # Start Code - component code to be run after the window creation

    # Save out the subject/session/run info for next time
    np.savetxt("_last_subject.txt", [expInfo["sub-"]], fmt="%s")
    np.savetxt("_last_session.txt", [expInfo["ses-"]], fmt="%s")
    np.savetxt("_last_run.txt", [int(expInfo["run-"])], fmt="%02d")
    np.savetxt("_last_Hz.txt", [float(expInfo["Stim Hz"])], fmt="%.1f")
    np.savetxt("_last_duration.txt", [float(expInfo["Aperture Duration"])], fmt="%.2f")

    # --- Initialize components for Routine "wait_block" ---

    stim_hz = float(expInfo["Stim Hz"])  # was 3
    total_stim_dur = float(expInfo["Aperture Duration"])  # was 1
    frame_dur = 1 / stim_hz
    calc_mask_repeats = stim_hz * total_stim_dur  # we want this to be an integer

    if calc_mask_repeats != int(calc_mask_repeats):
        print("\/" * 30)
        print(
            f"Stimulus Hz of {stim_hz} and aperture duration of {total_stim_dur} results in non-integer repeats of {calc_mask_repeats}. Adjusting these values to get an integer number of repeats."
        )
        calc_mask_repeats = int(calc_mask_repeats)
        print("New number of repeats:", calc_mask_repeats)
        print("\/" * 30)

    if calc_mask_repeats < 1:
        print("\/" * 30)
        print(
            "Calculated number of repeats is less than 1, which is not possible. Setting to 1."
        )
        calc_mask_repeats = 1
        print("New number of repeats:", calc_mask_repeats)
        print("\/" * 30)

    # Load the images and masks here
    # combine the mask and carrier subfolders to make the full paths to the images and masks
    mask_folder = os.path.join(base_mask_folder, expInfo["mask"])
    image_folder = os.path.join(base_image_folder, expInfo["carrier"])

    preloaded_images = []
    # List all image files (ensure sorted order if needed)
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".png")])
    mask_files = sorted([f for f in os.listdir(mask_folder) if f.endswith(".png")])

    print("Loading Images...")
    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        # Ensure RGB format
        pil_img = Image.open(img_path)
        img_array = np.array(pil_img, order="C").astype(float) / 255.0

        # Append to the list
        # flip it vertically so it shows up correctly.
        preloaded_images.append(np.flipud(img_array))

    num_images = len(preloaded_images)

    total_repeats = int(len(mask_files) * calc_mask_repeats)
    # Given this many masks, and the duration, how long should the scan be.
    scan_duration = len(mask_files) * total_stim_dur
    # on average fixation color changes every 20 seconds.
    number_of_rg_switches = int(scan_duration / 20)
    # was fixed at 15 before, but depends on number of masks, etc. 20s approx

    rep_mask_files = [x for x in mask_files for _ in range(int(calc_mask_repeats))]
    print("Done loading images.")
    print("--" * 20)
    # if two images provided, this handles flipping
    curr_carrier = 0

    # Handle fixation color changes.
    color_list = alternating_blocks(
        "red", "green", length=total_repeats, n_switches=number_of_rg_switches
    )

    # Run 'Begin Experiment' code from code
    wait_trigger = keyboard.Keyboard(deviceName="wait_trigger")
    text_3 = visual.TextStim(
        win=win,
        name="text_3",
        text="Scanner noises will begin soon,\n stimuli will appear shortly after",
        font="Arial",
        pos=(0, 0),
        draggable=False,
        height=40.0,
        wrapWidth=None,
        ori=0.0,
        color="white",
        colorSpace="rgb",
        opacity=None,
        languageStyle="LTR",
        depth=-2.0,
    )
    # --- Initialize components for Routine "retino_stim_loop" ---
    ret_stim_01 = visual.ImageStim(
        win=win,
        name="ret_stim_01",
        image="default.png",
        mask="sin",
        anchor="center",
        ori=0.0,
        pos=(0, 0),
        draggable=False,
        size=(1080, 1080),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=None,
        flipHoriz=False,
        flipVert=False,
        texRes=512.0,
        interpolate=True,
        depth=-1.0,
    )
    fixation_background = visual.ImageStim(
        win=win,
        name="fixation_background",
        image="default.png",
        mask=None,
        anchor="center",
        ori=0.0,
        pos=(0, 0),
        draggable=False,
        size=(1080, 1080),
        color=[1, 1, 1],
        colorSpace="rgb",
        opacity=0.2,
        flipHoriz=False,
        flipVert=False,
        texRes=128.0,
        interpolate=True,
        depth=-2.0,
    )
    polygon = visual.ShapeStim(
        win=win,
        name="polygon",
        size=(10, 10),
        vertices="circle",
        ori=0.0,
        pos=(0, 0),
        draggable=False,
        anchor="center",
        lineWidth=1.0,
        colorSpace="rgb",
        lineColor="white",
        fillColor="white",
        opacity=None,
        depth=-3.0,
        interpolate=True,
    )
    key_resp = keyboard.Keyboard(deviceName="key_resp")

    # create some handy timers

    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == "float":
            # get timestamps as a simple value
            globalClock = core.Clock(format="float")
        elif globalClock == "iso":
            # get timestamps in ISO format
            globalClock = core.Clock(format="%Y-%m-%d_%H:%M:%S.%f%z")
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo["expStart"] = data.getDateStr(
        format="%Y-%m-%d %Hh%M.%S.%f %z", fractionalSecondDigits=6
    )

    # --- Prepare to start Routine "wait_block" ---
    # create an object to store info about Routine wait_block
    wait_block = data.Routine(
        name="wait_block",
        components=[wait_trigger, text_3],
    )
    wait_block.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for wait_trigger
    wait_trigger.keys = []
    wait_trigger.rt = []
    _wait_trigger_allKeys = []
    # store start times for wait_block
    wait_block.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    wait_block.tStart = globalClock.getTime(format="float")
    wait_block.status = STARTED
    thisExp.addData("wait_block.started", wait_block.tStart)
    wait_block.maxDuration = None
    # keep track of which components have finished
    wait_blockComponents = wait_block.components
    for thisComponent in wait_block.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, "status"):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "wait_block" ---

    print(f"Scan duration will be {scan_duration:.2f} seconds.")
    print("--" * 20)
    print("READY FOR TRIGGER")
    wait_block.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *wait_trigger* updates
        waitOnFlip = False

        # if wait_trigger is starting this frame...
        if wait_trigger.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            wait_trigger.frameNStart = frameN  # exact frame index
            wait_trigger.tStart = t  # local t and not account for scr refresh
            wait_trigger.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(wait_trigger, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "wait_trigger.started")
            # update status
            wait_trigger.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(wait_trigger.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(
                wait_trigger.clearEvents, eventType="keyboard"
            )  # clear events on next screen flip
        if wait_trigger.status == STARTED and not waitOnFlip:
            theseKeys = wait_trigger.getKeys(
                keyList=["t", "5"], ignoreKeys=["escape"], waitRelease=False
            )
            _wait_trigger_allKeys.extend(theseKeys)
            if len(_wait_trigger_allKeys):
                wait_trigger.keys = _wait_trigger_allKeys[
                    -1
                ].name  # just the last key pressed
                wait_trigger.rt = _wait_trigger_allKeys[-1].rt
                wait_trigger.duration = _wait_trigger_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False

        # *text_3* updates

        # if text_3 is starting this frame...
        if text_3.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            text_3.frameNStart = frameN  # exact frame index
            text_3.tStart = t  # local t and not account for scr refresh
            text_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_3, "tStartRefresh")  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, "text_3.started")
            # update status
            text_3.status = STARTED
            text_3.setAutoDraw(True)

        # if text_3 is active this frame...
        if text_3.status == STARTED:
            # update params
            pass

        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, win=win, timers=[routineTimer], playbackComponents=[]
            )
            # skip the frame we paused on
            continue

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            wait_block.forceEnded = routineForceEnded = True
            break
        continueRoutine = (
            False  # will revert to True if at least one component still running
        )
        for thisComponent in wait_block.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if (
            continueRoutine
        ):  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "wait_block" ---
    for thisComponent in wait_block.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for wait_block
    wait_block.tStop = globalClock.getTime(format="float")
    wait_block.tStopRefresh = tThisFlipGlobal
    thisExp.addData("wait_block.stopped", wait_block.tStop)
    # check responses
    if wait_trigger.keys in ["", [], None]:  # No response was made
        wait_trigger.keys = None
    thisExp.addData("wait_trigger.keys", wait_trigger.keys)
    if wait_trigger.keys != None:  # we had a response
        thisExp.addData("wait_trigger.rt", wait_trigger.rt)
        thisExp.addData("wait_trigger.duration", wait_trigger.duration)
    thisExp.nextEntry()
    # the Routine "wait_block" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # set up handler to look after randomisation of conditions etc
    show_retino = data.TrialHandler2(
        name="show_retino",
        nReps=total_repeats,
        method="sequential",
        extraInfo=expInfo,
        originPath=-1,
        trialList=[None],
        seed=None,
    )
    thisExp.addLoop(show_retino)  # add the loop to the experiment
    thisShow_retino = show_retino.trialList[
        0
    ]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisShow_retino.rgb)
    if thisShow_retino != None:
        for paramName in thisShow_retino:
            globals()[paramName] = thisShow_retino[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()

    for thisShow_retino in show_retino:
        currentLoop = show_retino
        thisExp.timestampOnFlip(win, "thisRow.t", format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisShow_retino.rgb)
        if thisShow_retino != None:
            for paramName in thisShow_retino:
                globals()[paramName] = thisShow_retino[paramName]

        # --- Prepare to start Routine "retino_stim_loop" ---
        # create an object to store info about Routine retino_stim_loop
        retino_stim_loop = data.Routine(
            name="retino_stim_loop",
            components=[ret_stim_01, fixation_background, polygon, key_resp],
        )
        retino_stim_loop.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_2
        # select out 12 of the stimuli at once
        # this ensures that we have no repeates.

        # This 0 to 100 depends on how many images we have in carrier folder, right?
        stim_ixs = np.random.randint(low=0, high=num_images)
        # stim_ixs = np.random.randint(low=0, high=num_images, size=13).tolist()

        # mask_img = preloaded_masks.pop(0)

        # I think I did this because it had to be a file, not an array?
        # mask_img = f"./masks/mask{count:03d}.png"
        # mask_img =  # load directly below
        stim_color = color_list.pop()
        # Check if only 2 images provided
        # curr_carrier starts at 0
        if len(preloaded_images) == 2:
            ret_stim_01.setImage(preloaded_images[curr_carrier])
            curr_carrier = np.abs(curr_carrier - 1)
        else:
            ret_stim_01.setImage(preloaded_images[stim_ixs])
        ret_stim_01.setMask(os.path.join(mask_folder, rep_mask_files.pop(0)))
        fixation_background.setImage("background_radial_grid_v1.png")
        polygon.setFillColor(stim_color)
        polygon.setLineColor(stim_color)
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for retino_stim_loop
        retino_stim_loop.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        retino_stim_loop.tStart = globalClock.getTime(format="float")
        retino_stim_loop.status = STARTED
        thisExp.addData("retino_stim_loop.started", retino_stim_loop.tStart)
        retino_stim_loop.maxDuration = None
        # keep track of which components have finished
        retino_stim_loopComponents = retino_stim_loop.components
        for thisComponent in retino_stim_loop.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, "status"):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1

        # --- Run Routine "retino_stim_loop" ---
        # if trial has changed, end Routine now
        if (
            isinstance(show_retino, data.TrialHandler2)
            and thisShow_retino.thisN != show_retino.thisTrial.thisN
        ):
            continueRoutine = False
        retino_stim_loop.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < frame_dur:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *ret_stim_01* updates

            # if ret_stim_01 is starting this frame...
            if ret_stim_01.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                ret_stim_01.frameNStart = frameN  # exact frame index
                ret_stim_01.tStart = t  # local t and not account for scr refresh
                ret_stim_01.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(ret_stim_01, "tStartRefresh")  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "ret_stim_01.started")
                # update status
                ret_stim_01.status = STARTED
                ret_stim_01.setAutoDraw(True)

            # if ret_stim_01 is active this frame...
            if ret_stim_01.status == STARTED:
                # update params
                pass

            # if ret_stim_01 is stopping this frame...
            if ret_stim_01.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if (
                    tThisFlipGlobal
                    > ret_stim_01.tStartRefresh + frame_dur - frameTolerance
                ):
                    # keep track of stop time/frame for later
                    ret_stim_01.tStop = t  # not accounting for scr refresh
                    ret_stim_01.tStopRefresh = tThisFlipGlobal  # on global time
                    ret_stim_01.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, "ret_stim_01.stopped")
                    # update status
                    ret_stim_01.status = FINISHED
                    ret_stim_01.setAutoDraw(False)

            # *fixation_background* updates

            # if fixation_background is starting this frame...
            if (
                fixation_background.status == NOT_STARTED
                and tThisFlip >= 0.0 - frameTolerance
            ):
                # keep track of start time/frame for later
                fixation_background.frameNStart = frameN  # exact frame index
                fixation_background.tStart = (
                    t  # local t and not account for scr refresh
                )
                fixation_background.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(
                    fixation_background, "tStartRefresh"
                )  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "fixation_background.started")
                # update status
                fixation_background.status = STARTED
                fixation_background.setAutoDraw(True)

            # if fixation_background is active this frame...
            if fixation_background.status == STARTED:
                # update params
                pass

            # if fixation_background is stopping this frame...
            if fixation_background.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if (
                    tThisFlipGlobal
                    > fixation_background.tStartRefresh + frame_dur - frameTolerance
                ):
                    # keep track of stop time/frame for later
                    fixation_background.tStop = t  # not accounting for scr refresh
                    fixation_background.tStopRefresh = tThisFlipGlobal  # on global time
                    fixation_background.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, "fixation_background.stopped")
                    # update status
                    fixation_background.status = FINISHED
                    fixation_background.setAutoDraw(False)

            # *polygon* updates

            # if polygon is starting this frame...
            if polygon.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon.frameNStart = frameN  # exact frame index
                polygon.tStart = t  # local t and not account for scr refresh
                polygon.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon, "tStartRefresh")  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "polygon.started")
                # update status
                polygon.status = STARTED
                polygon.setAutoDraw(True)

            # if polygon is active this frame...
            if polygon.status == STARTED:
                # update params
                pass

            # if polygon is stopping this frame...
            if polygon.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon.tStartRefresh + frame_dur - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon.tStop = t  # not accounting for scr refresh
                    polygon.tStopRefresh = tThisFlipGlobal  # on global time
                    polygon.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, "polygon.stopped")
                    # update status
                    polygon.status = FINISHED
                    polygon.setAutoDraw(False)

            # *key_resp* updates
            waitOnFlip = False

            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, "tStartRefresh")  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, "key_resp.started")
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(
                    key_resp.clearEvents, eventType="keyboard"
                )  # clear events on next screen flip

            # if key_resp is stopping this frame...
            if key_resp.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if (
                    tThisFlipGlobal
                    > key_resp.tStartRefresh + frame_dur - frameTolerance
                ):
                    # keep track of stop time/frame for later
                    key_resp.tStop = t  # not accounting for scr refresh
                    key_resp.tStopRefresh = tThisFlipGlobal  # on global time
                    key_resp.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, "key_resp.stopped")
                    # update status
                    key_resp.status = FINISHED
                    key_resp.status = FINISHED
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(
                    keyList=["r", "g", "b", "y", "1", "2", "3", "4"],
                    ignoreKeys=["escape"],
                    waitRelease=False,
                )
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[
                        -1
                    ].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration

            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp,
                    win=win,
                    timers=[routineTimer],
                    playbackComponents=[],
                )
                # skip the frame we paused on
                continue

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                retino_stim_loop.forceEnded = routineForceEnded = True
                break
            continueRoutine = (
                False  # will revert to True if at least one component still running
            )
            for thisComponent in retino_stim_loop.components:
                if (
                    hasattr(thisComponent, "status")
                    and thisComponent.status != FINISHED
                ):
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if (
                continueRoutine
            ):  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # --- Ending Routine "retino_stim_loop" ---
        for thisComponent in retino_stim_loop.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for retino_stim_loop
        retino_stim_loop.tStop = globalClock.getTime(format="float")
        retino_stim_loop.tStopRefresh = tThisFlipGlobal
        thisExp.addData("retino_stim_loop.stopped", retino_stim_loop.tStop)
        # check responses
        if key_resp.keys in ["", [], None]:  # No response was made
            key_resp.keys = None
        show_retino.addData("key_resp.keys", key_resp.keys)
        if key_resp.keys != None:  # we had a response
            show_retino.addData("key_resp.rt", key_resp.rt)
            show_retino.addData("key_resp.duration", key_resp.duration)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if retino_stim_loop.maxDurationReached:
            routineTimer.addTime(-retino_stim_loop.maxDuration)
        elif retino_stim_loop.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-frame_dur)
        thisExp.nextEntry()

    # completed total_repeats repeats of 'show_retino'

    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()

    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment

    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + ".csv", delim="auto")
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.

    This function does NOT close the window or end the Python process - use `quit` for this.

    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip()
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.

    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip()
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # all we skip is this - left in as evidence - loop continues until canncel
    # terminate Python process
    # core.quit()


# if running this experiment as a script...
if __name__ == "__main__":
    # call all functions in order
    # Run the experiment until the user hits cancel on the expInfo dialog
    while True:
        expInfo = showExpInfoDlg(expInfo=expInfo)
        #  Because of loop, smash date back in
        expInfo["date|hid"] = data.getDateStr()

        thisExp = setupData(expInfo=expInfo)
        logFile = setupLogging(filename=thisExp.dataFileName)
        win = setupWindow(expInfo=expInfo)
        setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
        run(expInfo=expInfo, thisExp=thisExp, win=win, globalClock="float")
        saveData(thisExp=thisExp)
        quit(thisExp=thisExp, win=win)

        # When looping, we must reset some entries.
        expInfo.pop("date", None)
        expInfo.pop("psychopyVersion", None)
        expInfo.pop("expStart", None)
        expInfo.pop("frameRate", None)
        # Reload these lists - doesn't save selection, unfortunately.
        mask_subfolders, carrier_subfolders = get_subfolders(
            base_mask_folder, base_image_folder
        )
        expInfo["mask"] = mask_subfolders
        expInfo["carrier"] = carrier_subfolders

        # Increment run number
        _, _, saved_run_num, _, _ = load_previous_run_info()
        expInfo["run-"] = f"{saved_run_num:02d}"

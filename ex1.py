#!/usr/bin/env python

import sys
from geant4_pybind import *

class XXDetectorConstruction(G4VUserDetectorConstruction):
  """
  Simple model: a sphere with water in the box with air.
  """
 
  def __init__(self):
    super().__init__()
    self.fScoringVolume = None
 
  def Construct(self):
    nist = G4NistManager.Instance()

    envelop_x = 10*cm
    envelop_y = 10*cm
    envelop_z = 10*cm

    envelop_mat = nist.FindOrBuildMaterial("G4_AIR")

    sphere_rad = 7*cm
    mat = nist.FindOrBuildMaterial("G4_WATER")

    checkOverlaps = True

    world_x = 1.2*envelop_x
    world_y = 1.2*envelop_y
    world_z = 1.2*envelop_z

    sWorld = G4Box("World", 0.5*world_x, 0.5*world_y,
                   0.5*world_z)

    lWorld = G4LogicalVolume(sWorld, envelop_mat, "World")

    pWorld = G4PVPlacement(None, G4ThreeVector(),
                           lWorld, "World", None, False,
                           0, checkOverlaps)

    sSphere = G4Orb("Head", sphere_rad)
    lSphere = G4LogicalVolume(sSphere, mat, "Head")
    G4PVPlacement(None, G4ThreeVector(), lSphere,
                  "Head", lWorld, True, 0, checkOverlaps)

    self.fScoringVolume = lSphere

    return pWorld
 
ui = None
if len(sys.argv) == 1:
  ui = G4UIExecutive(len(sys.argv), sys.argv)

# Optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)

runManager.SetUserInitialization(XXDetectorConstruction())

# Physics list
physicsList = QBBC()
physicsList.SetVerboseLevel(1)

runManager.SetUserInitialization(physicsList)

# User action initialization
#runManager.SetUserInitialization(XXActionInitialization())

visManager = G4VisExecutive()
# G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
# visManager = G4VisExecutive("Quiet")
visManager.Initialize()

# Get the User Interface manager
UImanager = G4UImanager.GetUIpointer()

# # Process macro or start UI session
if ui == None:
  # batch mode
  command = "/control/execute "
  fileName = sys.argv[1]
  UImanager.ApplyCommand(command + fileName)
else:
  # interactive mode
  UImanager.ApplyCommand("/control/execute init_vis.mac")
  ui.SessionStart()

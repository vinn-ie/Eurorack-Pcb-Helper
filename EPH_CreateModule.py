import math
import wx
from pcbnew import *

# Eurorack defines
HP_MM = 5.08
FACEPLATE_HEIGHT_MM = 128.5
HORIZONTAL_EDGE_EXPANSION_MM = -3   # Horizontal edge expansion for rear pcb on each side
VERTICAL_EDGE_EXPANSION_MM = -14.5  # Vertical edge expansion for rear pcb on each side
FACEPLATE_MOUNT_HORIZONTAL_OFFSET_MM = 7.5
FACEPLATE_MOUNT_VERTICAL_OFFSET_MM = 3
M3_DIAMETER_MM = 3.2
PCB_MOUNT_HORIZONTAL_OFFSET_MM = 3
PCB_MOUNT_VERTICAL_OFFSET_MM = 3
# Aux origin
LOCAL_ORIG_X_MM = 50
LOCAL_ORIG_Y_MM = 40


class CreateModule():
    def __init__(self, input):
        # Load current board
        self.b = GetBoard()

        # User inputs
        self.hp = self._ConvertFloat(input["hp"])
        self.rad = self._ConvertFloat(input["rad"])
        self.mh_wdith = self._ConvertFloat(input["mh_w"])
        self.pcb_mh = self._ConvertFloat(input["pcb_mh"])

        # Derived variables
        self.std_width = math.floor(self.hp * HP_MM * 2) / 2  # Rounded down to nearest 0.5 mm
        self.pcb_width = self.std_width + 2*HORIZONTAL_EDGE_EXPANSION_MM
        self.std_height = FACEPLATE_HEIGHT_MM
        self.pcb_height = FACEPLATE_HEIGHT_MM + 2*VERTICAL_EDGE_EXPANSION_MM
        self.fp_orig = wxPointMM(LOCAL_ORIG_X_MM, LOCAL_ORIG_Y_MM)
        self.pcb_orig = wxPointMM(LOCAL_ORIG_X_MM - HORIZONTAL_EDGE_EXPANSION_MM, LOCAL_ORIG_Y_MM - VERTICAL_EDGE_EXPANSION_MM)

        # Declaration of segment/coordinate lists
        self.line_segments = []
        self.arc_segments = []
        self.fp_mh_coords  = []
        self.pcb_mh_coords = []

        # Create appropriate board
        if input["type"] == "Faceplate":
            self.CreateFaceplate()
        else:
            self.CreatePcb()

        if self.pcb_mh:
            # Create PCB mounting holes
            self._DefinePcbMounts(self.pcb_width, self.pcb_height)
            self._PlaceMounts(self.pcb_orig, self.pcb_mh_coords, 0)

        # Update UI
        Refresh()

    def _ConvertFloat(self, value):
        # Attempts float conversion, if box is empty this throws an exception
        # so we assign a value of 0.
        try:
            return float(value)
        except:
            return 0.0

    def _Deg2rad(self, deg):
        return (deg * math.pi / 180.0)

    def _DegSin(self, deg):
        return math.sin(self._Deg2rad(deg))

    def _DegCos(self, deg):
        return math.cos(self._Deg2rad(deg))
    
    def _DefineSegments(self, width, height, radius):
        # All coordinates are defined in local coordinates, they are adjusted using local_orig later.
        if not hasattr(self, 'line_segments'):
            self.line_segments = []
        if not hasattr(self, 'arc_segments'):
            self.arc_segments = []

        # Create list of straight line segments for board outline
        self.line_segments = [
            (wxPointMM(radius, 0), wxPointMM(width - radius, 0)),
            (wxPointMM(radius, height), wxPointMM(width - radius, height)),
            (wxPointMM(0, radius), wxPointMM(0, height - radius)),
            (wxPointMM(width, radius), wxPointMM(width, height - radius))
        ]

        # Create list of arc segments for board outline
        self.arc_segments = [
            (wxPointMM(radius, radius), -90),
            (wxPointMM(width - radius, radius), 0),
            (wxPointMM(radius, height - radius), 180),
            (wxPointMM(width - radius, height - radius), 90)
        ]

        return

    def _RoundedRectangle(self, local_orig):
        # Place straight segments
        for start, end in self.line_segments:
            segment = PCB_SHAPE(self.b)
            segment.SetShape(S_SEGMENT)
            segment.SetStart(VECTOR2I(start + local_orig))
            segment.SetEnd(VECTOR2I(end + local_orig))
            segment.SetLayer(Edge_Cuts)
            segment.SetWidth(FromMM(0.15))
            self.b.Add(segment)

        # Place arc segments
        for center, angle in self.arc_segments:
            arc = PCB_SHAPE(self.b)
            arc.SetShape(S_ARC)
            arc.SetCenter(VECTOR2I(center + local_orig))
            arc.SetStart(VECTOR2I(center + wxPointMM(self.rad * self._DegCos(angle), self.rad * self._DegSin(angle)) + local_orig))
            arc.SetArcAngleAndEnd(EDA_ANGLE(-90, DEGREES_T), True)  # Each corner is a quarter-circle
            arc.SetLayer(Edge_Cuts)
            arc.SetWidth(FromMM(0.15))
            self.b.Add(arc)

    def _DefineFaceplateMounts(self, width, height):
        if not hasattr(self, 'fp_mh_coords'):
            self.fp_mh_coords = []

        # Append the coordinates for each M3 mounting hole in the faceplate to the list
        self.fp_mh_coords.append(wxPointMM(0 + FACEPLATE_MOUNT_HORIZONTAL_OFFSET_MM, 0 + FACEPLATE_MOUNT_VERTICAL_OFFSET_MM))            # top left
        self.fp_mh_coords.append(wxPointMM(width - FACEPLATE_MOUNT_HORIZONTAL_OFFSET_MM, 0 + FACEPLATE_MOUNT_VERTICAL_OFFSET_MM))        # top right
        self.fp_mh_coords.append(wxPointMM(0 + FACEPLATE_MOUNT_HORIZONTAL_OFFSET_MM, height - FACEPLATE_MOUNT_VERTICAL_OFFSET_MM))       # bottom left
        self.fp_mh_coords.append(wxPointMM(width - FACEPLATE_MOUNT_HORIZONTAL_OFFSET_MM, height - FACEPLATE_MOUNT_VERTICAL_OFFSET_MM))   # bottom right


    def _DefinePcbMounts(self, width, height):
        if not hasattr(self, 'pcb_mh_coords'):
            self.pcb_mh_coords = []

        # Append the coordinates for each M3 mounting hole in the faceplate to the list
        self.pcb_mh_coords.append(wxPointMM(0 + PCB_MOUNT_HORIZONTAL_OFFSET_MM, 0 + PCB_MOUNT_VERTICAL_OFFSET_MM))            # top left
        self.pcb_mh_coords.append(wxPointMM(width - PCB_MOUNT_HORIZONTAL_OFFSET_MM, 0 + PCB_MOUNT_VERTICAL_OFFSET_MM))        # top right
        self.pcb_mh_coords.append(wxPointMM(0 + PCB_MOUNT_HORIZONTAL_OFFSET_MM, height - PCB_MOUNT_VERTICAL_OFFSET_MM))       # bottom left
        self.pcb_mh_coords.append(wxPointMM(width - PCB_MOUNT_HORIZONTAL_OFFSET_MM, height - PCB_MOUNT_VERTICAL_OFFSET_MM))   # bottom right


    def _PlaceMounts(self, local_orig, coords, hole_width):
        # Define elongated hole dimensions
        hole_length = M3_DIAMETER_MM + hole_width
        hole_width = M3_DIAMETER_MM

        for coord in coords:
            module = FOOTPRINT(self.b)
            module.SetPosition(VECTOR2I(coord + local_orig))
            self.b.Add(module)
            
            npth = PAD(module)
            npth.SetSize(VECTOR2I(wxSizeMM(hole_length, hole_width)))
            npth.SetShape(PAD_SHAPE_OVAL)
            npth.SetAttribute(PAD_ATTRIB_NPTH)
            npth.SetDrillSize(VECTOR2I(wxSizeMM(hole_length, hole_width)))
            npth.SetPosition(VECTOR2I(coord + local_orig))
            module.Add(npth)


    def CreateFaceplate(self):
        # OUTLINE
        self._DefineSegments(self.std_width, FACEPLATE_HEIGHT_MM, self.rad)
        self._RoundedRectangle(self.fp_orig)
        # MOUNT HOLES
        self._DefineFaceplateMounts(width=self.std_width, height=FACEPLATE_HEIGHT_MM)
        self._PlaceMounts(self.fp_orig, self.fp_mh_coords, self.mh_wdith)
        

    def CreatePcb(self):
        # OUTLINE
        self._DefineSegments(self.pcb_width, self.pcb_height, self.rad)
        self._RoundedRectangle(self.pcb_orig)



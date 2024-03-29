; Wait until the planner queue is empty
%wait

; Set user-defined variables

%global.state.SAFE_HEIGHT = -20 ; clear everything height(negative number, distance below Z limit)
;Following set probe location
%global.state.PROBE_X_LOCATION = -5; machine coordinates
%global.state.PROBE_Y_LOCATION = -867 ;machine coordinates
%global.state.PROBE_Z_LOCATION = -83   ;machine coordinates --> lower this (more negative) to start the probing closer to wasteboard

%global.state.PROBE_DISTANCE = 80
%global.state.PROBE_RAPID_FEEDRATE = 200 ;mm/min


%wait

; Keep a backup of current work position
%X0=posx, Y0=posy, Z0=posz

; Save modal state
%WCS = modal.wcs
%PLANE = modal.plane
%UNITS = modal.units
%DISTANCE = modal.distance
%FEEDRATE = modal.feedrate
%SPINDLE = modal.spindle
%COOLANT = modal.coolant

G21 ;metric
M5   ;Stop spindle
G90	;Absolute positioning

G53 G0 Z[global.state.SAFE_HEIGHT]
G53 X[global.state.PROBE_X_LOCATION] Y[global.state.PROBE_Y_LOCATION]
%wait

G53 Z[global.state.PROBE_Z_LOCATION]
G91
G38.2 Z-[global.state.PROBE_DISTANCE] F[global.state.PROBE_RAPID_FEEDRATE];fast probe(so it doesn't take forever)
G0 z2
G38.2 z-5 F40	;"dial-it-in" probes
G4 P.25
G38.4 z10 F20
G4 P.25
G38.2 z-2 F10
G4 P.25
G38.4 z10 F5
G4 P.25
G90
%global.state.TOOL_REFERENCE = posz	;establish a global tool reference work offset
%wait
(TOOL_REFERENCE = [global.state.TOOL_REFERENCE])

G91
G0 Z5
G90
G53 Z[global.state.SAFE_HEIGHT]
%wait
;Go to work zero at a SAFE_HEIGHT for Z
G0 X0 Y0
; Restore modal state
[WCS] [PLANE] [UNITS] [DISTANCE] [FEEDRATE] [SPINDLE] [COOLANT]

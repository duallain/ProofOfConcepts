;This macro allows you to use a fixed machine location for a tool change/probe. Ideal when you're workpiece surface has been carved away.

; Wait until the planner queue is empty
%wait

; Set user-defined variables

%SAFE_HEIGHT = -10 ; clear everything height(negative number, distance below Z limit)

%PROBE_DISTANCE = 100
%PROBE_RAPID_FEEDRATE = 200 ;mm/min


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


;Pause for manual tool change & probing
M0

G53 Z[global.state.PROBE_Z_LOCATION]
G91
G38.2 z-[global.state.PROBE_DISTANCE] F[global.state.PROBE_RAPID_FEEDRATE];fast probe (so it doesn't take forever)
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

%wait
; Update Z offset for new tool
G10 L20 Z[global.state.TOOL_REFERENCE]
%wait

G91
G0 Z5
G90
G53 Z[global.state.SAFE_HEIGHT]
%wait
;Go to work zero at a SAFE_HEIGHT for Z
G0 X0 Y0
; Restore modal state
[WCS] [PLANE] [UNITS] [DISTANCE] [FEEDRATE] [SPINDLE] [COOLANT]

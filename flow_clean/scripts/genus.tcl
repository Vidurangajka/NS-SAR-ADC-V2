# ==============================================================================
# scripts/genus.tcl - Synthesize controller for Sky130 9T
# ==============================================================================
set DESIGN "controller"
set PDK    "/home/user22/Sky130_cadence_pdk/sky130_scl_9T_0.1.1/sky130_scl_9T"

# 1. Search Paths and Target Libraries
set_db init_lib_search_path [list "$PDK/lib"]
set_db library              [list "sky130_tt_1.8_25_nldm.lib"]
set_db init_hdl_search_path [list "./rtl"]

# Prevent assignment statements in exported netlist
set_db remove_assigns true

# 2. Read and Elaborate RTL
read_hdl ${DESIGN}.v
elaborate $DESIGN

# 3. Apply Timing Constraints
read_sdc ./scripts/constraints.sdc

# Sanity check design
check_design -unresolved

# 4. Synthesis and Optimization
syn_generic
syn_map

# Ensure constants map to physical tie cells instead of floating logic 1/0
set_db [get_db lib_cells *TIE*] .avoid false
syn_opt

# 5. Export Gate Netlist and Signoff Timing Constraints
write_hdl -mapped > ./outputs/controller_netlist.v
write_sdc > ./outputs/controller.sdc

# 6. Reports
report_gates  > ./reports/gates.rpt
report_area   > ./reports/area.rpt
report_timing > ./reports/timing_synth.rpt

puts "=== SYNTHESIS COMPLETE: outputs/controller_netlist.v generated ==="
exit
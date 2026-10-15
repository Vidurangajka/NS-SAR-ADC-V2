##############################################################################################################
#####  
#####                                         PVS LVS COMPARISON
#####  
#####  Version                       :   16.10-p006
#####  NVN Run Start                 :   Sat Sep  5 17:46:26 2026
#####  ERC Summary File              :   controller.sum
#####  Extraction Report File        :   controller.rep
#####  Comparison Report File        :   controller.rep.cls
#####  Top Cell                      :   controller  <vs>  controller
#####  
#####                                :      @     @
#####                                :       @   @ 
#####                                :        @ @  
#####  Run Result                    :     MISMATCH
#####                                :        @ @  
#####                                :       @   @ 
#####                                :      @     @
#####  
#####  Run Summary                   :   [ERROR] Connectivity Mismatches
#####                                :   [ERROR] Parameter Mismatches
#####                                :   [WARN]  Top Cell Has Extra Pins
#####                                :   [INFO]  ERC Results: Empty
#####                                :   [INFO]  Extraction Clean
#####                                :   [INFO]  Some Sections Have Been Truncated
#####  
#####  Layout Design                 :   /home/user22/NS_SAR_ADC/flow_clean/lvs/controller.gds (gdsii)
#####  Layout File                   :   controller.net (cdl)
#####  Schematic File                :   /home/user22/NS_SAR_ADC/flow_clean/lvs/controller.cdl (cdl)
#####  Schematic File                :   /home/user22/Sky130_cadence_pdk/sky130_scl_9T_0.1.1/sky130_scl_9T/cdl/sky130_scl_9T.cdl (cdl)
#####  Rules File                    :   sky130.lvs.pvl
#####  Pin Swap File                 :   controller.rep.cps
#####  
#####  Extraction CPU Time           :   0h 0m 0s - (0s)
#####  Extraction Exec Time          :   0h 0m 0s - (0s)
#####  Extraction Peak Memory Usage  :   22.00MB
#####  NVN CPU Time                  :   0h 0m 0s - (0s)                 
#####  NVN Exec Time                 :   0h 0m 1s - (1s)                 
#####  NVN Peak Memory Usage         :   234.58MB
#####  LVS Total CPU Time            :   0h 0m 0s - (0s)                 
#####  LVS Total Exec Time           :   0h 0m 1s - (1s)                 
#####  LVS Total Peak Memory Usage   :   234.58MB
#####  
##############################################################################################################


##############################################################################################################
#
#                                            CELL MATCH STATISTICS                                            
#
##############################################################################################################

Cell Statistic Descriptions                  | Count
---------------------------------------------+----------
Cells matched                                |         0
Cells expanded                               |         0
Cells not run                                |         0
Cells which mismatch                         |         1
---------------------------------------------+----------
Total                                        |         1


Cell Statistic Detail                        | Count
---------------------------------------------+----------
Cells with parameter mismatches              |         1
Cells with mismatched instance subtypes      |         0
Cells that have been blackboxed              |         0


##############################################################################################################
#
#                                             CELL MATCH SUMMARY                                              
#
##############################################################################################################

               |     Initial Pins     |     Compare Pins     |              | 
Cell           |   lay    :    sch    |   lay    :    sch    | Status       | Detail
---------------+----------+-----------+----------+-----------+--------------+--------------------------
controller     |       *0 :       116 |       *0 :        55 | mismatch     | extra pins, truncated


##############################################################################################################
#
#                                                  LVS RULES                                                  
#
##############################################################################################################

Command Line LVS Rule Values
----------------------------

    layout_primary                          controller {-top_cell controller}

LVS Rules Given in the Rules File
---------------------------------

    lvs_abort                               -softchk                               no  
    lvs_abort                               -supply_error                          no  
    layout_path                             /home/user22/NS_SAR_ADC/flow_clean/lvs/controller.gds
    layout_format                           gdsii
    layout_format                           gdsii
    layout_primary                          TOPCELL
    schematic_path                          /home/user22/NS_SAR_ADC/flow_clean/lvs/controller.cdl
    schematic_path                          /home/user22/Sky130_cadence_pdk/sky130_scl_9T_0.1.1/sky130_scl_9T/cdl/sky130_scl_9T.cdl
    schematic_format                        cdl
    schematic_primary                       controller
    lvs_delete_cell_pin                     cap_vpp_02p4x04p6_m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_02p7x06p1_m1m2m3m4_shieldl1_fingercap b -source
    lvs_delete_cell_pin                     cap_vpp_02p7x11p1_m1m2m3m4_shieldl1_fingercap b -source
    lvs_delete_cell_pin                     cap_vpp_02p7x21p1_m1m2m3m4_shieldl1_fingercap b -source
    lvs_delete_cell_pin                     cap_vpp_02p7x41p1_m1m2m3m4_shieldl1_fingercap b -source
    lvs_delete_cell_pin                     cap_vpp_02p9x06p1_m1m2m3m4_shieldl1_fingercap2 b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_l1m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_l1m1m2_shieldpo_floatm3 b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_m1m2m3_shieldl1 b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_m1m2m3_shieldl1m5_floatm4 b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_m1m2_noshield_o2 b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_m1m2_shieldl1 b -source
    lvs_delete_cell_pin                     cap_vpp_05p9x05p9_m1m2m3m4_shieldl1_wafflecap b -source
    lvs_delete_cell_pin                     cap_vpp_06p8x06p1_l1m1m2m3_shieldpom4 b -source
    lvs_delete_cell_pin                     cap_vpp_06p8x06p1_m1m2m3_shieldl1m4 b -source
    lvs_delete_cell_pin                     cap_vpp_08p6x07p8_l1m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_08p6x07p8_l1m1m2_shieldpo_floatm3 b -source
    lvs_delete_cell_pin                     cap_vpp_08p6x07p8_m1m2m3_shieldl1 b -source
    lvs_delete_cell_pin                     cap_vpp_08p6x07p8_m1m2m3_shieldl1m5_floatm4 b -source
    lvs_delete_cell_pin                     cap_vpp_08p6x07p8_m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_08p6x07p8_m1m2_shieldl1 b -source
    lvs_delete_cell_pin                     cap_vpp_11p3x11p3_m1m2m3m4_shieldl1_wafflecap b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_l1m1m2m3m4_shieldm5 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_l1m1m2m3m4_shieldpom5 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_l1m1m2m3_shieldm4 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_l1m1m2m3_shieldpom4 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_l1m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_l1m1m2_shieldpom3 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m2m3m4_shieldm5 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m2m3_shieldl1 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m2m3_shieldl1m5_floatm4 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m2_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m2_shieldl1 b -source
    lvs_delete_cell_pin                     cap_vpp_11p5x11p7_m1m4_noshield b -source
    lvs_delete_cell_pin                     cap_vpp_04p4x04p6_l1m1m2_noshield top -source
    lvs_black_box                           cap_vpp_02p4x04p6_m1m2_noshield -black
    lvs_black_box                           cap_vpp_02p7x06p1_m1m2m3m4_shieldl1_fingercap -black
    lvs_black_box                           cap_vpp_02p7x11p1_m1m2m3m4_shieldl1_fingercap -black
    lvs_black_box                           cap_vpp_02p7x21p1_m1m2m3m4_shieldl1_fingercap -black
    lvs_black_box                           cap_vpp_02p7x41p1_m1m2m3m4_shieldl1_fingercap -black
    lvs_black_box                           cap_vpp_02p9x06p1_m1m2m3m4_shieldl1_fingercap2 -black
    lvs_black_box                           cap_vpp_04p4x04p6_l1m1m2_noshield -black
    lvs_black_box                           cap_vpp_04p4x04p6_l1m1m2_shieldpo_floatm3 -black
    lvs_black_box                           cap_vpp_04p4x04p6_m1m2m3_shieldl1 -black
    lvs_black_box                           cap_vpp_04p4x04p6_m1m2m3_shieldl1m5_floatm4 -black
    lvs_black_box                           cap_vpp_04p4x04p6_m1m2_noshield -black
    lvs_black_box                           cap_vpp_04p4x04p6_m1m2_noshield_o2 -black
    lvs_black_box                           cap_vpp_04p4x04p6_m1m2_shieldl1 -black
    lvs_black_box                           cap_vpp_05p9x05p9_m1m2m3m4_shieldl1_wafflecap -black
    lvs_black_box                           cap_vpp_06p8x06p1_l1m1m2m3_shieldpom4 -black
    lvs_black_box                           cap_vpp_06p8x06p1_m1m2m3_shieldl1m4 -black
    lvs_black_box                           cap_vpp_08p6x07p8_l1m1m2_noshield -black
    lvs_black_box                           cap_vpp_08p6x07p8_l1m1m2_shieldpo_floatm3 -black
    lvs_black_box                           cap_vpp_08p6x07p8_m1m2m3_shieldl1 -black
    lvs_black_box                           cap_vpp_08p6x07p8_m1m2m3_shieldl1m5_floatm4 -black
    lvs_black_box                           cap_vpp_08p6x07p8_m1m2_noshield -black
    lvs_black_box                           cap_vpp_08p6x07p8_m1m2_shieldl1 -black
    lvs_black_box                           cap_vpp_11p3x11p3_m1m2m3m4_shieldl1_wafflecap -black
    lvs_black_box                           cap_vpp_11p5x11p7_l1m1m2m3m4_shieldm5 -black
    lvs_black_box                           cap_vpp_11p5x11p7_l1m1m2m3m4_shieldpom5 -black
    lvs_black_box                           cap_vpp_11p5x11p7_l1m1m2m3_shieldm4 -black
    lvs_black_box                           cap_vpp_11p5x11p7_l1m1m2m3_shieldpom4 -black
    lvs_black_box                           cap_vpp_11p5x11p7_l1m1m2_noshield -black
    lvs_black_box                           cap_vpp_11p5x11p7_l1m1m2_shieldpom3 -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5 -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m2m3m4_shieldm5 -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m2m3_shieldl1 -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m2m3_shieldl1m5_floatm4 -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m2_noshield -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m2_shieldl1 -black
    lvs_black_box                           cap_vpp_11p5x11p7_m1m4_noshield -black
                                             
    lvs_cdn_flow_options                    -cdl_use_scale
                                             
    lvs_ignore_ports                        no  
    lvs_find_shorts                         no  
    lvs_break_ambig_max                     32
                                             
    lvs_reduce_split_gates                  no  
    lvs_recognize_gates                     -all
    lvs_recognize_gates                     -none
    lvs_recognize_gates                     -none
    lvs_reduce                              no  -series_mos
    lvs_reduce                              yes -parallel_mos
    lvs_reduce_device                       MN ( nfet_20v0 ) -parallel ...
    lvs_reduce_device                       MN ( nfet_20v0_zvt ) -parallel ...
    lvs_reduce_device                       MP ( pfet_20v0 ) -parallel ...
    lvs_reduce_device                       Q -parallel yes ...
    lvs_reduce_device                       C ( cap_mim_m3__base ) -parallel no 
                                             
    lvs_expand_cell_on_error                no  
                                             
    lvs_check_property                      D ( diode_pd2nw_05v5 ) a a -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_05v5 ) p p -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_05v5 ) a a -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_05v5 ) p p -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_05v5_hvt ) a a -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_05v5_hvt ) p p -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_05v5_lvt ) a a -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_05v5_lvt ) p p -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_11v0 ) a a -tolerance 1
    lvs_check_property                      D ( diode_pd2nw_11v0 ) p p -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_05v5_lvt ) a a -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_05v5_lvt ) p p -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_05v5_nvt ) a a -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_05v5_nvt ) p p -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_11v0 ) a a -tolerance 1
    lvs_check_property                      D ( diode_pw2nd_11v0 ) p p -tolerance 1
    lvs_check_property                      MN ( nfet_20v0 ) w w
    lvs_check_property                      MN ( nfet_20v0 ) l l
    lvs_check_property                      MN ( nfet_20v0_zvt ) w w
    lvs_check_property                      MN ( nfet_20v0_zvt ) l l
    lvs_check_property                      MP ( pfet_20v0 ) w w
    lvs_check_property                      MP ( pfet_20v0 ) l l
    lvs_check_property                      Q EA EA -tolerance 0
    lvs_check_property                      Q M M -tolerance 0
    lvs_check_property                      MP L l
    lvs_check_property                      MP W w
    lvs_check_property                      MN L l
    lvs_check_property                      MN W w
    lvs_check_property                      R W W
    lvs_check_property                      R L L
    lvs_check_property                      C L L
    lvs_check_property                      C W W
    lvs_report_file                         controller.rep
    lvs_report_max                          50 -mismatched_net_limit 100 
    lvs_short_equivalent_nodes              yes
    virtual_connect                         no  -colon
    virtual_connect                         yes -semicolon_as_colon
    virtual_connect                         no  -report
    virtual_connect                         -depth primary
                                             

Default LVS Rule Values
-----------------------

    layout_case_sensitive                   no
    // layout_cpf_file                       
    // schematic_cpf_file                    
    schematic_case_sensitive                no
    // hcell_file                            
    // hcell                                 
    // lvs_exclude_hcell                     
    lvs_push_devices                        yes
    lvs_push_devices_properties             no
    lvs_netlist                             yes -substrate_comment
    lvs_netlist                             yes -box_contents
    lvs_netlist                             yes -unnamed_box_pins
    lvs_netlist                             no -allow_inconsistent_model
    // lvs_write_netlist                     
    // lvs_write_netlist_reduced             
    lvs_spice                               yes -allow_floating_pins
    lvs_spice                               yes -allow_duplicate_subcircuit_names
    lvs_spice                               no  -conditional_ldd
    lvs_spice                               no  -prefer_pins
    lvs_spice                               no  -override_globals
    lvs_spice                               no  -redefine_param
    lvs_spice                               no  -replicate_devices
    lvs_spice                               yes -slash_is_space
    lvs_spice                               yes -keep_back_slash
    lvs_spice                               no  -allow_unquoted_strings
    lvs_spice                               no  -allow_inline_parameters
    lvs_spice                               no  -calculate_mos_area
    lvs_spice                               no  -strict_wl
    lvs_spice                               no  -cull_primitive_subcircuits
    lvs_spice                               no  -ignore_option_scale
    lvs_spice                               no  -show_neg_param_warning
    lvs_spice                               no  -scale_x_parameters
    // lvs_spice_option                      
    lvs_reverse_wl                          no
    // lvs_spice_multiplier_name             
                                             
    lvs_compare_case                        no
    lvs_cname                               no  -cell
    lvs_cname                               yes -pin
    lvs_cname                               yes -net
    lvs_cname                               no  -instance
    lvs_non_user_name                       -port "^[0-9]+$"
    lvs_non_user_name                       -net  "^[0-9]+$"
    // lvs_non_user_name                    -instance 
    lvs_out_of_range_exclude_zero           no
    // lvs_group_models                      
    lvs_strict_subtypes                     no
    // lvs_cpoint                            
    // lvs_power_name                        
    // lvs_ground_name                       
    // lvs_cell_list                         
    // lvs_device_type                       
                                             
    lvs_auto_pin_swap                       yes -swap_threshold 4000000
    lvs_swap_non_cpoint_pins                yes
    // lvs_swap_pins                         
    lvs_all_cap_pins_swappable              no
    lvs_builtin_device_pin_swap             yes
    // lvs_join_nets                         
    lvs_compare_port_names                  no
    lvs_global_sigs_are_ports               yes
    lvs_discard_pins                        no
                                             
    lvs_filter                              no  -bipolar
    lvs_filter                              no  -capacitors
    lvs_filter                              no  -diodes
    lvs_filter                              no  -mos
    lvs_filter                              no  -resistors
    // lvs_filter_option                     
    // lvs_filter_device                     
                                             
    lvs_reduction_priority                  -parallel
    lvs_derive_logic                        yes -sram
    lvs_derive_logic                        no  -dram
    lvs_derive_logic                        no  -rom
    // lvs_recognize_gates_tolerance         
    lvs_reduce                              yes -parallel_bipolar
    lvs_reduce                              yes -parallel_caps
    lvs_reduce                              yes -series_caps
    lvs_reduce                              yes -parallel_diodes
    lvs_reduce                              no  -series_diodes
    lvs_reduce                              yes -parallel_resistors
    lvs_reduce                              yes -series_resistors
    // lvs_reduce_do_not_merge               
                                             
    lvs_expand_on_device_climbing           no
    lvs_expand_unbalanced_cells             yes
                                             
    // lvs_property_map                      
    // lvs_transfer_property                 
    // lvs_report_opt                        
    lvs_report_units                        yes
    lvs_keep_data                           no
    lvs_keep_source_cells                   no
    lvs_create_match_db                     no
    // lvs_map_device                        
    unit                                    -length u
    unit                                    -resistance ohm
    unit                                    -capacitance pf
    lvs_verilog_bus_map_by_position         no
    lvs_verilog_keep_backslash              no
    lvs_do_not_normalize                    no
    // lvs_generic_device                    
    input_scale                             1000
    virtual_connect                         no  -colon
    virtual_connect                         yes -semicolon_as_colon
    // virtual_connect                      -name 
    virtual_connect                         no -report
    virtual_connect                         no -incremental
    lvs_preserve_parameterized_cells        no
    lvs_check_color                         no
    // lvs_schematic_color_path              
    // lvs_assign_conflict_layer             
    // lvs_conflict_layer_check             
    lvs_check_color_label                   no
    // lvs_preserve_cells                    
                                             

Effective LVS Rule Values
-------------------------

    lvs_swap_non_cpoint_pins                yes -unbound_pin_threshold 10000
    layout_primary                          controller
    lvs_recognize_gates                     -all
    virtual_connect                         no  -report


##############################################################################################################
#
#                                               CELL COMPARISON                                               
#
##############################################################################################################

                              ##################################################
                              #                                                #
                              #       ------->>> $ MISMATCH $ <<<-------       #
                              #                                                #
                              #          controller  <vs>  controller          #
                              #                                                #
                              #            CONNECTIVITY MISMATCHES             #
                              #              PARAMETER MISMATCHES              #
                              #                   EXTRA PINS                   #
                              #                                                #
                              ##################################################
                              # * Some sections truncated                      #
                              ##################################################

+===[controller]==============================================================================================
|                                                 STATISTICS                                                  
+=============================================================================================================


                   |        Original        |        Reduced        |     Unmatched     
Cell               |    lay     :    sch    |    lay    :    sch    |   lay   :   sch
-------------------+------------+-----------+-----------+-----------+---------+---------
MP [4 pins]        |            :           |           :           |         :         
 MP(PFET_01V8)     |     *1,209 :     1,024 |       576 :       576 |       1 :        1
 MP:ParMos2#1      |          - :         - |        64 :        64 |       0 :        0
 MP:SerMos2#1  .  .|.  .  .   - :.  .  .  - |.  .   134 :.  .   134 |.  .   0 :.  .  . 0
 MP:SerMos3#1      |          - :         - |        44 :        44 |       0 :        0
 MP:SerMos4#1  .  .|.  .  .   - :.  .  .  - |.  .  .  4 :.  .  .  4 |.  .   0 :.  .  . 0
 MP:SerMos5#1      |          - :         - |         4 :         4 |       0 :        0
 MP:SerMos6#1  .  .|.  .  .   - :.  .  .  - |.  .  .  2 :.  .  .  2 |.  .   0 :.  .  . 0
MN [4 pins]        |            :           |           :           |         :         
 MN(NFET_01V8) .  .|.  . *1,209 :.  . 1,024 |.  .   429 :.  .   429 |.  .   1 :.  .  . 1
 MN:ParMos2#1      |          - :         - |        33 :        33 |       0 :        0
 MN:SerMos2#1  .  .|.  .  .   - :.  .  .  - |.  .   179 :.  .   179 |.  .   0 :.  .  . 0
 MN:SerMos3#1      |          - :         - |        62 :        62 |       0 :        0
 MN:SerMos4#1      |          - :         - |         9 :         9 |       0 :        0
 MN:SerMos5#1      |          - :         - |         3 :         3 |       0 :        0
-------------------+------------+-----------+-----------+-----------+---------+---------
Total              |      2,418 :     2,048 |     1,543 :     1,543 |       2 :        2
===================+============+===========+===========+===========+=========+=========
Pins               |            :           |        *0 :        55 |      *0 :        1
Nets               |            :           |      *582 :       528 |       0 :        0
===================+============+===========+===========+===========+=========+=========

+===[controller]==============================================================================================
|                                      DEVICES REMOVED DURING REDUCTION                                       
+=============================================================================================================


                   |     Parallel      |      Series       |     Deleted Nets     
Cell               |   lay   :   sch   |   lay   :   sch   |    lay    :   sch
-------------------+---------+---------+---------+---------+-----------+----------
MP [4 pins]        |         :         |         :         |           :          
 MP(PFET_01V8)     |     185 :       - |       - :       - |         0 :         0
MN [4 pins]        |         :         |         :         |           :          
 MN(NFET_01V8)     |     185 :       - |       - :       - |         0 :         0
-------------------+---------+---------+---------+---------+-----------+----------

+===[controller]==============================================================================================
|                                                 EXTRA PINS                                                  
+====================================================================================================truncated

Side | Pins
-----+--------------------------------------------------------------------------------------------------------
Sch  | CLK_EN SAMPLE_N VREF_SEL_4_P[3] VREF_SEL_4_P[2] VREF_SEL_4_P[1] VREF_SEL_4_P[0] VREF_SEL_8_P[26]
     | VREF_SEL_8_P[25] VREF_SEL_8_P[24] VREF_SEL_8_P[22] VREF_SEL_8_P[20] VREF_SEL_8_P[19] VREF_SEL_8_P[18]
     | VREF_SEL_8_P[17] VREF_SEL_8_P[16] VREF_SEL_8_P[15] VREF_SEL_8_P[14] VREF_SEL_8_P[13] VREF_SEL_8_P[12]
     | VREF_SEL_8_P[11] VREF_SEL_8_P[10] VREF_SEL_8_P[9] VREF_SEL_8_P[8] VREF_SEL_8_P[7] VREF_SEL_8_P[6]
     | VREF_SEL_8_P[5] VREF_SEL_8_P[4] VREF_SEL_8_P[3] VREF_SEL_8_P[2] VREF_SEL_8_P[1] VREF_SEL_8_P[0]
     | VREF_SEL_1_N[1] VREF_SEL_4_N[3] VREF_SEL_4_N[2] VREF_SEL_4_N[1] VREF_SEL_4_N[0] VREF_SEL_8_N[26]
     | VREF_SEL_8_N[25] VREF_SEL_8_N[24] VREF_SEL_8_N[22] VREF_SEL_8_N[21] VREF_SEL_8_N[19] VREF_SEL_8_N[18]
     | VREF_SEL_8_N[17] VREF_SEL_8_N[16] VREF_SEL_8_N[15] VREF_SEL_8_N[14] VREF_SEL_8_N[13] VREF_SEL_8_N[12]
     | VREF_SEL_8_N[11]


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++ Section truncated to 50 issues, adjust this using the lvs_report_max rule +++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


+===[controller]==============================================================================================
|                                              SHORTS AND OPENS                                               
+=============================================================================================================
                                                
                                                
Layout Net: 102     | Schematic Net: FE_RN_2
====================+====================(sao 1)
       SHORT        | Schematic Pin: CLK_IN
====================+===========================


+===[controller]==============================================================================================
|                                            MISMATCHED INSTANCES                                             
+=============================================================================================================
                                                                                               
                                                                                               
Layout Inst : ** missing inst **           | Schematic Inst : XFE_OFC7_VREF_SEL_8_N_20/Mmn0
Layout Model:                              | Schematic Model: MN(NFET_01V8)
===========================================+=============================================(mi 1)
                                                                                               
                                                                                               
Layout Inst : ** missing inst **           | Schematic Inst : Xclk_out_buf/Mmp0
Layout Model:                              | Schematic Model: MP(PFET_01V8)
===========================================+=============================================(mi 2)
                                                                                               
                                                                                               
Layout Inst : X10/M0 @(225.340,6.570)      | Schematic Inst : ** missing inst **
Layout Model: MN(NFET_01V8)                | Schematic Model: 
===========================================+=============================================(mi 3)
                                                                                               
                                                                                               
Layout Inst : X10/M3 @(225.340,8.905)      | Schematic Inst : ** missing inst **
Layout Model: MP(PFET_01V8)                | Schematic Model: 
===========================================+=============================================(mi 4)
                                                                                               
                                                                                               
Layout Inst : X55/M0 @(117.700,23.130)     | Schematic Inst : Xclk_out_buf/Mmn0
Layout Model: MN(NFET_01V8)                | Schematic Model: MN(NFET_01V8)
===========================================+=============================================(mi 5)
Terminal: Layout Net                       | Terminal: Schematic Net
-------------------------------------------+---------------------------------------------------
G: 452                                     | ** FE_RN_1 **
** missing net **                          | G: CLK_IN
                                           | 
D: X55/13   .  .  .  .  .  .  .  .  .  .  .| ** XFE_OFC7_VREF_SEL_8_N_20/n0 **
** X10/13 **                               | D: Xclk_out_buf/net44
                                           | 
S: 4                                       | S: VSS
B: 4                                       | B: VSS


+===[controller]==============================================================================================
|                                       UNMATCHED SCHEMATIC PIN LABELS                                        
+=============================================================================================================

Labeled Schematic Pin     | Matched Layout Pin     | Matched Layout Net
--------------------------+------------------------+-----------------------
CLK1                      | ** missing pin **      | 280
CLK2                      | ** missing pin **      | 904
CLK3                      | ** missing pin **      | 903
EN  .  .  .  .  .  .  .  .| ** missing pin **  .  .| 549
RSTN                      | ** missing pin **      | 654
COMP_IN   .  .  .  .  .  .| ** missing pin **  .  .| 943
CLK_OUT                   | ** missing pin **      | 103
SA_EN  .  .  .  .  .  .  .| ** missing pin **  .  .| 168
VCM_CON                   | ** missing pin **      | 177
VCM_CON_N .  .  .  .  .  .| ** missing pin **  .  .| 178
PA_EN                     | ** missing pin **      | 148
PA_EN_N   .  .  .  .  .  .| ** missing pin **  .  .| 149
SAMPLE_P                  | ** missing pin **      | 655
VREF_SEL_1_P[1] .  .  .  .| ** missing pin **  .  .| 372
VREF_SEL_1_P[0]           | ** missing pin **      | 44
VREF_SEL_2_P .  .  .  .  .| ** missing pin **  .  .| 1
VREF_SEL_4_P[6]           | ** missing pin **      | 1427
VREF_SEL_4_P[5] .  .  .  .| ** missing pin **  .  .| 694
VREF_SEL_4_P[4]           | ** missing pin **      | 34
VREF_SEL_8_P[27]   .  .  .| ** missing pin **  .  .| 113
VREF_SEL_8_P[23]          | ** missing pin **      | 286
VREF_SEL_8_P[21]   .  .  .| ** missing pin **  .  .| 684
VREF_SEL_1_N[0]           | ** missing pin **      | 74
VREF_SEL_2_N .  .  .  .  .| ** missing pin **  .  .| 1309
VREF_SEL_4_N[6]           | ** missing pin **      | 1598
VREF_SEL_4_N[5] .  .  .  .| ** missing pin **  .  .| 1568
VREF_SEL_4_N[4]           | ** missing pin **      | 64
VREF_SEL_8_N[27]   .  .  .| ** missing pin **  .  .| 133
VREF_SEL_8_N[23]          | ** missing pin **      | 355
VREF_SEL_8_N[20]   .  .  .| ** missing pin **  .  .| 453
uo_out[7]                 | ** missing pin **      | 229
uo_out[6] .  .  .  .  .  .| ** missing pin **  .  .| 223
uo_out[5]                 | ** missing pin **      | 235
uo_out[4] .  .  .  .  .  .| ** missing pin **  .  .| 265
uo_out[3]                 | ** missing pin **      | 247
uo_out[2] .  .  .  .  .  .| ** missing pin **  .  .| 253
uo_out[1]                 | ** missing pin **      | 259
uo_out[0] .  .  .  .  .  .| ** missing pin **  .  .| 241
uio_out[7]                | ** missing pin **      | 382
uio_out[6]   .  .  .  .  .| ** missing pin **  .  .| 387
uio_out[5]                | ** missing pin **      | 392
uio_out[4]   .  .  .  .  .| ** missing pin **  .  .| 397
uio_out[3]                | ** missing pin **      | 402
uio_out[2]   .  .  .  .  .| ** missing pin **  .  .| 407
uio_out[1]                | ** missing pin **      | 412
uio_out[0]   .  .  .  .  .| ** missing pin **  .  .| 2039
uio_oe[7]                 | ** missing pin **      | 417
uio_oe[6] .  .  .  .  .  .| ** missing pin **  .  .| 422
uio_oe[5]                 | ** missing pin **      | 427
uio_oe[4] .  .  .  .  .  .| ** missing pin **  .  .| 432
uio_oe[3]                 | ** missing pin **      | 437
uio_oe[2] .  .  .  .  .  .| ** missing pin **  .  .| 442
uio_oe[1]                 | ** missing pin **      | 447
uio_oe[0]                 | ** missing pin **      | 377


+===[controller]==============================================================================================
|                                       MISMATCHED INSTANCE PARAMETERS                                        
+=============================================================================================================


                 Merged Instance Detail                  
=========+=====================+=========================
         |                     | 
Side     | Master Instance     | Instances
---------+---------------------+-----------------(midl 1)
Lay      | <X55/M7>            | X55/M7
         |                     +-------------------------
         |                     | X55/M2
         |                     +-------------------------
         |                     | X55/M3
         |                     +-------------------------
         |                     | X55/M4
         |                     +-------------------------
         |                     | X55/M5
         |                     +-------------------------
         |                     | X55/M6
         |                     +-------------------------
         |                     | X55/M8
         |                     +-------------------------
         |                     | X55/M9
---------+---------------------+-----------------(midl 2)
Lay      | <X55/M17>           | X55/M17
         |                     +-------------------------
         |                     | X55/M12
         |                     +-------------------------
         |                     | X55/M13
         |                     +-------------------------
         |                     | X55/M14
         |                     +-------------------------
         |                     | X55/M15
         |                     +-------------------------
         |                     | X55/M16
         |                     +-------------------------
         |                     | X55/M18
         |                     +-------------------------
         |                     | X55/M19
---------+---------------------+-----------------(midl 3)
Lay      | <X55/M10>           | X55/M10
         |                     +-------------------------
         |                     | X55/M11
---------+---------------------+-----------------(midl 4)
Lay      | <X10/M2>            | X10/M2
         |                     +-------------------------
         |                     | X10/M1
---------+---------------------+-----------------(midl 5)
Lay      | <X10/M4>            | X10/M4
         |                     +-------------------------
         |                     | X10/M5


Layout Instance                            | Schematic Instance                           |  Parameter Error  
-------------------------------------------+----------------------------------------------+------------(mip 1)
<X55/M7> @(120.710,23.130) MN(NFET_01V8)   | XFE_OFC7_VREF_SEL_8_N_20/Mmn1 MN(NFET_01V8)  |                   
w: 6.08 u                                  | W: 1.52 u                                    | 300%              
-------------------------------------------+----------------------------------------------+------------(mip 2)
<X55/M17> @(120.710,24.960) MP(PFET_01V8)  | XFE_OFC7_VREF_SEL_8_N_20/Mmp1 MP(PFET_01V8)  |                   
w: 9.04 u                                  | W: 2.26 u                                    | 300%              
-------------------------------------------+----------------------------------------------+------------(mip 3)
<X55/M10> @(117.700,24.960) MP(PFET_01V8)  | XFE_OFC7_VREF_SEL_8_N_20/Mmp0 MP(PFET_01V8)  |                   
w: 2.26 u                                  | W: 0.625 u                                   | 261.6%            
-------------------------------------------+----------------------------------------------+------------(mip 4)
<X10/M2> @(226.260,6.570) MN(NFET_01V8)    | Xclk_out_buf/Mmn1 MN(NFET_01V8)              |                   
w: 1.52 u                                  | W: 6.08 u                                    | 75%               
-------------------------------------------+----------------------------------------------+------------(mip 5)
<X10/M4> @(225.830,8.400) MP(PFET_01V8)    | Xclk_out_buf/Mmp1 MP(PFET_01V8)              |                   
w: 2.26 u                                  | W: 9.04 u                                    | 75%               


##############################################################################################################
#
#                                                END OF REPORT                                                
#
##############################################################################################################


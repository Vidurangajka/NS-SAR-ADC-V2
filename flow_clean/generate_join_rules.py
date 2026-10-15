import re
import os
import sys

assign_text = """
assign VREF_SEL_8_N[6] = FE_RN_2 ;
assign VREF_SEL_8_N[7] = FE_RN_2 ;
assign FE_RN_1 = FE_RN_2 ;
assign VREF_SEL_8_N[4] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[5] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[8] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[9] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[18] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[19] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[22] = VREF_SEL_8_N[23] ;
assign VREF_SEL_8_N[0] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[1] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[2] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[3] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[10] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[11] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[12] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[13] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[14] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[15] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[16] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[17] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[24] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[25] = VREF_SEL_8_N[27] ;
assign VREF_SEL_8_N[26] = VREF_SEL_8_N[27] ;

assign VREF_SEL_8_P[6] = VREF_SEL_8_P[21] ;
assign VREF_SEL_8_P[7] = VREF_SEL_8_P[21] ;
assign VREF_SEL_8_P[20] = VREF_SEL_8_P[21] ;
assign VREF_SEL_8_P[4] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[5] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[8] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[9] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[18] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[19] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[22] = VREF_SEL_8_P[23] ;
assign VREF_SEL_8_P[0] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[1] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[2] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[3] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[10] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[11] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[12] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[13] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[14] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[15] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[16] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[17] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[24] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[25] = VREF_SEL_8_P[27] ;
assign VREF_SEL_8_P[26] = VREF_SEL_8_P[27] ;

assign VREF_SEL_4_N[1] = VREF_SEL_4_N[5] ;
assign VREF_SEL_4_N[0] = VREF_SEL_4_N[6] ;
assign VREF_SEL_4_N[2] = VREF_SEL_4_N[6] ;
assign VREF_SEL_4_N[3] = VREF_SEL_4_N[6] ;

assign VREF_SEL_4_P[1] = VREF_SEL_4_P[5] ;
assign VREF_SEL_4_P[0] = VREF_SEL_4_P[6] ;
assign VREF_SEL_4_P[2] = VREF_SEL_4_P[6] ;
assign VREF_SEL_4_P[3] = VREF_SEL_4_P[6] ;

assign VREF_SEL_1_N[1] = SAMPLE_P ;
assign SAMPLE_N = SAMPLE_P ;
assign CLK_EN = EN ;
assign VREF_SEL_8_N[21] = VREF_SEL_8_N[20] ;
"""

# --------------------------------------------------
# Build alias map
# --------------------------------------------------

alias_map = {}

for line in assign_text.strip().splitlines():
    match = re.search(
        r'assign\s+([^\s=]+)\s*=\s*([^\s;]+)',
        line
    )

    if match:
        target = match.group(1)
        source = match.group(2)
        alias_map[target] = source


# --------------------------------------------------
# Resolve alias chains
# --------------------------------------------------

def get_root(net):
    visited = set()

    while net in alias_map and net not in visited:
        visited.add(net)
        net = alias_map[net]

    return net


final_map = {}

for target in alias_map:
    final_map[target] = get_root(target)


# --------------------------------------------------
# Check input CDL
# --------------------------------------------------

input_cdl = "outputs/controller.cdl"

if not os.path.isfile(input_cdl):
    print("")
    print("ERROR: CDL file not found:")
    print("  " + os.path.abspath(input_cdl))
    print("")
    print("Current directory:")
    print("  " + os.getcwd())
    print("")
    sys.exit(1)


# --------------------------------------------------
# Generate LVS_JOIN_NETS rules
# --------------------------------------------------

join_cmds = []

for target, source in final_map.items():

    if target != source:

   

                t
                source
           
        )


# --------------------
# Write output
# ---------

output_file = "lvs/join_assigns.rul"

with
    f.writelines(join_cmds)


# -----------
# Report
# --------------------------------

print("")
print("=========================
print(" LVS JOIN NET GENERATION")
print("===
print("Input CDL : " + os.path.abspath(input
print("Output RUL: " + os.path.abspath(outpu
print("Rules     : {}".format(len(join_cmds
print("====================================
print("")
print("Generated successfully.")



# Print generated rules
print("First 10 g
print("-------------------------------------

for line in join_cmds[:10]:
    print(line.

print("------------------------------------
print("")

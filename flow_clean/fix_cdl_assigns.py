import re

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

# 1. Create a dictionary of alias replacements
alias_map = {}
for line in assign_text.strip().splitlines():
    m = re.search(r'assign\s+([^\s=]+)\s*=\s*([^\s;]+)', line)
    if m:
        target, source = m.group(1), m.group(2)
        alias_map[target] = source

# Resolve chains (e.g. A = B and B = C -> A = C)
def get_root(net):
    visited = set()
    while net in alias_map and net not in visited:
        visited.add(net)
        net = alias_map[net]
    return net

final_map = {k: get_root(k) for k in alias_map}

# Read original CDL file
input_cdl = "lvs/controller.cdl"
with open(input_cdl, "r") as f:
    content = f.read()

# Generate LVS_JOIN_NETS commands for pvslvsctl
join_cmds = []
for target, source in final_map.items():
    if target != source:
        join_cmds.append(f'LVS_JOIN_NETS "{target}" "{source}";\n')

with open("lvs/join_assigns.rul", "w") as f:
    f.writelines(join_cmds)

print(f"Generated {len(join_cmds)} LVS_JOIN_NETS rules in lvs/join_assigns.rul!")
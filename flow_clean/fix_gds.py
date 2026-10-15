import struct

gds_file = "outputs/controller.gds"
metal_layer_map = {"met1": 68, "met2": 69, "met3": 70, "met4": 71}

def make_gds_box(layer, datatype, x1_um, y1_um, x2_um, y2_um):
    x1, y1 = int(round(x1_um * 1000)), int(round(y1_um * 1000))
    x2, y2 = int(round(x2_um * 1000)), int(round(y2_um * 1000))
    rec = bytearray()
    rec += struct.pack(">HH", 4, 0x0800)          # BOUNDARY
    rec += struct.pack(">HHh", 6, 0x0D02, layer)  # LAYER
    rec += struct.pack(">HHh", 6, 0x0E02, datatype) # DATATYPE
    coords = [x1, y1, x2, y1, x2, y2, x1, y2, x1, y1]
    rec += struct.pack(">HH", 4 + len(coords)*4, 0x1003)
    for c in coords:
        rec += struct.pack(">i", c)
    rec += struct.pack(">HH", 4, 0x1100)          # ENDEL
    return rec

def make_gds_text(name, layer, texttype, x_um, y_um):
    x_dbu, y_dbu = int(round(x_um * 1000)), int(round(y_um * 1000))
    str_bytes = name.encode('ascii')
    if len(str_bytes) % 2 != 0:
        str_bytes += b'\x00'
    rec = bytearray()
    rec += struct.pack(">HH", 4, 0x0C00)          # TEXT
    rec += struct.pack(">HHh", 6, 0x0D02, layer)  # LAYER
    rec += struct.pack(">HHh", 6, 0x1602, texttype) # TEXTTYPE
    rec += struct.pack(">HHh", 6, 0x1701, 0)      # PRESENTATION
    rec += struct.pack(">HHii", 12, 0x1003, x_dbu, y_dbu) # XY
    rec += struct.pack(">HH", 4 + len(str_bytes), 0x1906) + str_bytes # STRING
    rec += struct.pack(">HH", 4, 0x1100)          # ENDEL
    return rec

with open(gds_file, "rb") as f:
    data = bytearray(f.read())

str_idx = data.find(b"\x06\x06controller")
if str_idx == -1:
    str_idx = data.find(b"controller")
endstr_idx = data.find(b"\x00\x04\x07\x00", str_idx)

# 1. Scan controller cell elements and clone DataType 16 -> DataType 20
duplicated_drawing_polygons = bytearray()
i = str_idx
clone_count = 0

while i < endstr_idx:
    reclen, rectype = struct.unpack(">HH", data[i:i+4])
    if rectype == 0x0800:
        el_start = i
        el_end = i + reclen
        curr = el_end
        el_layer = None
        el_datatype = None
        
        while curr < endstr_idx:
            slen, stype = struct.unpack(">HH", data[curr:curr+4])
            if stype == 0x0D02:
                el_layer = struct.unpack(">h", data[curr+4:curr+6])[0]
            elif stype == 0x0E02:
                el_datatype = struct.unpack(">h", data[curr+4:curr+6])[0]
            curr += slen
            if stype == 0x1100:
                el_end = curr
                break
                
        if el_layer in [68, 69, 70, 71] and el_datatype == 16:
            element_copy = bytearray(data[el_start:el_end])
            p = 0
            while p < len(element_copy):
                sub_len, sub_type = struct.unpack(">HH", element_copy[p:p+4])
                if sub_type == 0x0E02:
                    struct.pack_into(">h", element_copy, p+4, 20)
                    break
                p += sub_len
            duplicated_drawing_polygons += element_copy
            clone_count += 1
            
        i = el_end
        continue
    i += reclen

print(f"Cloned {clone_count} pin polygons (DT 16) directly to drawing polygons (DT 20).")

# 2. Met2 Vertical Stripes + Via1 Cuts
extra_bytes = bytearray()
vdd_xs = [30.0, 90.0, 150.0, 210.0]
vss_xs = [31.0, 91.0, 151.0, 211.0]

for x in vdd_xs:
    extra_bytes += make_gds_box(69, 20, x - 0.24, 1.64, x + 0.24, 26.88)
for x in vss_xs:
    extra_bytes += make_gds_box(69, 20, x - 0.24, 1.64, x + 0.24, 26.88)

for x in vdd_xs:
    for y in [1.84, 10.12, 18.40, 26.68]:
        extra_bytes += make_gds_box(68, 44, x - 0.08, y - 0.08, x + 0.08, y + 0.08)

for x in vss_xs:
    for y in [5.98, 14.26, 22.54]:
        extra_bytes += make_gds_box(68, 44, x - 0.08, y - 0.08, x + 0.08, y + 0.08)

# 3. Pin text labels from pin_exact_boxes.txt
with open("pin_exact_boxes.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 4: continue
        name, layer, cx, cy = parts[0], parts[1], float(parts[2]), float(parts[3])
        glayer = metal_layer_map.get(layer, 69)
        extra_bytes += make_gds_text(name, glayer, 5, cx, cy)
        extra_bytes += make_gds_text(name, glayer, 16, cx, cy)

# 4. Power Port labels on Met2 stripes
for x in vdd_xs:
    extra_bytes += make_gds_tex
    extra_bytes += make_gds_text("VDD", 69, 16, x, 25.0)

for x
    extra_bytes += make_gds_text("VSS", 69, 5, x, 25.0)
    ext

modified_data = data
with open(gds_file, "wb") as f:
    f.write(modified_data)



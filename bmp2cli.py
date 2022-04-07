import sys, struct

def read_rows(path):
    image_file = open(path, "rb")
    header = image_file.read(54)
    header_data = struct.unpack('<2sIHHIIIIHHIIIIII', header) #https://stackoverflow.com/a/68141863 , https://en.wikipedia.org/wiki/BMP_file_format#Bitmap_file_header
   # print(header_data)

    width=header_data[6]
    height=header_data[7]
    bitdepth=header_data[9]
    numpixels=width*height
    numSubpixels=bitdepth/8
    #image_file.seek(54)


    # We need to read pixels in as rows to later swap the order
    # since BMP stores pixels starting at the bottom left.
    rows = []
    row = []
    pixel_index = 0

    while True:
        if pixel_index == width:
            pixel_index = 0
            rows.insert(0, row)
            if len(row) != width * 3:
                raise Exception(f"Row length is not {width}*3 but {len(row)} / 3.0 = {len(row) / 3.0}")
            row = []
        pixel_index += 1

        b_string = image_file.read(1)
        g_string = image_file.read(1)
        r_string = image_file.read(1)



        if len(r_string) == 0:
            # This is expected to happen when we've read everything.
            if len(rows) != width:
                print(f"Warning!!! Read to the end of the file at the correct sub-pixel (red) but we've not read {width} rows!")
            break

        if len(g_string) == 0:
            print("Warning!!! Got 0 length string for green. Breaking.")
            break

        if len(b_string) == 0:
            print("Warning!!! Got 0 length string for blue. Breaking.")
            break

        r = ord(r_string)
        g = ord(g_string)
        b = ord(b_string)

        row.append(r)
        row.append(g)
        row.append(b)

    image_file.close()

    return rows,width,height

def repack_sub_pixels(rows):
    print( "Repacking pixels...")
    sub_pixels = []
    for row in rows:
        for sub_pixel in row:
            sub_pixels.append(sub_pixel)

    diff = len(sub_pixels) - width * height * 3
    print(f"Packed {len(sub_pixels)} sub-pixels.")
    if diff != 0:
        print(f"Error! Number of sub-pixels packed does not match {width}*{height}: ({len(sub_pixels)} - 1920 * 1080 * 3 = {diff})")

    reds=sub_pixels[::3]
    greens=sub_pixels[1::3]
    blues=sub_pixels[2::3]
    return reds,greens,blues

def print_in_color(txt_msg, r,g,b):
    # Prints the text_msg in the foreground color specified by fore_tuple with the background specified by back_tuple
    # text_msg is the text, fore_tuple is foreground color tuple (r,g,b), back_tuple is background tuple (r,g,b)
    rf,bf,gf = r,b,g
    #rb,gb,bb = (0,0,0)
    msg = '{0}' + txt_msg
    #mat = '\33[38;2;' + str(rf) + ';' + str(gf) + ';' + str(bf) + ';48;2;' + str(rb) + ';' +str(gb) + ';' + str(bb) + 'm'
    mat = f'\33[38;2;{rf};{gf};{bf};48;2;0;0;0m'
    print(msg.format(mat),end='')
    #return msg.format(mat)

def getColourChar(char, r,g,b):
    # Prints the text_msg in the foreground color specified by fore_tuple with the background specified by back_tuple
    # text_msg is the text, fore_tuple is foreground color tuple (r,g,b), back_tuple is background tuple (r,g,b)
    rf,bf,gf = r,b,g
    #rb,gb,bb = (0,0,0)
    msg = '{0}' + char
    #mat = '\33[38;2;' + str(rf) + ';' + str(gf) + ';' + str(bf) + ';48;2;' + str(rb) + ';' +str(gb) + ';' + str(bb) + 'm'
    mat = f'\33[38;2;{rf};{gf};{bf};48;2;0;0;0m'
    #print(msg.format(mat),end='')
    return msg.format(mat)



if __name__ == "__main__":

    if len(sys.argv)>1:
        filename=str(sys.argv[1])
    else:
        filename = "hopper.bmp"
    print(f'Reading {filename}')

    #rows = read_rows("face.bmp")
    rows,width,height = read_rows(filename)
    reds,greens,blues = repack_sub_pixels(rows)

    #for index, elem in enumerate(reds):
    printRow=''
    for index in range(width*height):
        r = reds[index] #r = elem
        g = greens[index]
        b = blues[index]

        printRow += getColourChar('X',r,g,b)

        if index%(width)==0:
            print(printRow)
            printRow=''
            pass


    print('\33[0m') # Returns default print color to back to black

file = r"stereomick.ogg"

# Opens the file
with open(file, 'rb') as mick:
    # Initialize variables
    reverse_endian = []
    output_end = []
    data_saved = []
    oggs_buffer = bytearray(4)  # Initialize a buffer for "OggS"
    final_data = ""

    while True:
        byte = mick.read(1)
        if not byte:
            # End of file
            break

        # Append the byte to the buffer and remove the oldest byte if necessary
        oggs_buffer.append(byte[0])
        oggs_buffer.pop(0)

        # Check if the buffer contains "OggS"
        if oggs_buffer == b'OggS':
            off_mover = mick.tell()
            off_mover += 2
            mick.seek(off_mover)

            # Read the reversed section (4 bytes)
            reverse_endian_entry = mick.read(4).hex()

            off_mover = mick.tell()
            off_mover += 18
            mick.seek(off_mover)

            # Initialize data_saved_entry
            data_saved_entry = ""

            # Read until the next "OggS" or end of file
            while True:
                next_byte = mick.read(1)
                if not next_byte:
                    break
                data_saved_entry += next_byte.hex()

                # Check if the last four bytes contain "OggS" (prevents premature interruption)
                if len(oggs_buffer) == 4:
                    oggs_buffer.pop(0)  # Remove the oldest byte
                oggs_buffer.append(next_byte[0])

                if oggs_buffer == b'OggS':
                    data_saved_entry = data_saved_entry[0:-8]
                    break


            # Append the collected data
            reverse_endian.append(reverse_endian_entry)
            data_saved.append(data_saved_entry)

    #print(reverse_endian)
    #print(data_saved)

    # Assuming reverse_endian is a list of hexadecimal strings
    # this is hardcoded, which is not recommended, but I'm goofing off a bit here.
    for items in reverse_endian:
        items_split_1 = items[0:2]
        items_split_2 = items[2:4]
        items_split_3 = items[4:6]
        items_split_4 = items[6:8]
        reversed_items = items_split_4 + items_split_3 + items_split_2 + items_split_1
        output_end.append(reversed_items)

    #print(output_end)

    exclusion = 0
    # Now you have output_end and data_saved lists with collected data
    if len(data_saved) != len(output_end):
        print("An error has occurred where the data saved is not the same length as the output end list. Please check the file.")
    else:
        #rebuild file
        for packets in range (exclusion, len(data_saved)):
            current_endian = output_end[packets]
            #print(current_endian)
            current_data = data_saved[packets]
            #print(current_data)
            #add an int16 describing audio data length
            data_length = int(len(current_data) / 2)
            int16_hex = format(data_length & 0xFFFF, '04X')
            print("hex length of packet", int16_hex)
            data_now = int16_hex + current_endian + current_data
            print("data packet number, packet intro:", packets, int16_hex+current_endian)
            final_data = final_data + data_now

    #print(current_endian)
    #print(current_data)
    #print(final_data)



# 4F 67 67 53 (OggS) this is what we need to find in the file and collect everything between it
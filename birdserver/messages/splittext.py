def split_text(string, font, width):
    out = []

    for s in string.split('\n'):
        space_pos = 0
        start_posn = 0
        end_posn = 0
        test_posn = 0
        while start_posn < len(s):
            space_pos = s.find(' ', test_posn)
            if space_pos == -1:
                test_posn = len(s)
            else:
                test_posn = space_pos

            test_str = s[start_posn:test_posn]
            test_len = font.getsize(test_str)
            if test_len[0] > width:
                line = s[start_posn:end_posn]
                out.append(line.strip())
                start_posn = end_posn
            elif test_len[0] <= width and space_pos == -1:
                line = s[start_posn:]
                out.append(line.strip())
                start_posn = len(s)
            end_posn = test_posn
            test_posn += 1

            print end_posn, len(s)

    return out

# XXX: Let's try the pigeon message this time!

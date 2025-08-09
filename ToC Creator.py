

import os
import sys


"""
Run through file
when encountering #'s
keep track of how deep we are
keep track of the amount of headlines we have had with that level so we can number them

when getting less deep, set amount of that level to 0

When going deeper place 4 * Depth of indents


"""


FILE_PATH : str = "/home/moose/Desktop/teaching_git/git notes.md"
A_INDENT : str = "    " # Use this to decide how many spaces or tabs you want :3

def main_function():

    if not ( os.path.isfile(FILE_PATH) ):

        if FILE_PATH == "":
            print("Ehhh... mate, the FILE_PATH variable is empty...")
        else:
            print(f"The argument {FILE_PATH} does not appear to be the path to a file")

    table_of_content : str = __harvest_from_file(FILE_PATH)


    temp_file = open(FILE_PATH + "_temp", "w")
    temp_file.write(table_of_content)

    with open(FILE_PATH, "r") as file:
        for line in file:
            temp_file.write(line)

    temp_file.close()


    os.remove(FILE_PATH) 
    os.rename(FILE_PATH + "_temp", FILE_PATH) 


def __harvest_from_file(file_path : str) -> str:
    table_of_content : str = "\n\n\n\n# Table of Content:\n\n"

    title_counters : dict[int, int] = dict()

    # Lists lenght represents depth. The numbers the amount of hashtags that created it
    # This is so we account for not always starting at #. We may start at ###
    # And we may skip some so we go from ## to ####
    sub_headline_depth : list[int] = []


    current_hashtag_depth : int = 0


    with open(FILE_PATH, "r") as file:
        for line in file:

            if not line.startswith("#"):
                continue

            words : list[str] = line.split(" ")
            first_word : str = words[0]

            if not __line_only_contains( first_word, "#" ):
                print("Weird line:")
                print(line)
                continue



            if current_hashtag_depth < len(first_word): # Going down
                current_hashtag_depth = len(first_word)
                sub_headline_depth.append( current_hashtag_depth )
                
                headline : str = __create_headline(1, words[1:], len(sub_headline_depth)-1)
                title_counters[current_hashtag_depth] = 2 # We just wrote 1

                table_of_content += headline
                
            elif current_hashtag_depth > len(first_word): # Going up
                current_hashtag_depth = len(first_word)

                while sub_headline_depth[ len(sub_headline_depth)-1 ] > current_hashtag_depth:
                    sub_headline_depth.pop()
                    if len(sub_headline_depth) == 0: # This means we have gone higher than ever before
                        sub_headline_depth.append( current_hashtag_depth )
                        title_counters[current_hashtag_depth] = 1

                headline : str = __create_headline(title_counters[current_hashtag_depth], words[1:], len(sub_headline_depth)-1)
                title_counters[current_hashtag_depth] += 1

                table_of_content += headline


            else: # Meaning we are on the same hashtag amount as last
                headline : str = __create_headline( title_counters[current_hashtag_depth]  , words[1:], len(sub_headline_depth)-1 )
                title_counters[current_hashtag_depth] += 1
                table_of_content += headline


    table_of_content.__add__("\n\n\n")
    return table_of_content





def __line_only_contains( line : str, symbol: str) -> bool:
    if len(symbol) != 1:
        print("the symbol argument may only be 1 character" )
        sys.exit(-1)

    return line.count( symbol ) == len(line)





def __create_headline(number : int, words_to_write : list[str], indents : int ):

    title : str = ""

    for word in words_to_write:
        cleanen_word = word.strip()
        title += f"{cleanen_word} "

    title = title[:-1] # Remove last space

    title = title.strip("*")
    title = title.strip(":")

    endcoded_title : str = title.replace(" ", "-")

    total_indent : str = ""
    for _ in range( indents ):
        total_indent += A_INDENT

    # Looks like this:
    # 2. [To delete a remote branch](#To-delete-a-remote-branch)
    return f"{total_indent}{number}. [{title}](#{endcoded_title})\n"





if __name__ == "__main__":
    print("")
    main_function()
    print("")
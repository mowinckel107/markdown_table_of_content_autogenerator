

import os
import sys




A_INDENT : str = "   " # Use this to decide how many spaces or tabs you want :3

def main_function():

    if len(sys.argv) < 2:
        print("Need to give the script a path to the file you want to create a Table of Content for")
        exit(0)

    user_input = sys.argv[1]

    if not ( os.path.isfile(user_input) ):

        if user_input == "":
            print("Ehhh... mate, the user_input variable is empty...")
            sys.exit(-1)
        else:
            print(f"The argument user_input({user_input}) does not appear to be the path to a file")
            sys.exit(-1)

    table_of_content : str = __harvest_from_file(user_input)


    temp_file = open(user_input + "_temp", "w", encoding="utf-8")
    temp_file.write(table_of_content)

    with open(user_input, "r", encoding="utf-8") as file:
        for line in file:
            temp_file.write(line)

    temp_file.close()


    os.remove(user_input) 
    os.rename(user_input + "_temp", user_input)

    print("I created the table of content for you :3")


def __harvest_from_file(file_path : str) -> str:
    table_of_content : str = "\n\n\n\n# Table of Content:\n\n"

    title_counters : dict[int, int] = dict()

    # Lists lenght represents depth. The numbers the amount of hashtags that created it
    # This is so we account for not always starting at #. We may start at ###
    # And we may skip some so we go from ## to ####
    sub_headline_depth : list[int] = []


    current_hashtag_depth : int = 0


    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:

            if not line.startswith("#"):
                continue

            words : list[str] = line.split(" ")
            first_word : str = words[0]

            if not __line_only_contains( first_word, "#" ):
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

                headline : str = ""
                headline += __create_headline(title_counters[current_hashtag_depth], words[1:], len(sub_headline_depth)-1)
                # headline += "\n"
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

    if title.startswith("angle brackets:"):
        print("heeeere!")

    title = title.strip(" ")
    title = title.strip("*")
    title = title.strip(":")
    title = title.strip(".")

    endcoded_title : str = title


    endcoded_title = endcoded_title.replace("/", "")
    endcoded_title = endcoded_title.replace(":", "")
    endcoded_title = endcoded_title.replace("|", "")
    endcoded_title = endcoded_title.replace("[", "")
    endcoded_title = endcoded_title.replace("]", "")
    endcoded_title = endcoded_title.replace("<", "")
    endcoded_title = endcoded_title.replace(">", "")


    endcoded_title = endcoded_title.replace(" ", "-")


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


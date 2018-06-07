import os

# This function takes a directory path for your main directory
# as an input and checks if that path already exists.
# If it does not already exist it will create the main
# directory.

def create_main_directory(PathToDirectory):
    if not os.path.exists(PathToDirectory):
        print('Creating Main Directory in ' + PathToDirectory + '\n')
        os.makedirs(PathToDirectory)


# The next function will create 2 files and store them in the
# main directory. File 1 will store every link that has
# already been crawled and file 2 will store every link
# that has not been crawled yet. This prevents the web-crawler
# from crawling they same URL twice. The first link in the
# queue will be the start_url, because the program is going
# to need a target first in order to scan URL's associated
# to it.

def create_result_files(PathToDirectory, start_url):
    queue = os.path.join(PathToDirectory, 'queued.txt')
    crawled = os.path.join(PathToDirectory, 'crawled.txt')
    if not os.path.isfile(queue):
        write_to_file(queue, start_url)
    if not os.path.isfile(crawled):
        write_to_file(crawled, '')


# Now we need to create the 3 functions that write, append
# or delete results in a file

def write_to_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def append_to_file(path, data):
    with open(path, 'a') as f:
        f.write(data + '\n')


def delete_file_content(path):
    os.remove(path)
    open(path, 'w+')


# Now we will need a function that puts all crawled links
# into the crawled.txt file and another function that
# filters identical links that may appear twice in
# crawled.txt

# The following function takes a list of links and
# the crawled.txt file as an input. Then it appends the links with our earlier
# created append_to_file-function.

def put_links_in_file(links, f):
    for link in links:
        if not check_if_written2(link, f):
            append_to_file(f, link)


def put_ids_in_file(ids, f):
    if ids is not None:
        append_to_file(f, str(ids))


# This function filters duplicates links with
# a Python-Set. A Python-Set is a list that only
# contains unique values.

def filter_duplicates(links):
    results = set(links)
    return results


# This functions transfers links from queued.txt to crawled.txt
def transfer_links(url, PathToDirectory):
    with open(os.path.join(PathToDirectory, 'queued.txt'), 'r+') as f:
        modified = f.read().split('\n')
        delete_file_content(os.path.join(PathToDirectory, 'queued.txt'))
        with open(os.path.join(PathToDirectory, 'queued.txt'), 'r+') as f:
            for i in range(0, len(modified)):
                if modified[i] == url:
                    modified[i] = ''
                f.write(modified[i] + '\n')

    with open(os.path.join(PathToDirectory, 'crawled.txt'), 'r') as f:
        lines = f.read().split('\n')
        url_already_in = False
        for i in range(0, len(lines)):
            if lines[i] == url:
                url_already_in = True
        if not url_already_in:
            append_to_file(os.path.join(PathToDirectory, 'crawled.txt'), url)


# This functions checks if links that are about to be stored in crawled.txt are already in crawled.txt
def check_if_written(link, PathToDirectory):
    boolean = False
    with open(os.path.join(PathToDirectory, 'crawled.txt'), 'rt') as f:
        modified = f.read().split('\n')
        for i in range(0, len(modified)):
            if modified[i] == link:
                boolean = True
    return boolean


# This functions checks if links that are about to be stored in crawled.txt are already in crawled.txt
def check_if_written2(link, PathToDirectory):
    boolean = False
    with open(PathToDirectory, 'rt') as f:
        modified = f.read().split('\n')
        for i in range(0, len(modified)):
            if modified[i] == link:
                boolean = True
    return boolean


# This function checks if the url that is about to be scanned is part of the base url
def check_if_base_url(url, first_url):
    boolean = False
    url_parts = url.split('/')
    relevant_url_part = url_parts[2]
    first_url_parts = first_url.split('/')
    relevant_first_url_part = first_url_parts[2]
    if relevant_url_part != relevant_first_url_part:
        boolean = True
    return boolean


# This function counts all links in allLinks.txt
def count_links(PathToDirectory):
    with open(os.path.join(PathToDirectory, 'allLinks.txt'), 'r+') as f:
        lines = len(f.read().split('\n'))

    if lines > 1:
        return " " + str(lines-1) + " "
    else:
        return " " + str(lines) + " "


# This function counts all found text input id's
def count_ids(PathToDirectory):
    with open(os.path.join(PathToDirectory, 'ids.txt'), 'r+') as f:
        lines = len(f.read().split('\n'))

    if lines > 0 and lines > 1:
        return " " + str(lines - 1) + " "
    elif lines == 0 or lines == 1:
        return " " + str(lines - 1) + " "


# This function stores links into one file called allLinks.txt
def store_all_links(PathToDirectory):
    with open(os.path.join(PathToDirectory, 'queued.txt'), 'r+') as f:
        queued = f.read()

    with open(os.path.join(PathToDirectory, 'crawled.txt'), 'r') as f:
        crawled = f.read()

    allLinks = os.path.join(PathToDirectory, 'allLinks.txt')
    if not os.path.isfile(allLinks):
        write_to_file(allLinks, queued + crawled)


# This function stores text input field id's in a file called ids.txt
def store_all_ids(PathToDirectory):
    ids = os.path.join(PathToDirectory, 'ids.txt')
    if not os.path.isfile(ids):
        write_to_file(ids, '')


# This function creates a file called XSS_Results.txt and stores it in the main directory
def create_all_results_txt_file(PathToDirectory):
    allResults = os.path.join(PathToDirectory, 'XSS_Results.txt')
    if not os.path.isfile(allResults):
        write_to_file(allResults, '')


# This function removes empty lines from text files
def remove_empty_lines(file):
    # Get file contents
    fd = open(file)
    contents = fd.readlines()
    fd.close()

    new_contents = []

    # Get rid of empty lines
    for line in contents:
        # Strip whitespace
        if not line.strip():
            continue
        else:
            new_contents.append(line)

    # Create file without empty lines
    with open(file, 'w') as f:
        f.write("".join(new_contents))


# This function converts multiple lines of text in a text file into one list
def file_to_list(PathToDirectory):
    list = []
    ids = os.path.join(PathToDirectory, 'ids.txt')
    with open(ids, 'rt') as f:
        lines = f.read().split('\n')
        for line in lines:
            if len(line) > 0:
                list.append(line)
    return list

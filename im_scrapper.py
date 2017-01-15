"""
Main file for running the script.
Usage:
im_scrapper.py -h --> Shows help
im_scrapper.py -u <webpage_url> --> Downloads images from given url, stores
the image files and a text file with all urls for images in '/images' folder
in current working directory.
im_scrapper.py -u <webpage_url> -d <dir>
im_scrapper.py -url=<webpage_url> -dir=<dir> --> Downloads images from given url
specified with -u or --url= option, stores the image files and a text file
with all urls for images in directory specified with -d or --dir= option.

"""
import os
import logging
from scrapper.config import  files_dir
from scrapper.scrapping_functions import get_image_urls_from_webpage, \
    download_images

try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse


def main(argv):
    """
    Main function for handling user provided (options) parameters and
    running the function.
    :param argv: commandline arguments provided by user.
    :return:
    """
    import errno
    import getopt
    try:
        opts, args = getopt.getopt(argv, "hu:d:", ["help", "url=", 'dir='])
    except getopt.GetoptError:
        print("Use -h for usage information.")
        sys.exit(errno.EINVAL)
    in_url = None
    dir = files_dir
    try:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print("Usage:\n"
                      "fsec_hw.py -h --> shows help\n"
                      "fsec_hw.py --help --> shows help\n"
                      "fsec_hw.py -u <url> -d "
                      "<directory_path_for_storing_files>\n"
                      "fsec_hw.py --url=<url> -dir="
                      "<directory_path_for_storing_files>")
                sys.exit()
            elif opt in ('-u', '--url'):
                logging.info('User input for url = {url}'.format(url=arg))
                in_url = arg
                print('url=', in_url)
            elif opt in ('-d', '--dir'):
                logging.info('User input for dir = {dir}'.format(dir=arg))
                dir = arg
                print('dir=', dir)
            else:
                print("Use -h for usage information.")
                sys.exit(errno.EINVAL)
        if in_url is None:
            print('Use fsec_hw.py for usage information.')
            sys.exit(errno.EINVAL)

        # Find URLs from input url
        urls = get_image_urls_from_webpage(in_url)

        # Establish directory to store the downloaded images.
        parsed_url = urlparse(in_url)
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(dir + parsed_url.netloc):
            os.makedirs(dir + parsed_url.netloc)
            logging.info('{dir} created for storing images'.format(
                dir=dir + parsed_url.netloc))
        os.chdir(dir + parsed_url.netloc)

        # Write URLs to file
        f = open('{fn}.txt'.format(fn=parsed_url.netloc), 'w+')
        for url in urls:
            f.write(url+'\n')
        f.close()

        # Download Images
        stats = download_images(urls)
        logging.info('Successfully downloaded {succ} images and failed to '
                     'download {f} images from given website='
                     '{url}'.format(succ=stats['success'], f=stats['fail'],
                                    url=in_url))
        print('Successfully downloaded {succ} images and failed to '
              'download {f} images from given website={url}. \nExiting...'
              ''.format(succ=stats['success'], f=stats['fail'], url=in_url))
        return
    except OSError as os_ex:
        logging.error('Cannot create requested directory={dir} to store '
                      'files. Error={err}'.format(dir=dir, err=os_ex))
        return errno.EACCES
    except ImportError as ex:
        print("Error:{err}".format(err=ex))
        logging.error('Error:{err} while downloading images from {url}'
                      ''.format(err=ex, url=in_url or arg))
        return errno.EAGAIN


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print("Use -h for usage information.")
        sys.exit(0)
    main(sys.argv[1:])

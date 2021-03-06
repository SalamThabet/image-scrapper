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
import logging
from scrapper.config import files_dir
from scrapper.helpers import create_directory
from scrapper.scrapping_functions import get_image_urls_from_webpage, \
    download_images, get_netloc_from_url


def _write_url_file_to_disk(filename, url_list):
    """
    This function writes list of urls to given file.
    :param filename: path/name of file where urls should be written
    :param url_list: list of urls to be written to file
    :return:
    """
    try:
        f = open(filename, 'w+')
        for url in url_list:
            f.write(url+'\n')
        f.close()
        logging.info('successfully wrote {count} urls to file={file}.'.format(
            file=filename, count=len(url_list)))
        return True
    except Exception as ex:
        logging.error('Unable to write urls to file={file}. Error={err}'.format(
            file=filename, err=ex))
        return False


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

        # Create directory
        if not create_directory(dir + get_netloc_from_url(in_url)):
            return
        # Write url file to disk
        _write_url_file_to_disk(filename=get_netloc_from_url(in_url)+'.txt',
                                url_list=urls)
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

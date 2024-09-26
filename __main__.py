import argparse
from core.colors import green,end,back,red
import argparse
import threading
from art import text2art
import warnings
import core.config as mem
from core.exporter import exporter
from plugins.heuristic import heuristic
from core.utils import prepare_requests,create_query,update_request,requester
from core.bruter import check_response

warnings.filterwarnings('ignore') 
parser = argparse.ArgumentParser() # defines the parser
# Arguments that can be supplied

result=[]
killed_Urls=[]



parser.add_argument('-o', help='Path for output file.', dest='text_file')
parser.add_argument('-t', help='Number of concurrent threads. (default: 5)', dest='threads', type=int, default=5)
parser.add_argument('-i', help='Import target URLs from file.', dest='import_file', nargs='?', const=True)
parser.add_argument('-m', help='Environment mode: L (linux) or W (windows). (default: linux)', dest='mode', type=str, default='L')
args = parser.parse_args() # arguments to be parsed



a = text2art(f"Dalaho")
print(a)



mem.var = vars(args)


def narrower(request2):
   is_reflected= check_response(request2)
   if is_reflected:
       return True


def initialize(url):
    """
    handles parameter finding process for a single request object
    """
    
    response=requester(url)   
    if type(response) != str:
        found = heuristic(response)
        if found:
            query= create_query(found)

            if "?" in url:
                url2="".join([url,"&",query]) 
            else:
                url2="".join([url,"?",query]) 
            is_reflected = narrower(url2)
            if is_reflected:
                print(url2+"\n")
                result.append(url2+"\n")
        if "=" in url:
            request2=update_request(url)
            response = requester(request2)
            if type(response) != str:

                is_reflected = narrower(request2)
                if is_reflected:
                    print(request2+"\n")
                    result.append(request2+"\n")

def worker(url):
    # Wrapper function for threading, calls initialize
    try:
        initialize(url) 
    except Exception as e:
        global killed_Urls
        killed_Urls.append(url)


def worker_K(url):
    # Wrapper function for threading, calls initialize
    try:
        initialize(url) 
    except Exception as e:
        print(f"Error processing {url}:{e}")


def main():
    num_threads = mem.var['threads']
    thread_list = []
    while urls:
        for _ in range(num_threads):
            if urls:
                u = urls.pop(0) 
                thread = threading.Thread(target=worker, args=(u,))
                thread_list.append(thread)


        for thread in thread_list:
            thread.start()


        for thread in thread_list:
            thread.join()

        thread_list = []  # Clear the thread_list after joining threads

    if killed_Urls:
        if killed_Urls:
            u = killed_Urls.pop(0)  
            worker_K(u)


if __name__ == '__main__':
    if not mem.var['text_file']:
        print("Please add output file")
        exit()
    urls = prepare_requests(args)
    if len(urls) == 0:
        print("The import_file has no Url")
        exit()
    else:
        print(f"count of urls:{green}{len(urls)}")


    print(f"{red}Start")
    print(f"{back}Display only vulnerable URLs.")
    main()

    if len(result) !=0:
        exporter(result)
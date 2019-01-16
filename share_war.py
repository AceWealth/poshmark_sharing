import selenium, time, argparse, sys, textwrap
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Your Credentials File
from credentials import *
import pdb

def rt(d):
    times = np.random.rand(1000)+np.random.rand(1000)+d
    return np.random.choice(times, 1).tolist()[0]

def login():
    url = "https://poshmark.com/login"
    driver.get(url)

    time.sleep(rt(5))

    try:
        #Login
        print("[*] logging into Poshmark seller account...\
            the share war will begin momentarily...")
        username = driver.find_element_by_name("login_form[username_email]")
        username.send_keys(poshmark_username)
        time.sleep(rt(5))

        password = driver.find_element_by_name("login_form[password]")
        password.send_keys(poshmark_password)
        time.sleep(rt(5))

        password.send_keys(Keys.RETURN)
        time.sleep(rt(5))

        #Check for Captcha
        try:
            captcha_fail = driver.find_element_by_xpath("//span[@class='base_error_message']")
            if len(str(captcha_fail)) > 100:
                print(("[*] Caught by Captchas: Proceed to debugger\
                    in terminal..."))
                import pdb; pdb.set_trace()
                print(("[*] Please complete captchas, robots game before proceeding..."))
                login_pdb()
                return
            else:
                pass
        except:
            pass
 
        #Navigate to Seller Page
        time.sleep(rt(10))
        seller_page = "https://poshmark.com/closet/{}?availability=available".format(args.account)
        driver.get(seller_page)

    except:
        #Captcha Catch
        print("[*] ERROR in Share War: Thrwarted by Captchas")
        login_pdb()
        pass


def login_pdb():

    try:
        import pdb; pdb.set_trace()

        #Login
        username = driver.find_element_by_name("login_form[username_email]")
        username.clear()
        username.send_keys(poshmark_username)
        time.sleep(rt(5))

        password = driver.find_element_by_name("login_form[password]")
        password.send_keys(poshmark_password)
        time.sleep(rt(5))
        password.send_keys(Keys.RETURN)

        #Navigate to Seller Page
        time.sleep(rt(5))
        seller_page = "https://poshmark.com/closet/{}?availability=available".format(args.account)
        driver.get(seller_page)

    except:
        print("[*] ERROR in Share War: Thrwarted by Captchas")
        pass


def scroll_page(n, delay=3):
    scroll = 0
    print("[*] scrolling through all items in closet...")
    for i in range(1, n+1):
        scroll +=1
        scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(scroll_script)
        time.sleep(rt(delay))


def get_closet_urls():
    items = driver.find_elements_by_xpath("//div[@class='item-details']")
    urls = [item.find_element_by_css_selector('a').get_attribute('href') for item in items]
    return urls


def get_closet_share_icons():
    items = driver.find_elements_by_xpath("//div[@class='social-info social-actions d-fl ai-c jc-c']")
    share_icons = [item.find_element_by_css_selector("a[class='share']") for item in items]
    return share_icons


def clicks_share_followers(share_icon, d=4.5):

    #First share click
    driver.execute_script("arguments[0].click();", share_icon); time.sleep(rt(d))

    #Second share click
    share_followers = driver.find_element_by_xpath("//a[@class='pm-followers-share-link grey']")
    driver.execute_script("arguments[0].click();", share_followers); time.sleep(rt(d))


def share(d=4.5):
    #shortcut to reshare in debugger mode
    [clicks_share_followers(item, d) for item in share_icons]


def open_closet_item_url(url):
    print(url)
    driver.get(url)
    time.sleep(rt(5))


def deploy_share_war(n=3, order=True):
    print("[*] DEPLOYING SHARE WAR")

    try:
        login()
        scroll_page(n)
        share_icons = get_closet_share_icons()

        if order is True:
            share_icons.reverse()
        else:
            pass

        print("[*] sharing PoshMark listings for {} items in closet...".format(len(share_icons)))
        print("[*] please wait...")

        #Share Listings
        [clicks_share_followers(item) for item in share_icons]

        print("[*] closet successfully shared...posh-on...")
        pass

    except:
        print("[*] ERROR in Share War")
        pass


    print("[*] the share war will continue in {} minutes...current time: {}".format(int(random_loop_time/60), time.strftime('%l:%M%p %Z on %b %d, %Y')))


if __name__=="__main__":

    ##################################
    ## Arguments for Script
    ##################################

    ## Default Arguments with RawTextHelpFormatter
    class RawTextArgumentDefaultsHelpFormatter(
            argparse.ArgumentDefaultsHelpFormatter,
            argparse.RawTextHelpFormatter
        ):
            pass

    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
        [*] Help file for share_war.py
            from the poshmark_sharing repository:
            https://github.com/jmausolf/poshmark_sharing
        '''),
        usage='use "python %(prog)s --help" for more information',
        formatter_class=RawTextArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--time", default=3600, type=float, 
        help=textwrap.dedent('''\
            loop time in seconds to repeat the code
            :: example, repeat in two hours:
            :: -t 7200
            '''))
    parser.add_argument("-n", "--number", default=7, type=int, 
        help="number of closet scrolls")
    parser.add_argument("-o", "--order", default=True, type=bool, 
        help="preserve closet order")
    parser.add_argument("-a", "--account", default=poshmark_username, type=str, help="The accounts closet you want to share (default is the account provided in the credentials file)")
    parser.add_argument("-d", "--driver", default='0', type=str, 
        help=textwrap.dedent('''\
            selenium web driver selection
            drivers may be called by either entering the name
            of the driver or entering the numeric code 
            for that driver name as follows:
            Firefox==0, Chrome==1, Edge==2, Safari==3
            :: example, use Firefox:
            -d Firefox 
            -d 0

            :: example, use Chrome:
            -d Chrome
            -d 1
            '''))

    args = parser.parse_args()


    ##################################
    ## Run Script
    ##################################

    # Start Share War Loop
    starttime = time.time()

    while True:

        #Select and Start Webdriver
        try:
            # Try to start driver
            if args.driver == '0' or args.driver == 'Firefox':
                driver = webdriver.Firefox()
            elif args.driver == '1' or args.driver == 'Chrome':
                driver = webdriver.Chrome()
            elif args.driver == '2' or args.driver == 'Edge':
                driver = webdriver.Edge()
            elif args.driver == '3' or args.driver == 'Safari':
                driver = webdriver.Safari()
            else:
                print(textwrap.dedent('''
                    [*] ERROR Driver argument value not supported!
                        Check the help (-h) argument for supported values.
                    '''))

            #Driver Implicit Wait
            driver.implicitly_wait(0)

        except NameError:
            print(textwrap.dedent('''
                [*] ERROR You don't have the web driver for argument
                    given ({}) you need to download it, go here for
                    installation info:
                    https://selenium-python.readthedocs.io/installation.html#drivers
                '''.format(args.driver)))
            sys.exit()

        except Exception as e:
            print(textwrap.dedent('''
                [*] ERROR the selected driver may not be setup correctly. 
                    Ensure you can access it from the command line and 
                    try again. 
                    {}
                '''.format(e)))
            sys.exit()

        else:
            pass

        #Time Delay: While Loop
        random_loop_time = rt(args.time)

        #Run Main App
        deploy_share_war(args.number, args.order)

        time.sleep(rt(10))
        driver.close()

        #Time Delay: While Loop
        time.sleep(random_loop_time - ((time.time() - starttime) % 
            random_loop_time))
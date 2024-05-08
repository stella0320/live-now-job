from datetime import datetime


def main() :
    time = datetime.now()
    timeStr = time.strftime('%Y-%m-%d %H:%M')
    print (timeStr + " -- hello world!")
    print ("Welcome to python cron job")

if __name__ == "__main__":
    main()
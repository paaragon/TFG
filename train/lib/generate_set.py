from SolarData import SolarData
import argparse

def main(start_date, end_date, start_hour, end_hour, k, h):
    solar_data = SolarData(start_date, end_date, start_hour, end_hour)
    solar_data.loadData(k, h)

    solar_data.getData()
    solar_data.getTarget()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', action="store", dest="start_date", help="Start date for data set", type=int)
    parser.add_argument('-e', action="store", dest="end_date", help="End date for data set", type=int)
    parser.add_argument('-sh', action="store", dest="start_hour", help="Start date for data set",type=int)
    parser.add_argument('-eh', action="store", dest="end_hour", help="End date for data set", type=int)
    parser.add_argument('-k', action="store", dest="knumber", help="K previous instances", type=int)
    parser.add_argument('-t', action="store", dest="horiz", help="Prediction horizon (target)", type=int)

    arguments = parser.parse_args()

    start_date = arguments.start_date
    end_date = arguments.end_date
    start_hour = arguments.start_hour
    end_hour = arguments.end_hour
    k = arguments.knumber
    h = arguments.horiz
    
    main(start_date, end_date, start_hour, end_hour, k, h)
import logging
import argparse
from abc import ABC, abstractmethod

class LogProcessor(ABC):
    def __init__(self):
        logging.basicConfig(filename="processor.log",
                            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            level=logging.DEBUG)
    
    @abstractmethod
    def process_batch(self, file):
        """
        Process a batch of log entries, where each line of 
        the File object (could be file, socket, etc.) is a log entry
        """
        pass
    
    def process_file(self, filename):
        """
        Process a log file in its entirety given a filename
        """
        logging.info("Processing log file [%s]", filename)
        try:
            with open(filename) as f:
                self.process_batch(f)
        except FileNotFoundError as not_found:
            logging.error("Attempt to process file [%s] which doesnt exist", filename)

class CookieLogProcessor(LogProcessor):
    def __init__(self):
        super().__init__()
        self.date_cookie_map = {} # date: str -> cookies: [str..]

    def process_batch(self, file):
        """
        Count the most active cookies per day given a log file
        Assumptions:
            1. the log is a csv file with comma delimiter
            2. the log is sorted by timestamp with the most recent occurrence first
        """
        daily_occurrence_map = {} # cookie_id: str -> occurences (during current day): int
        last_date = None
        for line in file:
            line = line.strip()
            if not line:
                continue # empty line
            if ',' not in line:
                logging.info("Ill-formatted log entry found [%s]", line)
                continue
            
            cookie_id, ts = line.split(',')
            # Simple format checking to make sure program doesnt crash
            # Could use regex library to simplify and improve format checking, but its not allowed in spec
            if ts == "timestamp":
                continue
            elif len(ts) != 25:
                logging.info("Ill-formatted log entry found [%s]", line)
                continue
            
            date = ts[:10]
            if date != last_date and last_date is not None:
                self.update_top_cookies(daily_occurrence_map, last_date)
                daily_occurrence_map.clear()

            if cookie_id in daily_occurrence_map:
                daily_occurrence_map[cookie_id] += 1
            else:
                daily_occurrence_map[cookie_id] = 1
            last_date = date
        
        # Tail case: the items in daily_occurrence_map at the end of the loop has not been included
        self.update_top_cookies(daily_occurrence_map, last_date)
    
    def update_top_cookies(self, daily_map, date):
        """
        Helper function
        Given a map <cookie_id, occurences (on current date)>, find all the top cookies
        including ties, and update the global map
        """
        if not daily_map:
            return
        occur_sorted = sorted(list(daily_map.items()), key=lambda x: x[1], reverse=True)
        ls_active_ids = []
        top_count = occur_sorted[0][1]
        for cid, count in occur_sorted:
            if count == top_count:
                ls_active_ids.append(cid)
            else:
                break
        self.date_cookie_map[date] = ls_active_ids

    def find_active_by_date(self, date):
        """
        Returns a list of the most active (tie included) cookies of the given date
        Returns None is no cookie is found on that date
        """
        if date not in self.date_cookie_map:
            logging.warning("No active cookie found for date [%s]", date)
            return None
        return self.date_cookie_map[date]
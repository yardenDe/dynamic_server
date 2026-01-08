from datetime import datetime
from fastapi import HTTPException
from disk import csv_to_disk

class ApiManager:
    """Handles API requests, DB access, and CSV writing to disk"""
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    @staticmethod
    def to_ms(delta):
        return int(delta.total_seconds() * 1000)

    def manage_queries(self, table: str, fields: list):
        """Core method to get data from DB, save result as CSV and add log execution time"""
        if not table:
            raise HTTPException(status_code=400, detail="Table name is required")
        if not fields:
            fields = ["*"]
            
        query = f"SELECT {', '.join(fields)} FROM {table}"
        start_select = datetime.now()
        try:
            data = self.db_manager.execute_query(query)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        t_select = self.to_ms(datetime.now() - start_select)

        if not data:
            return []

        f_name = f"{table}_{datetime.now().strftime('%d%m%y_%H%M%S')}.csv"
        start_write = datetime.now()
        t_write = -1
        
        # If CSV writing fails, write_time will set to -1 in the log
        try:
            csv_to_disk(data, f_name)
            t_write = self.to_ms(datetime.now() - start_write)
        except Exception as e:
            print(f"Internal Disk Error: {e}")

        try:
            self.db_manager.add_log({
                "file_name": f_name,
                "date_created": datetime.now().strftime("%Y-%m-%d"),
                "record_count": len(data),
                "select_time_ms": t_select,
                "write_time_ms": t_write
            })
        except Exception as e:
            print(f"Error: {e}")
 
        return data
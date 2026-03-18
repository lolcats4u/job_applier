from .file_handlers import File
class Job():
    def __init__(self, title:str, description:str, board:Account, app:Account):
        self.title = title
        self.board_account = board
        self.app_account = app
        self.duplicate = None
        self.applied = None
    
    def __str__(self):
        return f"Title:{self.title}, Job Board: {self.board_account}, Application Type: {self.app_account}\n"

    def save(self):
        pass

    def set_duplicate(self):
        self.duplicate = True

    def set_applied(self):
        self.applied = True

def load_jobs(job_file):
    """
    "uid", "title", "board_title", "app_title", applied
    """
    jobs = {}
    loaded_job_file = File("./jobs/jobs.csv")
    for job in loaded_job_file.contents:
        jobs[job[0]] = Job(job[1], job[2], job[3])
    return jobs

if __name__ == "__main__":
    main()
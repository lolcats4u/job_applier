import typer

from .jobs import Job, load_jobs
from .accounts import Account, load_account

app = typer.Typer()
@app.callback()
def main(ctx:typer.Context):
    print("Welcome to Job App Dystopia\n")

@app.command()
def load(ctx:typer.context):
    ctx.jobs=load_jobs()

@app.command()
def select(selector:str, ctx:typer.context):
    print("Select the jobs you would like to apply to.\n")
    ctx.selected_jobs = list(filter(lambda job: selector in job, ctx.jobs))
    group_by_board = {}
    for job in ctx.selected_jobs:
        group_by_board[ctx.selected.jobs.board.account] = job
    ctx.selected_jobs = group_by_board

@app.command()
def apply(ctx:typer.context):
    Accounts = {}
    for board in ctx.selected_jobs:
        load_account(board)
        for job in board:
            


    




    


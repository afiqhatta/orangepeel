import pandas as pd
import click 

@click.command()
def show_available_sites(): 
    """This function shows which newspapers are in the database and are ready for scraping""" 
    df = pd.read_csv('metadata.csv')
    click.echo('Below are the available Malaysian news websites supported')
    click.echo(df['name'])

if __name__ == "__main__": 
    show_available_sites()

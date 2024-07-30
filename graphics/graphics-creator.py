# python3 graphics-creator.py data.psv
#
# pip3 install plotly
# pip3 install pandas
import plotly.express as px
import pandas as pd
import sys
from typing import List, Tuple
import itertools

def draw_data(x: List[int], y: List[int]):
    
    data = {
        'Distance': x,
        'Price': y
    }
    df = pd.DataFrame(data)

    # Create the box plot
    fig = px.box(df, x='Distance', y='Price', title="Price / Distance")
    fig.show()

def parse_data(filename: str) -> Tuple[List[int], List[int]]:
    column_distance: List[int] = []
    column_price: List[int] = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            chains: List[str] = line.strip().split("|")
            column_distance.append(int(chains[0]))
            column_price.append(int(chains[1]))            
    return (column_distance, column_price)

if __name__=='__main__':
    filename=sys.argv[1]
    data:List[List[int]] = parse_data(filename)
    draw_data(data[0], data[1])


import plotly.express as px

def makeGraph(selected_options):
    example_dict = {'Programming Language':selected_options,
                'Years of Experience':[(i + 1) * 2 for i in range(len(selected_options))]}

    return px.bar(example_dict, x = 'Programming Language', y = 'Years of Experience')
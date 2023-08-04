from dash import Dash, html, callback, Input, Output, dcc, dash_table,State
import mysql
from mysql.connector import connect
from dash_canvas import DashCanvas
from time import strftime
#from login_page import update_output
import dash_canvas
import base64
import json
import os

#USER_PASS_MAPPING = {'admin': '1234'}
# database for comments
host = 'localhost'
user = 'root'
password = 'chatme@2023'
database = 'mydatabase'

#database for annotations
host = 'localhost'
user = 'root'
password = 'chatme@2023'
database = 'mydatabase'

#app = Dash(__name__)
#app.title = "Data Annotation application"

# App layout
asset_folder = "./assets/"
image_files = [files for files in os.listdir(asset_folder) if files.endswith((".jpeg"))]



layout = html.Div(
    style={"display": "flex", "justify-content": "space-between", "background-color": "#3F000F", "color": "#3F000F"},
    children=[dcc.Link('Log out', href='/', style={'color': '#bed4c4'}),
        html.Div(
            style={"width": "50%", "height": "700px"},
            children=[
                dcc.Loading(
                    id="loading-image",
                    type="circle",
                    children=[
                        html.Div(
                            children=[
                                dcc.Store(id="current-image-index", data=0),
                                dcc.Store(id="current-image-filename", data=""),
                                dash_canvas.DashCanvas(
                                    id="canvas",
                                    lineWidth=2,
                                    width=500,
                                    height=700,
                                    hide_buttons=["zoom", "reset", "save", "select","pan", "pencil"]
                                ),
                                html.Button("Save Annotation", id="save-database",style={'background-color':'#3F000F','color':'#3F000F','border':'0','outline':'none'}, n_clicks=0),
                                html.Br(),
                                html.Button("Next Image", id="next-button", style={'margin-left':'60%','margin-top':'%','border-radius':'10px','height':'50px'}, n_clicks=0),
                                html.Div(id='container2', children=[])
                            ]
                        )
                    ]
                )
            ]
        ),

        html.Div(
            style={"width": "50%", "height": "700px"},  # Adjust the width as needed
            children=[
                html.Div(
                    id="dropdown-textarea-div",
                    children=[
                        html.Label('VALIDATION', style={'color': 'white'}),
                        dcc.Dropdown(
                            options=[{'label': opt, 'value': opt} for opt in ['correct', 'incorrect']],
                            id='validation',
                            placeholder="Select validation status of current annotation",
                            style={'background-color': 'lightgray'},
                            multi=True,
                            value=[]  # Set initial value to empty list
                        ),
                        html.Label('COMMENTS', style={'color': 'white'}),
                        dcc.Textarea(
                            id='textarea1',
                            placeholder='Enter your comment',
                            style={'height': '50px', 'margin-right': '5%', 'width': '100%'}
                        ),
                        
                        html.Label('VIEW OF ECHO', style={'color': 'white'}),
                        dcc.Dropdown(
                            options=[{'label': opt, 'value': opt} for opt in ['Parasternal long axis (PLAX)', 'Parasternal short axis(PSAX)', 'Apical Four Chamber(A4C)', 'Apical three chamber (A3C)',
                                                                               'Apical two chamber(A2C)', 'Suprasternal(SSN)', 'Subcostal', 'Doppler']],
                            id="echo",
                            placeholder="Select the view of the echocardiogram",
                            style={'background-color': 'lightgray', },
                            multi=True,
                            value=[]  # Set initial value to empty list
                        ),
                        html.Label('COMMENTS', style={'color': 'white'}),
                        dcc.Textarea(
                            id='textarea2',
                            placeholder='Enter your comment',
                            style={'height': '50px', 'margin-right': '5%', 'width': '100%'}
                        ),
                        
                        html.Label('THICKNESS STATE', style={'color': 'white'}),
                        dcc.Dropdown(
                            options=[{'label': opt, 'value': opt} for opt in ['Thick', 'Not Thick', 'Not Applicable']],
                            id="thickness",
                            placeholder="Select the state of thickness",
                            style={'background-color': 'lightgray'},
                            multi=True,
                            value=[]  # Set initial value to empty list
                        ),
                        html.Label('COMMENTS', style={'color': 'white'}),
                        dcc.Textarea(
                            id='textarea3',
                            placeholder='Enter your comment',
                            style={'height': '50px', 'margin-right': '5%', 'width': '100%'}
                        ),
                        
                        html.Label('CONDITIONS', style={'color': 'white'}),
                        dcc.Dropdown(
                            options=[{'label': opt, 'value': opt} for opt in ['Mitral Valve Regurgitation', 'Aortic Valve Regurgitation', 'Tricuspid Valve Regurgitation',
                                                                               'Pulmonary Valve Regurgitation', 'Aortic Valve Stenosis', 'Mitral Valve Stenosis', 'Tricuspid Valve Stenosis', 'Pulmonary Valve Stenosis',
                                                                               'Mitral Valve Prolapse', 'Not Applicable']],
                            id="condition",
                            placeholder="Select the condition or conditions",
                            style={'background-color': 'lightgray'},
                            multi=True,
                            value=[]  # Set initial value to empty list
                        ),
                        html.Label('COMMENTS', style={'color': 'white'}),
                        dcc.Textarea(
                            id='textarea',
                            placeholder='Enter your comment',
                            style={'height': '50px', 'margin-right': '5%', 'width': '100%'}
                        ),
                        
                        
                      
                       
                        html.Br(),
                        html.Button("SAVE", id="save-button", n_clicks=0, style={"color": "black"}),
                        html.Div(id='container', children=[], style={'color': 'blue'}),
                    ]
                )
            ]
        )
    ]
)
# the callback allow teh user to avigate through a list of images by clickig teh next button
#the callback and the function they are used to update image content displayed on canvas and track the current image index
@callback(
    Output("canvas", "image_content"),
    Output("current-image-index", "data"),
    Output("current-image-filename", "data"),
    Input("next-button", "n_clicks"),
    State("current-image-index", "data")
)
def update_canvas_image(n_clicks, current_index):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks < len(image_files):
        current_index = n_clicks
        image_filename = image_files[current_index]
        image_path = os.path.join(asset_folder, image_filename)
        with open(image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('ascii')
        return f"data:image/jpeg;base64,{encoded_image}", current_index, image_filename

    return "", current_index, ""

#callback and the function for comments
@callback(
    Output('container', 'children'),
    [Input('validation', 'value'),
     Input('textarea1', 'value'),
     Input('echo', 'value'),
     Input('textarea2','value'),
     Input('thickness', 'value'),
     Input('textarea3','value'),
     Input('condition', 'value'),
     #Input('severity', 'value'),
     Input('textarea', 'value'),

     Input('save-button', 'n_clicks'),
    State("current-image-filename", "data")],
)
def update_database(validate, view, comments, comment_e,thickness,comment_v,condition,comment_t, n_clicks, image_filename):
    

    if not image_filename:
        return []

    if n_clicks >= 1:
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        add_database = """INSERT INTO my_info6
        (FILENAME,VALIDATE,COMMENTS_V,VIEW_OF_ECHO,COMMENTS_E,THICKNESS_STATE,COMMENTS_T,CONDITIONS,COMMENTS,TIMETAKEN)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        validate = str(validate)
        comment_v=str(comment_v)
        view = str(view)
        comment_e=str(comment_e)
        thickness = str(thickness)
        comment_t=str(comment_t)
        condition = str(condition)
        comments = str(comments)
        timestamp = strftime("%Y-%m-%d %H:%M:%S")
        values = (image_filename,) + (validate,) + (comment_v,) +(view,)+(comment_e,) +(thickness,)+(comment_t,) +(condition,) +(comments,)+(timestamp,)

        #values = (image_filename, validate,comment_v, view,comment_e,thickness,comment_t,condition,comments,timestamp)

        cursor.execute(add_database, values)

        print('Labels saved to database!')

        conn.commit()
        cursor.close()
        conn.close()
#callback and the function for annotation
@callback(
    Output("container2", "children"),
    [Input("canvas", "json_data"),
     Input("save-database", "n_clicks"),
     State("current-image-index", "data")]
)
def save_annotations_to_database(json_data, n_clicks, current_index):
    if not json_data or n_clicks is None or n_clicks == 0:
        return 0

    image_filename = image_files[current_index]
    annotations = json.loads(json_data)["objects"]

    con = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor1 = con.cursor()

    add_annotation = """INSERT INTO my_annotation1 (FILENAME, TYPES_USED, WIDTH, HEIGHT, STROKEWIDTH, SCALEX)
                        VALUES (%s,%s,%s,%s,%s,%s)"""

    # Debug statement for JSON data
    print("JSON Data:", json_data)

    for annotation in annotations:
        annotation_type = annotation["type"]
        if annotation_type in ["rect", "line"]:  # Include other types here if needed
            Types_used = annotation_type
            width = annotation["width"]
            height = annotation["height"]
            strokewidth = annotation["strokeWidth"]
            scaleX = annotation["scaleX"]
            values = (
                image_filename,
                Types_used,
                width,
                height,
                strokewidth,
                scaleX,
            )

            # Debug statement for SQL query
            print("SQL Query:", add_annotation, values)

            cursor1.execute(add_annotation, values)

    print("Image annotations saved to database!")

    con.commit()
    cursor1.close()
    con.close()

    return 0   # Reset the n_clicks count after saving annotations





   
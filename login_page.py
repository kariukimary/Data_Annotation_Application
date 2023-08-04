from dash import Dash,html,dcc,callback
import dash
import pages
from dash.dependencies import Input,Output,State




layout=html.Div([
    
    html.H1("Login",style={'text-align':'center'}),
    html.Br(),
    html.Div(
        id="login",
        style={
            "background-color": "blue",
            'margin-right':'20%',
            'margin-left':'20%',
            'margin-top':'60px'
            
            
        },
    children=[html.Label('username',style={'color':'white','margin-left':'20%'}),
    dcc.Input(id='username',type='text',placeholder=' Enter username',style={'border-radius':'7px',
                                                                 'margin-top':'10px','margin-left':'20%','margin-right':'20%','height':'45px','width':'450px'}),
    html.Br(),
    html.Label('password',style={ 'margin-top':'60px','margin-right':'20%','margin-left':'20%','color':'white'}),
    dcc.Input(id='password',type='password',placeholder=' Enter password',style={'border-radius':'7px',
                                                                 'margin-top':'10px','margin-left':'20%','margin-right':'20%','width':'450px','height':'45px'}),
    html.I(id='eye-icon', className='fa fa-eye',n_clicks=0,style={'position':'absolute','right':'45px','cursor':'pointer'}),
    html.Br(),
    html.Button('Login',id='login-button',style={'border-radius':'7px','width':'85px','margin-left':'40%',
                                                 'margin-top':'10px','height':'35px','margin-right':'20%','background-color':'lightgray','hover':'grey'})]),
    
    html.Div(id='outputs',children='')])



@callback(
    Output('outputs','children'),
    [Input('login-button','n_clicks')],
    [State('username','value'),
     State('password','value')]
)
def update_output(n_clicks,username,password):
    details={'admin':'123','mary':'1234','admin2':'12345'}
    if username=='' or username is None or password=='' or password is None:
        return html.Div(children='')
    if username not in details:
        return html.Div(children='incorrect username')
    if details[username]==password:
        return html.Div(dcc.Link('Access Granted!',href='/pages/m_dash2.py'))
    else:
        return html.Div(children='incorect password')
   
    


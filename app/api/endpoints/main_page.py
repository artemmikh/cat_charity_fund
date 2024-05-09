from fastapi import APIRouter, Response

router = APIRouter()


@router.get('/')
def get_all_meeting_rooms():
    """Выводит ссылку на документацию на главную страницу"""
    html_content = '''
    <html>
    <head>
        <style>
            body {
                background-color: black;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-size: 50px;
                color: white;
            }
        </style>
    </head>
    <body>
        <A HREF="HTTP://127.0.0.1:8000/DOCS">DOCUMENTATION</A>
    </body>
    </html>
    '''
    return Response(content=html_content, media_type="text/html")

from mangum import Mangum

# Import your app object
from app import app

# Create the Mangum handler
handler = Mangum(app)
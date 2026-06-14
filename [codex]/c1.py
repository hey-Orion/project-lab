import os 
import yaml
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field, EmailStr, ValidationError

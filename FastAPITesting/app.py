#import psycopg2 as postgres
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import math, hashlib, os
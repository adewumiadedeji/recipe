from datetime import datetime
import jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import email_validator as _email_check
import fastapi as _fastapi
import fastapi.security as _security
from passlib.hash import bcrypt
import schemas as _schemas
import models as _models
import random
import json
import pika
import time
import os
import utils.database as _database
from sqlalchemy.exc import IntegrityError

# Load environment variables
JWT_SECRET = os.getenv("JWT_SECRET")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
oauth2schema = _security.OAuth2PasswordBearer("/api/token")


def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    return channel

def connect_to_rabbitmq():
    # Connect to RabbitMQ
    while True:
        try:
            connection_params = pika.ConnectionParameters(
                host='192.168.117.2',  # or '127.0.0.1'
                port=5672,         # default RabbitMQ port
                credentials=pika.PlainCredentials('guest', 'guest')
            )

            connection = pika.BlockingConnection(connection_params)
            # connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to RabbitMQ. Retrying in 5 seconds...")
            time.sleep(5)

def create_database():
    # Create database tables
    return _database.Base.metadata.create_all(bind=_database.engine)


async def get_user_by_email(email: str, db: _orm.Session):
    # Retrieve a user by email from the database
    return db.query(_models.User).filter(_models.User.email == email and _models.User.is_active==True).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    try:
        # Validate email
        valid = _email_check.validate_email(user.email)
        name = user.name
        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=400, detail="Please enter a valid email")
    
    # Create user
    try:
        user_obj = _models.User(
            email=email,
            name=name,
            hashed_password=_hash.bcrypt.hash(user.password)
        )
        db.add(user_obj)
        db.commit()  # Commit changes
        db.refresh(user_obj)  # Refresh the object with the latest DB state
        return user_obj
    except IntegrityError:
        db.rollback()  # Rollback on error
        raise _fastapi.HTTPException(status_code=400, detail="User with this email already exists.")
    except Exception as e:
        db.rollback()  # Rollback for any other error
        raise _fastapi.HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def authenticate_user(email: str, password: str, db: _orm.Session):
    # Authenticate a user
    user = await get_user_by_email(email=email, db=db)

    if not user:
        return False
    
    if not user.is_active:
        return 'is_active_false'
    

    return user

async def create_token(user: _models.User):
    # Create a JWT token for authentication
    
    user_obj = _schemas.User.from_orm(user)
    user_dict = user_obj.model_dump()
    
    # del user_dict["hashed_password"]
    del user_dict["created_at"]
    
    print("Payload: ", user_dict)
    # payload = {
    #     **user_dict,
    #     "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 30 minutes expiry
    # }
    token = jwt.encode(user_dict, JWT_SECRET, algorithm="HS256")
    
    return dict(access_token=token, token_type="bearer")

async def get_current_user(db: _orm.Session = _fastapi.Depends(_database.get_db), token: str = _fastapi.Depends(oauth2schema)):
     # Get the current authenticated user from the JWT token
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")
    return _schemas.User.from_orm(user)

def generate_otp():
    # Generate a random OTP
    return str(random.randint(100000, 999999))


def send_otp(email, otp):
    # Send an OTP email notification using RabbitMQ
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    message = {'email': email,
                'subject': 'Account Verification OTP Notification',
                'other': 'null',
                'body': f'Your OTP for account verification is: {otp} \n Please enter this OTP on the verification page to complete your account setup. \n If you did not request this OTP, please ignore this message.\n Thank you '
                }

    try:
        queue_declare_ok = channel.queue_declare(queue='notification_service', durable=True)
        current_durable = queue_declare_ok.method.queue

        if current_durable:
            if queue_declare_ok.method.queue != current_durable:
                channel.queue_delete(queue='notification_service')
                channel.queue_declare(queue='notification_service', durable=True)
        else:
            channel.queue_declare(queue='notification_service', durable=True)

        channel.basic_publish(
            exchange="",
            routing_key='notification_service',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print("Sent OTP email notification")
    except Exception as err:
        print(f"Failed to publish message: {err}")
    finally:
        channel.close()
        connection.close()
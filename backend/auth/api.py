from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from auth import schema, service
from fastapi import HTTPException
from utils import cryptoUtil, jwtUtil, constantUtil, emailUtil
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
import uuid

auth_router = InferringRouter()


@cbv(auth_router)
class AuthApi:
    @auth_router.post('/register', response_model=schema.UserResponse, status_code=201)
    async def register(self, user: schema.UserRegister):
        # Check user exists
        result = await service.find_exist_user(user.email)
        if result:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create new user
        user.password = cryptoUtil.hash_password(user.password)
        await service.create_user(user)

        return {**user.dict()}

    @auth_router.post('/login')
    async def login(self, from_data: OAuth2PasswordRequestForm = Depends()): # from_data: OAuth2PasswordRequestForm = Depends(), from_data: schema.UserLogin
        # Check user exists
        result = await service.find_exist_user(from_data.username)
        if not result:
            raise HTTPException(status_code=400, detail="User not found.")

        # Verify password
        user = schema.UserCreate(**result)
        verify_password = cryptoUtil.verify_password(
            from_data.password, user.password)
        if not verify_password:
            raise HTTPException(
                status_code=400, detail="Invalid username or password.")

        # Create token
        access_token_secret = jwtUtil.timedelta(
            minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await jwtUtil.create_access_token(
            data={"sub": from_data.username},
            expires_delta=access_token_secret
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "email": user.email,
                "fullname": user.fullname,
            }
        }
    
    @auth_router.post('/forgot-password')
    async def forgot_password(self, request: schema.ForgotPassword):
         # Check user exists
        result = await service.find_exist_user(request.email)
        # if result:
        #     raise HTTPException(status_code=400, detail="User already exists")
        

        # Create reset code and save in database
        reset_code = str(uuid.uuid1())
        await service.create_reset_code(request.email, reset_code)

        # Sending Email
        subject = "Reset password"
        recipient = [request.email]
        message = """
        <!DOCTYPE html>
        <html>
        <title>Reset password</title>
        <body>
        <div style="width:100%;font-family: nonospace;">
            <h1>Hello, {0:}</h1>
            <p>You have requested to reset your password. Please click the link below to reset your password.</p>
            <a href="http://localhost:8000/reset-password?code={1:}">Reset password</a>
            <p>if you did not request to reset your password, please ignore this email.</p>
            <p>Thank you.</p>
        </div>
        </body>
        </html>
        """.format(request.email, reset_code)

        await emailUtil.send_email(subject, recipient, message)

        return {
            'reset_code': reset_code,
            'code': 200,
            'message': 'Please check your email to reset your password.'  
        }

    @auth_router.patch('/reset-password')
    async def reset_password(self, request: schema.ResetPassword):
        # Check valid reset password token
        reset_token = await service.check_reset_password_token(request.reset_password_token)
        if not reset_token:
            raise HTTPException(status_code=404, detail="Reset password token has expired, please request a new one.")
        
        # Check both new & confirm password are matched
        if request.new_password != request.confirm_password:
            raise HTTPException(status_code=404, detail="New password and confirm password are not matched.")
        
        # Reset new password
        forgot_password_object = schema.ForgotPassword(**reset_token)
        new_hashed_password = cryptoUtil.hash_password(request.new_password)
        await service.reset_password(new_hashed_password, forgot_password_object.email)

        # Disable reset code (already user)
        await service.disable_reset_code(request.reset_password_token, forgot_password_object.email)

        return {
            'code': 200,
            'message': 'Your password has been reset.'
        }
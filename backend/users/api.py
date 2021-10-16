from fastapi import Depends, status, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from auth import schema as auth_schema, service as auth_service
from users import schema as user_schema, service as user_service
from utils import jwtUtil, cryptoUtil


users_router = InferringRouter()

@cbv(users_router)
class User_Api:
    @users_router.get("/profile")
    async def get_user(self, current_user: auth_schema.UserResponse = Depends(jwtUtil.get_current_active_user)):
        return current_user


    @users_router.patch("/profile")
    async def update_user( self, request: user_schema.UserUpdate, current_user: auth_schema.UserResponse = Depends(jwtUtil.get_current_user)):
        
        # Update user info
        await user_service.update_user(request, current_user)
        return {
            'status_code': status.HTTP_200_OK,
            'detail': 'User updated successfully.'
        }

    @users_router.delete("/profile")
    async def deactivate_account(self, current_user: auth_schema.UserResponse = Depends(jwtUtil.get_current_active_user)):
        # Delete user
        await user_service.deactivate_account(current_user)
        return {
            'status_code': status.HTTP_200_OK,
            'detail': 'User account has been deactivated successfully.'
        }
        
    @users_router.patch("/profile/change-password")
    async def change_password(
        self,
        change_password_object: user_schema.ChangePassword,
        current_user: auth_schema.UserResponse = Depends(jwtUtil.get_current_active_user)
    ):
        # Check user exist
        result = await auth_service.find_exist_user(current_user.email)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        # Verify current password
        user = auth_schema.UserCreate(**result)
        valid = cryptoUtil.verify_password(change_password_object.current_password, user.password)
        if not valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect.")
        
        # Check new password and confirm password
        if change_password_object.new_password != change_password_object.confirm_password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="New password and confirm password is not match.")

        # Change password
        change_password_object.new_password = cryptoUtil.hash_password(change_password_object.new_password)
        await user_service.change_password(change_password_object, current_user)
        return {
            'status_code': status.HTTP_200_OK,
            'detail': 'Password has been changed successfully.'
        }

    @users_router.post("/logout")
    async def logout(self, token: str = Depends(jwtUtil.get_token_user), current_user: auth_schema.UserResponse = Depends(jwtUtil.get_current_active_user)):
        # Save token to user to table blacklist
        await user_service.save_token_to_blacklist(token, current_user)
       
        return {
            'status_code': status.HTTP_200_OK,
            'detail': 'User has been logged out successfully.'
        }
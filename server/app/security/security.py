from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Criptografa a senha
async def get_password_hash(password):
    return pwd_context.hash(password)



# Compara senha com a senha criptografada
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

import bcrypt


# Criptografa a senha
def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# Compara senha com a senha criptografada
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Account, Template, User
from app.auth import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        account_exists = db.query(Account).first()
        if account_exists:
            print("Database already initialized")
            return
        
        # Criar conta de exemplo
        test_account = Account(
            name="Test Account",
            api_key=str(uuid.uuid4())
        )
        db.add(test_account)
        db.commit()
        db.refresh(test_account)
        
        print(f"Created test account with API key: {test_account.api_key}")
        
        # Criar usuário de teste
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("password123"),
            account_id=test_account.id
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"Created test user: username=testuser, password=password123")
        
        # Criar templates de exemplo
        templates = [
            Template(
                template_id="welcome_template",
                name="Welcome Message",
                channel="RCS",
                channel_type="Single",
                content="Welcome to our service, {{name}}! We're glad to have you with us."
            ),
            Template(
                template_id="promo_template",
                name="Promotion Message",
                channel="RCS",
                channel_type="Basic",
                content="Hi {{name}}, check out our latest promotion: {{promo_text}}. Valid until {{valid_date}}."
            )
        ]
        
        for template in templates:
            db.add(template)
        
        db.commit()
        print(f"Created {len(templates)} templates")
        
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization completed")

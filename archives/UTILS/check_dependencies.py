# check_dependencies.py
# source venv/Scripts/activate
# python check_dependencies.py


import traceback
import os

# Store results + error messages
results = {}
errors = {}

def test_import(name, func):
    print(f"\n=== Testing {name} ===")
    try:
        func()
        print(f"[PASS] {name} works")
        results[name] = True
    except Exception as e:
        print(f"[FAIL] {name} error:")
        print(type(e).__name__, e)
        traceback.print_exc()
        results[name] = False
        errors[name] = f"{type(e).__name__}: {e}"


# --------------------------
#  Test implementations
# --------------------------

def test_fastapi():
    from fastapi import FastAPI
    app = FastAPI()
    assert callable(app.get)

def test_pydantic():
    from pydantic import BaseModel, EmailStr
    class User(BaseModel):
        email: EmailStr
    User(email="test@example.com")

def test_requests():
    import requests
    response = requests.Response()
    assert isinstance(response, requests.Response)

def test_sqlalchemy():
    from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()
    Table(
        "items",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
    )
    metadata.create_all(engine)

def test_sqlmodel():
    from sqlmodel import SQLModel, Field, create_engine, Session
    class Item(SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        name: str
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Item(name="example"))
        session.commit()

def test_uvicorn():
    import uvicorn
    assert hasattr(uvicorn, "run")

def test_dotenv():
    from dotenv import load_dotenv
    open(".env", "w").write("TEST_VALUE=123")
    load_dotenv()
    assert os.getenv("TEST_VALUE") == "123"

def test_configparser():
    import configparser
    config = configparser.ConfigParser()
    config.read_dict({"section": {"key": "value"}})
    assert config["section"]["key"] == "value"


# --------------------------
#  Run tests
# --------------------------

if __name__ == "__main__":
    print("\n### PYTHON DEPENDENCY DIAGNOSTICS ###")

    tests = [
        ("FastAPI", test_fastapi),
        ("Pydantic", test_pydantic),
        ("Requests", test_requests),
        ("SQLAlchemy", test_sqlalchemy),
        ("SQLModel", test_sqlmodel),
        ("Uvicorn", test_uvicorn),
        ("python-dotenv", test_dotenv),
        ("configparser", test_configparser),
    ]

    for name, fn in tests:
        test_import(name, fn)

    # --------------------------
    # Final Detailed Summary
    # --------------------------
    print("\n### FINAL DETAILED SUMMARY ###")
    for name, status in results.items():
        state = "PASS" if status else "FAIL"
        print(f"- {name}: {state}")

    passed = sum(1 for x in results.values() if x)
    total = len(results)

    print("\n### TOTAL SUMMARY ###")
    print(f"Overall: {passed}/{total} tests passed")

    # --------------------------
    # Short Error Summary Only
    # --------------------------
    if errors:
        print("\n### SHORT ERROR SUMMARY ###")
        for name, err in errors.items():
            print(f"- {name}: {err}")
    else:
        print("\n### SHORT ERROR SUMMARY ###")
        print("No errors. All good.")

    print()

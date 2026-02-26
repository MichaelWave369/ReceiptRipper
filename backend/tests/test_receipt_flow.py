from io import BytesIO
from PIL import Image
from fastapi.testclient import TestClient

from receiptrip.main import app


def auth_header(client: TestClient):
    payload = {"email": "test@example.com", "password": "secret123", "default_currency": "USD"}
    client.post('/api/auth/register', json=payload)
    token = client.post('/api/auth/login', json=payload).json()['access_token']
    return {"Authorization": f"Bearer {token}"}


def test_receipt_upload_and_list():
    client = TestClient(app)
    headers = auth_header(client)

    image = Image.new('RGB', (200, 100), color='white')
    out = BytesIO()
    image.save(out, format='PNG')
    out.seek(0)

    r = client.post('/api/receipts/upload', headers=headers, files={"file": ("receipt.png", out.getvalue(), "image/png")})
    assert r.status_code == 200
    body = r.json()
    assert 'receipt' in body
    assert 'transaction_draft' in body

    listed = client.get('/api/receipts', headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) >= 1

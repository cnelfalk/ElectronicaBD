import urllib.request
import json
import sys

def test_endpoint(url, expected_code=200):
    print(f"Testing URL: {url}")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            code = response.getcode()
            body = response.read().decode('utf-8')
            data = json.loads(body)
            print(f"Response code: {code}")
            if code == expected_code:
                print("  [OK] Status code matched.")
            else:
                print(f"  [FAIL] Expected status {expected_code}, got {code}")
            
            # Print a snippet of the response data
            print(f"  Response Success: {data.get('success')}")
            if 'mensaje' in data:
                print(f"  Message: {data['mensaje']}")
            if 'veredicto' in data:
                print(f"  Verdict: {data['veredicto']}")
            if 'ganador' in data:
                print(f"  Winner: {data['ganador']}")
            print("-" * 50)
            return True, data
    except urllib.error.HTTPError as e:
        code = e.getcode()
        body = e.read().decode('utf-8')
        try:
            data = json.loads(body)
        except Exception:
            data = {"raw": body}
        print(f"Response code: {code}")
        if code == expected_code:
            print("  [OK] Status code matched expected error.")
            if 'mensaje' in data:
                print(f"  Expected Error Message: {data['mensaje']}")
            print("-" * 50)
            return True, data
        else:
            print(f"  [FAIL] Expected status {expected_code}, got {code}")
            print(f"  Response body: {body}")
            print("-" * 50)
            return False, data
    except Exception as e:
        print(f"Connection/Other Error: {e}")
        print("-" * 50)
        return False, None

if __name__ == "__main__":
    print("=== STARTING API TESTS ===")
    
    # 1. Compare Laptops (ID 5 vs ID 10) - Gaming profile
    ok1, data1 = test_endpoint("http://127.0.0.1:5000/api/comparar?idA=5&idB=10&perfil=gaming", 200)
    
    # 2. Compare CPUs (ID 47 vs ID 48) - Gaming profile
    ok2, data2 = test_endpoint("http://127.0.0.1:5000/api/comparar?idA=47&idB=48&perfil=gaming", 200)
    
    # 3. Compare Laptop vs CPU (ID 5 vs ID 47) - Mismatched categories
    ok3, data3 = test_endpoint("http://127.0.0.1:5000/api/comparar?idA=5&idB=47", 400)
    
    if ok1 and ok2 and ok3:
        print("=== ALL API TESTS PASSED SUCCESSFULLY ===")
        sys.exit(0)
    else:
        print("=== SOME API TESTS FAILED ===")
        sys.exit(1)

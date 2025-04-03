from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_swift():
    data = request.json
    swift_code = data.get("code", "")
    expected_output = data.get("expected_output", "").strip()

    # Save Swift code to a file
    with open("temp.swift", "w") as file:
        file.write(swift_code)

    # Run the Swift file
    result = subprocess.run(["swift", "temp.swift"], capture_output=True, text=True)

    # Get actual output
    actual_output = result.stdout.strip()

    # Compare output with expected
    test_result = "Pass" if actual_output == expected_output else "Fail"

    return jsonify({
        "output": actual_output,
        "expected": expected_output,
        "result": test_result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

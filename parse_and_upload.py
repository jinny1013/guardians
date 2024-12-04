import json
import requests
import sys
import os

def parse_txt_to_json(txt_file):
    data = []
    with open(txt_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    current_item = {}
    for line in lines:
        line = line.strip()
        if line.startswith("U-"):
            if current_item:
                data.append(current_item)
            current_item = {"id": line.split(" ")[0]}
            importance_and_category = line.split("|")[0].split(" ", 1)
            if len(importance_and_category) > 1:
                current_item["importance"], category = importance_and_category
                current_item["category"], current_item["check_item"] = category.split(">", 1)
        elif line.startswith("결과:"):
            current_item["result"] = line.split(":", 1)[1].strip()
        elif line.startswith("상태:"):
            current_item["current_status"] = line.split(":", 1)[1].strip()

    if current_item:
        data.append(current_item)

    return data

def save_json_to_file(json_data, txt_file):
    # JSON 파일 이름 생성
    base_name = os.path.basename(txt_file)
    json_file = os.path.join("/tmp/results", f"{os.path.splitext(base_name)[0]}.json")
    
    # JSON 데이터 저장
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    
    print(f"JSON 파일 저장: {json_file}")
    return json_file

def upload_json(json_file, server_url):
    # JSON 파일 로드 후 업로드
    with open(json_file, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    response = requests.post(server_url, json=json_data, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        print("JSON 데이터 업로드 성공!")
    else:
        print(f"업로드 실패: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # 입력값: txt 파일과 서버 URL
    if len(sys.argv) < 3:
        print("사용법: python3 parse_and_upload.py <txt_file> <server_url>")
        sys.exit(1)

    txt_file = sys.argv[1]
    server_url = sys.argv[2]

    # TXT 파일 파싱 및 JSON 저장
    json_data = parse_txt_to_json(txt_file)
    json_file = save_json_to_file(json_data, txt_file)

    # Flask 서버로 업로드
    upload_json(json_file, server_url)

import json
import requests
import sys

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
            current_item["importance"], category = line.split("|")[0].split(" ")[1:]
            current_item["category"], current_item["check_item"] = category.split(">", 1)
        elif line.startswith("결과:"):
            current_item["result"] = line.split(":")[1].strip()
        elif line.startswith("상태:"):
            current_item["current_status"] = line.split(":")[1].strip()

    if current_item:
        data.append(current_item)

    return data

def upload_json(data, server_url):
    response = requests.post(server_url, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        print("JSON 데이터 업로드 성공!")
    else:
        print(f"업로드 실패: {response.status_code} - {response.text}")

if __name__ == "__main__":
    txt_file = sys.argv[1]  # txt 파일 경로
    server_url = sys.argv[2]  # 웹 서버 URL
    json_data = parse_txt_to_json(txt_file)
    upload_json(json_data, server_url)
